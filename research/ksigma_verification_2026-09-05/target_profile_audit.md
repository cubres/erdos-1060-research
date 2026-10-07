# Target-profile audit

For a fixed target

\[
n=\prod_p p^{a_p},\qquad h(k)=k\sigma(k)=n,
\]

define the target profile of `k` to be the histogram of pairs
\((a_p,v_p(k))\) over all \(p\mid n\).  Put
\(r_a=\#\{p:v_p(n)=a\}\).

## Rigorous profile-count bound

For a fixed `a`, a histogram distributes the `r_a` target primes among the
`a+1` possible input exponents `0,...,a`.  Hence the number of profiles is at
most

\[
Q(n)=\prod_{a\ge1}{r_a+a\choose a}.
\]

Write \(L=\log n\) and take \(T=\lfloor L^{1/3}\rfloor\), for sufficiently
large `n`.  For `a<=T`,

\[
{r_a+a\choose a}\le(r_a+a)^a,
\]

and \(r_a\le L/(a\log2)\), so the logarithm of the product of these factors
is \(O(T^2\log L)\).  For `a>T`, viewing a histogram as the image of an
assignment of `r_a` labelled primes to `a+1` boxes gives

\[
{r_a+a\choose a}\le(a+1)^{r_a}.
\]

Since \(\log(a+1)/a\) is decreasing and
\(\sum_a ar_a\le L/\log2\), the remaining logarithm is at most

\[
\frac{L}{\log2}\frac{\log(T+2)}{T+1}.
\]

Therefore

\[
\log Q(n)=O\bigl(L^{2/3}\log L\bigr)
=o\!\left(\frac{L}{\log L}\right).
\]

Thus injectivity of the profile map on every fiber would imply the desired
Erdos bound.  General injectivity is false: a same-prime-signature odd
collision can be multiplied by a common squarefree CRT/Dirichlet factor that
equalizes the old target valuations.  The count bound itself remains valid.

## Exact finite evidence for the normalized question

In a fixed fiber, equality of the full histogram is equivalent to equality of
the positive subhistogram over `p|k`: for each `a`, the omitted `(a,0)` count
is `r_a` minus the number of positive pairs with first coordinate `a`.

The complete census with `k<100,000,000` and `h(k)<=10^16` retained
81,034,585 inputs and compared all 2,507,580 pairs in 2,374,602 collision
fibers.  It found zero equal-target-profile pairs.

The exact MILP in `target_profile_milp.py` additionally forbids selecting the
same local block `H(p,e)` on both sides.  It uses a one-hot variable for the
common target valuation at each possible input base and binary conjunction
variables to impose equality of every histogram bin.  Exact infeasibility has
been proved in the following bounded universes:

- all prime bases `p<=100`, exponents `e<=3`;
- all prime bases `p<=3000`, exponents `e<=2`.

Runs through `p<=100,e<=5` and `p<=200,e<=3` reached their time limits with no
incumbent and are inconclusive.  None of these finite computations proves the
normalized conjecture.
