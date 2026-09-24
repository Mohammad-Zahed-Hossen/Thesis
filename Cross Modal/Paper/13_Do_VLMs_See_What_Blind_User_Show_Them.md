# Do VLMs See What Blind Users Show Them? A Distribution-Shift and Evaluation-Protocol Audit on VizWiz

Sergei O. Kurashkin [1] _[,]_ [2], Vadim Tynchenko [1], and Aleksei Borodulin [1]

1 Bauman Moscow State Technical University, Moscow, Russia
2 RUDN University, Moscow, Russia kurashkin@bmstu.ru

Abstract. Assistive vision-language models (VLMs) are increasingly proposed to answer the visual questions of blind and low-vision users, yet progress is tracked by a single aggregate accuracy. Auditing nine open VLMs on VizWiz-VQA (real photographs taken by blind users) against VQAv2 (curated web images), we nd the aggregate number is governed as much by three evaluation-protocol choices as by the models.
(i) On answerable questions the curated-to-real shift is large and statistically signicant, +0 _._ 10 to +0 _._ 33 accuracy; the naive aggregate hides or even inverts it, with one model appearing to do better on real images. (ii) This follows from the 32 _._ 1% unanswerable share: a removed or degraded image pushes models toward the safe unanswerable reply, so the most abstaining models ( 12 _._ 9 42 _._ 0% ) rank highest in aggregate, and a prompt sweep shows the abstention is instruction-driven, collapsing when the clause is removed. (iii) The answer matcher moves absolute accuracy substantially (one model brackets at [0 _._ 21 _,_ 0 _._ 58] ), yet the ranking is stable between two principled matchers (strict exact-match and token-F1, Kendall _τ_ =0 _._ 94 ) and reorders only under a permissive containment bound. A blind text-only control shows the image contributes a signicant margin but a language-prior oor remains; a sighted-versusblind decomposition attributes at least half of the gap to the question and answer distribution, not image diculty. A controlled corruption sweep shows robustness to moderate synthetic blur, exposure, and crop, so the gap is not a simple capture-degradation eect. We recommend an answerability-split, abstention-aware, match-bracketed protocol and release code and per-prediction outputs.

                                    -                                    -                                    Keywords: Vision-language models Assistive technology VizWiz

               -               Evaluation Distribution shift Robustness

1 Introduction

Blind and low-vision (BLV) users photograph their surroundings and ask questions about them. The resulting images are frequently blurred, badly framed, or poorly exposed, the questions are conversational, and a large fraction cannot

2 S. O. Kurashkin et al.

**three protocol choices this paper varies**

_a range, not a point_

Reported accuracy

& **ranking** move with the choices

Fig. 1: The evaluation protocol. With the nine models and the data held xed, the reported VizWiz accuracy and the model ranking are governed by three protocol choices that papers usually leave implicit: the answerability split, the abstention instruction in the prompt, and the answer matcher. We measure how much each choice moves the number and the ranking, and use a blind text-only control and a corruption sweep to locate the curated-to-real gap.

be answered from the photograph at all [10]. Vision-language models (VLMs) are now positioned as the engine of such assistive systems, and recent benchmarks report strong aggregate accuracy on assistive data [14]. Before trusting these numbers to rank models or to certify readiness for deployment, we ask a prerequisite question: does a single accuracy gure on VizWiz measure what it appears to measure?

We audit nine open VLMs spanning four vendors and two model generations within a lineage, evaluated identically on VizWiz-VQA against the curated
VQAv2 reference. We nd that the headline number conates at least three distinct quantities, and that on the data that matters, real photographs taken by blind users, the model ranking depends on protocol choices that are usually left implicit (Fig. 1). Concretely:

A paired, signicance-tested audit isolates a large curated-to-real distribu tion shift on answerable questions (Sec. 4.1); the naive aggregate understates or inverts it.
The 32 _._ 1% unanswerable class makes aggregate accuracy reward abstention:

degraded or absent images raise it, and the most abstaining models rank highest (Sec. 4.2).
Exact-match scoring penalises verbose-but-correct answers, so the matcher

moves absolute scores; the ranking, however, holds across two principled matchers and shifts only under a permissive upper bound (Sec. 4.3).
A blind text-only control quanties the image's contribution and a residual

language prior (Sec. 4.4); a controlled corruption sweep shows the gap is not explained by simple synthetic capture degradations (Sec. 4.5).

Our aim is not a new model but a protocol: we argue for an answerabilitysplit, abstention-aware, match-bracketed evaluation, and release code and perprediction outputs so that assistive-VQA results can be read correctly.

A Distribution-Shift and Protocol Audit on VizWiz 3

2 Related Work

Assistive VQA and VizWiz. VizWiz introduced visual questions collected from blind photographers [10]; unlike curated benchmarks such as VQAv2 [9], its images are lower quality, its questions are conversational, and a substantial share are unanswerable because the needed information is absent from the photograph.
Recent work benchmarks VLMs as assistive generalists: @Bench evaluates VLMs across ve tasks selected by people with visual impairments, including VizWizVQA [14], and others lter VizWiz to study culturally inclusive description [16].
These eorts report task accuracy but do not isolate the curated-to-real shift with paired signicance, nor do they separate genuine answering ability from correct abstention on the unanswerable class, which is the gap we target.

