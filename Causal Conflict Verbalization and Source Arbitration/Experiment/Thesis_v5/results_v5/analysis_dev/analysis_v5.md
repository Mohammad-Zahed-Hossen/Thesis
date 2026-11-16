# v5 analysis

Δℓ is image minus text. CDE is oriented toward the source the reversed verdict names.

**Dev data: for tuning and the freeze record only, not findings.**

## Qwen/Qwen2.5-VL-3B-Instruct | chartqa | dev

- Role: **exploratory**; primary outcome: **dl** (headline Math parser: `structured`)
- Items: 5; analysed: 5; meets R5 minimum: False
- Boundary mismatches: 0 rows (0.000; gate ≤ 0.01)
- **Secondary behavioural — ΔP(follow reversed verdict) at k=1 (`structured`):**
  - T1_beh (flip−own DiD, bind−nonbind) = 0.000 (95% CI [0.000, 0.000]), p = 1.0000, Holm p = 1.0000
  - Co-primary T1_beh matched-pair (para_flip−para DiD) = 0.000 (95% CI [0.000, 0.000]), p = 1.0000
  - Explicit-instruction benchmark B_beh = 0.250 (95% CI [0.050, 0.450]); image direction 0.400 (95% CI [0.100, 0.700]), text direction 0.100 (95% CI [0.000, 0.300]). A benchmark, not a ceiling.
  - **T2_beh**: Δ = 0.100 (90% CI [0.000, 0.300]) vs ε = 0.05; reading: **inconclusive (TOST power 0.00 < 0.80; not evidence for either hypothesis)**; Holm p = 1.0000; TOST power 0.00; ρ_beh (descriptive) = 0.400
  - **T2_beh_pair**: Δ = 0.100 (90% CI [0.000, 0.300]) vs ε = 0.05; reading: **inconclusive (TOST power 0.00 < 0.80; not evidence for either hypothesis)**; Holm p = 1.0000; TOST power 0.00; ρ_beh (descriptive) = 0.400
  - **T3_beh**: Δ = 0.100 (90% CI [0.000, 0.300]) vs ε = 0.05; reading: **inconclusive (TOST power 0.00 < 0.80; not evidence for either hypothesis)**; Holm p = 1.0000; TOST power 0.00; ρ_beh (descriptive) = 0.400
  - Directional (descriptive) binding_toward_image: Δ = 0.100 (95% CI [0.000, 0.300], n = 5); benchmark 0.400; ρ_beh 0.250
  - Directional (descriptive) binding_toward_text: Δ = n/a (95% CI n/a, n = 0); benchmark 0.100; ρ_beh n/a
  - Directional (descriptive) nonbinding_toward_image: Δ = 0.100 (95% CI [0.000, 0.300], n = 5); benchmark 0.400; ρ_beh 0.250
  - Directional (descriptive) nonbinding_toward_text: Δ = n/a (95% CI n/a, n = 0); benchmark 0.100; ρ_beh n/a
  - Per-order binding flip_minus_own: image_first = 0.000 (95% CI [0.000, 0.000], n = 5); text_first = 0.200 (95% CI [0.000, 0.600], n = 5)
  - Per-order binding matched_pair_para_flip_minus_para: image_first = 0.000 (95% CI [0.000, 0.000], n = 5); text_first = 0.200 (95% CI [0.000, 0.600], n = 5)
  - Per-order nonbinding flip_minus_own: image_first = 0.000 (95% CI [0.000, 0.000], n = 5); text_first = 0.200 (95% CI [0.000, 0.600], n = 5)
  - Per-order nonbinding matched_pair_para_flip_minus_para: image_first = 0.000 (95% CI [0.000, 0.000], n = 5); text_first = 0.200 (95% CI [0.000, 0.600], n = 5)
  - binding: flip−own = 0.100 (95% CI [0.000, 0.300], p = 0.5007); para_flip−para = 0.100 (95% CI [0.000, 0.300], p = 0.5007); decomp [none−own=0.000, flip−none=0.100, para_flip−none=0.100]
  - nonbinding: flip−own = 0.100 (95% CI [0.000, 0.300], p = 0.5007); para_flip−para = 0.100 (95% CI [0.000, 0.300], p = 0.5007); decomp [none−own=0.000, flip−none=0.100, para_flip−none=0.100]
- **PRIMARY READING under binding: EXPLORATORY REGIME, not a confirmatory reading: NOT A READING: n = 5 is below the R5 minimum of 100; the edit-gate pass rate is below 60% (prereg §8). The decision table alone would say: H1: the verdict decides, and binding strengthens it**
- **PRIMARY READING under non-binding: EXPLORATORY REGIME, not a confirmatory reading: NOT A READING: n = 5 is below the R5 minimum of 100; the edit-gate pass rate is below 60% (prereg §8). The decision table alone would say: H1: the verdict decides; no evidence that binding strengthens it**
- Wording-floor gate deciding the readings: fixed (signed mean, image<->text churn, neither shift) (prereg §7.6)
- Replay noise (donor vs nonbinding own): attributable flips = n/a (n = 0); any-change = 0.800; (diagnostic only; it does not move the wording-floor limit)
- Ceil_ℓ: 1.168, 95% CI [0.865, 1.471]
  - image direction vs non-binding: 0.602, 95% CI [0.409, 0.795]
  - text direction vs non-binding: 0.566, 95% CI [0.456, 0.680]
