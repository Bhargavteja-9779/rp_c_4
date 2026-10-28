[Corresponding author name]\
[Department, Institution]\
[Address, Country]\
[E-mail]

[Date]

The Editors\
*Analytica Chimica Acta*\
Elsevier B.V.

Dear Editors,

Please consider our manuscript "Trustworthy prediction intervals after moving an NIR calibration to a new instrument or season: how many reference samples, and from how many batches?" for publication as a Research Paper in *Analytica Chimica Acta*.

Many laboratories move NIR calibrations: to a new handheld unit, to a second production spectrometer, or to a new harvest season. The move is usually checked by the prediction error on a few reference samples, but the results are reported, and products accepted or rejected, with an uncertainty range. We asked whether that range can still be trusted after the move, and what the reference samples have to look like for it to be trusted.

On three public data sets the answer to the first question was no. Uncertainty ranges taken over from the original calibration covered as few as {{min_cov_source}} of the reference values instead of 90%. The good news is that the reference samples needed for the transfer are enough to restore a valid range: the transfer is simply re-fitted with each sample left out in turn, and no extra measurements are needed.

The finding we consider most useful for practice concerns where the reference samples come from. With mango data that record the consignment of every fruit, 20 reference fruit from two consignments gave intervals that were too narrow for fruit from other consignments in {{r_k2_tjn_under}} instrument and season settings. The usual alternatives, including Gaussian and random-effects intervals, failed in the same way. The same 20 fruit spread over many consignments did not. {{r_cover_app}} The rule that follows, take transfer standards from many batches, costs nothing and can be applied immediately.

The work fits the journal's interest in chemometric methods with important applications. It addresses measurement uncertainty of transferred analytical methods, it is phrased in method-validation terms, and it ends with a concrete procedure. We do not claim new statistical theory: the interval construction is an application of the jackknife+ and of its batch-level version, which we cite. The contribution is the evidence on when such intervals hold after calibration transfer, the comparison with the methods laboratories actually use, and the resulting sampling rule.

All data are public. All code and raw results, and the scripts that regenerate every number, table and figure, will be made publicly available. The manuscript has not been published and is not under consideration elsewhere, and all authors have approved it. The authors declare no competing interests. An AI assistant was used for literature search support, code development, data analysis and drafting, as declared in the manuscript; the authors take full responsibility for the content.

Suggested reviewers: [to be provided by the authors]

Yours sincerely,

[Corresponding author name], on behalf of all authors