The VizWiz benchmark itself already supports a ner reading than a single number: the ocial evaluation reports accuracy per answer type (yes/no, number, other) and treats unanswerable as one such type [10]. That axis is complementary to ours rather than a substitute for it. It partitions questions by the form of the expected answer, and in our runs it does separate easy from hard formats: yes/no accuracy reaches 0 _._ 83 where free-form other stays near 0 _._ 50 for the same model. Unanswerable, however, sits alongside the answerable types as a fourth category, so a model that abstains everywhere still collects credit inside the reported breakdown, and the headline gure quoted in papers remains the single aggregate over all types. What we add is orthogonal: answering and abstaining as separate quantities, the abstention rate reported alongside them, and the matcher and prompt treated as variables rather than as xed properties of the benchmark.

Robustness to real capture conditions. The shift from web images to photographs taken by blind users has been studied for image classication: VizWiz-Classication tests ImageNet models on authentic BLV photographs [3]. Corruption robustness has a long line of work since common-corruption benchmarks [12], but typically on synthetic shifts of curated data rather than against a real assistive distribution with signicance. We bring controlled corruption attribution to assistive VQA and pair it with a real-vs.-curated comparison, nding that synthetic corruptions do not account for the real shift.

Evaluation methodology for free-form VQA. Open-ended VQA is scored by exact-match soft accuracy over ten human answers [9]. This metric was designed for terse answers and penalises verbose-but-correct outputs; whether this matters for modern, chatty VLMs on assistive data, and whether it changes rankings, has not, to our knowledge, been quantied. We treat the matcher as a variable and report a strict/lenient/token-F1 bracket with a ranking-stability test.

VLMs as visual assistants for blind and low-vision users. Beyond aggregate benchmarking, a growing body of work places VLMs inside concrete assistive settings. At the ACVR workshop, Magay et al . [19] deploy a multimodal foundation model on a wearable platform for spatial reasoning by BLV users, and

4 S. O. Kurashkin et al.

Hansen et al . [11] evaluate VLMs on a single safety-critical task, food-spoilage detection, where a condent wrong answer carries a real cost. Karamolegkou et al . [15] assess twelve multimodal models across ve user-centred tasks dened with visually impaired participants and report that automatic accuracy diverges from what users judge helpful. Closest to our concern, Huh et al . [13] show that long-form VLM answers to BLV questions often assert visual detail the photograph does not support, and that this failure concentrates on the unanswerable questions where the image is blurred or o-topic. This evidence motivates our separation of the answerable and unanswerable subsets: a system that is useful in deployment must answer when it can and abstain when it cannot, and a single aggregate score cannot tell these two competencies apart.

Abstention and selective prediction in VQA. The option to decline a question has been studied as selective prediction. Whitehead et al . [22] cast reliable VQA as a risk-coverage problem and show that, at a one-percent tolerance for error, a strong model relying on its softmax condence answers only a small fraction of questions, so reliability is governed by abstention calibration rather than raw accuracy. Dancette et al . [6] improve the accuracy-coverage trade-o, with the largest gains in the mixed in- and out-of-distribution regime that BLV imagery resembles. Srinivasan et al . [20] report the opposite failure, models that abstain more often than warranted, and argue for reducing over-abstention in visionlanguage reasoning. On VizWiz the question is sharper, because roughly a third of items are unanswerable by construction [10], so abstention is partly correct behaviour and partly a confound: any manipulation that raises the abstention rate also raises the aggregate score. We therefore report the abstention rate next to answering ability and the correct-abstention rate, instead of folding all three into one number.

3 Evaluation Protocol

3.1 Models and inference

We evaluate nine open VLMs, all _≤_ 13 B parameters and run in half precision on a single 80 GB GPU: LLaVA-1.6 (7B, 13B) [18], Qwen2.5-VL-7B and Qwen3-VL8B [4,5], InternVL3-8B and InternVL3.5-8B [21,23], Gemma-3-12B [8], Pixtral12B [2], and Idecs3-8B [17]. The set spans four vendors and pairs two generations within the Qwen and InternVL lineages, letting us ask whether protocol sensitivity is a property of a single family. (A gated model was excluded because access was not granted at run time.) Every model receives an identical instruction to answer in a few words and to reply unanswerable when the image does not support an answer; decoding is greedy. We log wall-clock and peak memory per unit; the full audit used 27 _._ 2 GPU-hours, peaking at 29 _._ 6 GB. As a calibration check, the strict VQAv2 accuracy of LLaVA-1.6 in our harness ( 0 _._ 80 at both sizes) matches the published LLaVA VQAv2 range (LLaVA-1.5: 0 _._ 785 and
0 _._ 800 at 7B and 13B [18]), conrming that the harness recovers the standard metric; the newer checkpoints do not report VQAv2 in their technical reports,

A Distribution-Shift and Protocol Audit on VizWiz 5

so a like-for-like external number is unavailable for them and every cross-model comparison here uses the same in-house harness.

3.2 Three protocol axes

We treat evaluation as a set of explicit choices and measure sensitivity to each.

(A) Answerability split. VizWiz-val contains 4 _,_ 319 questions, of which 32 _._ 1% are labelled unanswerable. We report accuracy separately on the answerable subset
(answering ability) and the unanswerable subset (the correct-abstention rate), rather than a single aggregate that mixes them.

(B) Abstention accounting. We report each model's abstention rate (fraction predicting unanswerable) so that aggregate gains driven by abstention are visible rather than folded into an accuracy number.

(C) Answer-matching bracket. We score every prediction three ways under one normalisation (lower-casing, punctuation stripping, removal of the articles {a, an, the}, and a canonical contraction map): strict standard VQA exact-match soft accuracy [9]; a lenient upper bound that credits a ground-truth answer appearing as a token-substring of the prediction (with yes/no extraction); and token-F1, the
F1 over whitespace tokens between prediction and reference. Strict and lenient take the standard min( _m/_ 3 _,_ 1) over the ten reference answers, and token-F1 takes the maximum over those ten references. We report the [ strict _,_ lenient _,_ token-F1 ] bracket and the Kendall- _τ_ correlation between the resulting model orderings.