- **T1** DiD = 0.090 (95% CI [0.038, 0.143]), sign-flip p = 0.0297, Holm-adjusted p = 0.0520: binding strengthens the verdict's effect (this changes after Holm correction)
- **T2** CDE = 0.464 (95% CI [0.316, 0.654]); ρ = 0.397, 90% CI [0.322, 0.484]; reading: **decision-relevant**
- **T3** CDE = 0.373 (95% CI [0.246, 0.532]); ρ = 0.319, 90% CI [0.258, 0.392]; reading: **decision-relevant**
- Holm-adjusted p: {"T2": 0.0006, "T3": 0.052, "T1": 0.052}
- Behavioural, binding: Δ = 0.100, 90% CI [0.000, 0.300], TOST: not equivalent; change rate own vs flip 0.000
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), image<->text churn 0.000 (limit 0.05), neither shift 0.000 (limit ±0.1), gate: **pass**; diagnostics: any-change churn 0.000, replay flips n/a; TOST power at this noise 1.00
- Behavioural, nonbinding: Δ = 0.100, 90% CI [0.000, 0.300], TOST: not equivalent; change rate own vs flip 0.000
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), image<->text churn 0.000 (limit 0.05), neither shift 0.000 (limit ±0.1), gate: **pass**; diagnostics: any-change churn 0.000, replay flips n/a; TOST power at this noise 1.00
- Δℓ decision table (§2.2), binding: NOT A READING: n = 5 is below the R5 minimum of 100; the edit-gate pass rate is below 60% (prereg §8). The decision table alone would say: H1: the verdict decides, and binding strengthens it
- Δℓ decision table (§2.2), non-binding: NOT A READING: n = 5 is below the R5 minimum of 100; the edit-gate pass rate is below 60% (prereg §8). The decision table alone would say: H1: the verdict decides; no evidence that binding strengthens it

Behavioural numbers by answer parser (the lines above use `structured` per pre-freeze D3):

| Parser | Neither | Δ bind [90% CI] | Δ non-bind | Matched pair bind | Floor signed mean bind | Any-change churn bind / non-bind | image↔text flips bind (of attributable pairs) | flips non-bind |
|---|---:|---|---:|---:|---:|---|---|---|
| strict | 0.200 | 0.100 [0.000, 0.300] | 0.100 | 0.100 | 0.000 | 0.000 / 0.000 | 0.000 (n = 7) | 0.000 (n = 8) |

Does Δℓ track the answer? (behavioural rows with an attributable answer, same cell and template):

| Parser | Attributable rows | Sign agreement | Majority-class baseline | AUC image-first | AUC text-first |
|---|---:|---:|---:|---:|---:|
| strict | 96/120 | 0.990 | 0.990 | 1.000 | n/a |

Secondary:

- matched_pair_binding: {"n": 5, "mean": 0.6307, "ci95": [0.46528173298628345, 0.8291246085578072]}
- cde_binding_image_first: {"n": 5, "mean": 0.4829, "ci95": [0.19686009933754875, 0.8781332506575078]}
- cde_binding_text_first: {"n": 5, "mean": 0.4444, "ci95": [0.4117474449682049, 0.48617990170751]}
- cde_binding_order_sign_flip: False
- matched_pair_nonbinding: {"n": 5, "mean": 0.5074, "ci95": [0.37317713595727886, 0.6417145999532659]}
- cde_nonbinding_image_first: {"n": 5, "mean": 0.3853, "ci95": [0.14965660614456283, 0.71577765988186]}
- cde_nonbinding_text_first: {"n": 5, "mean": 0.361, "ci95": [0.3038276397812297, 0.4182711293268949]}
- cde_nonbinding_order_sign_flip: False
- cde_decomposition: {"binding_none_minus_own": {"n": 5, "mean": 0.20418067033565118, "ci95": [0.0342560122563979, 0.4498817495764039]}, "binding_flip_minus_none": {"n": 5, "mean": 0.2594748512379253, "ci95": [0.149646270715942, 0.3808437117623543]}, "binding_para_flip_minus_none": {"n": 5, "mean": 0.37575315336796244, "ci95": [0.25039572053860565, 0.49692238180905407]}, "nonbinding_none_minus_own": {"n": 5, "mean": 0.13672495676823018, "ci95": [0.01733324159649783, 0.2784846469944023]}, "nonbinding_flip_minus_none": {"n": 5, "mean": 0.23643058538946207, "ci95": [0.14047339073731566, 0.3323877800416085]}, "nonbinding_para_flip_minus_none": {"n": 5, "mean": 0.36000253387363046, "ci95": [0.21895417844803894, 0.501050889299222]}}
- per_template: {"binding_k1": {"n": 5, "mean": 0.49444557313031207, "ci95": [0.3385324441055612, 0.6905492772130217]}, "nonbinding_k1": {"n": 5, "mean": 0.3601325856125913, "ci95": [0.2358465661248192, 0.5101626097224653]}, "binding_k2": {"n": 5, "mean": 0.5124708646800717, "ci95": [0.3494471455548774, 0.7475860757252667]}, "nonbinding_k2": {"n": 5, "mean": 0.39308354065510986, "ci95": [0.2621767998089005, 0.5691033377797188]}, "binding_k3": {"n": 5, "mean": 0.37132742110377875, "ci95": [0.23040795236302075, 0.5551516794837137]}, "nonbinding_k3": {"n": 5, "mean": 0.32972501895681494, "ci95": [0.20565882019116546, 0.4895046603691299]}, "binding_k4": {"n": 5, "mean": 0.47637822738014324, "ci95": [0.3325684190520163, 0.6326813078052936]}, "nonbinding_k4": {"n": 5, "mean": 0.4096810234062529, "ci95": [0.27443610644394845, 0.5750419455417431]}}
- loto: {"binding_excl_k1": {"n": 5, "mean": 0.45339217105466456, "ci95": [0.308017136828146, 0.6414536734167076]}, "nonbinding_excl_k1": {"n": 5, "mean": 0.3774965276727259, "ci95": [0.24902290052404474, 0.5395273883128539]}, "binding_excl_k2": {"n": 5, "mean": 0.447383740538078, "ci95": [0.30402807195438075, 0.6199649835067816]}, "nonbinding_excl_k2": {"n": 5, "mean": 0.36651287599188637, "ci95": [0.24024615596268428, 0.5248130938193449]}, "binding_excl_k3": {"n": 5, "mean": 0.4944315550635091, "ci95": [0.3401826695708183, 0.6930919737542152]}, "nonbinding_excl_k3": {"n": 5, "mean": 0.3876323832246514, "ci95": [0.2590854825019293, 0.5486863244790584]}, "binding_excl_k4": {"n": 5, "mean": 0.45941461963805424, "ci95": [0.31000514517932765, 0.6607429965526169]}, "nonbinding_excl_k4": {"n": 5, "mean": 0.3609803817415054, "ci95": [0.23456072870829506, 0.517822525790608]}}
- behaviour_neither_rate_headline: 0.200
- behaviour_neither_rate: 0.200
- behaviour_neither_rate_strict: 0.200
- chartqa_answer_only_match_share: 0.800
- seconds_per_item: 32.230
- verdict_nll_mean_by_verdict: {"flip": 0.7184, "own": 0.3719, "para": 1.2087, "para_flip": 1.561}
- manipulation_check: {"donor": {"rows": 60, "with_stated_verdict": 33, "attributable_answers": 0, "answer_follows_stated_verdict": null}, "free_binding": {"rows": 60, "with_stated_verdict": 14, "attributable_answers": 0, "answer_follows_stated_verdict": null}}
- relative_uncertainty_binding: {"n": 5, "balance_point": null, "note": "balance point not estimable"}

