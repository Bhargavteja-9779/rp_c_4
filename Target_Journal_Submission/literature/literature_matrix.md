# Literature matrix and novelty map (Phases 3–4)

All bibliographic data were verified through Crossref, DataCite or official proceedings pages (`references_verified.json`). Content statements rely on retrieved abstracts (`abstracts.json`) or on the well-established content of classic papers. **n/r** means the information was not retrieved, so no claim is made about it.

## A. Uncertainty / prediction intervals in multivariate calibration

| Paper | Year | Venue | Problem | Data | Method | Shift considered? | Limitation relevant to us |
|---|---|---|---|---|---|---|---|
| Faber & Kowalski | 1997 | J. Chemom. | PCR/PLS prediction intervals with errors in all variables | n/r | Error-propagation (EIV) expressions | No | Parametric; assumes the calibration error model holds for new samples |
| Olivieri et al. (IUPAC) | 2006 | Pure Appl. Chem. | Uncertainty and figures of merit for multivariate calibration | Review | Review | No | Defines the analytical need; no distribution-free guarantee |
| Bouckaert et al. | 2011 | Chemom. Intell. Lab. Syst. | Comparing PI methods for NIR | NIR | Several PI methods plus rescaling | No | In-distribution |
| Allegrini, Wentzell & Olivieri | 2016 | Anal. Chim. Acta | Error-dependent prediction uncertainty | n/r | Generalised error propagation | No | Parametric, in-distribution |
| ASTM E1655 | 2017 | ASTM standard | IR multivariate quantitative analysis practice | — | Leverage-based statistics / intervals | No | Parametric; source SEC |
| Jovic | 2025 | Food Chem. | Conformal regression for MIR adulteration | 2 MIR data sets | Normalised inductive CP, 12 models | **No** | No instrument/season shift |
| Duma et al. (preprint) | 2025 | arXiv 2512.23444 | Conformal-inspired intervals for PLS/PCR/kernel variants | Synthetic, NIR, hyperspectral | Input-dependent calibrated intervals | **No** (per abstract) | No transfer setting |
| Maxime et al. | 2025 | Chemom. Intell. Lab. Syst. | NN uncertainty for spectra (mango DM) | Mango | MC dropout, model averaging, SWAG | n/r | No coverage guarantee |
| Norinder et al. | 2014 | J. Chem. Inf. Model. | CP as an applicability-domain alternative (QSAR) | 10 public sets | Inductive CP | No | QSAR, no instrument transfer |
| Gu et al.; Redd & Kalivas; Qian et al.; Booksh et al. | 2019–2025 | Appl. Spectrosc.; J. Chemom.; CILS | Conformal **classification** of spectra | Raman / NIR | CP for classification / OCC | No | Classification only |

## B. Calibration transfer / model updating

| Paper | Year | Venue | Method | Standards needed | Output | Uncertainty after transfer? |
|---|---|---|---|---|---|---|
| Wang, Veltkamp & Kowalski | 1991 | Anal. Chem. | DS and PDS | Paired standards | Standardised spectra | No |
| Bouveresse & Massart | 1996 | CILS | Improved PDS | Paired | Spectra | No |
| Feudale et al. (review) | 2002 | CILS | Review (DS, PDS, SBC, …) | — | — | Not addressed |
| Workman (review) | 2018 | Appl. Spectrosc. | Review of transfer practice | — | — | States that identical results across instruments remain elusive |
| Nikzad-Langerodi et al. (di-PLS) | 2018 | Anal. Chem. | Domain-invariant PLS | Labelled source; (un)labelled target | Adapted model | No |
| Mishra & Nikzad-Langerodi | 2020 | Infrared Phys. Technol. | di-PLS for fruit NIR (instrument/season/temperature) | Unlabelled target | Adapted model | No |
| Fonseca Diaz, Roger & Saeys (uDOP) | 2022 | Anal. Chim. Acta | Standard-free transfer | None | Adapted model | n/r |
| Xie et al. (filter learning) | 2024 | Anal. Chim. Acta | Learned spectral filters | n/r | Adapted model | n/r |
| Fan et al. (PCELM-ELM) | 2025 | Anal. Chim. Acta | PCA + ELM transfer (corn, tobacco, tablets) | n/r | Point predictions | Not reported in abstract |
| Huang et al. (UCT-LMIR) | 2026 | Anal. Chim. Acta | Standard-free unsupervised transfer | None | Point predictions | n/r |
| Anderson et al.; Walsh et al. | 2020; 2024 | Postharvest Biol. Technol.; SAA | Robust mango DM models across seasons | Mango DMC | PLS / ANN / CNN | Point accuracy only (RMSEP, bias) |