3.3 Conditions and statistics

On VizWiz we evaluate a clean condition, a blind text-only control (image removed, measuring language-prior leakage), and a controlled corruption sweep
(Gaussian blur, exposure, o-centre crop at xed severities) on a xed subset for attribution. The curated reference is VQAv2-val (clean). Paired conditions on identical items (clean vs. corrupted; image vs. blind) use the Wilcoxon signedrank test (primary, for soft scores) and McNemar (binarised), with bootstrap condence intervals on the per-item drop and Holm correction across the corruption family. The unpaired curated-vs.-real comparison uses a two-sample bootstrap on the mean gap and the MannWhitney _U_ test. Model rankings across conditions use Friedman with a Nemenyi critical-dierence diagram [7]. The full scoring protocol is summarised in Alg. 1. All numbers below are produced by a single from-scratch run with resume disabled and veried by an automated review-proong gate. The run comprises 90 job-isolated units (nine models on the two datasets across the clean, blind, and corruption conditions), all completing successfully under greedy decoding.

6 S. O. Kurashkin et al.

Algorithm 1 Answerability-split, abstention-aware, match-bracketed evaluation.
Require: models _M_ ; datasets _D_ ; conditions _C_ (clean, blind, corruption); prompt _p_ ;

matchers _Φ_ = _{_ strict _,_ lenient _,_ token-F1 _}_
1: for _m ∈M_, _d ∈D_, _c ∈C_ do
2: for each item _x_ in _d_ do
4:3: _ax ←_ _[′]_ _←m_ Apply - _p,_ Image ( _c, x_ )( _x_ _[′]_ ) _,_ Question ( _x_ )� _/triangleright_ drop image (blind) or corrupt it

- _p,_ Image ( _x_ _[′]_ ) _,_ Question ( _x_ )

5: store _a_ ; abstain ( _x_ ) _←_ [ _a_ = "unanswerable" ]
6: end for
7: _A,_ _U_ _←_ answerable / unanswerable items of _d_ _/triangleright_ split, do not merge
8: for _ϕ ∈_ _Φ_ do
9: acc _ϕ_ mean _x∈A ϕ_ ( _ax,_ gt _x_ ) _/triangleright_ answering ability
_←_
10: end for
11: corr_abst _←_ mean _x∈U_ abstain ( _x_ ) ; abst_rate _←_ mean _x∈d_ abstain ( _x_ )
12: end for
13: return per split _{_ acc _ϕ}_ as a [ strict _,_ lenient _,_ token-F1 ] bracket, plus abst_rate _/triangleright_ never a single aggregate over _A ∪_ _U_

4 Experiments and Results

4.1 A large distribution shift on answerable questions

Table 1 reports accuracy on the curated reference and on the answerable VizWiz subset. Every model drops substantially from curated to real imagery, between
+0 _._ 107 (Qwen3-VL-8B) and +0 _._ 334 (InternVL3.5-8B), with six of nine models losing at least 0 _._ 20 . All drops are signicant under a two-sample bootstrap and
MannWhitney _U_ ( _p <_ 10 _[−]_ [3] ). The naive aggregate gap (VQAv2 minus aggregate
VizWiz, computed from the VZ-all column of Table 2) badly understates this:
it is only +0 _._ 022 for Qwen3-VL-8B and is negative ( _−_ 0 _._ 088 ) for Gemma-3-12B, which would absurdly suggest that a model performs better on real assistive photographs than on curated web images. The negative value belongs to the single model whose verbose answers collapse under exact-match (Sec. 4.3); the next two sections explain why. Section 4.4 further decomposes this answerablesubset gap and nds that at least half of it is the question and answer distribution rather than the image being harder to read.

4.2 The unanswerable-class confound

Table 2 decomposes aggregate VizWiz accuracy into answering ability (answerable subset) and correct abstention (unanswerable subset), alongside each model's abstention rate. The aggregate mixes the two and correlates with both: Kendall
_τ_ =0 _._ 89 against the answerable-subset ordering and _τ_ =0 _._ 78 against the abstention rate. A high aggregate therefore does not identify which of the two produced it. For the models that abstain most (Qwen2.5-VL-7B and Qwen3-VL8B, _≈_ 42% ) the two explanations coincide: they achieve the highest correct

A Distribution-Shift and Protocol Audit on VizWiz 7

Table 1: Distribution shift on answerable VizWiz questions: VQAv2 (curated) vs.
VizWiz-answerable (real), strict exact-match. The shift is large and positive for every model, and far larger than the naive aggregate gap (cf . Table 2).

Model VQAv2 VizWiz (ans.) Shift _∆_

Qwen3-VL-8B 0.717 0.609 +0 _._ 107
Qwen2.5-VL-7B 0.781 0.581 +0 _._ 200
LLaVA-1.6-13B 0.803 0.536 +0 _._ 266
LLaVA-1.6-7B 0.800 0.522 +0 _._ 278
InternVL3-8B 0.706 0.481 +0 _._ 225
InternVL3.5-8B 0.738 0.404 +0 _._ 334
Pixtral-12B 0.799 0.473 +0 _._ 326
Idecs3-8B 0.788 0.469 +0 _._ 319
Gemma-3-12B 0.211 0.224 _−_ 0 _._ 013

