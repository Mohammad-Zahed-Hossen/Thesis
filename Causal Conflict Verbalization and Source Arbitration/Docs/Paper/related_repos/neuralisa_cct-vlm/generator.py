from abc import ABC, abstractmethod
import math
import os
import random
from PIL import Image
import pandas as pd
import torch
from tqdm import tqdm
import json
from datasets import load_dataset, Dataset
import gc
from util import load_prompt, disk_cache, change_mask, enable_disk_cache, cache_path, project_path
import numpy as np
from PIL import Image, ImageChops


# Generator Registry
GENERATOR_REGISTRY = {}

def register_generator(name):
    def decorator(cls):
        GENERATOR_REGISTRY[name] = cls
        return cls
    return decorator

class Generator(ABC):
    """Create paired images, a question, and a fixed answer set."""
    def __init__(self, n_examples=10, image_dir="./images", image_size=(224, 224), skip=False):
        self.n_examples = n_examples
        self.image_dir = image_dir
        self.image_size = tuple(image_size)
        self.skip = skip

    def __getstate__(self):
        return {
            "image_dir": self.image_dir,
            "image_size": self.image_size
        }

    def __call__(self, _) -> pd.DataFrame:
        """Generate all requested examples and return them as a DataFrame."""
        if self.skip:
            print("Skipping generation.")
            return pd.DataFrame()
        self._load_models()
        data = pd.DataFrame([self.generate() for _ in tqdm(range(self.n_examples), desc="Generating examples")])
        data.set_index("id", inplace=True)
        self._drop_models()
        return data


    @abstractmethod
    def generate(self) -> pd.Series:
        """Generate one row using the schema documented in DATA.md."""
        raise NotImplementedError

    def _load_models(self):
        pass
    
    def _drop_models(self):
        pass