## Qwen/Qwen2.5-VL-3B-Instruct | math | dev

- Role: **confirmatory**; primary outcome: **behaviour** (headline Math parser: `structured`)
- Items: 95; analysed: 95; meets R5 minimum: False
- Boundary mismatches: 0 rows (0.000; gate ≤ 0.01)
- **PRIMARY (D1) — ΔP(follow reversed verdict) at k=1 (`structured`):**
  - T1_beh (flip−own DiD, bind−nonbind) = 0.153 (95% CI [0.068, 0.242]), p = 0.0010, Holm p = 0.0010
  - Co-primary T1_beh matched-pair (para_flip−para DiD) = 0.216 (95% CI [0.142, 0.289]), p = 0.0001
  - Explicit-instruction benchmark B_beh = 0.471 (95% CI [0.418, 0.526]); image direction 0.447 (95% CI [0.379, 0.516]), text direction 0.495 (95% CI [0.421, 0.568]). A benchmark, not a ceiling.
  - **T2_beh**: Δ = 0.505 (90% CI [0.442, 0.568]) vs ε = 0.05; reading: **decision-relevant**; Holm p = 0.0008; TOST power 0.00; ρ_beh (descriptive) = 1.073
  - **T2_beh_pair**: Δ = 0.605 (90% CI [0.542, 0.668]) vs ε = 0.05; reading: **decision-relevant**; Holm p = 0.0008; TOST power 0.00; ρ_beh (descriptive) = 1.285
  - **T3_beh**: Δ = 0.353 (90% CI [0.284, 0.421]) vs ε = 0.05; reading: **decision-relevant**; Holm p = 0.0008; TOST power 0.00; ρ_beh (descriptive) = 0.749
  - Directional (descriptive) binding_toward_image: Δ = 0.468 (95% CI [0.383, 0.553], n = 94); benchmark 0.447; ρ_beh 1.046
  - Directional (descriptive) binding_toward_text: Δ = 0.653 (95% CI [0.500, 0.806], n = 36); benchmark 0.495; ρ_beh 1.319
  - Directional (descriptive) nonbinding_toward_image: Δ = 0.362 (95% CI [0.271, 0.452], n = 94); benchmark 0.447; ρ_beh 0.809
  - Directional (descriptive) nonbinding_toward_text: Δ = 0.431 (95% CI [0.250, 0.611], n = 36); benchmark 0.495; ρ_beh 0.870
  - Per-order binding flip_minus_own: image_first = 0.484 (95% CI [0.389, 0.589], n = 95); text_first = 0.526 (95% CI [0.421, 0.632], n = 95)
  - Per-order binding matched_pair_para_flip_minus_para: image_first = 0.547 (95% CI [0.442, 0.653], n = 95); text_first = 0.663 (95% CI [0.568, 0.758], n = 95)
  - Per-order nonbinding flip_minus_own: image_first = 0.232 (95% CI [0.116, 0.347], n = 95); text_first = 0.474 (95% CI [0.368, 0.579], n = 95)
  - Per-order nonbinding matched_pair_para_flip_minus_para: image_first = 0.274 (95% CI [0.179, 0.368], n = 95); text_first = 0.505 (95% CI [0.400, 0.611], n = 95)
  - binding: flip−own = 0.505 (95% CI [0.432, 0.579], p = 0.0001); para_flip−para = 0.605 (95% CI [0.532, 0.679], p = 0.0001); decomp [none−own=0.111, flip−none=0.395, para_flip−none=0.489]
  - nonbinding: flip−own = 0.353 (95% CI [0.268, 0.432], p = 0.0001); para_flip−para = 0.389 (95% CI [0.321, 0.463], p = 0.0001); decomp [none−own=0.105, flip−none=0.247, para_flip−none=0.247]
- **PRIMARY READING under binding: NOT A READING: n = 95 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides, and binding strengthens it (flip−own and para_flip−para agree)**
- **PRIMARY READING under non-binding: NOT A READING: n = 95 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides; no evidence that binding strengthens it**
- Wording-floor gate deciding the readings: fixed (signed mean, image<->text churn, neither shift) (prereg §7.6)
- The Δℓ lines below are secondary/diagnostic in this regime (D1).
- Replay noise (donor vs nonbinding own): attributable flips = 0.026 (n = 114); any-change = 0.105; (diagnostic only; it does not move the wording-floor limit)
- Ceil_ℓ: 0.149, 95% CI [0.118, 0.186]
  - image direction vs non-binding: -0.014, 95% CI [-0.043, 0.013]
  - text direction vs non-binding: 0.163, 95% CI [0.124, 0.209]
