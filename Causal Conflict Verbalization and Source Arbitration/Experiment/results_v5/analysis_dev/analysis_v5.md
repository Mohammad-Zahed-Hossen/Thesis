# v5 analysis

Δℓ is image minus text. CDE is oriented toward the source the reversed verdict names.

**Dev data: for tuning and the freeze record only, not findings.**

## Qwen/Qwen2.5-VL-3B-Instruct | chartqa | dev

- Items: 6; analysed: 6; meets R5 minimum: False
- Boundary mismatches: 0 rows (0.000; gate ≤ 0.01)
- Ceil_ℓ: 1.148, 95% CI [0.903, 1.401]
  - image direction vs non-binding: 0.607, 95% CI [0.446, 0.766]
  - text direction vs non-binding: 0.541, 95% CI [0.442, 0.651]
- **T1** DiD = 0.104 (95% CI [0.053, 0.152]), sign-flip p = 0.0157, Holm-adjusted p = 0.0157: binding strengthens the verdict's effect
- **T2** CDE = 0.461 (95% CI [0.338, 0.624]); ρ = 0.401, 90% CI [0.332, 0.475]; reading: **decision-relevant**
- **T3** CDE = 0.357 (95% CI [0.252, 0.494]); ρ = 0.311, 90% CI [0.260, 0.371]; reading: **decision-relevant**
- Holm-adjusted p: {"T2": 0.0003, "T3": 0.0114, "T1": 0.0157}
- Behavioural, binding: Δ = 0.083, 90% CI [0.000, 0.250], TOST: not equivalent; change rate own vs flip 0.000
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), churn rate 0.000 (limit 0.05), gate: **pass**; TOST power at this noise 1.00
- Behavioural, nonbinding: Δ = 0.083, 90% CI [0.000, 0.250], TOST: not equivalent; change rate own vs flip 0.000
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), churn rate 0.000 (limit 0.05), gate: **pass**; TOST power at this noise 1.00
- **Combined reading under binding: H1: the verdict decides, and binding strengthens it**
- **Combined reading under non-binding: H1: the verdict decides; no evidence that binding strengthens it**

Secondary:

- matched_pair_binding: {"n": 6, "mean": 0.6039, "ci95": [0.4660683366629706, 0.7737071271318806]}
- cde_binding_image_first: {"n": 6, "mean": 0.4293, "ci95": [0.18801871450001875, 0.762641082785563]}
- cde_binding_text_first: {"n": 6, "mean": 0.4924, "ci95": [0.42134602810256183, 0.5965832654837868]}
- matched_pair_nonbinding: {"n": 6, "mean": 0.4786, "ci95": [0.3590488666441969, 0.6057570709290303]}
- cde_nonbinding_image_first: {"n": 6, "mean": 0.336, "ci95": [0.13223949345111682, 0.6189189776331963]}
- cde_nonbinding_text_first: {"n": 6, "mean": 0.3774, "ci95": [0.3219530936543985, 0.4292368842920647]}
- cde_decomposition: {"binding_none_minus_own": {"n": 6, "mean": 0.18830523343064365, "ci95": [0.04670135169793258, 0.3972762331460318]}, "binding_flip_minus_none": {"n": 6, "mean": 0.2725399247350651, "ci95": [0.18151282221677115, 0.37200952878174576]}, "nonbinding_none_minus_own": {"n": 6, "mean": 0.10539047460182094, "ci95": [-0.00633339668608338, 0.24296331860253606]}, "nonbinding_flip_minus_none": {"n": 6, "mean": 0.25130906629177235, "ci95": [0.16709860618054032, 0.3355195264030044]}}
- per_template: {"binding_k1": {"n": 6, "mean": 0.49085860912859464, "ci95": [0.3609310016079689, 0.6588656882006844]}, "nonbinding_k1": {"n": 6, "mean": 0.3393054443781795, "ci95": [0.22972164287736327, 0.4692091529230109]}, "binding_k2": {"n": 6, "mean": 0.5134242813372111, "ci95": [0.3703442999634717, 0.7093536238748736]}, "nonbinding_k2": {"n": 6, "mean": 0.37915052804463717, "ci95": [0.27214242474696626, 0.5258336923151445]}, "binding_k3": {"n": 6, "mean": 0.36952476179972615, "ci95": [0.25155136206788786, 0.5258654019297359]}, "nonbinding_k3": {"n": 6, "mean": 0.3176930875934583, "ci95": [0.21602060739921095, 0.4508427887703874]}, "binding_k4": {"n": 6, "mean": 0.4695729803973033, "ci95": [0.3497314734571975, 0.6084190819532278]}, "nonbinding_k4": {"n": 6, "mean": 0.3906491035580984, "ci95": [0.2779450060895114, 0.5284677269397674]}}
- loto: {"binding_excl_k1": {"n": 6, "mean": 0.4508406745114135, "ci95": [0.3296948126559814, 0.6125574877513119]}, "nonbinding_excl_k1": {"n": 6, "mean": 0.3624975730653979, "ci95": [0.25646377336400933, 0.5006288360641015]}, "binding_excl_k2": {"n": 6, "mean": 0.443318783775208, "ci95": [0.32380828951389523, 0.595388379537245]}, "nonbinding_excl_k2": {"n": 6, "mean": 0.34921587850991204, "ci95": [0.24399361181891033, 0.48468307309360625]}, "binding_excl_k3": {"n": 6, "mean": 0.491285290287703, "ci95": [0.36278686858657033, 0.6567933229871818]}, "nonbinding_excl_k3": {"n": 6, "mean": 0.3697016919936383, "ci95": [0.26257927472470327, 0.5090939813510075]}, "binding_excl_k4": {"n": 6, "mean": 0.4579358840885106, "ci95": [0.3333331222206147, 0.6282759794565478]}, "nonbinding_excl_k4": {"n": 6, "mean": 0.3453830200054249, "ci95": [0.24264071884126345, 0.47999615735979106]}}
- cde_binding_baseline_abs_dl_tertile1: {"n": 2, "mean": 0.361, "ci95": [0.2752775215364333, 0.44679334112637054]}
- cde_binding_baseline_abs_dl_tertile2: {"n": 2, "mean": 0.3611, "ci95": [0.3054067668970674, 0.41686124137049774]}
- cde_binding_baseline_abs_dl_tertile3: {"n": 2, "mean": 0.6604, "ci95": [0.4847945575165795, 0.8359375205473043]}
- behaviour_neither_rate: 0.243
- behaviour_neither_rate_strict: 0.243
- chartqa_answer_only_match_share: 0.757
- seconds_per_item: 32.771
- verdict_nll_mean_by_verdict: {"flip": 0.928, "none": 1.1876, "own": 0.7535, "para": 1.0117, "para_flip": 1.1347}
- manipulation_check: {"donor": {"rows": 60, "with_stated_verdict": 28, "attributable_answers": 0, "answer_follows_stated_verdict": null}, "free_binding": {"rows": 60, "with_stated_verdict": 12, "attributable_answers": 0, "answer_follows_stated_verdict": null}}
- relative_uncertainty_binding: {"n": 6, "balance_point": null, "note": "balance point not estimable"}

## Qwen/Qwen2.5-VL-3B-Instruct | math | dev

- Items: 80; analysed: 80; meets R5 minimum: False
- Boundary mismatches: 0 rows (0.000; gate ≤ 0.01)
- Ceil_ℓ: 0.152, 95% CI [0.117, 0.193]
  - image direction vs non-binding: -0.009, 95% CI [-0.041, 0.021]
  - text direction vs non-binding: 0.161, 95% CI [0.117, 0.212]
- **T1** DiD = 0.083 (95% CI [0.051, 0.113]), sign-flip p = 0.0001, Holm-adjusted p = 0.0003: binding strengthens the verdict's effect
- **T2** CDE = 0.233 (95% CI [0.182, 0.291]); ρ = 1.529, 90% CI [1.258, 1.865]; reading: **decision-relevant**
- **T3** CDE = 0.150 (95% CI [0.106, 0.204]); ρ = 0.984, 90% CI [0.736, 1.305]; reading: **decision-relevant**
- Holm-adjusted p: {"T1": 0.0003, "T2": 0.0003, "T3": 0.0003}
- Behavioural, binding: Δ = 0.581, 90% CI [0.512, 0.644], TOST: not equivalent; change rate own vs flip 0.809
  - Wording floor (para vs own): signed mean -0.081 (limit ±0.05), churn rate 0.029 (limit 0.05), gate: **FAIL**; TOST power at this noise 0.00
