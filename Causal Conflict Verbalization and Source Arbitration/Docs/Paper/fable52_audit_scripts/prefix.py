import sys, json, os
EXP = r"D:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\Experiment"
sys.path.insert(0, EXP)
import harness_v5 as h5
R = os.path.join(EXP, "results_v5")
for f in ("v5dev_conflict_base_qwen25.jsonl","v5dev_chartqa_base_qwen25.jsonl"):
    seen={}
    for l in open(os.path.join(R,f),encoding="utf-8"):
        r=json.loads(l); seen[r["id"]]=(h5.candidate_text(r["y_image"]) if r["family"]=="base_image" or True else None, h5.candidate_text(r["y_text"]))
    # base rows carry both golds
    n=len(seen); pre=sum(1 for a,b in seen.values() if a!=b and (a.startswith(b) or b.startswith(a))); dif=sum(1 for a,b in seen.values() if len(a)!=len(b))
    print(f, "items", n, "one candidate is a string-prefix of the other:", pre, "| different char length:", dif)
