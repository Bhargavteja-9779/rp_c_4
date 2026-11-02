# Third independent review (after the third research round) and resolutions

**Reviewer.** An independent agent, who read the upgraded manuscript, the result files, the code, the protocol and the git history.

**Checks.**
- 33 of 34 spot-checked numbers matched. The mismatch was "14 instruments", which is 14 settings on 11 units.
- Eq. (5) was re-derived and found correct.
- Git timing confirmed that the E15 predictions were committed (85f2405) before the E15 runs started and before their results were committed (84be247).

**Verdict on that version:** major revision. All items below were fixed and re-validated by rebuilding from the result files (`audit/scripts/consistency_checks.py`: 0 unfilled placeholders, 0 broken glyphs; abstract 246 words) and by re-running the tests (23 passed).

| ID | Severity | Issue | Resolution |
|---|---|---|---|
| C1 | CRITICAL | P4 failed for both TJ+N and Gauss-LOO at K = 2, but only the Gaussian failure was reported. The pre-registered consequence (the model becomes descriptive only) was ignored. | §4.4 now reports both failures with their numbers and applies the protocol rule: the model is described as descriptive and optimistic. "Predicts" was removed from the abstract, conclusions, highlights, cover letter and procedure. |
| C2 | MAJOR | P3 used the ICC estimated on the test consignments, and r = 0.99 was driven by the spread across designs. | §4.4 discloses the oracle ICC. It now reports per-design correlations (0.96 at K = 2, about 0.93 at K = 5, about 0.70 at K = 10) and per-design bias (0.06–0.07 at K = 2). "0.99" was removed from the abstract. The Fig. 5 caption explains the oracle ICC and that points below the diagonal mean optimism. |
| C3 | MAJOR | "14 instruments": the 14 settings use only 11 units. | Now "14 instrument–season settings (11 handheld units)" everywhere. The limitations note that three units appear in two seasons. |
| C4 | MAJOR | The harvest numbers omitted the referral cost and the guard-band result. | The abstract now gives the like-for-like pair (36% → 3.2%) and adds "at the cost of re-measuring about half the fruit". The cover letter adds that a fixed guard band does about as well. §4.5 gives the guard band at equal referral (2.8% vs 3.2%). |
| C5 | MAJOR | The software claims did not match the code: the tools are unscaled, the ANOVA rule was missing, and the browser check was not reproducible. | §4.7 states that the tools implement the unscaled TJ+/TJ+B and the Gaussian and random-effects intervals. `rule="anova"` was added to the API, the command-line program and the browser tool. New unit tests compare every rule with the research code. `software/check_tool_e2e.py` runs the browser tool in Chromium against the package: worst difference 0.005, within the 2-decimal display. A Node test checks the planner and the t quantiles. |
| C6 | MODERATE | "Too narrow by √κ" understated the loss, and the intercept-only model did not match slope/bias correction. | §2.5 now says the scale is underestimated by about √κ on average and that the coverage loss is larger with few batches. It notes the intercept-only assumption and why it makes the model optimistic. "For any design" is now "for balanced designs". |
| C7 | MODERATE | Same-season source model; "untouched" wording; ASTM-PI at K = 2 not reported; TJ+B counts pooled over α. | §3.2 and the limitations disclose the same-season training. The wording is now "not analysed before". ASTM-PI at 2 × 10 (mean 0.76, too narrow in 13/14) is reported. TJ+B counts are given per α (0/16 at 90%, 0/30 at 80%). |
| C8 | MODERATE | The guard-band equivalence holds by construction. | It is presented as an identity, with the caveat that the stated coverage is not met with two consignments. |
| C9 | MINOR | E10 fit reported as one mixed number. | Gauss-LOO and TJ+N are now reported separately (MAE 0.021 and 0.035; r 0.92 and 0.75), generated from the results. |
| C10 | MINOR | Tool usability. | The planner states that it rounds and that it is optimistic with two batches. The header rule of the parser is stated in the input label. |
| C11 | MINOR | Wording, a method glossary, length. | "Between X–Y" fixed. A glossary of method names was added at the start of §2.6. Length (≈10,100 words including tables and captions) remains long for ACA; see the readiness report. |
