
import argparse
import os
from main import CCT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a dependency-light end-to-end CCT smoke test.")
    parser.add_argument("--output-dir", default="./smoke_test_results")
    args = parser.parse_args()
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    config = {
        "output_dir": output_dir,
        "override": True,
        "run_generator": True,
        "generator": "Mock",
        "model": "Perfect Mock",
        "evaluator": "Mock",
        "generator_kwargs": {
            "n_examples": 5,
            "image_size": [224, 224]
        },
        "model_kwargs": {},
        "evaluator_kwargs": {},
        "visualizer_kwargs": {
            "image_spines": True
        }
    }
    
    cct = CCT(**config)
    cct()
    for name in ("generator.csv", "model.csv", "evaluator.csv"):
        path = os.path.join(output_dir, "data", name)
        if not os.path.isfile(path):
            raise RuntimeError(f"Smoke test did not create {path}")
    print("Smoke test completed successfully.")
