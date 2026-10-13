# Review round 2 — Reviewer #2 (novelty, prior art, contribution differentiation)

**Recommendation:** Major revision. The paper must state precisely what is new relative to the jackknife+, and must cover the closest prior art.

I re-ran a prior-art search (Crossref; web; arXiv) in addition to the authors' literature matrix. My concerns do not repeat Reviewer #1's.

## FATAL (candidate) — examined and downgraded to MAJOR
**N1. "This is the jackknife+ with a different fitting algorithm plugged in."** The inference engine is indeed Barber et al.'s jackknife+, and Appendix A is a direct instantiation of their argument.
- *Is it therefore incremental for ACA?* I consider the work publishable only if the manuscript makes the following explicit.
  - (a) The non-obvious modelling decision is *what* to put inside the leave-one-out loop. It is the transfer step, not the source model, which in practice cannot be re-fitted because the master data and model belong to a different instrument or season.
  - (b) The two natural practices both lack validity guarantees: using residuals of the fitted transfer (in-sample), and Gaussian intervals from the LOO RMSE. The ablation and α-sensitivity results show that each can fail.
  - (c) The contribution is a validated methodology for analytical practice (standards budget, minimum *m*, selection requirements, failure under drift), not new conformal theory.
- *Required:* add an explicit "What is and is not new" paragraph to the Introduction, and avoid any wording that suggests new conformal theory.

## MAJOR
| # | Issue | Fix |
|---|---|---|
| N2 | **Missing prior art: JAWS** (Prinster, Liu & Saria, NeurIPS 2022), a weighted jackknife+ under covariate shift. It is the closest *jackknife+-under-shift* method and is not cited. | Cite it. Explain that it relies on the covariate-shift assumption and labelled source data, which instrument changes violate; WCP-S is the split-conformal representative of that family and failed (§4.2). |
| N3 | **Missing related work on uncertainty for calibration transfer in sensors.** Zhivkov & Fidanova (2026, *Atmosphere*) derive distance-based uncertainty growth for transferred calibrations of air-quality sensors. It is empirical, with no finite-sample guarantee. | Cite it as evidence that uncertainty after calibration transfer is a recognised problem outside spectroscopy, and contrast it with the guarantee offered here. |
| N4 | **Transport baseline may be a strawman.** Doula's TCC includes a label-free mismatch correction (TCC-KS) and a weighted variant. The authors implement only the transport step, in a regression analogue. | State this explicitly in §2.4 and in the Limitations. The comparison concerns the transport idea, not the full TCC method, and a full regression adaptation of TCC is future work. |
| N5 | **Normalisation is not new.** Normalised nonconformity scores (Papadopoulos et al. 2011) and their use for spectra (Jovic 2025) exist. The novelty claim for TJ+N must be limited to (i) using PLS T²/Q of the *transferred* spectrum and (ii) re-evaluating σ inside the leave-one-out loop. | Revise contribution 2 and cite Papadopoulos et al. (2011). |

## MODERATE
| # | Issue | Fix |
|---|---|---|
| n1 | The claim "We found no study of interval validity for transferred spectroscopic calibrations" needs a stated search scope. | Add the search scope (databases, period, terms) to the Supplementary Material or a footnote-type sentence. |
| n2 | Practical "validation of calibration transfer" (comparing predictions on check samples before and after transfer) is common in industry and is related to Gauss-LOO. | Mention it as the practical analogue of Gauss-LOO. |

## MINOR
- The literature matrix should list JAWS, Zhivkov 2026 and Papadopoulos 2011.

## Is the research gap genuine?
Yes, after verification. None of the retrieved works evaluates or guarantees interval coverage for spectroscopic calibrations after instrument or season transfer using the transfer standards. The gap is narrow but real, and practically relevant.
