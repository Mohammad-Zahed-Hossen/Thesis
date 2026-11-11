#!/usr/bin/env python3
"""Tests for analyze_v5.py on synthetic transplant rows with known effects. No GPU.

Run from Experiment/:
    python -m unittest tests.test_analyze_v5 -v
"""
import csv
import json
import math
import os
import random
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import analyze_v5 as an
import harness_v5 as h5
import transplant_v5 as tp

FAMS = [("nonbinding", v) for v in tp.VERDICTS] + [("binding", v) for v in tp.VERDICTS] + [("explicit_image", "none"), ("explicit_text", "none")]


def synth(n=40, eff_bind=1.0, eff_non=0.2, ceil=2.0, own_image_every=0, noise=0.0, beh_follow=None, seed=0, regime="math", model_id="M"):
    """Rows where reversing the verdict moves Δℓ by eff toward the named source.

    own_image_every=m makes every m-th item's own verdict name the image, to test orientation.
    beh_follow(fam, ver) -> probability that the behavioural answer follows the named source.
    """
    rng = random.Random(seed)
    rows = []
    sides = ("image", "text") if regime == "math" else ("chart", "report")
    for i in range(n):
        own = sides[0] if own_image_every and i % own_image_every == 0 else sides[1]
        opp = sides[1] if own == sides[0] else sides[0]
        s = -1 if own == sides[0] else 1
        a, c = rng.uniform(-3, 3), rng.uniform(-3, 3)
        for fam, ver in FAMS:
            named = {"own": own, "flip": opp, "para": own, "para_flip": opp}.get(ver)
            for k in range(1, 5):
                for order in h5.ORDERS:
                    if fam.startswith("explicit"):
                        dl = c + (ceil / 2 if fam == "explicit_image" else -ceil / 2)
                    elif ver == "none":
                        dl = c
                    else:
                        eff = eff_bind if fam == "binding" else eff_non
                        dl = a + (s * eff if ver in ("flip", "para_flip") else 0.0)
                    dl += rng.gauss(0, noise) if noise else 0.0
                    base = dict(id=f"it{i}", model_id=model_id, regime=regime, phase="dev", family=fam, verdict=ver, k=k, order=order,
                                O=h5.ORDER_CODE[order], B=0.5 if fam == "binding" else -0.5 if fam == "nonbinding" else None,
                                own_source=own, named_source=named, y_image="11", y_text="22", wall_s=0.1)
                    rows.append({**base, "outcome": "dl", "dl": dl, "boundary_mismatch": False})
                    if k == 1:
                        p = beh_follow(fam, ver) if beh_follow else 0.5
                        follow = named is not None and rng.random() < p
                        target = an.side(named) if named else "image"
                        if not follow and named:
                            target = "text" if target == "image" else "image"
                        ans = "11" if target == "image" else "22"
                        rows.append({**base, "outcome": "beh", "full_text": f"working\n#### {ans}"})
    return rows


