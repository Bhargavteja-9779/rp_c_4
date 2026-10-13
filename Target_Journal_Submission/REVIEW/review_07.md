# Review round 7 — Reviewer #7 (scientific writing, logic, terminology, figures/tables, guideline compliance)

Scope: language, structure, unsupported claims, mathematical consistency and ACA compliance only. This review is independent of the scientific content reviews.

## MAJOR
| # | Issue | Fix applied |
|---|---|---|
| W1 | **Research questions are used but never defined.** Section headings cite RQ1–RQ6, which are defined only in the external pre-registration. | Added the list of RQ1–RQ6 at the end of the Introduction. |
| W2 | **Overstated causal wording.** "Source-calibrated intervals under-covered *whenever* the transfer added error" generalises beyond the evidence. | Rephrased to "when the transfer added substantial error … (compare Table 2)". |
| W3 | **Reference-list defect.** An HTML entity from Crossref metadata appeared in a journal name ("Infrared Physics &Amp; Technology"). | All bibliography fields are now HTML-unescaped (1 entry fixed). |

## MODERATE
| # | Issue | Fix |
|---|---|---|
| w1 | The abstract's Results opened with a 48-word sentence. | Split into two sentences. The abstract is now 235 words (limit 250) and mentions the independent instrument test. |
| w2 | Mango units alternated between "%" and "% DM". | Unified to "% DM". |
| w3 | The heading of §4.6 did not reflect the added E8 analysis. | Renamed "…, model classes and instruments". |
| w4 | Figures and tables must be cited in numerical order of first mention. | Verified: Figs. 1–10 and Tables 1–8 appear in order; supplementary items are labelled S1–S7. |

## Checked and found compliant (ACA guide for authors; Elsevier)
- Structured abstract (Background / Results / Significance) ≤ 250 words; 6 keywords.
- Highlights: 5 bullets, each ≤ 85 characters (`manuscript/Highlights.txt`).
- Graphical abstract supplied (`figures/graphical_abstract.png`, 300 dpi, ≈ 5:2).
- Numbered sections, numbered equations (1)–(4), Elsevier numeric reference style generated from verified metadata.
- CRediT statement, competing-interest, generative-AI, funding and data-availability declarations present. Author and affiliation fields are placeholders, to be completed by the authors.
- Line numbers and page numbers in the review manuscript (DOCX).

## Mathematical consistency (checked)
- The ranks in Eq. (4) match the implementation (`ceil((1−α)(m+1))`, `floor(α(m+1))`).
- The minimum-*m* statements follow from Eq. (4): *m* ≥ 9 for α = 0.10 and *m* ≥ 19 for α = 0.05; the split baseline needs *m* ≥ 18 at α = 0.10.
- Notation μ₋ᵢ, σ₋ᵢ and Rᵢ is consistent between §2.3 and Appendix A.

## Remaining minor items (accepted as they are)
- Some long sentences in technical passages, kept for precision.
- "TJ+N" and "TJ+" are both used deliberately (normalised vs unnormalised).
