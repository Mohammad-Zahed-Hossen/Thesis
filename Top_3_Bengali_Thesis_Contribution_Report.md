# Three Bengali AI Thesis Working Topics: Exact Contributions and Experimental Plans

Prepared for Mohammad Zahed Hossen | 15 September 2026

## Decision and scope

**Start with Topic 1, Bengali ASR confidence transfer. Keep Topic 2 as a conditional reserve. Treat Topic 3 as a benchmark-audit proposal whose data limitations must be resolved before model training.** These are three alternatives, not three projects to complete together.

This report develops the first three directions in the supplied assessment. The current request explicitly authorizes these non-VLM topics; older field locks do not override it. The Topic Discovery Handover supplies the contribution standard: a controlled empirical study using existing methods can be a valid thesis. A new architecture, a winning score, or guaranteed publication is not required.

Constraints remain 3–4 months, undergraduate CSE scope, Colab Pro, public legal data, open models, no paid APIs, private collection, major annotation, or specialist supervision. Proposals below are experimental designs, not results. No model training, audio decoding, complete dataset audit, or Colab profiling was performed for this report.

### Comparison

| Rank | Exact working title | Your central contribution | Present verdict |
|---|---|---|---|
| 1 | **Do Confidence Scores Transfer Across Bengali Speech Domains? Error Detection with Frozen ASR Models** | Establish whether cheap confidence-based selection transfers to unseen domains beyond length and normalization effects. | Proceed to a bounded pilot. |
| 2 | **Do Bengali AI-Rewrite Detectors Generalize Beyond Their Training Generators? A Paired and Source-Controlled Evaluation** | Measure transferable detection and false positives after controlling paired content, generator allocation, source and length. | Reserve: file access, metadata crossing and a very close paper remain unresolved. |
| 3 | **How Stable Are Bengali Synthetic-Speech Detectors Under Controlled Audio Processing? A BanglaFake Benchmark Audit** | Measure processing sensitivity on the same test utterances and document which conclusions the benchmark can identify. | Conditional audit only; speaker/class confounding prevents broad detection claims. |

The first is inference-heavy, the second is text classification plus evaluation design, and the third combines signal processing with detection evaluation. All need careful data reasoning. None is automatically novel merely because Bengali is involved.

## Evidence that changes the earlier assessment

| Finding | Evidence level | Consequence |
|---|---|---|
| BanSpeech offers audio, transcripts, domain partitions and file paths. | Release page and sample-record API inspected in the preceding research. | A concrete ASR pilot is supported, although recording-group reconstruction remains unverified. |
| The four-generator text release advertises paired originals and rewrites. | Official release description inspected; downloadable records not inspected. | Design the study conditionally; do not claim a working loader or verified generator balance. |
| A Bengali paraphrase-detection paper already compares transformers and reports strong performance. | Original paper inspected. | Another architecture leaderboard is insufficient. |
| A paper titled *Engineering a Lightweight, Cross-Generator-Robust Pipeline for Bengali AI-Paraphrase Detection: A Leakage- and Artifact-Aware Evaluation Process* is indexed under DOI 10.2139/ssrn.7243715. | Primary search record identified; full text inaccessible during this audit. | This is a serious overlap lead. No novelty clearance for Topic 2 until the actual design is checked. |
| BanglaFake's paper reports seven genuine speakers and one synthetic male voice; its tables disagree on the genuine count. | Original paper, Tables 1–2. | Class, voice and source may be entangled. Processing normalization cannot fix that design limitation. |
| A follow-up BanglaFake detection benchmark already exists. | Original paper inspected. | Topic 3 must examine evaluation or robustness, not claim the first Bengali detector. |

