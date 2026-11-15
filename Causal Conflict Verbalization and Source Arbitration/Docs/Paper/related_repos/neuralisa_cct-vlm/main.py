from model import MODEL_REGISTRY
from evaluator import EVALUATOR_REGISTRY
from visualizer import Visualizer
import pandas as pd
import json
import os


class CCT:
    def __init__(self, output_dir="./outputs/run", override=False, run_generator=False,
                 generator="Mock", model="Random Mock", evaluator="Mock",
                 generator_kwargs=None, model_kwargs=None, evaluator_kwargs=None,
                 visualizer_kwargs=None):
        generator_kwargs = generator_kwargs or {}
        model_kwargs = model_kwargs or {}
        evaluator_kwargs = evaluator_kwargs or {}
        visualizer_kwargs = visualizer_kwargs or {}
        self.output_dir = output_dir
        self.generation_csv_path = os.path.join(output_dir, "data", "generator.csv")
        self.model_csv_path = os.path.join(output_dir, "data", "model.csv")
        self.evaluation_csv_path = os.path.join(output_dir, "data", "evaluator.csv")
        self.override = override
        self.run_generator = run_generator
        self.data = None
        
        # Generator dependencies are imported only when generation is requested.
        self.generator = None
        if self.run_generator:
            from generator import GENERATOR_REGISTRY
            if generator not in GENERATOR_REGISTRY:
                raise ValueError(f"Generator '{generator}' not found. Available: {list(GENERATOR_REGISTRY.keys())}")
        if model not in MODEL_REGISTRY:
            raise ValueError(f"Model '{model}' not found. Available: {list(MODEL_REGISTRY.keys())}")
        if evaluator not in EVALUATOR_REGISTRY:
            raise ValueError(f"Evaluator '{evaluator}' not found. Available: {list(EVALUATOR_REGISTRY.keys())}")

        images_dir = os.path.join(self.output_dir, "images")
        data_dir = os.path.join(self.output_dir, "data")
        visualizations_dir = os.path.join(self.output_dir, "visualizations")
        if self.run_generator:
            self.generator = GENERATOR_REGISTRY[generator](image_dir=images_dir, **generator_kwargs)
        self.model = MODEL_REGISTRY[model](**model_kwargs)
        self.evaluator = EVALUATOR_REGISTRY[evaluator](output_dir=output_dir, **evaluator_kwargs)
        self.visualizer = Visualizer(output_dir=visualizations_dir, **visualizer_kwargs)
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(visualizations_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

    def __call__(self):
        if self.run_generator:
            self.step(self.generator, self.generation_csv_path)
        elif not os.path.exists(self.generation_csv_path):
            raise FileNotFoundError(
                f"Missing {self.generation_csv_path}. Set run_generator=true to create it, "
                "or place a prepared generator.csv at that path."
            )
        self.data = pd.read_csv(self.generation_csv_path)
        self.data = self.deserialize_df(self.data)
        self.step(self.model, self.model_csv_path)
        self.step(self.evaluator, self.evaluation_csv_path)
        self.step(self.visualizer, None)

    def step(self, step_function, output_path):
        """Helper to handle data processing, saving, and loading for each step."""
        if not self.override and output_path is not None and os.path.exists(output_path):
            data = pd.read_csv(output_path)
        else:
            data = step_function(self.data)
            data = self.serialize_df(data)
            if output_path is not None:
                self.override = True
                data.to_csv(output_path, index=False)
                data = pd.read_csv(output_path)
        self.data = self.deserialize_df(data)

    @staticmethod
    def serialize_df(df):
        """Convert dict/list columns to JSON strings for CSV saving."""
        for col in df.columns:
            df[col] = df[col].apply(lambda x: "<<json>>" + json.dumps(x) if isinstance(x, (dict, list)) else x)
        return df

    @staticmethod
    def deserialize_df(df):
        """Parse JSON strings back to dicts/lists from CSV."""
        for col in df.columns:
            df[col] = df[col].apply(lambda x: json.loads(x[8:]) if isinstance(x, str) and x.startswith("<<json>>") else x)
        return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the vCT/vCCT pipeline from a JSON configuration.")
    parser.add_argument("config", help="Path to a pipeline configuration file")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    print(json.dumps(config, indent=2))
    CCT(**config)()
