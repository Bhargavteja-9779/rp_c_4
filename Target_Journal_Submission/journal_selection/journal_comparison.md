# Journal comparison (80 candidates measured; ≥10 investigated in depth)

**Timing metric.** Days from `received` to `accepted` in PubMed history records deposited by publishers, for up to 300 research articles per journal (publication dates 2025-07-01 to 2026-09-30; reviews and editorials excluded). This is the submission-to-acceptance interval for papers that were eventually **accepted**. It is not first-decision time, and it is not acceptance-to-publication time. Reproduce with `python scripts/pubmed_acceptance_times.py out.csv`.

Journals not indexed in PubMed (for example Expert Systems with Applications, Results in Engineering, Energy and AI, Journal of Big Data) were checked through publisher-reported medians retrieved by web search:
- Results in Engineering: 76 days, rejected (>72).
- Alexandria Engineering Journal: 118–130 days, rejected.
- Energy and AI: 95–116 days, rejected.
- Journal of Energy Storage: 107 days, rejected.
- Pattern Recognition: 289 days, rejected.
- J. Computational Design & Engineering (OUP): 14 weeks (~98 days), rejected.
- Journal of Big Data (Springer): only a first-decision median (57 days) is published; acceptance time is **unverified**, so rejected.

IEEE journals deposit no PubMed received/accepted dates (n = 0), so their acceptance times are **unverified** here. MDPI titles were excluded by user instruction. Heliyon was excluded because Clarivate placed it on hold in 2024.

JIF and quartile values below come from aggregators and are **not verified against JCR**.