- Behavioural, nonbinding: Δ = 0.438, 90% CI [0.369, 0.506], TOST: not equivalent; change rate own vs flip 0.648
  - Wording floor (para vs own): signed mean -0.031 (limit ±0.05), churn rate 0.076 (limit 0.05), gate: **FAIL**; TOST power at this noise 0.00
- **Combined reading under binding: H1: the verdict decides, and binding strengthens it**
- **Combined reading under non-binding: H1: the verdict decides; no evidence that binding strengthens it**

Secondary:

- matched_pair_binding: {"n": 80, "mean": 0.2248, "ci95": [0.18066392675073456, 0.27429860418030994]}
- cde_binding_image_first: {"n": 80, "mean": 0.1846, "ci95": [0.13126394132946856, 0.24131976157087226]}
- cde_binding_text_first: {"n": 80, "mean": 0.2814, "ci95": [0.19010775506359884, 0.38766000074089235]}
- matched_pair_nonbinding: {"n": 80, "mean": 0.1458, "ci95": [0.10590879001358887, 0.191670064118852]}
- cde_nonbinding_image_first: {"n": 80, "mean": 0.1147, "ci95": [0.07418221643136469, 0.15794659726998178]}
- cde_nonbinding_text_first: {"n": 80, "mean": 0.1851, "ci95": [0.09868892866556662, 0.2942477153643812]}
- cde_decomposition: {"binding_none_minus_own": {"n": 80, "mean": 0.1374653036240246, "ci95": [0.08808219485320845, 0.18993232828313042]}, "binding_flip_minus_none": {"n": 80, "mean": 0.09550280863217873, "ci95": [0.042387066654569344, 0.15030937652088444]}, "nonbinding_none_minus_own": {"n": 80, "mean": 0.07555030267877252, "ci95": [0.03451147681929677, 0.12013077478060738]}, "nonbinding_flip_minus_none": {"n": 80, "mean": 0.07438364130705546, "ci95": [0.030931871689396137, 0.12053277738868533]}}
- per_template: {"binding_k1": {"n": 80, "mean": 0.22107593748953755, "ci95": [0.16746023083933145, 0.2834547189961092]}, "nonbinding_k1": {"n": 80, "mean": 0.1263945520929216, "ci95": [0.08362950390108015, 0.17976521313883978]}, "binding_k2": {"n": 80, "mean": 0.22446580818766965, "ci95": [0.16626042335092042, 0.29226538960481047]}, "nonbinding_k2": {"n": 80, "mean": 0.15306517140255893, "ci95": [0.10707433103727093, 0.20866042388201703]}, "binding_k3": {"n": 80, "mean": 0.2540480348193766, "ci95": [0.18576963944035865, 0.32829103057429526]}, "nonbinding_k3": {"n": 80, "mean": 0.1621966090691664, "ci95": [0.11865514299411248, 0.21354197360248753]}, "binding_k4": {"n": 80, "mean": 0.23228266852822949, "ci95": [0.1800832243746961, 0.29261043868303016]}, "nonbinding_k4": {"n": 80, "mean": 0.15807944337866503, "ci95": [0.10677896780055743, 0.22315756258296457]}}
- loto: {"binding_excl_k1": {"n": 80, "mean": 0.23693217051175855, "ci95": [0.18553667039961713, 0.2960187105239578]}, "nonbinding_excl_k1": {"n": 80, "mean": 0.1577804079501301, "ci95": [0.11288472122424598, 0.21243888507744363]}, "binding_excl_k2": {"n": 80, "mean": 0.23580221361238118, "ci95": [0.18521378970963837, 0.29416985409868834]}, "nonbinding_excl_k2": {"n": 80, "mean": 0.14889020151358434, "ci95": [0.10498550158683145, 0.2030170123338305]}, "binding_excl_k3": {"n": 80, "mean": 0.22594147140181225, "ci95": [0.17329471725365675, 0.28747087646943326]}, "nonbinding_excl_k3": {"n": 80, "mean": 0.14584638895804852, "ci95": [0.10029043623125755, 0.20257836359849637]}, "binding_excl_k4": {"n": 80, "mean": 0.23319659349886127, "ci95": [0.18192566559301485, 0.2916809194552485]}, "nonbinding_excl_k4": {"n": 80, "mean": 0.14721877752154897, "ci95": [0.10503134057250567, 0.19793973613266316]}}
- cde_binding_baseline_abs_dl_tertile1: {"n": 26, "mean": 0.1782, "ci95": [0.09104116668663502, 0.2964924260866862]}
- cde_binding_baseline_abs_dl_tertile2: {"n": 26, "mean": 0.2119, "ci95": [0.12177587418401416, 0.3139458294877673]}
- cde_binding_baseline_abs_dl_tertile3: {"n": 28, "mean": 0.3033, "ci95": [0.22878996137662314, 0.3811104771838082]}
- behaviour_neither_rate: 0.307
- behaviour_neither_rate_strict: 0.449
- seconds_per_item: 60.321
- verdict_nll_mean_by_verdict: {"flip": 0.7368, "none": 0.8466, "own": 0.6023, "para": 0.7507, "para_flip": 0.8547}
- manipulation_check: {"donor": {"rows": 400, "with_stated_verdict": 400, "attributable_answers": 282, "answer_follows_stated_verdict": 0.7695035460992907, "answer_follows_stated_verdict_ci95": [0.7198581560283688, 0.8191489361702128]}, "free_binding": {"rows": 400, "with_stated_verdict": 313, "attributable_answers": 213, "answer_follows_stated_verdict": 0.9436619718309859, "answer_follows_stated_verdict_ci95": [0.9107981220657277, 0.971830985915493]}}
- relative_uncertainty_binding: {"n": 80, "balance_point": 0.1093, "slope": 0.9473, "inside": {"n": 33, "cde_mean": 0.23215054235517546, "cde_ci95": [0.15820310993461384, 0.3105592483857757]}, "outside": {"n": 47, "cde_mean": 0.23354215069735054, "cde_ci95": [0.16286582695647772, 0.3148638338825301]}}

