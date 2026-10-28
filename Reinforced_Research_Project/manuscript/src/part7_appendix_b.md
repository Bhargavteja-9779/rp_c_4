
# Appendix B. Batch-level validity (Proposition 2) {.unnumbered}

**Setting.** The target population consists of batches (production lots, harvest consignments). Let $B_1,\dots,B_{K+1}$ be batches drawn so that they are exchangeable, for example at random from the population of batches. Within batch $k$, let $Z_{k1},\dots,Z_{kn_g}$ be drawn so that, conditionally on the batch, they are exchangeable, for example at random from the batch. The standards are the $Kn_g$ samples of batches $1,\dots,K$. The future routine sample is $Z_{K+1,1}$. The other members of batch $K+1$ are hypothetical and are used only in the argument.

The transfer algorithm $\mathcal{T}$ is symmetric in its input samples. For index sets of batches $S$, write $\mu_S,\sigma_S$ for the deployed predictor and difficulty function fitted on the standards of the batches in $S$. For $k\neq l$, let $-kl$ denote all batches except $k$ and $l$.

**Proposition 2 (TJ+G).** Define the batch scores
$$S_{kl}=\max_{j\le n_g}\frac{|y_{kj}-\mu_{-kl}(\mathbf{x}^T_{kj})|}{\sigma_{-kl}(\mathbf{x}^T_{kj})},\qquad S_k=S_{k,K+1},$$
and the interval
$$\hat C_G(\mathbf{x})=\big[\hat q^-_\alpha\{\mu_{-k}(\mathbf{x})-\sigma_{-k}(\mathbf{x})S_k\},\ \hat q^+_\alpha\{\mu_{-k}(\mathbf{x})+\sigma_{-k}(\mathbf{x})S_k\}\big],$$
where the quantiles are taken over the $K$ batches with the ranks of Eq. (4) ($m$ replaced by $K$). Then $\Pr\{y_{K+1,1}\in\hat C_G(\mathbf{x}^T_{K+1,1})\}\ge1-2\alpha$.

*Proof.* Let $\mathbf{x}=\mathbf{x}^T_{K+1,1}$.

- **Step 1 (miscoverage implies lost comparisons).** If $y_{K+1,1}\notin\hat C_G(\mathbf{x})$, the argument of Appendix A, Step 2 gives
  $$|y_{K+1,1}-\mu_{-k}(\mathbf{x})|/\sigma_{-k}(\mathbf{x})>S_{k,K+1}$$
  for at least $(1-\alpha)(K+1)$ batches $k$.
- **Step 2 (bound by the batch score).** Since $\mu_{-k}=\mu_{-(K+1),k}$ is fitted without batches $k$ and $K+1$, the left-hand side is one of the terms of the maximum defining $S_{K+1,k}$. Hence $S_{K+1,k}>S_{k,K+1}$ for at least $(1-\alpha)(K+1)$ indices, i.e. batch $K+1$ is *strange* in the sense of Appendix A, Step 3.
- **Step 3 (exchangeability).** $S_{kl}$ is a symmetric function of the members of batch $k$. The batches are exchangeable and $\mathcal{T}$ is symmetric, so the law of the matrix $(S_{kl})$ is invariant under simultaneous permutations of the batch indices.
- **Step 4 (counting).** The tournament lemma of Barber et al. [@barber2021] bounds the expected number of strange batches by $2\alpha(K+1)$. Therefore $\Pr\{\text{batch }K+1\text{ strange}\}\le2\alpha$. $\square$

**Remarks.**

1. **One standard per batch.** With $n_g=1$, TJ+G coincides with TJ+. Ordinary TJ+ is therefore valid for samples from *new* batches when every standard comes from a different, randomly drawn batch.
2. **The hierarchical jackknife+.** The hierarchical jackknife+ of Lee, Barber & Willett [@lee2026] uses the same leave-one-batch-out fits. It weights each member score by $1/((K+1)n_k)$ and places a mass $1/(K+1)$ at $\pm\infty$, with the same $1-2\alpha$ guarantee. TJ+H is its instantiation for the transfer step. It is less conservative than the maximum score of TJ+G when $n_g>1$. We use TJ+H as the primary batch-level construction and claim no new conformal methodology.
3. **Number of batches.** Both constructions give finite bounds only if $\lceil(1-\alpha)(K+1)\rceil\le K$, i.e. $K\ge9$ batches at $\alpha=0.10$, $K\ge19$ at $\alpha=0.05$ and $K\ge4$ at $\alpha=0.20$, whatever the number of standards per batch. The number of distinct batches, not the number of standards, determines whether a valid statement for new batches can be made.
4. **Samples from batches that supplied standards.** For routine samples from such batches, neither construction is tailored. Prediction sets for a new observation from an already observed group have been studied for hierarchical models [@dunn2023] and are not pursued here.