- **T1** DiD = 0.083 (95% CI [0.054, 0.113]), sign-flip p = 0.0001, Holm-adjusted p = 0.0003: binding strengthens the verdict's effect
- **T2** CDE = 0.229 (95% CI [0.180, 0.281]); ρ = 1.532, 90% CI [1.288, 1.818]; reading: **decision-relevant**
- **T3** CDE = 0.146 (95% CI [0.104, 0.192]); ρ = 0.974, 90% CI [0.743, 1.260]; reading: **decision-relevant**
- Holm-adjusted p: {"T1": 0.0003, "T2": 0.0004, "T3": 0.0004}
- Behavioural, binding: Δ = 0.505, 90% CI [0.442, 0.568], TOST: not equivalent; change rate own vs flip 0.800
  - Wording floor (para vs own): signed mean -0.047 (limit ±0.05), image<->text churn 0.045 (limit 0.05), neither shift 0.053 (limit ±0.1), gate: **pass**; diagnostics: any-change churn 0.237, replay flips 0.026; TOST power at this noise 0.00
- Behavioural, nonbinding: Δ = 0.353, 90% CI [0.284, 0.421], TOST: not equivalent; change rate own vs flip 0.615
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), image<->text churn 0.061 (limit 0.05), neither shift 0.037 (limit ±0.1), gate: **FAIL**; diagnostics: any-change churn 0.268, replay flips 0.026; TOST power at this noise 0.00
- Δℓ decision table (§2.2), binding: NOT A READING: n = 95 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides, and binding strengthens it
- Δℓ decision table (§2.2), non-binding: NOT A READING: n = 95 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides; no evidence that binding strengthens it

Behavioural numbers by answer parser (the lines above use `structured` per pre-freeze D3):

| Parser | Neither | Δ bind [90% CI] | Δ non-bind | Matched pair bind | Floor signed mean bind | Any-change churn bind / non-bind | image↔text flips bind (of attributable pairs) | flips non-bind |
|---|---:|---|---:|---:|---:|---|---|---|
| strict | 0.463 | 0.442 [0.379, 0.505] | 0.332 | 0.568 | -0.063 | 0.253 / 0.284 | 0.051 (n = 99) | 0.077 (n = 78) |
| structured | 0.395 | 0.505 [0.442, 0.568] | 0.353 | 0.605 | -0.047 | 0.237 / 0.268 | 0.045 (n = 110) | 0.061 (n = 98) |
| lenient | 0.301 | 0.595 [0.532, 0.658] | 0.400 | 0.700 | -0.074 | 0.205 / 0.189 | 0.040 (n = 124) | 0.078 (n = 129) |

Does Δℓ track the answer? (behavioural rows with an attributable answer, same cell and template):

| Parser | Attributable rows | Sign agreement | Majority-class baseline | AUC image-first | AUC text-first |
|---|---:|---:|---:|---:|---:|
| strict | 1224/2280 | 0.529 | 0.554 | 0.533 | 0.565 |
| structured | 1379/2280 | 0.523 | 0.560 | 0.541 | 0.568 |
| lenient | 1594/2280 | 0.511 | 0.538 | 0.548 | 0.561 |

Secondary:

Verdict-NLL resistance tertiles (`verdict_nll(flip) − verdict_nll(own)` under binding):

| Tertile | N | Mean ΔNLL | Δℓ CDE [95% CI] | Behavioural Δ [95% CI] |
|---|---:|---:|---|---|
| tertile1_low_resistance | 31 | 0.179 | 0.218 [0.159, 0.279] | 0.468 [0.323, 0.613] |
| tertile2_mid_resistance | 31 | 0.288 | 0.221 [0.133, 0.317] | 0.500 [0.387, 0.613] |
| tertile3_high_resistance | 33 | 0.447 | 0.247 [0.153, 0.354] | 0.545 [0.424, 0.667] |

