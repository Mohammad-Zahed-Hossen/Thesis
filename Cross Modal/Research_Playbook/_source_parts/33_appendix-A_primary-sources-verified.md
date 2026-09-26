---

# Appendix A: primary sources used

Every external claim in this playbook that concerns a specific paper is anchored below. All were opened at their primary arXiv record during preparation of this document (24 September 2026). Claims about general research practice that are not tied to one of these sources are labeled synthesis/recommendation **[L3]**.

| # | Source (primary record) | Used in this playbook for |
|---|---|---|
| 1 | Turpin, Michael, Perez, Bowman. *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* [arXiv:2305.04388](https://arxiv.org/abs/2305.04388) (NeurIPS 2023) | Illustrating unfaithful rationalization under input biasing in **text** models; the shape of the faithfulness question; its multimodal transfer as an open design gap (§12.5, §7.7) |
| 2 | Popordanoska, Li, Blaschko. *CLASH: A Benchmark for Cross-Modal Contradiction Detection.* [arXiv:2511.19199](https://arxiv.org/abs/2511.19199) | Example of a contradiction **detection** benchmark (controlled object/attribute contradictions, MCQ and open-ended, fine-tuning gains, reported modality biases); used to show why detection ≠ arbitration (§5.4, §6.3, §7.6, §12.5) |
| 3 | Liu et al. *More Thinking, Less Seeing? Assessing Amplified Hallucination in Multimodal Reasoning Models.* [arXiv:2505.21523](https://arxiv.org/abs/2505.21523) | Example of a behavioral phenomenon (longer chains ↔ reduced visual grounding) with RH-AUC/RH-Bench as a length–perception metric, plus attention analysis as a proposed mechanism (§5.4, §12.5) |
| 4 | Hasani et al. *Uncovering Grounding IDs: How External Cues Shape Multimodal Binding.* [arXiv:2509.24072](https://arxiv.org/abs/2509.24072) | Example of a mechanism claim supported by representation analysis plus causal intervention; used to distinguish binding from arbitration and to illustrate how mechanism claims are argued (§12.5, §4.2) |
| 5 | Traub et al. *Overcoming Common Flaws in the Evaluation of Selective Classification Systems.* [arXiv:2407.01032](https://arxiv.org/abs/2407.01032) | Replaces a widely used metric (AURC) with AUGRC because current metrics fail stated requirements, changing rankings on 5 of 6 datasets — the model case for **measurement-validity** contributions (§20.3, §22.3) |
| 6 | Schaeffer, Miranda, Koyejo. *Are Emergent Abilities of Large Language Models a Mirage?* [arXiv:2304.15004](https://arxiv.org/abs/2304.15004) | The canonical example of a "phenomenon" that depends on metric choice (discontinuous vs continuous), tested on published outputs — the model for a cheap, decisive metric audit (§5.4, §18.3, §22.3) |
| 7 | Gebru et al. *Datasheets for Datasets.* [arXiv:1803.09010](https://arxiv.org/abs/1803.09010) | Standard for documenting dataset motivation, composition, collection, preprocessing, uses, distribution, and maintenance; used for data-provenance discipline (§9.3, §17.1) |
| 8 | Henderson et al. *Deep Reinforcement Learning that Matters.* [arXiv:1709.06560](https://arxiv.org/abs/1709.06560) | Evidence that variance and reporting practice make results hard to interpret, with recommendations for significance metrics and tighter experimental reporting (§20.5, §25.4) |
| 9 | Pineau et al. *Improving Reproducibility in Machine Learning Research (NeurIPS 2019 Reproducibility Program).* [arXiv:2003.12206](https://arxiv.org/abs/2003.12206) | Code-submission policy, reproducibility challenge, and ML reproducibility checklist: the basis for `PROTOCOL.md`, pinned revisions, seeds, and archived raw outputs (§19.6, §24.5, §25.4) |

### A.1 Citation that could not be verified

The workspace's locked specification cites **`arXiv:2608.17205`, "Which Source Wins?"**, as reporting modality dominance under legibility degradation. I could not verify this identifier against a primary record during preparation, so it is marked **[Unknown]** in this playbook. **Action [L3]:** open the paper directly and record its manipulation, measurement, and population in the Evidence Ledger before relying on the claim. If it cannot be found, remove the citation and rebuild the "anchor literature" paragraph from verified sources. This is the single most consequential verification task remaining in the current project.

### A.2 Evidence standard applied

- Primary records (arXiv listings with version history, official proceedings) were used for every paper-specific statement above.
- No paper, author, dataset, or repository in this playbook was invented; where a claim could not be traced, it was labeled **[Unknown]** or omitted.
- Statements about your own project come from the retained files listed in Appendix B, not from memory or summary.
- General methodological advice that is not attributable to a specific source is labeled **[L3]** synthesis.
