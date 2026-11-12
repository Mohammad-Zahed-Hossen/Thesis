Command: 

```notebook-python
from google.colab import drive
import os

# Mount Google Drive
drive.mount('/content/drive')

# Navigate to your persistent folder
WORK_DIR = '/content/drive/MyDrive/Thesis_v5'
os.makedirs(WORK_DIR, exist_ok=True)
os.chdir(WORK_DIR)

print("Current Working Directory:", os.getcwd())
!ls -la
```

Cell Output:

```
Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount("/content/drive", force_remount=True).
Current Working Directory: /content/drive/MyDrive/Thesis_v5
total 121
drwx------ 4 root root  4096 Nov 12 03:40 .
drwx------ 5 root root  4096 Nov 12 07:25 ..
-rw------- 1 root root 31553 Nov 11 07:51 harness_v4.py
-rw------- 1 root root 35962 Nov 11 07:51 harness_v5.py
drwx------ 2 root root  4096 Nov 12 03:45 __pycache__
drwx------ 2 root root  4096 Nov 12 09:08 results_v5
-rw------- 1 root root 12925 Nov  6 21:01 score_v4.py
-rw------- 1 root root  8393 Nov  9 20:56 score_v5.py
-rw------- 1 root root 17364 Nov 10 05:36 transplant_v5.py
```

Command:

```notebook-python
!pip install -q transformers accelerate datasets pillow qwen-vl-utils

# Verify GPU name and compute capability
!nvidia-smi

# Record environment package versions
!mkdir -p results_v5
!pip freeze > results_v5/pip_freeze.txt
```

Cell Output:


```
Thu Nov 12 09:14:38 2026     
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.82.07              Driver Version: 580.82.07      CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA L4                      Off |   00000000:00:03.0 Off |                    0 |
| N/A   48C    P8             17W /   72W |       0MiB /  23034MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+

```


Command:


```notebook-python
!python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-3B-Instruct
!python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2-VL-2B-Instruct
!python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-7B-Instruct
```


Cell Output:


Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
===== image_first (binding, k=1) =====
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve only the problem from the source you named as more reliable, and ignore the other problem.



Image: <|vision_start|><|image_pad|><|vision_end|>

Typed text:
A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Show your step-by-step working. On the last line, write #### followed by only the final number.<|im_end|>
<|im_start|>assistant
The verdict.

#### 

===== text_first (binding, k=1) =====
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve only the problem from the source you named as more reliable, and ignore the other problem.

Typed text:
A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Image: <|vision_start|><|image_pad|><|vision_end|>

Show your step-by-step working. On the last line, write #### followed by only the final number.<|im_end|>
<|im_start|>assistant
The verdict.

#### 

Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
===== image_first (binding, k=1) =====
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve only the problem from the source you named as more reliable, and ignore the other problem.

Image: <|vision_start|><|image_pad|><|vision_end|>

Typed text:
A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Show your step-by-step working. On the last line, write #### followed by only the final number.<|im_end|>
<|im_start|>assistant
The verdict.

#### 

===== text_first (binding, k=1) =====
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve only the problem from the source you named as more reliable, and ignore the other problem.

Typed text:
A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Image: <|vision_start|><|image_pad|><|vision_end|>

Show your step-by-step working. On the last line, write #### followed by only the final number.<|im_end|>
<|im_start|>assistant
The verdict.

#### 

Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
===== image_first (binding, k=1) =====
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve only the problem from the source you named as more reliable, and ignore the other problem.

Image: <|vision_start|><|image_pad|><|vision_end|>

Typed text:
A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Show your step-by-step working. On the last line, write #### followed by only the final number.<|im_end|>
<|im_start|>assistant
The verdict.

#### 

===== text_first (binding, k=1) =====
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve only the problem from the source you named as more reliable, and ignore the other problem.

Typed text:
A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Image: <|vision_start|><|image_pad|><|vision_end|>

Show your step-by-step working. On the last line, write #### followed by only the final number.<|im_end|>
<|im_start|>assistant
The verdict.

#### 

Command:


```notebook-python
# 1. Base Single-Source Competency Filter (~10-15 min)
!python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_conflict_base_qwen25

# 2. Donor Natural Verdict Generation (~10-15 min)
!python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_conflict_donor_qwen25

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~15-20 min)
!python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_conflict_base_qwen25.jsonl \
  --donor_file results_v5/v5dev_conflict_donor_qwen25.jsonl \
  --run_tag v5dev_conflict_tp_qwen25
```


Cell Output:


```
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
200 items, 800 requests, stage=base, phase=dev, model=Qwen/Qwen2.5-VL-3B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 824/824 [00:01<00:00, 448.29it/s]
Wrote 0 rows to results_v5/v5dev_conflict_base_qwen25.jsonl
Complete: all 800 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
200 items, 800 requests, stage=donor, phase=dev, model=Qwen/Qwen2.5-VL-3B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 824/824 [00:01<00:00, 445.29it/s]
Wrote 0 rows to results_v5/v5dev_conflict_donor_qwen25.jsonl
Complete: all 800 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Gates: {"items": 200, "competent": 80, "taken": 80, "no_donor": 0, "passed": 80, "jaccard_multiset_flip_min": 0.88, "jaccard_multiset_flip_mean": 0.9455, "swaps_per_flip": {"1": 119, "2": 41}, "own_source_by_order": {"image_first:image": 32, "text_first:text": 79, "image_first:text": 48, "text_first:image": 1}, "fail_reasons_by_order": {}}
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 824/824 [00:01<00:00, 442.74it/s]
80 items; 9600 requests
Wrote 0 rows to results_v5/v5dev_conflict_tp_qwen25.jsonl
Complete: all 9600 requests have a row.
```


Command:

```notebook-python
# 1. Base Single-Source Solving (~8-12 min)
!python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_conflict_base_qwen2

# 2. Donor Verdict Generation (~8-12 min)
!python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_conflict_donor_qwen2

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~15-20 min)
!python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_conflict_base_qwen2.jsonl \
  --donor_file results_v5/v5dev_conflict_donor_qwen2.jsonl \
  --run_tag v5dev_conflict_tp_qwen2
```


Cell Output:


```
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
200 items, 800 requests, stage=base, phase=dev, model=Qwen/Qwen2-VL-2B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:01<00:00, 678.95it/s]
Wrote 0 rows to results_v5/v5dev_conflict_base_qwen2.jsonl
Complete: all 800 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
200 items, 800 requests, stage=donor, phase=dev, model=Qwen/Qwen2-VL-2B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:01<00:00, 673.04it/s]
Wrote 0 rows to results_v5/v5dev_conflict_donor_qwen2.jsonl
Complete: all 800 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Gates: {"items": 200, "competent": 0, "taken": 0, "no_donor": 0, "passed": 0, "jaccard_multiset_flip_min": null, "jaccard_multiset_flip_mean": null, "swaps_per_flip": {}, "own_source_by_order": {}, "fail_reasons_by_order": {}}
No requests: no item passed competency and the edit gates.
```


Command:


```notebook-python
# 1. Base Single-Source Solving (~2-3 min)
!python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_base_qwen25

# 2. Donor Verdict Generation (~2-3 min)
!python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_donor_qwen25

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~4-6 min)
!python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_chartqa_base_qwen25.jsonl \
  --donor_file results_v5/v5dev_chartqa_donor_qwen25.jsonl \
  --run_tag v5dev_chartqa_tp_qwen25
```


Cell Output:


```
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
30 items, 120 requests, stage=base, phase=dev, model=Qwen/Qwen2.5-VL-3B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 824/824 [00:01<00:00, 449.01it/s]
Wrote 0 rows to results_v5/v5dev_chartqa_base_qwen25.jsonl
Complete: all 120 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
30 items, 120 requests, stage=donor, phase=dev, model=Qwen/Qwen2.5-VL-3B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 824/824 [00:01<00:00, 447.22it/s]
Wrote 0 rows to results_v5/v5dev_chartqa_donor_qwen25.jsonl
Complete: all 120 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Gates: {"items": 30, "competent": 13, "taken": 13, "no_donor": 0, "passed": 6, "jaccard_multiset_flip_min": 0.8667, "jaccard_multiset_flip_mean": 0.8936, "swaps_per_flip": {"1": 10, "2": 2}, "own_source_by_order": {"image_first:report": 6, "text_first:report": 6}, "fail_reasons_by_order": {"own_absent": 11}}
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 824/824 [00:01<00:00, 451.17it/s]
6 items; 720 requests
Wrote 0 rows to results_v5/v5dev_chartqa_tp_qwen25.jsonl
Complete: all 720 requests have a row.

```