## Qwen/Qwen2.5-VL-7B-Instruct | chartqa | dev

- Items: 2; analysed: 2; meets R5 minimum: False
- Boundary mismatches: 0 rows (0.000; gate ≤ 0.01)
- Ceil_ℓ: 0.956, 95% CI [0.269, 1.644]
  - image direction vs non-binding: 0.409, 95% CI [0.101, 0.718]
  - text direction vs non-binding: 0.547, 95% CI [0.168, 0.926]
- **T1** DiD = 0.061 (95% CI [0.005, 0.117]), sign-flip p = 0.2425, Holm-adjusted p = 0.4850: binding is not shown to strengthen the verdict's effect
- **T2** CDE = 0.233 (95% CI [0.005, 0.461]); ρ = 0.244, 90% CI [0.018, 0.281]; reading: **inconclusive**
- **T3** CDE = 0.172 (95% CI [-0.000, 0.344]); ρ = 0.180, 90% CI [-0.001, 0.210]; reading: **equivalent to no effect**
- Holm-adjusted p: {"T3": 0.0003, "T1": 0.485, "T2": 0.485}
- Behavioural, binding: Δ = 0.000, 90% CI [0.000, 0.000], TOST: equivalent; change rate own vs flip 0.000
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), churn rate 0.000 (limit 0.05), gate: **pass**; TOST power at this noise 1.00
- Behavioural, nonbinding: Δ = 0.000, 90% CI [0.000, 0.000], TOST: equivalent; change rate own vs flip 0.000
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), churn rate 0.000 (limit 0.05), gate: **pass**; TOST power at this noise 1.00
- **Combined reading under binding: inconclusive**
- **Combined reading under non-binding: H0: saying is not choosing**

Secondary:

- matched_pair_binding: {"n": 2, "mean": 0.2633, "ci95": [0.049280465881383906, 0.4772930043107408]}
- cde_binding_image_first: {"n": 2, "mean": 0.2833, "ci95": [-0.024907092672583453, 0.5914268237031137]}
- cde_binding_text_first: {"n": 2, "mean": 0.1828, "ci95": [0.03480958251602717, 0.33077946016728677]}
- matched_pair_nonbinding: {"n": 2, "mean": 0.2496, "ci95": [0.05100683437849504, 0.44824272342311816]}
- cde_nonbinding_image_first: {"n": 2, "mean": 0.1808, "ci95": [-0.031232367488882917, 0.39275732385685835]}
- cde_nonbinding_text_first: {"n": 2, "mean": 0.1636, "ci95": [0.030930466823338165, 0.29618444736934174]}
- cde_decomposition: {"binding_none_minus_own": {"n": 2, "mean": 0.06460290702784732, "ci95": [-0.06159640358437171, 0.19080221764006636]}, "binding_flip_minus_none": {"n": 2, "mean": 0.16842428640061374, "ci95": [0.06654764850609357, 0.2703009242951339]}, "nonbinding_none_minus_own": {"n": 2, "mean": -0.006718256279691533, "ci95": [-0.07141183636349518, 0.05797532380411212]}, "nonbinding_flip_minus_none": {"n": 2, "mean": 0.17887822391985536, "ci95": [0.07126088603072281, 0.28649556180898794]}}
- per_template: {"binding_k1": {"n": 2, "mean": 0.2397299558113446, "ci95": [0.014960302721738206, 0.464499608900951]}, "nonbinding_k1": {"n": 2, "mean": 0.1544031756913683, "ci95": [-0.0003201186093063635, 0.30912646999204296]}, "binding_k2": {"n": 2, "mean": 0.21994268082544294, "ci95": [0.0057719732169061455, 0.43411338843397973]}, "nonbinding_k2": {"n": 2, "mean": 0.1816304259584286, "ci95": [0.0013198675907917234, 0.3619409843260655]}, "binding_k3": {"n": 2, "mean": 0.21578718892069448, "ci95": [0.0020685249481176005, 0.42950585289327137]}, "nonbinding_k3": {"n": 2, "mean": 0.17763490143788654, "ci95": [-0.019937676664267268, 0.37520747954004036]}, "binding_k4": {"n": 2, "mean": 0.25664894815636224, "ci95": [-0.0029958211998745155, 0.516293717512599]}, "nonbinding_k4": {"n": 2, "mean": 0.17497136747297196, "ci95": [0.018334126351692404, 0.3316086085942515]}}
- loto: {"binding_excl_k1": {"n": 2, "mean": 0.2307929393008332, "ci95": [0.0016148923217164102, 0.45997098627995]}, "nonbinding_excl_k1": {"n": 2, "mean": 0.17807889828976234, "ci95": [-9.456090726104686e-05, 0.35625235748678574]}, "binding_excl_k2": {"n": 2, "mean": 0.2373886976294671, "ci95": [0.004677668823327097, 0.4700997264356071]}, "nonbinding_excl_k2": {"n": 2, "mean": 0.16900314820074228, "ci95": [-0.0006412229739604092, 0.33864751937544496]}, "binding_excl_k3": {"n": 2, "mean": 0.23877386159771663, "ci95": [0.0059121515795899455, 0.4716355716158433]}, "nonbinding_excl_k3": {"n": 2, "mean": 0.17033498970758962, "ci95": [0.0064446251110592545, 0.33422535430412]}, "binding_excl_k4": {"n": 2, "mean": 0.2251532751858273, "ci95": [0.007600266962253984, 0.44270628340940066]}, "nonbinding_excl_k4": {"n": 2, "mean": 0.17122283436256114, "ci95": [-0.006312642560927302, 0.34875831128604956]}}
- behaviour_neither_rate: 0.000
- behaviour_neither_rate_strict: 0.000
- chartqa_answer_only_match_share: 1.000
- seconds_per_item: 62.101
- verdict_nll_mean_by_verdict: {"flip": 0.5455, "none": 0.2965, "own": 0.3443, "para": 0.4501, "para_flip": 0.501}
- manipulation_check: {"donor": {"rows": 60, "with_stated_verdict": 60, "attributable_answers": 46, "answer_follows_stated_verdict": 0.5652173913043478, "answer_follows_stated_verdict_ci95": [0.43478260869565216, 0.717391304347826]}, "free_binding": {"rows": 60, "with_stated_verdict": 55, "attributable_answers": 47, "answer_follows_stated_verdict": 0.7659574468085106, "answer_follows_stated_verdict_ci95": [0.6382978723404256, 0.8723404255319149]}}
- relative_uncertainty_binding: {"n": 2, "balance_point": null, "note": "balance point not estimable"}