class TestHelpers(unittest.TestCase):
    def test_sign_flip_p_formula(self):
        r = an.sign_flip_test([1.0] * 20, 999, 1)
        self.assertEqual(r["p"], (1 + r["b"]) / 1000)
        self.assertLess(r["p"], 0.01)
        self.assertGreater(an.sign_flip_test([1.0, -1.0] * 10, 999, 1)["p"], 0.3)

    def test_holm(self):
        out = an.holm({"a": 0.01, "b": 0.04, "c": 0.03})
        self.assertAlmostEqual(out["a"], 0.03)
        self.assertAlmostEqual(out["c"], 0.06)
        self.assertAlmostEqual(out["b"], 0.06)

    def test_readings(self):
        self.assertTrue(an.rho_reading((-0.1, 0.5), None).startswith("undetermined"))
        self.assertEqual(an.rho_reading((1, 2), (0.3, 0.9)), "decision-relevant")
        self.assertEqual(an.rho_reading((1, 2), (-0.1, 0.2)), "equivalent to no effect")
        self.assertEqual(an.rho_reading((1, 2), (0.1, 0.4)), "inconclusive")
        self.assertEqual(an.tost_reading((-0.03, 0.04)), "equivalent")
        self.assertEqual(an.tost_reading((-0.03, 0.06)), "not equivalent")
        self.assertEqual(an.combined_reading("equivalent to no effect", "equivalent", True), "H0: saying is not choosing")
        self.assertEqual(an.combined_reading("equivalent to no effect", "not equivalent", True), "mixed")
        self.assertIn("uninterpretable", an.combined_reading("equivalent to no effect", "equivalent", False))

    def test_t1_qualifies_h1_but_never_decides_it(self):
        with_t1 = an.combined_reading("decision-relevant", "not equivalent", True, t1_significant=True)
        without = an.combined_reading("decision-relevant", "not equivalent", True, t1_significant=False)
        self.assertEqual(with_t1, "H1: the verdict decides, and binding strengthens it")
        self.assertEqual(without, "H1: the verdict decides; no evidence that binding strengthens it")
        # T1 alone gives no H1, and it does not change the other rows.
        self.assertEqual(an.combined_reading("inconclusive", "equivalent", True, t1_significant=True), "inconclusive")
        self.assertEqual(an.combined_reading("equivalent to no effect", "equivalent", True, t1_significant=True), "H0: saying is not choosing")
        self.assertEqual(an.combined_reading("undetermined: prompt-level control too weak", "equivalent", True, True), "undetermined")

    def test_tost_power(self):
        self.assertEqual(an.tost_power(0.0, 100), 1.0)
        self.assertEqual(an.tost_power(1.0, 1), 0.0)
        # sd² = 0.05 at n = 215 is the 5% row of the freeze audit's power table (0.90).
        self.assertAlmostEqual(an.tost_power(math.sqrt(0.05), 215), 0.90, delta=0.01)
        self.assertEqual(an.tost_power(math.sqrt(0.2), 215), 0.0)
        self.assertGreater(an.tost_power(0.1, 200), an.tost_power(0.2, 200))

    def test_wording_floor_catches_symmetric_churn(self):
        """20% of answers move one way and 20% the other: the signed mean is 0, the churn is 40%."""
        diffs = [1.0] * 20 + [-1.0] * 20 + [0.0] * 60
        f = an.wording_floor(diffs, churn=0.40)
        self.assertAlmostEqual(f["signed_mean"], 0.0)
        self.assertFalse(f["signed_mean_exceeds_epsilon"])
        self.assertTrue(f["churn_exceeds_max"])
        self.assertFalse(f["floor_ok"])
        self.assertTrue(f["power_below_target"])
        self.assertEqual(f["max_churn"], an.EPSILON)

    def test_wording_floor_passes_and_fails_on_each_half(self):
        quiet = an.wording_floor([0.0] * 97 + [1.0, -1.0, 1.0], churn=0.03)
        self.assertTrue(quiet["floor_ok"])
        shifted = an.wording_floor([1.0] * 10 + [0.0] * 90, churn=0.10)
        self.assertTrue(shifted["signed_mean_exceeds_epsilon"] and shifted["churn_exceeds_max"])
        self.assertFalse(shifted["floor_ok"])
        # At the limit itself the gate still passes: the rule is "exceeds".
        self.assertTrue(an.wording_floor([1.0] * 5 + [0.0] * 95, churn=0.05)["floor_ok"])

    def test_percentile(self):
        self.assertEqual(an.percentile([0, 10], 0.5), 5)
        self.assertEqual(an.percentile([1, 2, 3], 0.0), 1)


