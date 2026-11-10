#!/usr/bin/env python3
"""Tests for the v5 verdict-transplant code. Needs no GPU, torch or network.

Run from Experiment/:
    python -m unittest tests.test_v5 -v

HFBackend is not covered: it needs a GPU session. Its first real check is the dev pass
in RUNBOOK_v5.md, including `harness_v5.py --print_example` against the real chat template.
"""
import json
import math
import os
import re
import sys
import tempfile
import unittest
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
sys.path.insert(0, EXPERIMENT)

import harness_v5 as h5
import score_v5 as sc
import transplant_v5 as tp

PREREG = os.path.join(os.path.dirname(EXPERIMENT), "Docs", "PREREGISTRATION_VERDICT_TRANSPLANT.md")
VISION = "<|vision_start|><|image_pad|><|vision_end|>"


def math_item():
    return h5.Item(
        id="gsm8k-1",
        source="gsm8k",
        image=None,
        image_question="Janet's ducks lay 16 eggs per day. How many does she sell?",
        text_question="A robe takes 2 bolts of blue fiber and half that much white fiber. How many bolts?",
        y_image="18",
        y_text="3",
    )


def chart_item():
    return h5.Item(
        id="cq-7",
        source="chartqa",
        image=None,
        image_question="",
        text_question="The report records a poverty rate of 14.8% in 2019.",
        y_image="11.8",
        y_text="14.8",
        image_only_question="What is the poverty rate in California in 2019?",
    )


DONOR = (
    "The image and the typed text do not agree. The typed text is about a robe, while the image is about ducks. "
    "I consider the typed text more reliable as it is a clear problem."
)


class TestLayout(unittest.TestCase):
    def render(self, regime, item, order, prefill=None):
        instr = h5.instruction(regime, "binding", 1, item.image_only_question)
        return h5.render_chat(h5.fake_qwen_chat_template, h5.build_content(regime, item, instr, order), prefill)

    def test_image_first_exact(self):
        it = math_item()
        instr = h5.instruction("math", "binding", 1)
        expected = (
            "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n"
            f"{instr}\n\nImage: {VISION}\n\nTyped text:\n{it.text_question}\n\n{h5.FORMAT_MATH}"
            "<|im_end|>\n<|im_start|>assistant\n"
        )
        self.assertEqual(self.render("math", it, "image_first"), expected)

    def test_text_first_exact(self):
        it = math_item()
        instr = h5.instruction("math", "binding", 1)
        expected = (
            "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n"
            f"{instr}\n\nTyped text:\n{it.text_question}\n\nImage: {VISION}\n\n{h5.FORMAT_MATH}"
            "<|im_end|>\n<|im_start|>assistant\n"
        )
        self.assertEqual(self.render("math", it, "text_first"), expected)

    def test_instruction_before_and_format_after_both_sources(self):
        for regime, item in (("math", math_item()), ("chartqa", chart_item())):
            fmt = h5.FORMAT_MATH if regime == "math" else h5.FORMAT_CHART
            for order in h5.ORDERS:
                text = self.render(regime, item, order)
                user = text.split("<|im_start|>user\n")[1].split("<|im_end|>")[0]
                instr = h5.instruction(regime, "binding", 1, item.image_only_question)
                self.assertTrue(user.startswith(instr), (regime, order))
                self.assertTrue(user.endswith(fmt), (regime, order))
                i_img, i_txt = user.index(VISION), user.index(item.text_question)
                self.assertEqual(i_img < i_txt, order == "image_first", (regime, order))
                self.assertLess(len(instr), min(i_img, i_txt))

    def test_only_sources_swap(self):
        """Removing the two source blocks leaves the same text in both orders."""
        it = math_item()
        a, b = self.render("math", it, "image_first"), self.render("math", it, "text_first")
        strip = lambda s: re.sub(r"\s+", " ", s.replace(f"Image: {VISION}", "").replace(f"Typed text:\n{it.text_question}", ""))
        self.assertEqual(strip(a), strip(b))

    def test_no_source_letters(self):
        for regime, item in (("math", math_item()), ("chartqa", chart_item())):
            for fam in h5.FAMILIES:
                for k in range(1, 5):
                    for order in h5.ORDERS:
                        instr = h5.instruction(regime, fam, k, item.image_only_question)
                        text = json.dumps(h5.build_content(regime, item, instr, order))
                        self.assertNotRegex(text, r"Source [AB]\b")

    def test_chartqa_headers(self):
        text = self.render("chartqa", chart_item(), "text_first")
        self.assertIn("Report:\nThe report records", text)
        self.assertIn(f"Chart: {VISION}", text)
        self.assertIn("Question: What is the poverty rate", text)

    def test_one_image_entry(self):
        for order in h5.ORDERS:
            content = h5.build_content("math", math_item(), "I", order)
            self.assertEqual(sum(c["type"] == "image" for c in content), 1)

    def test_prefill_left_open(self):
        text = self.render("math", math_item(), "image_first", prefill="I consider the image more reliable.\n\n####")
        self.assertTrue(text.endswith("<|im_start|>assistant\nI consider the image more reliable.\n\n####"))

    def test_base_text_has_no_image(self):
        self.assertFalse(h5.has_image(h5.build_base_content("math", math_item(), "base_text")))
        self.assertTrue(h5.has_image(h5.build_base_content("chartqa", chart_item(), "base_image")))


