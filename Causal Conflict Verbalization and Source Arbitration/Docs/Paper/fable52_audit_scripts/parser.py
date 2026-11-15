import sys, json, os, re
from collections import Counter
EXP = r"D:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\Experiment"
sys.path.insert(0, EXP)
import score_v5 as sc, score_v4 as v4
R = os.path.join(EXP, "results_v5")
pat = sc._MATH_FINAL_ANSWER
for m in ("qwen25","qwen25_7b"):
  for stage in ("tp","base"):
    n=0; meth=Counter(); kw=Counter(); trailing=0; cap=Counter(); ex=[]; disagree_lenient=0
    for l in open(os.path.join(R, f"v5dev_conflict_{stage}_{m}.jsonl"), encoding="utf-8"):
        r=json.loads(l)
        if "full_text" not in r: continue
        n+=1
        t=r["full_text"]
        src,ans,method=sc.behavioural_source(t,"math",r["y_image"],r["y_text"],parser="structured")
        meth[method if ans is not None else method+"(None)"]+=1
        if method=="structured_final_answer":
            ms=list(pat.finditer(t)); last=ms[-1]
            w=re.search(r"answer|number|result|total|boxed", last.group(0), re.I).group(0).lower(); kw[w]+=1
            tail=t[last.end():]
            if len(re.findall(r"\d", tail))>=3 and len(tail)>60:
                trailing+=1
                if len(ex)<3: ex.append((last.group(0), tail[:160].replace("\n"," / ")))
            cap[bool(r.get("hit_cap"))]+=1
            la,_=v4.extract_answer(t)
            if la is not None and not sc.answers_match(la, ans): disagree_lenient+=1
    print(m, stage, "gen rows", n, dict(meth)); print("   structured keyword of last match:", dict(kw), "| digits continue after match:", trailing, "| hit_cap:", dict(cap), "| structured != last-number:", disagree_lenient)
    for e in ex: print("     EX:", e)
