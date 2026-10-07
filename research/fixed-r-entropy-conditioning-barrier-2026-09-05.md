# Fixed-exponent entropy conditioning: the exact chain-lemma consequence

This note isolates what can be proved from the divisibility-chain lemma after
arbitrary conditioning on exponent histograms, prime-size bands, or target
state profiles.  It also gives a sharp abstract obstruction to obtaining
sublinear entropy by iterating those conditionings.

Throughout, input exponents are `< R`, so the local index alphabet is

\[
P_R=\{1,\ldots,R\},\qquad i=e+1,
\]

ordered by divisibility.  Put

\[
w_R=\operatorname{width}(P_R)=\left\lceil\frac R2\right\rceil.
\]

Indeed, the integers in `(R/2,R]` form an antichain of this size, while
partitioning the integers according to their odd part partitions `P_R` into
exactly `ceil(R/2)` chains.

For a prime `q`, write

\[
\lambda_q=-\log(1-1/q)=\log\frac q{q-1}.
\]

We use the following consequence of the chain lemma.  If `x` and `z` are two
distinct members of one actual fiber and their equal local blocks have been
cancelled, then

\[
\bigl(i_q(x),i_q(z)\text{ are comparable for every }q\bigr)
\quad\Longrightarrow\quad
\sum_{q:i_q(x)\ne i_q(z)}\lambda_q>\log4.                 \tag{CL}
\]

## 1. Exact tail encoding

**Proposition 1.**  Let `A` be a fiber, let `S` be its set of target-prime
coordinates, and suppose `S=H disjoint-union T` with

\[
\sum_{q\in T}\lambda_q\le\log4.
\]

Then

\[
|A|\le R^{|H|}w_R^{|T|}.                                \tag{1}
\]

More precisely, choose any partition of `P_R` into chains and let
`c:P_R -> {1,...,w_R}` give the chain containing an index.  The map

\[
x\longmapsto\left((i_q(x))_{q\in H},(c(i_q(x)))_{q\in T}\right)             \tag{2}
\]

is injective on `A`.

**Proof.**  Two members with the same image agree exactly on `H`.  At every
coordinate in `T`, their indices lie in the same chain and hence are
comparable.  After cancelling the common `H` blocks and any common `T`
blocks, the Euler mass of the remaining support is at most the mass of `T`,
which is at most `log 4`.  By (CL), the two members are equal.  Counting the
images gives (1).  QED.

The target valuations give a strictly sharper coordinate-dependent form.
Write `alpha_q=v_q(y)`.  Since every preimage divides `y`, its index at `q`
lies in

\[
P_{R,q}=\{1,\ldots,r_q\},\qquad
r_q=\min(R,\alpha_q+1),
\]

whose width is `w_q=ceil(r_q/2)`.  Repeating the proof with a minimum chain
partition separately at every coordinate gives

\[
|\mathcal F_R(y)|\le
\min_{H:\,\sum_{q\notin H}\lambda_q\le\log4}
\left(\prod_{q\in H}r_q\right)
\left(\prod_{q\notin H}w_q\right).                       \tag{1a}
\]

This is the exact elementary optimization of the head/tail chain encoding.
In particular, target primes of exponent one have `r_q=2,w_q=1` and cost no
tail entropy.  The obstruction begins at target exponent two, where the
allowed indices `2` and `3` are already incomparable.

There is an equivalent entropy statement.  If `X` is uniform on `A` and
`C_q=c(i_q(X))`, injectivity gives the exact identity

\[
\log|A|=H(X_H,C_T)
\le |H|\log R+H(C_T)
\le |H|\log R+\sum_{q\in T}H(C_q).                        \tag{3}
\]

Thus an entropy iteration can succeed only if it supplies new arithmetic
information implying that the total chain-colour entropy on the light tail is
`o(|S|)`.  The chain lemma itself supplies no such information.

## 2. The exact bound after band/profile conditioning

Suppose `T` is partitioned into cells `B_1,...,B_b`; a cell may encode a
dyadic prime band, a fixed target valuation, or their common refinement.
Condition on the exact local-state histogram in each cell.  If