## Qwen/Qwen2.5-VL-7B-Instruct | math | dev

- Items: 115; analysed: 115; meets R5 minimum: False
- Boundary mismatches: 0 rows (0.000; gate ≤ 0.01)
- Ceil_ℓ: 1.423, 95% CI [1.214, 1.633]
  - image direction vs non-binding: 0.670, 95% CI [0.559, 0.790]
  - text direction vs non-binding: 0.753, 95% CI [0.609, 0.903]
- **T1** DiD = 0.277 (95% CI [0.220, 0.336]), sign-flip p = 0.0001, Holm-adjusted p = 0.0003: binding strengthens the verdict's effect
- **T2** CDE = 1.619 (95% CI [1.337, 1.919]); ρ = 1.138, 90% CI [1.022, 1.254]; reading: **decision-relevant**
- **T3** CDE = 1.342 (95% CI [1.082, 1.626]); ρ = 0.943, 90% CI [0.835, 1.052]; reading: **decision-relevant**
- Holm-adjusted p: {"T1": 0.0003, "T2": 0.0003, "T3": 0.0003}
- Behavioural, binding: Δ = 0.496, 90% CI [0.448, 0.543], TOST: not equivalent; change rate own vs flip 0.554
  - Wording floor (para vs own): signed mean 0.000 (limit ±0.05), churn rate 0.000 (limit 0.05), gate: **pass**; TOST power at this noise 0.78
- Behavioural, nonbinding: Δ = 0.326, 90% CI [0.278, 0.374], TOST: not equivalent; change rate own vs flip 0.372
  - Wording floor (para vs own): signed mean -0.052 (limit ±0.05), churn rate 0.065 (limit 0.05), gate: **FAIL**; TOST power at this noise 0.55
- **Combined reading under binding: H1: the verdict decides, and binding strengthens it**
- **Combined reading under non-binding: H1: the verdict decides; no evidence that binding strengthens it**

Secondary:

