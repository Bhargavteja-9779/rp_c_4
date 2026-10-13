# Review round 8 — Reviewer #8 (competing researcher)

Stance: I work on uncertainty for transferred NIR models and want to show that the contribution is incremental, that an existing method already solves the problem, that the gain comes from another factor, or that the comparison is unfair.

## Attack 1 — "Any method that uses target residuals would do; the jackknife+ machinery is unnecessary."
- **Test:** compare all target-calibrated variants across every pipeline and α level (E1 + E8: 528 scenario cells).
- **Outcome (data):**
  - TJ+N: 0 under-covering cells.
  - TCV+N: 0.
  - Plain jackknife without "+" (TJ-naive-N): 3 (corn, DS, m = 10).
  - Gaussian LOO interval: 77.
  - In-sample transfer residuals: 199.
- **Verdict:** partially valid. The plain jackknife is nearly as good empirically. The "+" construction adds a guarantee and removed the three failures. The decisive element is the leave-one-out *re-fit of the transfer*: in-sample residuals fail in 199 of 528 cells. The manuscript must say clearly that the plain jackknife is a reasonable practical alternative (done in §4.4).

## Attack 2 — "A heteroscedastic Gaussian interval with the same σ(x) is as good, without any conformal machinery."
- **Test:** this was not in the original design, so a new experiment (E9) was specified before results. Gauss-LOO-N = μ ± t(m−1)·RMS(Rᵢ)·σ(x), compared with TJ+N and Gauss-LOO on all primary pipelines and on E8, at α = 0.05, 0.10 and 0.20, with 200 repetitions.
- **Outcome (data):**
  - Under-covering scenarios: TJ+N {{e9_tjn_under}}, Gauss-LOO {{e9_gauss_under}}, Gauss-LOO-N {{e9_gaussn_under}} (all α).
  - At α = 0.05: TJ+N {{e9_tjn_under_005}}, Gauss-LOO {{e9_gauss_under_005}}, Gauss-LOO-N {{e9_gaussn_under_005}}.
  - At α = 0.10: {{e9_tjn_under_01}}, {{e9_gauss_under_01}}, {{e9_gaussn_under_01}}.
  - Efficiency at α = 0.10: Gauss-LOO-N had a lower median interval score than TJ+N in {{e9_gaussn_better}} of {{e9_n_scen}} scenarios (median ratio {{e9_gaussn_rel_is}}).
- **Verdict:** reported in §4.3 and Supplementary Table S8. The advantage of TJ+N is validity without distributional assumptions, not uniformly narrower intervals.

## Attack 3 — "The gain is caused by the transfer standards, not the method."
Correct, and the authors already say so: all target-calibrated methods use the standards. The question the paper answers is *how* to use the same standards both for transfer and for calibration without splitting them and without distributional assumptions. The comparison with SCP-T-split (same information, valid, unbounded for m ≤ 15) isolates this.

## Attack 4 — "The baselines are unfair."
- **ASTM-PI uses an in-sample SEC:** addressed (SCP-S with cross-validated residuals fails similarly).
- **Transport implements only part of TCC:** acknowledged in the text.
- **PDS settings untuned:** acknowledged; the comparison is within pipeline.
- **WCP-S uses unlabelled test spectra (transductive)**, which is generous to WCP-S.

No unfairness in favour of the proposed method was found.

## Attack 5 — "The data sets favour the method."
- **Tablets:** source intervals were nearly valid for weight and hardness; this is reported, not hidden.
- **E8 (independent, not designed by the authors):** PDS was a poor transfer, and TJ+N was then valid but wide.

The data sets do not systematically favour TJ+N.

## Required changes
1. State the competitiveness of the plain jackknife and of Gaussian alternatives, with the E9 numbers.
2. Avoid any wording that implies superior efficiency in general.
