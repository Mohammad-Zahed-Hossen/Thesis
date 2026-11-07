#!/usr/bin/env python3
"""Tests for the v4 analysis and harness code. Needs no GPU, torch or network.

Run from Experiment/:
    python -m unittest tests.test_v4 -v

HFBackend isn't covered: it needs a GPU session. The Colab smoke test in RUNBOOK_v4.md
is its first real check.
"""
import ast
import copy
import csv
import json
import math
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
sys.path.insert(0, EXPERIMENT)

import analyze_v4 as an
import harness_v4 as h
import reanalyze_v3 as re3
import sample_for_coding as sfc
import score_v4 as sc
import statistical_analysis as st
import transplant_v4 as tp

V3_RESULTS = os.path.join(EXPERIMENT, "results_v3", "full_experiment_results v3.0.json")
V3_HARNESS = os.path.join(EXPERIMENT, "archive", "harness_v3", "production_experiment_harness_v3.py")


def quiet(*_args, **_kwargs):
    pass


class AnswerExtraction(unittest.TestCase):
    def test_direct_number(self):
        self.assertEqual(sc.extract_answer("work\n#### 42"), ("42", "hash_direct"))

    def test_currency_comma_and_period(self):
        self.assertEqual(sc.extract_answer("#### $1,200.")[0], "1200")

    def test_literal_template_then_sentence(self):
        self.assertEqual(sc.extract_answer("#### <answer>\nJoe will have $18 left."), ("18", "hash_tail"))

    def test_answer_tags(self):
        self.assertEqual(sc.extract_answer("#### <answer>7</answer>")[0], "7")

    def test_bare_template_uses_flagged_fallback(self):
        self.assertEqual(sc.extract_answer("so 5 + 6 = 11\n#### <answer>"), ("11", "fallback_last_number"))

    def test_words_without_number_are_not_an_answer(self):
        self.assertEqual(sc.extract_answer("3 cats.\n#### <answer>\nNot enough information."), (None, "hash_no_number"))

    def test_last_marker_wins_over_markdown_headers(self):
        self.assertEqual(sc.extract_answer("#### Calculation: 3 + 4\n#### 7")[0], "7")

    def test_only_text_after_the_last_marker_counts(self):
        self.assertEqual(sc.extract_answer("#### Step one gives 3\n#### 7 apples, from 9")[0], "7")

    def test_subtraction_is_not_a_negative_answer(self):
        self.assertEqual(sc.extract_answer("then 10-5")[0], "5")
        self.assertEqual(sc.extract_answer("10 - 5")[0], "5")

    def test_explicit_negative(self):
        self.assertEqual(sc.extract_answer("#### -5")[0], "-5")

    def test_no_number(self):
        self.assertEqual(sc.extract_answer("no digits here"), (None, "none"))

    def test_numeric_equality(self):
        self.assertTrue(sc.numeric_equal("18.00", "18"))
        self.assertTrue(sc.numeric_equal("$1,200", "1200"))
        self.assertFalse(sc.numeric_equal("18.5", "18"))
        self.assertFalse(sc.numeric_equal(None, "18"))
        self.assertFalse(sc.numeric_equal("abc", "18"))

    def test_answer_source(self):
        self.assertEqual(sc.answer_source("3", "3", "4"), "image")
        self.assertEqual(sc.answer_source("4.0", "3", "4"), "text")
        self.assertEqual(sc.answer_source("9", "3", "4"), "neither")
        self.assertEqual(sc.answer_source("3", "3", "3"), "both")


class Segmentation(unittest.TestCase):
    def test_keeps_third_sentence_before_solving(self):
        t = "They do not agree. The image is about cats. I consider the text more reliable.\n\nTo solve the problem: 2 + 2"
        v, s = sc.split_verbalization(t)
        self.assertIn("more reliable", v)
        self.assertTrue(s.strip().startswith("To solve"))
        self.assertEqual(v + s, t)

    def test_direct_answer_has_no_verbalization(self):
        self.assertEqual(sc.split_verbalization("To solve this, add 2 and 2.")[0], "")

    def test_two_sentence_fallback(self):
        v, s = sc.split_verbalization("One thing here. Another thing here. A third thing with 4.")
        self.assertEqual(v, "One thing here. Another thing here.")
        self.assertEqual(s.strip(), "A third thing with 4.")

    def test_abbreviation_is_not_a_sentence_end(self):
        v, _ = sc.split_verbalization("Mr. Jackson has pens. He has more. And then this.")
        self.assertEqual(v, "Mr. Jackson has pens. He has more.")

    def test_cue_inside_a_sentence_does_not_cut_it(self):
        # Regression: this cut donors to "...a clear and specific problem " in the first dev run.
        t = "They do not agree. The text is more reliable as it provides a clear problem to solve. The solution is as follows:\n\n1. Add."
        v, s = sc.split_verbalization(t)
        self.assertTrue(v.rstrip().endswith("a clear problem to solve."), v)
        self.assertTrue(s.lstrip().startswith("The solution"), s)
        self.assertEqual(v + s, t)

    def test_quoted_sentence_end_counts(self):
        v, _ = sc.split_verbalization('It asks "How many pens?" It also asks "How many hats?" And more here.')
        self.assertEqual(v, 'It asks "How many pens?" It also asks "How many hats?"')

    def test_numbered_list_is_a_cue(self):
        v, s = sc.split_verbalization("They differ. The text is clearer.\n1. Add them.")
        self.assertTrue(s.startswith("1. Add"), s)
        self.assertEqual(v, "They differ. The text is clearer.\n")

    def test_description_only_has_no_solve_segment(self):
        self.assertEqual(sc.split_verbalization("The image shows a problem about John.")[1], "")


