# Topic discovery and selection (Phases 1–2, 4)

Target journal fixed first: *Analytica Chimica Acta* (chemometric methodology demonstrating new principles). Constraints from the environment: 4 CPU cores, 15 GB RAM, no GPU, public data only.

## 15 candidate directions (internal screening)

| # | Direction | Data | Main risk(s) | Verdict |
|---|---|---|---|---|
| 1 | **Distribution-free prediction intervals for spectroscopic calibrations after calibration transfer / model update** | Corn (3 instruments), IDRC Shootout 2002 tablets (2 instruments), Mango DMC (4 seasons) | Must differentiate from jackknife+ (Barber 2021), Jovic 2025, Duma 2025, Doula 2026 (ICML) | **SELECTED** (see stress test) |
| 2 | New standard-free calibration-transfer algorithm | Corn, tablets | Crowded field (uDOP, filter learning, UCT-LMIR, di-PLS); improvements are often incremental and dataset-specific | Rejected: incremental |
| 3 | Deep learning vs PLS benchmark on NIR | Mango, tablets | Already benchmarked (Mishra 2022 review; Walsh 2024); gives no new principle | Rejected |
| 4 | Data augmentation for cross-instrument CNN robustness | Tablets | Wohlers et al. 2023 already covers it; small n | Rejected |
| 5 | Conformal classification of Raman spectra (Bacteria-ID) | Ho et al. 2019 | Conformal classification in chemometrics exists (Gu 2019; Booksh 2025; Qian 2024) | Rejected: prior art |
| 6 | Automated preprocessing selection / ensembles | Several NIR sets | SPORT / PORTO / ensemble preprocessing (Mishra et al.) exist | Rejected |
| 7 | Variable-selection stability under instrument change | Corn | Hard to demonstrate objectively; weak statistical evidence | Rejected |
| 8 | Outlier / applicability-domain detection for transferred models | Tablets | Q/T² diagnostics are standard; novelty unclear | Merged into #1 as the difficulty score |
| 9 | Temperature-robust NIR models | Mango temperature subset | Sun et al. 2020 already addressed it | Rejected |
| 10 | Tabular foundation models for NIR calibration | Mango | Preprint competition (arXiv 2605.21544); heavy compute | Rejected: compute and novelty |
| 11 | Uncertainty estimation for NIR CNNs (MC dropout, ensembles) | Mango | Maxime et al. 2025 (CILS) already covers this | Rejected; used as a baseline in #1 |
| 12 | Multiblock / multi-instrument fusion | Corn | Weak gap | Rejected |
| 13 | Calibration-sample-size planning for PLS | Simulated + NIR | Risk of being judged a purely statistical paper | Rejected |
| 14 | LIBS calibration transfer | No suitable public multi-instrument LIBS data found | Data risk | Rejected |
| 15 | Soil spectral library (LUCAS) transfer between countries | LUCAS (licence registration required) | Data access in this environment uncertain | Rejected: data risk |

## Stress test of #1 (sceptical ACA editor)

* *Too incremental?* Conformal methods exist, but no study we found establishes **whether prediction intervals stay valid after calibration transfer / model update**. None provides a procedure that **reuses the same few transfer standards** for both fitting the transfer and distribution-free calibration. In analytical practice, reference-analysed transfer samples are the scarce resource, so this is an analytical-chemistry problem (measurement uncertainty of a transferred method), not a generic ML exercise.
* *Already solved?* Classical PLS intervals (ASTM E1655 style; Faber; Allegrini et al. 2016) assume that the calibration error model carries over to the new instrument. Calibration-transfer papers report RMSEP only. A target-domain split-conformal approach is valid but wasteful; we test it as a baseline.
* *Simple combination of existing techniques?* Partly yes; the core inference engine is jackknife+. The contribution is the **transfer-aware construction**: leave-one-standard-out *re-fitting of the transfer map*, a proof that coverage holds for transferred pipelines, normalisation with chemometric diagnostics, and a systematic multi-dataset benchmark. This must be stated honestly in the paper.
* *Objectively demonstrable?* Yes. Coverage and width are directly measurable on held-out target samples with known reference values, over hundreds of random draws of the standards.
* *Strong baselines?* Yes: parametric PLS intervals; source split conformal; weighted conformal under covariate shift (Tibshirani 2019); target split conformal; Gaussian intervals from standard RMSE; a regression analogue of transported calibration (Doula 2026); and MC dropout for CNNs.
* *Dataset too small?* Corn (n = 80) is small, so tablets (655) and mango (~4,700 fruit) are added. Many random repetitions are used, with honest Monte-Carlo CIs.
* *Leakage?* Standards and test samples are drawn from the target pool, disjoint from source training data. Mango is split by fruit, not by spectrum.
* *Could the claimed improvement disappear under proper testing?* The main claim is **validity** (coverage ≥ nominal) together with efficiency relative to *other valid* methods. Both are tested with pre-registered, paired, Holm-corrected tests.
* Decision: **proceed**, with two pre-committed limitations: reference values for the standards are required (a label-free variant is exploratory), and the guarantee holds only for randomly selected standards (Kennard–Stone selection is tested as a robustness condition).
