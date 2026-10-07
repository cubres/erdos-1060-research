# Local gcd cancellation for bounded-exponent collisions of \(k\sigma(k)\)

**Date:** 5 September 2026  
**Status:** rigorous reduction and obstruction analysis; **not** a proof of Erdős
Problem 1060.

This note studies a normalized collision

\[
        h(u)=u\sigma(u)=v\sigma(v)=h(v),\qquad u\ne v,
\]

after every prime power occurring with the same exponent in \(u\) and \(v\)
has been removed from both sides.  Thus, if

\[
 u=\prod_{p\in D}p^{a_p},\qquad
 v=\prod_{p\in D}p^{b_p},
\]

then \(a_p\ne b_p\) for every \(p\in D\), with exponent zero allowed.  This
normalization is legitimate because \(h\) is multiplicative and identical
local factors \(h(p^e)\) cancel.

The main exact output is a rational-square identity.  It recovers the peer
manuscript's divisibility-chain lemma when its denominator is one and exposes
precisely why the same integrality argument does not extend to incomparable
exponent indices.

## 1. Exact local normal form

Write

\[
 S_e(p)=1+p+\cdots+p^e=\frac{p^{e+1}-1}{p-1},
 \qquad H_e(p)=p^eS_e(p).
\]

For one differing coordinate, let \(a>b\geq0\), put

\[
 d=(a+1,b+1),\qquad \delta=a-b,
\]

and define

\[
 G=S_{d-1}(p),\qquad U=\frac{S_a(p)}G,
 \qquad V=\frac{S_b(p)}G.
\tag{1}
\]

The classical identity

\[
 \gcd(S_a(p),S_b(p))=S_{(a+1,b+1)-1}(p)
\tag{2}
\]

follows immediately from
\(\gcd(p^m-1,p^n-1)=p^{(m,n)}-1\).  Consequently
\((U,V)=1\), \(p\nmid UV\), and

\[
 \frac{H_a(p)}{H_b(p)}=p^\delta\frac UV.
\tag{3}
\]

Cyclotomically,

\[
 U=\prod_{\substack{r\mid a+1\\r\nmid b+1\\r>1}}\Phi_r(p),
 \qquad
 V=\prod_{\substack{r\mid b+1\\r\nmid a+1\\r>1}}\Phi_r(p).
\tag{4}
\]

Formula (4) is an exact quotient identity.  The coprimality assertion comes
from (2), not from an assertion that arbitrary numerical cyclotomic values are
pairwise coprime.

## 2. The defect-square identity

For every \(p\in D\), let \(a_p^+=\max(a_p,b_p)\),
\(a_p^-=\min(a_p,b_p)\), and set

\[
 d_p=(a_p^++1,a_p^-+1),\quad
 \delta_p=a_p^+-a_p^-,\quad
 r_p=a_p^-+1-d_p\geq0.
\tag{5}
\]

Use (1) to define \(G_p,U_p,V_p\) with \(a=a_p^+\) and
\(b=a_p^-\).  Let \(P_+\) be the bases at which \(u\) has the larger
exponent and \(P_-\) those at which \(v\) has the larger exponent.  Put

\[
\begin{aligned}
 A&=\prod_{p\in P_+}p^{\delta_p},
 &B&=\prod_{p\in P_-}p^{\delta_p},\\
 X&=\prod_{p\in P_+}U_p\prod_{p\in P_-}V_p,
 &Y&=\prod_{p\in P_+}V_p\prod_{p\in P_-}U_p.
\end{aligned}
\tag{6}
\]

If \(g_0=\prod_{p\in D}p^{a_p^-}\) and
\(\Gamma=\prod_{p\in D}G_p\), then

\[
 u=g_0A,\quad v=g_0B,\quad
 \sigma(u)=\Gamma X,\quad \sigma(v)=\Gamma Y.
\]

Thus \(h(u)=h(v)\) is exactly

\[
                     AX=BY.                         \tag{7}
\]

Since \((A,B)=1\), there is a positive integer \(c\) such that

\[
                     X=cB,\qquad Y=cA.              \tag{8}
\]

Define the **index-defect divisor**

\[
                     C=\prod_{p\in D}p^{r_p}.       \tag{9}
\]

Notice that \(r_p\leq a_p^-\), so \(C\mid g_0\), while (8) shows that
\(c\mid X\).  In particular, both \(C\) and \(c\) divide the common target
\(h(u)=h(v)\).

