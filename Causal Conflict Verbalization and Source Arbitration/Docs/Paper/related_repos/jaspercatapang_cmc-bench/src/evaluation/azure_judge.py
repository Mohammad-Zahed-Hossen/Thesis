"""Remote chat judge for CMC-Bench (OpenAI-compatible client, e.g. Azure OpenAI): strict JSON label → normalized flags."""
from __future__ import annotations

import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Any

from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncAzureOpenAI, AzureOpenAI, OpenAIError

from evaluation.judge_constants import JUDGE_PROMPT_VERSION

ALLOWED_LABELS: frozenset[str] = frozenset({"IMAGE", "TEXT", "BOTH", "NEITHER", "ABSTAIN"})
ALLOWED_LABELS_DOC = ", ".join(sorted(ALLOWED_LABELS))

_STRICT_SYSTEM = """You are a deterministic scoring function, not an assistant.

Hard rules:
1) Your entire message must be exactly one JSON object. Nothing before or after it.
2) The JSON object must contain exactly one key: "label". No other keys. No "notes", no "reasoning", no arrays, no nesting.
3) The value of "label" must be exactly one of these five strings (uppercase, ASCII): """ + ALLOWED_LABELS_DOC + """.
4) Do not use markdown, code fences, backticks, or the word "json".
5) Output must be parseable by JSON.parse with no changes."""

_STRICT_USER_TEMPLATE = """You assign exactly one label to model_answer using the references below.

Label definitions (mutually exclusive — output exactly one):

- IMAGE: The model gives a substantive answer that matches image_reference. If image_reference and text_reference disagree, the model must match image_reference and not match text_reference.
- TEXT: The model gives a substantive answer that matches text_reference. If the two references disagree, the model must match text_reference and not match image_reference.
- BOTH: The model gives a substantive answer that matches image_reference and text_reference (including when the two references are identical).
- NEITHER: The model gives a substantive factual claim that matches neither image_reference nor text_reference (a third, incorrect, or unrelated answer). The model is not merely refusing — it commits to content that fails both references.
- ABSTAIN: The model does not commit to a substantive answer aligned with either reference: explicit refusal, cannot determine, only meta-commentary about conflict/modality, empty or non-answer, or no extractable factual claim comparable to the references.

Matching rules (same for image vs text):
- Treat paraphrase and trivial formatting differences (case, whitespace, punctuation) as the same answer when the meaning is the same.
- For numeric answers: treat as matching if the values are the same within 5% relative error when both are numeric; otherwise exact normalized string equality after lowercasing and collapsing whitespace.
- If the model hedges between references without clearly endorsing one side when references conflict, use ABSTAIN, not BOTH.
- If unsure between NEITHER and ABSTAIN: if there is any clear factual claim that is wrong vs both references, use NEITHER; if there is no clear factual commitment, use ABSTAIN.

Inputs:
condition (metadata only): {condition}
question: {query}
image_reference: {gold_answer}
text_reference: {text_answer}
model_answer: {model_answer}

Required output (replace LABEL with one of {allowed}; keep this exact shape):
{{"label":"LABEL"}}"""


