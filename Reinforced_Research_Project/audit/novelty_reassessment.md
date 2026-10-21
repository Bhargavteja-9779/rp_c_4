# Independent scientific re-evaluation and novelty reassessment (Phases 2 and 4)

## 1. Independent assessment (Phase 2; original claims set aside)

| # | Question | Answer from the evidence |
|---|---|---|
| 1 | What question does the work actually answer? | Whether prediction intervals for a calibration moved to another instrument or season keep their nominal coverage, and how to obtain valid intervals from the transfer standards alone. |
| 2 | What new knowledge does it establish? | (a) **Empirical:** source-calibrated intervals (ASTM-type, source split conformal, covariate-shift-weighted conformal) lose most of their coverage after transfer. This is quantified on 3 data sets and 4 pipelines, and is new in a regression/transfer setting. (b) **Methodological:** where the transfer step is refitted inside a leave-one-standard-out loop, the guarantee of Barber et al. (2021) applies. This is an instantiation, not new theory. |
| 3 | What does the method do that established methods do not? | Compared with source-based intervals, it calibrates on the deployed pipeline. Compared with split conformal on the standards, it does not discard half of them. Compared with Gaussian LOO intervals, it carries a distribution-free guarantee. |
| 4 | Is the difference meaningful? | **Against source-based intervals: yes** (coverage 0.03–0.76 → about 0.90). **Against split standards: yes** for m ≤ 15. **Against Gaussian LOO intervals: marginal** at 90% (rank 2.17 vs 2.52, p = 0.11); it matters at 95% (14/40 under-covering). |
| 5 | Type of contribution | Methodological application plus empirical benchmark. No new theory. |
| 6 | New finding or a known result reproduced? | The validity of TJ+ under random standards is **a known result** (a corollary of Barber et al. Thm. 1). The original benchmark's "0/40 under-covering" therefore verifies the implementation; it is not a discovery. The new findings are the failure of conventional intervals and the boundaries (drift, Kennard–Stone, conditional coverage). |
| 7 | Does the evidence support the scope of the claims? | Mostly, but the claim of usefulness "for transferred NIR calibrations" in general rests on random standards. Real transfer standards come from few lots, measured at one time. That condition was **never tested**. |
| 8 | Would the paper remain valuable without the performance gain? | Partly. The negative result on conventional intervals stands on its own. TJ+N's efficiency gain over Gauss-LOO is already absent. |
| 9 | Can the contribution be stated in 2–3 sentences? | Yes: "Source-domain uncertainty statements fail after calibration transfer. Refitting only the transfer step in a leave-one-standard-out loop gives finite-sample-valid intervals from the standards the transfer already requires." It is short because it is narrow. |
| 10 | Would a sceptical editor see a substantial article? | Borderline. The risk is "a known conformal method applied to a chemometric pipeline, validated where validity is guaranteed". |
| 11 | Could a simpler method answer the question? | Partly. Gaussian LOO intervals answer it at 90%. For SBC, the textbook OLS prediction interval was **not tested** at all. |
| 12 | **Strongest legitimate rejection argument** | "The guarantee holds only if transfer standards are a random sample of the future routine samples. In practice they are a few lots, chosen by design and measured at standardisation time. That is exactly where the paper offers no evidence. Where the guarantee holds, simple Gaussian or regression intervals perform as well." |

**Bottom line.** Implementation effort and benchmark breadth are high, but the scientific contribution is narrower than the manuscript implies. The most valuable unexploited asset is the batch structure in the mango data. It allows the study to answer a question that matters to every laboratory that transfers calibrations: **what is the unit of exchangeability for transfer standards, and how many distinct lots must they span for an uncertainty statement to hold for future lots?**

## 2. Novelty stress test (Phase 4)

The searches were performed by a dedicated prior-art pass with records verified through Crossref and arXiv; details are in `literature/competing_work_analysis.md`.

| Stress question | Verdict | Evidence |
|---|---|---|
| Is the main contribution already known? | **The inference engine, yes:** jackknife+ (Barber et al. 2021), and the batch-level version, the hierarchical jackknife+ (Lee, Barber & Willett 2026, Thm. 5, 1−2α for a new group). **Its use for calibration transfer, no:** no paper with coverage-valid regression intervals after PDS/DS/SBC was found. | Searches: Crossref (ACA, Talanta, CILS, J. Chemom., Appl. Spectrosc., JNIRS), arXiv, web. The closest are Doula 2026 (classification, unlabelled pairs) and Khairbek 2026 (classification, empirical coverage loss under spectral shift). Haggam et al. 2026 (CILS review) names "uncertainty-aware validation schemes" as a gap. |
| Does the method introduce a new principle? | No. | — |
| Is it only a combination of established components? | Yes (jackknife+ + transfer algorithm + normalised scores). | — |
| Is it mainly an application? | Yes, a methodological application with an empirical benchmark. | — |
| Is the claimed gap supported by primary evidence? | Yes, for interval validity after transfer (absence finding of moderate confidence). | — |
| Are the differences from prior work material? | Against chemometric UQ practice, yes. Against conformal theory, no. | — |
| Can they be shown experimentally? | Yes, and they were for source-based intervals. **Not yet** for realistic standard sampling. | — |
| Would removing the claimed novelty invalidate the paper? | Removing "new method" does not; the empirical findings carry the paper. | — |

## 3. Decision on the path

Two paths are combined; Paths C and D are rejected.

- **Path B (reformulate).** The contribution is restated as a **question about the validity of uncertainty statements for transferred calibrations**, with TJ+ as the reference construction. The headline question becomes: *under what sampling of transfer standards does a finite-sample uncertainty statement hold for future routine samples, and which construction should be used in each case?* No new conformal theory is claimed. The batch-level construction is presented as an instantiation of the hierarchical jackknife+ of Lee et al. (2026) for the transfer step, plus a simpler max-score variant (TJ+G) with its own short proof.
- **Path A (strengthen with a previously unproven property).** The experiments E10–E13 are designed to establish:
  1. **Real-batch evidence:** whether sample-level intervals (including TJ+N) under-cover samples from new lots when the standards come from few lots, and why (ICC of target errors).
  2. **A design rule:** the number of distinct lots K, not the number of standards m, controls whether a bounded, valid interval for new lots exists (K ≥ 9 at 90%). Spreading the standards one per lot makes ordinary TJ+ valid for new lots.
  3. **The simpler-method challenge:** OLS-PI for SBC, Boot-T, ASTM-T, and the random-effects ANOVA-PI for new batches.
  4. **Positive statistical evidence:** non-inferiority, training-conditional reliability, and scenario-clustered CIs.
- **Path C (redesign) — rejected.** No evidence that the method itself is deficient where its assumptions hold.
- **Path D (change direction) — rejected.** The gap is real; the problem is the scope of evidence, which is fixable with available data.

**Risk acknowledged in advance.** If E10 shows that batch effects after transfer are negligible in these data, the reformulated question still has an answer ("sample-level TJ+ is robust to lot structure here, and here is the ICC that explains why"). However, the contribution would then rest more heavily on the classical-competitor and statistical reinforcement.
