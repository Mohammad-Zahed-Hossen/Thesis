
Ran command: `python -c "
import urllib.request

url = 'https://openaccess.thecvf.com/content/WACV2026/papers/Fahim_BanglaProtha_Evaluating_Vision_Language_Models_in_Underrepresented_Long-tail_Cultural_Contexts_WACV_2026_paper.pdf'
pdf_path = r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper.pdf'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp, open(pdf_path, 'wb') as f:
        f.write(resp.read())
    print('PDF downloaded successfully, size:', len(open(pdf_path, 'rb').read()))
except Exception as e:
    print('Error downloading PDF:', e)
"`Checked task Download BanglaProtha WACV 2026 PDF Used tool: search_web Used tool: read_url_content Ran command:`python -c "
for mod in ['pypdf', 'pypdf2', 'pdfplumber', 'fitz']:
    try:
        __import__(mod)
        print('Available:', mod)
    except ImportError:
        pass
"`Ran command:`python -c "
import pdfplumber

pdf_path = r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper.pdf'
with pdfplumber.open(pdf_path) as pdf:
    print('Total pages:', len(pdf.pages))
    full_text = ''
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ''
        if any(w in text.lower() for w in ['dataset', 'split', 'train', 'test', 'statistics', 'images', 'questions', 'unique']):
            print(f'--- PAGE {i+1} ---')
            for line in text.split('\n'):
                if any(k in line.lower() for k in ['image', 'question', 'split', 'dataset', 'total', 'train', 'val', 'test', 'distractor', 'table']):
                    print(line[:120])
"`Ran command:`python -c "
import pdfplumber

pdf_path = r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper.pdf'
out_path = r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper_text.txt'

with pdfplumber.open(pdf_path) as pdf, open(out_path, 'w', encoding='utf-8') as f:
    for i, page in enumerate(pdf.pages):
        f.write(f'=== PAGE {i+1} ===\n')
        text = page.extract_text() or ''
        f.write(text + '\n\n')
print('Extracted full text!')
"`Ran command:`python -c "
with open(r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper_text.txt', encoding='utf-8') as f:
    text = f.read()

import re

# Look for Section 3 / dataset creation / statistics

for m in re.finditer(r'(=== PAGE \d+ ===[\s\S]{1,3000}?(?:dataset|statistics|curation|annotation|split))', text, re.IGNORECASE):
    print(m.group(0)[:500])
    print('='*40)
"`Ran command:`python -c "
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper_text.txt', encoding='utf-8') as f:
    text = f.read()

# Let's find sections mentioning numbers of images, questions, splits, etc.

lines = text.split('\n')
for i, l in enumerate(lines):
    if any(term in l.lower() for term in ['dataset statistics', '3. banglaprotha', '3.1', '3.2', '3.3', 'data curation', 'data collection', 'train', 'test split', 'split']):
        print(f'Line {i}: {l}')
        for j in range(max(0, i-2), min(len(lines), i+15)):
            print(f'   {lines[j]}')
        print('-'*50)
"`Ran command:`python -c "
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper_text.txt', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== PAGE ')
for p in pages:
    if p.startswith('2 ') or p.startswith('3 ') or p.startswith('4 '):
        print('=== PAGE ' + p[:4000])
"`Viewed content.md:1-150 Ran command:`python -c "
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper_text.txt', encoding='utf-8') as f:
    text = f.read()

# Search for appendix sections mentioning splits or data details

import re
matches = re.findall(r'.{0,100}(?:train-test|80:20|split|deduplicat|leakage|overlap|train split|test split).{0,100}', text, re.IGNORECASE)
for m in matches[:30]:
    print('-->', m.strip())
"`Ran command:`python -c "
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper_text.txt', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== PAGE ')
for p in pages:
    if p.startswith('9 ') or p.startswith('10 ') or p.startswith('11 '):
        print('=== PAGE ' + p[:3000])
"`Ran command:`python -c "
import urllib.request, json

# Kaggle dataset API endpoint

url = 'https://www.kaggle.com/api/v1/datasets/view/sourove/bangla-culturally-relevant-vqa'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(json.dumps(data, indent=2)[:1000])
except Exception as e:
    print('Error:', e)
"`Ran command:`python -c "
import urllib.request, json

url = 'https://www.kaggle.com/api/v1/datasets/list-files/sourove/bangla-culturally-relevant-vqa'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for f in data.get('datasetFiles', []):
            print(f.get('name'), f.get('totalBytes'), f.get('creationDate'))
except Exception as e:
    print('Error:', e)
"`Used tool: search_web Used tool: search_web Used tool: search_web Ran command:`python -c "
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha_paper_text.txt', encoding='utf-8') as f:
    text = f.read()

for line in text.split('\n'):
    if any(k in line.lower() for k in ['80:20', 'train-test', 'test split', 'data leakage', 'stratified', 'leakage', 'image-level']):
        print(line)
"`Ran command:`Get-ChildItem -Recurse "C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha\LLaMA-Factory\data"`Ran command:`python -c "
import json
with open(r'C:\Users\Admin\.gemini\antigravity\brain\3b2d3c7e-18ef-4a45-8027-341c17d9ca2e\scratch\BanglaProtha\LLaMA-Factory\data\dataset_info.json') as f:
    d = json.load(f)
for k in d:
    if any(term in k.lower() for term in ['bangla', 'protha', 'cultur']):
        print(k, d[k])
"`Ran command:`git log -p -n 5`Ran command:`git log --oneline`Ran command:`git fetch --unshallow && git log --oneline`
Searched for "BICR"
Viewed Adversarial%20literature%20autopsy.md:268-340
Searched for "CulturalMenuBench"
Viewed bangla-cultural-vlm-synthesis.md:70-115