def load_env_file(path: Path, *, override: bool = False) -> None:
    """Load KEY=VALUE lines into os.environ (no python-dotenv)."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if not k:
            continue
        if override or k not in os.environ:
            os.environ[k] = v


def azure_config_from_env() -> dict[str, str]:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    if not endpoint or not key or not deployment:
        raise ValueError(
            "Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT "
            "(optional: AZURE_OPENAI_API_VERSION, default 2024-02-15-preview)"
        )
    return {
        "endpoint": endpoint,
        "key": key,
        "deployment": deployment,
        "api_version": api_version,
    }


def _azure_openai_client(cfg: dict[str, str], timeout_s: float) -> AzureOpenAI:
    return AzureOpenAI(
        api_version=cfg["api_version"],
        azure_endpoint=cfg["endpoint"],
        api_key=cfg["key"],
        timeout=timeout_s,
    )


def _async_azure_openai_client(cfg: dict[str, str], timeout_s: float) -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        api_version=cfg["api_version"],
        azure_endpoint=cfg["endpoint"],
        api_key=cfg["key"],
        timeout=timeout_s,
    )


def create_async_azure_client(timeout_s: float = 120.0) -> AsyncAzureOpenAI:
    """Shared async client for concurrent judge calls (use as ``async with client:``)."""
    return _async_azure_openai_client(azure_config_from_env(), timeout_s)


def _clip_text(s: str, max_chars: int) -> str:
    s = str(s)
    if len(s) <= max_chars:
        return s
    return s[: max_chars - 3] + "..."


def _judge_user_prompt(
    *,
    query: str,
    gold_answer: str,
    text_answer: str,
    model_answer: str,
    condition: str,
    max_chars: int,
) -> str:
    return _STRICT_USER_TEMPLATE.format(
        condition=_clip_text(str(condition), max_chars),
        query=_clip_text(query, max_chars),
        gold_answer=_clip_text(gold_answer, max_chars),
        text_answer=_clip_text(text_answer, max_chars),
        model_answer=_clip_text(model_answer, max_chars),
        allowed=ALLOWED_LABELS_DOC,
    )


def _judge_request_kwargs(
    cfg: dict[str, str],
    *,
    max_completion_tokens: int,
    temperature: float | None,
    use_json_object_mode: bool,
    query: str,
    gold_answer: str,
    text_answer: str,
    model_answer: str,
    condition: str,
    max_chars: int,
) -> dict[str, Any]:
    user = _judge_user_prompt(
        query=query,
        gold_answer=gold_answer,
        text_answer=text_answer,
        model_answer=model_answer,
        condition=condition,
        max_chars=max_chars,
    )
    kwargs: dict[str, Any] = {
        "model": cfg["deployment"],
        "messages": [
            {"role": "system", "content": _STRICT_SYSTEM},
            {"role": "user", "content": user},
        ],
        "max_completion_tokens": max_completion_tokens,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    if use_json_object_mode:
        kwargs["response_format"] = {"type": "json_object"}
    return kwargs


_JSON_BLOCK = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)


def _strip_surrounding_noise(s: str) -> str:
    t = s.strip()
    m = _JSON_BLOCK.search(t)
    if m:
        t = m.group(1).strip()
    return t


def _parse_strict_label_object(text: str) -> str:
    """Parse model output; return normalized UPPERCASE label. Fails on extra keys or invalid label."""
    if not text or not text.strip():
        raise ValueError("empty judge content")
    t = _strip_surrounding_noise(text)
    try:
        obj = json.loads(t)
    except json.JSONDecodeError:
        start, end = t.find("{"), t.rfind("}")
        if start == -1 or end <= start:
            raise ValueError(f"no JSON object in judge output: {t[:240]!r}") from None
        obj = json.loads(t[start : end + 1])
    if not isinstance(obj, dict):
        raise ValueError(f"judge output must be a JSON object, got {type(obj).__name__}")
    keys = set(obj.keys())
    if keys != {"label"}:
        raise ValueError(f"judge JSON must have exactly key 'label', got keys {sorted(keys)}")
    raw = obj["label"]
    if not isinstance(raw, str):
        raise ValueError(f"label must be a string, got {type(raw).__name__}")
    label = raw.strip().upper()
    if label not in ALLOWED_LABELS:
        raise ValueError(f"label must be one of {sorted(ALLOWED_LABELS)}, got {raw!r}")
    return label


def label_to_flags(label: str) -> dict[str, bool]:
    """Map closed-set label to metrics booleans (deterministic)."""
    if label == "IMAGE":
        return {"matches_image": True, "matches_text": False, "abstains": False}
    if label == "TEXT":
        return {"matches_image": False, "matches_text": True, "abstains": False}
    if label == "BOTH":
        return {"matches_image": True, "matches_text": True, "abstains": False}
    if label == "NEITHER":
        return {"matches_image": False, "matches_text": False, "abstains": False}
    if label == "ABSTAIN":
        return {"matches_image": False, "matches_text": False, "abstains": True}
    raise ValueError(f"unknown label: {label!r}")


def _message_content_to_str(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for p in content:
            if isinstance(p, dict) and p.get("type") == "text":
                parts.append(str(p.get("text", "")))
        return "".join(parts)
    return str(content)


def _completion_to_judge_dict(completion: Any) -> dict[str, Any]:
    choices = completion.choices or []
    if not choices:
        raise ValueError(f"no choices in response: {completion!r}")
    msg = choices[0].message
    content_str = _message_content_to_str(getattr(msg, "content", None))
    label = _parse_strict_label_object(content_str)
    flags = label_to_flags(label)
    return {
        "judge_label": label,
        "judge_prompt_version": JUDGE_PROMPT_VERSION,
        "matches_image": flags["matches_image"],
        "matches_text": flags["matches_text"],
        "abstains": flags["abstains"],
        "raw_content": content_str[:2000],
    }


def judge_row(
    *,
    query: str,
    gold_answer: str,
    text_answer: str,
    model_answer: str,
    condition: str,
    max_chars: int = 4000,
    max_completion_tokens: int = 2048,
    temperature: float | None = None,
    timeout_s: float = 120.0,
    use_json_object_mode: bool = True,
) -> dict[str, Any]:
    """
    Call Azure chat completions; return normalized flags plus canonical judge_label.

    The model must return only {{"label": "..."}} with label in ALLOWED_LABELS.
    """
    cfg = azure_config_from_env()
    client = _azure_openai_client(cfg, timeout_s)
    kwargs = _judge_request_kwargs(
        cfg,
        max_completion_tokens=max_completion_tokens,
        temperature=temperature,
        use_json_object_mode=use_json_object_mode,
        query=query,
        gold_answer=gold_answer,
        text_answer=text_answer,
        model_answer=model_answer,
        condition=condition,
        max_chars=max_chars,
    )
    completion = client.chat.completions.create(**kwargs)
    return _completion_to_judge_dict(completion)


def judge_row_with_retries(
    *,
    max_retries: int = 5,
    base_sleep_s: float = 1.0,
    **kwargs: Any,
) -> dict[str, Any]:
    last: Exception | None = None
    use_json = kwargs.pop("use_json_object_mode", True)
    for attempt in range(max_retries):
        try:
            return judge_row(**kwargs, use_json_object_mode=use_json)
        except APIStatusError as e:
            last = e
            code = getattr(e, "status_code", None)
            if use_json and code == 400:
                use_json = False
                continue
            if code in (429, 500, 502, 503) and attempt < max_retries - 1:
                time.sleep(base_sleep_s * (2**attempt))
                continue
            raise
        except (APIConnectionError, APITimeoutError) as e:
            last = e
            if attempt < max_retries - 1:
                time.sleep(base_sleep_s * (2**attempt))
                continue
            raise
        except (json.JSONDecodeError, ValueError) as e:
            last = e
            if attempt < max_retries - 1:
                time.sleep(base_sleep_s * (2**attempt))
                continue
            raise
        except OpenAIError as e:
            last = e
            if attempt < max_retries - 1:
                time.sleep(base_sleep_s * (2**attempt))
                continue
            raise
    assert last is not None
    raise last


async def async_judge_row(
    *,
    client: AsyncAzureOpenAI,
    query: str,
    gold_answer: str,
    text_answer: str,
    model_answer: str,
    condition: str,
    max_chars: int = 4000,
    max_completion_tokens: int = 2048,
    temperature: float | None = None,
    use_json_object_mode: bool = True,
) -> dict[str, Any]:
    cfg = azure_config_from_env()
    kwargs = _judge_request_kwargs(
        cfg,
        max_completion_tokens=max_completion_tokens,
        temperature=temperature,
        use_json_object_mode=use_json_object_mode,
        query=query,
        gold_answer=gold_answer,
        text_answer=text_answer,
        model_answer=model_answer,
        condition=condition,
        max_chars=max_chars,
    )
    completion = await client.chat.completions.create(**kwargs)
    return _completion_to_judge_dict(completion)


async def async_judge_row_with_retries(
    *,
    client: AsyncAzureOpenAI,
    max_retries: int = 5,
    base_sleep_s: float = 1.0,
    **kwargs: Any,
) -> dict[str, Any]:
    last: Exception | None = None
    use_json = kwargs.pop("use_json_object_mode", True)
    for attempt in range(max_retries):
        try:
            return await async_judge_row(**kwargs, client=client, use_json_object_mode=use_json)
        except APIStatusError as e:
            last = e
            code = getattr(e, "status_code", None)
            if use_json and code == 400:
                use_json = False
                continue
            if code in (429, 500, 502, 503) and attempt < max_retries - 1:
                await asyncio.sleep(base_sleep_s * (2**attempt))
                continue
            raise
        except (APIConnectionError, APITimeoutError) as e:
            last = e
            if attempt < max_retries - 1:
                await asyncio.sleep(base_sleep_s * (2**attempt))
                continue
            raise
        except (json.JSONDecodeError, ValueError) as e:
            last = e
            if attempt < max_retries - 1:
                await asyncio.sleep(base_sleep_s * (2**attempt))
                continue
            raise
        except OpenAIError as e:
            last = e
            if attempt < max_retries - 1:
                await asyncio.sleep(base_sleep_s * (2**attempt))
                continue
            raise
    assert last is not None
    raise last
