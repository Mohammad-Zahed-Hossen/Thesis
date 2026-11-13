#!/usr/bin/env python3
"""Regression tests for v5 CPU-only code, scorer, transplant, and analysis fixes."""
import csv
import json
import os
import sys
import tempfile
import unittest
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
sys.path.insert(0, EXPERIMENT)

import analyze_v5 as an
import harness_v4 as h4
import harness_v5 as h5
import score_v4 as v4
import score_v5 as sc
import transplant_v5 as tp
from tests.test_analyze_v5 import synth


class TestSplitterAndScorerFixes(unittest.TestCase):
    def test_split_verbalization_preserves_us_uk_and_pivots_on_hash(self):
        text = "The chart covers U.S. poverty rates. The report disagrees. I consider the chart more reliable.\n#### 14.8"
        verb, solve = v4.split_verbalization(text)
        self.assertIn("I consider the chart more reliable.", verb)
        self.assertTrue(solve.startswith("#### 14.8"))
        self.assertEqual(verb + solve, text)

        text_uk = "In the U.K. data, the image shows 10. I consider the image more reliable. #### 10"
        v_uk, s_uk = v4.split_verbalization(text_uk)
        self.assertIn("I consider the image more reliable.", v_uk)
        self.assertTrue(s_uk.startswith("#### 10"))

    def test_regime_aware_stated_reliable_source(self):
        s = "The chart provides visual evidence, so the chart is more reliable."
        self.assertEqual(sc.stated_reliable_source(s, regime="chartqa"), "chart")
        s_visual_first = "The visual details are clear, and the report is more reliable."
        self.assertEqual(sc.stated_reliable_source(s_visual_first, regime="chartqa"), "report")

    def test_comparative_negation_returns_undetermined(self):
        for s in (
            "The typed text is less reliable than the image.",
            "The image is not reliable.",
            "The typed text is unreliable.",
            "The chart is not as reliable as the report.",
        ):
            self.assertEqual(sc.stated_reliable_source(s), "undetermined", s)

    def test_math_behavioural_fallback_rescues_structured_final_answer(self):
        text = "175 + 140 + 280 = 595 gems.\n\nThe final answer is 595."
        self.assertEqual(sc.behavioural_source(text, "math", "595", "100", allow_math_fallback=False)[0], "neither")
        src, ans, method = sc.behavioural_source(text, "math", "595", "100", allow_math_fallback=True)
        self.assertEqual((src, ans, method), ("image", "595", "structured_final_answer"))


class TestTransplantAndManifestFixes(unittest.TestCase):
    def test_swap_includes_visual_and_written(self):
        out, _ = tp.swap_sources("The visual is more reliable than the written.", "math")
        self.assertEqual(out, "The typed text is more reliable than the image.")

    def test_answer_leakage_gate_rejects_leaked_m_none(self):
        leaked = "The chart shows 14.8% while the report shows 11.8%. I consider the chart more reliable."
        v = tp.make_variants(leaked, "chartqa", y_image="14.8", y_text="11.8")
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "gate_answer_leakage")

        clean = "The chart and the report show different values for 2019. I consider the chart more reliable."
        v_ok = tp.make_variants(clean, "chartqa", y_image="14.8", y_text="11.8")
        self.assertTrue(v_ok.ok)

    def test_manifest_not_overwritten_when_force_write_false(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "run.manifest.json")
            script = os.path.abspath(__file__)
            cfg = h5.V5Config(run_tag="t", stage="base", model_id="Qwen/Qwen2.5-VL-3B-Instruct")
            b1 = SimpleNamespace(info=lambda: {"peak_vram_gb": 15.45, "resolved_model_commit": "abc"})
            h4.write_manifest(p, cfg, b1, 10, [script], force_write=True)
            b2 = SimpleNamespace(info=lambda: {"peak_vram_gb": 2.0, "resolved_model_commit": "abc"})
            h4.write_manifest(p, cfg, b2, 10, [script], force_write=False)
            with open(p, encoding="utf-8") as f:
                saved = json.load(f)
            self.assertEqual(saved["environment"]["peak_vram_gb"], 15.45)


class TestAnalyzeV5Fixes(unittest.TestCase):
    def test_holm_has_three_primary_tests_and_new_outputs(self):
        rows = synth(eff_bind=1.0, eff_non=0.2, ceil=2.0)
        for r in rows:
            if r["outcome"] == "dl":
                r["verdict_nll"] = 0.42
        res = an.analyze_group(rows, reps=200, draws=200)
        self.assertEqual(set(res["holm_adjusted"].keys()), {"T1", "T2", "T3"})
        self.assertIn("reading_nonbinding", res)
        self.assertIn("cde_decomposition", res["secondary"])
        self.assertIn("binding_none_minus_own", res["secondary"]["cde_decomposition"])
        self.assertIn("binding_flip_minus_none", res["secondary"]["cde_decomposition"])
        self.assertIn("per_template", res["secondary"])
        self.assertIn("loto", res["secondary"])
        self.assertIn("ci95", res["secondary"]["cde_binding_baseline_abs_dl_tertile1"])

        with tempfile.TemporaryDirectory() as d:
            csv_path = os.path.join(d, "long.csv")
            an.export_long(rows, csv_path)
            with open(csv_path, encoding="utf-8") as f:
                header = next(csv.reader(f))
            self.assertIn("verdict_nll", header)

    def test_change_rate_ignores_neither_transitions(self):
        beh = {
            ("it1", "binding", "own", "image_first"): {"src": "image", "image": 1},
            ("it1", "binding", "flip", "image_first"): {"src": "neither", "image": None},
            ("it2", "binding", "own", "image_first"): {"src": "image", "image": 1},
            ("it2", "binding", "flip", "image_first"): {"src": "image", "image": 1},
        }
        self.assertAlmostEqual(an.change_rate(beh, ["it1", "it2"], "binding", "own", "flip"), 0.0)
        self.assertAlmostEqual(an.neither_transition_rate(beh, ["it1", "it2"], "binding", "own", "flip"), 0.5)


if __name__ == "__main__":
    unittest.main()
