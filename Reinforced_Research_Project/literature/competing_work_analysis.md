# Competing-work analysis (Phase 4)

**Method.** The search was targeted and repeated for 2015–2026. It covered:

- Crossref queries restricted to ACA, Talanta, CILS, J. Chemometrics, Applied Spectroscopy and JNIRS;
- the arXiv API;
- web search.

Every record listed in `updated_literature_matrix.csv` was verified through Crossref, the arXiv API, or the record's landing page. Content statements are limited to retrieved abstracts or theorem text. ScienceDirect full texts returned HTTP 403, so several Elsevier abstracts were not retrieved; such items are marked in the matrix.

## 1. The closest competitors and what they leave open

### Conformal inference engines

**Barber et al. 2021 (jackknife+).** Coverage of at least 1−2α holds for any symmetric fitting algorithm under exchangeability. This is TJ+'s engine. Nothing in the transfer instantiation is new theory. What remains open:

- which part of a deployed chemometric pipeline must be refitted;
- whether the guarantee survives realistic sampling of the standards;
- whether simpler practice already suffices.

**Lee, Barber & Willett 2026 (hierarchical conformal / hierarchical jackknife+).** This is the decisive prior art for the batch extension. Leave-one-group-out refits with 1/N_k-weighted member scores give coverage of at least 1−2α for an observation from a *new* group, under hierarchical exchangeability. A batch-level transfer jackknife+ is therefore an instantiation (TJ+H), not a new method. Left open:

- whether lot structure *matters* for transferred spectroscopic calibrations, i.e. how large the intra-lot error correlation is after PDS or SBC;
- what it implies for the number of lots that must be sampled;
- how established laboratory practice (Gaussian LOO, random-effects tolerance intervals) behaves.

**Dunn, Wasserman & Ramdas 2023; Mallick et al. 2026.** These are alternative group-level constructions, and Mallick et al. covers partially observed test groups. They are cited as alternatives. The partially observed case is relevant when routine samples come from a lot that already supplied standards; E10 measures it as "same-batch coverage".

### Shift-aware and transfer-oriented conformal methods

**Tibshirani et al. 2019 (weighted CP); Prinster et al. 2022 (JAWS).** Both are covariate-shift corrections. The instrument changes the relation between spectrum and property, which violates the covariate-shift assumption. The original benchmark shows that WCP-S fails or becomes uninformative.

**Doula 2026 (conformal calibration transfer).** This is the closest *named* competitor. It transports labelled source calibration data through unlabelled paired observations, for classification, with an assumption-dependent coverage slack. Our setting differs: it is regression, the standards are labelled, and an exact jackknife+ bound applies.

**Khairbek 2026.** This is independent evidence, from reflectance spectroscopy in classification, that domain shift destroys conformal coverage. It supports the motivation of RQ1.

### Chemometric uncertainty quantification

**Jovic 2025; Duma et al. 2026; Sun, Cui & Qiao 2026 (preprint).** These apply conformal or conformal-inspired intervals in NIR/MIR regression **within one instrument**. None treats transfer. Sun et al. is the only chemometric CV+ use found.

**Classical PLS uncertainty.** This line includes Olivieri et al. 2006 (IUPAC), Bouckaert et al. 2011 and Chiappini et al. 2025 (bootstrap, ACA). These methods are parametric or resampling-based and in-distribution. Two competitors a chemometric reviewer would expect were missing from the original benchmark and are added in E11:

- **bootstrap intervals (Boot-T);**
- **re-estimated ASTM-type intervals (ASTM-T).**

**SBC as a regression problem.** SBC is an ordinary least-squares regression of y on f(x). The textbook prediction interval (OLS-PI) is the obvious parametric competitor; it was absent from the original benchmark and is added in E11.

### Analytical-validation tradition

**Mee 1984; Hubert et al. 2004; Rozet et al. 2012.** In method validation, β-expectation tolerance intervals equal prediction intervals (Rozet et al. 2012). Multi-batch β-expectation limits are derived from a one-way random-effects model (Mee 1984). This gives (i) the language for presenting conformal marginal coverage to analytical chemists and (ii) a classical batch-level competitor (ANOVA-PI, added to E10).

### Calibration-transfer literature

**Wang et al. 1991, Workman 2018 and the 2025–2026 ACA/CILS transfer papers.** These evaluate point accuracy (RMSEP, bias). **Haggam et al. 2026 (CILS review)** explicitly lists the lack of uncertainty-aware validation schemes as an open problem. **Yıldırım 2026 (Zenodo preprint)** proposes a dimensionless transfer-penalty ratio with GUM propagation, without intervals or coverage.

## 2. Verdict

- **Validity of prediction intervals after calibration transfer.** No prior study gives finite-sample-valid regression intervals for transferred spectroscopic calibrations, and none measures how conventional intervals fail. This is an absence finding of moderate confidence; grey literature and non-English sources are not excluded.
- **Leave-one-batch-out (hierarchical) jackknife+.** It is established (Lee et al. 2026). The reinforced paper therefore claims no new conformal methodology. It claims:
  - **(i)** the empirical characterisation of validity loss after transfer;
  - **(ii)** the correct instantiation (which step to refit, how to normalise with T²/Q);
  - **(iii)** **real-lot evidence** on the unit of exchangeability of transfer standards, and the design rule that follows from it;
  - **(iv)** a fair comparison with the classical procedures an analytical laboratory would actually use.