abstention accuracy ( 0 _._ 86 0 _._ 88 ) and are also the strongest on answerable questions, so we do not claim their lead is a scoring eect. The ordering does depend on the choice, however. Four of the nine models change rank between the aggregate and the answerable-only ordering, most visibly Idecs3-8B, which abstains least ( 12 _._ 9% ) and ranks eighth on the aggregate but seventh on answering ability; Gemma-3-12B moves the other way, penalised for attempting answers it gets wrong. The decisive evidence is mechanical rather than correlational: because
32 _._ 1% of questions are unanswerable, any manipulation that increases abstention (a degraded image, or no image at all) can raise aggregate accuracy, as
Secs. 4.4 and 4.5 show. Aggregate VizWiz accuracy thus rewards caution alongside perception, and cannot be read as an answering-ability ranking without the split.

To test whether this abstention is a property of the models or of the prompt, we re-ran the clean VizWiz evaluation on a xed 1500 -question subset under three further instructions: no abstention clause, a permissive one, and a strict one. The abstention rate is governed by the instruction. Removing the abstention clause collapses abstention from 19 51% to 0 11%, and the aggregate falls with it; among the three prompts that do license abstention the aggregate ranking is stable (Kendall _τ_ =0 _._ 83 0 _._ 94 ), but dropping the clause reorders it ( _τ_ =0 _._ 39 against the default).

Answering ability on the answerable subset is not itself prompt-invariant, and moves in the direction the abstention account predicts: the mean answerablesubset accuracy is 0 _._ 461 under the default prompt, falls to 0 _._ 381 once the abstention clause is dropped, and rises to 0 _._ 489 under the strict prompt. Without the clause a model must attempt the answerable questions it would otherwise decline, and those attempts are disproportionately wrong; the eect is largest for the most abstention-sensitive models (Qwen2.5-VL-7B, 0 _._ 547 _→_ 0 _._ 370 ). The answerable-subset ordering is considerably more stable than its level ( _τ_ =0 _._ 78
0 _._ 89 against the default prompt). Read as selective prediction, each prompt is one operating point: the strict prompt buys lower risk on attempted answerable

8 S. O. Kurashkin et al.

Table 2: The unanswerable-class confound. Aggregate VizWiz accuracy (VZ-all) mixes answering ability (VZ-ans.) with correct abstention on the 32 _._ 1% unanswerable share
(VZ-unans.). Models are sorted by VZ-all; the top of the table is also the most abstaining, showing that aggregate rank partly tracks abstention rather than perception.

Model VZ-all VZ-ans. VZ-unans. Abstain %

Qwen3-VL-8B 0.694 0.609 0.875 41.8
Qwen2.5-VL-7B 0.670 0.581 0.857 42.0
LLaVA-1.6-13B 0.587 0.536 0.694 29.2
InternVL3-8B 0.579 0.481 0.786 33.9
LLaVA-1.6-7B 0.564 0.522 0.654 27.4
Pixtral-12B 0.506 0.473 0.578 27.5
InternVL3.5-8B 0.470 0.404 0.610 24.2
Idecs3-8B 0.438 0.469 0.372 12.9
Gemma-3-12B 0.299 0.224 0.459 17.4

questions at the cost of coverage, and the no-abstention prompt does the reverse
(per-model coverage and risk are tabulated in the supplementary document accompanying the code release). The unanswerable-class confound is therefore real and robust to how the abstention instruction is worded, yet contingent on giving such an instruction at all, which is itself a protocol choice that papers rarely report.

Two further prompts separate the abstention instruction from the answer format. Asking for a word or short phrase rather than a sentence, while keeping the abstention clause, raises mean answerable-subset accuracy to 0 _._ 508, above every prompt in the rst sweep, and the gain concentrates exactly where the exact-match penalty of Sec. 4.3 bites: Gemma-3-12B, the one verbose model, improves from 0 _._ 201 to 0 _._ 363 . A prompt that instead asks the model to reserve unanswerable for genuinely uninformative images gives 0 _._ 421 . Part of what a strict matcher measures is therefore compliance with an answer format the prompt can simply request, which is a protocol choice rather than a property of the model.

4.3 The answer matcher moves scores, not the ranking

Table 3 reports the strict, lenient and token-F1 bracket (Fig. 2 shows the effect on individual answers). Strict exact-match penalises models that answer in complete sentences. Gemma-3-12B brackets at [0 _._ 211 _,_ 0 _._ 577] on VQAv2 and

[0 _._ 224 _,_ 0 _._ 567] on answerable VizWiz: its accuracy more than doubles under a lenient matcher, because answers such as Yes, it is sweet. are scored zero against the ground truth yes. The bracket is narrow for terse models (e.g. LLaVA, a strict-to-lenient gap of at most 0 _._ 03 ) and wide for verbose ones. Gemma-3-12B averages 2 _._ 4 words per answer against about 1 _._ 1 for every other model, and its strict-to-lenient gap of +0 _._ 37 on VQAv2 (against at most +0 _._ 10 for any other model) conrms that its low strict score is a scoring eect recoverable by lenient

A Distribution-Shift and Protocol Audit on VizWiz 9

**strict** **lenient** **token-F1**

**GT: yes** _“Yes, it is sweet.”_ 0.00 1.00 0.40

**GT: no** _“No, a jacket.”_ 0.00 1.00 0.67

**GT: no** _“No, zebras are fighting.”_ 0.00 1.00 0.40

The terse counterpart ( _“yes”_ / _“no”_ ) scores 1 _._ 00 under all three.