class TestTemplates(unittest.TestCase):
    def test_four_templates_each(self):
        for stems, endings in ((h5.MATH_STEMS, h5.MATH_ENDINGS), (h5.CHART_STEMS, h5.CHART_ENDINGS)):
            self.assertEqual(len(stems), 4)
            for arm in ("nonbinding", "binding", "explicit"):
                self.assertEqual(len(endings[arm]), 4)
                self.assertEqual(len(set(endings[arm])), 4)

    def test_canonical_text(self):
        self.assertEqual(
            h5.instruction("math", "binding", 1),
            "In two sentences, state whether the image and the typed text present the same problem, and say which "
            "source you consider more reliable. Then solve only the problem from the source you named as more "
            "reliable, and ignore the other problem.",
        )
        self.assertTrue(h5.instruction("math", "explicit_image", 3).endswith("Then work out only the problem from the image, and disregard the other problem."))
        self.assertTrue(h5.instruction("math", "explicit_text", 4).endswith("Then solve only the problem in the typed text, and leave the other problem aside."))
        self.assertTrue(h5.instruction("chartqa", "explicit_text", 2, "Q?").startswith("Question: Q?\nIn two sentences, say whether the chart"))
        self.assertTrue(h5.instruction("chartqa", "explicit_image", 1, "Q?").endswith("using only the chart, and ignore the other source."))

    def test_templates_match_preregistration(self):
        """Every template string is in the pre-registration verbatim ({X} written as X)."""
        with open(PREREG, encoding="utf-8") as f:
            doc = f.read()
        strings = h5.MATH_STEMS + h5.CHART_STEMS + [h5.FORMAT_MATH, h5.FORMAT_CHART]
        for endings in (h5.MATH_ENDINGS, h5.CHART_ENDINGS):
            for arm, items in endings.items():
                strings += [s.replace("{X}", "X") for s in items]
        strings += [t.replace("{X}", "X") for t in tp.PARA_TEMPLATES]
        for s in strings:
            self.assertIn(s, doc, s)

    def test_explicit_mirrors_binding(self):
        for regime, endings in (("math", h5.MATH_ENDINGS), ("chartqa", h5.CHART_ENDINGS)):
            for b, e in zip(endings["binding"], endings["explicit"]):
                self.assertEqual(b.split(",")[1:], e.split(",")[1:], (regime, b, e))

    def test_bad_template_index(self):
        with self.assertRaises(ValueError):
            h5.instruction("math", "binding", 5)