- matched_pair_binding: {"n": 95, "mean": 0.2203, "ci95": [0.17612051626257227, 0.2648368407901806]}
- cde_binding_image_first: {"n": 95, "mean": 0.1883, "ci95": [0.13351501082488249, 0.24613683395123]}
- cde_binding_text_first: {"n": 95, "mean": 0.2696, "ci95": [0.18490869929861908, 0.363149055108742]}
- cde_binding_order_sign_flip: False
- matched_pair_nonbinding: {"n": 95, "mean": 0.1422, "ci95": [0.10686040760242696, 0.18048763524380354]}
- cde_nonbinding_image_first: {"n": 95, "mean": 0.1154, "ci95": [0.07322936208400338, 0.16225294480637686]}
- cde_nonbinding_text_first: {"n": 95, "mean": 0.1759, "ci95": [0.09939310991296263, 0.26575171394097785]}
- cde_nonbinding_order_sign_flip: False
- cde_decomposition: {"binding_none_minus_own": {"n": 95, "mean": 0.1368724661243859, "ci95": [0.08908734842350788, 0.1868818544298497]}, "binding_flip_minus_none": {"n": 95, "mean": 0.0921030784336076, "ci95": [0.041402492420466154, 0.14138924007847933]}, "binding_para_flip_minus_none": {"n": 95, "mean": 0.09083515679270995, "ci95": [0.04771271486350082, 0.13487339068868426]}, "nonbinding_none_minus_own": {"n": 95, "mean": 0.08315296771358638, "ci95": [0.04162043452783252, 0.12829757835583586]}, "nonbinding_flip_minus_none": {"n": 95, "mean": 0.06246995053787382, "ci95": [0.02214613612726374, 0.10372958266690392]}, "nonbinding_para_flip_minus_none": {"n": 95, "mean": 0.06634596932439435, "ci95": [0.02886323046089117, 0.10577461833234163]}}
- per_template: {"binding_k1": {"n": 95, "mean": 0.21822474272790968, "ci95": [0.16759730617771804, 0.2716716491765528]}, "nonbinding_k1": {"n": 95, "mean": 0.12047487703934229, "ci95": [0.07866712420184792, 0.16734946092025918]}, "binding_k2": {"n": 95, "mean": 0.21945206851310406, "ci95": [0.16402433343212894, 0.27816617206127275]}, "nonbinding_k2": {"n": 95, "mean": 0.14577424258590074, "ci95": [0.10272659395914732, 0.19351469128252324]}, "binding_k3": {"n": 95, "mean": 0.25422617837893896, "ci95": [0.18974567106186305, 0.32220581144465693]}, "nonbinding_k3": {"n": 95, "mean": 0.1629990514281937, "ci95": [0.1212840100173336, 0.20787835539032712]}, "binding_k4": {"n": 95, "mean": 0.2239991886120212, "ci95": [0.17500083759371823, 0.2762650960307272]}, "nonbinding_k4": {"n": 95, "mean": 0.1532435019524041, "ci95": [0.1041190896367985, 0.20927862228798927]}}
- loto: {"binding_excl_k1": {"n": 95, "mean": 0.23255914516802142, "ci95": [0.18272804263255327, 0.28575114893935977]}, "nonbinding_excl_k1": {"n": 95, "mean": 0.1540055986554995, "ci95": [0.11127674436714494, 0.20120040345247417]}, "binding_excl_k2": {"n": 95, "mean": 0.23215003657295663, "ci95": [0.18288646107537546, 0.28507383784164647]}, "nonbinding_excl_k2": {"n": 95, "mean": 0.1455724768066467, "ci95": [0.10388353225773053, 0.19181329642041775]}, "binding_excl_k3": {"n": 95, "mean": 0.2205586666176783, "ci95": [0.1701433189007278, 0.2742041876987361]}, "nonbinding_excl_k3": {"n": 95, "mean": 0.1398308738592157, "ci95": [0.0959880751290727, 0.18949667322426375]}, "binding_excl_k4": {"n": 95, "mean": 0.23063432987331758, "ci95": [0.18100359200274577, 0.2835289316174924]}, "nonbinding_excl_k4": {"n": 95, "mean": 0.1430827236844789, "ci95": [0.10274262169047423, 0.18687231432863957]}}
- cde_binding_baseline_abs_dl_tertile1: {"n": 31, "mean": 0.2151, "ci95": [0.12321353951507716, 0.3287042300965385]}
- cde_binding_baseline_abs_dl_tertile2: {"n": 31, "mean": 0.1772, "ci95": [0.10781456352775932, 0.25511931977983376]}
- cde_binding_baseline_abs_dl_tertile3: {"n": 33, "mean": 0.2906, "ci95": [0.21077088207980849, 0.369021484382227]}
- behaviour_neither_rate_headline: 0.395
- behaviour_neither_rate: 0.301
- behaviour_neither_rate_strict: 0.463
- seconds_per_item: 60.496
- verdict_nll_mean_by_verdict: {"flip": 1.0608, "own": 0.7348, "para": 1.1334, "para_flip": 1.5464}
- manipulation_check: {"donor": {"rows": 400, "with_stated_verdict": 400, "attributable_answers": 281, "answer_follows_stated_verdict": 0.7686832740213523, "answer_follows_stated_verdict_ci95": [0.7188612099644128, 0.8185053380782918]}, "free_binding": {"rows": 400, "with_stated_verdict": 315, "attributable_answers": 213, "answer_follows_stated_verdict": 0.9436619718309859, "answer_follows_stated_verdict_ci95": [0.9107981220657277, 0.971830985915493]}}
- relative_uncertainty_binding: {"n": 95, "balance_point": 0.1625, "slope": 1.1564, "inside": {"n": 38, "cde_mean": 0.2249577637346208, "cde_ci95": [0.15785962398270434, 0.2952143033581026]}, "outside": {"n": 57, "cde_mean": 0.23165406510690859, "cde_ci95": [0.16460307839110644, 0.3072554185137757]}}

## Qwen/Qwen2.5-VL-7B-Instruct | math | dev

- Role: **confirmatory**; primary outcome: **behaviour** (headline Math parser: `structured`)
- Items: 140; analysed: 140; meets R5 minimum: False
- Boundary mismatches: 0 rows (0.000; gate ≤ 0.01)
- **PRIMARY (D1) — ΔP(follow reversed verdict) at k=1 (`structured`):**
  - T1_beh (flip−own DiD, bind−nonbind) = 0.146 (95% CI [0.093, 0.200]), p = 0.0001, Holm p = 0.0004
  - Co-primary T1_beh matched-pair (para_flip−para DiD) = 0.414 (95% CI [0.354, 0.475]), p = 0.0001
  - Explicit-instruction benchmark B_beh = 0.811 (95% CI [0.773, 0.845]); image direction 0.804 (95% CI [0.757, 0.846]), text direction 0.818 (95% CI [0.768, 0.864]). A benchmark, not a ceiling.
  - **T2_beh**: Δ = 0.457 (90% CI [0.411, 0.500]) vs ε = 0.05; reading: **decision-relevant**; Holm p = 0.0006; TOST power 0.14; ρ_beh (descriptive) = 0.564
  - **T2_beh_pair**: Δ = 0.668 (90% CI [0.618, 0.714]) vs ε = 0.05; reading: **decision-relevant**; Holm p = 0.0006; TOST power 0.07; ρ_beh (descriptive) = 0.824
  - **T3_beh**: Δ = 0.311 (90% CI [0.264, 0.357]) vs ε = 0.05; reading: **decision-relevant**; Holm p = 0.0006; TOST power 0.09; ρ_beh (descriptive) = 0.383
  - Directional (descriptive) binding_toward_image: Δ = 0.364 (95% CI [0.296, 0.432], n = 140); benchmark 0.804; ρ_beh 0.453
  - Directional (descriptive) binding_toward_text: Δ = 0.612 (95% CI [0.506, 0.718], n = 85); benchmark 0.818; ρ_beh 0.748
  - Directional (descriptive) nonbinding_toward_image: Δ = 0.254 (95% CI [0.189, 0.318], n = 140); benchmark 0.804; ρ_beh 0.316
  - Directional (descriptive) nonbinding_toward_text: Δ = 0.376 (95% CI [0.282, 0.482], n = 85); benchmark 0.818; ρ_beh 0.460
  - Per-order binding flip_minus_own: image_first = 0.657 (95% CI [0.579, 0.736], n = 140); text_first = 0.257 (95% CI [0.186, 0.329], n = 140)
  - Per-order binding matched_pair_para_flip_minus_para: image_first = 0.750 (95% CI [0.679, 0.821], n = 140); text_first = 0.586 (95% CI [0.507, 0.664], n = 140)
  - Per-order nonbinding flip_minus_own: image_first = 0.464 (95% CI [0.379, 0.550], n = 140); text_first = 0.157 (95% CI [0.093, 0.221], n = 140)
  - Per-order nonbinding matched_pair_para_flip_minus_para: image_first = 0.279 (95% CI [0.200, 0.357], n = 140); text_first = 0.229 (95% CI [0.164, 0.300], n = 140)
  - binding: flip−own = 0.457 (95% CI [0.404, 0.511], p = 0.0001); para_flip−para = 0.668 (95% CI [0.611, 0.721], p = 0.0001); decomp [none−own=0.200, flip−none=0.257, para_flip−none=0.468]
  - nonbinding: flip−own = 0.311 (95% CI [0.254, 0.368], p = 0.0001); para_flip−para = 0.254 (95% CI [0.196, 0.311], p = 0.0001); decomp [none−own=0.171, flip−none=0.139, para_flip−none=0.114]