**Proposition 1 (exact defect-square identity).**  With the preceding
notation,

\[
 \boxed{
 \left(\frac cC\right)^2
 =\prod_{p\in D}
 \frac{(1-p^{-(a_p^++1)})(1-p^{-(a_p^-+1)})}
      {(1-p^{-d_p})^2}.}
\tag{10}
\]

Every local factor on the right is strictly larger than one.  Consequently

\[
 1<\frac cC
 <\prod_{p\in D}(1-p^{-d_p})^{-1},                 \tag{11}
\]

and, because \(c,C\) are integers,

\[
 \boxed{
 \prod_{p\in D}(1-p^{-d_p})^{-1}>1+\frac1C.}
\tag{12}
\]

**Proof.**  Multiplying the two equations in (8) gives

\[
 c^2=\frac{XY}{AB}
     =\prod_{p\in D}\frac{U_pV_p}{p^{\delta_p}}.
\tag{13}
\]

For a local pair \(a>b\),

\[
 \frac{S_a(p)}{S_{d-1}(p)}
 =p^{a+1-d}\frac{1-p^{-(a+1)}}{1-p^{-d}},
\]

and similarly with \(b\).  Since

\[
 (a+1-d)+(b+1-d)-(a-b)=2(b+1-d)=2r,
\]

substitution in (13) proves (10).  We have
\(d_p\leq a_p^-+1<a_p^++1\).  If equality holds in the first inequality,
one numerator factor in (10) equals \(1-p^{-d_p}\) and the other is larger;
if it is strict, both are larger.  Hence each quotient in (10) is greater
than one.  On the other hand, its positive square root is strictly less than
\((1-p^{-d_p})^{-1}\), because both numerator factors are less than one.
This proves (11).  Finally \(c/C>1\) and integrality give \(c\geq C+1\),
which combined with (11) proves (12).  \(\square\)

## 3. Exact recovery of the divisibility-chain obstruction

The condition \(r_p=0\) is equivalent to

\[
 d_p=a_p^-+1,
\]

which is equivalent to
\(a_p^-+1\mid a_p^++1\).  Therefore \(C=1\) if and only if the two
exponent indices are divisibility-comparable at every differing coordinate.

In that case, the local factor in (10) simplifies to

\[
 \frac{1-p^{-(a_p^++1)}}{1-p^{-(a_p^-+1)}}
 <(1-p^{-1})^{-1}.
\]

As \(c\) is now an integer greater than one, (10) yields

\[
 4\leq c^2
 <\prod_{p\in D}\frac p{p-1}.                       \tag{14}
\]

Thus

\[
 \prod_{p\in D}\frac p{p-1}\leq4
 \quad\Longrightarrow\quad u=v
\]

under coordinatewise index comparability.  This is precisely the arithmetic
lemma driving the peer chain-packing proof.  Proposition 1 shows its exact
stopping point: for an incomparable pair, \(r_p>0\), and the integer square
\(c^2\) is replaced after normalization by the rational square \((c/C)^2\).

## 4. The denominator obstruction is genuine

It would finish the preceding argument if one could assert \(C\mid c\), but
that assertion is false in a very small exact collision:

\[
 h(315)=315\cdot624=196560=351\cdot560=h(351).
\tag{15}
\]

Take \(u=351=3^3\cdot13\) and
\(v=315=3^2\cdot5\cdot7\).  At the common base \(3\), the indices are
\(4\) and \(3\), so \(d=1\), \(r=2\), and \(C=3^2=9\).  The quantities
in (6) are

\[
 A=3\cdot13=39,\quad B=5\cdot7=35,
 \quad X=40\cdot14=560,\quad Y=13\cdot6\cdot8=624.
\]

Hence

\[
             c=X/B=Y/A=16,qquad c/C=16/9,           \tag{16}
\]

so \(C\nmid c\).  In particular, no extension of the square-gap proof may
silently treat \(c/C\) as an integer.

The same obstruction is not confined to a small example.  In the independently
verified cubefree collision
`min_euler_mass_u20000_e2_gt11.json`, the incomparable transitions are the
\(1\leftrightarrow2\) transitions, and

\[
\begin{aligned}
 C&=30479507950175015606654562325060211569,\\
 c&=42614134766498560938681337852723200000,\\
 (c,C)&=391.
\end{aligned}
\tag{17}
\]

Thus the reduced denominator of \(c/C\) still has 35 decimal digits.  Its
differing-base Euler mass is