class TestStatedSource(unittest.TestCase):
    def test_labels(self):
        cases = {
            "I consider the typed text more reliable.": "text",
            "The image is more reliable than the text.": "image",
            "The more reliable source is the chart.": "chart",
            "I consider the report more reliable as it states a value.": "report",
            "The chart seems more reliable to me.": "chart",
            "It is impossible to say which source is more reliable.": "undetermined",
            "Both are equally reliable.": "undetermined",
            "They do not agree. Then I solve it.": "absent",
            "The context makes it reliable.": "undetermined",
        }
        for text, label in cases.items():
            self.assertEqual(sc.stated_reliable_source(text), label, text)

    def test_opposite(self):
        self.assertEqual(sc.opposite_source("chart", "chartqa"), "report")
        self.assertEqual(sc.opposite_source("text", "math"), "image")
        self.assertIsNone(sc.opposite_source("chart", "math"))


class TestAnswers(unittest.TestCase):
    def test_match(self):
        self.assertTrue(sc.answers_match("14.8%", "14.8"))
        self.assertTrue(sc.answers_match("18.00", "18"))
        self.assertTrue(sc.answers_match("1,000", "1000"))
        self.assertTrue(sc.answers_match("Yes.", "yes"))
        self.assertTrue(sc.answers_match("The Democrats", "democrats"))
        self.assertFalse(sc.answers_match("14.8", "11.8"))
        self.assertFalse(sc.answers_match(None, "1"))

    def test_strict(self):
        self.assertEqual(sc.extract_answer_strict("#### 14.8%"), ("14.8", "hash"))
        self.assertEqual(sc.extract_answer_strict("The chart shows 11.8.\n#### Yes"), ("yes", "hash"))
        self.assertEqual(sc.extract_answer_strict("11.8"), ("11.8", "first_line"))
        self.assertEqual(sc.extract_answer_strict("The chart shows 11.8 in 2019. So it is 11.8."), (None, "none"))
        self.assertEqual(sc.extract_answer_strict("####"), (None, "none"))

    def test_behavioural_math_rejects_fallback(self):
        src, ans, method = sc.behavioural_source("so the answer is 18", "math", "18", "3")
        self.assertEqual((src, ans, method), ("neither", None, "fallback_last_number"))
        self.assertEqual(sc.behavioural_source("2+1=3\n#### 3", "math", "18", "3")[0], "text")

    def test_candidate_text(self):
        self.assertEqual(h5.candidate_text("18.0"), "18")
        self.assertEqual(h5.candidate_text("2.50"), "2.5")
        self.assertEqual(h5.candidate_text("Yes"), "Yes")


class TestMargin(unittest.TestCase):
    def test_log_softmax(self):
        lp = sc.log_softmax([1.0, 2.0, 3.0])
        self.assertAlmostEqual(sum(math.exp(x) for x in lp), 1.0, places=12)
        self.assertAlmostEqual(lp[2] - lp[0], 2.0, places=12)

    def test_positions(self):
        self.assertEqual(sc.continuation_positions(3, 5), [(2, 3), (3, 4)])
        with self.assertRaises(ValueError):
            sc.continuation_positions(5, 5)

    def test_continuation_logprob_on_mock_logits(self):
        # Vocabulary of 4; sequence [0, 1, 2, 3]; prefix length 2, so tokens 2 and 3 are scored.
        logits = [[0, 0, 0, 0], [0.0, 1.0, 3.0, 0.0], [2.0, 0.0, 0.0, 1.0], [9, 9, 9, 9]]
        total, n = sc.continuation_logprob(logits, [0, 1, 2, 3], 2)
        expect = sc.log_softmax(logits[1])[2] + sc.log_softmax(logits[2])[3]
        self.assertEqual(n, 2)
        self.assertAlmostEqual(total, expect, places=12)

    def test_leading_whitespace_token_is_not_scored(self):
        self.assertEqual(sc.leading_ws_skip([" ", "1", "8"]), 1)
        self.assertEqual(sc.leading_ws_skip([" 18"]), 0)  # space merged into the answer token
        self.assertEqual(sc.leading_ws_skip(["1", "8"]), 0)
        self.assertEqual(sc.leading_ws_skip([" "]), 0)  # never skip the only token
        # Sequence [0, 1, 2, 3], prefix length 2; token 2 is the space, so only token 3 is scored.
        logits = [[0, 0, 0, 0], [0.0, 1.0, 3.0, 0.0], [2.0, 0.0, 0.0, 1.0], [9, 9, 9, 9]]
        total, n = sc.continuation_logprob(logits, [0, 1, 2, 3], 2, skip=1)
        self.assertEqual(n, 1)
        self.assertAlmostEqual(total, sc.log_softmax(logits[2])[3], places=12)

    def test_margin_sign_and_normalisation(self):
        # Image: -2.0 over 2 tokens (-1.0 each); text: -3.0 over 1 token.
        self.assertAlmostEqual(sc.margin(-2.0, 2, -3.0, 1), 2.0)
        self.assertGreater(sc.margin(-1.0, 1, -5.0, 1), 0)  # positive favours the image
        with self.assertRaises(ValueError):
            sc.margin(-1.0, 0, -1.0, 1)