class AttemptClassifier(unittest.TestCase):
    IMAGE = "Janet's ducks lay 16 eggs. How much does she make at the market?"
    TEXT = "A robe takes 2 bolts of blue fiber. How many bolts does it take?"

    def test_image_problem(self):
        self.assertEqual(sc.classify_attempt("Janet sells eggs from ducks at the market", self.IMAGE, self.TEXT).label, "image")

    def test_text_problem(self):
        self.assertEqual(sc.classify_attempt("The robe uses bolts of fiber", self.IMAGE, self.TEXT).label, "text")

    def test_one_word_margin_is_unknown(self):
        self.assertEqual(sc.classify_attempt("The robe", self.IMAGE, self.TEXT).label, "unknown")
        self.assertEqual(sc.classify_attempt("Janet", self.IMAGE, self.TEXT).label, "unknown")

    def test_word_boundaries(self):
        # v3 matched "ram" inside "program" and counted it as a hit.
        a = sc.classify_attempt("this program diagram", "Ram has pens and Ramesh too", "Tom sells kites")
        self.assertEqual(a.image_hits, 0)

    def test_sentence_initial_stopwords_are_not_entities(self):
        # v3 kept these because capitalised words bypassed its stoplist.
        self.assertFalse({"how", "the", "she"} & sc.extract_entities("How many? The cat. She ran."))

    def test_names_are_not_mangled(self):
        # v3's rstrip("'s") turned James into "jame" and Ross into "ro".
        e = sc.extract_entities("James met Ross and Chris's dog")
        self.assertTrue({"james", "ross", "chris"} <= e)

    def test_plural_counts(self):
        self.assertEqual(sc.classify_attempt("ducks and birds", "A duck and a bird here", "Kites and strings here").image_hits, 2)


class RefusalAndVerdict(unittest.TestCase):
    def test_verdict_uncertainty_then_solving_is_not_refusal(self):
        t = "I cannot determine if they agree or contradict each other. However, I can solve it. 2 + 2 = 4."
        self.assertFalse(sc.is_refusal(t))

    def test_stated_intent_to_solve_is_not_refusal_even_without_digits(self):
        self.assertFalse(sc.is_refusal("I cannot determine if they agree. However, I can solve the problem by adding them"))

    def test_numbers_after_phrase_is_not_refusal(self):
        self.assertFalse(sc.is_refusal("We cannot determine this directly. So 3 x 4 = 12."))

    def test_real_refusal(self):
        self.assertTrue(sc.is_refusal("The problem cannot be solved based on the given information."))
        self.assertTrue(sc.is_refusal("Costs 3 dollars. There is not enough information to answer."))

    def test_verdicts(self):
        cases = {
            "The image and the text do not agree.": "conflict",
            "The two contradict each other.": "conflict",
            "They are about different problems.": "conflict",
            "The image and the text agree.": "agree",
            "They do not contradict each other.": "agree",
            "I cannot determine if they agree or contradict each other.": "cannot_determine",
            "There is no agreement or contradiction between them.": "no_relation",
            "The image and the text do not provide any information about Peter.": "no_info",
            "A problem about horses.": "none",
        }
        for text, label in cases.items():
            self.assertEqual(sc.classify_verdict(text), label, text)

    def test_no_info_with_explicit_conflict_is_conflict(self):
        self.assertEqual(sc.classify_verdict("They do not agree. The text does not contain any cats."), "conflict")

    def test_stated_reliable(self):
        cases = {
            "I consider the text more reliable as it is specific.": "text",
            "The image is more reliable.": "image",
            "The more reliable source is the image.": "image",
            "I cannot determine which source is more reliable.": "undetermined",
            "They do not agree.": "absent",
        }
        for text, label in cases.items():
            self.assertEqual(sc.stated_reliable_source(text), label, text)


