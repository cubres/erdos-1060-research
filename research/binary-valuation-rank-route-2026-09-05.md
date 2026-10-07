# The valuation-rank route for bounded-exponent fibers

This note gives an exact linear-algebra bound for a fiber of

\[
                 h(k)=k\sigma(k),
\]

an exact multiscale version of the bound, and a certified obstruction to two
overly strong forms of a private-prime argument.  It is a reduction, not a
proof of Erdos Problem 1060.

## 1. Categorical valuation-rank lemma

Let

\[
 H(p,e)=p^e(1+p+\cdots+p^e),\qquad H(p,0)=1,
\]

and let

\[
 V=\bigoplus_{\ell\ \operatorname{prime}}\mathbb Q\mathbf e_\ell,
 \qquad
 W(p,e)=(v_\ell(H(p,e)))_\ell\in V.
\]

Fix a finite set `S` of base primes.  At each `p in S`, let `A_p` be a
nonempty set of allowed exponents, and choose a baseline `a_p in A_p`.  Form
the difference columns

\[
 C_{p,e}=W(p,e)-W(p,a_p)
 \quad(p\in S,\ e\in A_p\setminus\{a_p\}).                 \tag{1}
\]

Put

\[
 M=\sum_{p\in S}(|A_p|-1),\qquad
 \rho=\dim_\mathbb Q\operatorname{span}\{C_{p,e}\}.       \tag{2}
\]

**Lemma 1 (categorical rank bound).**  For every positive integer `y`,

\[
 \#\left\{(e_p)\in\prod_{p\in S}A_p:
             \prod_{p\in S}H(p,e_p)=y\right\}
       \le 2^{M-\rho}.                                    \tag{3}
\]

**Proof.**  One-hot encode a state vector by variables `x_(p,e) in {0,1}`
for the nonbaseline states: all the variables in the `p`-block are zero when
`e_p=a_p`, and otherwise exactly one of them is one.  Taking prime
valuations turns the displayed product equation into

\[
                 Cx=b                                      \tag{4}
\]

for a fixed vector `b in V`.  Choose `rho` linearly independent columns of
`C` and call their variables pivot variables.  Projection of the solutions
of (4) to the remaining `M-rho` binary variables is injective.  Indeed, two
solutions with the same nonpivot variables have a difference supported on
the pivot columns; independence of those columns forces all their remaining
differences to be zero.  There are at most `2^(M-rho)` possible nonpivot bit
vectors.  The one-hot restrictions can only reduce this number.  This proves
(3).  \(\square\)

The use of `Q` in (2) is important only for stating ordinary matrix rank.
All columns themselves are integer valuation vectors, so a nonzero minor
modulo any prime is also a valid lower-rank certificate over `Q`.

## 2. Binary cells and conditioning

Suppose every active coordinate `p` has two allowed states
`alpha_p != beta_p`.  Put

\[
 c_p=W(p,\beta_p)-W(p,\alpha_p),
 \qquad
 r=\operatorname{rank}_\mathbb Q\{c_p:p\in S\}.           \tag{5}
\]

Lemma 1 becomes the especially transparent bound

\[
                         |\mathcal B_y|\le 2^{|S|-r}.       \tag{6}
\]

Thus it is rank *deficiency*, not merely the existence of relations, that
matters.  A bounded number of primitive relations is harmless; a linear
number of independent relations would be fatal to this route.

There is also a useful exact conditioning form.  Let `E subset S` be a set
of coordinates which will be fixed explicitly.  On `S setminus E`, define
`M_E` and `rho_E` by (1)--(2), using the exponent values which actually occur
in the family.  Splitting the family according to its state vector on `E`
and applying Lemma 1 in each cell gives

\[
       |\mathcal F|\le R^{|E|}2^{M_E-\rho_E},              \tag{7}
\]

when every exponent is in `{0,...,R-1}`.  Consequently, with

\[
                         B(y)=\frac{\log y}{\log\log y},
\]

the fixed-`R` assertion follows from the following uniform arithmetic
criterion:

\[
 |E|=o_R(B(y)),\qquad M_E-\rho_E=o_R(B(y)).                \tag{8}
\]

This formulation permits all troublesome small base primes or exceptional
local profiles to be put in `E`.

## 3. Exact multiscale accounting

Let `I` be the set of all nonbaseline column labels `(p,e)` outside the
conditioned set, and partition it into any ordered scale blocks

\[
                         I=I_1\sqcup\cdots\sqcup I_J.
\]

Set

\[
 U_j=\operatorname{span}_\mathbb Q\{C_i:i\in I_1\cup\cdots\cup I_j\},
 \quad U_0=0,
\]

and

\[
 \rho_j=\dim U_j-\dim U_{j-1},
 \qquad \delta_j=|I_j|-\rho_j.                            \tag{9}
\]

Then telescoping gives the exact identity