class TestMinimalEdit(unittest.TestCase):
    def test_swap_math(self):
        self.assertEqual(tp.swap_sources("I consider the typed text more reliable.", "math")[0], "I consider the image more reliable.")
        self.assertEqual(tp.swap_sources("The image is more reliable than the text.", "math")[0], "The typed text is more reliable than the image.")
        self.assertEqual(tp.swap_sources("Image beats text.", "math")[0], "Typed text beats image.")

    def test_swap_chart(self):
        self.assertEqual(tp.swap_sources("The report is more reliable than the chart.", "chartqa")[0], "The chart is more reliable than the report.")

    def test_article_repair(self):
        out, fixes = tp.swap_sources("A text is less reliable than an image.", "math")
        self.assertEqual(out, "An image is less reliable than a typed text.")
        self.assertEqual(fixes, 2)

    def test_variants_math(self):
        v = tp.make_variants(DONOR, "math")
        self.assertTrue(v.ok, v.reason)
        self.assertEqual((v.own_source, v.flip_source), ("text", "image"))
        self.assertTrue(v.texts["flip"].endswith("I consider the image more reliable as it is a clear problem."))
        self.assertEqual(v.texts["none"], DONOR.rsplit(" I consider", 1)[0])
        self.assertEqual(sc.stated_reliable_source(v.texts["para"]), "text")
        self.assertEqual(sc.stated_reliable_source(v.texts["para_flip"]), "image")
        # para and para_flip share every sentence but the last, which differs only in the source noun.
        p, pf = tp.sentences(v.texts["para"]), tp.sentences(v.texts["para_flip"])
        self.assertEqual(p[:-1], pf[:-1])
        self.assertEqual(p[-1].replace("the typed text", "X"), pf[-1].replace("the image", "X"))
        # Everything outside the reliability sentence is untouched.
        self.assertEqual(tp.sentences(v.texts["flip"])[:2], tp.sentences(DONOR)[:2])

    def test_para_template_differs_from_original(self):
        v = tp.make_variants("The image and the typed text differ. I consider the typed text more reliable.", "math")
        self.assertTrue(v.ok, v.reason)
        self.assertEqual(v.para_template, 1)  # template 0 equals the original sentence
        self.assertTrue(v.texts["para"].endswith("The typed text seems more reliable to me."))

    def test_variants_chart(self):
        v = tp.make_variants("The chart and the report disagree. I consider the report more reliable.", "chartqa")
        self.assertTrue(v.ok, v.reason)
        self.assertEqual(v.texts["flip"], "The chart and the report disagree. I consider the chart more reliable.")

    def test_rejections(self):
        self.assertEqual(tp.make_variants("They do not agree. I will solve the text.", "math").reason, "own_absent")
        self.assertEqual(tp.make_variants("I cannot tell which is more reliable.", "math").reason, "own_undetermined")
        two = "The text is more reliable. The image is less reliable."
        self.assertEqual(tp.make_variants(two, "math").reason, "multiple_reliability_sentences")
        self.assertEqual(tp.make_variants("I consider the report more reliable.", "math").reason, "own_wrong_regime")

    def test_jaccard_gate(self):
        self.assertAlmostEqual(tp.jaccard("typed text is reliable", "image is reliable"), 2 / 5)
        v = tp.make_variants("Typed text is reliable.", "math")
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "gate3_jaccard")
        self.assertLess(v.jaccard_flip, tp.JACCARD_MIN)

    def test_multiset_jaccard_sees_what_sets_miss(self):
        # Both nouns also occur in the first sentence, so the set version is 1.0.
        v = tp.make_variants(DONOR, "math")
        self.assertEqual(v.jaccard_flip, 1.0)
        self.assertLess(v.jaccard_multiset_flip, 1.0)
        self.assertEqual(v.changed_flip, 2)  # "typed text" -> "image"
        self.assertEqual(tp.changed_tokens("a b c", "a b c"), 0)

    def test_swap_count_gate(self):
        one = tp.make_variants("The image and the typed text differ. I consider the typed text more reliable.", "math")
        self.assertTrue(one.ok, one.reason)
        self.assertEqual(one.n_swaps, 1)
        two = tp.make_variants("The image and the typed text differ. I consider the image more reliable as it shows the content of the image.", "math")
        self.assertTrue(two.ok, two.reason)
        self.assertEqual(two.n_swaps, 2)
        three = tp.make_variants("The image and the typed text differ. The text is more reliable than the image because the image is blurry.", "math")
        self.assertFalse(three.ok)
        self.assertEqual(three.reason, "gate3_too_many_swaps")
        self.assertGreater(three.n_swaps, tp.MAX_SWAPS)

    def test_grammar_gate_ignores_model_wording(self):
        self.assertTrue(tp.grammar_ok("The image and the typed text are similar.", "The image and the typed text are similar."))
        self.assertFalse(tp.grammar_ok("The image are reliable.", "The text is reliable."))