## C. Conformal / distribution-free inference foundations

| Paper | Year | Venue | Relevance |
|---|---|---|---|
| Vovk, Gammerman & Shafer | 2005 | Springer book | Conformal prediction foundations |
| Papadopoulos, Vovk & Gammerman | 2011 | JAIR | Normalised nonconformity for regression |
| Lei et al. | 2018 | JASA | Split / full conformal regression |
| Barber, Candès, Ramdas & Tibshirani | 2021 | Ann. Stat. | **Jackknife+ / CV+**: coverage ≥ 1−2α with leave-one-out refits |
| Tibshirani, Barber, Candès & Ramdas | 2019 | NeurIPS 32 | Weighted CP under covariate shift (baseline WCP-S) |
| Romano, Patterson & Candès | 2019 | NeurIPS 32 | CQR (related adaptive intervals) |
| Guan | 2023 | Biometrika | Localised CP |
| Fontana, Zeni & Vantini | 2023 | Bernoulli | Review |
| Angelopoulos & Bates | 2023 | Found. Trends ML | Tutorial |
| Prinster, Liu & Saria (JAWS) | 2022 | NeurIPS 35 | Weighted jackknife+ under covariate shift (needs labelled source data and the covariate-shift assumption, which instrument changes violate) |
| Papadopoulos, Vovk & Gammerman (normalised scores) | 2011 | JAIR | Normalised nonconformity; basis of TJ+N's σ(x) scaling (not claimed as new) |
| Doula (preprint, ICML 2026) | 2026 | arXiv 2609.10737 | **Transported conformal calibration** with unlabelled paired data; classification, image benchmarks (baseline "Transport", regression analogue) |

**Uncertainty after calibration transfer outside spectroscopy:** Zhivkov & Fidanova (2026, *Atmosphere*) characterise uncertainty growth with distance for transferred calibrations of low-cost air-quality sensors (empirical, no finite-sample guarantee).

## Gap analysis

* **What exists:** (i) calibration-transfer algorithms evaluated by RMSEP/bias; (ii) interval methods (parametric, conformal) validated in-distribution; (iii) generic conformal theory, including jackknife+ and covariate-shift weighting; (iv) one ML preprint on transporting calibration between paired domains, for classification.
* **What these fail to address:** whether prediction intervals of a *transferred* spectroscopic calibration keep their nominal coverage, and how to obtain valid intervals when the only target information is the handful of transfer standards that were also used to fit the transfer.
* **Why it matters:** analytical results require stated uncertainty (IUPAC; ASTM E1655 practice). Transfer standards with reference values are expensive, so splitting them for calibration wastes them, and source-calibrated intervals can be badly mis-calibrated after the instrument or season changes.
* **What this work adds:** (1) a quantified demonstration that conventional intervals under-cover after transfer; (2) TJ+: leave-one-standard-out *re-fitting of the transfer step*, giving distribution-free coverage ≥ 1−2α while reusing all standards; (3) chemometric (T²/Q) normalisation; (4) an exploratory label-free variant; (5) a public, reproducible benchmark over 3 data sets, 2 shift types and 3 model classes.
* **How it is verified:** experiments E1–E8 (see `research_design/preregistration.md`).

## Novelty map

| Existing work | Contribution | What this work does differently |
|---|---|---|
| Barber et al. 2021 | Jackknife+ for a fixed regression algorithm | We apply it to the **transfer step** (the source model stays fixed), state the exchangeability conditions on transfer standards, and show the data-efficiency gain over splitting in chemometric transfer |
| Tibshirani et al. 2019 | Weighted CP for covariate shift | Instrument change alters P(y\|x), which violates covariate shift; WCP-S is tested as a baseline |
| Doula 2026 | Transported calibration with unlabelled paired data (classification) | Regression; labelled standards; its analogue is used as a baseline |
| Jovic 2025; Duma et al. 2025 | Conformal / conformal-inspired intervals for spectral regression | Instrument/season shift and transfer re-fitting, both absent from those works |
| Calibration-transfer literature | Point-accuracy transfer | Uncertainty validity after transfer |

**Honest positioning:** the inference engine (jackknife+) is not new. The contribution is its correct instantiation for transferred calibrations, together with the empirical evidence that it is needed and works. It is a methodological-application contribution in chemometrics, not a new conformal theory.