- **PRIMARY READING under binding: NOT A READING: n = 140 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides, and binding strengthens it (flip−own and para_flip−para agree)**
- **PRIMARY READING under non-binding: NOT A READING: n = 140 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides; no evidence that binding strengthens it**
- Wording-floor gate deciding the readings: fixed (signed mean, image<->text churn, neither shift) (prereg §7.6)
- The Δℓ lines below are secondary/diagnostic in this regime (D1).
- Replay noise (donor vs nonbinding own): attributable flips = 0.009 (n = 230); any-change = 0.071; (diagnostic only; it does not move the wording-floor limit)
- Ceil_ℓ: 1.382, 95% CI [1.196, 1.573]
  - image direction vs non-binding: 0.674, 95% CI [0.576, 0.779]
  - text direction vs non-binding: 0.707, 95% CI [0.583, 0.842]
- **T1** DiD = 0.290 (95% CI [0.237, 0.345]), sign-flip p = 0.0001, Holm-adjusted p = 0.0003: binding strengthens the verdict's effect
- **T2** CDE = 1.569 (95% CI [1.317, 1.834]); ρ = 1.136, 90% CI [1.032, 1.246]; reading: **decision-relevant**
- **T3** CDE = 1.279 (95% CI [1.049, 1.528]); ρ = 0.926, 90% CI [0.826, 1.030]; reading: **decision-relevant**
- Holm-adjusted p: {"T1": 0.0003, "T2": 0.0004, "T3": 0.0004}
- Behavioural, binding: Δ = 0.457, 90% CI [0.411, 0.500], TOST: not equivalent; change rate own vs flip 0.544
  - Wording floor (para vs own): signed mean -0.011 (limit ±0.05), image<->text churn 0.000 (limit 0.05), neither shift 0.011 (limit ±0.1), gate: **pass**; diagnostics: any-change churn 0.154, replay flips 0.009; TOST power at this noise 0.34
- Behavioural, nonbinding: Δ = 0.311, 90% CI [0.264, 0.357], TOST: not equivalent; change rate own vs flip 0.368
  - Wording floor (para vs own): signed mean -0.054 (limit ±0.05), image<->text churn 0.058 (limit 0.05), neither shift 0.021 (limit ±0.1), gate: **FAIL**; diagnostics: any-change churn 0.154, replay flips 0.009; TOST power at this noise 0.52
- Δℓ decision table (§2.2), binding: NOT A READING: n = 140 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides, and binding strengthens it
- Δℓ decision table (§2.2), non-binding: NOT A READING: n = 140 is below the R5 minimum of 150. The decision table alone would say: H1: the verdict decides; no evidence that binding strengthens it

Behavioural numbers by answer parser (the lines above use `structured` per pre-freeze D3):

| Parser | Neither | Δ bind [90% CI] | Δ non-bind | Matched pair bind | Floor signed mean bind | Any-change churn bind / non-bind | image↔text flips bind (of attributable pairs) | flips non-bind |
|---|---:|---|---:|---:|---:|---|---|---|
| strict | 0.619 | 0.193 [0.154, 0.232] | 0.146 | 0.339 | -0.018 | 0.218 / 0.211 | 0.000 (n = 68) | 0.014 (n = 69) |
| structured | 0.182 | 0.457 [0.411, 0.500] | 0.311 | 0.668 | -0.011 | 0.154 / 0.154 | 0.000 (n = 200) | 0.058 (n = 223) |
| lenient | 0.118 | 0.493 [0.450, 0.536] | 0.321 | 0.714 | 0.011 | 0.082 / 0.121 | 0.000 (n = 234) | 0.062 (n = 242) |

Does Δℓ track the answer? (behavioural rows with an attributable answer, same cell and template):

| Parser | Attributable rows | Sign agreement | Majority-class baseline | AUC image-first | AUC text-first |
|---|---:|---:|---:|---:|---:|
| strict | 1280/3360 | 0.562 | 0.770 | 0.690 | 0.698 |
| structured | 2748/3360 | 0.574 | 0.595 | 0.759 | 0.699 |
| lenient | 2964/3360 | 0.568 | 0.582 | 0.752 | 0.700 |

Secondary:

Verdict-NLL resistance tertiles (`verdict_nll(flip) − verdict_nll(own)` under binding):

| Tertile | N | Mean ΔNLL | Δℓ CDE [95% CI] | Behavioural Δ [95% CI] |
|---|---:|---:|---|---|
| tertile1_low_resistance | 46 | 0.246 | 1.703 [1.318, 2.096] | 0.565 [0.467, 0.663] |
| tertile2_mid_resistance | 46 | 0.368 | 1.666 [1.196, 2.161] | 0.380 [0.293, 0.467] |
| tertile3_high_resistance | 48 | 0.563 | 1.349 [0.938, 1.855] | 0.427 [0.344, 0.510] |