Fig. 2: The same verbose-but-correct answer is scored 0, graded, or 1 depending only on the matcher (real matcher outputs on answerable items). Strict exact-match penalises the sentence form, the lenient containment bound credits it fully, and token-F1 sits between; a terse yes/no scores 1 _._ 00 under all three. The matcher therefore moves absolute scores, and Table 3 shows the ranking nonetheless holds between strict and token-F1.

matching rather than a collapse of ability. The matcher therefore moves absolute accuracy substantially, but a wide bracket is a statement about scores, not about the ranking. A principled graded matcher settles which it is: under normalised token-F1 the model ranking matches the strict ranking almost exactly on both datasets (Kendall _τ_ =0 _._ 94, _p <_ 0 _._ 001 ), whereas the lenient containment bound, which deliberately over-credits, is the only matcher that reorders models on real imagery ( _τ_ =0 _._ 56 against strict on VizWiz-answerable, against _τ_ =0 _._ 89 on curated). The choice of matcher thus changes the headline number a model reports (a verbose model can gain 0 _._ 2 or more) and must always be stated, but it leaves the ordering stable across the two principled metrics; the apparent ranking sensitivity is conned to the permissive upper bound and is not genuine ambiguity in the order.

All three matchers are lexical by design. A lexical family is deterministic, cheap to rerun, and adds no third-party model to the measurement, which matters for an audit whose point is that the measuring instrument should not be a free variable. Semantic matchers, whether embedding similarity or an LLM judge, would credit paraphrases that token-F1 misses and are the natural extension of the bracket; we do not adopt one here because the judge becomes an unaudited component with its own prompt sensitivity and its own drift between versions, which would reintroduce at the scoring stage the very problem this paper is about. The recommendation is unchanged either way: report a bracket rather than a point, and state which matcher produced the headline.

10 S. O. Kurashkin et al.

Table 3: Answer-matching bracket: strict exact-match, lenient containment (upper bound), and normalised token-F1. The matcher moves absolute accuracy substantially
(a wide strictlenient gap marks a verbosity-sensitive model), but the model ranking is stable between the two principled matchers: Kendall _τ_ ( strict _,_ token-F1 ) = 0 _._ 94 on both datasets ( _p_ _<_ 0 _._ 001 ). Only the permissive lenient bound reorders models on real data ( _τ_ ( strict _,_ lenient ) = 0 _._ 56 on VizWiz-answerable against 0 _._ 89 on VQAv2).

VQAv2 VizWiz (ans.)

Model strict lenient token-F1 strict lenient token-F1

Qwen3-VL-8B 0.717 0.746 0.784 0.609 0.713 0.843
Qwen2.5-VL-7B 0.781 0.800 0.851 0.581 0.705 0.819
LLaVA-1.6-13B 0.803 0.813 0.875 0.536 0.584 0.757
LLaVA-1.6-7B 0.800 0.807 0.870 0.522 0.549 0.725
InternVL3-8B 0.706 0.720 0.763 0.481 0.617 0.712
InternVL3.5-8B 0.738 0.755 0.809 0.404 0.580 0.663
Pixtral-12B 0.799 0.808 0.874 0.473 0.545 0.664
Idecs3-8B 0.788 0.797 0.863 0.469 0.506 0.680
Gemma-3-12B 0.211 0.577 0.461 0.224 0.567 0.604

4.4 Blind control: the image helps, but a language prior remains

Removing the image and keeping the question (a blind text-only control) separates perception from language priors, a known failure mode of VQA models [1]. On answerable questions the image contributes a large, signicant margin:
Qwen3-VL-8B falls from 0 _._ 609 to 0 _._ 315 (McNemar _p <_ 10 _[−]_ [100] ), and the remaining models, apart from Gemma-3-12B, fall by between 0 _._ 09 (InternVL3.5-8B) and 0 _._ 27 (Qwen2.5-VL-7B), all with Wilcoxon _p ≪_ 0 _._ 001 . Yet the blind oor is non-trivial ( 0 _._ 23 0 _._ 33 ): a sizeable fraction of answerable questions are guessable from text alone, a caution for any accuracy reported without such a control.
Gemma-3-12B is the exception: its blind score exceeds its sighted score on answerable questions ( +0 _._ 057, _p <_ 10 _[−]_ [4] ). This reects the exact-match penalty on its verbose sighted answers rather than any benet from removing the image.

The blind control also separates the two axes that the curated-to-real comparison conates: the questions and answers (VQAv2 is templated and carries a strong language prior) and the images (curated web photos versus blind-user captures). Running both datasets sighted and blind under a no-abstention prompt, so that a blind score is a language-prior oor rather than an abstention rate, splits the gap exactly into a question/prior axis, VQAv2blind _−_ VizWizblind, and an image axis, ( VQAv2s _−_ VQAv2blind ) _−_ ( VizWizs _−_ VizWizblind ) . For the models that answer imageless VQAv2 from the prior (LLaVA-1.6-7B/13B, Idecs3,
Pixtral; VQAv2-blind 0 _._ 38 0 _._ 45, matching the known VQAv2 prior) the gap is dominated by the question axis: 0 _._ 32 of a 0 _._ 37 gap ( 87% ), leaving only 0 _._ 05 for the image. Over all nine models the split is 0 _._ 19 question versus 0 _._ 17 image
(bootstrap 95% CIs over models [0 _._ 11 _,_ 0 _._ 27] and [0 _._ 07 _,_ 0 _._ 27], both excluding zero), but this understates the question axis: several models still decline to answer im

A Distribution-Shift and Protocol Audit on VizWiz 11

