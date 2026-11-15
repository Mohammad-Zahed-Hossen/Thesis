from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import random
import torch
from PIL import Image
from typing import Tuple
from util import disk_cache, enable_disk_cache, cache_path, project_path

# Model Registry
MODEL_REGISTRY = {}

def register_model(name):
    def decorator(cls):
        MODEL_REGISTRY[name] = cls
        return cls
    return decorator

class Model(ABC):
    """Query a VLM on paired images and return scores and explanations."""

    def __init__(self, model_name: str = "unknown", revision=None, skip=False):
        self.model_name = model_name
        self.revision = revision
        self.skip = skip

    def __getstate__(self):
        return {
            "model_name": self.model_name,
            "revision": self.revision,
        }

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.skip:
            print("Skipping model inference.")
            return data
        data['scores_a'] = [[] for _ in range(len(data))]
        data['scores_b'] = [[] for _ in range(len(data))]
        data['explanation_a'] = ''
        data['explanation_b'] = ''
        filtered_data = data[data['error'] == False]
        tqdm.pandas(desc="Querying model")
        filtered_data = filtered_data.progress_apply(self.query_both, axis=1)
        data.update(filtered_data)
        return data

    @abstractmethod
    def query_both(self, example: pd.Series) -> pd.Series:
        """Queries the model with the given images and question. Enriches the pandas Series with label scores and explanations for both inputs.
        The input Series must contain the following keys:
          - 'image_a': Path to the first input image.
          - 'image_b': Path to the second input image.
          - 'question': The question to be answered.
          - 'labels': A list of possible answers.
          - 'task': "vqa" or "ve"
          - 'error': True if an error occurred and this example should be skipped in all subsequent steps, False otherwise.
          - 'reason': A description of the error that occurred, if any.
        The resulting dict additionally contains the following keys:
          - 'scores_a': A list of scores for each label for the first image.
          - 'scores_b': A list of scores for each label for the second image.
          - 'explanation_a': The explanation for the chosen label for the first image.
          - 'explanation_b': The explanation for the chosen label for the second image.
        """
        raise NotImplementedError("Implement in subclass")


@register_model("Random Mock")
class RandomMockModel(Model):

    def query_both(self, example: pd.Series) -> pd.Series:
        explanation_a = "This is a mock explanation A."
        explanation_b = "This is a mock explanation B " + random.choice([f"mentioning the changed object {example['changed']}.", "not mentioning the changed object."])
        return pd.Series({
            **example,
            "scores_a": self.random_scores(len(example['labels'])),
            "scores_b": self.random_scores(len(example['labels'])),
            "explanation_a": explanation_a,
            "explanation_b": explanation_b
        })

    def random_scores(self, num_labels: int) -> list:
        """Generate random scores for a given number of labels."""
        scores = [random.uniform(0, 1) for _ in range(num_labels)]
        # Softmax to make it a valid probability distribution
        scores = [s / sum(scores) for s in scores]
        return scores

@register_model("Perfect Mock")
class PerfectMockModel(Model):

    def __init__(self, **kwargs):
        super().__init__("baseline-perfect", **kwargs)
        self._mention_change = False

    def query_both(self, example: pd.Series) -> pd.Series:
        self._mention_change = not self._mention_change
        scores_a = [0.0 for _ in example['labels']]
        scores_a[0] = 1.0
        scores_b = [0.0 for _ in example['labels']]
        scores_b[1 if self._mention_change else 0] = 1.0
        explanation_a = "This is a mock explanation A."
        explanation_b = "This is a mock explanation B " + (f"mentioning the changed object {example['changed']}." if self._mention_change else "not mentioning the changed object.")
        return pd.Series({
            **example,
            "scores_a": scores_a,
            "scores_b": scores_b,
            "explanation_a": explanation_a,
            "explanation_b": explanation_b
        })


