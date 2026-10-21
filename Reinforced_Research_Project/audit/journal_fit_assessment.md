# Journal-fit reassessment (Phase 5)

## Evidence base (all measured in this cycle)

- **PubMed history dates.** Publisher-deposited `received` and `accepted` dates for up to 500 research articles per journal, publication window 2025-10-01 to 2026-10-20. Script: `audit/scripts/journal_timing_refresh.py`; results: `audit/data/journal_timing_refresh.csv`, per-article days in `…_raw.json`. The 95% CI of the share accepted within 72 days is a bootstrap over articles.
- **Crossref `assertion` history dates.** Used for publishers that deposit them (Wiley). Script: `audit/scripts/crossref_timing.py`; results: `audit/data/crossref_timing.csv`. Elsevier, RSC and SAGE deposit no history dates in Crossref (checked); RSC and SAGE also deposit none in PubMed.
- **What the metric is.** It is *submission → final acceptance for papers that were accepted*, which is the user's constraint. It is not first-decision time. It says nothing about rejected papers, and no measurement can guarantee the timeline of a particular manuscript.
- **JIF and quartile.** Clarivate JCR is not accessible from this environment. Values are aggregator-reported and marked unverified.

## Journal-fit matrix

| Journal (publisher) | n | Median d (IQR) | % ≤ 72 d (95% CI) | 90th pct d | JIF / quartile (unverified) | Scope fit for the reinforced paper | 72-day status |
|---|---|---|---|---|---|---|---|
| **Analytica Chimica Acta (Elsevier)** | 500 | **59 (44–78)** | **67.8 (63.6–72.0)** | 103 | ≈6, Q1 Chem. Analytical | **High.** The scope explicitly includes chemometric methodology that "demonstrates new principles or important applications". It publishes calibration-transfer methods (2022–2026) and multivariate prediction-uncertainty papers. | Measured distribution; median ≤ 72 d; **not guaranteed** (≈1 in 3 accepted papers take longer) |
| Talanta (Elsevier) | 499 | 67 (50–95) | 57.5 (53.1–61.9) | 126 | ≈6, Q1 | Good (chemometrics accepted; more application-oriented) | Measured; median ≤ 72 d; lower probability than ACA |
| Anal. Bioanal. Chem. (Springer) | 498 | 69 (51–99) | 54.6 (50.2–58.8) | 133 | ≈4, Q1/Q2 | Moderate–good | Measured; median ≤ 72 d; lower probability |
| Spectrochim. Acta A (Elsevier) | 500 | 77 (57–109) | 44.8 (40.4–49.2) | 155 | ≈4.5, Q1 Spectroscopy | Good (spectroscopy) | **Fails** (median > 72 d) |
| Analytical Chemistry (ACS) | 473 | 96 (73–124) | 24.7 (20.9–28.5) | 161 | ≈6.8, Q1 | Moderate (rarely chemometric methodology) | **Fails** |
| J. Pharm. Biomed. Anal. (Elsevier) | 500 | 84 (68–111) | 31.6 | 145 | ≈3.4 | Low–moderate | **Fails** |
| Food Research International (Elsevier) | 500 | 85.5 | 32.0 | 146 | ≈7 | Low | **Fails** |
| Food Chemistry (Elsevier) | 498 | 183 | 0.8 | 278 | ≈9 | Moderate (Jovic 2025 published there) | **Fails** |
| J. Chemometrics (Wiley) | 101 (Crossref) | 124 (68.5–198.5) | 30.7 (21.8–39.6) | — | ≈2, Q2/Q3 | **High** | **Fails** |
| J. Raman Spectrosc. (Wiley) | 155 (Crossref) | 112 | 21.9 | — | — | Low | **Fails** |
| Chemometr. Intell. Lab. Syst. (Elsevier) | 0 (not in PubMed; no Crossref history) | — | — | — | ≈3.8 (aggregator), Q2 | **High** | **Unverified**, so not eligible as satisfying the constraint |
| Analyst; Analytical Methods (RSC) | 0 (no deposited dates) | — | — | — | — | Good | **Unverified** |
| Applied Spectroscopy; JNIRS (SAGE) | 0 | — | — | — | — | High (NIR) | **Unverified** |

## Can the paper meet ACA's standard?

ACA's expectation is chemometric work that "demonstrates new principles or important applications".

- **Original version.** Its weak point was methodological novelty: a known conformal method, validated where validity is guaranteed.
- **Reinforced version.** It answers a question every analytical laboratory that transfers calibrations faces: *for which future samples does an uncertainty statement built from transfer standards hold, and how must standards be sampled?* The answer rests on real lot structure and is compared against the procedures laboratories actually use (Gaussian, OLS, bootstrap, random-effects intervals). This places it in the "important application of chemometric principles to analytical practice" category, phrased in ACA's language of measurement uncertainty and β-expectation tolerance intervals.
- **Residual mismatch risk.** An editor may still regard it as statistics. The mitigation is the analytical framing: lots, standards budget, the method-validation vocabulary, and practical design rules.

## Decision: **RETAIN AFTER SCIENTIFIC REINFORCEMENT** — Analytica Chimica Acta

1. **Fit.** ACA has the best combination of scope fit (high) and measured speed (fastest median and highest share ≤ 72 d among scope-compatible, measurable Q1 journals). Downgrading would not solve a scientific weakness. The weaknesses are instead addressed in the research itself (E10–E13).
2. **Hard constraint.** The 72-day final-acceptance constraint is **verified only as a historical distribution**: 67.8% (95% CI 63.6–72.0%) of recently *accepted* ACA research papers were accepted within 72 days. It is **not verifiable for this manuscript**. Any revision requiring a second review round very likely exceeds 72 days (90th percentile 103 d). No journal in the matrix with a verifiable timeline offers a higher probability with comparable scope fit.
3. **Fallback.** *Talanta* (57.5% ≤ 72 d) is the documented fallback. The scope-ideal journals (*J. Chemometrics*, *CILS*) either fail the constraint (J. Chemom., median 124 d) or cannot be verified (CILS) and are therefore **not** selected.
4. **Author checks before submission.** The authors must re-check (a) the JIF and quartile in JCR and (b) the current Elsevier guide for authors. The guide page returned HTTP 403 from this environment; the abstract (≤ 250 words) and highlights (3–5 × ≤ 85 characters) limits come from the earlier indexed snapshot.