- matched_pair_binding: {"n": 140, "mean": 2.3184, "ci95": [2.0153962860192722, 2.6326727869033943]}
- cde_binding_image_first: {"n": 140, "mean": 1.6964, "ci95": [1.376587286890123, 2.0373928367016125]}
- cde_binding_text_first: {"n": 140, "mean": 1.4425, "ci95": [1.1570534433408246, 1.7533292755770236]}
- cde_binding_order_sign_flip: False
- matched_pair_nonbinding: {"n": 140, "mean": 1.8522, "ci95": [1.5992855456876431, 2.113731815118703]}
- cde_nonbinding_image_first: {"n": 140, "mean": 1.2962, "ci95": [1.018336432642141, 1.5916581394887377]}
- cde_nonbinding_text_first: {"n": 140, "mean": 1.2628, "ci95": [0.9902175518803438, 1.5622994759677857]}
- cde_nonbinding_order_sign_flip: False
- cde_decomposition: {"binding_none_minus_own": {"n": 140, "mean": 1.4558899595815966, "ci95": [1.2228772225827265, 1.7040394258992249]}, "binding_flip_minus_none": {"n": 140, "mean": 0.11354652045643802, "ci95": [-0.043680182302226964, 0.27042250226547154]}, "binding_para_flip_minus_none": {"n": 140, "mean": 0.7050086330571763, "ci95": [0.571813568514804, 0.8468676194956425]}, "nonbinding_none_minus_own": {"n": 140, "mean": 1.190103357785303, "ci95": [0.9801341580802336, 1.4136421442700908]}, "nonbinding_flip_minus_none": {"n": 140, "mean": 0.0893817817325994, "ci95": [-0.05582019312869353, 0.23437187821629377]}, "nonbinding_para_flip_minus_none": {"n": 140, "mean": 0.5722584833779149, "ci95": [0.4566229965863662, 0.7005252199932545]}}
- per_template: {"binding_k1": {"n": 140, "mean": 1.55624012303936, "ci95": [1.3030349671484878, 1.8258218947187346]}, "nonbinding_k1": {"n": 140, "mean": 1.230174611105793, "ci95": [1.0003672749207737, 1.4815042584638378]}, "binding_k2": {"n": 140, "mean": 1.6440199610935917, "ci95": [1.378795050779632, 1.9239895703547931]}, "nonbinding_k2": {"n": 140, "mean": 1.3106242399100474, "ci95": [1.0682879024236047, 1.5727517115881393]}, "binding_k3": {"n": 140, "mean": 1.4762736228815976, "ci95": [1.2392113683723687, 1.727734708318984]}, "nonbinding_k3": {"n": 140, "mean": 1.2005320515802373, "ci95": [0.9902585315053425, 1.4222231416783093]}, "binding_k4": {"n": 140, "mean": 1.601212213137589, "ci95": [1.338413073738294, 1.8787214821805382]}, "nonbinding_k4": {"n": 140, "mean": 1.3766096554755323, "ci95": [1.121583035964341, 1.6487277358314651]}}
- loto: {"binding_excl_k1": {"n": 140, "mean": 1.5738352657042596, "ci95": [1.3214178848060267, 1.8379480466283167]}, "nonbinding_excl_k1": {"n": 140, "mean": 1.2959219823219392, "ci95": [1.064036924166978, 1.5424144827998227]}, "binding_excl_k2": {"n": 140, "mean": 1.5445753196861822, "ci95": [1.2960439514102902, 1.8035332900349124]}, "nonbinding_excl_k2": {"n": 140, "mean": 1.2691054393871875, "ci95": [1.0414787964828667, 1.514149782993593]}, "binding_excl_k3": {"n": 140, "mean": 1.600490765756847, "ci95": [1.3420633808856623, 1.8748381508691114]}, "nonbinding_excl_k3": {"n": 140, "mean": 1.3058028354971243, "ci95": [1.0655801817509776, 1.564300899028544]}, "binding_excl_k4": {"n": 140, "mean": 1.5588445690048498, "ci95": [1.307718385210561, 1.8229420143875485]}, "nonbinding_excl_k4": {"n": 140, "mean": 1.2471103008653592, "ci95": [1.022248354487113, 1.488032452015699]}}
- cde_binding_baseline_abs_dl_tertile1: {"n": 46, "mean": 1.0986, "ci95": [0.7795824297039563, 1.4574385604921447]}
- cde_binding_baseline_abs_dl_tertile2: {"n": 46, "mean": 1.3768, "ci95": [1.0018794666428834, 1.7813680752083805]}
- cde_binding_baseline_abs_dl_tertile3: {"n": 48, "mean": 2.2053, "ci95": [1.7173083897997465, 2.749987984819156]}
- behaviour_neither_rate_headline: 0.182
- behaviour_neither_rate: 0.118
- behaviour_neither_rate_strict: 0.619
- seconds_per_item: 178.249
- verdict_nll_mean_by_verdict: {"flip": 1.0843, "own": 0.6814, "para": 1.3871, "para_flip": 1.8786}
- manipulation_check: {"donor": {"rows": 400, "with_stated_verdict": 399, "attributable_answers": 332, "answer_follows_stated_verdict": 0.9397590361445783, "answer_follows_stated_verdict_ci95": [0.9126506024096386, 0.963855421686747]}, "free_binding": {"rows": 400, "with_stated_verdict": 396, "attributable_answers": 316, "answer_follows_stated_verdict": 0.9841772151898734, "answer_follows_stated_verdict_ci95": [0.9683544303797469, 0.9968354430379747]}}
- relative_uncertainty_binding: {"n": 140, "balance_point": -0.1988, "slope": 0.8022, "inside": {"n": 39, "cde_mean": 1.0961110356828512, "cde_ci95": [0.6996942716100333, 1.5395479604822877]}, "outside": {"n": 101, "cde_mean": 1.7522057110266698, "cde_ci95": [1.4550455660185488, 2.0718335068668665]}}

