# The Dedekind--psi approximation: a sharper factorization and its exact obstruction

**Date:** 5 September 2026  
**Status:** rigorous partial result and no-go result; **not** a proof of Erdős
Problem 1060.

Put

\[
 h(n)=n\sigma(n),\qquad
 \psi(n)=n\prod_{p\mid n}(1+p^{-1}),\qquad
 D(n)=n\psi(n).
\]

Noppakaew and Pongsriiam prove that every function
\(n\mapsto n^a\psi(n)^b\), with positive integral \(a,b\), is injective
([*Product of Some Polynomials and Arithmetic
Functions*](https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf),
Theorem 3).  In particular, \(D\) is injective.  This note determines exactly
what that fact gives for a fiber of \(h\), improves the approximation by one
power of each repeated prime, and explains why neither improvement supplies
the missing little-\(o\) estimate.

## 1. The standard Dedekind factorization

If \(p^e\Vert n\), then

\[
 h(p^e)=p^{2e}\frac{1-p^{-(e+1)}}{1-p^{-1}},
 \qquad
 D(p^e)=p^{2e}(1+p^{-1}).
\]

Consequently

\[
 \boxed{h(n)=D(n)\rho(n)},\qquad
 \rho(n)=\prod_{p^e\Vert n}
 \frac{1-p^{-(e+1)}}{1-p^{-2}}.
 \tag{1}
\]

The local factor is one for \(e=1\); for \(e\ge2\) it is strictly between
one and \((1-p^{-2})^{-1}\).  Thus \(\rho(n)\) depends only on the exact
powerful part of \(n\).

If \(h(k)=h(m)=N\), then

\[
 \frac{D(k)}{D(m)}=\frac{\rho(m)}{\rho(k)}.       \tag{2}
\]

In particular, equality of the two \(\rho\)-values implies \(D(k)=D(m)\),
then \(k=m\).  This recovers the powerful-part injection, but does not count
the possible values of the powerful part.

Fix \(z\ge3\), and suppose two members of the fiber have the same exponents
at every prime at most \(z\).  The corresponding local factors cancel in
(2), and

\[
 \left|\log\frac{D(k)}{D(m)}\right|
 \le B_2(z):=\sum_{p>z}-\log(1-p^{-2})
 =O\!\left(\frac1{z\log z}\right).               \tag{3}
\]

For completeness, \(-\log(1-p^{-2})\ll p^{-2}\), and Chebyshev's bound
\(\pi(t)\ll t/\log t\), followed by partial summation, gives

\[
 \sum_{p>z}p^{-2}
 =-\frac{\pi(z)}{z^2}+2\int_z^\infty\frac{\pi(t)}{t^3}\,dt
 \ll\frac1{z\log z}.
\]

The only unconditional gap supplied by integrality is much smaller.  Since
\(1\le D(k)\le N\), distinct members satisfy

\[
 \left|\log\frac{D(k)}{D(m)}\right|
 \ge \log(1+N^{-1})\ge\frac1{N+1}.                \tag{4}
\]

Comparing (3) and (4) would require \(z\log z\gg N\).  That is beyond the
entire relevant range (indeed \(k\le\sqrt N\)).  Thus injectivity plus the
integer spacing of \(D\) does not make the tail vanish.

## 2. A sharper injective rational approximant

The identity

\[
 \frac{1+p^{-1}}{1-p^{-2}}=\frac1{1-p^{-1}}
 \tag{5}
\]

suggests dividing by the second Jordan Euler factor.  It is useful first to
record the global version

\[
 A_0(n)=\prod_{p^e\Vert n}\frac{p^{2e+1}}{p-1}
       =\frac{n^3\psi(n)}{J_2(n)},                 \tag{6}
\]

where \(J_2(n)=n^2\prod_{p\mid n}(1-p^{-2})\) is Jordan's second totient.
The function \(A_0\), although rational-valued, is injective.  Indeed, after
cancelling identical local states in an equality \(A_0(u)=A_0(v)\), let
\(P\) be the largest base prime at which the exponents differ.  Factors
belonging to smaller bases have numerator a power of that smaller prime and
denominator composed of primes smaller than it.  Hence their \(P\)-adic
valuations vanish.  The \(P\)-adic valuation of the remaining local factor is
\(0\) in state zero and \(2e+1\) in state \(e\ge1\), so it determines the
state, a contradiction.

For fibers of \(h\), the squarefree states can be made exact.  Define the
rational multiplicative-by-local-states map

\[
 A(p,0)=1,\qquad A(p,1)=p(p+1),\qquad
 A(p,e)=\frac{p^{2e+1}}{p-1}\quad(e\ge2),
 \qquad A(n)=\prod_{p^e\Vert n}A(p,e).             \tag{7}
\]

### Proposition 1 (third-order powerful-part approximation)

The function \(A:\mathbb N\to\mathbb Q_{>0}\) is injective, and