- matched_pair_binding: {"n": 115, "mean": 2.375, "ci95": [2.033441955420586, 2.732546330532927]}
- cde_binding_image_first: {"n": 115, "mean": 1.7509, "ci95": [1.3841809242581669, 2.137204451333219]}
- cde_binding_text_first: {"n": 115, "mean": 1.4867, "ci95": [1.1731038102437854, 1.8195071114424304]}
- matched_pair_nonbinding: {"n": 115, "mean": 1.9251, "ci95": [1.641051369082938, 2.224030478934048]}
- cde_nonbinding_image_first: {"n": 115, "mean": 1.365, "ci95": [1.0440137253978448, 1.702348495335532]}
- cde_nonbinding_text_first: {"n": 115, "mean": 1.3191, "ci95": [1.013898788323229, 1.642479217586405]}
- cde_decomposition: {"binding_none_minus_own": {"n": 115, "mean": 1.5154428798121606, "ci95": [1.249847774824832, 1.7996141738875484]}, "binding_flip_minus_none": {"n": 115, "mean": 0.10333670770482348, "ci95": [-0.08594057574733406, 0.2897866933752517]}, "nonbinding_none_minus_own": {"n": 115, "mean": 1.2579884856160557, "ci95": [1.0230506867743248, 1.5139731114987875]}, "nonbinding_flip_minus_none": {"n": 115, "mean": 0.08406788432929939, "ci95": [-0.09259764003626998, 0.2547524678562926]}}
- per_template: {"binding_k1": {"n": 115, "mean": 1.6149635601446894, "ci95": [1.327499330141171, 1.9167083476815172]}, "nonbinding_k1": {"n": 115, "mean": 1.2909104057549805, "ci95": [1.0318988283256403, 1.574427920593554]}, "binding_k2": {"n": 115, "mean": 1.6946331946277169, "ci95": [1.4000584297839866, 2.0069059924608137]}, "nonbinding_k2": {"n": 115, "mean": 1.375240819062464, "ci95": [1.1015824199174338, 1.6701892290583353]}, "binding_k3": {"n": 115, "mean": 1.5174354639573553, "ci95": [1.2515854531202262, 1.7997487249412123]}, "nonbinding_k3": {"n": 115, "mean": 1.2485301694129525, "ci95": [1.0143957012126432, 1.500247121491038]}, "binding_k4": {"n": 115, "mean": 1.6480861313381752, "ci95": [1.3527938543137734, 1.9572064173827213]}, "nonbinding_k4": {"n": 115, "mean": 1.4535440855510229, "ci95": [1.164868108872703, 1.770019568289509]}}
- loto: {"binding_excl_k1": {"n": 115, "mean": 1.6200515966410824, "ci95": [1.3384681917867987, 1.9176979069089957]}, "nonbinding_excl_k1": {"n": 115, "mean": 1.35910502467548, "ci95": [1.098809035343758, 1.6431957892491798]}, "binding_excl_k2": {"n": 115, "mean": 1.5934950518134066, "ci95": [1.3147408005924623, 1.8905032693213466]}, "nonbinding_excl_k2": {"n": 115, "mean": 1.3309948869063186, "ci95": [1.0747153642871972, 1.6107009175289309]}, "binding_excl_k3": {"n": 115, "mean": 1.6525609620368606, "ci95": [1.3618637594383791, 1.9591913850965104]}, "nonbinding_excl_k3": {"n": 115, "mean": 1.3732317701228225, "ci95": [1.1006712573653625, 1.6714666558969344]}, "binding_excl_k4": {"n": 115, "mean": 1.6090107395765871, "ci95": [1.3290655573014316, 1.905063637150498]}, "nonbinding_excl_k4": {"n": 115, "mean": 1.3048937980767992, "ci95": [1.0526023830352416, 1.579225620075808]}}
- cde_binding_baseline_abs_dl_tertile1: {"n": 38, "mean": 1.0615, "ci95": [0.74146720712344, 1.4254775938956694]}
- cde_binding_baseline_abs_dl_tertile2: {"n": 38, "mean": 1.3457, "ci95": [0.9252314767614614, 1.7869844095511094]}
- cde_binding_baseline_abs_dl_tertile3: {"n": 39, "mean": 2.4279, "ci95": [1.8542790312672128, 3.0594069707712284]}
- behaviour_neither_rate: 0.108
- behaviour_neither_rate_strict: 0.627
- seconds_per_item: 177.010
- verdict_nll_mean_by_verdict: {"flip": 0.6249, "none": 0.5239, "own": 0.5045, "para": 0.677, "para_flip": 0.7343}
- manipulation_check: {"donor": {"rows": 400, "with_stated_verdict": 396, "attributable_answers": 329, "answer_follows_stated_verdict": 0.9422492401215805, "answer_follows_stated_verdict_ci95": [0.9148936170212766, 0.9665653495440729]}, "free_binding": {"rows": 400, "with_stated_verdict": 392, "attributable_answers": 312, "answer_follows_stated_verdict": 0.9839743589743589, "answer_follows_stated_verdict_ci95": [0.967948717948718, 0.9967948717948718]}}
- relative_uncertainty_binding: {"n": 115, "balance_point": -0.0836, "slope": 0.8193, "inside": {"n": 34, "cde_mean": 1.0579809702078589, "cde_ci95": [0.6745365927289768, 1.506520941591932]}, "outside": {"n": 81, "cde_mean": 1.8541765379924195, "cde_ci95": [1.4955808269104087, 2.2403842535178176]}}

## Size comparison: Qwen2.5-VL-3B vs. Qwen2.5-VL-7B (secondary, descriptive)

### Regime: chartqa

- Common competent & gated items: N = 0
- **fewer than two items in intersection**

### Regime: math

- Common competent & gated items: N = 50
- ρ_bind (3B) on intersection: 1.369
- ρ_bind (7B) on intersection: 1.056
- Δρ (7B minus 3B): -0.314 (95% CI [-0.784, 0.050])

