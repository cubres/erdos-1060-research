# Obstructions to rough parametric cubefree collisions

Write

\[
 A(x)=x(x+1),\qquad B(x)=x^2(x^2+x+1),\qquad
 T(x)=\frac{B(x)}{A(x)}=\frac{x(x^2+x+1)}{x+1}.
\]

These results do **not** prove a positive reciprocal-mass gap.  They rule out
three natural low-complexity ways in which a counterexample family might have
arisen.

## 1. No affine polynomial template

**Proposition 1.**  Let all proposed input-prime bases be distinct affine
polynomials over the integers which are positive for all sufficiently large
values of the parameter.  There is no normalized nontrivial polynomial
identity between products of the blocks `A(L)` and `B(L)` which can specialize
infinitely often to cubefree prime-base collisions.

The same assertion holds for affine forms in any finite number of parameters,
on a cone on which all the forms tend to positive infinity.

**Proof.**  Put \(\Phi(X)=X^2+X+1\).  For every nonconstant affine form
\(L\), the polynomial \(\Phi(L)\) is irreducible over \(\mathbb Q\).  In one
variable this follows from its discriminant \(-3a^2\), where \(a\) is the
slope of `L`; the multivariate case follows after an invertible linear change
of variables which makes `L` one of the coordinates.

The factor \(\Phi(L)\) in

\[
 B(L)=L^2\Phi(L)
\]

cannot match any factor from an `A`-block, all of whose irreducible factors are
affine.  It must therefore be associated to a factor \(\Phi(M)\) in an
opposite `B`-block.  If

\[
 \Phi(L)=c\Phi(M),
\]

comparison after completing the square,
\(\Phi(X)=(X+1/2)^2+3/4\), gives \(c=1\) and
\(M=L\) or \(M=-L-1\).  The second alternative is incompatible with both
forms tending to positive infinity on the same cone.  Thus the opposite block
has the same base `L`, so it is an identical local block and cancels.

After all `B`-blocks have been cancelled, only squarefree blocks remain.  At
any specialization at which the bases are distinct primes, Gyulev's
squarefree injectivity lemma says that equality of the two products of
`A`-blocks forces the two squarefree inputs to be equal.  Hence a normalized
nontrivial specialization is impossible.  \(\square\)

This proposition rules out an unconditional construction based only on
Dirichlet primes in affine forms.  It does not rule out nonlinear recurrences,
Pell-type subsequences, or identities involving irreducible nonlinear prime
values.

## 2. The smallest transfer is isolated

**Proposition 2.**  For distinct primes \(p,q,r\),

\[
 B(p)A(q)=A(p)A(r)                                      \tag{1}
\]

holds if and only if \((p,q,r)=(2,3,7)\).  This is the collision
\(h(12)=h(14)=336\).

**Proof.**  Cancelling `A(p)` turns (1) into

\[
 (p+1)r(r+1)=p(p^2+p+1)q(q+1).                         \tag{2}
\]

Since \(T(p)>p^2\), equation (2) gives

\[
 r(r+1)>p^2q(q+1)>pq(pq+1),
\]

so \(r>pq\).  In (2), the prime `r` cannot divide `p`, `q`, or `q+1`.
Consequently

\[
 r\mid p^2+p+1.
\]

Write \(p^2+p+1=rd\).  Reducing (2) modulo `p` gives
\(r\equiv-1\pmod p\).  Since \(rd\equiv1\pmod p\), it follows that
\(d\equiv-1\pmod p\), and hence \(d\ge p-1\).  For \(p\ge5\),

\[
 r\le \frac{p^2+p+1}{p-1}=p+2+\frac3{p-1}<2p,
\]

contrary to \(r>pq\ge2p\).

For `p=3`, the bounds force `q=2` and `r=13`, which does not satisfy (2).
For `p=2`, they force `q=3` and `r=7`, and direct substitution verifies
(2).  \(\square\)

## 3. No low-mass same-radical star

The fraction `T(n)` is in lowest terms, because

\[
 n(n^2+n+1)\equiv-1\pmod {n+1}.                        \tag{3}
\]

**Proposition 3.**  Let \(m\ge2\), and let
\(p_1,\ldots,p_m,r\) be distinct primes.  If

\[
 \prod_{i=1}^m\left(1+\frac1{p_i}\right)<2,            \tag{4}
\]

then

\[
 \prod_{i=1}^m T(p_i)\ne T(r).                         \tag{5}
\]

**Proof.**  Put

\[
 P=\prod_i p_i,\quad D=\prod_i(p_i+1),\quad
 N(x)=x(x^2+x+1).
\]

Since \(x^2<T(x)<x^2+1\), (5), if true, would imply `r>P`:
if `r<=P`, then, as `P` is composite, `r<=P-1`, and

\[
 T(r)<r^2+1\le(P-1)^2+1<P^2<\prod_iT(p_i).
\]

Let

\[
 G=\gcd\left(\prod_iN(p_i),D\right).
\]

By (3), comparison of the reduced denominators in (5) gives

\[
 r+1=\frac DG.
\]

But `r>P`, so

\[
 G<\frac D{P+1}<\frac DP
   =\prod_i\left(1+\frac1{p_i}\right)<2.
\]

Thus `G=1` and `r=D-1`.

For every \(p\ge2\),

\[
 \frac{N(p)}{(p+1)^3}
 =1-\frac{2p^2+2p+1}{(p+1)^3}
 <1-\frac1{p+1}.                                      \tag{6}
\]

Choose one `p_j`.  Since there is at least one other prime,
\(D/(p_j+1)\ge3\).  From (6),

\[
 \frac{\prod_iN(p_i)}{D^3}
 <1-\frac1{p_j+1}
 <1-\frac2D.
\]

On the other hand, for `r=D-1`,

\[
 \frac{N(r)}{D^3}
 =1-\frac2D+\frac2{D^2}-\frac1{D^3}
 >1-\frac2D.
\]

Therefore \(N(r)>\prod_iN(p_i)\), contradicting equality of the
numerators after `G=1`.  \(\square\)

In particular, a sequence of same-radical cubefree collisions whose Euler
mass tends to zero cannot have only one `1 -> 2` exponent switch on either
side.  Eventually it must contain at least two upgrades in each direction.

## 4. Exact factor-exhausting cyclotomic cycles do not close

A further common template is to ask for positive integers on a cycle satisfying

\[
 x_{i-1}x_{i+1}=x_i^2+x_i+1.                           \tag{7}
\]

No such finite positive cycle exists: at an index where `x_i` is maximal, the
left side of (7) is at most \(x_i^2\), while the right side is strictly larger
than \(x_i^2\).  Thus a rough family cannot be obtained from a closed chain in
which every \(\Phi_3(x_i)\) is exhausted by its two neighbouring bases.

For an open chain, the exponent-balance matrix for the blocks
\(B(x_i)=x_i^2x_{i-1}x_{i+1}\) is the tridiagonal matrix with diagonal `2`
and adjacent entries `1`; its determinant is `m+1` on a chain of length `m`.
It therefore has no nonzero exact multiplicative relation supported wholly in
the interior.

## Verdict

No exact parametric cubefree collision with all differing base primes tending
to infinity was found.  The propositions above rigorously exclude affine
prime-form identities, the unique three-block transfer except for `12/14`,
same-radical one-sided stars in the low-mass regime, and factor-exhausting
cyclotomic chains.  They do not exclude a branched nonlinear construction with
at least two exponent upgrades on both sides.