class TestCells(unittest.TestCase):
    def variants(self):
        v = tp.make_variants(DONOR, "math")
        return {o: v for o in h5.ORDERS}

    def test_grid(self):
        reqs = tp.build_cells(math_item(), "math", self.variants(), beh_k=[1])
        score = [r for r in reqs if r.mode == "score"]
        beh = [r for r in reqs if r.mode == "generate"]
        self.assertEqual(len(score), 2 * 12 * 4)
        self.assertEqual(len(beh), 2 * 12)
        self.assertEqual(len({r.key for r in reqs}), len(reqs))
        self.assertTrue(all(r.prefill.endswith("####") for r in score))
        explicit = [r for r in reqs if r.cell["family"].startswith("explicit")]
        self.assertTrue(explicit and all(r.cell["verdict"] == "none" for r in explicit))
        flip = next(r for r in score if r.cell["verdict"] == "flip")
        self.assertEqual(flip.cell["named_source"], "image")
        self.assertIn("I consider the image more reliable", flip.prefill)

    def test_behaviour_prefill(self):
        self.assertEqual(tp.behaviour_prefill("V.", "math"), "V.\n\n")
        self.assertEqual(tp.behaviour_prefill("V.", "chartqa"), "V.\n\n####")
        self.assertIsNone(tp.behaviour_prefill("", "math"))
        self.assertEqual(tp.score_prefill(""), "####")


