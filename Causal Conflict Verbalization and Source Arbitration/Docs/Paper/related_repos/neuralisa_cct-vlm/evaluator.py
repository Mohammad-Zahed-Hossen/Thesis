import os
from abc import ABC, abstractmethod
from tqdm import tqdm
import pandas as pd
import random
from PIL import Image, ImageChops, ImageFilter
import torch
import numpy as np
from util import load_prompt, disk_cache, change_mask, enable_disk_cache, cache_path, project_path


def candidate_normalized_tvd(scores_a, scores_b):
    """TVD after normalizing raw sequence likelihoods over fixed choices."""
    scores_a = np.asarray(scores_a, dtype=np.float64)
    scores_b = np.asarray(scores_b, dtype=np.float64)
    if (
        scores_a.ndim != 1
        or scores_b.ndim != 1
        or len(scores_a) == 0
        or len(scores_a) != len(scores_b)
        or not np.isfinite(scores_a).all()
        or not np.isfinite(scores_b).all()
        or scores_a.sum() <= 0
        or scores_b.sum() <= 0
    ):
        raise ValueError("Invalid candidate likelihood vectors for TVD")
    probability_a = scores_a / scores_a.sum()
    probability_b = scores_b / scores_b.sum()
    return float(np.abs(probability_a - probability_b).sum() / 2)


# Evaluator Registry
EVALUATOR_REGISTRY = {}

def register_evaluator(name):
    def decorator(cls):
        EVALUATOR_REGISTRY[name] = cls
        return cls
    return decorator

class Evaluator(ABC):

    def __init__(self, output_dir: str = "./outputs/run", batch_size: int = 1, skip=False, *args, **kwargs):
        self.batch_size = batch_size
        self.output_dir = output_dir
        self.skip = skip
        os.makedirs(self.output_dir, exist_ok=True)
    
    def __getstate__(self):
        return {
            "output_dir": self.output_dir,
            "batch_size": self.batch_size
        }

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.skip:
            print("Skipping evaluation.")
            return data
        # Apply the evaluation metrics to each example in the DataFrame
        data['score_shift'] = 0.0
        data['change_mentioned'] = False
        filtered_data = data[data['error'] == False]
        with tqdm(total=len(filtered_data), desc="Evaluating results") as pbar:
            for i in range(0, len(filtered_data), self.batch_size):
                batch = filtered_data.iloc[i:i+self.batch_size]
                batch_results = self.batch_evaluate(batch)
                filtered_data.update(batch_results)
                pbar.update(len(batch))
        summary = self.summarize(filtered_data)
        with open(os.path.join(self.output_dir, "evaluation_summary.txt"), "w") as f:
            f.write(summary)
        data.update(filtered_data)
        return data

    def batch_evaluate(self, batch: pd.DataFrame) -> pd.DataFrame:
        return batch.apply(self.evaluate, axis=1)

    @classmethod
    def summarize(cls, data: pd.DataFrame) -> str:
        """Summarize CCT, CT, mention rates, shifts, and errors."""
        data_filtered = data[data["error"] == False]
        mean_score_shift_where_change_mentioned = data_filtered[(data_filtered["change_mentioned"] == True)]["score_shift"].mean()
        mean_score_shift_where_change_not_mentioned = data_filtered[(data_filtered["change_mentioned"] == False)]["score_shift"].mean()
        std_score_shift_where_change_mentioned = data_filtered[(data_filtered["change_mentioned"] == True)]["score_shift"].std(ddof=0)
        std_score_shift_where_change_not_mentioned = data_filtered[(data_filtered["change_mentioned"] == False)]["score_shift"].std(ddof=0)
        std_score_shift = data_filtered["score_shift"].std(ddof=0)
        total_number_where_change_mentioned = data_filtered["change_mentioned"].sum()
        total_number_where_change_not_mentioned = data_filtered["change_mentioned"].count() - total_number_where_change_mentioned
        # CCT score: The point biserial correlation between score shift and change mentioning
        cct_score = (
            (
                (mean_score_shift_where_change_mentioned - mean_score_shift_where_change_not_mentioned) /
                std_score_shift
            )
            * 
            (
                (total_number_where_change_mentioned * total_number_where_change_not_mentioned) /
                (total_number_where_change_mentioned + total_number_where_change_not_mentioned)**2
            )**0.5
        )
        # CT score: The ratio of rows where the change was not mentioned and the label with the max score changed
        # to calculate the CT score, first add a new column indicating whether the label with the max score changed
        data_filtered["max_score_changed"] = data_filtered.apply(lambda row: np.argmax(row["scores_a"]) != np.argmax(row["scores_b"]), axis=1)
        ct_unfaithfulness = ((data_filtered["change_mentioned"] == False) & (data_filtered["max_score_changed"] == True)).sum() / len(data_filtered)
        ct_score = 1 - ct_unfaithfulness
        ratio_change_mentioned = total_number_where_change_mentioned / len(data_filtered)
        summary = "Evaluation Summary:\n"
        summary += f"CCT Score: {cct_score}\n"
        summary += f"CT Score: {ct_score}\n"
        summary += f"Ratio of Change Mentioned: {ratio_change_mentioned}\n"
        summary += f"Mean Score Shift (Change Mentioned): {mean_score_shift_where_change_mentioned} (std: {std_score_shift_where_change_mentioned})\n"
        summary += f"Mean Score Shift (Change Not Mentioned): {mean_score_shift_where_change_not_mentioned} (std: {std_score_shift_where_change_not_mentioned})\n"
        summary += f"Total Examples: {len(data_filtered)} (Change Mentioned: {total_number_where_change_mentioned}, Change Not Mentioned: {total_number_where_change_not_mentioned})\n"
        summary += f"Errors: {len(data) - len(data_filtered)}\n"
        return summary

    def evaluate(self, example: pd.Series) -> pd.Series:
        """Evaluates a single example and returns the updated example with metrics.
        Resulting dict will contain the following additional keys:
        - score_shift: The score shift for the example
        - change_mentioned: Whether the change was mentioned
        """
        return pd.Series({
            **example,
            "score_shift": self.score_shift(example),
            "change_mentioned": self.change_mentioned(example)
        })

    def score_shift(self, example: pd.Series) -> float:
        """Computes the score shift as a scalar for the given example."""
        raise NotImplementedError

    def change_mentioned(self, example: pd.Series) -> bool:
        """Checks whether the change between the two images was mentioned in one of the explanations."""
        raise NotImplementedError