## Gate reports

- v5dev_chartqa_tp_qwen2.gates.json: {"items": 30, "competent": 10, "taken": 10, "no_donor": 0, "passed": 0, "jaccard_multiset_flip_min": null, "jaccard_multiset_flip_mean": null, "swaps_per_flip": {}, "own_source_by_order": {}, "fail_reasons_by_order": {"own_absent": 18, "own_undetermined": 2}}
- v5dev_chartqa_tp_qwen25.gates.json: {"items": 30, "competent": 13, "taken": 13, "no_donor": 0, "passed": 6, "jaccard_multiset_flip_min": 0.8667, "jaccard_multiset_flip_mean": 0.8936, "swaps_per_flip": {"1": 10, "2": 2}, "own_source_by_order": {"image_first:report": 6, "text_first:report": 6}, "fail_reasons_by_order": {"own_absent": 11}}
- v5dev_chartqa_tp_qwen25_7b.gates.json: {"items": 30, "competent": 13, "taken": 13, "no_donor": 0, "passed": 2, "jaccard_multiset_flip_min": 0.9481, "jaccard_multiset_flip_mean": 0.9774, "swaps_per_flip": {"1": 1, "2": 3}, "own_source_by_order": {"image_first:report": 2, "text_first:report": 2}, "fail_reasons_by_order": {"gate3_too_many_swaps": 8, "own_absent": 3, "own_wrong_regime": 1}}
- v5dev_conflict_tp_qwen2.gates.json: {"items": 200, "competent": 0, "taken": 0, "no_donor": 0, "passed": 0, "jaccard_multiset_flip_min": null, "jaccard_multiset_flip_mean": null, "swaps_per_flip": {}, "own_source_by_order": {}, "fail_reasons_by_order": {}}
- v5dev_conflict_tp_qwen25.gates.json: {"items": 200, "competent": 80, "taken": 80, "no_donor": 0, "passed": 80, "jaccard_multiset_flip_min": 0.88, "jaccard_multiset_flip_mean": 0.9455, "swaps_per_flip": {"1": 119, "2": 41}, "own_source_by_order": {"image_first:image": 32, "text_first:text": 79, "image_first:text": 48, "text_first:image": 1}, "fail_reasons_by_order": {}}
- v5dev_conflict_tp_qwen25_7b.gates.json: {"items": 200, "competent": 124, "taken": 124, "no_donor": 0, "passed": 115, "jaccard_multiset_flip_min": 0.875, "jaccard_multiset_flip_mean": 0.9549, "swaps_per_flip": {"1": 175, "2": 55}, "own_source_by_order": {"image_first:image": 71, "text_first:text": 115, "image_first:text": 44}, "fail_reasons_by_order": {"gate3_too_many_swaps": 8, "own_undetermined": 1}}

## Multi-model item intersections

- chartqa: intersection N = 0 across {'Qwen/Qwen2.5-VL-3B-Instruct': 6, 'Qwen/Qwen2.5-VL-7B-Instruct': 2}
- math: intersection N = 50 across {'Qwen/Qwen2.5-VL-3B-Instruct': 80, 'Qwen/Qwen2.5-VL-7B-Instruct': 115}

## Provenance

- Duplicate rows: 0
- v5dev_chartqa_tp_qwen25.manifest.json: {"resolved_model_commit": null, "peak_vram_gb": 6.993551731109619, "written_at": "2026-11-12T09:18:04", "n_items": 6}
- v5dev_chartqa_tp_qwen25_7b.manifest.json: {"resolved_model_commit": null, "peak_vram_gb": 15.696582794189453, "written_at": "2026-11-12T15:52:36", "n_items": 2}
- v5dev_conflict_tp_qwen25.manifest.json: {"resolved_model_commit": null, "peak_vram_gb": 6.993551731109619, "written_at": "2026-11-12T09:16:27", "n_items": 80}
- v5dev_conflict_tp_qwen25_7b.manifest.json: {"resolved_model_commit": null, "peak_vram_gb": 15.687393188476562, "written_at": "2026-11-12T15:42:37", "n_items": 115}