class TestAnalyzeGroup(unittest.TestCase):
    def test_known_effects(self):
        r = an.analyze_group(synth(eff_bind=1.0, eff_non=0.2, ceil=2.0), reps=300, draws=300)
        self.assertEqual(r["n_analysed"], 40)
        self.assertAlmostEqual(r["ceil"]["mean"], 2.0)
        self.assertAlmostEqual(r["T2_rho_binding"]["cde"], 1.0)
        self.assertAlmostEqual(r["T2_rho_binding"]["rho"], 0.5)
        self.assertAlmostEqual(r["T3_rho_nonbinding"]["rho"], 0.1)
        self.assertAlmostEqual(r["T1_did"]["mean"], 0.8)
        self.assertLess(r["T1_did"]["p"], 0.01)
        self.assertEqual(r["T2_rho_binding"]["reading"], "decision-relevant")
        self.assertEqual(r["T3_rho_nonbinding"]["reading"], "equivalent to no effect")
        self.assertTrue(r["T1_did"]["significant"])
        self.assertTrue(r["T1_did"]["significant_after_holm"])
        self.assertAlmostEqual(r["behaviour_binding"]["mean_abs_dl_gap_own_vs_flip"], 1.0)
        self.assertAlmostEqual(r["behaviour_binding"]["mean_abs_dl_gap_own_vs_para"], 0.0)
        self.assertEqual(r["reading_binding"], "H1: the verdict decides, and binding strengthens it")
        self.assertAlmostEqual(r["ceil_image_direction"]["mean"], 1.0)
        self.assertAlmostEqual(r["ceil_text_direction"]["mean"], 1.0)
        self.assertAlmostEqual(r["secondary"]["matched_pair_binding"]["mean"], 1.0)

    def test_orientation_with_image_own_verdicts(self):
        """Items whose own verdict names the image still count the effect as positive."""
        r = an.analyze_group(synth(eff_bind=1.0, eff_non=0.0, own_image_every=3), reps=200, draws=200)
        self.assertAlmostEqual(r["T2_rho_binding"]["cde"], 1.0)

    def test_h1_without_a_binding_effect(self):
        """The verdict moves the answer equally with and without binding: H1, but T1 is not significant."""
        r = an.analyze_group(synth(eff_bind=1.0, eff_non=1.0, noise=0.05, seed=5), reps=300, draws=300)
        self.assertEqual(r["T2_rho_binding"]["reading"], "decision-relevant")
        self.assertFalse(r["T1_did"]["significant"])
        self.assertEqual(r["reading_binding"], "H1: the verdict decides; no evidence that binding strengthens it")

    def test_null_effect_and_h0(self):
        """The answer always stays with the own source, whatever the verdict says."""
        ignore = lambda fam, ver: 1.0 if ver in ("own", "para") else 0.0
        r = an.analyze_group(synth(n=200, eff_bind=0.0, eff_non=0.0, noise=0.05, beh_follow=ignore, seed=3), reps=400, draws=400)
        self.assertEqual(r["T2_rho_binding"]["reading"], "equivalent to no effect")
        self.assertGreater(r["T1_did"]["p"], 0.05)
        floor = r["behaviour_binding"]["wording_floor_para_minus_own"]
        self.assertEqual((floor["churn_rate"], floor["floor_ok"]), (0.0, True))
        self.assertEqual(r["reading_binding"], "H0: saying is not choosing")

    def test_symmetric_churn_blocks_h0(self):
        """Random answers: the signed wording shift is near 0, but half the answers change."""
        r = an.analyze_group(synth(n=200, eff_bind=0.0, eff_non=0.0, noise=0.05, beh_follow=lambda fam, ver: 0.5, seed=3), reps=400, draws=400)
        floor = r["behaviour_binding"]["wording_floor_para_minus_own"]
        self.assertLess(abs(floor["signed_mean"]), an.EPSILON)
        self.assertFalse(floor["signed_mean_exceeds_epsilon"])
        self.assertGreater(floor["churn_rate"], 0.3)
        self.assertTrue(floor["churn_exceeds_max"])
        self.assertFalse(r["wording_floor_ok_binding"])
        self.assertIn("uninterpretable", r["reading_binding"])

    def test_undetermined_without_ceiling(self):
        r = an.analyze_group(synth(ceil=0.0, noise=0.5), reps=200, draws=200)
        self.assertTrue(r["T2_rho_binding"]["reading"].startswith("undetermined"))
        self.assertNotIn("rho", r["T2_rho_binding"])

    def test_boundary_mismatch_rows_dropped(self):
        rows = synth()
        bad = next(x for x in rows if x["outcome"] == "dl")
        bad["boundary_mismatch"] = True
        r = an.analyze_group(rows, reps=100, draws=100)
        self.assertEqual(r["boundary_mismatch_rows"], 1)

    def test_behavioural_delta_when_verdict_is_ignored(self):
        """The answer stays with the own source under both verdicts: the effect is 0, not -1."""
        follow = lambda fam, ver: 1.0 if ver == "own" else 0.0 if ver == "flip" else 1.0
        r = an.analyze_group(synth(beh_follow=follow), reps=200, draws=200)
        d = r["behaviour_binding"]["delta_flip_minus_own"]
        self.assertAlmostEqual(d["mean"], 0.0)
        self.assertEqual(d["reading"], "equivalent")
        self.assertAlmostEqual(r["behaviour_binding"]["wording_floor_para_minus_own"]["mean"], 0.0)

    def test_behavioural_delta_when_verdict_is_followed(self):
        """The answer follows whichever source the verdict names: the effect is +1."""
        r = an.analyze_group(synth(beh_follow=lambda fam, ver: 1.0), reps=200, draws=200)
        d = r["behaviour_binding"]["delta_flip_minus_own"]
        self.assertAlmostEqual(d["mean"], 1.0)
        self.assertEqual(d["reading"], "not equivalent")
        self.assertAlmostEqual(r["behaviour_binding"]["change_rate_own_vs_flip"], 1.0)

    def test_min_items_rule(self):
        self.assertFalse(an.analyze_group(synth(n=20), reps=50, draws=50)["meets_min_items"])
        self.assertTrue(an.analyze_group(synth(n=100, regime="chartqa"), reps=50, draws=50)["meets_min_items"])