class Statistics(unittest.TestCase):
    def test_mcnemar_small_known_value(self):
        # b=3, c=1: 2 * (C(4,0) + C(4,1)) / 2^4 = 0.625
        self.assertAlmostEqual(10 ** st.mcnemar_exact_log10p(3, 1), 0.625)

    def test_mcnemar_is_capped_at_one(self):
        self.assertEqual(st.mcnemar_exact_log10p(5, 5), 0.0)
        self.assertEqual(st.mcnemar_exact_log10p(0, 0), 0.0)

    def test_mcnemar_does_not_underflow(self):
        self.assertAlmostEqual(st.mcnemar_exact_log10p(1057, 25), -274.86, places=1)

    def test_format(self):
        self.assertEqual(st.format_log10p(0.0), "1")
        self.assertEqual(st.format_log10p(math.log10(0.5)), "0.5000")
        self.assertTrue(st.format_log10p(-274.86).endswith("e-275"))

    def test_holm(self):
        got = st.holm_adjust_log10([math.log10(0.01), math.log10(0.04), math.log10(0.03)])
        self.assertAlmostEqual(10 ** got[0], 0.03)
        self.assertAlmostEqual(10 ** got[2], 0.06)
        self.assertAlmostEqual(10 ** got[1], 0.06)

    def test_interval_widens_under_clustering(self):
        # Same mean and same n, but one cluster structure has only two problems.
        values = [1.0] * 50 + [0.0] * 50
        free = [str(i) for i in range(100)]
        low, high = st.pigeonhole_ci(values, free, free, reps=300)
        tied = ["a"] * 50 + ["b"] * 50
        low2, high2 = st.pigeonhole_ci(values, tied, tied, reps=300)
        self.assertLess(high - low, high2 - low2)
        self.assertLessEqual(low, 0.5)
        self.assertGreaterEqual(high, 0.5)

    def test_validate_rejects_missing_arm(self):
        with self.assertRaises(ValueError):
            st.validate([{"id": "x", "arms": {"arm1_direct": {}}}])
        with self.assertRaises(ValueError):
            st.validate([])


