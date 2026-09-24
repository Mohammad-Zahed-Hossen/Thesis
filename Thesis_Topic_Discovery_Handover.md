# Thesis Topic Discovery Handover

## Purpose

I am a final-year CSE student seeking one feasible undergraduate AI/CSE thesis topic. I am **not** asking an AI to defend a preselected field, produce fashionable keywords, or give a generic application idea. I need help discovering and validating a researchable problem and the resources needed to study it.

## The key principle

Use the same standard for every field and candidate. Do not reject a direction simply because related work, a benchmark, or a baseline already exists. Those assets may make an undergraduate empirical contribution possible.

A thesis does not need a new model or algorithm. It can make a valid contribution by answering a precise, consequential question through a trustworthy experiment using existing models and public data.

## What I am trying to find

A candidate must contain all of the following:

1. **A concrete problem or failure mode** that matters beyond a generic local application.
2. **A specific, testable research question**, with competing possible explanations.
3. **Public, legal, accessible data** that can support an honest evaluation.
4. **Open models and reproducible baselines** that can be run before proposing anything new.
5. **A leakage-resistant split or evaluation protocol.** For example, group related samples, recordings, documents, templates, source items, or generated variants together.
6. **Direct metrics and simple strong baselines.** The experiment must show whether an apparent gain is caused by a shortcut such as length, source, template, generator identity, or preprocessing.
7. **A useful outcome even without a new best score.** A robust negative result can be valuable if it rules out a plausible explanation or shows when a method does not transfer.

## Feasibility constraints

- Final-year undergraduate scope, roughly 3–4 months.
- Google Colab Pro is the main compute resource.
- Public data and open-source models only.
- No private data, paid APIs, field deployment, clinical access, major manual annotation, or dependence on specialist-domain supervision.
- The work must be an AI/CSE research contribution, not a product build.
- Prefer an inference-first or lightweight-adaptation project. Full pretraining or expensive model development is unrealistic.

## What to reject

Reject a candidate when it is only one of these:

- a chatbot, RAG system, agent, dashboard, or application;
- generic classification, OCR, object detection, or fine-tuning for a local setting;
- a claim of novelty based only on a local language, region, or dataset;
- a method whose test data, labels, license, baseline, or compute path cannot be verified;
- a project where the expected result is merely “model X scored higher than model Y.”

Do **not** reject a candidate merely because it is an empirical evaluation, replication, benchmark audit, robustness study, or analysis using existing methods. Judge whether its question and evaluation design add evidence that the closest work does not already provide.

## Required reasoning from the AI

For each serious candidate, provide:

- exact technical problem;
- what closest work already establishes;
- the remaining uncertainty that the proposed experiment could answer;
- dataset access, license, labels, sample structure, and split risks;
- minimum reproducible baseline and simple comparison baselines;
- metrics, controls, and ablations;
- realistic Colab compute plan;
- what a meaningful positive result, negative result, and failure would look like;
- a clear verdict: **proceed to pilot**, **reserve**, or **reject**, with evidence.

Use primary papers, official dataset pages, and official code/model repositories for decisive claims. Clearly label what is verified, inferred, or unknown. Do not call a research gap “solved” merely because adjacent papers exist.

## Decision rule

The immediate goal is not to select a final thesis title by argument alone. It is to identify the best candidate for a short, bounded pilot that can verify data access, baseline reproduction, split validity, and whether the core question survives simple controls.

Recommend one candidate only when it is materially stronger than the alternatives under the same standard. Otherwise, recommend the single most informative pilot rather than another broad topic search.
