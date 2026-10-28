
## 4.3. Where the standards come from matters more than how many there are

The results so far assume that the standards are a random sample of everything the instrument will measure later. In a packhouse this is rarely true. The fruit used to adapt a new handheld unit are typically picked from one or two consignments on the day of installation, and the unit is then used on consignments that arrive weeks later. We reproduced this on the mango data, where each fruit's consignment is recorded. The errors of the transferred predictors were clearly shared within consignments: the intra-consignment correlation of the errors was {{r_icc_range}} across the eight setting-pipeline combinations.

Table 4 and Fig. 4 show what happens to fruit from consignments that supplied no standards. With 20 standards taken from only two consignments, TJ+N was too narrow in {{r_k2_tjn_under}} combinations, with coverage of {{r_k2_tjn_cov}} for a nominal 0.90. The simple alternatives were worse:

- Gaussian intervals from the same left-out errors were too narrow in {{r_k2_gauss_under}};
- the split-standards interval was too narrow in {{r_k2_split_under}};
- the classical random-effects interval for a new batch (ANOVA-PI), which is designed for exactly this situation but has to estimate the between-batch variance from two batches, was too narrow in {{r_k2_anova_under}};
- the intervals carried over from the source calibration were too narrow everywhere.

The damage was largest for slope/bias correction. A slope and an offset fitted on two consignments learn the particular bias of those two consignments, and the left-out errors within them cannot reveal how different the next consignment will be. The same intervals were fine for the remaining fruit of the two sampled consignments (TJ+N coverage {{r_k2_tjn_same_cov}}). The intervals were therefore accurate for the batches that had been sampled, but not for new ones.

Spreading the same number of standards over more consignments removed the problem step by step. TJ+N was too narrow in {{r_tjn_under_K5}} combinations with 5 × 4 standards and {{r_tjn_under_K10}} with 10 × 2. With one fruit from each of 15 or 20 consignments, no combination was too narrow at any confidence level ({{r_tjn_under_ng1}}), as Appendix B predicts.

The batch-level version TJ+B was never too narrow wherever it gave a bounded interval ({{r_tjb_under_bounded}} combinations over all random designs and confidence levels; coverage {{r_tjb_cov}} at 90%). With fewer than nine consignments it gives no finite interval at 90%, which is the honest answer: two consignments cannot certify what a third will look like. Where both were bounded, its intervals were wider than those of TJ+N with 10 × 2 standards (median width ratio {{r_tjb_width_10}}) and identical with one fruit per consignment. A Gaussian interval with leave-one-consignment-out errors and K − 1 degrees of freedom was not too narrow either, but with two consignments its *t* factor made it {{r_gausslgo_width_2}} times wider than TJ+N, too wide to be useful.

The chronological design, with standards from the five earliest consignments and tests on everything harvested later, is the most realistic and the least favourable case: the later consignments were harvested weeks or seasons later, partly from other regions and cultivars. TJ+N was too narrow in {{r_chrono_tjn_under}} combinations, Gaussian intervals in {{r_chrono_gauss_under}}, ANOVA-PI in {{r_chrono_anova_under}}, and the source-based ASTM interval in all {{r_chrono_n}}. With five consignments, TJ+B could not give a bounded 90% interval; at the 80% level, where five consignments are enough, it covered {{r_chrono_tjb_020}} of the later fruit. No guarantee covers this design, and these numbers show why: early-season standards cannot speak for the late season.

For a laboratory, the lesson is cheap to apply. The cost of a transfer is the number of reference analyses, and that cost is the same whether 20 fruit come from 2 consignments or from 20. Taking one or two samples from each of many batches gives intervals that remain valid for future batches; taking many samples from a few batches does not.

{{table_batch}}

![**Fig. 4.** Coverage of nominal 90% intervals for mango fruit from consignments that supplied no standards, as a function of how 20 (or 15) standards were spread over consignments. Markers: mean over the eight setting-pipeline combinations (season shift; three handheld-instrument pairs; SBC, PDS or no transfer); lines: range. Hollow markers: unbounded intervals. Left: methods that treat samples as the unit; right: methods that treat consignments as the unit. Dashed line: nominal level.](figures/fig_batch_coverage.png){width=16.5cm}
