# Cyclotomic audit of the fixed-exponent Euler-mass gap

## Status

Let

\[
 H(p,e)=p^e\sigma(p^e),\qquad
 \lambda(D)=\sum_{p\in D}-\log(1-1/p).
\]

The proposed assertion is that, for every fixed `R`, there is an
`eta_R>0` such that every nontrivial normalized equality

\[
 \prod_pH(p,a_p)=\prod_pH(p,b_p),\qquad 0\leq a_p,b_p<R,
\]

satisfies `lambda({p:a_p!=b_p})>=eta_R`.  The work below neither proves nor
disproves this assertion.  It does prove two necessary-structure lemmas,
finds a rougher exact cubefree collision, and identifies a classical theorem
which shows why largest-prime descent plus Zsigmondy cannot establish the
gap by itself.

## 1. Exact cross-multiplier reduction

After equal local blocks have been cancelled, put

\[
 u=\prod_pp^{a_p},\quad v=\prod_pp^{b_p},\quad
 g=(u,v),\quad A=u/g,\quad B=v/g.
\]

Then `(A,B)=1`, and `h(u)=h(v)` is equivalent to

\[
 A\sigma(u)=B\sigma(v).
\]

Consequently there is an integer `t` such that

\[
 \sigma(u)=Bt,\qquad \sigma(v)=At.                 \tag{1}
\]

Writing `I(n)=sigma(n)/n` and `rho=t/g`, (1) gives the exact identity

\[
 I(u)I(v)=\rho^2.                                   \tag{2}
\]

Let `D=supp(u) union supp(v)` and `S=supp(u) intersect supp(v)`.  Since

\[
 I(p^e)<(1-1/p)^{-1},
\]

(2) implies

\[
 0<\log\rho
 <\frac{\lambda(D)+\lambda(S)}2
 \leq\lambda(D).                                   \tag{3}
\]

The first inequality is strict because neither residual input is `1` and
each nontrivial divisor sum is larger than its argument.  In particular, a
countersequence with `lambda(D)->0` would have

\[
 \frac tg\longrightarrow1.
\]

As `t` and `g` are integers and `t>g`, it would also have

\[
 g\geq\frac1{e^{\lambda(D)}-1}\longrightarrow\infty. \tag{4}
\]

Thus any failure of the gap must be driven by an increasingly large common
input divisor carrying unequal exponents.  It cannot come from disjoint
supports.  Indeed, if `S` is empty, then `g=1`, `t>=2`, and now every base
occurs only once in `I(u)I(v)`, so

\[
 4\leq t^2=I(u)I(v)<e^{\lambda(D)};
\]

hence `lambda(D)>log 4`.

There is a second exact consequence which is useful in testing possible
counterfamilies.  Since `h(n)=n^2 I(n)`, equality also gives

\[
 \left(\frac AB\right)^2=\frac{I(v)}{I(u)}.
\]

Therefore

\[
 \left|\log\frac AB\right|<\frac{\lambda(D)}2.       \tag{4a}
\]

The coprime integers `A` and `B` are unequal in a nontrivial collision.  If,
say, `A>B`, then `A/B>=1+1/B`; hence

\[
 \min(A,B)>\frac1{\exp(\lambda(D)/2)-1}.             \tag{4b}
\]

Thus a countersequence would require both a huge common divisor `g` and two
huge coprime products of the unmatched prime-power increments which are
exceptionally close to one another.

## 2. What cyclotomic factorization actually yields

For exponents `a,b`,

\[
 \frac{H(p,a)}{H(p,b)}
 =p^{a-b}
  \frac{\prod_{d\mid a+1,\ d>1}\Phi_d(p)}
       {\prod_{d\mid b+1,\ d>1}\Phi_d(p)}.          \tag{5}
\]

The common cyclotomic factors in (5) are exactly those with
`d | gcd(a+1,b+1)`, consistently with

\[
 \gcd(\sigma(p^a),\sigma(p^b))
 =\sigma\!\left(p^{\gcd(a+1,b+1)-1}\right).         \tag{6}
\]

For fixed `R`, all indices in (5) are at most `R`.  Zsigmondy's theorem
usually supplies a primitive divisor of each residual `Phi_d(p)`.  When that
primitive divisor `q` does not divide `d`, it satisfies

\[
 \operatorname{ord}_q(p)=d,\qquad q\equiv1\pmod d.  \tag{7}
\]

