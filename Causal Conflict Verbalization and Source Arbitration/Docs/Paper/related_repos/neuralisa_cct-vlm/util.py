import re
import os
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter
import pandas as pd
from functools import wraps
from contextlib import contextmanager


PROJECT_ROOT = Path(__file__).resolve().parent


def project_path(*parts: str) -> str:
    """Return a path relative to the repository root."""
    return str(PROJECT_ROOT.joinpath(*parts))


def cache_path(name: str) -> str:
    """Return a portable cache path, configurable through CCT_CACHE_DIR."""
    root = Path(os.environ.get("CCT_CACHE_DIR", PROJECT_ROOT / ".cache"))
    return str(root / name)


def load_prompt(prompt_template_path: str) -> tuple[str, list]:
    """
    Parse a prompt string to remove comments and unnecessary whitespace,
    extract and load embedded images, and replace their paths with vision tokens.

    Args:
        prompt_template_path (str): path to the input prompt template.

    Returns:
        Tuple[str, List[Image.Image]]: The cleaned prompt string and list of loaded images.
    """
    # Read entire template
    with open(prompt_template_path, 'r') as f:
        raw_text = f.read()

    # Clean out comments and empty lines
    cleaned_text = '\n'.join(
        line.split('#')[0].strip()
        for line in raw_text.splitlines()
        if line.strip() and not line.strip().startswith('#')
    )

    # Extract all image paths of common extensions
    pattern = r'\[([^\]]+\.(?:png|jpg|jpeg|bmp|gif))\]'
    image_paths = re.findall(pattern, cleaned_text)
    images = [Image.open(path) for path in image_paths]

    # Replace image references with vision tokens
    replaced_text = re.sub(
        pattern,
        '<|vision_start|><|image_pad|><|vision_end|>',
        cleaned_text
    )


    return replaced_text + '\n', images


def model_skip_error(func):
    def wrapper(self, example: pd.Series) -> pd.Series:
        if not example['error']:
            try:
                result = func(self, example)
                return result
            except ValueError as e:
                msg = f"Error in model: {e}"
                return pd.Series({
                    **example,
                    "scores_a": [],
                    "scores_b": [],
                    "explanation_a": "",
                    "explanation_b": "",
                    "error": True,
                    "reason": msg
                })
        return pd.Series({
            **example,
            "scores_a": [],
            "scores_b": [],
            "explanation_a": "",
            "explanation_b": ""
        })
    return wrapper


def evaluator_skip_error(func):
    def wrapper(self, example: pd.Series) -> pd.Series:
        if not example['error']:
            try:
                result = func(self, example)
                return result
            except ValueError as e:
                msg = f"Error in evaluator: {e}"
                return pd.Series({
                    **example,
                    "score_shift": 0.0,
                    "change_mentioned": False,
                    "error": True,
                    "reason": msg
                })
        return pd.Series({
            **example,
            "score_shift": 0.0,
            "change_mentioned": False
        })
    return wrapper


USE_CACHE = True

@contextmanager
def enable_disk_cache(enable: bool = True):
    """Context manager to temporarily disable disk caching."""
    global USE_CACHE
    previous_state = USE_CACHE
    USE_CACHE = enable
    try:
        yield
    finally:
        USE_CACHE = previous_state

def disk_cache(cache_dir: str):
    """Decorator to cache method results to disk using joblib.
    The goal of this decorator is to make joblib's Memory work as a method decorator.
    Caution: only use on methods that do not modify self!"""
    from joblib import Memory
    memory = Memory(cache_dir, verbose=0)

    def decorator(func):
        memory_func = memory.cache(func)

        @wraps(func)
        def wrapped_func(self, *args, **kwargs):
            if USE_CACHE:
                return memory_func(self, *args, **kwargs)
            else:
                print("WARNING: Disk cache disabled.")
            return func(self, *args, **kwargs)

        return wrapped_func

    return decorator


def change_mask(image_a: Image.Image, image_b: Image.Image, threshold: int = 25, median_filter: int = 5) -> Image.Image:
    """Creates a mask by taking the pixelwise difference between the two images."""
    difference = ImageChops.difference(image_a, image_b)
    difference = difference.convert("L")  # Convert to grayscale
    difference = difference.point(lambda x: 255 if x > threshold else 0)  # Threshold to create binary mask
    difference = difference.filter(ImageFilter.MedianFilter(size=median_filter))  # Apply median filter to remove outliers
    return difference.convert("1")