## Size comparison: Qwen2.5-VL-3B vs. Qwen2.5-VL-7B (secondary, descriptive)

### Regime: math

- Common competent & gated items: N = 80
- ρ_bind (3B) on intersection: 1.513
- ρ_bind (7B) on intersection: 1.064
- Δρ (7B minus 3B): -0.449 (95% CI [-0.833, -0.124])
- Behavioural Δ_bind (flip−own) 3B vs 7B on intersection (N = 80): 0.519 vs 0.475, Δ_bind(7B−3B) = -0.044 (95% CI [-0.144, 0.056])
- Behavioural Δ_bind matched-pair (para_flip−para) 3B vs 7B (N = 80): 0.606 vs 0.675, Δ_bind_pair(7B−3B) = 0.069 (95% CI [-0.044, 0.175])

## Gate reports

- v5dev_conflict_tp_qwen2.gates.json: {"items": 200, "competent": 0, "taken": 0, "no_donor": 0, "passed": 0, "edit_gate_pass_rate": null, "edit_gate_ok": false, "meets_min_items": false, "jaccard_multiset_flip_min": null, "jaccard_multiset_flip_mean": null, "swaps_per_flip": {}, "swap_scope": "sentence", "source_nouns_outside_swap_scope": {}, "own_source_by_order": {}, "fail_reasons_by_order": {}, "competency_parser": "structured"}
- v5dev_conflict_tp_qwen25.gates.json: {"items": 200, "competent": 95, "taken": 95, "no_donor": 0, "passed": 95, "edit_gate_pass_rate": 1.0, "edit_gate_ok": true, "meets_min_items": false, "jaccard_multiset_flip_min": 0.88, "jaccard_multiset_flip_mean": 0.9468, "swaps_per_flip": {"1": 137, "2": 53}, "swap_scope": "sentence", "source_nouns_outside_swap_scope": {"0": 190}, "own_source_by_order": {"image_first:image": 36, "text_first:text": 94, "image_first:text": 59, "text_first:image": 1}, "fail_reasons_by_order": {}, "competency_parser": "structured"}
- v5dev_conflict_tp_qwen25_7b.gates.json: {"items": 200, "competent": 154, "taken": 154, "no_donor": 0, "passed": 140, "edit_gate_pass_rate": 0.9091, "edit_gate_ok": true, "meets_min_items": false, "jaccard_multiset_flip_min": 0.875, "jaccard_multiset_flip_mean": 0.9557, "swaps_per_flip": {"1": 211, "2": 69}, "swap_scope": "sentence", "source_nouns_outside_swap_scope": {"0": 280}, "own_source_by_order": {"image_first:image": 85, "text_first:text": 140, "image_first:text": 55}, "fail_reasons_by_order": {"gate3_too_many_swaps": 13, "own_undetermined": 1}, "competency_parser": "structured"}
- v5dev_chartqa_tp_qwen2.gates.json: {"items": 30, "competent": 10, "taken": 10, "no_donor": 0, "passed": 0, "edit_gate_pass_rate": 0.0, "edit_gate_ok": false, "meets_min_items": false, "jaccard_multiset_flip_min": null, "jaccard_multiset_flip_mean": null, "swaps_per_flip": {}, "swap_scope": "sentence", "source_nouns_outside_swap_scope": {}, "own_source_by_order": {}, "fail_reasons_by_order": {"own_absent": 18, "own_undetermined": 2}, "competency_parser": "structured"}
- v5dev_chartqa_tp_qwen25.gates.json: {"items": 30, "competent": 13, "taken": 13, "no_donor": 0, "passed": 5, "edit_gate_pass_rate": 0.3846, "edit_gate_ok": false, "meets_min_items": false, "jaccard_multiset_flip_min": 0.8667, "jaccard_multiset_flip_mean": 0.8856, "swaps_per_flip": {"1": 9, "2": 1}, "swap_scope": "sentence", "source_nouns_outside_swap_scope": {"0": 10}, "own_source_by_order": {"image_first:report": 5, "text_first:report": 5}, "fail_reasons_by_order": {"own_absent": 10, "gate_answer_leakage": 2}, "competency_parser": "structured"}
- v5dev_chartqa_tp_qwen25_7b.gates.json: {"items": 30, "competent": 13, "taken": 13, "no_donor": 0, "passed": 0, "edit_gate_pass_rate": 0.0, "edit_gate_ok": false, "meets_min_items": false, "jaccard_multiset_flip_min": null, "jaccard_multiset_flip_mean": null, "swaps_per_flip": {}, "swap_scope": "sentence", "source_nouns_outside_swap_scope": {}, "own_source_by_order": {}, "fail_reasons_by_order": {"gate3_too_many_swaps": 9, "gate_answer_leakage": 15}, "competency_parser": "structured"}

## Multi-model item intersections

- math: intersection N = 80 across {'Qwen/Qwen2.5-VL-3B-Instruct': 95, 'Qwen/Qwen2.5-VL-7B-Instruct': 140}

## Provenance

- Duplicate rows: 0
- v5dev_conflict_tp_qwen25.manifest.json: {"resolved_model_commit": "66285546d2b821cf421d4f5eb2576359d3770cd3", "peak_vram_gb": 7.531827449798584, "written_at": "2026-11-15T22:19:36", "n_items": 95}
- v5dev_conflict_tp_qwen25_7b.manifest.json: {"resolved_model_commit": "cc594898137f460bfe9f0759e9844b3ce807cfb5", "peak_vram_gb": 15.687393188476562, "written_at": "2026-11-16T11:24:43", "n_items": 140}
- v5dev_chartqa_tp_qwen25.manifest.json: {"resolved_model_commit": "66285546d2b821cf421d4f5eb2576359d3770cd3", "peak_vram_gb": 7.503275394439697, "written_at": "2026-11-15T22:51:32", "n_items": 5}