But (7) makes `q` private to the exponent index, not to the base `p`.
The same `q` can divide `Phi_d(r)` for another base `r`, and equalities of
products permit exactly such cross-base matching.  Zsigmondy therefore does
not create a leaf that can automatically be peeled from the valuation
relation.

The known greatest-prime-factor theorem for a fixed polynomial is also too
weak for this purpose.  Shorey and Tijdeman prove, in particular, lower
bounds of logarithmic-logarithmic size for the greatest prime factor of
suitable polynomial values.  Even a much larger factor is not forced to be
an input base: it may be matched by a cyclotomic value on the other side.
Likewise, fixed-`S` unit-equation theorems do not apply, because both the set
of target primes and the number of factors vary in the proposed gap.

There is an additional reason that a blanket multiplicative-independence
argument cannot work.  Drungilas and Dubickas, *Multiplicative dependence of
shifted algebraic numbers*, Colloq. Math. 96 (2003), Theorem 1, prove that for
every quadratic algebraic number `alpha` and every integer cutoff `t`, the
set `{alpha+j:j>=t}` has a nontrivial product relation of length at most eight.
Taking `alpha` to be a primitive cube root of unity and then taking norms
gives exact relations among at most eight arbitrarily far-out integer values
of `Phi_3`.  Their construction does not give a prime-base counterexample: in
the displayed parametrization in their proof one pair of arguments is
consecutive, so both cannot be odd primes.  It nevertheless proves that
setwise independence of cyclotomic values at general integer arguments is
false, not merely unavailable.

Primary source:
https://www.impan.pl/shop/en/publication/transaction/download/product/86849

## 3. A rigorous incidence-core obstruction

For a normalized collision make a bipartite graph.  One class consists of
the side-labelled selected local blocks `H(p,e)`; the other consists of all
primes dividing those blocks.  Join a block to a prime when the prime divides
the block.  Edge multiplicities are ignored in the graph, though retained in
the valuation equality.

**Lemma.** Every connected component of this incidence graph has cycle rank
at least two.  Equivalently, if a component has `E` edges and `V` vertices,
then

\[
 E-V+1\geq2.                                         \tag{8}
\]

**Proof.** Every prime-row is incident with a block on each side, since its
total left and right valuations agree.  Thus each prime-row has degree at
least two.  Every block has degree at least two: it contains its base `p`,
and `sigma(p^e)>1` has a prime factor different from `p`.

Suppose a connected component had cycle rank one.  A connected unicyclic
graph of minimum degree two is a simple cycle, so every vertex would have
degree exactly two.  At each prime-row its two incident blocks must lie on
opposite sides and must contain that prime to the same valuation.

Mark the base-prime incidence of each block as a base edge and its other
edge as a sigma edge.  A row cannot join two base edges: the two blocks would
then have the same base prime, and valuation equality would force the same
exponent, contrary to cancellation of identical local blocks.  Around the
cycle, the number of rows joining two base edges equals the number joining
two sigma edges (count base-edge endpoints).  Hence neither type occurs;
every row joins one base edge to one sigma edge.

It follows that the blocks can be cyclically ordered so that

\[
 \sigma(p_i^{e_i})=p_{i+1}^{e_{i+1}}
\]

at every step (the equality of exponents here is the valuation equality at
the degree-two row).  But

\[
 p_{i+1}^{e_{i+1}}=\sigma(p_i^{e_i})>p_i^{e_i},
\]

which is impossible around a finite directed cycle.  This proves (8).
`QED`

Thus a genuine collision requires a branched, globally balanced cyclotomic
core.  A single dependency cycle, even one made entirely from primitive
cyclotomic divisors, is insufficient.

## 4. Mills's theorem severely limits the local-cycle strategy

W. H. Mills proved in Theorem 3 of *A system of quadratic Diophantine
equations*, Pacific J. Math. 3 (1953), 209--220, that positive integers `x,y`
satisfy

\[
 x\mid y^2+y+1,\qquad y\mid x^2+x+1                 \tag{9}
\]

if and only if they are consecutive terms of

\[
 1,1,3,13,61,291,1393,\ldots,                       \tag{10}
\]

where

\[
 x_{n+1}=5x_n-x_{n-1}-1,
 \qquad x_{n-1}x_{n+1}=x_n^2+x_n+1.                 \tag{11}
\]