\[
 \boxed{h(n)=A(n)\vartheta(n)},\qquad
 \vartheta(n)=\prod_{\substack{p^e\Vert n\\e\ge2}}
 (1-p^{-(e+1)}).                                  \tag{8}
\]

Consequently, on each fiber of \(h\), the map \(n\mapsto\vartheta(n)\) is
injective.  If two fiber members agree at every prime at most \(z\), then

\[
 \left|\log\frac{A(k)}{A(m)}\right|
 \le B_3(z):=\sum_{p>z}-\log(1-p^{-3})
 =O\!\left(\frac1{z^2\log z}\right).             \tag{9}
\]

#### Proof

The factorization is local.  It is tautological in states zero and one, while
for \(e\ge2\),

\[
 \frac{p^{2e+1}}{p-1}(1-p^{-(e+1)})
 =p^e\frac{p^{e+1}-1}{p-1}=h(p^e).
\]

For injectivity, cancel identical local states from \(A(u)=A(v)\), and let
\(P\) be the largest remaining base.  If \(P\ge5\), no factor at a smaller
base \(q\) has nonzero \(P\)-adic valuation: for a repeated state its only
numerator prime is \(q\) and its denominator divides \(q-1\); for state one,
\(A(q,1)=q(q+1)\), and \(P\mid q+1\) with \(q<P\) can occur only when
\((q,P)=(2,3)\).  At base \(P\), the possible \(P\)-adic valuations are

\[
 0,\ 1,\ 5,\ 7,\ 9,\ldots
\]

for exponents \(0,1,2,3,4,\ldots\), respectively.  They are distinct, a
contradiction.  Only bases 2 and 3 can remain.

For clarity, the pairs of \((v_2,v_3)\) contributed by the base 2 are

\[
 (0,0),\ (1,1),\ (2a+1,0)\ (a\ge2),
\]

and those contributed by base 3 are

\[
 (0,0),\ (2,1),\ (-1,2b+1)\ (b\ge2).
\]

Their sums determine \((a,b)\) uniquely.  If \(b\ge2\), the parity of the
3-adic valuation first detects whether \(a=1\), then determines \(b\), and
the 2-adic valuation determines the remaining value of \(a\).  The cases
\(b=0,1\) are immediate from the displayed lists.  Hence \(A\) is injective.

Finally, after cancellation of the small-prime states, both tail logarithms
\(-\log\vartheta\) lie in \([0,B_3(z)]\).  Since
\(-\log(1-p^{-3})\ll p^{-3}\), partial summation gives
\(B_3(z)\ll z^{-2}/\log z\).  This proves (9).  \(\square\)

This is a genuine one-power improvement over (3): only repeated input primes
occur, and an exponent-two prime contributes at order \(p^{-3}\), not
\(p^{-2}\).

## 3. Why the sharper approximation still does not close the problem

The price for (9) is that \(A\) is rational-valued.  In lowest terms, the
denominator of \(A(k)\) divides

\[
 \prod_{p^e\Vert k,\ e\ge2}(p-1)
 \le\prod_{p^e\Vert k,\ e\ge2}p
 \le \sqrt{k}\le N^{1/4}.                         \tag{10}
\]

Moreover

\[
 \zeta(3)^{-1}\le\vartheta(k)\le1,
 \qquad N\le A(k)=N/\vartheta(k)\le\zeta(3)N.
\]

Therefore two distinct \(A\)-values in a common fiber have only the general
rational-spacing bound

\[
 \left|\log\frac{A(k)}{A(m)}\right|
 \ge \frac{1}{\zeta(3)N^{3/2}}.                   \tag{11}
\]

Indeed, two reduced rationals with denominators at most \(N^{1/4}\) differ
by at least \(N^{-1/2}\), and \(|\log x-\log y|\ge|x-y|/\max(x,y)\).

For (9) to contradict (11) one would need
\(z^2\log z\gg N^{3/2}\), roughly \(z>N^{3/4+o(1)}\).  But every repeated
base in a preimage already satisfies \(p^2\le k\le\sqrt N\), hence
\(p\le N^{1/4}\).  Thus the metric argument becomes effective only after the
tail is empty for the trivial reason that every possible repeated prime was
fixed.  The extra power of \(p\) in (9) is real, but the loss of integrality
more than absorbs it.

No lower bound stronger than (4), or its rational analogue (11), follows
from injectivity alone.  The following precise clustering lemma shows why a
generic short-interval theorem for these injective values cannot supply the
missing step.

### Proposition 2 (simultaneous rough-value clustering)

Fix \(r\ge1\), \(C>0\), and \(B>0\).  For each sufficiently large \(x\), let
\(\mathcal P_x=\{p:x<p\le2x\}\).  Suppose \(F_1,\ldots,F_r\) are positive
multiplicative functions such that, on primes in this interval,

\[
 |\log F_j(p)|\le C\log x\qquad(1\le j\le r).
\]