\[
n_{r,a}=|\{q\in B_r:i_q(X)=a\}|,
\qquad
N_{r,j}=\sum_{a:c(a)=j}n_{r,a},
\]

then Proposition 1 gives

\[
|A_{\rm conditioned}|
\le R^{|H|}\prod_{r=1}^b
 { |B_r|\choose N_{r,1},\ldots,N_{r,w_R}}.                \tag{4}
\]

To see this, once the head and the chain-colour word are fixed, (2) gives at
most one fiber member.  In cell `B_r`, exactly the displayed multinomial
number of colour words have the prescribed colour counts.

One may choose a different chain partition in each cell and minimize the
right side.  If `pi_r(a)=n_{r,a}/|B_r|`, define

\[
\Gamma_R(\pi_r)=
 \min_{c:\,c^{-1}(j)\text{ chains}}
 H(c_*\pi_r).
\]

Stirling's formula rewrites (4) as

\[
\log|A_{\rm conditioned}|
\le |H|\log R+
\sum_{r=1}^b |B_r|\Gamma_R(\pi_r)+O_R(b\log(|S|+1)).       \tag{5}
\]

This is the strongest direct deterministic entropy estimate obtained by
encoding every tail coordinate only through a chain containing its state.

Even allowing the chain distribution to depend optimally on the conditioned
profile does not remove the positive rate.  This can be seen exactly in the
cubefree case.  On `m` positive coordinates let `n_1` carry input exponent
one and `n_2=m-n_1` carry input exponent two, and put `rho=n_1/m`.  The two
indices `2,3` are incomparable.  Choosing the chain `{1,2}` with probability
`x` and `{1,3}` with probability `1-x` gives the sharp profile cost

\[
 \inf_{0<x<1}\{-n_1\log x-n_2\log(1-x)\}
   =mH(\rho),                                           \tag{5a}
\]

where `H(rho)=-rho log rho-(1-rho)log(1-rho)`.  Sharpness here is literal for
the abstract constant-composition class: every chain box contains at most one
of its `binom(m,n_1)` words, and
`log binom(m,n_1)=mH(rho)+O(log(m+1))`.

The physical exponent budget is

\[
                  \Omega=n_1+2n_2=m(2-\rho).
\]

If `r=1/phi`, so `r+r^2=1`, the log-sum inequality gives

\[
 H(\rho)\le -\rho\log r-(1-\rho)\log r^2
            =(2-\rho)\log\phi,                         \tag{5b}
\]

with equality at `rho=r`.  Hence

\[
 \max_{0\le\rho\le1}\frac{H(\rho)}{2-\rho}=\log\phi. \tag{5c}
\]

Thus exact type conditioning followed by a type-optimal chain measure
recovers, rather than improves, the peer manuscript's cubefree coefficient
`(log phi)/2` after using
`Omega<=log(y)/(2 log z)`.  Iterating over bands cannot improve a worst-case
uniform estimate: the same maximizing ratio can be placed in every band.

## 3. What Mertens gives in a fixed-`R` fiber

Let `q_1<...<q_s` be the target primes.  Since `q_j` is at least the `j`-th
prime, Mertens' theorem and the prime number theorem imply, uniformly for
`m=s^{theta+o(1)}` with fixed `0<theta<1`,

\[
\sum_{j>m}\lambda_{q_j}
\le \log\frac{\log p_s}{\log p_m}+o(1)
=\log(1/\theta)+o(1).                                    \tag{6}
\]

Consequently, for every fixed `theta>1/4`, Proposition 1 applied with the
first `m=ceil(s^theta)` primes in the head yields

\[
|\mathcal F_R(y)|
\le R^{\lceil s^\theta\rceil}
   w_R^{s-\lceil s^\theta\rceil}.                         \tag{7}
\]

For `R>=3`, this still has entropy `(log w_R+o(1))s`; it is not a
little-`o(s)` estimate.  Formula (5) can improve (7) only when the actual
state distributions have total induced chain-colour entropy `o(s)`.

## 4. Sharp abstract obstruction, including fixed profiles