class TestBaseAndDonorAnalyses(unittest.TestCase):
    def donor_row(self, fam, verdict_source, answer, i=0):
        text = f"The image and the typed text do not agree. I consider {verdict_source} more reliable.\n\nTo solve the problem, compute.\n\n#### {answer}"
        return dict(id=f"it{i}", model_id="M", regime="math", family=fam, order="image_first", y_image="11", y_text="22", full_text=text)

    def test_manipulation_check(self):
        rows = [self.donor_row("free_binding", "the typed text", "22", i) for i in range(3)]
        rows += [self.donor_row("free_binding", "the image", "22", 3)]  # says image, solves text
        rows += [self.donor_row("donor", "the typed text", "11", 4), self.donor_row("donor", "the typed text", "99", 5)]
        out = an.manipulation_check(rows)
        self.assertEqual(out["free_binding"]["rows"], 4)
        self.assertAlmostEqual(out["free_binding"]["answer_follows_stated_verdict"], 0.75)
        self.assertEqual(out["donor"]["with_stated_verdict"], 2)
        self.assertEqual(out["donor"]["attributable_answers"], 1)  # "99" matches neither answer
        self.assertAlmostEqual(out["donor"]["answer_follows_stated_verdict"], 0.0)

    def test_relative_uncertainty(self):
        rows = [
            dict(id="a", outcome="nll", family="base_image", lp_image=-2.0, n_image=2, lp_text=-9.0, n_text=1),
            dict(id="a", outcome="nll", family="base_text", lp_image=-9.0, n_image=1, lp_text=-3.0, n_text=1),
            dict(id="b", outcome="nll", family="base_image", lp_image=-1.0, n_image=1, lp_text=0.0, n_text=1),
            dict(id="c", outcome="beh", family="base_image", full_text="#### 1"),
        ]
        dh = an.relative_uncertainty(rows)
        self.assertEqual(set(dh), {"a"})  # b lacks its text row; c is a generation row
        self.assertAlmostEqual(dh["a"], 2 * (3.0 - 1.0) / (3.0 + 1.0))

    def test_logistic_and_balance_point(self):
        rng = random.Random(0)
        xs = [rng.uniform(-2, 2) for _ in range(400)]
        ys = [int(rng.random() < 1 / (1 + math.exp(-(2.0 * (x - 0.5))))) for x in xs]
        b0, b1 = an.logistic_1d(xs, ys)
        self.assertAlmostEqual(-b0 / b1, 0.5, delta=0.2)
        self.assertIsNone(an.logistic_1d([1, 2, 3], [1, 1, 1]))
        ids = [f"i{j}" for j in range(400)]
        dh = dict(zip(ids, xs))
        baseline = {i: (1.0 if y else -1.0) for i, y in zip(ids, ys)}
        cde = {i: (1.0 if abs(dh[i] - 0.5) <= 0.5 else 0.0) for i in ids}
        out = an.uncertainty_strata(dh, baseline, cde)
        self.assertGreater(out["inside"]["cde_mean"], out["outside"]["cde_mean"])
        self.assertEqual(an.uncertainty_strata({"a": 1.0}, {"a": 1.0}, {"a": 1.0})["balance_point"], None)

    def test_group_uses_base_and_donor_files(self):
        rows = synth(n=12)
        base = []
        for i in range(12):
            base += [
                dict(id=f"it{i}", model_id="M", regime="math", outcome="nll", family="base_image", lp_image=-1.0 - i / 10, n_image=1, lp_text=-1.0, n_text=1),
                dict(id=f"it{i}", model_id="M", regime="math", outcome="nll", family="base_text", lp_image=-1.0, n_image=1, lp_text=-2.0 + i / 10, n_text=1),
            ]
        donors = [self.donor_row("free_binding", "the typed text", "22", i) for i in range(12)]
        r = an.analyze_group(rows, reps=50, draws=50, base_rows=base, donor_rows=donors)
        self.assertEqual(r["secondary"]["manipulation_check"]["free_binding"]["answer_follows_stated_verdict"], 1.0)
        self.assertEqual(r["secondary"]["relative_uncertainty_binding"]["n"], 12)

    def test_size_comparison_3b_vs_7b(self):
        r3 = synth(n=20, eff_bind=0.8, ceil=2.0, noise=0.1, model_id=an.MODEL_3B, seed=1)
        r7 = synth(n=20, eff_bind=1.6, ceil=2.0, noise=0.1, model_id=an.MODEL_7B, seed=2)
        sc = an.analyze_size_comparison(r3, r7, reps=100, seed=42)
        self.assertEqual(sc["n_intersection"], 20)
        self.assertAlmostEqual(sc["rho_3b_on_intersection"], 0.4, places=1)
        self.assertAlmostEqual(sc["rho_7b_on_intersection"], 0.8, places=1)
        self.assertAlmostEqual(sc["delta_rho_7b_minus_3b"], 0.4, places=1)
        self.assertEqual(len(sc["delta_rho_ci95"]), 2)
        self.assertLess(sc["delta_rho_ci95"][0], sc["delta_rho_ci95"][1])
        self.assertLessEqual(sc["delta_rho_ci95"][0], sc["delta_rho_7b_minus_3b"])
        self.assertGreaterEqual(sc["delta_rho_ci95"][1], sc["delta_rho_7b_minus_3b"])