| Journal | n | Median days | IQR | % ≤72 d | JIF (unverified) | Quartile | Scope fit for chemometric UQ | Decision |
|---|---|---|---|---|---|---|---|---|
| Frontiers in Plant Science (Frontiers) | 300 | 53.5 | 39–75 | 72.7% | ~4-5 (unverified) | Q1 Plant Sciences (aggregator) | Poor for chemometric methodology unless plant-centred | Rejected: scope fit |
| Frontiers in Microbiology | 300 | 54 | 40–86.75 | 66.7% | ~4 (unverified) | Q2 (aggregator) | Poor | Rejected: scope |
| Analytica Chimica Acta (Elsevier) | 300 | 58 | 43–77 | 70.3% | ~6.1 (2025, aggregator) | Q1 Chem. Analytical (aggregator) | Excellent: chemometric methodology explicitly in scope; publishes calibration transfer | SELECTED |
| Frontiers in Endocrinology | 300 | 60.5 | 41–83 | 67% |  |  |  | Not shortlisted: scope |
| Frontiers in Physiology | 300 | 61 | 43–92.75 | 58.7% |  |  |  | Not shortlisted: scope |
| Frontiers in Neuroscience | 300 | 62 | 44.25–86.5 | 60.3% |  |  |  | Not shortlisted: scope |
| Frontiers in Neurorobotics | 77 | 64 | 42.5–102 | 55.8% |  |  |  | Not shortlisted: scope |
| Frontiers in Medicine | 300 | 64.5 | 45–85.5 | 59.7% |  |  |  | Not shortlisted: scope |
| Biomedical Optics Express (Optica) | 293 | 65 | 53–82 | 60.4% | ~3 (unverified) | Q2 Optics / Q1? (unverified) | Moderate (biomedical spectroscopy only) | Rejected: lower JIF, biomedical scope |
| Frontiers in Psychiatry | 300 | 66 | 47–101 | 57% |  |  |  | Not shortlisted: scope |
| Frontiers in Genetics | 300 | 67.5 | 47.25–108 | 55% |  |  |  | Not shortlisted: scope |
| Frontiers in Pharmacology | 300 | 68 | 51–101.75 | 57.7% |  |  |  | Not shortlisted: scope |
| Frontiers in Bioengineering and Biotechnology | 300 | 68 | 47–101 | 55.3% |  |  |  | Not shortlisted: scope |
| Talanta (Elsevier) | 299 | 68 | 51–95 | 58.5% | ~6 (aggregator, unverified) | Q1 Chem. Analytical (aggregator) | Good: chemometrics accepted; more application-oriented | Fallback |
| Frontiers in Oncology | 300 | 68 | 46–100.5 | 55% |  |  |  | Not shortlisted: scope |
| Frontiers in Public Health | 300 | 68 | 48–96.75 | 56% |  |  |  | Not shortlisted: scope |
| Frontiers in Nutrition | 300 | 69 | 49–97.75 | 53.7% |  |  |  | Not shortlisted: scope |
| Frontiers in Immunology | 300 | 70 | 53–103 | 52.7% |  |  |  | Not shortlisted: scope |
| Frontiers in Artificial Intelligence | 300 | 73 | 54.25–107.5 | 49% | ~3 (unverified) | Q2 (unverified) | Moderate | Rejected: median 73 d > 72, lower JIF |
| Frontiers in Big Data | 126 | 74.5 | 49.75–119.75 | 48.4% |  |  |  | Rejected: median > 72 d |
| Spectrochim Acta A (Elsevier) | 300 | 75 | 54–105 | 48% |  |  |  | Rejected: median > 72 d |
| Frontiers in Computational Neuroscience | 152 | 75 | 50.25–109 | 46.1% |  |  |  | Rejected: median > 72 d |
| Frontiers in Human Neuroscience | 300 | 76 | 52–109.75 | 47% |  |  |  | Rejected: median > 72 d |
| Bioresource Technology (Elsevier) | 299 | 76 | 60–101 | 45.8% |  |  |  | Rejected: median > 72 d |
| Ultrasonics Sonochemistry (Elsevier) | 299 | 76 | 57–114 | 45.8% |  |  |  | Rejected: median > 72 d |
| J Chem Theory Comput (ACS) | 158 | 77 | 59–97.25 | 44.9% |  |  |  | Rejected: median > 72 d |
| J Chem Inf Model (ACS) | 201 | 79 | 60–108 | 39.8% | ~5.3-6 (unverified) | Q1 | Good for ML-chemistry | Rejected: median 79 d > 72 |
| Frontiers in Digital Health | 300 | 80 | 53–125.75 | 42.7% |  |  |  | Rejected: median > 72 d |
| Environmental Research (Elsevier) | 287 | 83 | 59–123 | 40.1% | ~7.7 (unverified) | Q1 | Poor | Rejected: median 83 d |
| Frontiers in Cardiovascular Medicine | 300 | 85 | 56–123 | 38.7% |  |  |  | Rejected: median > 72 d |
| Water Research (Elsevier) | 300 | 86 | 68.25–117.75 | 29% | ~12 (unverified) | Q1 | Poor | Rejected: median 86 d |
| Journal of Biophotonics (Wiley) | 299 | 89 | 63–126 | 34.1% |  |  |  | Rejected: median > 72 d |
| Plant Physiol Biochem (Elsevier) | 299 | 91 | 66–140 | 31.8% |  |  |  | Rejected: median > 72 d |
| Comput Struct Biotechnol J (Elsevier) | 300 | 91 | 62–118.5 | 35.3% | ~4-6 (unverified) | Q1/Q2 | Poor | Rejected: median 91 d |
| J Hazardous Materials (Elsevier) | 300 | 94 | 73–121.5 | 24.3% |  |  |  | Rejected: median > 72 d |
| Plant Methods (BMC) | 159 | 97 | 71–147 | 28.3% |  |  |  | Rejected: median > 72 d |
| Journal of Neuroscience Methods (Elsevier) | 295 | 106 | 75–150 | 21.7% |  |  |  | Rejected: median > 72 d |
| ACS Omega (ACS) | 300 | 106 | 76–136 | 21.3% |  |  |  | Rejected: median > 72 d |
| Int J Biol Macromol (Elsevier) | 290 | 110.5 | 84–153.5 | 15.2% |  |  |  | Rejected: median > 72 d |
| Advanced Science (Wiley) | 300 | 113 | 79.25–160.75 | 21.7% |  |  |  | Rejected: median > 72 d |
| Journal of Nanobiotechnology (BMC) | 299 | 115 | 86–151 | 15.7% |  |  |  | Rejected: median > 72 d |
| J Environmental Management (Elsevier) | 300 | 116.5 | 77–164.25 | 20.3% |  |  |  | Rejected: median > 72 d |
| European Heart Journal Digital Health (OUP) | 220 | 118 | 88–155.5 | 10.9% |  |  |  | Rejected: median > 72 d |
| JAMIA (OUP) | 268 | 120.5 | 85.5–163.75 | 16.4% | ~4.7-6 (unverified) | Q1 | Poor | Rejected: median 120.5 d |
| Physics in Medicine & Biology (IOP) | 289 | 124 | 101–161.5 | 8.7% |  |  |  | Rejected: median > 72 d |
| Computers in Biology and Medicine (Elsevier) | 299 | 124 | 79–193 | 20.7% |  |  |  | Rejected: median > 72 d |
| Digital Discovery (RSC) | 70 | 124.5 | 96.75–154 | 15.7% |  |  |  | Rejected: median > 72 d |
| Briefings in Bioinformatics (OUP) | 299 | 125 | 92–170 | 11.4% | ~7-9 (unverified) | Q1 | Poor | Rejected: median 125 d |
| Journal of Translational Medicine (BMC) | 298 | 125 | 87.75–169.5 | 19.5% |  |  |  | Rejected: median > 72 d |
| Brain Informatics (Springer) | 54 | 127.5 | 86.75–186.5 | 20.4% |  |  |  | Rejected: median > 72 d |
| Ecotoxicol Environ Saf (Elsevier) | 300 | 128 | 89–181.75 | 13.3% |  |  |  | Rejected: median > 72 d |
| Physiological Measurement (IOP) | 185 | 128 | 100–168 | 9.2% |  |  |  | Rejected: median > 72 d |
| Bioinformatics Advances (OUP) | 299 | 130 | 99–160 | 12.4% |  |  |  | Rejected: median > 72 d |
| Journal of Cheminformatics (Springer) | 207 | 132 | 107–172 | 3.4% |  |  |  | Rejected: median > 72 d |
| J Neural Engineering (IOP) | 291 | 138 | 108–190 | 7.2% |  |  |  | Rejected: median > 72 d |
| Scientific Reports (Nature) | 288 | 138 | 90.25–198.25 | 11.8% |  |  |  | Rejected: median > 72 d |
| Science of the Total Environment (Elsevier) | 141 | 142 | 93.5–209 | 13.5% |  |  |  | Rejected: median > 72 d |
| Plant Phenomics | 161 | 143 | 104.5–178 | 7.5% |  |  |  | Rejected: median > 72 d |
| Bioinformatics (OUP) | 262 | 144 | 103.75–197.25 | 8.4% | ~5 (unverified) | Q1 | Poor (bio) | Rejected: median 144 d |
| BMC Bioinformatics (BMC) | 300 | 146.5 | 104–229.75 | 9.3% |  |  |  | Rejected: median > 72 d |
| J Biomedical Informatics (Elsevier) | 214 | 148 | 112.75–187 | 2.8% |  |  |  | Rejected: median > 72 d |
| Neuroimage (Elsevier) | 299 | 148 | 107–204 | 7.7% |  |  |  | Rejected: median > 72 d |
| NAR Genomics and Bioinformatics (OUP) | 228 | 153.5 | 115–203.5 | 5.3% |  |  |  | Rejected: median > 72 d |
| Nucleic Acids Research (OUP) | 294 | 157.5 | 77.25–243.25 | 23.5% |  |  |  | Rejected: median > 72 d |
| Journal of Advanced Research (Elsevier) | 300 | 163.5 | 122–221.75 | 2.7% |  |  |  | Rejected: median > 72 d |
| Patterns (Cell Press) | 103 | 167 | 125–209 | 2.9% |  |  |  | Rejected: median > 72 d |
| PNAS Nexus (OUP) | 298 | 170.5 | 112–230.75 | 10.1% |  |  |  | Rejected: median > 72 d |
| BMC Med Inform Decis Mak (BMC) | 299 | 176 | 107–377 | 11% |  |  |  | Rejected: median > 72 d |
| Food Chemistry (Elsevier) | 298 | 178 | 131–223 | 1.3% |  |  |  | Rejected: median > 72 d |
| Medical Physics (Wiley) | 298 | 181.5 | 125–238 | 4.7% |  |  |  | Rejected: median > 72 d |
| Comput Methods Programs Biomed (Elsevier) | 300 | 183 | 131.5–245 | 3.7% |  |  |  | Rejected: median > 72 d |
| iScience (Cell Press) | 297 | 186 | 138.5–249 | 3.7% |  |  |  | Rejected: median > 72 d |
| npj Digital Medicine (Nature) | 300 | 189 | 132–257.5 | 4.3% |  |  |  | Rejected: median > 72 d |
| PLOS Computational Biology (PLOS) | 279 | 196 | 139–280 | 1.4% |  |  |  | Rejected: median > 72 d |
| GigaScience (OUP) | 99 | 198 | 140–252 | 12.1% |  |  |  | Rejected: median > 72 d |
| Neural Networks (Elsevier) | 300 | 216 | 158.25–296 | 1% |  |  |  | Rejected: median > 72 d |
| Medical Image Analysis (Elsevier) | 299 | 228 | 166–312 | 0.3% |  |  |  | Rejected: median > 72 d |
| Brain Communications (OUP) | 299 | 232 | 174–295 | 1.3% |  |  |  | Rejected: median > 72 d |
| Communications Biology (Nature) | 298 | 243.5 | 175.75–326.25 | 1% |  |  |  | Rejected: median > 72 d |
| Artificial Intelligence in Medicine (Elsevier) | 210 | 293 | 171–387.25 | 0.5% |  |  |  | Rejected: median > 72 d |