\[
              M_E-\rho_E=\sum_{j=1}^J\delta_j.            \tag{10}
\]

Hence an entropy argument may work one prime scale at a time: it is enough
to prove that the sum of the scale deficiencies in (10) is `o_R(B(y))`.
No independence between scales is being assumed in this statement; the
quotient dimension in (9) accounts exactly for all earlier-scale relations.

Here is a more concrete sufficient condition suitable for witness charging.
For each `j`, choose `G_j subset I_j` and a set `Q_j` of valuation-row primes,
with the row sets `Q_j` pairwise disjoint.  Assume

1. the matrix with rows `Q_j` and columns `G_j` has full column rank; and
2. for `i<j`, every column in `G_j` vanishes on all rows in `Q_i`.

The matrix on row blocks `Q_1,...,Q_J` and column blocks
`G_1,...,G_J` is block lower triangular with full-column-rank diagonal
blocks.  Therefore all the selected columns are independent and

\[
 M_E-\rho_E\le\sum_{j=1}^J(|I_j|-|G_j|).                  \tag{11}
\]

Thus a proof that charges all but `o_R(B(y))` local state columns to such
scale-compatible witnesses would complete the fixed-exponent step.

## 4. Why arbitrary categorical fibers do not reduce freely to pairs

For `R>2`, controlling every two-state box does not by itself control an
arbitrary `R`-state family.  If independently at every coordinate one chooses
a uniformly random two-element subset of `{0,...,R-1}`, then a fixed word is
retained with probability `(2/R)^s`.  Consequently the strongest generic
deduction from a uniform binary-box bound `K_s` is only

\[
                         |\mathcal F|\le (R/2)^sK_s,       \tag{12}
\]

which loses a positive exponential factor.  The same obstruction appears by
counting covers: a binary product box has `2^s` words, so at least `(R/2)^s`
such boxes are needed to cover the full `R`-ary cube.  Formula (12) is sharp
at this purely set-theoretic level, as is seen by taking the family to be the
entire `R`-ary cube.

Three legitimate ways to avoid this loss are:

- use the full categorical rank bound (3);
- prove that only `o(s)` coordinates have more than two occurring states and
  condition those coordinates; or
- prove an arithmetic, rather than generic, cover by `exp(o(s))` binary
  cells.

The abstract incomparable cube `{2,3}^s` from the divisibility-chain
obstruction shows why the third item cannot follow from coordinatewise chain
covering alone.

## 5. Exact audit on the rough-210 cubefree collision

Use the exact certificate
`ksigma_verification_2026-09-05/cubefree_rough210_collision.json`.  Its union
of differing base primes is

\[
\begin{aligned}
S=\{&11,13,17,19,23,31,43,61,83,97,127,271,307,331,\\
    &367,733,5419\}.
\end{aligned}
\]

At each `p in S`, take the left and right exponents in the certificate as the
two allowed states and put

\[
                c_p=W(p,e_p^{\rm right})-W(p,e_p^{\rm left}).
\]

Exact factorization gives

\[
                         \sum_{p\in S}c_p=0.               \tag{13}
\]

Thus the rank is at most 16.  For the first 16 base columns, omitting only
the column for 5419, take the 16 valuation rows

\[
 2,3,5,7,11,13,17,19,23,31,43,83,97,127,271,367.
\]

The determinant of this exact integer minor is `-12`.  Therefore

\[
               \operatorname{rank}_\mathbb Q\{c_p:p\in S\}=16,             \tag{14}
\]

and its nullspace is generated by the all-one relation (13).  Lemma 1 bounds
the specified binary cell at the common target by `2^(17-16)=2`; the two
certified endpoint words attain this bound.  The accompanying checker also
enumerates all `2^17=131072` words in that binary box.

This same example is an exact counterexample to complete private-witness
peeling.  The union of the column supports has 21 valuation rows.  Their
support degrees are

\[
 16,9,2,5,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
\]

in increasing row-prime order.  In particular, no row occurs in a unique
column, so support-degree-one peeling cannot make even its first move.
Nevertheless the actual rank deficiency is only one.  Any successful witness
argument must therefore permit genuine multi-column elimination or quotient
rank, rather than demand a private prime at every stage.

The exact checker is
`ksigma_verification_2026-09-05/verify_rough210_binary_rank.py`; its recorded
output is
`ksigma_verification_2026-09-05/rough210_binary_rank_audit.json`.

## 6. What remains

The missing arithmetic theorem can now be stated without an informal use of
the word entropy: after conditioning `o_R(B(y))` exceptional coordinates,
prove that the categorical local-ratio valuation matrix has rank deficiency
`o_R(B(y))`, uniformly over every bounded-exponent fiber.  The rough-210
example shows that zero deficiency and leaf peeling are false goals, but it
is fully consistent with the required sublinear-deficiency statement.