ageless VQAv2 even without an abstention clause, ooring their VQAv2-blind score and inating their apparent image axis. Either way, at least half of the curated-to-real gap, and among well-behaved models the large majority, is the question and answer distribution rather than the image being harder to read.
The control depends on the no-abstention prompt: under the default prompt an imageless model replies unanswerable, which scores zero on VQAv2 and would misattribute the whole gap to the image.

Removing the image entirely is only one way to break the question-image relationship. Three further controls separate having an image from having this image: a uniform grey image, a patch-shued image that preserves local statistics but destroys scene structure, and a mismatched image taken from a dierent item, which keeps a real photograph in the input while making it irrelevant to the question. On the answerable subset, mean accuracy falls from 0 _._ 478 clean to 0 _._ 376 (shued), 0 _._ 359 (grey) and 0 _._ 256 (mismatched); the paired drops are

_−_ 0 _._ 085, _−_ 0 _._ 102 and _−_ 0 _._ 205 . The mismatched control is the most damaging of the three, which is the expected ordering if the models are reading the photograph rather than pattern-matching on question form: a plausible but wrong image is worse than an obviously uninformative one. Abstention behaves consistently, rising to 61 98% under a grey image but only 35 69% under a mismatched one, so the models detect an empty image more reliably than a misleading one, which is the more dangerous failure for an assistive system.

One caveat applies to every answerable-subset number in this paper, including these. The soft VQA metric credits a reply of unanswerable whenever any of the ten annotators gave that answer, and 46% of items labelled answerable have at least one such annotation, worth 0 _._ 316 on average. Abstaining on the answerable subset therefore earns partial credit rather than zero: under a grey image, abstaining predictions average 0 _._ 406 where attempted ones average 0 _._ 154 .
The answerable split removes most of the abstention confound, not all of it; a stricter variant would exclude items with any unanswerable annotation, at the cost of discarding nearly half the subset.

4.5 Synthetic corruptions do not explain the shift

We applied a controlled blur/exposure/crop sweep to a xed subset of 886 answerable questions (the same items across all models and severities) to test whether the curated-to-real gap is a simple capture-degradation eect. It is not:
the per-model mean accuracy change over the sweep is small ( _−_ 0 _._ 028 to +0 _._ 044 ), four of the nine models even improve slightly on average, and the cells that survive Holm correction concentrate at the most severe blur and crop (blur level 5, crop level 4) rather than at the moderate severities (Figure 3). These VLMs are, at these severities, largely robust to moderate synthetic blur, exposure shifts, and o-centre crops. The real distribution shift (Sec. 4.1) therefore reects deeper dierences (content, question style, and capture eects not reproduced by these synthetic corruptions) rather than the blur and framing degradations one might rst suspect.

12 S. O. Kurashkin et al.

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
||||||||||
||||||||||

crop severity

VizWiz ANSWERABLE robustness to crop

0.70

0.65

0.60

0.55

0.50

0.45

0.40

0.35

0.3

0.2

VizWiz ANSWERABLE robustness to blur

0.65

0.60

0.55

0.50

0.45

0.40

0.35

0.30

0.25

0.20

|Col1|Col2|giiildnnlae tte vm eef airrcm nn1s|vv6a3ll_3 33_ 18_ 5_31 8b_ b2 8bb b lpqql|aiwwxv eetarnna1 23l6_5v_1 lv7 _2l8b _b7bb|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||

blur severity

|Col1|VizWiz ANSWERABLE robustness to exposure|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
||||gem<br>idef<br>inte<br>~~inte~~<br>llav|ma3_12b<br>ics3_8b<br>rnvl35_8b<br>~~rnvl3_8b~~<br>a16_13b|llav<br>pixt<br>qwe<br>~~qwe~~|a16_7b<br>ral_12b<br>n25vl_7b<br>~~n3vl_8b~~||||
|||||||||||
|||||||||||

exposure severity

0.70

0.65

0.60

0.55

0.50

0.45

0.40

0.35

0.30

0.25

0.20

0.15

Fig. 3: Accuracy on answerable VizWiz vs. corruption severity (blur, exposure, ocentre crop), with bootstrap condence bands. The curves are near-at across severities, conrming robustness to moderate synthetic corruptions.

To check that this negative result is not an accident of the three corruption families we happened to choose, we repeated the sweep with six further families that match the capture failures blind photographers report: camera pan (motion blur), sensor noise, specular glare, a nger over the lens (occlusion), low resolution, and severe misframing, at two severities each ( 108 additional jobisolated units). The conclusion holds and sharpens. Motion blur, sensor noise, glare and low resolution leave answerable-subset accuracy essentially unchanged
(mean paired change +0 _._ 003 to +0 _._ 015 ), occlusion costs a little at the severe level ( _−_ 0 _._ 020 ), and only severe misframing produces a clear loss ( _−_ 0 _._ 067 on average, _−_ 0 _._ 114 for Pixtral-12B). Where the image is degraded but still framed on the subject, these models cope; where the subject leaves the frame, they do not.
That single exception is informative, because misframing is a composition failure rather than an image-quality one, and it is the failure mode a capture-time interface could most directly help with.

The expanded sweep also demonstrates the abstention mechanism of Sec. 4.2 rather than merely arguing for it. Every corruption raises the abstention rate
(by 8 to 25 percentage points), and because correct abstention is rewarded on the 32 _._ 1% unanswerable class, aggregate accuracy rises even as answering ability stays at: in 88 of the 108 corrupted cells the aggregate VizWiz score exceeds the clean score. Qwen3-VL-8B reaches 0 _._ 753 under severe motion blur against 0 _._ 694 clean, and InternVL3-8B 0 _._ 659 against 0 _._ 579 . A reader who ranks assistive VLMs by aggregate VizWiz accuracy would conclude from these runs that damaging the photograph improves the model.