\[
 0.4079030209054945\ldots,
 \qquad \prod_{p\in D}\frac p{p-1}
 =1.503661330384694\ldots.                            \tag{18}
\]

This is a finite counterexample to any proposed universal Euler-product gap
larger than the value in (18); it does not disprove the existence of a smaller
positive gap.

## 5. A sharper abundance-proximity constraint

The usual Euler-mass estimate loses a full power of \(p\) when a prime occurs
on both sides with positive but unequal exponents.  Let

\[
 J_e(p)=\frac{S_e(p)}{p^e}=1+p^{-1}+\cdots+p^{-e}.
\]

Since \(H_e(p)=p^{2e}J_e(p)\), a collision gives the exact identity

\[
 2\log\frac uv
 =-\sum_{p\in D}\log\frac{J_{a_p}(p)}{J_{b_p}(p)}.
\tag{19}
\]

For \(a>b\),

\[
 0<\log\frac{J_a(p)}{J_b(p)}
 <\sum_{j=b+1}^{a}p^{-j}
 <\frac{p^{-(b+1)}}{1-p^{-1}}.                       \tag{20}
\]

If \(D_0=\{p:\min(a_p,b_p)=0\}\) and
\(D_+=D\setminus D_0\), (19)--(20) imply

\[
 2\left|\log\frac uv\right|
 <\sum_{p\in D_0}\frac1{p-1}
  +\sum_{p\in D_+}\frac1{p(p-1)}.                   \tag{21}
\]

Writing \(u=g_0A_0,v=g_0B_0\) with \((A_0,B_0)=1\), unique factorization
also gives

\[
 2\log\left(1+\frac1{\min(A_0,B_0)}\right)
 <\sum_{p\in D_0}\frac1{p-1}
  +\sum_{p\in D_+}\frac1{p(p-1)}.                   \tag{22}
\]

For a same-radical collision, the entire right side is a reciprocal-square
sum.  This is substantially sharper than the union Euler mass, but it still
does not give a uniform gap: \(\min(A_0,B_0)\) can be a product of arbitrarily
many large prime powers, making the rational-spacing term on the left far
smaller than the reciprocal-square sum.

## 6. What a largest-base descent really gives

Assume all exponents are at most \(E\), and let \(P=\max D\).  Taking the
\(P\)-adic valuation of \(h(u)=h(v)\) gives

\[
 a_P-b_P+
 \sum_{q\in D}\bigl(v_P(S_{a_q}(q))-v_P(S_{b_q}(q))\bigr)=0.             \tag{23}
\]

The summand with \(q=P\) is zero because \(P\nmid S_e(P)\).  It follows
that there is a prime base \(q<P\) and one of its two exponent states
\(1\leq e\leq E\) for which

\[
                         P\mid S_e(q).                \tag{24}
\]

For \(P\geq5\), necessarily \(e\geq2\): if \(e=1\), then
\(P\mid q+1\leq P\), so \(q=P-1\), impossible for two primes except
\((q,P)=(2,3)\).

Let \(t=\operatorname{ord}_P(q)\).  Since \(2\leq q<P\), (24) implies

\[
 1<t\mid e+1,\qquad t\mid P-1.                       \tag{25}
\]

Consequently, after \(P\) and the cap \(E\) are fixed, there are at most

\[
                   \sum_{t=2}^{E+1}\varphi(t)=O(E^2) \tag{26}
\]

possible residues \(q\in[2,P-1]\) that can serve as such an upward
predecessor.  Also

\[
 P\leq S_e(q)<2q^e
 \quad\Longrightarrow\quad
 q>(P/2)^{1/E}.                                      \tag{27}
\]

Equations (24)--(27) are a valid bounded-branching, bounded-log-drop descent
statement.  They do **not** make the dependency graph acyclic.

For exponent two, Mills classified the positive integer solutions of

\[
 x\mid y^2+y+1,qquad y\mid x^2+x+1
\]

as consecutive terms in a recurrence.  An exact prime pair far out in this
recurrence is

\[
 p=22419767768701,qquad q=107419560853453,
\]

with

\[
 q\mid p^2+p+1,qquad p\mid q^2+q+1.                 \tag{28}
\]

Both primality and the divisibilities are checked by
`verify_mills_phi3_prime_cycle.py`.  The two-base Euler mass is only
\(5.39127864745\cdot10^{-14}\).  This pair is not itself an \(h\)-collision,
but it rigorously shows that a directed cyclotomic cycle cannot be charged a
fixed amount of Euler mass.