For completeness, the descent is short.  If `1<x<y` satisfies (9), set
`z=(x^2+x+1)/y`.  Then `0<z<x`.  From `yz congruent 1 (mod x)` and
`y^2+y+1 congruent 0 (mod x)`, multiplication by `z^2` gives

\[
 z^2+z+1\equiv0\pmod x.
\]

Thus `(z,x)` again satisfies (9), and descent reaches `(1,1)` or `(1,3)`.
Reversing the step gives (10)--(11).

The sequence contains the consecutive prime terms

\[
 p=22419767768701,qquad q=107419560853453.
\]

They satisfy

\[
 \Phi_3(p)=4679277990051\,q,
 \qquad
 \Phi_3(q)=p\,514678036498563.                       \tag{12}
\]

Hence each prime is a primitive order-three divisor of the other prime's
cyclotomic value.  Nevertheless

\[
 \log\frac p{p-1}+\log\frac q{q-1}
 =5.391278647451121368\ldots\times10^{-14}.          \tag{13}
\]

This is not an `h`-collision.  Also, one prime pair does **not** disprove a
positive lower bound for prime reciprocal cycles: such a lower bound could be
smaller than (13).  What (10)--(13) rigorously show is more limited but still
important.  Mills gives reciprocal order-three cycles at arbitrarily large
*integer* bases, and an actual prime pair already drives the local Euler cost
below `5.4e-14`.  Thus the order/divisibility conditions alone give no useful
mass charge; a proof of the proposed gap must additionally use primality,
global valuation balance, and the branching forced by (8).

The exact arithmetic and deterministic 64-bit primality checks for (12)--
(13) are in `ksigma_verification_2026-09-05/verify_mills_phi3_prime_cycle.py`.

Primary source:
https://msp.org/pjm/1953/3-1/pjm-v3-n1-p15-p.pdf

## 5. A rougher exact cubefree collision

An exact MILP discovery followed by arbitrary-precision reconstruction gives
a normalized cubefree collision with all input bases greater than `17`.
It has 75 differing bases, minimum base `19`, maximum base `38971`, and

\[
 \lambda(D)=0.42735407613039728\ldots,
 \qquad e^{\lambda(D)}=1.533195433533326\ldots.       \tag{14}
\]

The certificate is

`ksigma_verification_2026-09-05/rough_gt17_u50000_e2_disjoint_trial.json`,

and the independent standard-library verifier is

`ksigma_verification_2026-09-05/verify_cubefree_rough17.py`.

This collision does not improve the best mass incumbent
`0.40790302090549446...`, whose minimum base is `17`.  It does show that no
proof can force a cubefree collision to contain one of the primes at most
`17`.

For comparison, the old minimum-base-17 certificate has one connected
incidence component of cycle rank 84; the new minimum-base-19 certificate
has one connected component of cycle rank 198.  These exact figures
illustrate the distinction between a tiny local cyclotomic cycle and the
large globally balanced core required by an actual collision.

## 6. Exact remaining lemma

The sharp unresolved statement after the classical tools are exhausted is:

> For fixed `R`, every branched, globally valuation-balanced signed selection
> of distinct local states `H(p,e)`, with at most one state per base on each
> side and with no identical state on both sides, has base Euler mass bounded
> away from zero.

This is equivalent to the proposed gap, but its formulation records the two
features that Zsigmondy and largest-prime descent fail to provide:

1. balance of **all** valuations, not merely an order relation along one
   primitive-divisor cycle; and
2. control of a core with cycle rank at least two, not merely existence of a
   dependency cycle.

No theorem in the literature checked here supplies that global conclusion.
In particular:

- Zsigmondy/Birkhoff--Vandiver provides primitive divisors but not
  cross-base uniqueness;
- Mills provides arbitrarily large integer reciprocal order-three cycles, and
  an explicit prime cycle of Euler mass below `5.4e-14`, but no prime
  counterfamily;
- Shorey--Tijdeman controls the size of a prime factor of one polynomial
  value, not the matching of factors between two varying products;
- Madritsch--Ziegler proves multiplicative independence of certain individual
  algebraic cyclotomic bases, which does not imply multiplicative
  independence of arbitrary products of their rational norms; and
- Drungilas--Dubickas proves that arbitrary far-out quadratic shifts, hence
  their quadratic norms, actually admit bounded-length product relations;
  their construction does not specialize all arguments to primes;
- standard `S`-unit bounds require a fixed `S`, whereas `S` varies here.

Accordingly, citing any of these results as a proof of a positive `eta_R`
would leave a genuine logical gap.