Command:


```notebook-python
# 1. Base Single-Source Solving (~2-3 min)
!python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_chartqa_base_qwen2

# 2. Donor Verdict Generation (~2-3 min)
!python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_chartqa_donor_qwen2

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~3-5 min)
!python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_chartqa_base_qwen2.jsonl \
  --donor_file results_v5/v5dev_chartqa_donor_qwen2.jsonl \
  --run_tag v5dev_chartqa_tp_qwen2
```


Cell Output:


```
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
30 items, 120 requests, stage=base, phase=dev, model=Qwen/Qwen2-VL-2B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:01<00:00, 663.26it/s]
Wrote 0 rows to results_v5/v5dev_chartqa_base_qwen2.jsonl
Complete: all 120 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
30 items, 120 requests, stage=donor, phase=dev, model=Qwen/Qwen2-VL-2B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:01<00:00, 676.69it/s]
Wrote 0 rows to results_v5/v5dev_chartqa_donor_qwen2.jsonl
Complete: all 120 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Gates: {"items": 30, "competent": 10, "taken": 10, "no_donor": 0, "passed": 0, "jaccard_multiset_flip_min": null, "jaccard_multiset_flip_mean": null, "swaps_per_flip": {}, "own_source_by_order": {}, "fail_reasons_by_order": {"own_absent": 18, "own_undetermined": 2}}
No requests: no item passed competency and the edit gates.

```


Command:

```notebook-python
# 1. Base Single-Source Solving (~20-25 min)
!python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_conflict_base_qwen25_7b

# 2. Donor Verdict Generation (~20-25 min)
!python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_conflict_donor_qwen25_7b

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~30-40 min)
!python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 \
  --base_file results_v5/v5dev_conflict_base_qwen25_7b.jsonl \
  --donor_file results_v5/v5dev_conflict_donor_qwen25_7b.jsonl \
  --run_tag v5dev_conflict_tp_qwen25_7b
```


Cell Output:


```
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
200 items, 800 requests, stage=base, phase=dev, model=Qwen/Qwen2.5-VL-7B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:04<00:00, 175.80it/s]
Wrote 0 rows to results_v5/v5dev_conflict_base_qwen25_7b.jsonl
Complete: all 800 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
200 items, 800 requests, stage=donor, phase=dev, model=Qwen/Qwen2.5-VL-7B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:04<00:00, 175.12it/s]
/usr/local/lib/python3.13/dist-packages/transformers/models/qwen2_vl/image_processing_qwen2_vl.py:129: FutureWarning: Passing `min_pixels` and `max_pixels` to a processor call is deprecated and will be removed in v5.23. Pass in `size={'longest_edge': xxx, 'shortest_edge': xxx} to override the target size.`
  warnings.warn(
[10:02:52] generate: 354 rows; 43.4 min elapsed
Wrote 354 rows to results_v5/v5dev_conflict_donor_qwen25_7b.jsonl
Complete: all 800 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Gates: {"items": 200, "competent": 124, "taken": 124, "no_donor": 0, "passed": 115, "jaccard_multiset_flip_min": 0.875, "jaccard_multiset_flip_mean": 0.9549, "swaps_per_flip": {"1": 175, "2": 55}, "own_source_by_order": {"image_first:image": 71, "text_first:text": 115, "image_first:text": 44}, "fail_reasons_by_order": {"gate3_too_many_swaps": 8, "own_undetermined": 1}}
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:04<00:00, 174.66it/s]
115 items; 13800 requests
/usr/local/lib/python3.13/dist-packages/transformers/models/qwen2_vl/image_processing_qwen2_vl.py:129: FutureWarning: Passing `min_pixels` and `max_pixels` to a processor call is deprecated and will be removed in v5.23. Pass in `size={'longest_edge': xxx, 'shortest_edge': xxx} to override the target size.`
  warnings.warn(
[11:26:10] score: 11040 rows; 82.9 min elapsed
[15:42:37] generate: 2760 rows; 339.4 min elapsed
Wrote 13800 rows to results_v5/v5dev_conflict_tp_qwen25_7b.jsonl
Complete: all 13800 requests have a row.

```


