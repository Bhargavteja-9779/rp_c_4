# Review round 1 — Reviewer #1 (general analytical-chemistry reviewer, Analytica Chimica Acta)

**Manuscript:** "Valid prediction intervals for transferred multivariate calibrations: reusing the transfer standards with a leave-one-standard-out jackknife+"
**Recommendation:** Major revision

## Summary
The authors study prediction intervals for NIR calibrations after calibration transfer or model updating. They propose re-fitting the transfer step in a jackknife+ loop (TJ+, TJ+N) and benchmark it on three public data sets with a pre-registered protocol. The problem is relevant, and the reporting of negative results (Gauss-LOO competitiveness, drift failure, label-free failure) is commendable. Several issues need attention.

## FATAL
None identified.

## MAJOR
| # | Issue | Required fix |
|---|---|---|
| M1 | **Proof of Proposition 1 is too loose.** The statement that Barber et al.'s argument "uses only exchangeability of the matrix (R_ij)" is asserted, not shown. Three things are left unstated: that the normalised score must be well defined (σ > 0), that the test point's paired master spectrum is part of the exchangeable unit, and how the event "y ∉ Ĉ" maps onto the comparison matrix. | Add an appendix with a step-by-step proof: (i) the augmented data and fits without {i, j}; (ii) the score matrix; (iii) the implication y ∉ Ĉ ⇒ R_{m+1,i} > R_{i,m+1} for ≥ (1−α)(m+1) indices; (iv) the counting (tournament) lemma; (v) the role of ε > 0. |
| M2 | **Relevance to analytical measurement uncertainty is not discussed.** ACA readers will ask how a coverage interval relates to measurement uncertainty (GUM/IUPAC figures of merit), and whether the reference-method error is included. | Add a discussion subsection: TJ+ intervals are *prediction* intervals for the reference value as measured by the reference method. They therefore include reference-method error, model error and transfer error, but they are not a GUM-type uncertainty budget. Relate to IUPAC figures of merit [Olivieri 2006]. |
| M3 | **Primary transfer pipeline is not the most accurate.** Table 2 shows SBC with lower RMSEP than PDS on corn for all four properties, and the window-5 PDS is less accurate than window 3 (§4.8). A reader may suspect a deliberately weak transfer. | State explicitly in §4.1 that the pipelines were fixed a priori and not tuned on target data, that SBC was more accurate on corn, and that interval validity was unaffected (all pipelines: 0/152 under-covering). |
| M4 | **Incorrect statement about the tablets.** §4.2 says that under-coverage "occurred mainly for the assay with few standards". The data show severe under-coverage for the assay at m = 10 (0.81–0.85, all three source methods), but also marginal yet systematic under-coverage of SCP-S/WCP-S for *weight* at every m (0.894–0.895). | Correct the sentence to reflect both patterns. |
| M5 | **External validity.** Only one season shift and two instrument pairs (corn) plus one tablets pair. The mango shift is a season shift on a single instrument. | See review 5. An independent instrument shift is needed (the providers' extended mango file contains paired spectra from several instruments). |

## MODERATE
| # | Issue | Fix |
|---|---|---|
| m1 | Title says "multivariate calibrations" although only NIR was tested. | Change to "transferred NIR calibrations". |
| m2 | Contribution 1 claims "checkable conditions"; exchangeability is not checkable from data. | Reword to "explicit conditions". |
| m3 | The Gauss-LOO comparison reports only the scenarios where TJ+N won on tablets/mango (9/16), not those where Gauss-LOO won (5/16). | Report both counts. |
| m4 | §4.5 says the 30 robustness scenarios "preserve the joint distribution", but Kennard–Stone selection does not preserve exchangeability. | Rephrase to "all robustness conditions other than post-standardisation drift". |
| m5 | MC-dropout explanation ("epistemic variance does not reflect the season shift") is stated as fact. | Soften to a plausible explanation. |
| m6 | Sentence on PDS windows ("3: 0.237, 7: …") is hard to read, and the window-5 value is missing. | Rewrite with units and include window 5. |
| m7 | Supplementary Tables S2/S3 and Fig. S2 are cited but no supplementary file exists. | Generate a supplementary document from result files. |
| m8 | Conservativeness at small *m* (coverage 0.93–0.95 at m = 10–15 on corn) is explained, but the practical consequence (wider intervals than necessary) is not. | Add one sentence and a pointer to the discreteness of conformal ranks. |

## MINOR
- Table 2 shows the response label "dry_matter"; use "dry matter".
- Table 3 caption reads "α = 0.1"; use 0.10 for consistency.
- §3.1: state the mango file and record version used.
- Highlights (3–5 bullets, ≤ 85 characters) and a graphical abstract are required by ACA and missing.
- Several sentences are long; see review 7 for language.

## Positive aspects (brief)
The pre-registration and deviation log, the honest reporting of competitor strength and of failure modes, and the complete reproducibility are strengths.
