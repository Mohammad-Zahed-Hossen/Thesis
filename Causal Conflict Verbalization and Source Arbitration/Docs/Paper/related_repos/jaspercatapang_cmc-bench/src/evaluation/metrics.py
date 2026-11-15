"""
CMC-Bench metrics: accuracy, modality_following_rate, MPB, HR, delta_acc.
All from observed answers. Helpers: match_image, match_text, abstention heuristic.
"""
import re
from collections import defaultdict
from typing import Any

from data.schema import Condition, condition_is_conflict


def _get_condition(r: Any) -> Condition | str:
    c = getattr(r, "condition", r.get("condition"))
    if isinstance(c, Condition):
        return c
    return c if isinstance(c, str) else Condition.ALIGNED


def _is_conflict_record(r: Any) -> bool:
    c = _get_condition(r)
    if isinstance(c, Condition):
        return condition_is_conflict(c)
    return c not in ("aligned",)


def _normalize_answer(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[,.]", "", s)
    return s


def _numeric_close(pred: str, gold: str, rel_tol: float = 0.05) -> bool:
    def to_num(x: str) -> float | None:
        x = re.sub(r"[%\s]", "", x)
        try:
            return float(x)
        except ValueError:
            return None

    a, b = to_num(pred), to_num(gold)
    if a is not None and b is not None and b != 0:
        return abs(a - b) / abs(b) <= rel_tol
    if a is not None and b is not None:
        return abs(a - b) < 1e-6
    return False


def answer_correct(pred: str, gold: str, fuzzy_numeric: bool = True) -> bool:
    """True if pred matches gold (exact normalized or fuzzy numeric)."""
    p, g = _normalize_answer(pred), _normalize_answer(gold)
    if p == g:
        return True
    if fuzzy_numeric and _numeric_close(pred, gold):
        return True
    return False


def is_abstention(pred: str) -> bool:
    """Heuristic: answer suggests abstention / neither / cannot determine."""
    if not pred or len(pred.strip()) < 4:
        return True
    p = pred.strip().lower()
    phrases = (
        "don't know",
        "do not know",
        "cannot determine",
        "can't determine",
        "unclear",
        "conflict",
        "contradict",
        "disagree",
        "disagreement",
        "cannot tell",
        "can't tell",
        "not sure",
        "insufficient",
        "ambiguous",
    )
    return any(phrase in p for phrase in phrases)


def compute_matches(
    records: list,
    predictions: list[dict],
    key_instance: str = "instance_id",
    key_answer: str = "answer",
) -> list[dict]:
    """
    For each (record, pred): compute matches_image, matches_text, matches_neither, flags_disagreement.
    Records have instance_id, gold_answer, text_answer, condition.
    """
    pred_map = {p[key_instance]: p for p in predictions}
    rec_map = {}
    for r in records:
        inst = getattr(r, "instance_id", r.get("instance_id"))
        rec_map[inst] = r

    out = []
    for inst, pred in pred_map.items():
        rec = rec_map.get(inst)
        if rec is None:
            continue
        gold = getattr(rec, "gold_answer", rec.get("gold_answer", ""))
        text_ans = getattr(rec, "text_answer", rec.get("text_answer", ""))
        ans = pred.get(key_answer, "")
        cond = _get_condition(rec)
        cond_str = cond.value if isinstance(cond, Condition) else str(cond)

        matches_image = answer_correct(ans, gold)
        matches_text = answer_correct(ans, text_ans)
        matches_neither = not matches_image and not matches_text
        flags_disagreement = is_abstention(ans)

        out.append({
            "instance_id": inst,
            "model": pred.get("model", ""),
            "condition": cond_str,
            "answer": ans,
            "matches_image": matches_image,
            "matches_text": matches_text,
            "matches_neither": matches_neither,
            "flags_disagreement": flags_disagreement,
        })
    return out


def compute_accuracy(
    records: list,
    predictions: list[dict],
    key_instance: str = "instance_id",
    key_pred: str = "answer",
    key_gold: str = "gold_answer",
) -> dict[str, float]:
    """Accuracy per condition: fraction matching gold."""
    by_condition: dict[str, list[tuple[str, str]]] = defaultdict(list)
    pred_map = {p[key_instance]: p.get(key_pred, "") for p in predictions}
    for r in records:
        inst = getattr(r, "instance_id", r.get("instance_id"))
        gold = getattr(r, "gold_answer", r.get(key_gold, ""))
        cond = _get_condition(r)
        cond_str = cond.value if isinstance(cond, Condition) else str(cond)
        pred = pred_map.get(inst, "")
        by_condition[cond_str].append((pred, gold))
    acc = {}
    for cond, pairs in by_condition.items():
        if not pairs:
            acc[cond] = 0.0
            continue
        correct = sum(1 for p, g in pairs if answer_correct(p, g))
        acc[cond] = correct / len(pairs)
    return acc


def compute_modality_following_rate(
    records: list,
    behavioral_list: list[dict],
) -> float:
    """
    In conflict conditions: fraction siding with correct modality.
    Image-correct -> matches_image; text-correct -> matches_text; both-wrong -> matches_neither or flags_disagreement.
    """
    rec_map = {getattr(r, "instance_id", r.get("instance_id")): r for r in records}
    conflict_preds = []
    for b in behavioral_list:
        rec = rec_map.get(b["instance_id"])
        if rec is None:
            continue
        if not _is_conflict_record(rec):
            continue
        conflict_preds.append((rec, b))

    if not conflict_preds:
        return 0.0
    detected = 0
    for rec, b in conflict_preds:
        cond = _get_condition(rec)
        cond_str = cond.value if isinstance(cond, Condition) else str(cond)
        if cond_str == Condition.IMAGE_CORRECT.value:
            if b.get("matches_image"):
                detected += 1
        elif cond_str == Condition.TEXT_CORRECT.value:
            if b.get("matches_text"):
                detected += 1
        elif cond_str == Condition.BOTH_WRONG.value:
            if b.get("matches_neither") or b.get("flags_disagreement"):
                detected += 1
    return detected / len(conflict_preds)


def compute_mpb(records: list, behavioral_list: list[dict]) -> tuple[float, float]:
    """Among conflict cases: proportion following image vs text."""
    rec_map = {getattr(r, "instance_id", r.get("instance_id")): r for r in records}
    side_image, side_text = 0, 0
    for b in behavioral_list:
        rec = rec_map.get(b["instance_id"])
        if rec is None or not _is_conflict_record(rec):
            continue
        if b.get("matches_image"):
            side_image += 1
        elif b.get("matches_text"):
            side_text += 1
    n = side_image + side_text
    if n == 0:
        return 0.0, 0.0
    return side_image / n, side_text / n


def compute_hr(records: list, behavioral_list: list[dict]) -> float:
    """Hallucination rate on conflict conditions: responses that neither align with
    either source nor commit to one, covering both unsupported fabrication (NEITHER)
    and explicit refusal (ABSTAIN). Equals ConfabR + CDR (paper Eq. for HR)."""
    rec_map = {getattr(r, "instance_id", r.get("instance_id")): r for r in records}
    conflict_with_pred = [(rec_map.get(b["instance_id"]), b) for b in behavioral_list]
    conflict_with_pred = [(r, b) for r, b in conflict_with_pred if r and _is_conflict_record(r)]
    if not conflict_with_pred:
        return 0.0
    hallucinated = sum(
        1 for _, b in conflict_with_pred
        if b.get("matches_neither") or b.get("flags_disagreement")
    )
    return hallucinated / len(conflict_with_pred)


def compute_confab_and_cdr(
    records: list,
    behavioral_list: list[dict],
) -> tuple[float, float]:
    """ConfabR (NEITHER only) and CDR (ABSTAIN) on conflict trials.

    A response can satisfy both ``matches_neither`` and ``flags_disagreement`` (e.g. a short
    answer containing the word "unclear"). The ABSTAIN bucket takes precedence so that
    HR = ConfabR + CDR holds without double counting.
    """
    rec_map = {getattr(r, "instance_id", r.get("instance_id")): r for r in records}
    conflict_bl = [
        b for b in behavioral_list
        if (rec_map.get(b["instance_id"]) is not None
            and _is_conflict_record(rec_map[b["instance_id"]]))
    ]
    n = len(conflict_bl) or 1
    confab_r = sum(
        1 for b in conflict_bl
        if b.get("matches_neither") and not b.get("flags_disagreement")
    ) / n
    cdr = sum(1 for b in conflict_bl if b.get("flags_disagreement")) / n
    return confab_r, cdr


def compute_delta_acc(acc_by_condition: dict[str, float]) -> float:
    """Aligned accuracy minus mean conflict-condition accuracy."""
    aligned = acc_by_condition.get("aligned", 0.0)
    conflict_conds = [
        Condition.IMAGE_CORRECT.value,
        Condition.TEXT_CORRECT.value,
        Condition.BOTH_WRONG.value,
    ]
    conflict_accs = [acc_by_condition.get(c, 0.0) for c in conflict_conds]
    if not conflict_accs:
        return 0.0
    return aligned - (sum(conflict_accs) / len(conflict_accs))


def compute_accuracy_from_behavioral(
    records: list,
    behavioral_list: list[dict],
) -> dict[str, float]:
    """Per-condition accuracy from judge-derived flags.

    Image-correct  : IMAGE or BOTH
    Text-correct   : TEXT or BOTH
    Aligned        : IMAGE, TEXT, or BOTH
    Both-wrong     : NEITHER or ABSTAIN (i.e. matches_neither or flags_disagreement)
    """
    bmap = {b["instance_id"]: b for b in behavioral_list}
    sums: dict[str, tuple[int, int]] = defaultdict(lambda: (0, 0))
    for r in records:
        inst = getattr(r, "instance_id", r.get("instance_id"))
        cond = _get_condition(r)
        cond_str = cond.value if isinstance(cond, Condition) else str(cond)
        b = bmap.get(inst)
        if b is None:
            continue
        if cond_str == Condition.IMAGE_CORRECT.value:
            is_correct = b.get("matches_image") or b.get("matches_both", False)
        elif cond_str == Condition.TEXT_CORRECT.value:
            is_correct = b.get("matches_text") or b.get("matches_both", False)
        elif cond_str == Condition.BOTH_WRONG.value:
            is_correct = b.get("matches_neither") or b.get("flags_disagreement")
        else:  # aligned
            is_correct = (
                b.get("matches_image")
                or b.get("matches_text")
                or b.get("matches_both", False)
            )
        correct, total = sums[cond_str]
        sums[cond_str] = (correct + (1 if is_correct else 0), total + 1)
    return {c: num / den if den else 0.0 for c, (num, den) in sums.items()}


def compute_all_metrics_from_judge(
    records: list,
    behavioral_list: list[dict],
    model_name: str = "",
) -> dict[str, Any]:
    """Judge-derived metrics: Acc per condition, MFR, MPB, ConfabR, CDR, HR=ConfabR+CDR, ΔAcc."""
    for b in behavioral_list:
        b["model"] = b.get("model", model_name)
    acc = compute_accuracy_from_behavioral(records, behavioral_list)
    mfr = compute_modality_following_rate(records, behavioral_list)
    mpb_img, mpb_txt = compute_mpb(records, behavioral_list)
    delta = compute_delta_acc(acc)
    confab_r, cdr = compute_confab_and_cdr(records, behavioral_list)
    return {
        "accuracy": acc,
        "modality_following_rate": mfr,
        "conflict_detection_rate": cdr,
        "confabulation_rate": confab_r,
        "hallucination_rate": confab_r + cdr,
        "modality_preference_image": mpb_img,
        "modality_preference_text": mpb_txt,
        "accuracy_drop": delta,
    }


def compute_all_metrics(
    records: list,
    predictions: list[dict],
    model_name: str = "",
) -> dict[str, Any]:
    """Returns accuracy (per cond), modality_following_rate, conflict_detection_rate, mpb, hr, accuracy_drop."""
    for p in predictions:
        p["model"] = p.get("model", model_name)
    acc = compute_accuracy(records, predictions)
    behavioral = compute_matches(records, predictions)
    mfr = compute_modality_following_rate(records, behavioral)
    mpb_img, mpb_txt = compute_mpb(records, behavioral)
    hr = compute_hr(records, behavioral)
    confab_r, cdr = compute_confab_and_cdr(records, behavioral)
    delta = compute_delta_acc(acc)
    return {
        "accuracy": acc,
        "modality_following_rate": mfr,
        "conflict_detection_rate": cdr,
        "confabulation_rate": confab_r,
        "modality_preference_image": mpb_img,
        "modality_preference_text": mpb_txt,
        "hallucination_rate": hr,
        "accuracy_drop": delta,
    }
