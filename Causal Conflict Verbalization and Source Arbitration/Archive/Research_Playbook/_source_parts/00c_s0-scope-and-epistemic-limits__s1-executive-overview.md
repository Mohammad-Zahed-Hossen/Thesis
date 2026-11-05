## 0. Scope and epistemic limits

I studied the retained workspace: the context and handover documents, the rejected/parked-field report, the VLM and Bengali-VLM exploration folders, the multimodal-agent and medical-imaging audits, four canonical proposals, the adversarial audits, the locked specification, the pilot code, the raw result files (JSON/CSV), the statistical suite, and the analysis reports. **[L2]**

Three limits follow directly from that evidence base:

1. **No Git history.** The repository was never committed, so chronology is reconstructed from content, cross-references, filenames, and experiment provenance — not from authorship timestamps.
2. **Retrospective documents are claims, not confirmation.** Several "canonical," "final," and "100% complete" reports restate earlier conclusions. A conclusion repeated in five documents is still one conclusion. This manual treats repetition as a process signal, not as replication.
3. **The conversation history is incomplete.** Where this playbook describes what you did in earlier sessions, it is an inference from surviving artifacts. Those inferences are marked **[L2]**, and I do not claim access to exchanges I cannot see.

One citation that appears in the workspace (`arXiv:2608.17205`, *"Which Source Wins?"*) could not be verified from a primary source when I checked it. Treat it as **[Unknown]** until you open the paper yourself. That is not a project failure; it is exactly the check this playbook formalizes in §12 and §13.

---

## 1. Executive overview

A strong researcher is not primarily someone who has read the most papers. They are someone who can:

- notice when a phenomenon is real versus a measurement artifact;
- hold two explanations at once and design the observation that separates them;
- estimate whether a question is answerable *before* spending months on it; and
- change the question when the evidence demands it.

The process is a loop, not a pipeline:

```text
research area
   ↓
concrete observation or failure
   ↕                      literature map
   ↕                      claims and mechanisms
   ↕                      competing explanations
   ↕                      closest existing experiments
   ↕                      a candidate question
   ↕                      feasibility, data, baselines
   ↓
minimum discriminating experiment
   ↓
evidence (including surprises)
   ↺  narrow / broaden / add control / change metric / pivot / kill
```

Only when the loop stops producing new information does it become a project:

```text
frozen question
 → hypotheses with opposite predictions
 → variables, controls, dataset, baselines, metrics
 → pilot
 → main experiment
 → ablations and robustness
 → analysis
 → interpretation
 → contribution
 → thesis → paper
```

**Central operating rule [L3]:** instead of asking "what is novel?", ask "what observation would change what we believe, and what is the smallest honest experiment that could produce it?"

Five questions to keep visible (printable form in Appendix C):

1. What exactly did I observe, and could my measurement have produced it?
2. What mechanism do the closest papers claim?
3. What alternative explanation would produce the same observation?
4. What result would separate the alternatives?
5. What would we know afterwards that we do not know now?

If question 4 cannot be answered in one sentence, you do not yet have a research question. You have a research area. **[L3]**
