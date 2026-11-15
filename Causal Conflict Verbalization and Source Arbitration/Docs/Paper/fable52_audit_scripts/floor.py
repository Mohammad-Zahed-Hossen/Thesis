import sys, json, os, re
from collections import Counter
EXP = r"D:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\Experiment"
sys.path.insert(0, EXP)
import analyze_v5 as an, score_v5 as sc, transplant_v5 as tp
R = os.path.join(EXP, "results_v5")
A = json.load(open(os.path.join(R, "analysis_dev", "analysis_v5.json")))
for r in A["results"]:
    if r["regime"] != "math": continue
    print("==", r["model_id"], "n_items", r["n_items"], "n_analysed", r["n_analysed"], "bm", r["boundary_mismatch_rows"])
    bp = r["behaviour_primary"]
    for k in ("T2_beh","T2_beh_pair","T3_beh"):
        t = bp["decision_tests"][k]; print(" ", k, round(t["effect"],3), [round(x,3) for x in t["effect_ci90"]], t["reading"], "bench", round(t.get("benchmark",0),3))
    print("  T1_beh", {k: round(v,4) if isinstance(v,float) else v for k,v in bp["T1_beh_did"].items()})
    print("  primary:", r["primary_reading_binding"][:160]); print("  primary nb:", r["primary_reading_nonbinding"][:160])
    for fam in ("binding","nonbinding"):
        w = r[f"behaviour_{fam}"]["wording_floor_para_minus_own"]
        print("  floor", fam, {k: (round(v,3) if isinstance(v,float) else v) for k,v in w.items() if k in ("n","signed_mean","churn_rate","neither_shift","any_change_rate_diagnostic","floor_ok","tost_power_at_this_noise")})
    sec = r["secondary"]
    print("  per-order dl:", {k: round(v["mean"],3) for k,v in sec.items() if k.startswith("cde_") and k.endswith("_first")})
    print("  verdict_nll:", sec.get("verdict_nll_mean_by_verdict"), "manip:", {k:(v["answer_follows_stated_verdict"], v["attributable_answers"]) for k,v in sec.get("manipulation_check",{}).items()})
    print("  by_parser neither:", {p: round(v["neither_rate"],3) for p,v in r["behaviour_by_parser"].items()})
# churn anatomy
for m in ("qwen25","qwen25_7b"):
    rows = an.load_rows([os.path.join(R, f"v5dev_conflict_tp_{m}.jsonl")])
    beh = an.behaviour_table(rows, parser="structured")
    ids = an.item_ids(rows)
    for fam in ("nonbinding","binding"):
        n = fl = 0; tmpl = Counter(); gen_verdict = 0; multi = Counter(); lenratio=[]; methods=Counter(); cap=0
        for i in ids:
            for o in ("image_first","text_first"):
                x, y = beh.get((i,fam,"own",o)), beh.get((i,fam,"para",o))
                if not (x and y): continue
                if x["src"] in ("image","text") and y["src"] in ("image","text"):
                    n += 1
                    if x["src"] != y["src"]:
                        fl += 1
                        own_pref, para_pref = x["row"]["prefill"], y["row"]["prefill"]
                        tmpl[y["row"]["para_template"]] += 1
                        lenratio.append((len(own_pref), len(para_pref)))
                        # does the generated continuation after para restate a verdict?
                        gen = y["row"]["full_text"][len(para_pref):]
                        if re.search(r"\breliable\b", gen[:400], re.I): gen_verdict += 1
                        methods[(x["method"], y["method"])] += 1
                        cap += bool(y["row"].get("hit_cap") or x["row"].get("hit_cap"))
                        multi[f"{o}:own={x['row']['own_source']}:{x['src']}->{y['src']}"] += 1
        print(m, fam, f"attributable {n}, flips {fl} ({fl/n:.3f}); para templates {dict(tmpl)}; para continuation restates verdict {gen_verdict}; hit_cap {cap}; methods {dict(methods)}")
        print("    transitions", dict(multi)); print("    prefill chars own->para", lenratio)
