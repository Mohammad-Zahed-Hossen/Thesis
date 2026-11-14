# OpenResearch Prompt — Pre-Freeze Exhaustive Literature Audit (2026-11-15)

> Paste everything below the line into OpenResearch. It has direct read access to this repository and to alphaXiv, OpenAlex, PubMed and bioRxiv search tools.
> Written 2026-11-15 by Claude Code from the repo state at commit `157c694`.

---

## 0. Your role and the one-sentence job

You are a research auditor for an undergraduate BSc CSE thesis that is **about to freeze its pre-registration** (git tag `prereg-v5`). Your job is to find **every paper that bears on this thesis** — especially any that would **break its novelty boundary, change a design decision, or be demanded by an examiner** — verify each one from primary text, and leave behind a durable, machine-readable literature map plus a **research-objective brief** that any future AI agent can read first before touching the project.

You are a skeptical research partner, not a cheerleader. A paper that kills the novelty claim is the **most valuable** thing you can find. Report it plainly.

---

## 1. Read these first (in this order) — do not skip

All paths are relative to the repo root `D:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\`.

1. `CLAUDE.md` — project rules, invariants, verified constants, claim boundaries. **Binding on you.**
2. `Experiment/README.md` — current status and next steps.
3. `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` — the design spec. Read §1 (estimand), **§1.1 Novelty boundary** (the exact claim you are stress-testing), §2 (hypotheses, decision table), §4–§7 (prompts, minimal-edit gates, outcomes, analysis), §11 (deviation log).
4. `Docs/Paper/README.md` and `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md` — the existing 18 core papers + CMC-Bench + 2 Ch. 2 leads (§0 inventory, §2 matrix, §4 design rules, §5 checklist).
5. `Docs/Paper/post-v5-pdf-audit/post-v5-pdf-audit.md`, `Docs/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md`, `Docs/Paper/prereg-freeze-audit/prereg-freeze-audit.md` — earlier audits (know what was already checked and how).
6. Skim the code only to confirm what the design actually does: `Experiment/harness_v5.py` (`build_content`, prompt templates), `Experiment/transplant_v5.py` (minimal-edit verdict flips and gates), `Experiment/score_v5.py`, `Experiment/analyze_v5.py`.

**Trust rules (from `CLAUDE.md`):** every `.md` in `Docs/` is AI-generated and is *not* ground truth — including the knowledge base. Ground truth is the code, the `results_v*/` data, and the PDFs in `Docs/Paper/*.pdf`. If a doc contradicts a PDF or the code, the PDF/code wins and you log the discrepancy.

---

## 2. What the thesis actually claims (so you know what to search against)

**Working title:** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict.*

**Core manipulation.** A VLM sees an image and a typed text that support different answers. We **prefix-force** a reliability verdict into the model's *own* assistant turn ("I consider the image / the typed text more reliable"), using a **minimal edit** of the model's own verbalization (only the source noun phrase swapped; token Jaccard ≥ 0.85), with a **matched paraphrase pair** (`para` / `para_flip`) as wording control. We measure whether the subsequent answer follows the verdict.

**Controls and factors.** Evidence order counterbalanced (`<image><text>` vs `<text><image>`, instruction fixed, no "Source A/B" letters); a **binding** instruction arm ("solve only the problem from the source you named…") vs non-binding; **explicit single-source ceilings** (`explicit_image` / `explicit_text`) to normalise effects (ρ = CDE / ceiling); **competency conditioning** (only items solvable from each source alone); greedy decoding, repetition penalty 1.0, pinned revisions.

**Estimand.** A **controlled direct effect** of the verdict at a fixed instruction — never "mediation" or "natural indirect effect".

**Outcomes.** GSM8K/SVAMP (task-selection conflict, confirmatory): behavioural choice shift ΔP(Y=T) at template k=1, `para_flip − para` co-primary; teacher-forced `####` log-likelihood margin Δℓ is secondary. ChartQA-Conflict (evidence conflict, exploratory): Δℓ primary. Equivalence via TOST at ε = 5.0 pp; wording-floor gate.

**Models.** Qwen2.5-VL-3B and -7B (confirmatory), Qwen2-VL-2B (diagnostic). Stimuli from Ghosh et al., *Which Source Wins?* (arXiv:2608.17205).

**Novelty boundary (verbatim intent of prereg §1.1).** No prior study (a) intervenes on a VLM's *own stated source-reliability verdict* by **assistant-turn prefix-forcing** a minimally edited version of it with a matched-template control, (b) measures whether the answer follows **under image–text conflict with counterbalanced order**, and (c) tests whether a **binding instruction** changes that effect. Your job is to try hard to falsify each of (a), (b), (c) — separately and in combination.

---

## 3. Already covered — do not re-audit these, but DO use them as snowball seeds

The 19 core sources + 2 leads already in `Docs/Paper/`:
2608.17205, 2610.33841, 2610.19407, 2609.06704, 2609.26986, 2610.38296, 2607.27304, 2604.14888, 2511.02243, 2503.02199, 2504.08974, 2602.14518, 2606.28273, 2505.23945, 2603.01437, 2510.27484, 2307.13702, 2609.25366, CMC-Bench (MAGMaR 2026, `2026.magmar-main.3`), 2606.22862, and Smith 2026 (OpenReview `uul4iRQSJ2`, PDF not available).

**Known gaps — found earlier (2026-11-09) but never entered into the knowledge base. Audit these first:**

| arXiv | What was noted | Why it may matter |
|---|---|---|
| 2609.00550 | *Same Semantics* — rendered-text vs typed-text preference unstable and order-dependent | Directly about our stimulus format (rendered image of a problem vs typed problem) and order |
| 2507.01790 | Hua et al. — router heads in Qwen2.5-VL-7B | Mechanistic modality arbitration in one of our exact models |
| 2604.09364 | Nooralahzadeh — arbitration failure, activation patching | Causal intervention on modality arbitration; novelty-adjacent |
| 2510.11196 | Moll — medical CoT faithfulness via input perturbation, LLM judge, no prefill | Faithfulness method contrast |
| 2605.27773 | Text-only, correlational — CoT near-identical across opposite decisions | "Stating ≠ choosing" precedent |
| 2305.04388 | Turpin et al. — unfaithful CoT explanations (biasing features) | Classic citation an examiner will expect; not in KB |
| 2511.19199 | CLASH — cross-modal contradiction detection benchmark | Was in topic-selection archive; re-check relevance |

Verify each ID resolves to the paper described (the 2026-11-09 notes came from page extracts, not full text).

---

## 4. Search plan

### 4.1 Tool routing

- **alphaXiv** — primary for arXiv CS/ML. Use `discover_papers` for semantic queries, `get_paper_content` / `answer_pdf_queries` to read full text and verify claims, and the researcher tools to check other papers by key authors.
- **OpenAlex** — venue-published work not on arXiv (ACL Anthology, CVPR/ICCV/ECCV, NeurIPS/ICML/ICLR proceedings, TMLR, workshops), **citation graph** (forward citations of anchor papers, references of anchor papers), and author disambiguation.
- **PubMed / bioRxiv** — only for the *cognitive-science* and *medical-VLM* angles (§4.2 axis H and part of axis G). Do not pad the audit with off-topic biomedical papers.

Record every query you run (tool, exact string, date filter, number of hits, number screened) in the search log (§6). A search that returned nothing useful is still logged. Do not infer novelty from an empty search — say "not found by queries X, Y, Z" instead.

### 4.2 Search axes (run all; queries are starting points — expand them)

**A. Direct novelty threats (highest priority).**
- "prefix forcing" / "prefill" / "assistant turn injection" + vision-language / multimodal
- "intervene on chain of thought" / "edited reasoning" / "counterfactual rationale" + VLM / MLLM
- "stated reliability" / "verbalized source preference" / "self-reported modality preference" + causal
- "does the model follow its own explanation" / "explanation-action consistency" + multimodal
- "verbalized confidence steering" / "self-consistency of stated beliefs" in VLMs
- "binding instruction" / "act on your judgment" / "commit-then-answer" prompting

**B. Image–text / cross-modal conflict and modality preference.**
- "modality conflict", "cross-modal inconsistency", "text bias in VLMs", "blind faith in text", "visual vs textual evidence", "modality following", "source arbitration", "knowledge conflict multimodal", "typographic attack" (only where it concerns rendered vs typed text conflict), "rendered text vs typed text", "OCR text in image vs prompt text"

**C. CoT faithfulness methodology (text-only and multimodal).**
- "chain-of-thought faithfulness", "early answering", "adding mistakes to CoT", "paraphrased reasoning", "counterfactual simulatability", "causal mediation analysis of reasoning", "post-hoc rationalization", "unfaithful explanations", "CoT monitoring", "reasoning trace intervention", "thought anchors", "resampling reasoning"

**D. Ordering, position and instruction effects in multimodal prompts.**
- "evidence order effect VLM", "position bias multimodal", "recency bias image text", "instruction position", "noncommutativity of evidence", "label bias A/B multiple choice"

**E. Measurement / statistics that the design relies on.**
- Teacher-forced log-likelihood margins as preference measures; length-normalised log-odds; TOST equivalence testing in ML evaluation; sign-flip / permutation tests for paired LLM evaluations; paraphrase / wording noise floors; competency or "solvable-from-both" conditioning.

**F. Mechanistic work on modality arbitration in Qwen-VL family.**
- "Qwen2.5-VL" + "attention heads" / "activation patching" / "steering vector" / "modality routing"; "logit lens multimodal"; "visual token contribution".

**G. Applied neighbours an examiner may raise.**
- Multimodal RAG with conflicting evidence; document/chart QA under counterfactual reports (ChartQA-Conflict lineage); medical VLM faithfulness and conflict; sycophancy toward user-provided text in VLMs; "self-attribution" effects when the model's own text is edited.

**H. Cognitive-science grounding (PubMed / bioRxiv; keep short, 3–8 papers max).**
- Human cue integration and source reliability weighting (Bayesian cue combination, visual–verbal conflict); choice-blindness / confabulated reasons (verbal report vs decision). Only include papers that would actually be cited in a Ch. 2 paragraph.

### 4.3 Date window and snowballing

- Main window: **2022-01 to 2026-11-15**, with **exhaustive coverage of 2026-05 → 2026-11** (newest preprints are the most likely novelty threats and are least likely to be in the KB).
- Classic pre-2022 papers only if they are foundational and an examiner would expect them.
- **Snowball both ways** from the eight anchor papers (2607.27304, 2608.17205, 2610.33841, 2610.19407, 2609.06704, 2609.26986, 2610.38296, 2604.14888): all references (backward) and all citing papers (forward, via OpenAlex and alphaXiv). Then one more hop from any new paper you grade A.
- Check other recent papers by the anchor authors (Bhowal, Ghosh, Dassen, Barua, Menzat, Li, Assefa, Sánchez Villegas).

### 4.4 Stopping rule

Stop when (i) every axis has been searched with at least 4 distinct queries on at least 2 tools, (ii) two consecutive snowball hops add no new A/B papers, and (iii) every A paper has been read in full text. If you hit a tool or budget limit first, say exactly which axes and hops are incomplete.

---

## 5. Screening, grading and verification

### 5.1 Grades

- **A — Must cite / may threaten novelty or change a design decision.** Read full text. Fill the full extraction schema.
- **B — Should cite in Ch. 2 related work.** Read abstract + method + key results. Fill the short schema.
- **C — Background / borderline.** One-line note.
- **X — Screened out.** One-line reason (kept in the log so nobody re-screens it).

### 5.2 Novelty-threat rating (A and B papers)

For each of the three novelty components — (a) prefix-forcing the model's *own* source verdict with minimal edit + matched control, (b) under image–text conflict with counterbalanced order, (c) binding-instruction contrast — rate the paper: **overlaps / partial / none**, with a one-sentence justification and page/section citation. A paper with "overlaps" on any component, or "partial" on two or more, is a **novelty threat** and goes at the top of the report with a proposed rewording of prereg §1.1.

### 5.3 Extraction schema (A papers)

```
id / venue / year / authors / URL
access: [Full text read] | [Abstract only] | [PDF not available]
task + stimuli
models (exact names; flag any Qwen2-VL / Qwen2.5-VL)
manipulation (what exactly is intervened on; prompt vs prefix vs activation)
conflict type (image–text / text–text / parametric–context / none)
order counterbalanced? (yes/no/not reported)
outcome measure(s) + metric
key numeric result(s) with table/figure + page
statistical method (CIs, permutation, TOST, etc.)
novelty threat: (a) __ (b) __ (c) __  + justification
design implication for this thesis (concrete: which prereg section, what would change)
verbatim quote (≤ 25 words, with page) supporting the key claim
```

### 5.4 Verification rules

- Every numeric claim and every quote must come from the paper's text you actually read, with page/table. If you only saw an abstract, tag it `[Abstract only]` and do not report numbers beyond the abstract.
- Tag every claim **[Verified] / [Inferred] / [Hypothesis] / [Unknown]**.
- **Never invent a paper, ID, author, venue or number.** If an ID does not resolve, say so. arXiv IDs in this project are 2026-era (`26xx.xxxxx`); double-check each one resolves to the stated title.
- Check the existing KB's §2 matrix for errors as you go; if a core paper's description is wrong, log it under "KB corrections".
- Watch for the known traps listed in `CLAUDE.md` → *Literature checks* (e.g. *Which Source Wins?* tested 2B and 7B, not 3B; the +16.7/+15.0 pp order effect is natural-image VQA; "larger models less faithful" is Lanham, not Turpin; Dassen et al. do not prefix-force).

---

## 6. Deliverables (write all of these; create folder `Docs/Paper/lit-audit-2026-11-15/`)

1. **`lit-audit-2026-11-15.md` — the audit report.**
   - §0 Executive summary: number screened / A / B / C / X; **novelty verdict** (intact / needs narrowing / broken) with the evidence; top 5 design implications.
   - §1 Novelty threats (A papers that overlap or partially overlap), each with proposed rewording of prereg §1.1.
   - §2 A-paper spec sheets (schema §5.3).
   - §3 B-paper table (id, venue, one-line relevance, which thesis chapter/section cites it).
   - §4 Design implications mapped to prereg sections and invariants (order, binding, minimal edit, competency, outcomes, TOST/ε, wording floor). For each: *keep / change / add limitation*, with source. **Do not edit the prereg yourself.**
   - §5 KB corrections (errors found in existing `Docs/Paper/*.md`).
   - §6 Coverage and limitations: axes/hops not completed, tools that failed, paywalled papers.
2. **`search_log.csv`** — columns: `date, tool, axis, query, filters, hits, screened, kept_A, kept_B`.
3. **`papers.csv`** — one row per screened paper: `id, title, first_author, year, venue, url, grade, axis, access, threat_a, threat_b, threat_c, one_line_relevance, cited_by_anchor, cites_anchor`.
4. **`references.bib`** — BibTeX for all A and B papers (verified metadata only).
5. **`RESEARCH_OBJECTIVE.md` — put this one at the repo path `Docs/RESEARCH_OBJECTIVE.md`.** A 1–2 page brief that any future AI agent reads first. Contents:
   - The research question in one sentence and the estimand (controlled direct effect).
   - H₁ / H₀ / binding question in plain language (from prereg §2), and what each outcome would mean.
   - The **defensible novelty claim after this audit**, worded conservatively, with the 5–8 closest papers and how this thesis differs from each (one line each).
   - Claim boundaries (what must never be claimed — copy from `CLAUDE.md` and add any new ones the audit justifies).
   - The 10–15 papers a newcomer must read, in reading order, with one line on why.
   - Open questions the literature does not answer and that this thesis can (and cannot) answer.
   - Pointers: prereg, KB, this audit, `Experiment/README.md`. Date-stamp it and mark it AI-generated, verified against the PDFs listed.
6. **Download** open-access PDFs of new A papers into `Docs/Paper/` using the existing naming convention (`<arxiv_id>.pdf`), and list any you could not get. Do not download B/C papers.
7. **Update** `Docs/Paper/README.md` (inventory table and counts) and add an §-level entry to `THESIS_LITERATURE_KNOWLEDGE_BASE.md` pointing to the new audit. Keep the counts consistent everywhere you touch them (`CLAUDE.md` states "18 core papers + CMC-Bench; 20 local PDFs" — if your audit changes those numbers, list every file that states them so the author can update them; do not edit `CLAUDE.md` yourself).

---

## 7. Hard constraints

- **Read-only on the design.** Do not edit `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`, `CLAUDE.md`, any `Experiment/*.py`, tests, or anything in `Experiment/results_*/` or `coding_*/`. Propose changes in the audit report instead.
- **Do not touch the confirm split or run any model.** No confirmatory data exists and none may be generated.
- **Do not commit or tag.** Leave changes uncommitted for the author to review.
- **No "first"/"novel" language** beyond what the evidence supports; always phrase novelty as "within the N papers screened by queries listed in `search_log.csv`".
- **Copyright:** quotes ≤ 25 words each; summarise, do not reproduce.
- **Privacy:** do not put the author's name, email or repo paths into any external search query.
- **Shared memory:** your memory folder is junctioned to Claude Code's (`...\.claude\projects\D--Thesis-Important\memory\`). If you save a memory, check for an existing file first, keep `MEMORY.md` one line per file, and add one note pointing to `Docs/RESEARCH_OBJECTIVE.md` and the audit folder.

---

## 8. Final message to the author

End with a short chat summary: novelty verdict (one line), count of A/B papers found that were **not** already in the KB, the single most dangerous paper (if any) with its link, the top 3 recommended prereg changes, and what you could not cover. Keep it under 200 words; everything else lives in the files.