class TestPipelineDryRun(unittest.TestCase):
    def test_end_to_end_with_echo_backend(self):
        items = [
            h5.Item(id=f"gsm8k-{i}", source="gsm8k", image=None, image_question=f"Q{i}", text_question=f"T{i}", y_image=str(i + 10), y_text=str(i))
            for i in range(1, 7)
        ]
        cfg = h5.V5Config(run_tag="t", backend="echo")
        backend = h5.EchoBackend()
        with tempfile.TemporaryDirectory() as d:
            base_path, donor_path, out_path = (os.path.join(d, n) for n in ("b.jsonl", "d.jsonl", "o.jsonl"))
            h5.run(h5.base_requests(items, "math"), backend, cfg, base_path, log=lambda *_: None)
            h5.run(h5.donor_requests(items, "math"), backend, cfg, donor_path, log=lambda *_: None)
            competent = {it.id for it in items}  # echo answers are random; force all in
            donors = tp.load_donor_verbalizations(donor_path, cfg.model_id)
            reqs, gates, passed = tp.plan(items, "math", competent, donors, "dev", 250, 42, [1])
            self.assertEqual(gates["passed"], len(passed))
            self.assertEqual(len(passed), len(items), gates)
            self.assertEqual(len(reqs), len(passed) * 120)
            h5.run(reqs, backend, cfg, out_path, log=lambda *_: None)
            self.assertEqual(h5.report_missing(reqs, out_path), 0)
            def count():
                with open(out_path, encoding="utf-8") as f:
                    return sum(1 for _ in f)
            n = count()
            self.assertEqual(h5.run(reqs, backend, cfg, out_path, log=lambda *_: None), 0)  # resume writes nothing
            self.assertEqual(count(), n)
            with open(out_path, encoding="utf-8") as f:
                rows = [json.loads(l) for l in f]
            dl = [r for r in rows if r["outcome"] == "dl"]
            self.assertTrue(all(isinstance(r["dl"], float) for r in dl))
            self.assertEqual({r["order"] for r in rows}, set(h5.ORDERS))

    def test_confirm_takes_seeded_competent(self):
        items = [h5.Item(id=f"x{i}", source="gsm8k", image=None, image_question="q", text_question="t", y_image="1", y_text="2") for i in range(20)]
        donors = {(it.id, o): DONOR for it in items for o in h5.ORDERS}
        competent = {f"x{i}" for i in range(0, 20, 2)}
        _, g1, p1 = tp.plan(items, "math", competent, donors, "confirm", 4, 42, [1])
        _, g2, p2 = tp.plan(items, "math", competent, donors, "confirm", 4, 42, [1])
        self.assertEqual((g1["competent"], g1["taken"]), (10, 4))
        self.assertEqual(p1, p2)
        self.assertTrue(set(p1) <= competent)

    def test_competency_uses_strict_parsing(self):
        row = {"family": "base_image", "regime": "math", "y_image": "18", "y_text": "18", "full_text": "it is 18"}
        self.assertFalse(h5.base_correct(row))
        row["full_text"] = "16-3-4=9, 9*2=18\n#### 18"
        self.assertTrue(h5.base_correct(row))


class TestStages(unittest.TestCase):
    def test_base_stage_has_generation_and_gold_score_rows(self):
        reqs = h5.base_requests([math_item()], "math")
        self.assertEqual(sorted(r.key for r in reqs), ["base_image", "base_text", "nll|base_image", "nll|base_text"])
        score = [r for r in reqs if r.mode == "score"]
        self.assertTrue(all(r.prefill == "####" and r.cell["outcome"] == "nll" for r in score))
        self.assertEqual([r.uses_image for r in score], [True, False])

    def test_score_rows_do_not_count_toward_competency(self):
        self.assertFalse(h5.base_correct({"family": "base_image", "regime": "math", "y_image": "18", "y_text": "3", "lp_image": -1.0}))

    def test_donor_stage_adds_free_binding_rows(self):
        reqs = h5.donor_requests([math_item()], "math")
        fams = [r.cell["family"] for r in reqs]
        self.assertEqual(fams.count("donor"), 2)
        self.assertEqual(fams.count("free_binding"), 2)
        self.assertEqual(len({r.key for r in reqs}), 4)
        binding = next(r for r in reqs if r.cell["family"] == "free_binding")
        self.assertIn(h5.MATH_ENDINGS["binding"][0], binding.content[0]["text"])
        self.assertTrue(all(r.prefill is None for r in reqs))

    def test_donor_loader_ignores_free_binding_rows(self):
        cfg = h5.V5Config(run_tag="t", backend="echo")
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "d.jsonl")
            h5.run(h5.donor_requests([math_item()], "math"), h5.EchoBackend(), cfg, path, log=lambda *_: None)
            donors = tp.load_donor_verbalizations(path, cfg.model_id)
        self.assertEqual(set(donors), {("gsm8k-1", o) for o in h5.ORDERS})