4.6 Cross-condition ranking

Figure 4 summarises the model ordering across all ten evaluation conditions. The
Friedman test rejects the null of equal model performance ( _χ_ [2] =59 _._ 4, _p_ =6 _._ 1 _×_
10 _[−]_ [10] ), but the Nemenyi critical dierence is wide ( CD=3 _._ 8 for nine models over ten conditions), so only the extremes are separated: the abstention-heavy Qwen models lead and the degenerate Gemma-3-12B trails, while the middle of the eld is statistically tied. The ranking tracks aggregate accuracy and therefore inherits the abstention confound of Sec. 4.2. The diagram's message is deliberately a

Qwen3-VL-8B

Qwen2.5-VL-7B

LLaVA-1.6-13B

LLaVA-1.6-7B

InternVL3-8B

A Distribution-Shift and Protocol Audit on VizWiz 13

CD = 3.80

average rank (1 = best)

1 2 3 4 5 6 7 8 9

Gemma-3-12B

Idefics3-8B

Pixtral-12B

InternVL3.5-8B

Fig. 4: Critical-dierence diagram of the nine models ranked by per-condition aggregate accuracy across the ten evaluation conditions of Sec. 3.3 (VQAv2 clean; VizWiz clean, blind, three blur severities, under- and over-exposure, and two crop severities)
(Friedman _χ_ [2] =59 _._ 4, _p_ =6 _._ 1 _×_ 10 _[−]_ [10] ; Nemenyi CD=3 _._ 8 ). Models joined by a bar are not signicantly dierent. Because the ranking uses aggregate per-condition accuracy, the most abstaining models place highest, which is a property of the aggregate metric rather than of answering ability.

negative one: across conditions the aggregate yields no robust capability ordering beyond the two extremes, which is itself the point, since a single-number ranking on this data is not meaningful.

5 Limitations

The lenient matcher is a deliberate upper bound that can over-credit; we report it only as a bracket around the standard metric, never as a headline. Our corruption sweep uses xed synthetic severities rather than the full natural variation of BLV capture, so its negative result bounds the role of the corruptions we test, not of all capture eects.

We evaluate open checkpoints _≤_ 13 B on a single GPU and exclude one gated model, so the claims are scoped to that set. Whether the same protocol sensitivities hold for substantially larger or proprietary systems is open; we would expect the mechanism to persist, since it follows from the composition of the benchmark rather than from model capacity, but we have not measured it. A single benchmark also limits the scope: VizWiz is the assistive benchmark with an explicit unanswerable class, which is what makes the confound measurable, and other assistive tasks may weight these axes dierently.

Decoding is greedy throughout, and the prompt is held xed across models within each sweep. Because we show that phrasing moves both abstention and answerable-subset accuracy, a shared prompt is itself a choice: dierent model families recommend dierent prompting conventions, and per-family prompts could shift absolute numbers, though the sweep suggests the ordering is the more stable quantity. Finally, this is an audit of measurement, not of downstream benet. We do not show that optimising under the proposed protocol yields models that serve blind and low-vision users better, and we report no study with

14 S. O. Kurashkin et al.

BLV participants; establishing that the split metrics and the graded matcher track perceived usefulness and safety needs a user study, which we regard as the natural next step for this line of work.

6 Conclusion

Aggregate accuracy on assistive VQA conates perception, abstention behaviour, and answer formatting. On real photographs taken by blind users these protocol choices move the headline number and, in the case of the answerability split and the abstention instruction, the model ranking itself; the answer matcher, by contrast, changes absolute scores while leaving the ranking stable across principled metrics. The curated-to-real shift is large and real on answerable questions but is hidden by the unanswerable class, and it is not explained by simple synthetic corruptions. We recommend an answerability-split, abstention-aware, match-bracketed evaluation, and release code and per-prediction outputs to support it.

A reporting checklist for assistive VQA.

1. Report the answerable and unanswerable subsets separately; do not headline
a single aggregate over both.
2. Report the abstention rate (fraction replying unanswerable) next to accuracy, and give the prompt's abstention instruction verbatim, as it governs
that rate.
3. Report a strict/lenient bracket and a graded matcher (token-F1); state which
matcher the headline number uses.
4. State the prompt and decoding (greedy or sampling) verbatim, since both
move the headline number.
5. Where feasible, include a blind text-only control to quantify the languageprior oor.