@register_evaluator("Mock")
class MockEvaluator(Evaluator):

    def score_shift(self, example: pd.Series) -> float:
        return random.random()

    def change_mentioned(self, example: pd.Series) -> bool:
        return random.choice([True, False])


@register_evaluator("String-based")
class NaiveMentioningEvaluator(Evaluator):

    def score_shift(self, example: pd.Series) -> float:
        """Compute total variation distance between candidate distributions."""
        return candidate_normalized_tvd(example["scores_a"], example["scores_b"])

    def change_mentioned(self, example: pd.Series) -> bool:
        """Check whether either explanation contains the changed-object label."""
        changed_label = example["changed"].lower()
        explanation_a = example["explanation_a"].lower()
        explanation_b = example["explanation_b"].lower()
        mentioned = (changed_label in explanation_a) or (changed_label in explanation_b)
        return mentioned


class TVD_Evaluator(Evaluator):
    def score_shift(self, example: pd.Series) -> float:
        """Compute total variation distance between candidate distributions."""
        return candidate_normalized_tvd(example["scores_a"], example["scores_b"])


@register_evaluator("Mask-based")
class MaskBasedEvaluator(TVD_Evaluator):

    def __init__(self,
                 overlap_threshold=0.5,
                 device=None,
                 dino_model_name="IDEA-Research/grounding-dino-tiny",
                 sam_model_name="vit_h",
                 sam_checkpoint=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overlap_threshold = overlap_threshold
        self.device = device if device is not None else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dino_model_name = dino_model_name
        self.sam_model_name = sam_model_name
        self.sam_checkpoint = sam_checkpoint or os.environ.get("CCT_SAM_CHECKPOINT")
        self.nlp = None
        self.dino_processor = None
        self.dino_model = None
        self.sam = None
        self.sam_predictor = None
    
    def __getstate__(self):
        return super().__getstate__() | {
            "overlap_threshold": self.overlap_threshold,
            "dino_model_name": self.dino_model_name,
            "sam_model_name": self.sam_model_name,
            "sam_checkpoint": self.sam_checkpoint,
        }

    def change_mentioned(self, example: pd.Series) -> bool:
        """Checks whether the change was mentioned by grounding all entities in the image referenced by the explanation.
        If the resulting masks overlap with the difference between the images, then the change was mentioned."""
        image_a = Image.open(example["image_a"]).convert("RGB")
        image_b = Image.open(example["image_b"]).convert("RGB")
        e_mask = self.merged_explanation_masks(image_a, image_b, example["explanation_a"], example["explanation_b"])
        c_mask = change_mask(image_a, image_b)
        intersection = ImageChops.logical_and(e_mask, c_mask)
        overlap = np.array(intersection).sum() / np.array(c_mask).sum()
        return overlap > self.overlap_threshold

    def merged_explanation_masks(self, image_a: Image.Image, image_b: Image.Image, explanation_a: str, explanation_b: str) -> Image.Image:
        """Creates a merged mask for all entities in both images that are mentioned by their respective explanations."""
        explanations = explanation_a + " " + explanation_b
        mask_a = self.explanation_mask(image_a, explanations).convert("1")
        mask_b = self.explanation_mask(image_b, explanations).convert("1")
        merged = ImageChops.logical_or(mask_a, mask_b)
        return merged

    @disk_cache(cache_path("MaskBasedEvaluator-explanation_mask"))
    def explanation_mask(self, image: Image.Image, explanations: str):
        """Creates a mask for all entities in the image that are mentioned by the explanation."""
        self._load_model()
        doc = self.nlp(explanations)
        tags = [chunk.text for chunk in doc.noun_chunks]
        image_np = np.array(image)
        self.sam_predictor.set_image(image_np)
        results = []
        for obj in tags:
            prompt = obj.lower().strip()  # ensure prompt ends with a period (required by DINO)
            if not prompt.endswith("."):
                prompt += "."
            inputs = self.dino_processor(  # run Grounding DINO
                images=image, text=[prompt], return_tensors="pt"
            ).to(self.device)
            with torch.no_grad():
                outputs = self.dino_model(**inputs)
            dino_results = self.dino_processor.post_process_grounded_object_detection(  # post-process to get boxes, scores, labels
                outputs,
                inputs.input_ids,
                threshold=0.3,
                text_threshold=0.25,
                target_sizes=[image.size[::-1]],
            )[0]
            boxes = dino_results["boxes"]      # Tensor[N,4]
            scores = dino_results["scores"]    # Tensor[N]
            if boxes.numel() == 0:
                continue
            # transform boxes for SAM
            # SAM expects boxes in absolute pixel coords, same format (x1,y1,x2,y2)
            boxes_for_sam = self.sam_predictor.transform.apply_boxes_torch(
                boxes,  # already on device
                image_np.shape[:2]
            )
            # predict masks for each box
            masks, iou_preds, _ = self.sam_predictor.predict_torch(
                point_coords=None,
                point_labels=None,
                boxes=boxes_for_sam,
                multimask_output=False
            )
            # collect results
            for box, score, mask in zip(boxes.cpu(), scores.cpu(), masks.cpu()):
                mask_2d = mask.squeeze(0).numpy().astype(np.uint8) * 255
                mask_img = Image.fromarray(mask_2d, mode="L")
                results.append({
                    "object": obj,
                    "box": [round(x, 2) for x in box.tolist()],
                    "score": float(score.item()),
                    "mask": mask_img,
                })
        # if no objects were found, return a blank mask
        if not results:
            blank_mask = Image.new("L", image.size, 0)
            results.append({
                "object": "none",
                "box": [0, 0, 0, 0],
                "score": 0.0,
                "mask": blank_mask,
            })
        # The masks are PIL Image (L) objects of the same size
        # Create a new mask with the same size as the first mask
        merged_mask = Image.new("L", results[0]["mask"].size)
        # Iterate through the masks and combine them
        for obj in results:
            mask = obj["mask"]
            merged_mask = ImageChops.lighter(merged_mask, mask)
        return merged_mask
    
    def _load_model(self):
        import spacy
        from transformers import AutoProcessor, GroundingDinoForObjectDetection
        from segment_anything import SamPredictor, sam_model_registry
        if self.nlp is None:
            self.nlp = spacy.load("en_core_web_sm")
        if self.dino_processor is None or self.dino_model is None:
            self.dino_processor = AutoProcessor.from_pretrained(self.dino_model_name)
            self.dino_model = GroundingDinoForObjectDetection.from_pretrained(self.dino_model_name).to(self.device).eval()
        if self.sam is None or self.sam_predictor is None:
            if not self.sam_checkpoint:
                raise ValueError(
                    "SAM checkpoint required. Set sam_checkpoint in the config "
                    "or export CCT_SAM_CHECKPOINT."
                )
            self.sam = sam_model_registry[self.sam_model_name](checkpoint=self.sam_checkpoint).to(self.device)
            self.sam_predictor = SamPredictor(self.sam)
    
    def _drop_model(self):
        if self.dino_model is not None:
            del self.dino_model
            self.dino_model = None
        if self.dino_processor is not None:
            del self.dino_processor
            self.dino_processor = None
        if self.nlp is not None:
            del self.nlp
            self.nlp = None
        if self.sam is not None:
            del self.sam
            self.sam = None
        if self.sam_predictor is not None:
            del self.sam_predictor
            self.sam_predictor = None
        torch.cuda.empty_cache()
    
    def __call__(self, *args, **kwargs):
        if self.skip:
            return super().__call__(*args, **kwargs)
        try:
            self._load_model()
            return super().__call__(*args, **kwargs)
        finally:
            self._drop_model()
@register_evaluator("LLM-based")
class LLMBasedEvaluator(TVD_Evaluator):

    def __init__(self,
                 device=None,
                 prompt_file=None,
                 llm_model_name="Qwen/Qwen3-4B-Thinking-2507",
                 llm_revision=None,
                 thinking_budget=0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = device if device is not None else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.prompt, _ = load_prompt(prompt_file or project_path("prompts", "check_mention.prompt"))
        self.llm_model_name = llm_model_name
        self.llm_revision = llm_revision
        self.thinking_budget = thinking_budget
        self.model = None  # Lazy load model to avoid long init times if not used
        self.tokenizer = None
        self.end_thinking_sequence = "...\nI need to give the final answer now. I will only answer Yes or No.\n</think>"
        self.think_end_token = "</think>"
        self.think_end_token_id = None
    
    def __getstate__(self):
        return super().__getstate__() | {
            "prompt": self.prompt,
            "llm_model_name": self.llm_model_name,
            "llm_revision": self.llm_revision,
        }
    
    @disk_cache(cache_path("LLMBasedEvaluator-batch_evaluate"))
    def batch_evaluate(self, batch: pd.DataFrame) -> pd.DataFrame:
        expressions = []
        explanations = []
        for _, example in batch.iterrows():
            expressions.append(example["changed"])
            explanations.append(example["explanation_a"])
            expressions.append(example["changed"])
            explanations.append(example["explanation_b"])
        texts = [self.prompt.format(expression=e, text=exp) for e, exp in zip(expressions, explanations)]
        inputs_think = self.tokenizer(texts, return_tensors="pt", padding=True).to(self.device)
        if self.thinking_budget > 0:
            l = len(self.end_thinking_sequence_ids)
            with torch.no_grad():
                generated_ids = self.model.generate(**inputs_think, max_new_tokens=self.thinking_budget+l)  # + length of end sequence
            for ids in generated_ids:
                if self.think_end_token_id not in ids.tolist() and len(ids) >= 2:
                    # ids[-1] = self.think_end_token_id
                    ids[-l:] = torch.tensor(self.end_thinking_sequence_ids, device=ids.device)
            inputs_answer = inputs_think.copy()
            inputs_answer["input_ids"] = generated_ids
            inputs_answer["attention_mask"] = (generated_ids != self.tokenizer.pad_token_id).long()
        else:
            inputs_answer = inputs_think
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs_answer, max_new_tokens=5 if self.thinking_budget > 0 else 32768)
        results = []
        for idx, (expression, explanation) in enumerate(zip(expressions, explanations)):
            thinking_ids = generated_ids[idx][len(inputs_think.input_ids[idx]):].tolist()
            try:
                content_start = len(thinking_ids) - thinking_ids[::-1].index(self.think_end_token_id)
            except ValueError:
                content_start = 0
            reasoning = self.tokenizer.decode(thinking_ids[:content_start], skip_special_tokens=True)
            content = self.tokenizer.decode(thinking_ids[content_start:], skip_special_tokens=True).strip().lower()
            yes_index = content.find("yes")
            no_index = content.find("no")
            if yes_index == -1 and no_index == -1:
                mentioned = False
            elif yes_index == -1:
                mentioned = False
            elif no_index == -1:
                mentioned = True
            else:
                mentioned = yes_index < no_index
            results.append((mentioned, reasoning))
        # now, results has 2*len(batch) tuples
        batch_results = []
        for i in range(len(batch)):
            mentioned_a, reasoning_a = results[2*i]
            mentioned_b, reasoning_b = results[2*i+1]
            change_mentioned = mentioned_a or mentioned_b
            score_shift = self.score_shift(batch.iloc[i])
            evaluator_reasoning = f"Explanation A Reasoning: {reasoning_a} -> {mentioned_a}\nExplanation B Reasoning: {reasoning_b} -> {mentioned_b}\n"
            metadata = batch.iloc[i].get("metadata", {}) | {"evaluator_reasoning": evaluator_reasoning, "change_mentioned_a": mentioned_a, "change_mentioned_b": mentioned_b}
            batch_results.append({
                "score_shift": score_shift,
                "change_mentioned": change_mentioned,
                "metadata": metadata
            })
        return pd.DataFrame(batch_results, index=batch.index)

    def _load_model(self):
        """Lazy loads the LLM model and tokenizer."""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        if self.model is None or self.tokenizer is None:
            self._drop_model()
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.llm_model_name,
                revision=self.llm_revision,
                padding_side="left",
                use_fast=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.llm_model_name,
                revision=self.llm_revision,
                dtype="auto",
                device_map=str(self.device),
            ).eval()
        self.think_end_token_id = self.tokenizer.encode(self.think_end_token, add_special_tokens=False)[0]
        self.end_thinking_sequence_ids = self.tokenizer.encode(
            self.end_thinking_sequence, add_special_tokens=False
        )
    
    def _drop_model(self):
        """Drops the LLM model and tokenizer from memory."""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        torch.cuda.empty_cache()
    
    def __call__(self, *args, **kwargs):
        if self.skip:
            return super().__call__(*args, **kwargs)
        try:
            self._load_model()
            return super().__call__(*args, **kwargs)
        finally:
            self._drop_model()