class TestChartQASet(unittest.TestCase):
    def rows(self, n=230, same_answer=()):
        return [
            h5.item_from_chartqa_row(
                {"conflict_id": i, "image": None, "text_report": f"report {i}", "question": f"q{i}",
                 "chart_answer": "7" if i in same_answer else str(1000 + i), "report_answer": "7" if i in same_answer else str(5000 + i)}
            )
            for i in range(n)
        ]

    def test_pinned_release_gives_229_without_item_45(self):
        kept = h5.chartqa_analysis_set(self.rows())
        self.assertEqual(len(kept), 229)
        self.assertEqual(len(kept), h5.CHARTQA_ANALYSED_ITEMS)
        self.assertNotIn("45", {it.id for it in kept})
        self.assertEqual({it.id for it in kept}, {str(i) for i in range(230)} - {"45"})
        self.assertEqual(len(h5.distinct(kept)), 229)  # distinct() removes nothing further

    def test_wrong_row_count_is_refused(self):
        with self.assertRaises(SystemExit):
            h5.chartqa_analysis_set(self.rows(229))
        with self.assertRaises(SystemExit):
            h5.chartqa_analysis_set(self.rows(231))

    def test_missing_excluded_item_is_refused(self):
        rows = [r for r in self.rows(231) if r.id != "45"]  # 230 rows, but id 45 is absent
        with self.assertRaises(SystemExit):
            h5.chartqa_analysis_set(rows)

    def test_equal_answer_pair_breaks_the_count(self):
        with self.assertRaises(SystemExit):
            h5.chartqa_analysis_set(self.rows(same_answer={3}))

    def test_unpinned_revision_is_filtered_but_not_counted(self):
        kept = h5.chartqa_analysis_set(self.rows(60), pinned=False)
        self.assertEqual(len(kept), 59)
        self.assertNotIn("45", {it.id for it in kept})

    def test_dev_and_confirm_sizes(self):
        kept = h5.chartqa_analysis_set(self.rows())
        dev = h5.h4.split_phase(kept, "dev", 30)
        confirm = h5.h4.split_phase(kept, "confirm", 30)
        self.assertEqual((len(dev), len(confirm)), (30, 199))
        self.assertFalse({it.id for it in dev} & {it.id for it in confirm})


class TestConfig(unittest.TestCase):
    def args(self, **kw):
        base = dict(run_tag="t", model_id="Qwen/Qwen2-VL-2B-Instruct", model_revision=None, dataset_revision=None, split="chartqa",
                    phase="dev", dev_size=None, batch_size=8, max_pixels=1, seed=42, limit=None, dry_run=True)
        base.update(kw)
        return SimpleNamespace(**base)

    def test_chartqa_dev_size_default_and_guard(self):
        cfg = h5.config_from_args(self.args(), "base")
        self.assertEqual(cfg.dev_size, 30)
        self.assertEqual(cfg.model_revision, h5.MODEL_PINS["Qwen/Qwen2-VL-2B-Instruct"])
        with self.assertRaises(SystemExit):
            h5.config_from_args(self.args(dev_size=200), "base")
        self.assertEqual(h5.config_from_args(self.args(split="conflict"), "base").dev_size, 200)


if __name__ == "__main__":
    unittest.main()