The positive rate in (7) cannot be removed using only (CL), even with
arbitrarily many iterations of subexponential-valued profile conditioning.

**Proposition 2.**  Fix `R>=3` and put `w=w_R`.  For every `s` there are `s`
primes, all in one dyadic interval, whose total Euler mass is at most `log 4`,
and a family of `w^s` state words satisfying every forbidden-pair conclusion
of (CL).

**Proof.**  Choose a power of two `X` so large that `[X,2X]` contains at least `s` primes
and `2s/(X-1)<log4`, and select `q_1,...,q_s` there.  Let

\[
U=\{\lfloor R/2\rfloor+1,\ldots,R\}.
\]

This is a `w`-element antichain in `P_R`.  Take `\mathcal C_s=U^s`.
Distinct words differ in a coordinate at which their two indices are
incomparable, so the antecedent of (CL) is false for every distinct pair.
The whole family is therefore consistent with all information supplied by
(CL), and has size `w^s`.  QED.

This obstruction survives exact exponent-histogram conditioning.  If `s` is
divisible by `w`, take the balanced constant-composition class

\[
\mathcal C_s^{\rm bal}
=\{x\in U^s:|\{q:x_q=a\}|=s/w\text{ for all }a\in U\}.
\]

Then

\[
|\mathcal C_s^{\rm bal}|
=\frac{s!}{(s/w)!^w}
=\exp\bigl(s\log w-O_R(\log s)\bigr).                    \tag{8}
\]

All coordinates can be assigned the same formal target valuation
`alpha>=2(R-1)`.  Thus (8) also has one fixed histogram of the pairs
`(alpha_q,e_q)`, i.e. one fixed target-state profile, and all base primes lie
in one dyadic band.  The words are divisors of the corresponding formal
target and satisfy the aggregate size constraint `k^2<=y`, though they are
not asserted to be actual preimages.  This is a countermodel to an inference
from chain comparability, profile data, and the size budget, not a
counterexample to Erdos 1060.

The countermodel also lives at exactly the conjecture's entropy scale.  One
may take `X=A s log s`, with a sufficiently large fixed constant `A` (and a
nearby dyadic endpoint): the prime number theorem gives at least `s` primes
in `[X,2X]`, while their total Euler mass is `O(1/log s)`.  For the formal
target

\[
y_s=\prod_{j=1}^s q_j^{2(R-1)}
\]

we then have

\[
\log y_s=(2(R-1)+o(1))s\log s,
\]

while (8) has logarithm `(log w+o(1))s`.  Hence its logarithm is a fixed
positive multiple of `log(y_s)/log log(y_s)`.  Profile counting plus (CL)
therefore encounters precisely a positive main-term coefficient, rather than
only a lower-order artifact.

For `R=3` one can make the obstruction match the peer theorem's cubefree
coefficient while also respecting all of its aggregate size data and any
prescribed finite collection `L` of small valuation rows.  Let `r=1/phi`,
put \(M_L=36\prod_{\ell\in L,\,\ell\ge5}\ell\), choose `s` primes
\(q_i\equiv1\pmod {M_L}\) in `[X,2X]`, with `X` a sufficiently large
constant multiple (depending on `L`) of `s log s`, and put

\[
 m=\left\lfloor\frac{s}{2-r}\right\rfloor,
 \qquad n_1=\lfloor rm\rfloor,
 \qquad n_2=m-n_1.
\]

Fix `s-m` coordinates at exponent zero.  On the other `m` coordinates take
the whole constant-composition class with `n_1` exponent-one states and
`n_2` exponent-two states.  Its logarithmic size is

\[
 mH(r)+O(\log s)=s\log\phi+o(s),                       \tag{8a}
\]

whereas every word has

\[
 \Omega=n_1+2n_2=s+O(1).                               \tag{8b}
\]

Use the single formal target

\[
                 y=2^{n_1}3^{n_2}\prod_{i=1}^s q_i^2. \tag{8c}
\]