There is an exact Vieta-type descent when a prime \(Q>\max(p,q)\) divides
both \(p^2+p+1\) and \(q^2+q+1\).  The two distinct roots modulo \(Q\)
give

\[
 p+q+1=Q.
\]

Putting \(m=(pq-1)/Q\), one obtains

\[
 (p-m)(q-m)=m^2+m+1,
\]

and

\[
 p^2+p+1=Q(p-m),\qquad q^2+q+1=Q(q-m).               \tag{29}
\]

This explains Mills's quadratic descent, but it relies on a common divisor
larger than both bases.  It gives no control over longer cycles, mixed
exponents, or common divisors below the larger base.

## 7. The cubefree same-radical ratio

For cubefree inputs having the same radical, every differing exponent is
\(1\leftrightarrow2\).  Thus a collision would give a signed subset-product
relation among

\[
 T(p)=\frac{H_2(p)}{H_1(p)}
     =\frac{p(p^2+p+1)}{p+1}.                         \tag{30}
\]

The numerator and denominator in (30) are coprime.  Exact computation found
no relation core for prime bases up to \(10^7\), but that finite observation
must not be extrapolated to a theorem.  The following is what the
largest-prime argument proves unconditionally.

**Proposition 2 (forced cubic predecessor).**  Suppose that \(\mathcal A\)
and \(\mathcal B\) are disjoint finite sets of primes and

\[
                 \prod_{p\in\mathcal A}T(p)
                 =\prod_{p\in\mathcal B}T(p).        \tag{31}
\]

Let \(P=\max(\mathcal A\cup\mathcal B)\), and assume \(P\geq5\).  Then
\(P\equiv1\pmod3\).  Among the two nontrivial cube roots modulo \(P\),
exactly one is a prime base in \(\mathcal A\cup\mathcal B\); it lies on the
side opposite \(P\).  The other root is absent (or is not prime).

**Proof.**  Give a base sign \(\varepsilon_p=1\) on \(\mathcal A\) and
\(-1\) on \(\mathcal B\).  Taking the \(P\)-adic valuation of (31) gives

\[
 0=\varepsilon_P+
   \sum_{q<P}\varepsilon_qv_P(q^2+q+1)
   -\sum_{q<P}\varepsilon_qv_P(q+1).                 \tag{32}
\]

The last sum is zero: \(P\mid q+1\leq P\) would give \(q=P-1\), which is
not prime for odd \(P\geq5\).  Hence some \(q<P\) satisfies
\(P\mid q^2+q+1\).  It has order three modulo \(P\), proving
\(P\equiv1\pmod3\).  There are precisely two such residues.  Moreover,

\[
 q^2+q+1\leq(P-1)^2+(P-1)+1<P^2,
\]

so every occurrence has \(P\)-adic valuation exactly one.  Therefore (32)
is the sum of \(\varepsilon_P\) and at most two numbers in
\(\{-1,1\}\).  The only way it can vanish is for exactly one root-base to
occur, with sign \(-\varepsilon_P\).  \(\square\)

In particular, the rational numbers \(T(p)\) are signed-subset independent
on any set of primes containing no prime congruent to \(1\pmod3\).  Indeed,
the largest base in a nontrivial relation would contradict Proposition 2
unless all bases lay in \(\{2,3\}\), and the latter two values are checked
directly.  This gives a genuine same-radical cubefree special case, but a
general fiber can contain linearly many primes congruent to \(1\pmod3\).

There can be no two-base relation: polynomial division gives

\[
 T(x)=x^2+\frac{x}{x+1},
\]

which is strictly increasing for \(x>0\).  Proposition 2, however, does not
iterate to a proof of multiplicative independence.  The obstruction is
already visible in the Mills pair (28).  If \(p<q\) are adjacent Mills terms,
with previous and next terms \(r,s\), then

\[
 \Phi_3(p)=rq,\qquad \Phi_3(q)=ps,
\]

and the two columns restricted to the base-prime rows \(p,q\) are

\[
\begin{pmatrix}1&1\\1&1\end{pmatrix}.              \tag{33}
\]

Here the denominators cause no cancellation: the Mills recurrence gives
\(q+1=5p-r\), so \(p\nmid q+1\), while \(p+1<q\).  Thus the base-prime
valuation matrix is singular even for the extremely rough exact prime pair
in (28).  (Infinitely many adjacent prime pairs in the Mills recurrence are
not known.)  Cancelling those two rows merely transforms the ratio to