@register_generator("Mock")
class MockGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_ctr = 0
    
    def __getstate__(self):
        return super().__getstate__() | {"id_ctr": self.id_ctr}

    def generate(self) -> pd.Series:
        self.id_ctr += 1
        os.makedirs(self.image_dir, exist_ok=True)
        image_a_path = os.path.join(self.image_dir, f"mock_{self.id_ctr}_a.png")
        image_b_path = os.path.join(self.image_dir, f"mock_{self.id_ctr}_b.png")
        image_a = Image.new("RGB", self.image_size, (245, 245, 245))
        image_b = image_a.copy()
        # A deterministic visible perturbation keeps the smoke test meaningful.
        patch_size = max(4, min(self.image_size) // 5)
        image_b.paste((220, 60, 60), (8, 8, 8 + patch_size, 8 + patch_size))
        image_a.save(image_a_path)
        image_b.save(image_b_path)
        return pd.Series({
            "id": self.id_ctr,
            "image_a": image_a_path,
            "image_b": image_b_path,
            "question": "What is the 3rd closest object to the knife?",
            "labels": ["cherry", "spoon", "apple", "banana", "rubber duck", "knife"],
            "changed": "apple",
            "task": "vqa",
            "error": False,
            "reason": "",
            "metadata": {}
        })
    
@register_generator("Procedural 2D VQE")
class Procedural2DGeneratorVQE(Generator):
    def __init__(self, n_objects=10, object_size=30, objects_file="./objects/objects.json", **kwargs):
        super().__init__(**kwargs)
        self.n_objects = (n_objects, n_objects) if isinstance(n_objects, int) else n_objects
        self.object_size = (object_size, object_size) if isinstance(object_size, int) else object_size
        self.objects_file = objects_file
        self.objects_dir = os.path.dirname(objects_file)
        with open(self.objects_file, "r") as f:
            self.objects = json.load(f)
        self._id_ctr = 0

    def generate(self) -> pd.Series:
        self._id_ctr += 1
        scene_objects = []
        n_objects = random.randint(*self.n_objects)
        for obj in random.sample(self.objects, n_objects):
            scene_objects.append({
                "label": obj["label"],
                "image": Image.open(f"{self.objects_dir}/{obj['image']}").convert("RGBA"),
                "position": (random.randint(0, self.image_size[0]), random.randint(0, self.image_size[1])),
                "size": random.randint(*self.object_size)
            })
        image_a = Image.new("RGBA", self.image_size, (255, 255, 255, 255))
        for obj in scene_objects[:-1]:
            self._render_object(image_a, obj)
        image_b = image_a.copy()
        self._render_object(image_b, scene_objects[-1])
        nth = random.randint(1, len(scene_objects))
        question = f"What is the {self._ordinal(nth)} closest object to the {scene_objects[0]['label']}?"
        # save the images
        image_a_path = os.path.join(self.image_dir, f"{self._id_ctr}a.png")
        image_b_path = os.path.join(self.image_dir, f"{self._id_ctr}b.png")
        image_a.save(image_a_path)
        image_b.save(image_b_path)
        metadata = {
            "id": self._id_ctr,
            "n_objects_a": len(scene_objects) - 1,
            "n_objects_b": len(scene_objects),
            "perturbation_method": "remove object"
        }
        return pd.Series({
            "id": self._id_ctr,
            "image_a": image_a_path,
            "image_b": image_b_path,
            "question": question,
            "labels": [obj["label"] for obj in scene_objects],
            "changed": scene_objects[-1]["label"],
            "task": "vqa",
            "error": False,
            "reason": "",
            "metadata": metadata
        })

    @staticmethod
    def _render_object(img: Image.Image, obj: dict):
        """Render a single object on the image."""
        
        # Get original dimensions
        obj_img = obj["image"]
        orig_width, orig_height = obj_img.size
        diagonal = math.hypot(orig_width, orig_height)

        # Calculate scaling factor to fit within circle while preserving aspect ratio
        scale = obj["size"] / diagonal
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        
        obj_img = obj_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate paste position (center the object)
        paste_x = int(obj["position"][0] - new_width // 2)
        paste_y = int(obj["position"][1] - new_height // 2)

        # Paste with alpha transparency
        img.paste(obj_img, (paste_x, paste_y), obj_img)
    

    @staticmethod
    def _ordinal(nth: int) -> str:
        """Convert an integer to its ordinal representation."""
        if 10 <= nth % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(nth % 10, "th")
        return f"{nth}{suffix}"    


@register_generator("QwenImageEdit")
class QwenImageEdit(Generator):

    def __init__(
            self, dataset_name="SNLIVE", data_dir: str | None = None, split="validation",
            device=None,
            seed=42,
            use_qwen_image_edit_plus=False,
            change_fraction_threshold=0.20,
            qwen_2p5_vl_prompt_file: str | None = None,
            consensus_filter_threshold: float = 0.5,
            dino_model_name: str = "IDEA-Research/grounding-dino-tiny",
            dino_revision: str | None = None,
            sam_checkpoint: str | None = None,
            sam_model_name: str = "vit_h",
            model_path: str | None = None,
            model_revision: str | None = None,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if device is None else device
        self.dataset_name = dataset_name
        data_dir = data_dir or os.environ.get("CCT_DATA_DIR", project_path("data"))
        qwen_2p5_vl_prompt_file = qwen_2p5_vl_prompt_file or project_path("prompts", "detect_objects.prompt")
        sam_checkpoint = sam_checkpoint or os.environ.get("CCT_SAM_CHECKPOINT")
        self.model_path = model_path or os.environ.get("CCT_QWEN_IMAGE_EDIT_MODEL", "Qwen/Qwen-Image-Edit")
        self.model_revision = model_revision
        self.dataset = self.prepare_dataset(dataset_name=dataset_name, data_dir=data_dir, split=split).shuffle(seed=seed)
        self.qwen_2p5_vl_prompt, _ = load_prompt(qwen_2p5_vl_prompt_file)
        self.change_fraction_threshold = change_fraction_threshold
        self.use_qwen_image_edit_plus = use_qwen_image_edit_plus
        self.consensus_filter_threshold = consensus_filter_threshold
        self.dino_model_name = dino_model_name
        self.dino_revision = dino_revision
        self.sam_checkpoint = sam_checkpoint
        self.sam_model_name = sam_model_name
        self.seed = seed
        self._preloaded = []
        self._id_ctr = 0
        self.qwen_image_edit_model = None
        self.nlp = None
        self.dino_processor = None
        self.dino_model = None
        self.sam = None
        # Check that resolution is one of (1024x1024、1184x880、1392x752、1568x672) - could be lists or tuples
        valid_resolutions = [(1024, 1024), (1184, 880), (1392, 752), (1568, 672)]
        if tuple(self.image_size) not in valid_resolutions and not self.skip:
            raise ValueError(f"Invalid image size {self.image_size}. Must be one of {valid_resolutions}.")
    
    def __getstate__(self):
        return super().__getstate__() | {
            "seed": self.seed,
            "_id_ctr": self._id_ctr,
            "qwen_2p5_vl_prompt": self.qwen_2p5_vl_prompt,
            "use_qwen_image_edit_plus": self.use_qwen_image_edit_plus,
            "dataset_name": self.dataset_name
        }
    
    def __call__(self, data):
        self._id_ctr = len(data) if data is not None else 0
        return super().__call__(data)
    
    def prepare_dataset(self, dataset_name, data_dir, split) -> Dataset:
        if dataset_name == "SNLIVE":
            if split == "val":
                split = "validation"
            return load_dataset("HuggingFaceM4/SNLI-VE", trust_remote_code=True, data_dir=data_dir + "/Flickr30k", split=split)
        elif dataset_name == "CVBENCH":
            from datasets import load_dataset
            return load_dataset("nyu-visionx/CV-Bench", "2D", split=split).filter(lambda x: str(x.get("task", "")).lower() == "count")
        elif dataset_name == "AOKVQA":
            if split == "validation":
                split = "val"
            ds_path = f"{data_dir}/AOKVQA/aokvqa_v1p0_{split}.json"
            with open(ds_path, "r") as f:
                ds_raw = json.load(f)
            ds_list = []
            for item in ds_raw:
                image = Image.open(f"{data_dir}/COCO2017/{split}2017/{item['image_id']:012}.jpg")
                ds_item = {
                    "image": image,
                    "question": item["question"],
                    "choices": item["choices"]
                }
                ds_list.append(ds_item)
                image.close()
            return Dataset.from_list(ds_list)

    def get_data(self) -> tuple:
        """Get the current base image, hypothesis and the tag to remove from the base image.
        """
        example = self.dataset[self._id_ctr % len(self.dataset)]
        example_image = example['image'].convert("RGB")
        base_image = self.preprocess_image(example_image)
        if self.dataset_name == "SNLIVE":
            question = example['hypothesis']
            labels = ["entailment", "contradiction", "neutral"]
        elif self.dataset_name == "CVBENCH":
            import re
            question = example['question']
            labels = example['choices']
            m = re.search(r"how many\s+([a-zA-Z][a-zA-Z -]*)\s+(?:are|is|can|do|does)\b", question.lower())
            tag = m.group(1).strip() if m else ""
            if len(tag) < 3: tag = ""
            return base_image, question, tag, labels
        elif self.dataset_name == "AOKVQA":
            question = example['question']
            labels = example['choices']
        else:
            raise ValueError(f"Unknown dataset name {self.dataset_name}")
        tag = self.tag_image(base_image)
        return base_image, question, tag, labels

    def generate(self) -> pd.Series:
        error = False
        reason = ""
        image_a, question, tag_to_remove, labels = self.get_data()
        image_b = self.edit_image(image_a, tag_to_remove)
        image_c = change_mask(image_a, image_b)
        image_d = self.description_mask(image_a, tag_to_remove)
        image_a_path = os.path.join(self.image_dir, f"{self._id_ctr}a.png")
        image_b_path = os.path.join(self.image_dir, f"{self._id_ctr}b.png")
        image_c_path = os.path.join(self.image_dir, f"{self._id_ctr}c.png")
        image_d_path = os.path.join(self.image_dir, f"{self._id_ctr}d.png")
        image_a.save(image_a_path)
        image_b.save(image_b_path)
        image_c.save(image_c_path)
        image_d.save(image_d_path)
        # Filter based on change fraction and consensus ratio
        frac = np.array(image_c).mean()
        intersection = np.array(image_c) & np.array(image_d)
        consensus_ratio = intersection.sum() / np.array(image_c).sum() if np.array(image_c).sum() > 0 else 0.0
        if not tag_to_remove:
            error = True
            reason = "NoTag: No suitable object for removal detected"
        elif frac > self.change_fraction_threshold:
            error = True
            reason = f"ChangeFraction: Fraction {frac:.2f} above threshold {self.change_fraction_threshold:.2f}"
        elif consensus_ratio < self.consensus_filter_threshold:
            error = True
            reason = f"ConsensusFilter: Ratio {consensus_ratio:.2f} below threshold {self.consensus_filter_threshold:.2f}"
        self._id_ctr += 1
        return pd.Series({
            "id": self._id_ctr - 1,
            "image_a": image_a_path,
            "image_b": image_b_path,
            "change_actual_mask": image_c_path,
            "change_description_mask": image_d_path,
            "question": question,
            "labels": labels,
            "changed": tag_to_remove,
            "task": "ve" if self.dataset_name == "SNLIVE" else "vqa",
            "error": error,
            "reason": reason,
            "metadata": {}
        })

    @disk_cache(cache_path("QwenImageEdit-edit_image"))
    def edit_image(self, image: Image.Image, tag_to_remove: str) -> Image.Image:
        if not tag_to_remove:
            return image.copy()
        prompt = f"Remove only the {tag_to_remove}. Keep the rest of the picture exactly the same (pixel-perfect)."
        inputs = {
            "image": image,
            "prompt": prompt,
            "generator": torch.manual_seed(0),
            "true_cfg_scale": 4.0,
            "negative_prompt": " ",
            "num_inference_steps": 50,
        }

        with torch.inference_mode():
            output = self.qwen_image_edit_model(**inputs)

        return output.images[0]

    @disk_cache(cache_path("QwenImageEdit-tag_image"))
    def tag_image(self, image: Image.Image) -> str:
        """Use the RAM++ model to get a list of image tags."""
        text = self.qwen_2p5_vl_prompt
        inputs = self.qwen_image_edit_model.processor(text=text, images=[image], return_tensors="pt", padding=False).to(self.device)
        eos_token_id = self.qwen_image_edit_model.tokenizer.eos_token_id
        generated_ids = self.qwen_image_edit_model.text_encoder.generate(**inputs, max_new_tokens=512, do_sample=True, pad_token_id=eos_token_id)
        generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
        full_text_answer = self.qwen_image_edit_model.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return self.process_response(full_text_answer)

    def process_response(self, response: str) -> str:
        idx = response.lower().rfind("answer")
        if idx != -1:
            response = response[idx + len("answer"):].strip()
        else:
            return ""
        remove_chars = '"*:[].' + "`'<>"
        for char in remove_chars:
            response = response.replace(char, "")
        response = response.lower().strip()
        if response == "none":
            return ""
        if response.startswith("the "):
            response = response[4:]
        if response.startswith("a "):
            response = response[2:]
        return response

    @disk_cache(cache_path("QwenImageEdit-description_mask"))
    def description_mask(self, image_a, description) -> Image.Image:
        """
        Ground each object name in the image and return masks.

        Returns a single mask that combines all masks for the objects as a black and white image.
        black pixels are masked (cannot be changed further down the pipeline),
        white pixels are not masked (can be changed further down the pipeline).
        """
        if not description:
            return Image.new("1", image_a.size, 0)  # blank mask

        # 1) load image
        image_np = np.array(image_a)

        # tell SAM what image we're working on
        self.sam_predictor.set_image(image_np)

        results = []

        # ensure prompt ends with a period (required by DINO)
        prompt = description.lower().strip()
        if not prompt.endswith("."):
            prompt += "."

        root_obj = self.extract_root_object(prompt)
        if root_obj is None:
            return Image.new("1", image_a.size, 0)  # blank mask

        # 2) run Grounding DINO
        inputs = self.dino_processor(
            images=image_a, text=[prompt], return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            outputs = self.dino_model(**inputs)

        # 3) post-process to get boxes, scores, labels
        dino_results = self.dino_processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=0.3,
            text_threshold=0.25,
            target_sizes=[image_a.size[::-1]],
        )[0]
        boxes = dino_results["boxes"]      # Tensor[N,4]
        scores = dino_results["scores"]    # Tensor[N]

        # keep only boxes for the root object
        keep = []
        for i, label in enumerate(dino_results["text_labels"]):
            if root_obj in label.lower():
                keep.append(i)
        boxes = boxes[keep]
        scores = scores[keep] 

        if boxes.numel() == 0:
            return Image.new("1", image_a.size, 0)  # blank mask

        # 4) transform boxes for SAM
        #   SAM expects boxes in absolute pixel coords, same format (x1,y1,x2,y2)
        boxes_for_sam = self.sam_predictor.transform.apply_boxes_torch(
            boxes,  # already on device
            image_np.shape[:2]
        )

        # 5) predict masks for each box
        masks, iou_preds, _ = self.sam_predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=boxes_for_sam,
            multimask_output=False
        )

        # 6) collect results
        for box, score, mask in zip(boxes.cpu(), scores.cpu(), masks.cpu()):
            mask_2d = mask.squeeze(0).numpy().astype(np.uint8) * 255
            mask_img = Image.fromarray(mask_2d).convert("1")
            results.append({
                "object": root_obj,
                "box": [round(x, 2) for x in box.tolist()],
                "score": float(score.item()),
                "mask": mask_img,
            })
    
        # if no objects were found, return a blank mask
        if not results:
            blank_mask = Image.new("1", image_a.size, 0)
            results.append({
                "object": "none",
                "box": [0, 0, 0, 0],
                "score": 0.0,
                "mask": blank_mask,
            })

        # The masks are PIL Image (L) objects of the same size
        # Create a new mask with the same size as the first mask
        merged_mask = Image.new("1", results[0]["mask"].size)
        # Iterate through the masks and combine them
        for obj in results:
            mask = obj["mask"]
            merged_mask = ImageChops.lighter(merged_mask, mask)

        return merged_mask
    
    def extract_root_object(self, description: str) -> str:
        # Return directly when the description contains a single word.
        description = description.strip().lower()

        if len(description.split()) == 1:
            return description.strip('.')

        doc = self.nlp(description)

        root = list(doc.sents)[0].root

        if root.pos_ in {"NOUN", "PROPN", "PRON"}:
            return root.text.lower().strip('.')

        candidates = [token for token in doc if token.pos_ in {"NOUN", "PROPN", "PRON"}]

        if candidates:
            return candidates[0].text.lower().strip('.')

        return description.split()[0].strip('.')  # fallback to leftmost word

    def preprocess_image(self, image: Image.Image):
        """Resize and crop the image to the configured image size."""
        image = image.convert("RGB")
        scale = min(self.image_size[0] / image.width, self.image_size[1] / image.height)
        new_size = (int(image.width * scale), int(image.height * scale))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        width, height = image.size
        left = (width - self.image_size[0]) / 2
        top = (height - self.image_size[1]) / 2
        right = (width + self.image_size[0]) / 2
        bottom = (height + self.image_size[1]) / 2
        return image.crop((left, top, right, bottom))
    
    def _load_models(self):
        from diffusers import QwenImageEditPipeline
        if self.qwen_image_edit_model is None:
            self.qwen_image_edit_model = QwenImageEditPipeline.from_pretrained(
                self.model_path,
                revision=self.model_revision,
                torch_dtype=torch.bfloat16,
            ).to(self.device)
            self.qwen_image_edit_model.set_progress_bar_config(disable=True)
        if self.nlp is None:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        if self.dino_model is None or self.dino_processor is None:
            from transformers import AutoProcessor, GroundingDinoForObjectDetection
    
            self.dino_processor = AutoProcessor.from_pretrained(
                self.dino_model_name, revision=self.dino_revision
            )
            dino_model = GroundingDinoForObjectDetection.from_pretrained(
                self.dino_model_name, revision=self.dino_revision
            )
            self.dino_model = dino_model.to(self.device).eval()
        if self.sam is None:
            from segment_anything import sam_model_registry, SamPredictor

            if not self.sam_checkpoint:
                raise ValueError(
                    "SAM checkpoint required. Set sam_checkpoint in the config "
                    "or export CCT_SAM_CHECKPOINT."
                )
            sam = sam_model_registry[self.sam_model_name](checkpoint=self.sam_checkpoint)
            self.sam = sam.to(self.device) # eval?
            self.sam_predictor = SamPredictor(self.sam)

    def _drop_models(self):
        del self.qwen_image_edit_model
        del self.dino_model
        del self.dino_processor
        del self.nlp
        del self.sam_predictor
        del self.sam
        self.qwen_image_edit_model = None
        torch.cuda.empty_cache()
        gc.collect()
