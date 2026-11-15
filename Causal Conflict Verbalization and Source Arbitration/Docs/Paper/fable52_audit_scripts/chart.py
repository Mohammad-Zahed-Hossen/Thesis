import sys, json, os
from collections import Counter
EXP = r"D:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\Experiment"
sys.path.insert(0, EXP)
import score_v5 as sc
R = os.path.join(EXP, "results_v5")
for m in ("qwen2","qwen25","qwen25_7b"):
    c=Counter(); miss=[]
    for l in open(os.path.join(R, f"v5dev_chartqa_base_{m}.jsonl"), encoding="utf-8"):
        r=json.loads(l)
        if "full_text" not in r: continue
        gold = r["y_image"] if r["family"]=="base_image" else r["y_text"]
        ans, method = sc.extract_answer_strict(r["full_text"])
        ok = sc.answers_match(ans, gold)
        c[(r["family"], ok)] += 1
        if not ok and r["family"]=="base_image": miss.append((gold, r["full_text"][-60:].replace("\n"," / "), method, r.get("hit_cap")))
    print(m, dict(c))
    for x in miss[:20]: print("   gold=%r out=%r %s cap=%s" % x)