# Final Boundary Verification: Candidate Proposal 3

**Candidate Formulation under Evaluation:**
*A diagnostic audit of visual grounding vs. language-prior reliance for selective prediction in Vision-Language Models (VLMs) under regional/cultural distribution shift (using Bengali cultural benchmarks).*

---

## 1. Verification of BanglaProtha Dataset

Direct inspection was performed on:

* The primary WACV 2026 paper: [Fahim et al., *BanglaProtha: Evaluating Vision Language Models in Underrepresented Long-tail Cultural Contexts*, IEEE/CVF WACV 2026, pp. 1159–1169](https://openaccess.thecvf.com/content/WACV2026/papers/Fahim_BanglaProtha_Evaluating_Vision_Language_Models_in_Underrepresented_Long-tail_Cultural_Contexts_WACV_2026_paper.pdf)
* The official code repository: [`farhanishmam/BanglaProtha`](https://github.com/farhanishmam/BanglaProtha)
* The official dataset repository: [Kaggle: `sourove/bangla-culturally-relevant-vqa`](https://www.kaggle.com/datasets/sourove/bangla-culturally-relevant-vqa) (Creator: Md Sakib Ul Rahman Sourove, Author #2; 2.18 GB)

### Property-by-Property Audit


| Property                                         | Finding                                           | Status                                    | Exact Source & Evidence                                                                                                                                                                                                                                               |
| :------------------------------------------------- | :-------------------------------------------------- | :------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Exact unique images**                          | **6,942 images**                                  | **VERIFIED**                              | WACV 2026 paper, Page 3, Table 1: BNATURE (2,079), BORNON (1,402), BANGLALEKHA (2,541), BengaliWebsites (920). Total = 6,942.                                                                                                                                         |
| **Exact questions**                              | **8,034 questions**                               | **VERIFIED**                              | WACV 2026 paper, Page 3, Table 1: BNATURE (2,517), BORNON (1,638), BANGLALEKHA (2,816), BengaliWebsites (1,063). Total = 8,034.                                                                                                                                       |
| **Official train/val/test structure**            | **80:20 Train/Test split; No official Val split** | **VERIFIED (Train/Test) / UNKNOWN (Val)** | WACV 2026 paper, Page 3, §3:*"Finally, BANGLAPROTHA is divided into the standard 80:20 train-test splits."* (~6,427 train, ~1,607 test). No separate validation split is documented in the paper text.                                                               |
| **Same image in multiple questions**             | **YES (Overall ratio 1.16 : 1)**                  | **VERIFIED**                              | WACV 2026 paper, Page 3, Table 1: 8,034 questions across 6,942 images. At least 1,092 questions share an underlying image with another question. Ratio varies from 1.11 (BanglaLekha) to 1.21 (BNature).                                                              |
| **Identical images across train/test splits**    | **Undocumented split grouping**                   | **UNKNOWN / UNVERIFIED**                  | The paper does not state whether the 80:20 partition was grouped by image hash or split randomly by question. If split randomly by question, ~16% to 20% of test questions share an image with the training set.                                                      |
| **Near-duplicate images**                        | **Undocumented; high likelihood**                 | **UNKNOWN (Undocumented)**                | Images were collected from existing captioning datasets and web-scraped (2,800 images). No perceptual hashing (pHash) or near-duplicate deduplication is reported. Cultural landmarks and dishes naturally contain near-duplicate angles.                             |
| **Same entity across splits**                    | **YES (Practically certain)**                     | **INFERRED**                              | With 8,034 questions across 9 cultural domains (Food, Clothing, Social Life, Arts & History, etc.), common cultural entities (e.g.,*Nakshi Kantha*, *Shorshe Ilish*, *Shaheed Minar*) inevitably appear across multiple distinct questions and images in both splits. |
| **Suitability for leakage-resistant evaluation** | **SUITABLE ONLY with custom image-grouped split** | **VERIFIED CONDITIONALLY**                | Because each sample in the dataset contains a discrete`filename` attribute, a researcher can bypass the unverified 80:20 split and enforce a strictly image-disjoint, entity-stratified calibration/test partition.                                                   |

### Evaluation Threat Analysis of the Four Image Hazards

1. **Multiple questions on the same image:**
   *Threat Level: Low (Manageable).* Standard in VQA benchmarks (e.g., VQA v2). It does not threaten zero-shot evaluation, and only threatens calibration if questions sharing the same image are split across calibration and test sets.
2. **Duplicate images across splits:**
   *Threat Level: Fatal for fine-tuning or split calibration; Neutral for pure zero-shot.* If an uncertainty probe or conformal threshold is tuned on Split A and evaluated on Split B with duplicate images, the probe measures visual memorization, not calibration. **Control:** Must re-split by unique image filename/hash.
3. **Same entity across different images:**
   *Threat Level: High (Scientific Confound).* This is not data leakage, but the central mechanism under study: if the model memorized the entity name from textual web pretraining, it will guess the entity correctly across *all* images of that entity using language priors alone, decoupling accuracy from visual perception.
4. **Near-duplicate images:**
   *Threat Level: Moderate.* If the base foundation model saw near-identical web images of famous landmarks or dishes during pretraining, its visual recognition is memorized rather than generalizable.

---

## 2. Verification of the Blank-Image / Visual-Sensitivity Premise

Primary literature establishes that input perturbation (blank-image, masked-image, noise injection) is a standard method to diagnose VLM visual reliance:

1. **BICR (*Grounded or Guessing? LVLM Confidence Estimation via Blind-Image Contrastive Ranking*, Khanmohammadi et al., `arXiv:2605.10893`, May 2026):**
   * *Exact perturbation:* Blank black image ($I = \mathbf{0}$) replacing the genuine image while keeping the prompt identical.
   * *Signal measured:* Pairwise ranking loss on intermediate residual hidden states: $\mathcal{L}_{\text{rank}} = \max(0, \gamma - (s(h_{\text{orig}}) - s(h_{\text{blank}})))$.
   * *Does it predict correctness?* Yes on standard Western benchmarks (GQA, POPE, MMMU-Pro). BICR reduced ECE to 0.056 (vs. 0.078 for uncalibrated hidden states) and improved AUROC by +3.32 points.
   * *Reported limitations:* The authors explicitly define blank-image contrast as an **operational proxy**, not a direct semantic grounding measurement. They explicitly note that **multilingual, non-English, and culturally shifted transfer was untested**.
2. **BCEA (*Look Again Before You Abstain*, Xu et al., `arXiv:2606.16667`, June 2026):**
   * *Exact perturbation:* Masked-image ablation and localized patch masking.
   * *Signal measured:* Logit drop on answer tokens between full image and masked image.
   * *Reported limitations:* Global image-dependence scores fail for relational and fine-grained visual claims; claim-level interventions are required.
3. **ChitraMiti (`arXiv:2609.12509`, September 2026):**
   * *Exact perturbation:* Modality ablation (text-only vs. image-only vs. paired) on Bengali visual reasoning.
   * *Finding:* Proves that open VLMs frequently suffer from modality imbalance in Bengali prompts, ignoring visual tokens in favor of textual heuristics.
4. **Visual Contrastive Decoding (VCD, Leng et al., CVPR 2024):**
   * *Exact perturbation:* Gaussian noise injection into visual tokens to contrast against language-prior generation.

### Scientific Threshold Status

> [!IMPORTANT]
> **Explicit Verification:** Any threshold stating that *">85% unchanged predictions means the model is blind"* or that *"$\Delta_{\text{logit}} > 0.30$ means sufficient visual sensitivity"* is a **proposed experimental heuristic, NOT a verified scientific threshold**.
>
> Primary literature (BICR, VCD, ChitraMiti, BanglaProtha) does not define binary cutoff thresholds for visual blindness. In the literature, visual reliance is continuously distributed and evaluated via comparative ranking metrics (AUROC, Kendall’s $\tau$, ECE, AUGRC) against text-only and unperturbed baselines.

---

## 3. Verification of the Actual Scientific Gap

### Narrow Pre-emption Check

> **The Targeted Question:** Under cultural or regional distribution shift, does visual-grounding sensitivity remain a useful predictor of answer reliability, or can language/cultural priors produce correct answers that are weakly dependent on the image?

Searching across literature covering *multimodal shortcutting, unimodal reliance, correct-but-ungrounded answers, and knowledge-application gaps*:

1. **`CulturalMenuBench` (`arXiv:2609.03526`, Sep 2026):**
   * *What they tested:* Evaluated 18 regional cuisines across 10 languages.
   * *Finding:* Established the **cultural knowledge-application gap**: models score >94% when presented with cultural food names in text, but drop to $\le 56\%$ when presented with images. Textual recognition outperformed visual recognition by +7 to +18 points.
   * *Overlap:* Proves that cultural knowledge resides in the text backbone and is weakly activated by visual tokens.
   * *Remaining Gap:* CulturalMenuBench evaluated raw accuracy only. It did **not** evaluate confidence calibration, uncertainty estimation, selective prediction, or risk-coverage formalisms.
2. **`SPC` (Selective Prior Calibration, `arXiv:2607.29240`, Jul 2026):**
   * *What they tested:* Conflict between commonsense language priors and visual evidence using counterfactual images (e.g., 6-fingered hands).
   * *Finding:* Language priors actively override visual tokens during decoding.
   * *Remaining Gap:* Tested synthetic visual counterfactuals in English; did not test regional cultural distribution shifts or selective abstention.
3. **`Evidence-Order Calibration` (`arXiv:2609.09184`, Sep 2026):**
   * *What they tested:* Visual reasoning under evidence degradation on English GQA.
   * *Finding:* Evidence-monotonicity violations (EMVR = 0.436) are separable from correctness ranking; evidence-supervised heads failed to beat native MaxProb softmax for risk ranking.
   * *Remaining Gap:* Evaluated English spatial reasoning, not cultural entity recognition under asymmetric pretraining.
4. **`BICR` (`arXiv:2605.10893`, May 2026):**
   * *What they tested:* Penalizing ungrounded predictions using blank-image ranking.
   * *Fatal Assumption in BICR:* BICR assumes that ungrounded answers are *incorrect hallucinations* and should be suppressed. In cultural domains (*CulturalMenuBench*, *BanglaVerse*), models frequently guess the *correct* cultural entity via textual priors without visual grounding. BICR’s penalty would actively suppress correct cultural predictions.

### Pre-emption Verdict: NOT PRE-EMPTED

The fundamental scientific tension—**whether visual grounding penalties degrade selective prediction in culturally shifted domains because correct answers frequently rely on ungrounded language priors**—has not been tested by any published work.

---

## 4. Verification of the Strongest Competing Explanations

Can the expected experimental outcome be fully explained by simpler confounders?


| Competing Explanation                     | Does It Explain the Outcome?                                                                 | How the Diagnostic Experiment Distinguishes It                                                                                                                                                                                                                                                                                                                                                        |
| :------------------------------------------ | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Ordinary OOD Epistemic Uncertainty**    | Partially. OOD shift inflates overall uncertainty.                                           | **Distinguished by comparing against Temperature-Scaled Softmax.** If a standard post-hoc temperature-scaled softmax baseline achieves identical AUGRC to visual contrastive probes ($\Delta_{\text{blank}}$), the effect is generic OOD uncertainty, not modality imbalance.                                                                                                                         |
| **Missing Cultural Parametric Knowledge** | High competitor. If the model never learned the entity, it fails regardless of vision.       | **Distinguished by a Text-Only LLM Baseline.** Present the question and options without an image ($I = \emptyset$). If text-only accuracy is high (e.g., 70%) while visual VLM accuracy is low (e.g., 40%), the knowledge exists in the text backbone but fails visual grounding (the knowledge-application gap). If text-only accuracy is chance level (25%), the failure is a total knowledge void. |
| **Bengali Tokenization Fragmentation**    | Moderate competitor. Rare Bengali words fragment into byte tokens, distorting probabilities. | **Distinguished by Single-Token Option Logits.** By framing the task as 4-way Multiple-Choice QA predicting option letters (A, B, C, D) using the exact protocol from `infer.py`, the target is an invariant single ASCII token, completely bypassing Bengali text generation length and morphological tokenization artifacts.                                                                        |
| **Positional & Distractor Biases**        | Minor competitor. Models prefer option 'A' or certain common words.                          | **Distinguished by Option Permutation.** Evaluating over 4-way option permutations (as established in BanglaProtha §D.4) isolates positional letter preference from entity belief.                                                                                                                                                                                                                   |

---

## 5. Audit of the Proposed Scientific Contribution

Evaluating strictly the **diagnostic formulation** (inference-only; no RAG; no engineering pipeline):

### If the visual-grounding signal works (Hypothesis $H_1$):

* **Established Knowledge:** Blank-image contrastive delta ($\Delta_{\text{blank}}$) reliably separates correct from incorrect predictions on Bengali cultural entities, improving selective risk-coverage (AUGRC) over raw softmax.
* **Significance:** Proves that despite asymmetric pretraining, correct VLM predictions on low-resource cultural concepts remain causally dependent on visual features. It demonstrates that contrastive visual reliance probes (*BICR*) transfer zero-shot across linguistic and geographic distribution shifts without requiring retraining.

### If the visual-grounding signal fails (Hypothesis $H_0$):

* **Established Knowledge:** Blank-image contrastive delta fails to improve, or actively harms, selective risk-coverage compared to simple temperature-scaled softmax.
* **Significance:** Uncovers the **failure boundary of visual-grounding confidence**. It demonstrates that in culturally shifted domains, foundation VLMs operate under an asymmetric cross-modal regime: correct answers are decoupled from visual evidence because the model answers via ungrounded textual memory. Penalizing visually ungrounded answers suppresses correct predictions. This empirically refutes the assumption that visual grounding is a universal requirement for multimodal reliability.

### Would either result be scientifically meaningful outside Bangladesh/Bengali?

**YES.**
The broader scientific phenomenon is **Unimodal Prior Decoupling under Asymmetric Cross-Modal Pretraining**. This condition occurs across all global low-resource cultures, indigenous artifacts, rare biological taxa, and specialized technical domains where models have acquired web-scraped textual descriptions but possess minimal paired visual data. Bengali cultural data serves as an empirical exemplar of this general representational condition.

---

## 6. Closest-Papers Verification Table


| Paper                                                                     | Exact Research Question                                                                                                   | Method                                                                                                                                                                                                                                                                                                | Dataset / Domain                                                                                             | Main Finding                                                                                                 | Overlap with Proposal                                                           | Live Remaining Gap                                                                                     |
| :-------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------- |
| **BICR** (Khanmohammadi et al., `arXiv:2605.10893`, May 2026)             | Can contrastive ranking between real and blank images separate visually grounded confidence from language-prior guessing? | Pairwise ranking loss on hidden states ($h_{\text{orig}}$ vs. $h_{\text{blank}}$); linear probes. | GQA, POPE, MMMU-Pro, MME-Finance (English). | Improves AUROC (+3.32) and ECE (0.056); proves ungrounded answers can be detected. | Identical visual ablation mechanism ($\Delta_{\text{blank}}$). | Untested on multilingual, non-Western cultural entities where correct answers may rely on ungrounded priors. |                                                                                                              |                                                                                 |                                                                                                        |
| **SIEVES** (Rodriguez & Rohrbach, `arXiv:2604.25855`, Apr 2026)           | Does scoring visual localization quality and evidence-answer coherence improve selective VQA under distribution shift?    | Auxiliary selector network scoring$c_{\text{corr}}, c_{\text{loc}}, c_{\text{coh}}$ from image crops and CoT. | V* Bench, VizWiz, AdVQA, HR-Bench (English). | Triples coverage at low error tolerances ($C@1\%$); generalizes OOD.                                                                   | Identical selective prediction formalisms (AURC, AUGRC).                                                     | Requires explicit visual crops and Western spatial reasoning; does not test cultural parametric entity gaps. |                                                                                 |                                                                                                        |
| **BCEA** (Xu et al., `arXiv:2606.16667`, Jun 2026)                        | Can an adaptive decision rule (Answer / Abstain / Acquire) provide distribution-free risk guarantees for VLMs?            | Conformal risk control over logit drops under image masking; budgeted visual acquisition.                                                                                                                                                                                                             | POPE, MS-COCO claims (English).                                                                              | Guarantees error bounds$\le 5\%$ while maximizing coverage via evidence acquisition.                         | Uses visual perturbation to trigger abstention.                                 | Evaluates binary object-existence claims on COCO; does not evaluate cultural world knowledge or MCQA.  |
| **CulturalMenuBench** (He et al., `arXiv:2609.03526`, Sep 2026)           | Do VLMs fail in cultural understanding because they lack cultural knowledge or because they fail to activate it visually? | Visual trojan testing; comparing entity text names vs. visual food presentation across 18 regions.                                                                                                                                                                                                    | 10 languages, 18 regions (cultural cuisine).                                                                 | Reveals a massive knowledge-application gap: >94% on text drops to$\le 56\%$ on images.                      | Demonstrates the exact decoupling of textual knowledge from visual recognition. | Evaluated accuracy only; zero uncertainty estimation, confidence calibration, or selective prediction. |
| **BanglaProtha** (Fahim et al., IEEE/CVF WACV 2026)                       | How do open and closed VLMs perform on long-tail Bengali cultural contexts with semantically close distractors?           | 4-way MCQA evaluation under 5 prompting and 3 fine-tuning strategies.                                                                                                                                                                                                                                 | 6,942 images, 8,034 questions across 9 Bengali cultural domains.                                             | Monolingual VLMs fail (<42%); multilingual models exhibit strong positional bias; fine-tuning helps.         | Primary evaluation benchmark providing verified cultural visual MCQA.           | Evaluated accuracy only; zero calibration, selective prediction, or visual perturbation probing.       |
| **BanglaVerse** (Sayeedi et al., `arXiv:2603.21165`, Mar 2026)            | What are the failure modes of VLMs on comprehensive Bengali cultural multimodal understanding?                            | Broad evaluation across 9 domains; manual failure coding.                                                                                                                                                                                                                                             | 1,152 images, 32.2K dialectal/multilingual QA items.                                                         | 42.6% of errors are local entity misidentifications; concludes bottleneck is missing knowledge.              | Documents real-world Bengali entity recognition failures.                       | Evaluated generation accuracy only; no uncertainty quantification or selective prediction.             |
| **ChitraMiti** (Saha et al., `arXiv:2609.12509`, Sep 2026)                | Do Bengali VLMs suffer from modality imbalance in visual reasoning tasks?                                                 | Modality ablation (text-only vs. image-only) on Bengali geometric diagrams.                                                                                                                                                                                                                           | Bengali geometric reasoning diagrams.                                                                        | Accuracy drops when visual relations are swapped, showing weak visual reliance.                              | Uses modality ablation in Bengali.                                              | Restricted to geometric reasoning; no cultural entities, calibration, or selective prediction.         |
| **Evidence-Order Calibration** (Kim et al., `arXiv:2609.09184`, Sep 2026) | Does evidence consistency correlate with answer correctness in selective visual reasoning?                                | Reliability heads trained on hidden states and token entropy under progressive visual masking.                                                                                                                                                                                                        | English GQA / VQA.                                                                                           | Proves evidence-supervised heads fail to outperform raw MaxProb softmax for risk ranking.                    | Tests selective prediction under evidence loss.                                 | Evaluated on English spatial reasoning; does not test cultural knowledge asymmetry.                    |

---

# Final Output

### A. What Is Now Verified?

1. **BanglaProtha Scale and Structure:** Verified directly from Fahim et al. (WACV 2026) that the dataset contains **6,942 unique images** and **8,034 multiple-choice questions** across 9 cultural domains, with an overall question-to-image ratio of 1.16:1.
2. **Kaggle Dataset Availability:** Verified that the complete 2.18 GB dataset is hosted on Kaggle (`sourove/bangla-culturally-relevant-vqa`, version 5) by author Md Sakib Ul Rahman Sourove.
3. **Blank-Image Probing Validity:** Verified from BICR (`arXiv:2605.10893`) that blank-image contrastive hidden-state probing is an established operational proxy for visual reliance that improves calibration on Western VQA benchmarks.
4. **Cultural Knowledge-Application Decoupling:** Verified from CulturalMenuBench (`arXiv:2609.03526`) that in culturally shifted domains, models frequently retain parametric knowledge in their language backbones that fails to activate from visual tokens (+7 to +18 point text-vs-vision gap).
5. **Open Interaction Gap:** Verified that no existing paper has tested whether visual-grounding penalties (*BICR*) degrade selective prediction risk-coverage when correct answers stem from ungrounded cultural text priors.

### B. What Was Wrong or Overstated in the Previous Audit?

1. **BanglaProtha Dataset Size Was Understated:** The previous audit cited *"~1,200 cultural images, ~3,500 MCQA"* based on an unverified early estimate. The actual verified size is **6,942 images and 8,034 MCQA questions**.
2. **Repository CSV Size Was Misleading:** The GitHub repository (`farhanishmam/BanglaProtha`) contains only an 80-row sample in `data/data.csv`; the actual benchmark must be loaded from Kaggle.
3. **Thresholds Were Unsubstantiated Heuristics:** The criteria *">85% unchanged predictions = blindness"* and *"$\Delta_{\text{logit}} > 0.30$ = sufficient visual sensitivity"* were arbitrary experimental heuristics, not scientific thresholds established by literature.
4. **Split Deduplication Assumption:** The previous audit assumed the official 80:20 split was clean. In reality, the paper does not document image-grouped partitioning, meaning the official split may leak images across train/test splits. A custom image-hash grouped split is required.

### C. Remaining Scientific Gap

> **Under regional cultural distribution shift, does visual-grounding contrastive probing improve selective prediction risk–coverage over native softmax calibration ($H_1$), or does the presence of correct-but-ungrounded cultural knowledge cause visual-grounding penalties to suppress true positive answers ($H_0$)?**

### D. Remaining Fatal Risks

1. **Total Visual Deafness / Language Invariance:** If compact models (`Qwen2.5-VL-3B`, `Gemma-3-4B`) display zero measurable logit divergence across original and blank images on Bengali MCQA, visual tokens are completely ignored, rendering visual perturbation probing inert. (Controlled by measuring continuous $\Delta_{\text{logit}}$ distributions).
2. **Failure to Beat Temperature Scaling:** If post-hoc temperature scaling on native softmax logits achieves identical selective risk-coverage (AUGRC) to contrastive perturbation probes, the entire multi-condition visual perturbation machinery is redundant. (Controlled by including Platt temperature scaling as a mandatory baseline).
3. **Category Imbalance Confound:** If performance variations are driven entirely by broad category difficulty (e.g., high accuracy on famous landmarks, zero accuracy on rural attire), selective prediction may simply learn a category-frequency prior. (Controlled by evaluating macro-averaged AUGRC across categories).

---

### E. Decision Status

## **SURVIVES TO FINAL COMPARISON**

**Rationale:**The surviving **diagnostic formulation** has successfully cleared the boundary audit:

1. The constructive flaws (RAG label leakage, multi-signal linear ensembling) have been completely excised.
2. The benchmark dataset (`BanglaProtha`) is verified as a public, large-scale (6,942 images / 8,034 MCQA items), high-quality discrete target space.
3. The underlying tension—whether visual grounding penalties suppress correct-but-ungrounded cultural knowledge—is a genuine, un-preempted scientific question.
4. Both positive and negative experimental outcomes yield publishable, non-trivial mechanistic insights into asymmetric cross-modal pretraining.
5. All competing explanations (tokenization fragmentation, class difficulty, ordinary OOD shift) can be cleanly controlled using single-letter MCQA logits, text-only LLM baselines, and temperature scaling.

Proposal 3 possesses sufficient scientific and experimental viability to enter the final comparative matrix alongside Proposals 1 and 2.
