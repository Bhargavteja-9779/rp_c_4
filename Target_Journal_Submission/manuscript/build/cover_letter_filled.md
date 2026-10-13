[Corresponding author name]
[Department, Institution]
[Address, Country]
[E-mail]

[Date]

The Editors
*Analytica Chimica Acta*
Elsevier B.V.

**Submission of an original research article: "Valid prediction intervals for transferred NIR calibrations: reusing the transfer standards with a leave-one-standard-out jackknife+"**

Dear Editors,

We submit the above manuscript for consideration as a Research Paper in *Analytica Chimica Acta*.

**What the work addresses.** Multivariate NIR calibrations are routinely transferred to new instruments or harvest seasons using a few transfer standards, and analytical results must be reported with a statement of uncertainty. We show that prediction intervals calibrated in the source domain can lose most of their coverage after transfer. Across 40 pre-registered scenarios on three public NIR data sets, coverage fell to as low as 0.03 for nominal 90% intervals. We propose a transfer jackknife+, which re-fits only the transfer step in a leave-one-standard-out loop. It thereby reuses the same standards that the transfer requires to obtain distribution-free intervals with a finite-sample coverage guarantee.

**Main findings.**
- The proposed intervals were never flagged as under-covering across instruments, seasons, transfer pipelines (PDS, DS, slope/bias correction) and model classes (PLS, ridge, 1D-CNN). This includes an independent instrument-transfer test between handheld spectrometers that was added during internal review.
- They are bounded with far fewer standards than the valid alternative of splitting the standards.
- We report candidly where a simpler Gaussian approach is equally efficient: at 90%, though it under-covers at 95%.
- All methods fail under spectral drift after standardisation.

**Fit to the journal.** The journal's scope explicitly includes chemometric methodology that demonstrates new principles or important applications, and the journal regularly publishes work on calibration transfer and on prediction uncertainty in multivariate calibration. Our contribution links these two lines: it addresses the measurement-uncertainty statement of a transferred analytical method, and it gives practical guidance (minimum number of standards, how to select them, monitoring of Q residuals).

**Originality and transparency.** The inference engine (jackknife+) is established. Our contribution is its correct instantiation for calibration transfer, a proof adapted to this setting, and a pre-registered, fully reproducible benchmark that includes negative results. To our knowledge, interval validity after calibration transfer has not been studied systematically before. All data are public, and all code, raw results and the scripts that regenerate every number, table and figure will be made publicly available.

**Declarations.**
- This manuscript is original, has not been published previously, and is not under consideration for publication elsewhere.
- All authors have approved the manuscript and agree with its submission.
- The authors declare no competing interests.
- The study used only publicly available data; no human or animal subjects were involved, and no ethics approval was required.
- An AI assistant was used for literature search support, code development, data analysis and drafting, as declared in the manuscript. The authors take full responsibility for the content.

**Suggested reviewers** (optional): [to be provided by the authors]

Thank you for considering our manuscript.

Yours sincerely,

[Corresponding author name], on behalf of all authors
