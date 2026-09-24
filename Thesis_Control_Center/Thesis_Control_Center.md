# Thesis Control Center

**Status:** Topic discovery (do not treat a candidate as chosen)  
**Purpose:** Single source of truth for my undergraduate CSE thesis. Prevents research conversations on different AI platforms from becoming disconnected or contradictory.

The four platform projects are workbenches, not separate sources of truth. Any decision that changes my direction must be recorded here before it is treated as final.

---

## Researcher profile and constraints

- Final-year BSc CSE student, strongest in AI/ML, deep learning, Transformers/LLM basics, Python, and web/API development.
- I can learn a small amount of a new domain, but I do not have reliable supervision in medicine, pharmacy, nanotechnology, or electronics.
- Preferred thesis work: AI/CSE-heavy; public or accessible data; reproducible experiments; a clear baseline; measurable contribution; feasible within undergraduate time and compute constraints.
- Compute: Google Colab Pro for GPU. Local desktop: Ryzen 5 5600G, 8 GB RAM, integrated graphics. Avoid projects requiring local GPU, large paid APIs, private hospital access, wet labs, or custom hardware.
- Goal: an honest, finishable thesis that also strengthens AI/ML engineering and research skills.

---

## Candidate topic pool

Explore without forcing any domain:

1. Federated learning, privacy, and non-IID learning.
2. Healthcare AI, only where data, validation, and domain dependence are manageable.
3. Multimodal/VLM systems and trustworthy VLMs.
4. LLM systems: evaluation, retrieval, hallucination, inference efficiency, or machine unlearning.
5. Pharmaceutical/nanomedicine AI only if the problem is data-driven and does not require deep specialist supervision.

---

## Non-negotiable topic filter

Reject or substantially narrow any candidate that fails two or more of these:

- Clear research question and a defensible gap, not merely “apply model X to dataset Y.”
- Public/accessible dataset with legal, practical access and an understandable data schema.
- A baseline that I can reproduce on Colab Pro.
- Evaluation metrics that directly test the proposed claim.
- Scope suitable for one student and a university thesis timeline.
- No dependency on clinical partnership, wet lab, paid data/API, or unavailable expert annotation.
- A contribution that survives comparison against a simple, strong baseline.

---

## Required output format for every research task

1. Direct answer in 3–8 bullets.
2. Evidence table: claim | evidence/source | confidence | limitation.
3. Recommendation: continue, narrow, park, or reject.
4. Next smallest action: one task that can be completed in 30–90 minutes.
5. Decision-log entry when the task changes topic direction.

Use primary sources for technical claims: original papers, official dataset documentation, benchmark leaderboards/repositories, and official framework documentation. Clearly label assumptions, inferences, and uncertain claims. Include direct links and publication dates for research claims.

---

## Anti-overwhelm rules

- Work on one candidate topic per chat.
- Do not request a full literature review before passing feasibility screening.
- Do not retain a vague “interesting” topic without a dataset, baseline, evaluation plan, and stated risk.
- No more than five active candidates at once.
- End each session by updating the Decision Log and naming the next action.
- Do not let a model invent novelty. Verify purported gaps against recent primary research.

---

## Platform roles

| Platform   | Primary role                                                                 | Do not use it as                                      |
|------------|------------------------------------------------------------------------------|-------------------------------------------------------|
| Perplexity | Discovery, current literature, datasets, labs, official links, citation verification | Final judge of novelty or feasibility                |
| Claude     | Long-paper reading, synthesis across uploaded reports, argument critique, outline refinement | Main source for time-sensitive facts without checking sources |
| ChatGPT    | Research strategy, method design, experimental planning, implementation support, structured decision-making | A place to keep unrecorded final decisions           |
| Kimi       | Secondary independent review, long-context cross-check, alternative framing  | The sole source of evidence                           |

---

## Discovery workflow

1. Perplexity: discover papers, datasets, benchmarks, and terminology for one candidate.
2. Claude: read 3–6 key papers and make a structured synthesis, including methods and limitations.
3. ChatGPT: turn evidence into a narrowed research question, minimum viable experiment, baselines, metrics, compute plan, and risk register.
4. Kimi: independently challenge the gap and identify hidden complexity, data issues, and stronger baselines.
5. Control Center: record the verdict. Only then proceed, park, or reject.

---

## Topic scorecard

Score 1 (weak) to 5 (strong). A candidate needs at least 25/35 and no score below 3 in Feasibility or Evaluation.

| Criterion                        | Score | Notes/evidence |
|----------------------------------|-------|----------------|
| Problem clarity                  |       |                |
| Evidence of a real gap           |       |                |
| Dataset access and quality       |       |                |
| Feasibility on Colab Pro         |       |                |
| Baselines and evaluation         |       |                |
| Domain-dependence risk           |       |                |
| Career/research value            |       |                |
| **Total / 35**                   |       |                |

---

## Decision Log

| Date       | Candidate                  | Verdict | Evidence-based reason                          | Next action                          |
|------------|----------------------------|---------|------------------------------------------------|--------------------------------------|
| 2026-08-20 | Thesis topic exploration   | Active  | Broad search phase; no topic frozen.           | Screen candidates using the scorecard. |

---

## After a topic is frozen

Create **Thesis Specification v1** by replacing the Candidate Topic Pool with:

- Working title and research question.
- Problem setting and boundaries.
- Dataset(s), access status, and data risks.
- Proposed method and explicit non-contributions.
- Reproducible baseline list.
- Evaluation metrics, ablations, and success criteria.
- Compute budget, timeline, and fallback plan.
- Core paper list (10–15 papers) with one-line relevance notes.

Do not change this specification casually. Put proposed changes in the Decision Log first, then update the versioned specification.

---

## Project setup checklist

- Create a project named **Thesis | Topic Discovery** in ChatGPT, Claude, Perplexity, and Kimi.
- Paste the platform-specific instruction into each project.
- Upload this file to each project as its first reference file.
- Keep only this file plus essential short references during discovery: no paper dump.
- Create one chat per candidate, named `Candidate — <short name>`.
- At the end of every useful chat, copy its decision-log entry back into this document.
