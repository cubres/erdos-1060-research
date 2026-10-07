# A reciprocal-mass route for fixed-exponent fibers

This note records a rigorous sufficient condition for the fixed-`R` step in
Erdos Problem 1060, and explains exactly what the divisibility-chain lemma does
and does not prove.  It is a reduction and a partial theorem, not a solution of
the open problem.

Put

\[
  h(k)=k\sigma(k),\qquad
  \mathcal F_R(y)=\{k:h(k)=y,\ v_p(k)<R\text{ for every }p\}.
\]

For distinct `u,v` in one fiber, cancel every identical local block
`H(p,e)=p^e sigma(p^e)` appearing on both sides, and put

\[
 \Delta(u,v)=\{p:v_p(u)\ne v_p(v)\},\qquad
 \lambda(D)=\sum_{p\in D}-\log(1-1/p).
\]

## 1. Euler-mass gap implies sublinear entropy

The following finite form isolates the entire combinatorial argument.  Let
`q_1<...<q_s` be the primes dividing `y`, and suppose that every two distinct
members of a subfamily `A` have

\[
             \lambda(\Delta(u,v))\geq\eta.
\]

If `m` is any integer for which

\[
 \sum_{j=m+1}^s-\log(1-1/q_j)<\eta,                    \tag{0}
\]

then projection to the first `m` exponent coordinates is injective on `A`.
Consequently