Every word divides this target.  It also satisfies `k^2<=y` for all large
`s`.  Indeed `n_0=s-m=n_2+O(1)`.  Relative to
`prod q_i^2`, the worst assignment puts the exponent-two states at the top
of the dyadic interval and the exponent-zero states at the bottom, costing at
most `2 n_2 log 2+O(log X)`; but

\[
 n_1\log2+n_2\log3-2n_2\log2
 =n_1\log2-n_2\log(4/3)\gg s.
\]

Moreover, the congruence calculation in (11) below shows that every word
contributes exactly `n_1` to the 2-adic row and `n_2` to the 3-adic row.
Thus these formal target valuations are not merely slack.  Since
`log X=(1+o(1))log s`,

\[
 \log y=(2+o(1))s\log s,
 \qquad
 \frac{\log y}{\log\log y}=(2+o(1))s.                 \tag{8d}
\]

Thus (8a) equals

\[
 \left(\frac12\log\phi+o(1)\right)
 \frac{\log y}{\log\log y},                           \tag{8e}
\]

exactly the peer chain-packing coefficient.  The exponent histogram, target
valuation profile, Euler-mass tail, and size budget are all fixed throughout
this class.  Again, these formal words need not have a common `h`-value; the
point is that iterating the chain theorem after conditioning on precisely
those data cannot improve its leading constant.

There is a version for an arbitrary multiscale partition.  If the coordinate
cells have sizes `n_1,...,n_b`, choose a most balanced `U`-histogram separately
inside every cell.  The resulting single profile class has size at least

\[
\prod_{r=1}^b\frac{w^{n_r}}{(n_r+1)^w}
\ge
\exp\left(s\log w-wb\log(1+s/b)\right).                  \tag{9}
\]

The first inequality follows because there are at most `(n_r+1)^w`
composition vectors and the largest type class is a balanced one; the second
is concavity of `log(1+x)`.  In particular, every conditioning that records
histograms on `b=o(s)` cells still leaves

\[
\exp((\log w-o(1))s)
\]

abstract words in one profile class.

## 5. Fully adaptive conditioning cannot amplify the lemma

The preceding statement does not depend on how the side information is
organized.  Let

\[
\Phi_s:U^s\longrightarrow Z_s
\]

be the complete transcript of any adaptive sequence of exponent-histogram,
band-histogram, or state-profile queries.  If
`|Phi_s(U^s)|=exp(o(s))`, then by the pigeonhole principle some transcript
class has size

\[
\frac{w^s}{|\Phi_s(U^s)|}
=\exp((\log w-o(1))s).                                   \tag{10}
\]

Every subset of `U^s` still satisfies the (CL) forbidden-pair condition
vacuously.  Therefore no iteration whose total transcript has `o(s)` bits can
force `o(s)` residual entropy from the chain lemma.  Conversely, a transcript
fine enough to make every class subexponential must itself take
`exp((log w-o(1))s)` values, so summing over transcripts restores the same
positive exponential rate.

The corresponding fractional-cover obstruction is exact.  A coordinatewise
chain box has the form `C_1 times ... times C_s`, with every `C_i` a chain in
`P_R`.  Since a chain meets `U` in at most one point, such a box meets `U^s`
in at most one word.  If nonnegative box weights fractionally cover `U^s`,
summing the point-covering inequalities over its `w^s` words proves that the
total box weight is at least `w^s`.  Singleton boxes attain this.  Thus the
fractional chain-box covering number, as well as the integral one, is exactly
`w^s`; random or fractional chain choices have the same positive rate.

For example, one histogram query has at most `(s+1)^R` outcomes.  Thus at
least `Omega_R(s/log s)` such queries are information-theoretically necessary
even to distinguish the antichain cube up to subexponential classes, and the
number of resulting transcripts is then already exponential.

The obstruction also survives conditioning on any prescribed finite set of
small-prime valuation equations.  Let `L` be a finite set of row primes and
put

\[
 M=36\prod_{\substack{\ell\in L\\\ell\ge5}}\ell.
\]