@register_model("ChatVLM")
class ChatVLM(Model):
    def __init__(self, prompt_mode="predict-then-explain", prompts_dir=None, device=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        # Defer loading model and processor until needed
        self.model = None
        self.processor = None
        self.prompt_mode = prompt_mode
        self.prompts_dir = Path(prompts_dir or project_path("prompts"))
        # self.prompt_vqa_explain_path = self.prompts_dir / ("model_pe_vqa_explain.txt" if prompt_mode == "predict-then-explain" else "model_ep_vqa_explain.txt")
        # self.prompt_vqa_answer_path = self.prompts_dir / ("model_pe_vqa_answer.txt" if prompt_mode == "predict-then-explain" else "model_ep_vqa_answer.txt")
        # self.prompt_ve_explain_path = self.prompts_dir / ("model_pe_ve_explain.txt" if prompt_mode == "predict-then-explain" else "model_ep_ve_explain.txt")
        # self.prompt_ve_answer_path = self.prompts_dir / ("model_pe_ve_answer.txt" if prompt_mode == "predict-then-explain" else "model_ep_ve_answer.txt")
        if prompt_mode == "predict-then-explain":
            self.prompt_vqa_explain_path = self.prompts_dir / "model_pe_vqa_explain.txt"
            self.prompt_vqa_answer_path = self.prompts_dir / "model_pe_vqa_answer.txt"
            self.prompt_ve_explain_path = self.prompts_dir / "model_pe_ve_explain.txt"
            self.prompt_ve_answer_path = self.prompts_dir / "model_pe_ve_answer.txt"
        elif prompt_mode == "explain-then-predict":
            self.prompt_vqa_explain_path = self.prompts_dir / "model_ep_vqa_explain.txt"
            self.prompt_vqa_answer_path = self.prompts_dir / "model_ep_vqa_answer.txt"
            self.prompt_ve_explain_path = self.prompts_dir / "model_ep_ve_explain.txt"
            self.prompt_ve_answer_path = self.prompts_dir / "model_ep_ve_answer.txt"
        elif prompt_mode == "chain-of-thought":
            self.prompt_vqa_explain_path = self.prompts_dir / "model_cot_vqa_reasoning.txt"
            self.prompt_vqa_answer_path = self.prompts_dir / "model_cot_vqa_answer.txt"
            self.prompt_ve_explain_path = self.prompts_dir / "model_cot_ve_reasoning.txt"
            self.prompt_ve_answer_path = self.prompts_dir / "model_cot_ve_answer.txt"
        elif prompt_mode == "reasoning-trace":
            assert "Qwen3" in self.model_name and "Thinking" in self.model_name, "Reasoning trace is only supported for Qwen3 thinking models."
            self.prompt_vqa_explain_path = self.prompts_dir / "model_pe_vqa_explain.txt"
            self.prompt_vqa_answer_path = self.prompts_dir / "model_rsn_vqa_answer.txt"
            self.prompt_ve_explain_path = self.prompts_dir / "model_pe_ve_explain.txt"
            self.prompt_ve_answer_path = self.prompts_dir / "model_rsn_ve_answer.txt"

        with open(self.prompt_vqa_explain_path, "r") as f:
            self.prompt_vqa_explain = f.read()
        with open(self.prompt_vqa_answer_path, "r") as f:
            self.prompt_vqa_answer = f.read()
        with open(self.prompt_ve_explain_path, "r") as f:
            self.prompt_ve_explain = f.read()
        with open(self.prompt_ve_answer_path, "r") as f:
            self.prompt_ve_answer = f.read()

    def __getstate__(self):
        return super().__getstate__() | {
            "prompt_mode": self.prompt_mode,
            "prompt_vqa_explain": self.prompt_vqa_explain,
            "prompt_vqa_answer": self.prompt_vqa_answer,
            "prompt_ve_explain": self.prompt_ve_explain,
            "prompt_ve_answer": self.prompt_ve_answer,
        }
    
    def query_both(self, example: pd.Series) -> pd.Series:
        error = example['error']
        reason = example['reason']
        scores_a, scores_b = [], []
        explanation_a, explanation_b = "", ""
        try:
            scores_a, explanation_a = self.query(example['image_a'], example['question'], example['labels'], example['task'])
            scores_b, explanation_b = self.query(example['image_b'], example['question'], example['labels'], example['task'])
        except AssertionError as e:
            print(f"Error querying model {self.model_name}: {str(e)}")
            error = True
            reason = f"Model: {str(e)}"
        return pd.Series({
            'error': error,
            'reason': reason,
            "scores_a": scores_a,
            "scores_b": scores_b,
            "explanation_a": explanation_a,
            "explanation_b": explanation_b
        })

    def query(self, image_path: str, question: str, labels: list, task: str) -> Tuple:
        """Process a VLM query and return response.
        For now this supports predict-then-explain only."""
        assert task in ["vqa", "ve"], f"Unknown task: {task}"
        image = Image.open(image_path)

        if self.prompt_mode == "predict-then-explain":
            return self.predict_then_explain(image, question, labels, task)
        elif self.prompt_mode == "explain-then-predict":
            return self.explain_then_predict(image, question, labels, task)
        elif self.prompt_mode == "chain-of-thought":
            return self.chain_of_thought(image, question, labels, task)
        elif self.prompt_mode == "reasoning-trace":
            return self.reasoning_trace(image, question, labels, task)
        else:
            raise ValueError(f"Unknown prompt mode: {self.prompt_mode}")

    @torch.no_grad()
    def reasoning_trace(self, image: Image, question: str, labels: list, task: str) -> Tuple:
        self._load_model()

        # 1. get the reasoning trace from the answer
        choices = ", ".join(labels[:-1]) + " or " + labels[-1]
        if task == "vqa":
            prompt_answer = self.prompt_vqa_answer.format(question=question, choices=choices)
        elif task == "ve":
            prompt_answer = self.prompt_ve_answer.format(hypothesis=question)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt_answer}
                ]
            },
        ]
        full_answer = self.explain(messages, max_new_tokens=1000, decode_skip_special_tokens=False)
        # print("Full answer with reasoning trace:\n", full_answer)
        # split everything between '<think>' and '</think>' as reasoning
        end_tag = "</think>"
        truncate_thinking_sequence = f"...\nI need to give the final answer now. I will only answer with {choices}\n</think>"
        reasoning_truncated = False
        if end_tag not in full_answer:
            full_answer += truncate_thinking_sequence  # ensure the ending tag is present
            reasoning_truncated = True
        end_idx = full_answer.find(end_tag)
        if end_idx != -1:
            explanation = full_answer[:end_idx].strip()
        else:
            explanation = "No reasoning trace found."

        # 2. get the scores for each answer candidate
        messages += [
            {
                "role": "assistant",
                "content": [{"type": "text", "text": explanation + end_tag}]
            }
        ]

        scores = self.score_labels(messages, labels, chain_of_thought=True)

        assert not any([s != s for s in scores]), f"Scores contain NaN: {scores}"
    
        if reasoning_truncated:
            explanation += "\n[Reasoning trace truncated due to length.]"

        return scores, explanation

    @torch.no_grad()
    def chain_of_thought(self, image: Image, question: str, labels: list, task: str) -> Tuple:
        self._load_model()

        cot_trigger = "Let's think step by step."
        skip_native_reasoning = "<think>\n\n</think>\n"

        if self.model_name == "YannQi/R-4B":
            # R-4B is actually a native reasoning model. For the classic CoT, we need to skip its native reasoning.
            cot_trigger = skip_native_reasoning + cot_trigger

        # 1. let the model think step by step
        choices = ", ".join(labels[:-1]) + " or " + labels[-1]
        if task == "vqa":
            prompt_reasoning = self.prompt_vqa_explain.format(question=question, choices=choices)
        elif task == "ve":
            prompt_reasoning = self.prompt_ve_explain.format(hypothesis=question)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt_reasoning}
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": cot_trigger}]
            }
        ]
        reasoning = self.explain(messages, chain_of_thought=True)

        # in some cases reasoning containes a '</think>' token. We only care about the text after that. (if any)
        if "</think>" in reasoning:
            reasoning = reasoning.split("</think>")[-1].strip()

        # 2. get the scores for each answer candidate
        if task == "vqa":
            prompt_answer = self.prompt_vqa_answer.format(choices=choices)
        elif task == "ve":
            prompt_answer = self.prompt_ve_answer

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt_reasoning}
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": cot_trigger + reasoning}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_answer}
                ]
            }
        ]

        scores = self.score_labels(messages, labels)

        assert not any([s != s for s in scores]), f"Scores contain NaN: {scores}"

        if self.model_name == "YannQi/R-4B":
            # remove the skip_native_reasoning prefix part from the reasoning
            # so we get the classical CoT style reasoning only
            cot_trigger = cot_trigger[len(skip_native_reasoning):]

        return scores, cot_trigger + reasoning

    @torch.no_grad()
    def explain_then_predict(self, image: Image, question: str, labels: list, task: str) -> Tuple:
        self._load_model()

        # 1. get the full text answer
        choices = ", ".join(labels[:-1]) + " or " + labels[-1]
        if task == "vqa":
            prompt_explain = self.prompt_vqa_explain.format(question=question, choices=choices)
        elif task == "ve":
            prompt_explain = self.prompt_ve_explain.format(hypothesis=question)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt_explain}
                ]
            },
        ]
        explanation = self.explain(messages)

        # 2. get the scores for each answer candidate
        if task == "vqa":
            prompt_answer = self.prompt_vqa_answer.format(choices=choices)
        elif task == "ve":
            prompt_answer = self.prompt_ve_answer

        messages += [
            {
                "role": "assistant",
                "content": [{"type": "text", "text": explanation}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_answer}
                ]
            }
        ]

        scores = self.score_labels(messages, labels)

        assert not any([s != s for s in scores]), f"Scores contain NaN: {scores}"

        return scores, explanation
    
    @torch.no_grad()
    def predict_then_explain(self, image: Image, question: str, labels: list, task: str) -> Tuple:
        self._load_model()

        # 1. get the scores for each answer candidate
        choices = ", ".join(labels[:-1]) + " or " + labels[-1]
        if task == "vqa":
            prompt_answer = self.prompt_vqa_answer.format(question=question, choices=choices)
        elif task == "ve":
            prompt_answer = self.prompt_ve_answer.format(hypothesis=question)

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt_answer}
                ]
            }
        ]

        scores = self.score_labels(messages, labels)

        max_score_label = labels[scores.index(max(scores))]

        assert not any([s != s for s in scores]), f"Scores contain NaN: {scores}"

        # 2. get the full text answer
        if task == "vqa":
            prompt_explain = self.prompt_vqa_explain.format(answer=max_score_label)
        elif task == "ve":
            prompt_explain = self.prompt_ve_explain.format(answer=max_score_label)
        messages += [
            {
                "role": "assistant",
                "content": [{"type": "text", "text": max_score_label}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt_explain}]
            }
        ]
        explanation = self.explain(messages)

        return scores, explanation

    @disk_cache(cache_path("ChatVLM-explain"))
    def explain(self, messages, chain_of_thought=False, max_new_tokens=512, decode_skip_special_tokens=True) -> str:
        """Generate explanation given the messages."""
        # print(messages)
        # print("Generating explanation...")
        # print("=" * 80)
        inputs = self.process_messages(messages, chain_of_thought=chain_of_thought)
        if "Ovis" in self.model_name:
            inputs['inputs'] = inputs.pop('input_ids')
            inputs.pop('attention_mask', None)
            output = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
            assert output[0].sum() != 0, "Generated ids are all zero!"
            full_text_answer = self.model.text_tokenizer.decode(output[0], skip_special_tokens=decode_skip_special_tokens)
        else:
            generated_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
            generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
            assert generated_ids_trimmed[0].sum() != 0, "Generated ids are all zero!"
            full_text_answer = self.processor.decode(generated_ids_trimmed[0], skip_special_tokens=decode_skip_special_tokens, clean_up_tokenization_spaces=False)
        return full_text_answer
    
    def score_labels(self, messages, labels, chain_of_thought=False):
        """Compute scores for each label given the messages.
        Labels will be formatted to lowercase.
        The prompt should ask the model to answer with lowercase labels only."""
        # print("Scoring labels...")
        # print("=" * 80)
        labels_lower = [label.lower() for label in labels]
        labels_tokenized = self.tokenize(labels_lower)
        scores = [1.0 for _ in labels]
        # iterate over the choices
        for i in range(len(labels)):
            inputs = self.process_messages(messages, chain_of_thought=chain_of_thought)
            # quit()
            # preprocess the input
            # iterate over the tokens of the label
            for token in labels_tokenized.input_ids[i]:
                # call the model to get the logits for the next token
                output = self.model(**inputs)
                # Get the logits for the next token
                logits = output.logits[:, -1, :]  # shape: [batch_size, vocab_size]
                # Softmax the logits to get probabilities
                # Use float32 so low-probability answer tokens do not round to
                # zero in bf16/fp16 before being converted to Python floats.
                probs = torch.softmax(logits.float(), dim=-1)
                # Multiply the score with the probability of the next token
                scores[i] *= probs[0, token].item()
                # Update the input with the next token
                inputs['input_ids'] = torch.cat([inputs['input_ids'], torch.tensor([[token]], device=self.device)], dim=1)
                inputs['attention_mask'] = torch.cat([inputs['attention_mask'], torch.ones((inputs['attention_mask'].shape[0], 1), device=self.device)], dim=1)
                if "mm_token_type_ids" in inputs:
                    inputs["mm_token_type_ids"] = torch.cat(
                        [
                            inputs["mm_token_type_ids"],
                            torch.zeros(
                                (inputs["mm_token_type_ids"].shape[0], 1),
                                device=self.device,
                                dtype=inputs["mm_token_type_ids"].dtype,
                            ),
                        ],
                        dim=1,
                    )
        return scores
    
    def tokenize(self, labels):
        """Tokenize the given labels using the processor's tokenizer."""
        if "Ovis" in self.model_name:
            # Ovis uses a different tokenizer interface
            tokens = self.model.text_tokenizer(labels)
        else:
            tokens = self.processor.tokenizer(labels)
        return tokens
    
    def process_messages(self, messages, chain_of_thought=False):
        image = next(msg["content"][0]["image"] for msg in messages if any(content["type"] == "image" for content in msg["content"]))
        if "Qwen3.5" in self.model_name:
            try:
                inputs = self.processor.apply_chat_template(
                    messages,
                    tokenize=True,
                    add_generation_prompt=not chain_of_thought,
                    return_dict=True,
                    return_tensors="pt",
                    enable_thinking=False,
                )
            except TypeError:
                inputs = self.processor.apply_chat_template(
                    messages,
                    tokenize=True,
                    add_generation_prompt=not chain_of_thought,
                    return_dict=True,
                    return_tensors="pt",
                )
            inputs = inputs.to(self.device)
        elif "Ovis" in self.model_name:
            input_ids, pixel_values, grid_thws = self.model.preprocess_inputs(
                messages=messages,
                add_generation_prompt=not chain_of_thought,
                enable_thinking=False,
            )
            inputs = {
                "pixel_values": pixel_values.to(self.device) if pixel_values is not None else None,
                "grid_thws": grid_thws.to(self.device) if grid_thws is not None else None,
                "input_ids": input_ids.to(self.device),
                "attention_mask": torch.ne(input_ids, self.model.text_tokenizer.pad_token_id).to(device=self.device),
                "enable_thinking": False,
            }
            # print("Prompt:")
            # print(self.model.text_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=not chain_of_thought))
        elif self.model_name == "YannQi/R-4B":
            # R-4B takes thinking mode as argument
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=not chain_of_thought, thinking_mode="short")
            # print("Processed text input:\n", text)
            inputs = self.processor(images=image, text=text, return_tensors="pt").to(self.device)
        else:
            # Works for QwenVL, InternVL and Kimi-VL
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=not chain_of_thought, return_dict=False)
            # print("Processed text input:\n", text)
            inputs = self.processor(text=text, images=[image], return_tensors="pt", padding=True).to(self.device)
        if chain_of_thought:
            # For chain-of-thought, we have to cut off the assistant message terminal part
            cutoff_length = 3 if self.model_name == "YannQi/R-4B" else 2
            inputs['input_ids'] = inputs['input_ids'][:, :-cutoff_length]
            inputs['attention_mask'] = inputs['attention_mask'][:, :-cutoff_length]
            if "mm_token_type_ids" in inputs:
                inputs["mm_token_type_ids"] = inputs["mm_token_type_ids"][:, :-cutoff_length]
        # if "Ovis" not in self.model_name:
            # print("Prompt:")
            # print(self.processor.tokenizer.batch_decode(inputs['input_ids'], skip_special_tokens=False)[0])
        return inputs


    def _load_model(self):
        if self.model is None or self.processor is None:
            from transformers import AutoProcessor
            import torch
            if "Qwen3.5" in self.model_name:
                from transformers import AutoModelForImageTextToText
                self.model = AutoModelForImageTextToText.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    torch_dtype=torch.bfloat16,
                    device_map=str(self.device),
                    attn_implementation="sdpa",
                )
                self.processor = AutoProcessor.from_pretrained(self.model_name, revision=self.revision, use_fast=True)
            elif "Qwen3" in self.model_name and "-A" in self.model_name:
                from transformers import Qwen3VLMoeForConditionalGeneration
                self.model = Qwen3VLMoeForConditionalGeneration.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    dtype=torch.float16,
                    device_map=self.device,
                )
                self.processor = AutoProcessor.from_pretrained(self.model_name, revision=self.revision, use_fast=True)
            elif "Qwen3" in self.model_name:
                from transformers import Qwen3VLForConditionalGeneration
                self.model = Qwen3VLForConditionalGeneration.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    dtype=torch.float16,
                    device_map=self.device,
                    attn_implementation="sdpa",
                )
                self.processor = AutoProcessor.from_pretrained(self.model_name, revision=self.revision, use_fast=True)
            elif "Qwen2.5" in self.model_name:
                from transformers import Qwen2_5_VLForConditionalGeneration
                self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    dtype=torch.float16,
                    device_map=self.device,
                )
                self.processor = AutoProcessor.from_pretrained(self.model_name, revision=self.revision, use_fast=True)
            elif "InternVL" in self.model_name:
                from transformers import InternVLForConditionalGeneration
                self.model = InternVLForConditionalGeneration.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    dtype=torch.float16,
                    device_map=self.device,
                )
                self.processor = AutoProcessor.from_pretrained(self.model_name, revision=self.revision, use_fast=True)
            elif "Ovis" in self.model_name:
                from transformers import AutoModelForCausalLM
                if not hasattr(torch.nn.Module, "is_parallelizable"):
                    torch.nn.Module.is_parallelizable = False
                try:
                    from transformers.models.qwen3.modeling_qwen3 import Qwen3ForCausalLM
                    if not hasattr(Qwen3ForCausalLM, "is_parallelizable"):
                        Qwen3ForCausalLM.is_parallelizable = False
                except Exception:
                    pass
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    torch_dtype=torch.bfloat16,
                    trust_remote_code=True
                ).to(self.device)
                self.processor = False # Ovis doesn't have a processor 
            elif self.model_name == "YannQi/R-4B":
                from transformers import AutoModel, AutoProcessor
                self.model = AutoModel.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    torch_dtype=torch.float32,
                    trust_remote_code=True,
                ).to(self.device)
                self.processor = AutoProcessor.from_pretrained(self.model_name, revision=self.revision, trust_remote_code=True)
            elif "Kimi-VL" in self.model_name:
                import torch
                import transformers.utils.import_utils as import_utils
                if not hasattr(import_utils, "is_torch_fx_available"):
                    import_utils.is_torch_fx_available = lambda: True
                from transformers import AutoConfig, AutoModelForCausalLM, AutoProcessor
                config = AutoConfig.from_pretrained(self.model_name, revision=self.revision, trust_remote_code=True)
                rope_scaling = getattr(config.text_config, "rope_scaling", None)
                if isinstance(rope_scaling, dict) and "type" not in rope_scaling and "rope_type" in rope_scaling:
                    rope_scaling["type"] = "linear" if rope_scaling["rope_type"] == "default" else rope_scaling["rope_type"]
                if isinstance(rope_scaling, dict) and "factor" not in rope_scaling:
                    rope_scaling["factor"] = 1.0
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    revision=self.revision,
                    config=config,
                    torch_dtype="auto",
                    device_map=self.device,
                    trust_remote_code=True,
                )
                self.processor = AutoProcessor.from_pretrained(self.model_name, revision=self.revision, trust_remote_code=True)
            else:
                raise ValueError(f"Unsupported model name: {self.model_name}")
    
    def _drop_model(self):
        if self.model is not None:
            del self.model
            self.model = None
        if self.processor is not None:
            del self.processor
            self.processor = None
        torch.cuda.empty_cache()

    def __call__(self, *args, **kwargs):
        if self.skip:
            return super().__call__(*args, **kwargs)
        try:
            self._load_model()
            return super().__call__(*args, **kwargs)
        finally:
            self._drop_model()