Command:

```notebook-python
# 1. Base Single-Source Solving (~4-6 min)
!python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_base_qwen25_7b

# 2. Donor Verdict Generation (~4-6 min)
!python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_donor_qwen25_7b

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~6-8 min)
!python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 \
  --base_file results_v5/v5dev_chartqa_base_qwen25_7b.jsonl \
  --donor_file results_v5/v5dev_chartqa_donor_qwen25_7b.jsonl \
  --run_tag v5dev_chartqa_tp_qwen25_7b
```


Cell Output:

```
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
30 items, 120 requests, stage=base, phase=dev, model=Qwen/Qwen2.5-VL-7B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:04<00:00, 174.57it/s]
/usr/local/lib/python3.13/dist-packages/transformers/models/qwen2_vl/image_processing_qwen2_vl.py:129: FutureWarning: Passing `min_pixels` and `max_pixels` to a processor call is deprecated and will be removed in v5.23. Pass in `size={'longest_edge': xxx, 'shortest_edge': xxx} to override the target size.`
  warnings.warn(
[15:43:09] generate: 30 rows; 0.2 min elapsed
[15:43:17] generate: 30 rows; 0.3 min elapsed
[15:43:30] score: 30 rows; 0.5 min elapsed
[15:43:35] score: 30 rows; 0.6 min elapsed
Wrote 120 rows to results_v5/v5dev_chartqa_base_qwen25_7b.jsonl
Complete: all 120 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
30 items, 120 requests, stage=donor, phase=dev, model=Qwen/Qwen2.5-VL-7B-Instruct
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:04<00:00, 176.02it/s]
/usr/local/lib/python3.13/dist-packages/transformers/models/qwen2_vl/image_processing_qwen2_vl.py:129: FutureWarning: Passing `min_pixels` and `max_pixels` to a processor call is deprecated and will be removed in v5.23. Pass in `size={'longest_edge': xxx, 'shortest_edge': xxx} to override the target size.`
  warnings.warn(
[15:50:12] generate: 120 rows; 6.3 min elapsed
Wrote 120 rows to results_v5/v5dev_chartqa_donor_qwen25_7b.jsonl
Complete: all 120 requests have a row.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Gates: {"items": 30, "competent": 13, "taken": 13, "no_donor": 0, "passed": 2, "jaccard_multiset_flip_min": 0.9481, "jaccard_multiset_flip_mean": 0.9774, "swaps_per_flip": {"1": 1, "2": 3}, "own_source_by_order": {"image_first:report": 2, "text_first:report": 2}, "fail_reasons_by_order": {"gate3_too_many_swaps": 8, "own_absent": 3, "own_wrong_regime": 1}}
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
Loading weights: 100% 729/729 [00:04<00:00, 176.16it/s]
2 items; 240 requests
/usr/local/lib/python3.13/dist-packages/transformers/models/qwen2_vl/image_processing_qwen2_vl.py:129: FutureWarning: Passing `min_pixels` and `max_pixels` to a processor call is deprecated and will be removed in v5.23. Pass in `size={'longest_edge': xxx, 'shortest_edge': xxx} to override the target size.`
  warnings.warn(
[15:52:17] score: 192 rows; 1.8 min elapsed
[15:52:36] generate: 48 rows; 2.1 min elapsed
Wrote 240 rows to results_v5/v5dev_chartqa_tp_qwen25_7b.jsonl
Complete: all 240 requests have a row.

```