Then there is a family \(\mathcal U_x\) of squarefree, \(x\)-rough integers
with

\[
 |\mathcal U_x|
 \ge \exp\!\left((\log2+o(1))\frac{x}{\log x}\right),               \tag{12}
\]

such that for every \(u,v\in\mathcal U_x\) and every \(j\),

\[
 \left|\log\frac{F_j(u)}{F_j(v)}\right|\le x^{-B}.                  \tag{13}
\]

#### Proof

Let \(t=|\mathcal P_x|=(1+o(1))x/\log x\), by the prime number theorem, and
form all \(2^t\) subset products \(u_S=\prod_{p\in S}p\).  For each fixed
\(j\), their logarithms \(\log F_j(u_S)\) lie in an interval of length at
most \(Ct\log x=O(x)\).  Partition each of the \(r\) coordinate intervals
into pieces of length \(x^{-B}\).  The resulting number of boxes is at most
\(O(x^{B+1})^r\), which is polynomial in \(x\).  One box therefore contains

\[
 \frac{2^t}{O(x^{B+1})^r}
 =\exp\!\left((\log2+o(1))\frac{x}{\log x}\right)
\]

subset products.  They form \(\mathcal U_x\) and satisfy (13). \(\square\)

This applies simultaneously to any fixed finite list of the injective maps
\(n^a\psi(n)^b\), \(n^aJ_2(n)^b\), and to \(D\): their local logarithms on
squarefree primes are \(O(\log p)\).  Thus even among rough inputs, a
multiplicative interval of polynomially small width can contain exponentially
many values on the natural \(x/\log x\) scale.  These integers do **not** lie
in one \(h\)-fiber; that is exactly the point.  Closeness and injectivity by
themselves cannot replace an arithmetic theorem using the exact common-target
condition.

## 4. Why iterating the known injective functions does not improve the error

The Noppakaew--Pongsriiam family is algebraically redundant for this purpose:

\[
 n^a\psi(n)^b=n^{a-b}D(n)^b.                      \tag{14}
\]

When \(a=b\), this is merely a power of \(D\); both the logarithmic tail in
(3) and the logarithmic separation are multiplied by the same \(b\), so
nothing improves.  When \(a\ne b\), the uncontrolled factor \(n^{a-b}\)
means that the value is no longer concentrated near a common quantity on an
\(h\)-fiber.

The second Jordan function does identify the only natural second-order
cancellation.  On a prime support, the two available Euler factors are
\(1+p^{-1}\) and \(1-p^{-2}\).  Matching
\((1-p^{-1})^{-1}\) through order \(p^{-2}\) forces the exponents

\[
 (1+p^{-1})^u(1-p^{-2})^v,\qquad u=1,\quad v=-1,                  \tag{15}
\]

and in fact (15) is the exact identity (5).  Hence a negative Jordan power is
unavoidable; it produces the rational function \(A_0=n^3\psi/J_2\), not a
new integer-valued approximant with a stronger gap.  Higher positive powers
of \(n^a\psi^b\) or \(n^aJ_2^b\) do not cancel the next term.

There is also a sharp local-truncation obstruction.  Let

\[
 T_s(p^e)=\sum_{j=0}^{\min(s-1,e)}p^{2e-j},
 \qquad T_s(n)=\prod_{p^e\Vert n}T_s(p^e),                         \tag{16}
\]

the product of the top \(s\) terms of each local block \(h(p^e)\).  The cases
\(s=1\) and \(s=2\) are \(n^2\) and \(D(n)\), respectively, and are
injective.  For every \(s\ge3\), however,

\[
 T_s(12)=h(12)=336=h(14)=T_s(14).                                 \tag{17}
\]

Thus no iteration by taking one more exact geometric-series term can remain
injective.  More generally, every multiplicative local approximant agreeing
with \(h(p^e)\) for all \(e\le2\) inherits the collision (17).  The
exponent-two correction \(1-p^{-3}\) in (8) is therefore the first genuine
obstruction, not an omitted routine term.

## 5. Conclusion

The Dedekind route proves the useful new factorization (8) and improves the
rough powerful-prime tail from \(O((z\log z)^{-1})\) to
\(O((z^2\log z)^{-1})\).  It does **not** prove Erdős Problem 1060.  To turn
it into a proof one still needs an arithmetic separation or entropy theorem
that applies to values in one exact common \(h\)-fiber and is much stronger
than generic integer/rational spacing.  Proposition 2 rules out obtaining
such a theorem merely from the injectivity or short-interval sparsity of any
fixed finite collection of the standard \(\psi\)- and \(J_2\)-approximants;
(17) rules out the obvious next local truncation.

Equivalently, the unsolved issue has moved from an Euler tail of order
\(p^{-2}\) to the exponent-two relations carried by the factors
\(1-p^{-3}\).  Their cross-prime cancellations are the same bounded-exponent
valuation/transition phenomenon isolated elsewhere in the investigation.
