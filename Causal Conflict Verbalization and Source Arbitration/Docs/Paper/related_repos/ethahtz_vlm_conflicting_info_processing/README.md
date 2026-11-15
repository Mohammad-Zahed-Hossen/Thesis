# Conflicting Multimodal Information Processing

This repository contains the code for running experiments presented in [How Do Vision-Language Models Process Conflicting Information Across Modalities?](https://arxiv.org/abs/2507.01790)

## Abstract

  

> AI models are increasingly required to be multimodal, integrating disparate input streams into a coherent state representation on which subsequent behaviors and actions can be based. This paper seeks to understand how such models behave when input streams present conflicting information. Focusing specifically on vision-language models, we provide inconsistent inputs (e.g., an image of a dog paired with the caption "A photo of a cat") and ask the model to report the information present in one of the specific modalities (e.g., "What does the caption say / What is in the image?"). We find that models often favor one modality over the other, e.g., reporting the image regardless of what the caption says, but that different models differ in which modality they favor. We find evidence that the behaviorally preferred modality is evident in the internal representational structure of the model, and that specific attention heads can restructure the representations to favor one modality over the other. Moreover, we find modality-agnostic "router heads" which appear to promote answers about the modality requested in the instruction, and which can be manipulated or transferred in order to improve performance across datasets and modalities. Together, the work provides essential steps towards identifying and controlling if and how models detect and resolve conflicting signals within complex multimodal environments.

## Table of Contents

  

- [Conflicting Multimodal Information Processing](#conflicting-multimodal-information-processing)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Overall Organization](#overall-organization)
  - [Behavioral Evaluation](#behavioral-evaluation)
  - [Precomputing Consistent and Inconsistent Multimodal Representations](#precomputing-consistent-and-inconsistent-multimodal-representations)
  - [Probe and Cluster Fitting on Representations](#probe-and-cluster-fitting-on-representations)
  - [Attention Head Attribution and Intervention](#attention-head-attribution-and-intervention)
  - [How to Cite](#how-to-cite)

  

## Installation

  

Use the command below to set up the environment:

```
pip install -r requirements.txt
```

  
## Overall Organization


The main scripts are located under the `./src` folder. To run a script, the easiest way is to use a confuguration file defined in the `./configs` folder, with the `--config` flag. Otherwise, you can look up the corresponding arguments and enter the arguments manually (or with a bash script) for each python script.

 

## Behavioral Evaluation 

 

To run the behavioral evaluations, 
```
python src/prompt_evaluation.py --config configs/behavioral_experiment.json 
``` 


Here is an example configuration (`./configs/behavioral_experiment.json`)

```
{
    "seed": 42,
    "work_dir": ".",
    "model_name": "Qwen/Qwen2.5-VL-7B-Instruct",
    "dataset": "Pascal",
    "version": 0,
    "caption_type": "inconsistent",
    "modality_to_report": "image",
    "order": "icq",
    "n_candidates": 5,
    "is_assistant_prompt": 1,
    "is_explicit_helper": 0,
    "use_pointers": 1,
    "batch_size": 10
}
```

Some of the important arguments include:
- `model_name`: the HuggingFace model string that represent the model to be evaluated (choose from `llava-hf/llava-1.5-7b-hf`, `Salesforce/instructblip-vicuna-7b`, `Qwen/Qwen2.5-VL-7B-Instruct`, `llava-hf/llava-onevision-qwen2-7b-ov-hf`); 
- `dataset`: the dataset to be used for evaluation (choose from `cifar10`, `cifar100`, `imagenet100`, `Pascal`, `CUB_color`)
- `caption_type`: defines how the caption and image relate to each other, choose from 
    - `consistent` (where the caption and image are consistent with each other), 
    - `inconsistent` (where the caption and image are inconsistent), 
    - `text_only` (where there is no image but only caption), 
    - `no_caption` (where there is no caption but only image)
- `modality_to_report`: defines the target modality, choose from `image` and `text`

 
## Precomputing Consistent and Inconsistent Multimodal Representations

  

Before running any analyses on models' internal representations, we first precompute last-token representations on consistent or inconsistent input image and caption pairs. 
```
python src/precompute_representations.py --config configs/precompute_representations.json 
``` 
  
Most of the arguments are the same as for behavioral evaluation, the `split` argument defines to compute representations of a dataset's `train` or `test` split.
  

## Probe and Cluster Fitting on Representations

  

After obtraining the representations for any model-dataset pair, we can conduct probing and clustering analyses on them.
 
### Training and Evaluating Unimodal Probe
```
python src/train_unimodal_probe.py --config configs/train_unimodal_probe.json 
``` 
### Training and Evaluating Consistency Probe
```
python src/train_consistency_probe.py --config configs/train_consistency_probe.json 
``` 

To replicate our results on k-fold evaluation on the **label class space**, use the following script and configuration:
```
python src/train_consistency_probe_with_fold.py --config configs/train_consistency_probe_with_fold.json 
``` 
### Fitting and Evaluating Clusters for Modality Salience
```
python src/cluster_analysis.py --config configs/clustering_analysis.json 
``` 
 

## Attention Head Attribution and Intervention
To run attribution and intervention on individual attention heads, use:
```
python src/single_head_attribution_intervention.py --config configs/attention_head_intervention.json 
``` 
 
To intervene on multiple attention heads, use:
```
python src/multi_head_attribution_intervention.py --config configs/multi_attention_head_intervention.json 
``` 

To see the effects of intervention on model behavior and representations, we support additional arguments to the previous `src/prompt_evaluation.py` and `src/precompute_representations.py` scripts:

```
{
    "seed": 42,
    "work_dir": ".",
    "model_name": "Qwen/Qwen2.5-VL-7B-Instruct",
    "dataset": "Pascal",
    "version": 0,
    "caption_type": "inconsistent",
    "modality_to_report": "image",
    "order": "icq",
    "n_candidates": 5,
    "is_assistant_prompt": 1,
    "is_explicit_helper": 0,
    "use_pointers": 1,
    "batch_size": 10
    "alpha": 10.0,
    "layer_idx": [11, 20],
    "head_idx": [14, 16]
}
```

Here, `alpha` deines the scalar that got multiplied to each attention heads' outputs. `layer_idx` and `head_idx` defines two list that indicates the heads to be intervened on. Here we are intervening `L11H14` and `L20H16`.


## How to Cite

```
@article{hua2025vision,
  title={How Do Vision-Language Models Process Conflicting Information Across Modalities?},
  author={Hua, Tianze and Yun, Tian and Pavlick, Ellie},
  journal={arXiv preprint arXiv:2507.01790},
  year={2025}
}
```