class TestOutputs(unittest.TestCase):
    def test_csv_and_main(self):
        rows = synth(n=10)
        with tempfile.TemporaryDirectory() as d:
            run = os.path.join(d, "tp.jsonl")
            with open(run, "w", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")
            out = os.path.join(d, "out")
            sys.argv = ["analyze_v5.py", "--runs", run, "--output_dir", out, "--reps", "50", "--draws", "50"]
            self.assertEqual(an.main(), 0)
            with open(os.path.join(out, "long_v5.csv"), encoding="utf-8") as f:
                data = list(csv.DictReader(f))
            self.assertEqual(len(data), 10 * 2 * 2 * 2 * (4 + 1))  # items x families x {own, flip} x orders x (4 dl + 1 beh)
            self.assertEqual({x["D"] for x in data}, {"0.5", "-0.5"})
            self.assertTrue(os.path.exists(os.path.join(out, "analyze_v5_lme4.R")))
            with open(os.path.join(out, "analysis_v5.md"), encoding="utf-8") as f:
                self.assertIn("Dev data", f.read())

    def test_main_size_comparison(self):
        r3 = synth(n=10, eff_bind=0.8, ceil=2.0, model_id=an.MODEL_3B, seed=1)
        r7 = synth(n=10, eff_bind=1.6, ceil=2.0, model_id=an.MODEL_7B, seed=2)
        with tempfile.TemporaryDirectory() as d:
            run3 = os.path.join(d, "tp3.jsonl")
            run7 = os.path.join(d, "tp7.jsonl")
            with open(run3, "w", encoding="utf-8") as f:
                for r in r3:
                    f.write(json.dumps(r) + "\n")
            with open(run7, "w", encoding="utf-8") as f:
                for r in r7:
                    f.write(json.dumps(r) + "\n")
            out = os.path.join(d, "out")
            sys.argv = ["analyze_v5.py", "--runs", run3, run7, "--output_dir", out, "--reps", "50", "--draws", "50"]
            self.assertEqual(an.main(), 0)
            with open(os.path.join(out, "analysis_v5.json"), encoding="utf-8") as f:
                res = json.load(f)
            self.assertEqual(len(res["size_comparisons"]), 1)
            self.assertEqual(res["size_comparisons"][0]["n_intersection"], 10)
            with open(os.path.join(out, "analysis_v5.md"), encoding="utf-8") as f:
                text = f.read()
            self.assertIn("## Size comparison: Qwen2.5-VL-3B vs. Qwen2.5-VL-7B", text)
            self.assertIn("Δρ (7B minus 3B)", text)


if __name__ == "__main__":
    unittest.main()