\[
                 \frac{T(q)}{T(p)}
                 =\frac{s(p+1)}{r(q+1)},             \tag{34}
\]

and Mills's theorem gives no control over the prime factors of
\(r,s,p+1,q+1\).  For the verified large prime pair in (28), the neighboring
terms are in fact composite.  A proof must control the entire residual
cofactor network in (34); the forced predecessor alone does not do so.

An Eisenstein-integer reformulation reaches the same barrier.  If
\(\omega^2+\omega+1=0\), then

\[
 T(p)^2=N_{\mathbb Q(\omega)/\mathbb Q}
 \left(\frac{p(p-\omega)^2}{p+1}\right).             \tag{35}
\]

A relation (31) therefore produces an element of norm one.  In an imaginary
quadratic field, norm one does not force a fractional element to be a root
of unity: split prime factors may occur as \(\pi/\bar\pi\).  The mutual
\(\Phi_3\)-divisibility in (33) is exactly the kind of conjugate-prime
exchange that survives taking norms.  Hence unique factorization in the
Eisenstein integers, without an additional global argument controlling these
exchanges, does not prove (31) trivial.

Nor does a primitive-divisor argument make a factor private across different
bases.  If a rational prime \(\ell\equiv1\pmod3\) divides one
\(\Phi_3(p)\), choose either nontrivial cube-root residue modulo \(\ell\);
Dirichlet's theorem supplies infinitely many prime bases \(q\) in that
residue class, all with \(\ell\mid\Phi_3(q)\).  For every prime \(\ell\),
Dirichlet likewise supplies infinitely many prime \(q\equiv-1\pmod\ell\),
so \(\ell\mid q+1\).  Zsigmondy primitiveness is relative to lower powers of
one fixed base, not to the other prime bases in (31).  This explains why the
empty finite relation core through \(10^7\) is useful evidence but not the
shadow of an immediate private-prime theorem.

Accordingly, multiplicative independence of all the prime-indexed rational
numbers \(T(p)\) is **not proved here** and was not found in the audited
literature.  Even if established, it would settle only the same-radical
cubefree subcase, not arbitrary radical changes or general fixed \(R\).

## 8. Consequence for the proposed fixed-\(R\) proof

The local gcd calculation does not close the fixed-exponent step.  It reduces
it to a sharper and fully explicit obstruction:

* comparable index pairs have defect \(r_p=0\), hence \(C=1\), and the
  integer-square gap proves the chain lemma;
* every incomparable index pair contributes a base-prime power to \(C\);
* the remaining multiplier is only the rational \(c/C\), and actual
  collisions show that its denominator need not cancel;
* largest-prime descent has bounded branching, but the exact extremely rough
  prime 2-cycle in (28), together with the unbounded integer Mills cycles,
  prevents any argument based solely on acyclicity or a fixed mass charge per
  cycle.

Thus a successful proof along this route still needs a **global** theorem
showing that the defect divisors/cyclotomic cycles occurring simultaneously
inside one fiber have sublinear entropy.  Neither the elementary gcd identity,
Mills's 2-cycle classification, nor the currently audited cyclotomic and
S-unit literature supplies that theorem.

The identity (2) and its cyclotomic factorization are classical.  I did not
find Proposition 1 packaged in the form (10)--(12) in the sources already
audited for this project, but no claim of originality or priority should be
made without a broader literature check.  In any event, Proposition 1 is a
reduction, not the missing sublinear-entropy theorem and not a solution of
Erdős Problem 1060.

## 9. Verification references

* W. H. Mills, *A System of Quadratic Diophantine Equations*, Pacific J.
  Math. 3 (1953), 209--220:
  <https://msp.org/pjm/1953/3-1/pjm-v3-n1-p15-p.pdf>.
* Exact cubefree certificate:
  `ksigma_verification_2026-09-05/min_euler_mass_u20000_e2_gt11.json`.
* Independent certificate checker:
  `ksigma_verification_2026-09-05/verify_min_euler_mass_gt11.py`.
* Exact checker for (10), (15)--(17), and the matrix (33):
  `ksigma_verification_2026-09-05/verify_local_gcd_descent.py`.
* Mills-pair checker:
  `ksigma_verification_2026-09-05/verify_mills_phi3_prime_cycle.py`.