\[
                         |A|\leq R^m.                  \tag{0'}
\]

Indeed, two members with the same projection would have their entire
difference support in the tail in (0).  This exact statement has no
asymptotic or uniformity qualification.

**Proposition 1.**  Fix `R`.  Suppose there is a constant `eta_R>0` such that
every normalized nontrivial collision of `R`-free inputs satisfies

\[
       \lambda(\Delta(u,v))\geq \eta_R.                 \tag{1}
\]

Then, for every `theta>exp(-eta_R)`, uniformly in `y`,

\[
 |\mathcal F_R(y)|\leq
 R^{\,\omega(y)^{\theta+o(1)}}.                         \tag{2}
\]

In particular,

\[
 \log |\mathcal F_R(y)|
   =o_R\!\left(\frac{\log y}{\log\log y}\right).
\]

**Proof.**  Write the primes dividing `y` as
`q_1<...<q_s`, and let `p_j` denote the `j`th prime.  Since `q_j>=p_j`,
Mertens' product theorem and the prime number theorem give, for
`m=floor(s^theta)`,

\[
 \begin{aligned}
 \sum_{j=m+1}^s-\log(1-1/q_j)
 &\leq \sum_{j=m+1}^s-\log(1-1/p_j)\\
 &=\log\frac{\log p_s}{\log p_m}+o(1)
  =\log(1/\theta)+o(1)<\eta_R.
 \end{aligned}
\]

Consequently two members of the fiber which agree at `q_1,...,q_m`
must be equal: otherwise their normalized difference is supported in the tail
and contradicts (1).  Projection to the first `m` exponent coordinates is
therefore injective, and each coordinate has at most `R` values.  This proves
(2).  Finally `s=omega(y)=O(log y/log log y)`, and `theta<1`, so the logarithm
of the right side of (2) is `o_R(log y/log log y)`.  QED.

Thus the vague "sublinear entropy" target can be replaced by a concrete
arithmetic question: is the Euler mass of a normalized bounded-exponent
collision bounded away from zero?

## 2. The gap in the support-disjoint sector

**Lemma 2.**  If `a,b>1`, `(a,b)=1`, and `h(a)=h(b)`, then

\[
 \prod_{p\mid ab}\frac p{p-1}>4.                         \tag{3}
\]

**Proof.**  Coprimality and `a sigma(a)=b sigma(b)` give
`sigma(a)=tb` and `sigma(b)=ta` for an integer `t`.  Since both divisor sums
are strictly larger than their arguments, `t>1`, hence `t>=2`.  With
`I(n)=sigma(n)/n`,

\[
 4\leq t^2=I(a)I(b)
   <\prod_{p\mid ab}(1-1/p)^{-1}.
\]

This proves (3).  QED.

Call a fiber **support-compatible** if, for every two of its members and every
prime `p`, positive exponents at `p` are equal.  After identical local blocks
are cancelled, the two residual inputs are then coprime.  Proposition 1 and
Lemma 2 give the following unconditional special case.

**Corollary 3.**  For every fixed `R`, every support-compatible subfamily
`A` of `\mathcal F_R(y)` and every fixed `theta>1/4` satisfies

\[
       |A|\leq R^{\,\omega(y)^{\theta+o(1)}}.             \tag{4}
\]

The exponent `1/4` comes from `eta=log 4`; it is not asserted to be optimal.

## 3. Incorporating the divisibility-chain lemma

Use the following independently checked lemma from the peer manuscript:
if `h(u)=h(v)`, the two indices `v_p(u)+1,v_p(v)+1` are divisibility-comparable
at every differing prime, and

\[
       \prod_{p\in\Delta(u,v)}\frac p{p-1}\leq4,
\]

then `u=v`.

For a subfamily `A`, call a coordinate `p` bad if

\[
 E_p(A)=\{v_p(k)+1:k\in A\}
\]

is not a chain in the divisibility poset on `{1,...,R}`.  Let `Z(A)` be the
set of bad coordinates.

**Proposition 4 (chain-transversal bound).**  For every fixed `theta>1/4`,

\[
 |A|\leq
 R^{\,|Z(A)|+\omega(y)^{\theta+o(1)}}.                  \tag{5}
\]

**Proof.**  Project a member of `A` to its exponent coordinates on `Z(A)` and
on the first `floor(s^theta)` target primes.  If two members have the same
projection, every remaining pair of indices is divisibility-comparable, while
Mertens' theorem makes the Euler product on their differing tail support less
than `4`.  The chain lemma makes the two members equal.  The projection is
injective, giving (5).  QED.

Consequently the fixed-`R` theorem would follow from the still-unproved
assertion `|Z(\mathcal F_R(y))|=o_R(log y/log log y)`.  This is a more precise
chain-transversal version of the missing entropy statement.

## 4. Why a fractional chain cover alone cannot finish

For `R>=3`, the indices `2` and `3` (input exponents `1` and `2`) are
incomparable.  Take `s` arbitrarily large primes, all so large that their
entire Euler product is less than `4`.  In the abstract word space, every two
distinct words in

\[
             \{2,3\}^s
\]

differ at an incomparable coordinate.  Thus all `2^s` words evade the premise
of the chain lemma.  Even restricting to the fixed-weight slice with exactly
`floor(s/2)` symbols equal to `2` leaves

\[
             {s\choose\lfloor s/2\rfloor}
             =\exp((\log2+o(1))s)
\]

words, so merely recording the exponent histogram does not repair the loss.

More directly, every product box whose allowed symbols form a divisibility
chain in each coordinate contains at most one point of this binary cube.
Thus an ordinary cover needs at least `2^s` boxes.  A fractional cover does
not help: summing the `2^s` point-cover constraints shows that its total
weight is at least `2^s`, because each box occurs in at most one of those
constraints.  Hence any such argument based only on coordinatewise
comparability incurs a positive exponential rate.  Arithmetic information
about the incomparable transitions, already the transition `1<->2`, is
essential.

This construction is a countermodel to an inference from the chain lemma, not
an actual `h`-fiber.  Producing or excluding the latter is precisely the open
number-theoretic step.

## 5. Finite counterexample search for the gap

The script `ksigma_verification_2026-09-05/min_euler_mass_collision.py` sets up
the exact valuation-balance MILP and minimizes the Euler mass of an incumbent;
every incumbent is rechecked with arbitrary-precision integers.  In the
cubefree universe of prime bases `7<p<=7000`, the certified optimum is the
known collision coprime to `210`, with 17 differing bases and

\[
 \lambda(\Delta)=0.4519989263271031\ldots,
 \qquad
 \prod_{p\in\Delta}\frac p{p-1}
  =1.5714502613531889\ldots.
\]

This is finite evidence compatible with a positive gap, not a proof of one.

A larger run found another exactly verified cubefree collision using only
base primes greater than `11` (the least is `17`), with

\[
 \lambda(\Delta)=0.40790302090549446\ldots,
 \qquad
 \prod_{p\in\Delta}\frac p{p-1}=1.5036613303846937\ldots.
\]

Its certificate is
`ksigma_verification_2026-09-05/min_euler_mass_u20000_e2_gt11.json`.
The optimizer reached its time limit, so this is a verified incumbent, not a
certified optimum.  In particular, the computation neither proves nor
disproves a uniform positive gap; it warns that the gap cannot presently be
guessed from the first rough collision alone.