Data and code availability. Code, the exact prompts, the per-prediction model outputs, and the per-condition scoring tables are released at [https://github.](https://github.com/digger32/vlm-eval-a1)
[com/digger32/vlm-eval-a1](https://github.com/digger32/vlm-eval-a1) and archived at [https://doi.org/10.5281/](https://doi.org/10.5281/zenodo.21833735)
[zenodo.21833735.](https://doi.org/10.5281/zenodo.21833735) The release reproduces every number in this paper from the raw predictions, including the critical-dierence diagram of Figure 4.

References

1. Agrawal, A., Batra, D., Parikh, D., Kembhavi, A.: Don't just assume; look and
answer: Overcoming priors for visual question answering. In: CVPR. pp. 49714980
(2018)
2. Agrawal, P., Antoniak, S., Bou Hanna, E., Bout, B., Chaplot, D., et al.: Pixtral
12B. arXiv preprint arXiv:2410.07073 (2024)
3. Bafghi, R.A., Gurari, D.: A new dataset based on images taken by blind people for testing the robustness of image classication models trained for ImageNet
categories. In: CVPR. pp. 1626116270 (2023)

A Distribution-Shift and Protocol Audit on VizWiz 15

4. Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., et al.: Qwen3-VL technical report.
arXiv preprint arXiv:2511.21631 (2025)
5. Bai, S., Chen, K., Liu, X., Wang, J., Ge, W., Song, S., Dang, K., Wang, P., Wang,
S., Tang, J., et al.: Qwen2.5-VL technical report. arXiv preprint arXiv:2502.13923
(2025)
6. Dancette, C., Whitehead, S., Maheshwary, R., Vedantam, R., Scherer, S., Chen, X.,
Cord, M., Rohrbach, M.: Improving selective visual question answering by learning from your peers. In: CVPR. pp. 2404924059 (2023), arXiv:2306.08751
7. Dem²ar, J.: Statistical comparisons of classiers over multiple data sets. Journal
of Machine Learning Research 7, 130 (2006)
8. Gemma Team: Gemma 3 technical report. arXiv preprint arXiv:2503.19786 (2025)
9. Goyal, Y., Khot, T., Summers-Stay, D., Batra, D., Parikh, D.: Making the V in
VQA matter: Elevating the role of image understanding in visual question answering. In: CVPR. pp. 69046913 (2017)
10. Gurari, D., Li, Q., Stangl, A.J., Guo, A., Lin, C., Grauman, K., Luo, J., Bigham,
J.P.: VizWiz grand challenge: Answering visual questions from blind people. In:
CVPR. pp. 36083617 (2018)
11. Hansen, R., Setia, H., Hamilton-Fletcher, G., Jain, A., Liu, Z., Zoair, M.,
Aboutaleb, R., Wen, Q., Li, Y., Rizzo, J.R.: Visual language model-based food safety support for persons with blindness. In: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) Workshops. pp. 25032512
(2025)
12. Hendrycks, D., Dietterich, T.: Benchmarking neural network robustness to common
corruptions and perturbations. In: ICLR (2019)
13. Huh, M., Xu, F., Peng, Y.H., Chen, C., Murugu, H., Gurari, D., Choi, E., Pavel,
A.: Long-form answers to visual questions from blind and low vision people. In:
Conference on Language Modeling (COLM) (2024), arXiv:2408.06303
14. Jiang, X., Zheng, J., Liu, R., Li, J., Zhang, J., Matthiesen, S., Stiefelhagen, R.:
@Bench: Benchmarking vision-language models for human-centered assistive technology. In: WACV (2025), arXiv:2409.14215
15. Karamolegkou, A., Nikandrou, M., Pantazopoulos, G., Sanchez Villegas, D., Rust,
P., Dhar, R., Hershcovich, D., Søgaard, A.: Evaluating multimodal language models as visual assistants for visually impaired users. In: Proceedings of the 63rd
Annual Meeting of the Association for Computational Linguistics (ACL) (2025), arXiv:2503.22610
16. Karamolegkou, A., Rust, P., Cui, R., Cao, Y., Søgaard, A., Hershcovich, D.: Visionlanguage models under cultural and inclusive considerations. In: Proceedings of
the 1st Human-Centered Large Language Modeling Workshop (HuCLLM @ ACL
2024). pp. 5366 (2024), arXiv:2407.06177
17. Laurençon, H., Maraoti, A., Sanh, V., Tronchon, L.: Building and better understanding vision-language models: Insights and future directions. arXiv preprint
arXiv:2408.12637 (2024)
18. Liu, H., Li, C., Li, Y., Li, B., Zhang, Y., Shen, S., Lee, Y.J.: LLaVA-NeXT: Improved reasoning, OCR, and world knowledge. [https://llava-vl.github.io/](https://llava-vl.github.io/blog/2024-01-30-llava-next/)
[blog/2024-01-30-llava-next/](https://llava-vl.github.io/blog/2024-01-30-llava-next/) (January 2024)
19. Magay, A., Tripathi, D., Hao, Y., Fang, Y.: A light and smart wearable platform
with multimodal foundation model for enhanced spatial reasoning in people with blindness and low vision. In: Computer Vision ECCV 2024 Workshops (12th International Workshop on Assistive Computer Vision and Robotics, ACVR). Lecture Notes in Computer Science, vol. 15634, pp. 323339. Springer (2025)

16 S. O. Kurashkin et al.

20. Srinivasan, T., Hessel, J., Gupta, T., Lin, B.Y., Choi, Y., Thomason, J., Chandu,
K.R.: Selective selective prediction: Reducing unnecessary abstention in visionlanguage reasoning. arXiv preprint arXiv:2402.15610 (2024)
21. Wang, W., Gao, Z., Gu, L., Pu, H., Cui, L., Wei, X., Liu, Z., Jing, L., Ye, S., Shao,
J., et al.: InternVL3.5: Advancing open-source multimodal models in versatility, reasoning, and eciency. arXiv preprint arXiv:2508.18265 (2025)
22. Whitehead, S., Petryk, S., Shakib, V., Gonzalez, J., Darrell, T., Rohrbach, A.,
Rohrbach, M.: Reliable visual question answering: Abstain rather than answer incorrectly. In: ECCV. Lecture Notes in Computer Science, vol. 13696, pp. 148
166. Springer (2022), arXiv:2204.13631
23. Zhu, J., Wang, W., Chen, Z., Liu, Z., Ye, S., Gu, L., Tian, H., Duan, Y., Su, W.,
Shao, J., et al.: InternVL3: Exploring advanced training and test-time recipes for open-source multimodal models. arXiv preprint arXiv:2504.10479 (2025)
