# archive

Superseded code and early pilots. Nothing here is part of the active pipeline. Don't edit these files.

| Path | Contents |
|---|---|
| `harness_v3/production_experiment_harness_v3.py` | The harness behind `results_v3/`. Tests read its prompts to confirm that v4's `*_v3` arms are verbatim |
| `pilots_v1_v2/prefreeze_pilot.py`, `prefreeze_pilot_results.json` | First pilot, N = 20 |
| `pilots_v1_v2/prefreeze_pilot_v2.py`, `prefreeze_pilot_v2_results.json` | Second pilot, N = 20 |
| `pilots_v1_v2/prefreeze_pilot.ipynb` | Colab notebook for the pilots and the v3 run |
| `pilots_v1_v2/pilot_diagnostic_analysis.md` | AI-written diagnostic of the first pilot. Its "100% detection" claim comes from 20 items with no congruent control |

`production_experiment_harness.py` was removed on 2026-11-07. It was byte-identical to the v3 copy here, and it remains in git history.
