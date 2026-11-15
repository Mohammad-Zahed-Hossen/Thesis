import sys, json, re, os
from collections import Counter
EXP = r"D:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\Experiment"
sys.path.insert(0, EXP)
import harness_v5 as h5, transplant_v5 as tp, score_v5 as sc
R = os.path.join(EXP, "results_v5")
def rows(p):
    with open(os.path.join(R, p), encoding="utf-8") as f:
        for l in f:
            yield json.loads(l)
for split, regime in (("conflict", "math"), ("chartqa", "chartqa")):
    for m in ("qwen2", "qwen25", "qwen25_7b"):
        base = os.path.join(R, f"v5dev_{split}_base_{m}.jsonl")
        comp = {p: h5.competent_ids(base, parser=p) for p in sc.MATH_PARSERS}
        ys = {}
        donors = {}
        for r in rows(f"v5dev_{split}_donor_{m}.jsonl"):
            ys[r["id"]] = (r["y_image"], r["y_text"])
            if r.get("family") == "donor":
                donors[(r["id"], r["order"])] = sc.split_verbalization(r["full_text"])[0]
        gp = f"v5dev_{split}_tp_{m}.gates.json"
        old = json.load(open(os.path.join(R, gp)))
        oldp = set(old["passed_ids"])
        passed, reasons = [], Counter()
        empty_none = 0; ncells = 0; dbl = 0; rel_leak = 0
        for i in sorted(comp["structured"]):
            vs = {o: tp.make_variants(donors[(i, o)], regime, y_image=ys[i][0], y_text=ys[i][1]) for o in h5.ORDERS if (i, o) in donors}
            bad = [v.reason for v in vs.values() if not v.ok]
            if bad or len(vs) < 2:
                reasons.update(bad); continue
            passed.append(i)
            for v in vs.values():
                ncells += 1
                if not v.texts["none"]: empty_none += 1
                if re.search(r"\b(image image|typed text typed text|report report|chart chart|typed image|image text)\b", v.texts["flip"], re.I): dbl += 1
                a, b = v.verdict_chars["own"]; sent = v.texts["own"][a:b]
                if tp._has_answer_leakage(sent, *ys[i]): rel_leak += 1
        print(f"{split:8s} {m:10s} competent strict/structured/lenient = {len(comp['strict'])}/{len(comp['structured'])}/{len(comp['lenient'])} | stored gates: competent {old['competent']} passed {old['passed']} | current code: passed {len(passed)} (rate {len(passed)/max(1,len(comp['structured'])):.2f}) reasons {dict(reasons)} | stored-passed not passing now: {len(oldp-set(passed))}, new: {len(set(passed)-oldp)} | cells {ncells}: empty m_none {empty_none}, doubled-noun flips {dbl}, answer inside reliability sentence {rel_leak}")