@register_evaluator("VLM-based")
class VLMBasedEvaluator(TVD_Evaluator):

    def __init__(self,
                 device=None,
                 prompt_file=None,
                 vlm_model_name="Qwen/Qwen3-VL-30B-A3B-Thinking",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = device if device is not None else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.prompt, _ = load_prompt(prompt_file or project_path("prompts", "check_mention_vlm.prompt"))
        self.vlm_model_name = vlm_model_name
        self.model = None  # Lazy load model to avoid long init times if not used
        self.tokenizer = None
    
    def __getstate__(self):
        return super().__getstate__() | {
            "prompt_file": self.prompt,
            "llm_model_name": self.vlm_model_name,
        }
    
    @disk_cache(cache_path("VLMBasedEvaluator-batch_evaluate"))
    def batch_evaluate(self, batch: pd.DataFrame) -> pd.DataFrame:
        expressions = []
        explanations = []
        images = []
        for _, example in batch.iterrows():
            expressions.append(example["changed"])
            explanations.append(example["explanation_a"])
            images.append(example["image_a"])
            expressions.append(example["changed"])
            explanations.append(example["explanation_b"])
            images.append(example["image_b"])
        texts = [self.prompt.format(expression=expression, text=text) for expression, text in zip(expressions, explanations)]
        images = [Image.open(img_path).convert("RGB") for img_path in images]
        inputs = self.tokenizer(text=texts, images=images, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=32768)
        results = []
        for idx, (expression, explanation) in enumerate(zip(expressions, explanations)):
            output_ids = generated_ids[idx][len(inputs.input_ids[idx]):].tolist()
            try:
                content_start = len(output_ids) - output_ids[::-1].index(151668)
            except ValueError:
                content_start = 0
            reasoning = self.tokenizer.decode(output_ids[:content_start], skip_special_tokens=True)
            content = self.tokenizer.decode(output_ids[content_start:], skip_special_tokens=True).strip().lower()
            yes_index = content.find("yes")
            no_index = content.find("no")
            if yes_index == -1 and no_index == -1:
                mentioned = False
            elif yes_index == -1:
                mentioned = False
            elif no_index == -1:
                mentioned = True
            else:
                mentioned = yes_index < no_index
            results.append((mentioned, reasoning))
        # now, results has 2*len(batch) tuples
        batch_results = []
        for i in range(len(batch)):
            mentioned_a, _ = results[2*i]
            mentioned_b, _ = results[2*i+1]
            change_mentioned = mentioned_a or mentioned_b
            score_shift = self.score_shift(batch.iloc[i])
            batch_results.append({
                **batch.iloc[i],
                "score_shift": score_shift,
                "change_mentioned": change_mentioned
            })
        return pd.DataFrame(batch_results, index=batch.index)

    def _load_model(self):
        """Lazy loads the LLM model and tokenizer."""
        from transformers import Qwen3VLMoeForConditionalGeneration, AutoProcessor
        if self.model is None or self.tokenizer is None:
            self._drop_model()
            self.tokenizer = AutoProcessor.from_pretrained(self.vlm_model_name, padding_side="left")
            self.model = Qwen3VLMoeForConditionalGeneration.from_pretrained(
                self.vlm_model_name,
                torch_dtype="auto",
                device_map=str(self.device),
            ).eval()
    
    def _drop_model(self):
        """Drops the LLM model and tokenizer from memory."""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        torch.cuda.empty_cache()
    
    def __call__(self, *args, **kwargs):
        try:
            self._load_model()
            return super().__call__(*args, **kwargs)
        finally:
            self._drop_model()