By the prime number theorem in the fixed progression `1 mod M`, for every
`s` there is a sufficiently large dyadic interval containing `s` distinct
primes \(q_i\equiv1\pmod M\); the interval can be taken so large that
their total Euler mass is below `log 4`.  For every such base `q`, direct
congruence calculation gives

\[
\begin{array}{c|cc}
 &v_\ell(H(q,1))&v_\ell(H(q,2))\\ \hline
\ell=2&1&0\\
\ell=3&0&1\\
\ell\in L,\ \ell\ge5&0&0.
\end{array}                                             \tag{11}
\]

Indeed, `q congruent to 1 mod 4` makes `v_2(q+1)=1`, while
`q^2+q+1` is odd; `q congruent to 1 mod 9` makes
`v_3(q^2+q+1)=1` and `3` does not divide `q+1`; and for `ell>=5`, the two
relevant residues are `2` and `3` modulo `ell`.  Therefore all words with a
fixed number of exponent-one and exponent-two states make exactly the same
total contribution to every row in `L`.  Exact conditioning on those
valuation sums, the exponent histogram, the dyadic band, and the Euler tail
still leaves the exponential constant-composition class.

This remains a method countermodel, not an actual common `h`-fiber.  It also
identifies the only possible multiscale escape: the number or logarithmic
weight of valuation rows used must grow with `s`, and one must exploit the
resulting modulus/prime-size cost.  The chain lemma contains no estimate that
performs that tradeoff.

In fact, "finite" can be strengthened to a slowly growing row set without
changing the leading entropy scale.  Fix any constant `c>0`, and let `L_s`
be the first

\[
 t(s)=\left\lfloor
 c\frac{\log\log s}{\log\log\log s}\right\rfloor       \tag{12}
\]

primes at least five.  For

\[
 M_s=36\prod_{\ell\in L_s}\ell
\]

the prime number theorem and Chebyshev's theta estimate give

\[
 \log M_s=(c+o(1))\log\log s,
 \qquad M_s=(\log s)^{c+o(1)}.                          \tag{13}
\]

Take `X=K phi(M_s)s log s`, where `K` is a sufficiently large fixed
constant.  Since `log X=(1+o(1))log s` and
`M_s<=(log X)^{c+1}` for large `s`, the Siegel--Walfisz theorem, used with
any fixed exponent larger than `c+1`, gives

\[
 \pi(2X;M_s,1)-\pi(X;M_s,1)
 =(1+o(1))\frac{X}{\varphi(M_s)\log X}>s.               \tag{14}
\]

Selecting the bases from this progression again gives total Euler mass
`O(s/X)=o(1)` and `log q_i=(1+o(1))log s`.  Consequently the sharp cubefree
construction (8a)--(8e) simultaneously neutralizes `t(s)->infinity` exact
valuation rows and retains the coefficient `(log phi)/2`.  Thus even a
slowly growing initial block of valuation equations cannot amplify the chain
argument to little-`o`; substantially more global arithmetic information is
required.

## 6. A fiber-aware finite warning

The abstract obstruction is not merely caused by allowing arbitrary state
words.  The exact normalized cubefree relation recorded in
`ksigma_verification_2026-09-05/min_euler_mass_u7000_e2_gt7.json` has:

* equal `h`-values;
* no identical local block on the two sides;
* all input base primes greater than `7`;
* the same exponent histogram (eight exponent-`1` blocks and four
  exponent-`2` blocks on each side); and
* Euler product `1.5714502613531889... < 4` on the differing bases.

Hence even for an actual normalized fiber, roughness, small Euler mass, and an
exact exponent histogram do not imply uniqueness.  This finite relation does
not produce an asymptotically large fiber and therefore is not a
counterexample to the desired estimate.

## Conclusion

The exact output of multiscale conditioning is (2)--(5).  For `R>=3`, the
divisibility poset has a nontrivial antichain, and that antichain has positive
zero-error capacity `log w_R` per unconstrained coordinate.  Histogram and
band conditioning of subexponential total complexity cannot lower this rate.
To prove the fixed-`R` theorem one needs an additional arithmetic statement
which controls the incomparable transitions themselves; no iteration of the
chain lemma can manufacture that statement.
