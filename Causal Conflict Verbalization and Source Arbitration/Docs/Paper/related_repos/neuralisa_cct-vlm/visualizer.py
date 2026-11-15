import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
from textwrap import wrap
from tqdm import tqdm
import os

class Visualizer:
    def __init__(
            self,
            skip=False,
            output_dir="./outputs/visualizations",
            figsize=(14, 12),
            height_ratios=(3, 2, 1),
            image_spines=False,
            bar_spines=False,
            bar_label_rotation=-45,
            dpi=300,
            suptitle_y=1.05,
            bottom_text_y=0.02,
            bottom_text_fontsize=20,
            bottom_text_ha='center',
            suptitle_fontsize=20,
            suptitle_fontweight="bold"):
        self.skip = skip
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        self.figsize = figsize
        self.height_ratios = height_ratios
        self.image_spines = image_spines
        self.bar_spines = bar_spines
        self.bar_label_rotation = bar_label_rotation
        self.dpi = dpi
        self.suptitle_y = suptitle_y
        self.bottom_text_y = bottom_text_y
        self.bottom_text_fontsize = bottom_text_fontsize
        self.bottom_text_ha = bottom_text_ha
        self.suptitle_fontsize = suptitle_fontsize
        self.suptitle_fontweight = suptitle_fontweight
    
    def __call__(self, data):
        if self.skip:
            print("Skipping visualization.")
            return data
        filtered_data = data[data['error'] == False]
        for i, example in tqdm(filtered_data.iterrows(), desc="Visualizing examples", total=filtered_data.shape[0]):
            self.visualize_example(example, i)
        return data

    def visualize_example(self, example, i):
        sns.set_theme(style="whitegrid")

        fig = plt.figure(figsize=self.figsize, constrained_layout=True)
        gs = GridSpec(
            nrows=3, ncols=2, figure=fig,
            height_ratios=self.height_ratios,
        )


        image_paths = {"A": example["image_a"], "B": example["image_b"]}

        for col, (key, img_path) in enumerate(image_paths.items()):
            ax = fig.add_subplot(gs[0, col])
            ax.set_xticks([]); ax.set_yticks([])

            if not os.path.isfile(img_path):
                raise FileNotFoundError(f"Image not found: {img_path}")
            img = plt.imread(img_path)

            ax.imshow(img)
            ax.set_title(f"Image {key}", fontsize=12, pad=8)
            for spine in ax.spines.values():
                spine.set_visible(self.image_spines)

        df_left  = pd.DataFrame({
            "scores": [f"{v:.2f}\n{k}" for k, v in zip(example["labels"], example["scores_a"])],
            "value": example["scores_a"]
        })
        df_right = pd.DataFrame({
            "scores": [f"{v:.2f}\n{k}" for k, v in zip(example["labels"], example["scores_b"])],
            "value": example["scores_b"]
        })
        data = {"A": df_left, "B": df_right}

        for col, (key, df) in enumerate(data.items()):
            ax = fig.add_subplot(gs[1, col])
            sns.barplot(ax=ax, data=df, x="scores", y="value")
            ax.set_title(f"Scores {key}", pad=10)
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_facecolor('white')
            ax.grid(False)
            for spine in ax.spines.values():
                spine.set_visible(self.bar_spines)
            ax.set_ylim(0, 1)
            ax.set_yticklabels([])
            ax.tick_params(axis='x', rotation=self.bar_label_rotation)

        # --- Row 3: Notes (text in two columns) ---
        explanations = {"A": example["explanation_a"], "B": example["explanation_b"]}
        for col, (key, txt) in enumerate(explanations.items()):
            ax = fig.add_subplot(gs[2, col])
            ax.axis("off")
            ax.set_title(f"Explanation {key}")
            escaped_txt = txt.replace("$", r"\$") if isinstance(txt, str) else str(txt)
            ax.text(0, 1, "\n".join(wrap(escaped_txt, width=68)),
                    ha="left", va="top", fontsize=11)

        suptitle = f"Example ID {i}\n"
        suptitle += str(example["question"])
        plt.suptitle(suptitle, y=self.suptitle_y, fontsize=self.suptitle_fontsize, fontweight=self.suptitle_fontweight)
        
        # Add the last line below the figure
        score_shift_formatted = f"{float(example['score_shift']):.3f}"
        bottom_text = f"Change: {example['changed']}, Change mentioned: {example['change_mentioned']}, Score shift: {score_shift_formatted}"
        fig.text(0.5, self.bottom_text_y, bottom_text, ha=self.bottom_text_ha, fontsize=self.bottom_text_fontsize, fontweight=self.suptitle_fontweight)
        output_path = os.path.join(self.output_dir, f"visualisation_{i}.png")
        plt.savefig(output_path, bbox_inches="tight", dpi=self.dpi)
        plt.close(fig)


if __name__ == "__main__":
    example = {
        "question": "What is the closest object to the Apple?",
        "image_a": "images/mock/image_a.png",
        "image_b": "images/mock/image_b.png",
        "labels": ["apple", "banana", "orange", "grape"],
        "scores_a": [0.8, 0.1, 0.1, 0.0],
        "scores_b": [0.7, 0.1, 0.2, 0.0],
        "explanation_a": "This is the explanation for image A.",
        "explanation_b": "This is the explanation for image B.",
        "changed": "Keyboard",
        "change_mentioned": False,
        "score_shift": "0.1"
    }
    visualizer = Visualizer()
    visualizer.visualize_example(example, 0)