class V3Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(V3_RESULTS, encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_paired_numbers_match_the_stored_data(self):
        r = st.analyze_experiment(self.data, reps=50)
        p = r["primary"]
        self.assertEqual(p["table"], {"both_visual": 392, "arm2_only": 1057, "arm3_only": 25, "neither": 145})
        self.assertAlmostEqual(p["difference_arm2_minus_arm3"], 1032 / 1619)
        self.assertAlmostEqual(p["paired_odds_ratio"], 42.28)
        self.assertEqual(r["arm4"]["text_match_4b_only"], 105)
        self.assertEqual(r["arm4"]["text_match_4a_only"], 19)

    def test_report_contains_no_fixed_verdicts(self):
        report = st.render_markdown(st.analyze_experiment(self.data, reps=50)).lower()
        for phrase in ("causally", "very large", "strongest possible", "definitive", "legitimate epistemic"):
            self.assertNotIn(phrase, report)

    def test_report_numbers_change_with_the_data(self):
        # A planted change must reach the output, so the report can't be a fixed string.
        mutated = copy.deepcopy(self.data)
        for d in mutated[:100]:
            d["arms"]["arm2_placebo"]["choice"] = "ambiguous"
        self.assertNotEqual(
            st.render_markdown(st.analyze_experiment(self.data, reps=20)),
            st.render_markdown(st.analyze_experiment(mutated, reps=20)),
        )

    def test_check_passes_on_stored_data(self):
        self.assertEqual(re3.check(self.data, re3.compute(self.data, reps=20)), [])

    def test_check_rejects_a_planted_fault(self):
        mutated = copy.deepcopy(self.data)
        mutated[0]["arms"]["arm3_conflict"]["choice"] = "abstains" if mutated[0]["arms"]["arm3_conflict"]["choice"] != "abstains" else "ambiguous"
        errors = re3.check(mutated, re3.compute(mutated, reps=20))
        self.assertTrue(any("arm3_conflict abstain" in e for e in errors), errors)

    def test_scorer_reproduces_the_cross_over_direction(self):
        distinct = [d for d in self.data if not sc.numeric_equal(d["image_answer"], d["text_answer"])]
        self.assertEqual(len(distinct), 1600)

        def rate(arm, source):
            hits = 0
            for d in distinct:
                answer, _ = sc.extract_answer(d["arms"][arm]["text"])
                hits += sc.answer_source(answer, d["image_answer"], d["text_answer"]) == source
            return hits / len(distinct)

        self.assertGreater(rate("arm2_placebo", "image"), rate("arm2_placebo", "text") + 0.2)
        self.assertGreater(rate("arm3_conflict", "text"), rate("arm3_conflict", "image") + 0.2)

    def test_cannot_determine_outputs_are_mostly_not_refusals(self):
        legacy = [d for d in self.data if d["arms"]["arm3_conflict"]["choice"] == "abstains"]
        refused = sum(sc.is_refusal(d["arms"]["arm3_conflict"]["text"]) for d in legacy)
        self.assertEqual(len(legacy), 221)
        self.assertLess(refused, 60)


def make_item(i: int, source: str = "gsm8k", n: int = 10) -> h.Item:
    j = (i + 1) % n
    return h.Item(
        id=f"{source}-image-L0-{i:04d}", source=source, image=None,
        image_question=f"{source} problem {i}", text_question=f"{source} problem {j}",
        y_image=str(i + 100), y_text=str(j + 100),
    )


class Prompts(unittest.TestCase):
    def test_v3_arms_are_verbatim(self):
        with open(V3_HARNESS, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        v3 = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id.startswith("PROMPT_ARM"):
                v3[node.targets[0].id] = ast.literal_eval(node.value)
        self.assertEqual(h.ARMS["direct_v3"].templates[0], v3["PROMPT_ARM1_DIRECT"])
        self.assertEqual(h.ARMS["placebo_v3"].templates[0], v3["PROMPT_ARM2_PLACEBO"])
        self.assertEqual(h.ARMS["conflict_v3"].templates[0], v3["PROMPT_ARM3_CONFLICT"])

    def test_v4_arms_share_the_same_ending(self):
        names = ["filler", "desc_image_first", "desc_text_first", "detect_only", "reliability_only", "conflict_full"]
        for n in names:
            for t in h.ARMS[n].templates:
                self.assertTrue(t.startswith(h.OPEN), n)
                self.assertTrue(t.endswith("Then solve the problem. " + h.FORMAT), n)

    def test_arm_sets_only_name_real_arms(self):
        for arms in h.ARM_SETS.values():
            for a in arms:
                self.assertIn(a, h.ARMS)

    def test_paraphrase_set_has_paraphrases(self):
        for a in h.ARM_SETS["paraphrase"]:
            self.assertGreaterEqual(len(h.ARMS[a].templates), 3, a)
            h.build_request(make_item(0), a, 2)

    def test_chartqa_prompt_shows_the_report(self):
        # v3 never displayed text_report, so this mode contained no conflict.
        row = {"conflict_id": 7, "question": "What was revenue?", "text_report": "Revenue was 4.10 million.", "chart_answer": 3.89, "report_answer": 4.1}
        item = h.item_from_chartqa_row(row)
        prompt = h.build_request(item, "conflict_full").prompt
        self.assertIn("Revenue was 4.10 million.", prompt)
        self.assertIn("What was revenue?", prompt)
        self.assertEqual((item.y_image, item.y_text), ("3.89", "4.1"))

    def test_chartqa_image_only_asks_the_question_without_the_report(self):
        row = {"conflict_id": 7, "question": "What was revenue?", "text_report": "Revenue was 4.10 million.", "chart_answer": 3.89, "report_answer": 4.1}
        prompt = h.build_request(h.item_from_chartqa_row(row), "base_image").prompt
        self.assertIn("What was revenue?", prompt)
        self.assertNotIn("4.10", prompt)

    def test_chartqa_rejects_congruent_arm(self):
        item = h.Item("1", "chartqa", None, "", "report", "1", "2")
        with self.assertRaises(ValueError):
            h.build_request(item, "congruent_direct")

    def test_congruent_uses_the_image_problem_as_text(self):
        item = make_item(3)
        req = h.build_request(item, "congruent_conflict")
        self.assertIn(item.image_question, req.prompt)
        self.assertNotIn(item.text_question, req.prompt)
        self.assertEqual(h.gold_answers(req), {"y_image": item.y_image, "y_text": item.y_image})

    def test_single_source_gold(self):
        item = make_item(3)
        self.assertEqual(h.gold_answers(h.build_request(item, "base_text"))["y_text"], item.y_text)
        self.assertEqual(h.gold_answers(h.build_request(item, "base_image"))["y_image"], item.y_image)
        self.assertFalse(h.build_request(item, "base_text").uses_image)
        self.assertNotIn(item.image_question, h.build_request(item, "base_text").prompt)


class Splits(unittest.TestCase):
    def setUp(self):
        self.items = [make_item(i, "gsm8k", 800) for i in range(800)] + [make_item(i, "svamp", 200) for i in range(200)]

    def test_dev_is_proportional_by_source(self):
        dev = h.split_phase(self.items, "dev", 100)
        self.assertEqual(sum(i.source == "gsm8k" for i in dev), 80)
        self.assertEqual(sum(i.source == "svamp" for i in dev), 20)

    def test_dev_and_confirm_share_no_problem(self):
        dev = h.split_phase(self.items, "dev", 100)
        confirm = h.split_phase(self.items, "confirm", 100)
        used = set().union(*(h.problem_keys(i) for i in dev))
        self.assertFalse(used & set().union(*(h.problem_keys(i) for i in confirm)))
        self.assertFalse({i.id for i in dev} & {i.id for i in confirm})
        self.assertGreater(len(confirm), 850)

    def test_real_v3_item_split(self):
        items = h.load_items_from_v3(V3_RESULTS)
        self.assertEqual(len(items), 1600)
        dev = h.split_phase(items, "dev", 200)
        confirm = h.split_phase(items, "confirm", 200)
        self.assertEqual(len(dev), 200)
        self.assertFalse(set().union(*(h.problem_keys(i) for i in dev)) & set().union(*(h.problem_keys(i) for i in confirm)))
        self.assertGreater(len(confirm), 1380)

    def test_equal_answers_are_dropped(self):
        a, b = make_item(0), make_item(1)
        b.y_text = "101.0"
        b.y_image = "101"
        self.assertEqual([i.id for i in h.filter_distinct([a, b])], [a.id])

    def test_unknown_phase(self):
        with self.assertRaises(ValueError):
            h.split_phase(self.items, "test")


class ChatAndDecode(unittest.TestCase):
    @staticmethod
    def template(messages, tokenize, add_generation_prompt):
        out = ""
        for m in messages:
            content = m["content"] if isinstance(m["content"], str) else "".join("<img>" if c["type"] == "image" else c["text"] for c in m["content"])
            out += f"<|im_start|>{m['role']}\n{content}<|im_end|>\n"
        return out + ("<|im_start|>assistant\n" if add_generation_prompt else "")

    def test_generation_prompt(self):
        self.assertTrue(h.render_chat(self.template, "Q", None, True).endswith("<|im_start|>assistant\n"))

    def test_prefill_leaves_assistant_turn_open(self):
        text = h.render_chat(self.template, "Q", "My view.\n\n", True)
        self.assertTrue(text.endswith("My view.\n\n"))
        self.assertNotIn("<|im_end|>\n<|im_start|>assistant\n<", text[-5:])

    def test_text_only_has_no_image_token(self):
        self.assertNotIn("<img>", h.render_chat(self.template, "Q", None, False))
        self.assertIn("<img>", h.render_chat(self.template, "Q", None, True))

    def test_changed_prefill_is_an_error(self):
        def stripping(messages, tokenize, add_generation_prompt):
            return self.template(messages, tokenize, add_generation_prompt).replace("\n\n", "\n")

        with self.assertRaises(RuntimeError):
            h.render_chat(stripping, "Q", "My view.\n\n", True)

    def test_decode_stops_at_any_eos(self):
        self.assertEqual(h.decode_ids([1, 2, 9, 3], {8, 9}, 0), ([1, 2], True))
        self.assertEqual(h.decode_ids([1, 2, 8, 3], {8, 9}, 0), ([1, 2], True))

    def test_decode_without_eos(self):
        self.assertEqual(h.decode_ids([1, 2, 3], {8}, 0), ([1, 2, 3], False))


class Runner(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "run.jsonl")
        self.cfg = h.RunConfig(run_tag="t", batch_size=4, backend="echo")
        self.items = [make_item(i) for i in range(10)]
        self.requests = [h.build_request(i, "direct") for i in self.items]

    def tearDown(self):
        self.tmp.cleanup()

    def test_writes_every_request(self):
        self.assertEqual(h.run_requests(self.requests, h.EchoBackend(), self.cfg, self.path, log=quiet), 10)

    def test_resume_skips_finished_rows(self):
        h.run_requests(self.requests[:4], h.EchoBackend(), self.cfg, self.path, log=quiet)
        self.assertEqual(h.run_requests(self.requests, h.EchoBackend(), self.cfg, self.path, log=quiet), 6)
        with open(self.path, encoding="utf-8") as f:
            ids = [json.loads(line)["id"] for line in f]
        self.assertEqual(sorted(ids), sorted(i.id for i in self.items))

    def test_resume_reruns_a_cut_off_line(self):
        h.run_requests(self.requests[:2], h.EchoBackend(), self.cfg, self.path, log=quiet)
        with open(self.path, encoding="utf-8") as f:
            lines = f.readlines()
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(lines[0] + lines[1][:20])
        self.assertEqual(len(h.load_done(self.path)), 1)

    def test_oom_halves_then_finishes(self):
        backend = h.EchoBackend(oom_above=1)
        self.assertEqual(h.run_requests(self.requests, backend, self.cfg, self.path, log=quiet), 10)
        self.assertEqual(set(backend.batches), {1})

    def test_oom_at_one_item_is_raised(self):
        with self.assertRaises(h.BackendOutOfMemory):
            h.generate_safe(h.EchoBackend(oom_above=0), self.requests[:1], self.cfg)

    def test_cap_flag(self):
        self.cfg.max_new_tokens = 3
        h.run_requests(self.requests[:1], h.EchoBackend(), self.cfg, self.path, log=quiet)
        with open(self.path, encoding="utf-8") as f:
            self.assertTrue(json.loads(f.readline())["hit_cap"])

    def test_row_keeps_prefill_in_full_text(self):
        req = h.Request(self.items[0], "z0_m0", "P", "conflict", prefill="Mine.\n\n")
        row = h.make_row(req, h.Generation("rest", 1, False), self.cfg, 0.0)
        self.assertEqual(row["full_text"], "Mine.\n\nrest")
        self.assertEqual(row["generated"], "rest")

    def test_incomplete_run_is_reported(self):
        h.run_requests(self.requests[:9], h.EchoBackend(), self.cfg, self.path, log=quiet)
        self.assertEqual(h.report_missing(self.requests, self.path), 1)
        h.run_requests(self.requests, h.EchoBackend(), self.cfg, self.path, log=quiet)
        self.assertEqual(h.report_missing(self.requests, self.path), 0)

    def test_manifest_blocks_changed_settings(self):
        path = os.path.join(self.tmp.name, "m.json")
        h.write_manifest(path, self.cfg, h.EchoBackend(), 1, [V3_HARNESS])
        h.write_manifest(path, self.cfg, h.EchoBackend(), 1, [V3_HARNESS])
        self.cfg.repetition_penalty = 1.05
        with self.assertRaises(SystemExit):
            h.write_manifest(path, self.cfg, h.EchoBackend(), 1, [V3_HARNESS])

    def test_confirm_needs_pins(self):
        cfg = h.RunConfig(run_tag="t", phase="confirm", model_id="unknown/model")
        with self.assertRaises(SystemExit):
            h.resolve_revisions(cfg)

    def test_known_model_gets_a_pin(self):
        cfg = h.RunConfig(run_tag="t", phase="confirm")
        h.resolve_revisions(cfg)
        self.assertEqual(cfg.model_revision, h.MODEL_PINS[cfg.model_id])
        self.assertEqual(cfg.dataset_revision, h.DATASET_PINS[h.CONFLICT_DATASET])


class Transplant(unittest.TestCase):
    def test_prefill_keeps_a_real_blank_line(self):
        self.assertEqual(tp.donor_prefill("They differ. Text is better.\n\nTo solve: 2 + 2 = 4."), "They differ. Text is better.\n\n")

    def test_prefill_keeps_a_single_newline(self):
        self.assertEqual(tp.donor_prefill("They differ. Text is better.\n1. Add."), "They differ. Text is better.\n")

    def test_prefill_drops_a_space_the_next_token_carries(self):
        self.assertEqual(tp.donor_prefill("They differ. Text wins. To solve it, add."), "They differ. Text wins.")

    def test_prefill_continuation_rebuilds_the_donor(self):
        # The output must be recoverable from prefill + continuation, as real generation does.
        for text in ("They differ. Text wins.\n\nTo solve: 4.", "They differ. Text wins. To solve it, add."):
            prefill = tp.donor_prefill(text)
            self.assertTrue(text.startswith(prefill))
            self.assertEqual(prefill + text[len(prefill) :], text)

    def test_prefill_for_a_donor_that_never_solved(self):
        self.assertEqual(tp.donor_prefill("One thing. Another thing."), "One thing. Another thing.\n\n")

    def test_no_verbalization_means_no_donor(self):
        self.assertEqual(tp.donor_prefill("To solve this, add 2 and 2."), "")

    def test_all_cells_for_items_with_both_donors(self):
        items = [make_item(0), make_item(1)]
        neutral = {items[0].id: "n0\n\n", items[1].id: "n1\n\n"}
        conflict = {items[0].id: "c0\n\n"}
        reqs, excluded = tp.build_requests(items, neutral, conflict, "desc_image_first", "conflict_full")
        self.assertEqual(excluded, {"no_neutral_donor": 0, "no_conflict_donor": 1})
        self.assertEqual({r.item.id for r in reqs}, {items[0].id})
        self.assertEqual(len(reqs), 14)

    def test_crossing_is_correct(self):
        item = make_item(0)
        reqs, _ = tp.build_requests([item], {item.id: "NEUTRAL\n\n"}, {item.id: "CONFLICT\n\n"}, "desc_image_first", "conflict_full")
        cell = {r.arm: r for r in reqs}
        z0, z1 = h.build_request(item, "desc_image_first").prompt, h.build_request(item, "conflict_full").prompt
        self.assertEqual((cell["z0_m1"].prompt, cell["z0_m1"].prefill), (z0, "CONFLICT\n\n"))
        self.assertEqual((cell["z1_m0"].prompt, cell["z1_m0"].prefill), (z1, "NEUTRAL\n\n"))
        self.assertEqual(cell["z0_m0"].prefill, "NEUTRAL\n\n")
        self.assertEqual(cell["z1_m1"].prefill, "CONFLICT\n\n")
        self.assertIn("image more reliable", cell["z0_rel_image"].prefill)
        self.assertIn("typed text more reliable", cell["z1_rel_text"].prefill)

    def test_donors_from_another_model_are_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "donor.jsonl")
            with open(path, "w", encoding="utf-8") as f:
                f.write(json.dumps({"arm": "conflict_full", "model_id": "other/model", "id": "x", "full_text": "They differ."}) + "\n")
            with self.assertRaises(SystemExit):
                tp.load_donors(path, "desc_image_first", "conflict_full", "this/model")


def fake_row(arm, item_id, text, y_i="1", y_t="2", hit_cap=False, tokens=10):
    return {
        "model_id": "m", "split": "conflict", "phase": "dev", "repetition_penalty": 1.0, "do_sample": False, "seed": 42, "paraphrase": 0,
        "id": item_id, "arm": arm, "source": "gsm8k", "stimulus": "conflict",
        "image_question": f"image {item_id}", "text_question": f"text {item_id}",
        "y_image": y_i, "y_text": y_t, "full_text": text, "hit_cap": hit_cap, "tokens": tokens,
        "score": sc.score_output(text, f"image {item_id}", f"text {item_id}", y_i, y_t),
    }


class Analysis(unittest.TestCase):
    def test_contrast_counts_and_direction(self):
        rows = []
        for i in range(30):
            rows.append(fake_row("conflict_full", f"i{i}", "#### 2"))
            rows.append(fake_row("filler", f"i{i}", "#### 1"))
        r = an.analyze(rows, reps=20)
        result = list(r.values())[0]["behaviour_primary"]
        text = next(c for c in result if c["outcome"] == "answer:text")
        self.assertEqual((text["first_only"], text["second_only"], text["n"]), (30, 0, 30))
        self.assertAlmostEqual(text["difference"], 1.0)

    def test_contrast_uses_only_items_in_both_arms(self):
        rows = [fake_row("conflict_full", "a", "#### 2"), fake_row("filler", "a", "#### 1"), fake_row("filler", "b", "#### 1")]
        result = list(an.analyze(rows, reps=20).values())[0]["behaviour_primary"]
        self.assertEqual(result[0]["n"], 1)

    def test_settings_are_not_pooled(self):
        a = fake_row("filler", "a", "#### 1")
        b = fake_row("conflict_full", "a", "#### 2")
        b["repetition_penalty"] = 1.05
        results = an.analyze([a, b], reps=20)
        self.assertEqual(len(results), 2)
        for v in results.values():
            self.assertEqual(v["behaviour_primary"], [])

    def test_gates_pass_when_clean(self):
        rows = [fake_row("filler", f"i{i}", "#### 1") for i in range(100)]
        summaries = {k: v["arms"] for k, v in an.analyze(rows, reps=10).items()}
        self.assertEqual(an.check_gates(summaries), [])

    def test_gate_catches_token_cap(self):
        rows = [fake_row("filler", f"i{i}", "#### 1", hit_cap=i < 5) for i in range(100)]
        failures = an.check_gates({k: v["arms"] for k, v in an.analyze(rows, reps=10).items()})
        self.assertTrue(any("token cap" in f for f in failures), failures)

    def test_gate_allows_cap_just_under_limit(self):
        rows = [fake_row("filler", f"i{i}", "#### 1", hit_cap=i < 4) for i in range(100)]
        self.assertEqual(an.check_gates({k: v["arms"] for k, v in an.analyze(rows, reps=10).items()}), [])

    def test_gate_catches_missing_answers(self):
        rows = [fake_row("filler", f"i{i}", "words only" if i < 11 else "#### 1") for i in range(100)]
        failures = an.check_gates({k: v["arms"] for k, v in an.analyze(rows, reps=10).items()})
        self.assertTrue(any("answer or refusal" in f for f in failures), failures)

    def test_refusal_counts_as_a_valid_outcome_for_the_gate(self):
        rows = [fake_row("filler", f"i{i}", "It cannot be solved." if i < 20 else "#### 1") for i in range(100)]
        self.assertEqual(an.check_gates({k: v["arms"] for k, v in an.analyze(rows, reps=10).items()}), [])

    def test_wording_control_and_fidelity(self):
        rows = [
            fake_row("z0_eq_a", "a", "#### 1"), fake_row("z0_eq_b", "a", "#### 2"),
            fake_row("z0_eq_a", "b", "#### 1"), fake_row("z0_eq_b", "b", "#### 1.0"),
            fake_row("z1_m1", "a", "They differ.\n\nTo solve: #### 7"), fake_row("conflict_full", "a", "They differ.\n\nTo solve: #### 7"),
            fake_row("z1_m1", "b", "They differ.\n\nTo solve: #### 8"), fake_row("conflict_full", "b", "They differ.\n\nTo solve: #### 9"),
        ]
        r = list(an.analyze(rows, reps=10).values())[0]
        self.assertAlmostEqual(r["prefix_sensitivity"][0]["answer_changed"], 0.5)
        self.assertAlmostEqual(r["fidelity"][0]["same_answer"], 0.5)

    def test_fidelity_excludes_donors_that_never_solved(self):
        rows = [
            fake_row("z1_m1", "a", "They differ. Text wins.\n\nTo solve: #### 7"),
            fake_row("conflict_full", "a", "They differ. Text wins.\n\nTo solve: #### 7"),
            fake_row("z1_m1", "b", "They differ. Text wins.\n\n#### 8"),
            fake_row("conflict_full", "b", "They differ. Text wins."),
        ]
        f = list(an.analyze(rows, reps=10).values())[0]["fidelity"][0]
        self.assertEqual((f["n"], f["excluded_no_solve"], f["same_answer"]), (1, 1, 1.0))

    def test_missing_rows_fail_the_gates(self):
        rows = [fake_row("filler", "a", "#### 1"), fake_row("filler", "b", "#### 1"), fake_row("direct", "a", "#### 1")]
        self.assertEqual(list(an.missing_rows(rows).values())[0], {"direct": ["b"]})
        self.assertTrue(any("direct: 1 missing" in f for f in an.completeness_failures(rows)))

    def test_complete_rows_pass_completeness(self):
        rows = [fake_row("filler", "a", "#### 1"), fake_row("direct", "a", "#### 1")]
        self.assertEqual(an.completeness_failures(rows), [])

    def test_v3_abstention_phrases_match_the_v3_harness(self):
        with open(V3_HARNESS, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "detect_abstention")
        assign = next(n for n in fn.body if isinstance(n, ast.Assign))
        self.assertEqual(ast.literal_eval(assign.value), an.V3_ABSTENTION_PHRASES)

    def test_penalty_effects_pair_the_same_items(self):
        low = [fake_row("placebo_v3", f"i{i}", "#### 2") for i in range(10)]
        high = [fake_row("placebo_v3", f"i{i}", "#### 1") for i in range(10)]
        for r in high:
            r["repetition_penalty"] = 1.05
        image = next(p for p in an.penalty_effects(low + high) if p["measure"] == "exact image")
        self.assertEqual((image["low_rate"], image["high_rate"], image["high_only"], image["low_only"]), (0.0, 1.0, 10, 0))
        self.assertEqual((image["low_penalty"], image["high_penalty"]), (1.0, 1.05))

    def test_penalty_needs_two_values(self):
        self.assertEqual(an.penalty_effects([fake_row("filler", "a", "#### 1")]), [])

    def test_solvability_pairs_the_same_problem(self):
        solved = fake_row("base_image", "a", "#### 5", y_i="5", y_t="5")
        solved["image_question"] = "problem p"
        missed = fake_row("base_text", "z", "#### 9", y_i="5", y_t="5")
        missed["text_question"] = "problem p"
        v = list(an.analyze([solved, missed], reps=10).values())[0]["solvability"]
        self.assertEqual((v["n"], v["image_rate"], v["text_rate"], v["image_only"]), (1, 1.0, 0.0, 1))

    def test_fake_model_output_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = h.RunConfig(run_tag="x", backend="echo")
            path = os.path.join(d, "x.jsonl")
            h.run_requests([h.build_request(make_item(0), "direct")], h.EchoBackend(), cfg, path, log=quiet)
            h.write_manifest(os.path.join(d, "x.manifest.json"), cfg, h.EchoBackend(), 1, [V3_HARNESS])
            with self.assertRaises(SystemExit):
                an.load_rows([path])
            self.assertEqual(len(an.load_rows([path], allow_dry_run=True)), 1)

    def test_run_without_manifest_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.jsonl")
            open(path, "w").close()
            with self.assertRaises(SystemExit):
                an.load_rows([path])

    def test_overlapping_runs_are_refused(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = h.RunConfig(run_tag="x", backend="echo")
            path = os.path.join(d, "x.jsonl")
            h.run_requests([h.build_request(make_item(0), "direct")], h.EchoBackend(), cfg, path, log=quiet)
            h.write_manifest(os.path.join(d, "x.manifest.json"), cfg, h.EchoBackend(), 1, [V3_HARNESS])
            with self.assertRaises(SystemExit):
                an.load_rows([path, path], allow_dry_run=True)


class Coding(unittest.TestCase):
    def test_kappa_known_values(self):
        self.assertAlmostEqual(sfc.cohens_kappa(["a", "b"] * 5, ["a", "b"] * 5), 1.0)
        self.assertAlmostEqual(sfc.cohens_kappa(["a", "a", "b", "b"], ["a", "b", "a", "b"]), 0.0)

    def test_allocation_respects_cap_and_total(self):
        got = sfc.allocate({"rare": 3, "mid": 50, "big": 1000}, 60)
        self.assertEqual(got["rare"], 3)
        self.assertEqual(sum(got.values()), 60)

    def _write_set(self, d, n=6, flip_scorer=False, blank=False):
        header = ["coding_id", "image_problem", "text_problem", "model_output"] + sfc.CODE_COLUMNS
        for coder in "AB":
            with open(os.path.join(d, f"{coder}.csv"), "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(header)
                for i in range(n):
                    w.writerow([f"c{i}", "x", "y", "z", "" if blank and i == 0 else "image", "no", "conflict", "text"])
        with open(os.path.join(d, "key.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["coding_id", "item_id", "arm", "stratum", "weight", "score_attempt", "score_refusal", "score_verdict", "score_stated_reliable"])
            for i in range(n):
                wrong = flip_scorer and i < n // 2
                w.writerow([f"c{i}", f"item{i}", "arm2_placebo", "s", "1.0", "text" if wrong else "image", "no", "conflict", "text"])
        return os.path.join(d, "A.csv"), os.path.join(d, "B.csv"), os.path.join(d, "key.csv")

    def test_accuracy_reports_a_planted_scorer_error(self):
        with tempfile.TemporaryDirectory() as d:
            _, r = sfc.evaluate(*self._write_set(d, flip_scorer=True))
        self.assertAlmostEqual(r["fields"]["attempted_problem"]["weighted_accuracy"], 0.5)
        self.assertAlmostEqual(r["fields"]["refused"]["weighted_accuracy"], 1.0)

    def test_rescoring_replaces_stale_labels_and_keeps_the_weight(self):
        data = [{"id": "x", "image_question": "Ducks lay eggs", "text_question": "Robes need bolts", "image_answer": "1", "text_answer": "2",
                 "arms": {"arm3_conflict": {"text": "They do not agree. I consider the text more reliable.\n\nThe robes need bolts. #### 2"}}}]
        key = {"c0": {"item_id": "x", "arm": "arm3_conflict", "weight": "3.5", "score_attempt": "stale", "score_refusal": "stale", "score_verdict": "stale", "score_stated_reliable": "stale"}}
        sfc.rescore_key(key, data)
        self.assertEqual(key["c0"]["score_verdict"], "conflict")
        self.assertEqual(key["c0"]["score_stated_reliable"], "text")
        self.assertEqual(key["c0"]["score_refusal"], "no")
        self.assertEqual(key["c0"]["weight"], "3.5")

    def test_blank_codes_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                sfc.evaluate(*self._write_set(d, blank=True))

    def test_real_sample_is_blinded_and_sized(self):
        with open(V3_RESULTS, encoding="utf-8") as f:
            data = json.load(f)
        rows = sfc.draw_sample(data, 1)
        self.assertEqual(len(rows), sum(sfc.ARM_SAMPLE.values()))
        with tempfile.TemporaryDirectory() as d:
            sfc.write_sample(data, rows, d)
            with open(os.path.join(d, "coder_A.csv"), encoding="utf-8-sig", newline="") as f:
                header = next(csv.reader(f))
            for leak in ("arm", "stratum", "weight", "score_attempt"):
                self.assertNotIn(leak, header)
            with open(os.path.join(d, "coder_A.csv"), "rb") as a, open(os.path.join(d, "coder_B.csv"), "rb") as b:
                self.assertEqual(a.read(), b.read())


if __name__ == "__main__":
    unittest.main()
