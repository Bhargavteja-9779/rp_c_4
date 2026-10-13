# Selected target journal

| Field | Value |
|---|---|
| **TARGET JOURNAL** | *Analytica Chimica Acta* (ACA) |
| **PUBLISHER** | Elsevier B.V. (published continuously since 1947) |
| **ISSN** | 0003-2670 (print); 1873-4324 (online) |
| **JCR STATUS** | Indexed in Clarivate Journal Citation Reports (Science Citation Index Expanded) |
| **JCR QUARTILE** | Q1, *Chemistry, Analytical*, as reported by secondary sources that mirror JCR (OOIR / Web of Science-derived listings, BioxBio). **Direct JCR access was not available from this environment**, so the quartile must be re-checked in JCR before submission. |
| **JOURNAL IMPACT FACTOR** | ~6.1 (2025 JCR, released June 2026) and 6.0 (2024 JCR), as reported by OOIR and BioxBio. **Not verified against the JCR database itself.** |
| **JCR SUBJECT CATEGORY** | Chemistry, Analytical |
| **VERIFIED REVIEW/DECISION TIMELINE** | Not independently verified; Elsevier's journal-insights page could not be fetched (HTTP 403). |
| **VERIFIED ACCEPTANCE TIMELINE** | **Median 58 days** from receipt to acceptance (IQR 43–77 days; 55.0% accepted ≤60 days, **70.3% ≤72 days**). Measured directly from the publisher-deposited PubMed `received`/`accepted` history dates of 300 research articles published 2025-07 to 2026-09 (`pubmed_acceptance_times.csv`, script `scripts/pubmed_acceptance_times.py`). This is the *submission-to-acceptance* interval for **accepted** papers. It is not first-decision time, and it says nothing about rejected papers. |
| **APC** | Hybrid journal: no fee for the subscription route. The optional open-access APC is reported at USD 3,910 (aggregator, undated) or 4,030 (Cirad database, 2024); confirm on the Elsevier page. |
| **SCOPE FIT** | The official scope states that "fundamental research on analytical chemistry theory and methodology, including chemometric techniques, is especially encouraged when it demonstrates new principles or important applications", and that data treatment is in scope. The journal discourages narrow, application-only work, so our contribution is framed as a general chemometric methodology. |
| **RESEARCH FIT** | ACA publishes calibration-transfer methodology regularly: Fonseca Diaz et al. 2022 (uDOP, 10.1016/j.aca.2022.340154); Xie et al. 2024 (filter learning, 10.1016/j.aca.2024.342404); Fan et al. 2025 (PC-ELM, 10.1016/j.aca.2025.344151); Huang et al. 2026 (UCT-LMIR, 10.1016/j.aca.2026.346104). It also publishes multivariate prediction-uncertainty work (Allegrini, Wentzell & Olivieri 2016, 10.1016/j.aca.2015.11.028). |
| **KEY AUTHOR GUIDELINES** (Elsevier guide for authors, via indexed snapshot) | Abstract ≤250 words, standalone, no references. Highlights: 3–5 bullets, ≤85 characters each, in a separate file. Graphical abstract expected. 1–7 keywords. Elsevier numbered reference style. CRediT author statement. Declaration of competing interests. Declaration of generative-AI use. Data availability statement. Figures supplied as separate high-resolution files. |
| **KEY REJECTION RISKS** | (1) Desk rejection as "pure statistics/ML, not analytical chemistry"; mitigated by analytical-chemistry framing (measurement uncertainty of transferred NIR calibrations, figures of merit, standards budget). (2) Reviewers judging it incremental relative to jackknife+ and the conformal literature; mitigated by a specific transfer-standard-reuse design, a coverage proof for the transfer setting, and a 3-dataset benchmark. (3) Small public datasets (corn n = 80). (4) Acceptance-time risk: about 30% of accepted ACA papers take more than 72 days. |

## Why ACA over the other ≤72-day options
The PubMed measurements (80 journals; see `journal_comparison.md`) show that almost every reputable title from OUP, Elsevier, Springer Nature, Wiley, IOP, PLOS and ACS has a **median submission-to-acceptance time above 72 days**. Examples: Bioinformatics (OUP) 144 days, Briefings in Bioinformatics (OUP) 125, JAMIA (OUP) 120.5, Scientific Reports 138, J. Chem. Inf. Model. (ACS) 79, Computers in Biology and Medicine 124.

Only a handful of Q1/Q2 titles have medians at or below about 70 days. Among those, ACA has:
* the **highest JIF** of the scope-compatible options (~6.1, against Talanta ~6, Frontiers in Plant Science ~4–5, Frontiers in Microbiology ~4 and Biomedical Optics Express ~3, all aggregator-reported);
* the **fastest median** among the non-Frontiers options (58 days, against Talanta 68 and BOE 65);
* a **long-established Elsevier editorial standard** and an explicit chemometrics scope;
* the best methodological fit for a chemometric uncertainty-quantification contribution.

*Talanta* (Elsevier, median 68 days, Q1 Analytical Chemistry) is the documented fallback.

## Honesty statement
* No journal can guarantee the 72-day constraint for a specific manuscript. The measured median (58 days) and the fraction ≤72 days (70.3%) describe **accepted** papers only.
* The JIF and quartile come from secondary sources that reproduce JCR values. The JCR database was not accessible from this environment, so they must be re-checked before submission.
