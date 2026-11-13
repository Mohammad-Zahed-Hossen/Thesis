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


class TestSecondBatchFixes(unittest.TestCase):
    """Fixes from Thesis/docs/Archive/claude_v5_forensic_code_and_construct_audit.md: H3, L2, M2, M4, M3."""

    # H3: the two-sentence fallback must not cut off a reliability verdict that follows.
    def test_split_keeps_third_sentence_verdict(self):
        text = (
            "The problem in the image and the typed text are not the same. "
            "The image asks about elves, while the typed text asks about expenses. "
            "Therefore, the typed text is considered more reliable."
        )
        verb, solve = v4.split_verbalization(text)
        self.assertEqual(verb, text)
        self.assertEqual(solve, "")
        self.assertEqual(sc.stated_reliable_source(verb, regime="math"), "text")

    def test_split_extension_stops_at_the_verdict_and_preserves_text(self):
        text = "They differ. The image is about ducks. I consider the image more reliable. The image shows 3 ducks and 4 more arrive. That makes 7."
        verb, solve = v4.split_verbalization(text)
        self.assertTrue(verb.endswith("I consider the image more reliable."))
        self.assertTrue(solve.startswith(" The image shows 3 ducks"))
        self.assertEqual(verb + solve, text)

    def test_split_without_a_verdict_still_takes_two_sentences(self):
        text = "They differ. The image is about ducks. There are 3 ducks. Then 4 more arrive. That makes 7."
        verb, solve = v4.split_verbalization(text)
        self.assertEqual(verb, "They differ. The image is about ducks.")
        self.assertEqual(verb + solve, text)

    def test_split_does_not_reach_past_the_fifth_sentence(self):
        text = "One. Two. Three. Four. Five. The image is more reliable."
        verb, _ = v4.split_verbalization(text)
        self.assertEqual(verb, "One. Two.")

    def test_split_with_a_solving_cue_is_unchanged(self):
        text = "They differ. I consider the typed text more reliable.\n\nTo solve the problem: 2 + 2 = 4.\n\n#### 4"
        verb, solve = v4.split_verbalization(text)
        self.assertEqual(verb, "They differ. I consider the typed text more reliable.")
        self.assertEqual(verb + solve, text)

    # L2: a period inside a number or "U.S." must not cut the reliability sentence.
    def test_reliability_sentence_survives_decimals_and_abbreviations(self):
        s = "The chart shows 14.8% for the U.S. in 2019 and is more reliable than the report."
        self.assertEqual(sc.reliability_sentence("They disagree. " + s).strip(), s)
        # The old pattern kept only the text after the last inner period, which lost "chart".
        self.assertEqual(sc.stated_reliable_source("They disagree. " + s, regime="chartqa"), "chart")
        self.assertNotIn("chart", sc._REL_SENT.search(s).group(0).split("reliable")[0])

    def test_reliability_sentence_respects_lines_and_absence(self):
        self.assertIsNone(sc.reliability_sentence("They differ. I will solve the text."))
        self.assertEqual(sc.stated_reliable_source("They differ. I will solve the text."), "absent")
        two_lines = "The image is clear\nThe typed text is more reliable"
        self.assertEqual(sc.stated_reliable_source(two_lines, regime="math"), "text")

    # M2: flips change the verdict clause only.
    def test_clause_scope_leaves_the_justification_alone(self):
        own = "The report is more reliable as it provides the exact response shares in the pie chart."
        out, _ = tp.swap_sources(own, "chartqa", scope="clause")
        self.assertEqual(out, "The chart is more reliable as it provides the exact response shares in the pie chart.")
        self.assertEqual(tp.count_swaps(own, "chartqa", scope="clause"), 1)
        self.assertEqual(tp.nouns_outside_scope(own, "chartqa", scope="clause"), 1)
        self.assertEqual(tp.nouns_outside_scope(own, "chartqa", scope="sentence"), 0)
        sentence_wide, _ = tp.swap_sources(own, "chartqa")  # the default scope is the dev-pass one
        self.assertEqual(tp.SWAP_SCOPE, "sentence")
        self.assertIn("pie report", sentence_wide)

    def test_clause_scope_swaps_both_sides_of_a_comparison(self):
        out, _ = tp.swap_sources("The text is more reliable than the image because the image is blurry.", "math", scope="clause")
        self.assertEqual(out, "The image is more reliable than the typed text because the image is blurry.")

    def test_clause_grows_to_reach_the_source_noun(self):
        left = "The chart, being a summary of the data, is considered more reliable."
        self.assertEqual(tp.swap_sources(left, "chartqa", scope="clause")[0], "The report, being a summary of the data, is considered more reliable.")
        template = "I would treat the image as more reliable."
        self.assertEqual(tp.swap_sources(template, "math", scope="clause")[0], "I would treat the typed text as more reliable.")
        right = "The more reliable source, as far as I can tell, is the chart."
        self.assertEqual(tp.swap_sources(right, "chartqa", scope="clause")[0], "The more reliable source, as far as I can tell, is the report.")

    def test_clause_scope_passes_what_sentence_scope_rejected(self):
        v = "They differ. Given that the chart is a picture and the report is a summary, the report is considered more reliable."
        self.assertEqual(tp.make_variants(v, "chartqa").reason, "gate3_too_many_swaps")
        tp.SWAP_SCOPE = "clause"
        try:
            clause = tp.make_variants(v, "chartqa")
        finally:
            tp.SWAP_SCOPE = "sentence"
        self.assertTrue(clause.ok, clause.reason)
        self.assertEqual(clause.n_swaps, 1)
        self.assertTrue(clause.texts["flip"].endswith("the chart is considered more reliable."))
        self.assertIn("Given that the chart is a picture and the report is a summary", clause.texts["flip"])

    # M4: verdict_nll covers the verdict sentence only.
    def test_variants_record_the_verdict_sentence_span(self):
        v = tp.make_variants("They differ. I consider the typed text more reliable as it is clear.", "math")
        for name in ("own", "flip", "para", "para_flip"):
            a, b = v.verdict_chars[name]
            sentence = v.texts[name][a:b]
            self.assertIn("reliable", sentence)
            self.assertNotIn("They differ", sentence)
            self.assertFalse(sentence.startswith(" "))
        self.assertNotIn("none", v.verdict_chars)

    def test_score_requests_carry_the_span_only_when_there_is_a_verdict(self):
        item = h5.Item(id="i", source="gsm8k", image=None, image_question="q", text_question="t", y_image="1", y_text="2", image_only_question="")
        var = tp.make_variants("They differ. I consider the typed text more reliable.", "math")
        reqs = tp.build_cells(item, "math", {o: var for o in h5.ORDERS}, [1])
        for r in reqs:
            if r.mode != "score":
                self.assertIsNone(r.verdict_chars)
            elif r.cell["verdict"] == "none":
                self.assertIsNone(r.verdict_chars, r.key)  # includes both explicit arms
            else:
                a, b = r.verdict_chars
                self.assertIn("reliable", r.prefill[a:b])
                self.assertNotIn("####", r.prefill[a:b])

    def test_verdict_token_span(self):
        prefix = [1, 2, 3, 4, 5, 6, 7, 8]  # chat 1-2 | sentence one 3-4 | verdict 5-6 | "\n\n####" 7-8
        self.assertEqual(sc.verdict_token_span(prefix, [1, 2, 3, 4], [1, 2, 3, 4, 5, 6]), (4, 6, True))
        # The verdict's last token merged with what follows: that token is left out.
        self.assertEqual(sc.verdict_token_span(prefix, [1, 2, 3, 4], [1, 2, 3, 4, 5, 99]), (4, 5, False))
        # The token before the verdict straddles the boundary: it is left out too.
        self.assertEqual(sc.verdict_token_span(prefix, [1, 2, 3, 99], [1, 2, 3, 4, 5, 6]), (4, 6, False))
        self.assertIsNone(sc.verdict_token_span(prefix, [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]))

    # Parsers and analysis outputs.
    def test_negation_in_a_later_clause_does_not_cancel_the_verdict(self):
        s = "I consider the typed text more reliable as it is clear, while the image could be less reliable."
        self.assertEqual(sc.stated_reliable_source(s, regime="math"), "text")
        self.assertEqual(sc.stated_reliable_source("The image is not very reliable.", regime="math"), "undetermined")
        self.assertEqual(sc.stated_reliable_source("The report is no more reliable than the chart.", regime="chartqa"), "undetermined")

    def test_three_math_parsers(self):
        hashed = "2 + 2 = 4\n\n#### 4"
        stated = "2 + 2 = 4.\n\nThe final answer is 4."
        bare = "So she has 2 + 2 = 4 apples."
        expect = {"strict": ("image", "neither", "neither"), "structured": ("image", "image", "neither"), "lenient": ("image", "image", "image")}
        for parser, want in expect.items():
            got = tuple(sc.behavioural_source(t, "math", "4", "9", parser=parser)[0] for t in (hashed, stated, bare))
            self.assertEqual(got, want, parser)
        with self.assertRaises(ValueError):
            sc.behavioural_source(hashed, "math", "4", "9", parser="loose")

    def test_auc(self):
        self.assertEqual(an.auc([3, 4], [1, 2]), 1.0)
        self.assertEqual(an.auc([1, 2], [3, 4]), 0.0)
        self.assertEqual(an.auc([1, 1], [1, 1]), 0.5)
        self.assertIsNone(an.auc([], [1]))

    def test_validity_diagnostics(self):
        def row(i, order, outcome, dl=None, text=None):
            r = {"id": i, "family": "binding", "verdict": "own", "k": 1, "order": order, "outcome": outcome, "regime": "math", "y_image": "4", "y_text": "9"}
            return {**r, "dl": dl} if outcome == "dl" else {**r, "full_text": text}

        rows = []
        for i, (dl, ans) in enumerate([(2.0, "4"), (1.0, "9"), (-1.0, "9"), (-2.0, "9")]):
            rows += [row(str(i), "image_first", "dl", dl=dl), row(str(i), "image_first", "beh", text=f"#### {ans}")]
        rows += [row("x", "image_first", "dl", dl=5.0), row("x", "image_first", "beh", text="no answer here")]
        d = an.validity_diagnostics(rows, "strict")
        self.assertEqual((d["n_attributable"], d["n_behavioural_rows"]), (4, 5))
        self.assertAlmostEqual(d["sign_agreement"], 0.75)
        self.assertAlmostEqual(d["majority_baseline"], 0.75)
        self.assertEqual(d["auc_image_first"], 1.0)
        self.assertIsNone(d["auc_text_first"])

    def test_any_change_counts_neither_and_flip_rate_does_not(self):
        beh = {
            ("a", "binding", "own", "image_first"): {"src": "image"},
            ("a", "binding", "para", "image_first"): {"src": "neither"},
            ("b", "binding", "own", "image_first"): {"src": "image"},
            ("b", "binding", "para", "image_first"): {"src": "text"},
            ("c", "binding", "own", "image_first"): {"src": "text"},
            ("c", "binding", "para", "image_first"): {"src": "text"},
        }
        ids = ["a", "b", "c"]
        self.assertAlmostEqual(an.any_change_rate(beh, ids, "binding", "own", "para"), 2 / 3)
        self.assertAlmostEqual(an.change_rate(beh, ids, "binding", "own", "para"), 0.5)
        self.assertEqual(an.attributable_pairs(beh, ids, "binding", "own", "para"), 2)

    def test_readings_are_qualified_below_the_minimum(self):
        rows = synth(eff_bind=1.0, eff_non=0.2, ceil=2.0)
        res = an.analyze_group(rows, reps=200, draws=200)
        self.assertFalse(res["meets_min_items"])
        self.assertTrue(res["reading_binding_reported"].startswith("NOT A READING"))
        self.assertIn(res["reading_binding"], res["reading_binding_reported"])
        self.assertTrue(res["reading_nonbinding_reported"].startswith("NOT A READING"))
        self.assertIn("behaviour_by_parser", res)
        self.assertEqual(set(res["behaviour_by_parser"]), set(sc.MATH_PARSERS))
        self.assertEqual(set(res["validity_dl_vs_behaviour"]), set(sc.MATH_PARSERS))
        rendered = an.render([res], {})
        self.assertIn("NOT A READING", rendered)
        self.assertIn("| strict |", rendered)

    def test_qualify_reading(self):
        self.assertEqual(an.qualify_reading("H1", 200, 150, True), ("H1", []))
        text, caveats = an.qualify_reading("H1", 6, 100, False)
        self.assertTrue(text.startswith("NOT A READING"))
        self.assertEqual(len(caveats), 2)

    def test_holm_enters_each_interval_test_with_a_doubled_p(self):
        rows = synth(eff_bind=1.0, eff_non=0.2, ceil=2.0)
        res = an.analyze_group(rows, reps=200, draws=200)
        e = res["T2_rho_binding"]
        entered = min(1.0, 2 * min(e["p_decision_relevant"], e["p_equivalent"]))
        self.assertGreaterEqual(res["holm_adjusted"]["T2"], entered - 1e-12)

    def test_fake_backend_runs_are_refused(self):
        with tempfile.TemporaryDirectory() as d:
            run = os.path.join(d, "x.jsonl")
            with open(run, "w", encoding="utf-8") as f:
                for r in synth(eff_bind=1.0, eff_non=0.2, ceil=2.0):
                    f.write(json.dumps(r) + "\n")
            with open(os.path.join(d, "x.manifest.json"), "w", encoding="utf-8") as f:
                json.dump({"environment": {"backend": "echo"}}, f)
            self.assertEqual(an.fake_backend_runs([run]), [run])
            argv = sys.argv
            try:
                sys.argv = ["analyze_v5.py", "--runs", run, "--output_dir", os.path.join(d, "out"), "--reps", "50", "--draws", "50"]
                self.assertEqual(an.main(), 2)
                self.assertFalse(os.path.exists(os.path.join(d, "out")))
                sys.argv += ["--allow_dry_run"]
                self.assertEqual(an.main(), 0)
            finally:
                sys.argv = argv

    def test_base_correct_uses_structured_parser_by_default(self):
        stated = {"regime": "math", "family": "base_image", "y_image": "18", "y_text": "9", "full_text": "Work: 9*2=18.\n\nThe final answer is 18."}
        bare = {**stated, "full_text": "it is 18"}
        self.assertTrue(h5.base_correct(stated))
        self.assertFalse(h5.base_correct(stated, parser="strict"))
        self.assertFalse(h5.base_correct(bare))

    def test_d1_to_d5_pre_freeze_fields_and_additivity(self):
        self.assertEqual(an.HEADLINE_PARSER, "structured")
        self.assertEqual(an.confirmatory_role("Qwen/Qwen2-VL-2B-Instruct", "math"), "diagnostic_only")
        self.assertEqual(an.confirmatory_role("Qwen/Qwen2.5-VL-7B-Instruct", "chartqa"), "exploratory")
        self.assertEqual(an.confirmatory_role("Qwen/Qwen2.5-VL-3B-Instruct", "math"), "confirmatory")

        rows = synth(eff_bind=1.0, eff_non=0.2, ceil=2.0)
        # Attach synthetic behavioural rows across all 5 verdicts + matching donor rows for D1/D2/D5.
        ids = sorted({r["id"] for r in rows})
        beh_rows = []
        donor_rows = []
        for idx, i in enumerate(ids):
            for fam in ("binding", "nonbinding"):
                for ver in ("own", "none", "para", "flip", "para_flip"):
                    for order in ("image_first", "text_first"):
                        ans = "4" if (ver in ("flip", "para_flip") or (ver == "none" and idx % 2 == 0)) else "9"
                        beh_rows.append(
                            {
                                "model_id": "M",
                                "regime": "math",
                                "phase": "dev",
                                "id": i,
                                "family": fam,
                                "verdict": ver,
                                "k": 1,
                                "order": order,
                                "outcome": "beh",
                                "y_image": "4",
                                "y_text": "9",
                                "own_source": "text",
                                "named_source": "image" if ver in ("flip", "para_flip") else ("text" if ver in ("own", "para") else None),
                                "full_text": f"The final answer is {ans}.",
                            }
                        )
            for order in ("image_first", "text_first"):
                donor_rows.append(
                    {
                        "model_id": "M",
                        "regime": "math",
                        "id": i,
                        "family": "donor",
                        "order": order,
                        "y_image": "4",
                        "y_text": "9",
                        "full_text": "They differ. The typed text is more reliable.\n\nThe final answer is 9.",
                    }
                )
        beh = an.behaviour_table(beh_rows, parser="structured")
        d_fo = an.beh_diff(beh, ids, "binding", "flip", "own")
        d_no = an.beh_diff(beh, ids, "binding", "none", "own")
        d_fn = an.beh_diff(beh, ids, "binding", "flip", "none")
        for i in ids:
            self.assertAlmostEqual(d_no[i] + d_fn[i], d_fo[i], places=9)

        res = an.analyze_group(rows + beh_rows, reps=100, draws=100, donor_rows=donor_rows)
        self.assertEqual(res["primary_outcome"], "behaviour")
        self.assertEqual(res["confirmatory_role"], "confirmatory")
        self.assertTrue(res["behaviour_primary"]["is_primary_for_regime"])
        self.assertIn("matched_pair_para_flip_minus_para", res["behaviour_primary"]["binding"])
        self.assertIn("none_minus_own", res["behaviour_primary"]["binding"])
        self.assertIn("flip_minus_none", res["behaviour_primary"]["binding"])
        self.assertIn("para_flip_minus_none", res["behaviour_primary"]["binding"])
        self.assertEqual(len(res["behaviour_primary"]["holm_adjusted"]), 3)
        self.assertIsNotNone(res["replay_noise"])
        self.assertIn("replay_adjusted_max_churn", res["behaviour_binding"]["wording_floor_para_minus_own"])

    def test_sample_v5_for_coding_sample_and_evaluate(self):
        import sample_v5_for_coding as sv5

        with tempfile.TemporaryDirectory() as d:
            donor_path = os.path.join(d, "test_donor_qwen25.jsonl")
            out_dir = os.path.join(d, "coding_v5")
            records = []
            for idx in range(6):
                records.append(
                    {
                        "id": f"m_{idx}",
                        "model_id": "Qwen/Qwen2.5-VL-3B-Instruct",
                        "regime": "math",
                        "family": "donor" if idx % 2 == 0 else "free_binding",
                        "order": "image_first" if idx < 3 else "text_first",
                        "y_image": "10",
                        "y_text": "20",
                        "full_text": "Looking carefully at both inputs, the two sources clearly disagree with each other. I consider the typed text to be more reliable here.\n\n#### 20",
                    }
                )
            with open(donor_path, "w", encoding="utf-8") as f:
                for rec in records:
                    f.write(json.dumps(rec) + "\n")

            argv = sys.argv
            try:
                sys.argv = ["sample_v5_for_coding.py", "sample", "--donor_files", donor_path, "--out_dir", out_dir, "--n_donors", "4", "--n_flips_per_model", "2"]
                self.assertEqual(sv5.main(), 0)
            finally:
                sys.argv = argv

            key_v = sv5.read_csv_map(os.path.join(out_dir, "KEY_verdicts_do_not_open.csv"))
            ca_v = sv5.read_csv_map(os.path.join(out_dir, "coder_A_verdicts.csv"))
            cb_v = sv5.read_csv_map(os.path.join(out_dir, "coder_B_verdicts.csv"))
            self.assertEqual(len(key_v), 4)
            self.assertNotIn("predicted_stated_source", next(iter(ca_v.values())))
            for sid in key_v:
                ca_v[sid]["coder_stated_source"] = "text"
                cb_v[sid]["coder_stated_source"] = "text"
            v_eval = sv5.evaluate_verdicts(ca_v, cb_v, key_v)
            self.assertEqual(v_eval["parser_accuracy_overall"], 1.0)
            self.assertEqual(v_eval["inter_coder_agreement"], 1.0)

            key_f = sv5.read_csv_map(os.path.join(out_dir, "KEY_flips_do_not_open.csv"))
            ca_f = sv5.read_csv_map(os.path.join(out_dir, "coder_A_flips.csv"))
            self.assertEqual(len(key_f), 2)
            for sid in key_f:
                ca_f[sid]["coder_grammatical_coherent"] = "1"
                ca_f[sid]["coder_names_intended_source"] = "1"
            f_eval = sv5.evaluate_flips(ca_f, None, key_f)
            self.assertEqual(f_eval["grammatical_rate"], 1.0)
            self.assertEqual(f_eval["names_intended_source_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
