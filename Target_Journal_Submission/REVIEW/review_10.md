# Review round 10 — Final adversarial review (attempt to reject)

Independent of rounds 1–9: I re-read the manuscript, the code and the result files with the explicit goal of finding a reason to reject.

## Search for ONE fatal flaw
| Candidate | Investigation | Verdict |
|---|---|---|
| **Data leakage** | Code audit: standards and test samples are disjoint within each repetition. Mango replicates are averaged per fruit before splitting. σ and the source model use source data only. E8 source fruit are disjoint from the target pool. Seeds depend only on (repetition, m). | No leakage found. |
| **Invalid statistical estimand** | Mean per-repetition coverage with a fixed test-set size per scenario is an unbiased estimate of P(y ∈ Ĉ) under the repetition distribution. The bootstrap is over repetitions. | Sound (conditional on data sets, as stated). |
| **Proof error** | Appendix A re-derived: (i) the lower-tail count m − ⌊α(m+1)⌋ + 1 ≥ (1−α)(m+1) holds; (ii) R_{i,m+1} equals the procedure's Rᵢ because the fit excluding i and m+1 is the LOO fit on the standards; (iii) Barber et al.'s counting lemma applies to any score matrix. | Correct. |
| **Results driven by a bug** | One bug (LV sensitivity) was found and fixed in round 4 and affected only Table S3. All headline results come from E1/E4/E5/E8/E9, whose code paths were unaffected. The unit tests cover quantile ranks, PDS, PLS and a coverage simulation. | No result-changing bug remains that I could find. |
| **Claim not supported** | Abstract/Conclusions cross-checked against values.json (see final_audit.md). | No unsupported headline claim. |

**No fatal flaw found.**

## MAJOR weaknesses (real ones only; 8 found)
| # | Weakness | Status |
|---|---|---|
| 1 | **Modest methodological novelty.** The method is jackknife+ applied to the transfer step. | Irreducible. Stated openly ("What is and is not new"). Mitigated by the breadth of evidence and the practical guidance. |
| 2 | **No efficiency advantage at 90% over simple Gaussian intervals.** Gauss-LOO ranks best on interval score; Gauss-LOO-N is ≈3% more efficient. | Stated in the abstract, §4.3 and the Limitations. The value claimed is validity, not width. |
| 3 | **Drift after standardisation defeats all methods, even at ¼ channel.** This limits the practical guarantee to stable instruments. | Tested (E4, E4b); stated in the abstract, Results, Limitations and Conclusions, with the recommendation to monitor Q and re-check on fresh samples. |
| 4 | **Marginal, not training-conditional, coverage.** With m = 20, 6–10% of standard draws gave realised coverage < 0.80. | Quantified (§4.9); guidance given. |
| 5 | **The guarantee requires random standards with reference values.** Common practice (Kennard–Stone, NBS glass standards without reference values) violates this. | Kennard–Stone tested (conservative but uncovered by theory); the label-free variant failed. Stated as a limitation and recommendation. |
| 6 | **Evidence from public benchmarks only.** Corn is small (n = 80); perturbations are simulated; no process or industrial case. | E8 (independent instrument data) added; limitation stated. |
| 7 | **Post-hoc analyses (E8, E9, E4b) were added during internal review.** | Each was specified before its results and logged (deviations 7, 10, 11). The pre-registered core (E1–E7) is unchanged. A sceptic may still discount them; they are labelled as review-driven. |
| 8 | **Transfer pipelines were sometimes poor** (corn PDS window 5; E8 PDS RMSEP up to 7.4 % DM). TJ+N intervals were then valid but very wide. | Reported. Framed correctly: interval validity also diagnoses transfer quality. Point-accuracy tuning was out of scope. |

## MODERATE weaknesses (real ones only; 12 found)
1. The difficulty function σ(x) is a simple additive form in √T² and √Q; no alternative heteroscedastic models (e.g. kNN residual models) were compared. The partial benefit is stated.
2. The T²-only variant was the most balanced on corn but is post hoc. Labelled exploratory.
3. The Friedman test treats dependent scenarios as independent. Now stated, with ranks interpreted descriptively.
4. The tablets weight/hardness responses are insensitive to the transfer, which pads the scenario count with "easy" cases. Results are reported per response, and the conclusions do not rely on them.
5. Coverage is conservative for m = 10–15 (discrete ranks), giving wider intervals than necessary. Explained.
6. ASTM-PI for ridge models uses an approximate leverage and degrees of freedom. Stated.
7. Transport implements only the transport step of TCC. Stated.
8. WCP-S uses transductive target spectra, which favours WCP-S. Stated.
9. The MC-dropout baseline adds the source residual variance (one of several conventions). Documented in code; alternatives were not explored.
10. At α = 0.01, TJ+ needs m ≥ 99. Added to the Limitations.
11. Probabilistic joint models (GP, Bayesian PLS) were not compared. Added to the Limitations.
12. The manuscript is long. Reduced by moving one table and one figure to the Supplementary Material; further shortening is left to the authors.

## MINOR
- Author names, affiliations, funding, repository URL and archived DOI are placeholders.
- The display equations carry manual numbers "(1)–(4)" inside the math; acceptable in DOCX.
- Some long technical sentences remain.
- Supplementary tables are long; they are machine-generated and complete.

## Author-mode response
Every scientifically defensible issue that could be fixed by analysis has been addressed in rounds 1–10, with new experiments where needed (E4b, E8, E9, the E7_lv re-run). The remaining weaknesses are intrinsic to the method or to the data and are disclosed. **Decision of this round: no remaining fixable issue blocks submission.**