Sources: [BanSpeech release](https://huggingface.co/datasets/SUST-CSE-Speech/banspeech), [paired text release](https://data.mendeley.com/datasets/9gffsw9mjy/4), [Bengali paraphrase paper](https://arxiv.org/html/2512.21709v1), [closest text audit lead](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7243715), [BanglaFake paper](https://arxiv.org/html/2505.10885v1), [follow-up detector study](https://arxiv.org/html/2512.21702v1).

## Topic 1: Bengali ASR confidence transfer

### Question, motivation and boundaries

**Question:** Does a lightweight error predictor fitted on some Bengali speech domains select reliable transcripts in an unseen domain better than native recognition confidence, after controlling utterance length and text normalization?

For example, confidence that is useful for narration may behave differently on interviews. Your experiment tests whether it still identifies mistakes. Regional relevance comes from evaluating varied Bangladeshi speech conditions. It does not establish that the mechanism is uniquely Bengali or that the results generalize to every dialect.

**Primary hypothesis:** At 80% utterance coverage, a small predictor using confidence and length features reduces the high-error rate on held-out domains relative to native confidence. Replication on a second recognizer tests whether this is model-specific.

Define a high-error utterance as WER greater than 0.20 before final evaluation. Also report 0.10 and 0.30 sensitivity thresholds and continuous WER. These are research operating points, not practical acceptability standards.

Competing explanations are: native confidence already suffices; length alone explains the benefit; confidence contains useful information but its numerical scale changes across domains; or its ranking becomes weak. These explanations can coexist.

### Assets and verified limitations

BanSpeech's paper describes 8,085 human-validated utterances, about 6.52 hours across 13 general domains. The extra dialect subset is not validated for ASR scoring and should be excluded. Its release metadata lists CC-BY-NC-4.0 while its prose lists CC BY 4.0; preserve this discrepancy rather than silently choosing a license. [Paper](https://arxiv.org/pdf/2210.12921), [release](https://huggingface.co/datasets/SUST-CSE-Speech/banspeech).

Use [Whisper-small](https://huggingface.co/openai/whisper-small) first. Add [BengaliAI BanglaConformer](https://huggingface.co/bengaliAI/BanglaConformer), a released approximately 121M-parameter recognizer, as a second architecture if its dependency and confidence-extraction path works. Its card provides older NeMo installation instructions, which require compatibility testing. Model availability is verified; your reproduction is not.

### What you would actually build

1. **Dataset manifest:** utterance ID, domain, original file path, provisional recording group, duration, reference text, hash and exclusion reason. Validate inferred grouping rules; a filename prefix is not automatically a speaker ID.
2. **Frozen inference runner:** one fixed decoding configuration per recognizer. Save transcript, token/frame summary scores, runtime and checkpoint revision. Never use reference text as a decoding prompt.
3. **Scoring pipeline:** apply the same predefined normalization to references and predictions, then compute substitution, deletion and insertion counts, reference word count, WER and CER.
4. **Error-selection experiment:** fit small predictors on development domains and evaluate untouched domains.
5. **Analysis:** compare ranking, policy transfer, length controls and normalization sensitivity with group-aware uncertainty estimates.

The final deliverables are manifests, reproducible prediction files, evaluation code, result tables and a defensible explanation of when confidence is useful. They are not a transcription application.

### Exact methods

For a nonempty reference, let utterance error be e_i = (S_i + D_i + I_i) / N_i, and let y_i = 1 when e_i > 0.20. WER can exceed 1; do not clip the primary WER results. Handle empty references explicitly rather than dividing by zero.

For Whisper, start with mean log probability over generated text tokens, excluding prompt/control tokens using a documented rule. For CTC, raw frame confidence can be dominated by blanks; use a clearly specified nonblank aggregation and do not describe it as the same probability measure. Score extraction must be tested against the decoded hypothesis.

Fit regularized logistic regression to predict y_i from a small feature set: native score, log duration, predicted token count and token count per second. Standardize features using training data only. Do not include reference length, WER or correctness as inference features.

Compare:

| Variant | Purpose |
|---|---|
| Accept all and repeated random rejection | Establish total recognition error and chance selection. |
| Native confidence ranking | Main strong baseline. |
| Logistic regression using confidence alone | Separates simple calibration from additional information. |
| Duration/token features alone | Tests length-related shortcuts. |
| Confidence plus duration/token features | Main proposed comparison. |
| Equal-domain sample weights versus ordinary fitting | Optional test of whether abundant domains dominate fitting; a standard method, not algorithmic novelty. |

Keep one small hyperparameter grid shared across variants. Optional disagreement between two recognizers adds inference cost and should come only after the minimum study works.

### Split and analysis plan

Set aside a small development portion for code and protocol design, respecting recording groups. Do not use it for final claims. Then lock the protocol and use outer leave-one-domain-out evaluation on the remaining data. Inner selection uses only the other domains. Remove shared recording groups from training when they overlap the outer test domain. All derived versions stay with their originals.

If multiple domains share speakers without speaker metadata, state that limitation. Claims concern held-out domains and identified source groups, not proven speaker independence. Unknown pretraining overlap is a separate limitation that a new split cannot eliminate.

Primary comparison: average across evaluable domains of the paired difference in high-error rate at 80% coverage. Also report corpus WER among retained transcripts, computed as summed edit counts divided by summed reference words, and an explicitly labeled mean utterance WER. Do not mix them.

Report per-domain coverage and error, AUROC for y_i, and risk–coverage curves. A domain containing one error class has undefined AUROC; report it as such. Treat zero coverage as undefined risk, not zero error.

Run two distinct policy experiments:

- **Batch ranking:** choose the top-scored 80% without test labels. This uses the test score distribution and evaluates a batch policy.
- **Fixed threshold:** choose a threshold on inner development data and apply it unchanged. Report the resulting error and coverage; 80% target coverage need not transfer.

Bootstrap paired method differences at the recording-group level within domains, and report fold variation. Do not treat 13 folds with overlapping training sets as independent replications. If source groups are too few, use descriptive estimates and reduce the strength of the claim.

### Precise contribution claim

If supported: “We establish which inexpensive confidence signals retain error-selection value across the tested Bengali speech domains, and quantify whether additional features improve over native confidence after length and normalization controls.”

This is an empirical contribution. Fitting logistic regression, collecting another WER table, or finding an isolated significant result is not the contribution.

Success can be a stable improvement or a precise finding that the simpler baseline is adequate. Before testing, select a smallest worthwhile difference, for example three percentage points in high-error rate at 80% coverage. That number is a proposed design choice. An interval excluding that improvement supports a claim of no meaningful benefit from the added complexity. Equivalence requires the entire interval to fall within prespecified positive and negative margins; a wide interval is inconclusive.

Stop if source structure cannot support the intended comparison, useful scores cannot be extracted, or the whole conclusion is merely that recognition quality varies by domain. A failure of a weak second model should not be used to strengthen a general claim.

### Closest-work matrix

| Work and evidence inspected | Existing result/design | Distinction and limitation for this thesis |
|---|---|---|
| [BanSpeech](https://arxiv.org/pdf/2210.12921), dataset and evaluation sections | Compares recognition approaches across domains. | Your object is error selection and transfer, not another recognition leaderboard. |
| [OOD-Speech](https://arxiv.org/abs/2305.09688), paper record and model release | Bengali out-of-domain benchmark. | Provides context and a recognizer; does not alone establish your gap. |
| [Huo et al., 2025](https://arxiv.org/html/2509.07195v1), methods/results | Whisper token overconfidence under added noise, selective temperature scaling. | Natural domain changes and utterance selection differ; generic noisy confidence calibration is already covered. |
| [TruCLeS, 2025](https://www.isca-archive.org/interspeech_2025/ravi25_interspeech.pdf), Sections 2–3 | Learned word confidence, Hindi/English out-of-domain evaluation. | Domain-transfer confidence is not new. Your scope is inexpensive Bengali policies and controls. |
| [RAS, 2026](https://arxiv.org/html/2604.24278v4), methods/experiments | Partial-transcript abstention, reliability metric and trained placeholder generation. | Whole-utterance selection with frozen recognizers differs; do not claim to invent ASR abstention. |

### Budget and pilot

Cache model predictions once. If each recognizer processes H hours at real-time factor r_m, inference time is approximately H times the sum of r_m. For H = 6.52 and two models each at r = 0.5, this is 6.52 GPU-hours; at r = 2, it is 26.08. These are arithmetic scenarios, not measured runtime. Feature extraction and reruns add cost. Peak memory remains unmeasured; reduce batch size first.

Five-day pilot: Day 1 manifest and groups; Day 2 Whisper inference on 300–500 development utterances from several domains; Day 3 score/normalization tests and simple baselines; Day 4 hold out one development domain and profile the second model; Day 5 lock the protocol or record the concrete blocker. Pilot scores are exploratory and excluded from confirmatory conclusions.

## Topic 2: Bengali AI-rewrite detector generalization

### Question and exact contribution

**Question:** After keeping related source texts together and balancing observable content differences, how well do Bengali rewrite detectors recognize outputs from a generator absent during training, and what false-positive rate do they produce on human text?

**Working contribution:** a controlled transfer evaluation, including a diagnostic comparison of simple lexical methods and a Bengali encoder. A detector trained on one writing pattern may simply learn that pattern. Your evidence would show how much predictive value remains under stricter evaluation, not prove universal human/AI attribution.

Hypothesis: apparent detector performance falls on unseen generators even under pair-disjoint evaluation, with some of the difference associated with length and source composition. This can be disproved by stable, precisely estimated transfer after controls. A positive transfer result is also valuable if it establishes the limits of a simple baseline.

### Data and overlap gates

The [four-generator release](https://data.mendeley.com/datasets/9gffsw9mjy/4) describes 2,000 originals and 2,000 rewrites, Pair_ID, generator/source, category and length metadata, under CC BY 4.0. Each original is reportedly rewritten by one generator, not necessarily by all four. Records were not downloaded; these are documentation-level facts. Access attempts in the prior audit returned 403. Do not claim the dataset is unavailable to everyone, or bypass access restrictions.

First inspect generator-by-category counts, source-document IDs and whether the same original has multiple versions. If a generator occurs only in one category, its effect cannot be separated from that category. Restrict to overlapping categories only when enough examples remain; otherwise abandon the isolated generator claim.

The [SSRN audit lead](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7243715) is exceptionally close in stated scope. Its indexed title is verified, but its detailed experiments are not. Resolving this one paper is a specific prerequisite, not an invitation to restart broad searching. If it already performs the proposed controls on comparable data, select a materially different uncertainty or reject this exact title.

### Minimum experiment and your work

1. Validate pairing, labels, generator names, category counts and source IDs. Hash duplicates and cluster near-duplicate passages conservatively.
2. Create a group key combining the original and its rewrites; merge groups from the same identifiable source document.
3. Train TF-IDF logistic regression and one fine-tuned BanglaBERT classifier under the same group partitions.
4. Evaluate ordinary group-disjoint transfer, generator holdout and, if supported, source/category holdout.
5. Report performance by generator, source and length; test simple balancing and calibration controls.

Use [BanglaBERT](https://huggingface.co/csebuetnlp/banglabert) with its documented tokenizer/normalization. Fit a task-specific classification head. An unfitted head on a generic encoder is not a meaningful zero-shot detector. No generation API is required because outputs already exist in the proposed corpus.

### Exact split logic

For held-out generator g, test its rewrites together with their paired human originals. Remove all those original groups from training and validation. Train on the other generators and their human counterparts. Model selection and decision thresholds use validation groups only.

This paired test balances semantic content across labels but does not automatically remove source-topic differences between generator folds. Use the generator-by-category table to determine which comparisons are identifiable. Report per-category results or weighted common-support results alongside unweighted results. Do not hide discarded categories or sample loss.

For a split-sensitivity audit, compare a clearly labeled row-random protocol with group-disjoint protocols at comparable training sizes. The row-random result is a diagnostic, never the valid final result. Different test composition and training size can explain differences, so the raw score gap alone is not a causal estimate of leakage.

### Baselines, proposed intervention and metrics

| Variant | Role |
|---|---|
| Length/punctuation statistics with logistic regression | Detects easy formatting cues. |
| Character n-gram TF-IDF logistic regression | Strong inexpensive lexical/style baseline. |
| Word n-gram TF-IDF logistic regression | Alternative lexical baseline. |
| BanglaBERT classifier | Tests whether contextual representation adds transferable value. |
| Training-only source/length reweighting | Optional standard intervention to reduce visible imbalance. |

Fit vocabularies, feature scaling and weighting parameters on training data only. Use one small shared search budget. Truncation and chunking must be consistent across classes; aggregate any chunks at original text level. Pair similarity can support auditing but must not be used as a detector input when the original is unavailable at use time.

Primary metrics: macro-F1 and human-text false-positive rate at a validation-fixed threshold, with per-generator breakdown. Add AUROC, recall, Brier score and confidence intervals clustered by source group. Fix a development operating point such as 5% false-positive rate and report its actual test false-positive rate plus detection recall. Do not claim a guaranteed 5% bound.

Control for length both through a length-only baseline and stratified/matched reporting. A score decline after matching may reflect changed difficulty, not proof that length was the sole causal mechanism. Treat generator identity, prompt version and source as separate variables wherever metadata permit.

### What you can claim and what you cannot

Supported claim template: “For the evaluated corpus and generators, we quantify which detection results survive source grouping and generator holdout, and whether inexpensive balancing improves transfer without raising false positives.”

A useful negative result could show TF-IDF matching the encoder within a predefined margin, failure of balancing, or a precise boundary where transfer fails. A null result with insufficient independent sources is not enough. Detector output is not proof of cheating, authorship or malicious intent; the thesis evaluates a benchmark task.

Deliverables: validated metadata inventory, split manifests, CPU baselines, one encoder reproduction, transfer matrix, false-positive analysis and code. Stop if grouping or generator/category support is inadequate, access remains blocked, or closest work already answers the same controlled question.

### Closest-work matrix

| Work | Existing evidence | Remaining distinction/status |
|---|---|---|
| [Paired Bengali release, version 4](https://data.mendeley.com/datasets/9gffsw9mjy/4) | Supplies the proposed data design. | A dataset record is not proof that transfer has been evaluated. Files still need inspection. |
| [Islam et al., 2025](https://arxiv.org/html/2512.21709v1), Section IV | GPT-3.5 paraphrases in BanglaTextDistinguish; transformer comparison; stratified 60/20/20 split. | Group preservation is not clearly specified in the inspected description. Do not assert demonstrated leakage. Multiple-generator controls differ. |
| [Jobu, SSRN 7243715](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7243715) | Indexed title explicitly concerns cross-generator, leakage and artifact-aware Bengali detection. | Full-text overlap unresolved; strongest threat to selecting this topic. |
| [MULTITuDE, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.616/) | Unseen-language and unseen-generator detector evaluation. | General transfer testing is established; Bengali paired-source evidence must add something specific. |
| [RAID, ACL 2024](https://aclanthology.org/2024.acl-long.674/) | Tests detector robustness across generation conditions and domains. | Another robustness table is insufficient; your contribution needs source-controlled findings and false-positive analysis. |

### Budget and first-week plan

CPU models should precede GPU training. Minimum neural scope: one encoder, four generator folds, three seeds, three epochs if early validation supports that cap. This is 36 epoch-equivalents; at a measured t hours per epoch the base cost is 36t, before tuning and ablations. Do not run every baseline across a large hyperparameter grid. Profile one epoch first; reduce sequence length only after checking truncation impact.

Days 1–2: obtain and inspect files, validate pairs and crossing, and resolve the specific closest-paper overlap. Day 3: TF-IDF group-disjoint baseline. Day 4: one held-out generator and source/length controls. Day 5: one encoder pilot only if gates passed. Otherwise record the blocker and stop this topic.

## Topic 3: Bengali synthetic-speech benchmark audit

### Question and bounded contribution

**Question:** For fixed Bengali genuine/synthetic test utterances, how do detector scores and errors change under class-balanced audio-processing interventions, and does matched training reduce that sensitivity?

This is a processing-robustness audit on a limited benchmark. It cannot establish general detection of unseen voices or synthesis systems using the currently documented data.

Hypothesis: common processing changes cause material changes in detection errors, and simple training augmentation reduces the worst tested change without excessive loss on unprocessed audio. A drop alone demonstrates processing sensitivity, not that a model used only spurious cues. The experiment needs multiple complementary controls.

### Critical dataset findings

The [BanglaFake paper](https://arxiv.org/html/2505.10885v1) describes a VITS synthesis system. Table 1 lists 12,260 genuine and 13,260 synthetic samples, seven genuine speakers and one synthetic male voice. Table 2 instead totals 13,260 in each class. Source provenance and actual file counts must therefore be reconciled before adopting these numbers.

This audit confirmed a roughly 5.64 GB `final_data.zip` in the [dataset repository](https://huggingface.co/datasets/sifat1221/banglaFake). The visible root contains no separate metadata or license file; the archive contents were not downloaded. The paper's phrase “open license” does not specify usable terms. The viewer error is not evidence that the ZIP itself is corrupt.

A one-synthetic-voice dataset cannot support a conventional train/test holdout of synthetic speakers. Even a genuine-speaker holdout would not establish synthetic-speaker generalization. If real recordings of the corresponding synthetic target speaker can be verified, a matched-voice subset may reduce one confound, but it still cannot establish unseen-voice or unseen-generator performance.

### Six implementation phases

1. **Asset gate:** confirm license, inspect archive inventory and metadata, reconcile counts, identify speakers, text prompts, source recordings and genuine/synthetic pairing.
2. **Data audit:** measure duration, sample rate, channel count, leading/trailing silence, clipping fraction and loudness. Map these by label and source.
3. **Group split:** group shared text prompts and all derivatives before a proposed 70/15/15 split. Use official splits only after auditing their meaning. Report which speaker/source controls are possible.
4. **Detection baselines:** reproduce a task-specific open detector and train a small spectral baseline if justified.
5. **Paired processing experiment:** transform the exact same held-out originals, using label-independent settings, and compare paired score/error changes.
6. **Matched-training control:** determine whether sensitivity changes when the model sees equivalent processing during training.

### Baseline choices

- Duration/silence/loudness logistic regression, with no filenames or labels encoded in features: a diagnostic shortcut baseline.
- LFCC summary features with logistic regression: a reproducible CPU spectral baseline.
- [AASIST-L](https://github.com/clovaai/aasist): the official repository provides a trained anti-spoofing checkpoint and evaluation code. Use its prescribed input preparation. Out-of-language performance is unknown until measured.
- Optional ResNet18 on log-mel inputs: implement a documented comparator to the existing Bengali benchmark. If exact code is unavailable, call it a reimplementation, not an exact reproduction.

A generic Whisper or wav2vec encoder is not a pretrained synthetic-speech detector. A trained detection head or justified scoring rule is necessary.

### Controlled processing matrix

All inputs first pass through the detector's necessary sample-rate/channel conversion. This common baseline is separate from the interventions.

| Condition | Operation | What it tests |
|---|---|---|
| P0 | Common baseline decoding only | Reference score and errors. |
| P1 | Fixed rule for boundary-silence trimming, with preserved speech and a failure flag | Sensitivity to boundary material. |
| P2 | The same loudness-normalization target without clipping | Sensitivity to amplitude statistics. |
| P3 | One fixed encode/decode setting applied equally to both labels | Sensitivity to codec processing. |

Choose exact settings using development audio and document them before final evaluation. Do not select the setting that creates the largest test collapse. Do not process only synthetic or only genuine test audio in the main robustness experiment.

Keep the number of conditions small. Test the frozen detector on P0–P3. Then train the small comparator on P0 and on a fixed mixture of P0–P3, evaluating each on every condition. A known augmentation such as RawBoost may replace the mixture as one optional comparator. It is not a new method.

Silence-only evaluation is useful only when the resulting segments are valid inputs; padding differences and empty segments can manufacture another shortcut. Record the eligible subset and include a length-only control.

### Metrics, interpretation and claim limits

Primary outcome: paired change in detection error at a validation-fixed decision threshold, separately for genuine and synthetic audio. Also report AUROC, EER, macro-F1 and per-source results. EER computed on each test condition is descriptive, not the error of the fixed operating threshold.

Bootstrap by prompt/source group with paired resampling across processing conditions. With very few speakers, intervals describe sampled utterance groups, not population-level speaker generalization.

Matched training helps distinguish sensitivity to unfamiliar processing from persistent weakness under that condition. Neither score changes nor augmentation gains alone identify a unique causal artifact. Processing can remove legitimate synthesis cues as well as incidental cues. Speaker/class confounding remains after all four operations.

Supported claim template: “On the audited BanglaFake release, we quantify how specified processing operations affect selected detectors and show whether matched training reduces that sensitivity, under documented speaker and source limitations.”

A useful negative result is stable performance with intervals narrow enough to exclude a prespecified material change, or failure of augmentation to improve the worst condition. Documenting an impossible generalization claim is valuable, but a list of metadata problems alone is usually too small for the intended full thesis. Stop if license or grouping cannot be established or if only a heavily confounded generic classifier remains.

### Closest-work matrix

| Work | Existing evidence | Proposed distinction |
|---|---|---|
| [BanglaFake, 2025](https://arxiv.org/html/2505.10885v1), Tables 1–2 and Section 4 | Corpus construction and synthesis-quality analysis. | Paired detector-response experiments plus release audit; no claim to create a new corpus. |
| [Zero-Shot to Zero-Lies, 2025](https://arxiv.org/html/2512.21702v1), Section IV | Bengali detector comparison with 70/15/15 partitions and five-second inputs. | The inspected methods do not establish the proposed paired processing and matched-training experiment. Code-level split details remain unverified. |
| [AASIST official implementation](https://github.com/clovaai/aasist) | Trained detector and compact variant with evaluation code. | Provides a baseline, not a Bengali robustness guarantee. |
| [RawBoost](https://arxiv.org/abs/2111.04433) | Existing augmentation for nuisance variation in spoof detection. | Your potential contribution is the controlled assessment, not inventing augmentation. |
| [How to Construct Perfect and Worse-than-Coin-Flip Spoofing Countermeasures, 2023](https://arxiv.org/abs/2306.00044) | Studies shortcut learning in spoof countermeasures. | Generic shortcut detection is known; a Bengali audit must add verifiable benchmark-specific evidence. |

### Budget and first-week plan

Do not train a TTS system. Download and preprocess in Colab after access/license checks; avoid loading the whole archive into 8 GB local RAM. Generate processed versions on demand or in a bounded cache.

If validated audio duration is H, four inference conditions cost approximately 4Hr GPU-hours for one model at measured real-time factor r. Two training regimes, three seeds and up to five epochs yield 30 epoch-equivalents for the small comparator. Profile one epoch before committing. Memory and total runtime are not measured.

Day 1 license and archive inventory; Day 2 count/provenance/pairing audit; Day 3 CPU diagnostic baselines; Day 4 trained AASIST-L inference on a balanced development subset; Day 5 paired processing controls. Do not proceed to training if the asset gate fails.

## Common 12-week execution structure

| Period | Work for the selected topic only | Required output |
|---|---|---|
| Week 1 | Bounded feasibility pilot | Access, grouping, runtime, baseline and go/no-go record. |
| Weeks 2–3 | Baseline and protocol stabilization | Versioned data manifest, fixed evaluation rules, prediction checks. |
| Weeks 4–6 | Main comparison | Complete primary results under the locked protocol. |
| Weeks 7–8 | Controls and uncertainty | Ablations, group analysis, uncertainty intervals. |
| Weeks 9–10 | Replication and error analysis | Second model or justified replication; explanation of limits. |
| Weeks 11–12 | Writing and reproducibility | Thesis, environment specification, code, results and limitations. |

Keep weeks 13–16 as contingency if available. Write methods and data notes during execution rather than postponing all writing.

## Final recommendation and decision log

**Choose Topic 1 for the next pilot.** It has the clearest verified data path and the lowest dependence on uncertain generator/speaker metadata. Topic 2 could become attractive after its two precise blockers are resolved. Topic 3 has a legitimate empirical question, but currently supports a narrower conclusion than the earlier assessment implied.

The claim that existing methods cannot support a thesis remains rejected. The opposite claim, that every benchmark audit is sufficient, is also rejected. What matters is whether the experiment provides reliable evidence about a consequential uncertainty.

Next 60–90-minute task for Topic 1: load development samples from three BanSpeech domains, inventory source identifiers, and verify one Whisper-small transcription plus its confidence score. Produce a manifest and record the model/environment version. This is a feasibility check, not a result supporting the hypothesis.

| Date | Decision | Basis | Next action |
|---|---|---|---|
| 2026-09-15 | Topic 1: proceed to pilot; Topic 2: reserve; Topic 3: conditional audit | Public ASR resources; unresolved text access/overlap; documented synthetic-speech confounds. No final thesis freeze. | Perform the Topic 1 asset and score-extraction check. |
