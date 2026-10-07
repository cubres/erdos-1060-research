# Transition cycles, feedback sets, and VC dimension for fibers of \(k\sigma(k)\)

**Date:** 5 September 2026  
**Status:** rigorous partial results and exact obstructions; **not** a proof of Erdős Problem 1060.

## 1. Setup and the exact feedback-set bridge

Write

\[
 h(k)=k\sigma(k),\qquad \mathcal F_N=\{k:h(k)=N\}.
\]

Fix a subfamily \(\mathcal F\subseteq\mathcal F_N\) in which every input-prime
exponent is at most \(R\).  Let \(S\) be the union of the prime supports of the
members of \(\mathcal F\), and put

\[
 A_q=\{v_q(k):k\in\mathcal F\}\subseteq\{0,1,\ldots,R\}.
\]

The **state-dependent transition digraph** \(D_{\mathcal F}\) has vertex set
\(S\), with an arc \(q\to p\) when the function

\[
 e\longmapsto v_p(\sigma(q^e))
\]

is nonconstant on \(A_q\).  There are no loops, since
\(\sigma(q^e)\equiv1\pmod q\).  Every \(k\in\mathcal F\), with
\(a_q=v_q(k)\), satisfies the simultaneous valuation equations

\[
 v_p(N)=a_p+\sum_{q\in S}v_p(\sigma(q^{a_q}))
 \qquad(p\in S).                                      \tag{1}
\]

**Feedback-set lemma.**  If \(T\) is a directed feedback vertex set of
\(D_{\mathcal F}\), then the projection

\[
 k\longmapsto (v_p(k))_{p\in T}
\]

is injective on \(\mathcal F\).  Consequently

\[
 |\mathcal F|\leq\prod_{p\in T}|A_p|\leq(R+1)^{|T|}. \tag{2}
\]

**Proof.**  Fix the coordinates on \(T\), and take a topological ordering of
\(D_{\mathcal F}-T\).  At a vertex \(p\), every term in (1) that genuinely
depends on an as-yet-unrecovered coordinate comes from an incoming arc
\(q\to p\); its tail occurs earlier in the topological order.  Terms for
missing arcs are constant on the whole fiber.  Thus (1) uniquely recovers
\(a_p\), successively for every \(p\notin T\).  This proves injectivity and
(2). \(\square\)

It would therefore suffice, for fixed \(R\), to prove

\[
 \tau(D_{\mathcal F})
   =o_R\!\left(\frac{\log N}{\log\log N}\right),       \tag{3}
\]

uniformly over all bounded-exponent fibers.  The results below do not prove
(3).

## 2. Local arithmetic of upward arcs

Call an arc \(q\to p\) **upward** if \(q<p\).

**Lemma 2.1 (bounded upward indegree).**  For any fixed head prime \(p\), the
number of smaller prime tails \(q<p\) that can occur through states
\(1\leq e\leq R\) is at most

\[
 C_R=\sum_{e=1}^{R}e=\frac{R(R+1)}2.                  \tag{4}
\]

**Proof.**  For fixed \(e\), the condition
\(p\mid\sigma(q^e)=1+q+\cdots+q^e\) says that \(q\pmod p\) is a root of a
nonzero polynomial of degree \(e\) over \(\mathbf F_p\).  It therefore has at
most \(e\) residue classes.  Since \(q<p\), each residue class contains at
most one possible prime \(q\).  Sum over \(e\). \(\square\)

This is useful sparsity, but bounded indegree or degeneracy alone does not
force a sublinear feedback set: a disjoint union of directed 2-cycles already
has bounded degree and a linear feedback number.

The following stronger observation charges each upward arc to the target.

**Lemma 2.2 (upward-edge charge).**  If \(q\to p\) is an upward arc, then
either \((q,p)=(2,3)\), or

\[
 q^2p\mid N.                                         \tag{5}
\]

**Proof.**  Nonconstancy means that for some occurring state
\(e\in A_q\), one has \(p\mid\sigma(q^e)\).  Necessarily \(e\geq1\).  If
\(e=1\), then \(p\mid q+1\); because \(p>q\), this forces \(p=q+1\), hence
the consecutive primes are \((q,p)=(2,3)\).  Otherwise an occurring state
\(e\geq2\) has \(p\mid\sigma(q^e)\).  For the corresponding preimage, its
local factor

\[
 H(q,e)=q^e\sigma(q^e)
\]

divides \(N=h(k)\), and hence \(q^2p\mid N\). \(\square\)

Notice that the proof permits other occurring states at \(q\): it chooses a
state at which the relevant valuation is positive.  If that state were 1,
the upward edge would necessarily be the exceptional \(2\to3\).

## 3. A quantitative theorem for vertex-disjoint directed cycles

Let \(\nu(D)\) denote the maximum number of pairwise vertex-disjoint directed
cycles.  Let \(\ell_j\) be the \(j\)-th prime.

**Theorem 3.1 (the \(1/3\) packing bound).**  If
\(t=\nu(D_{\mathcal F})\geq2\), then

\[
 N\ \geq\
 \left(\prod_{j=1}^{t-1}\ell_j^2\right)
 \left(\prod_{j=t}^{2t-2}\ell_j\right).             \tag{6}
\]

In particular, uniformly in every bounded-exponent fiber,

\[
 \nu(D_{\mathcal F})
 \leq\left(\frac13+o(1)\right)
       \frac{\log N}{\log\log N}.                   \tag{7}
\]

**Proof.**  Every directed cycle contains an upward arc, because a finite
cycle cannot be strictly decreasing at every edge.  Select one upward arc
\(q_i\to p_i\) in each of \(t\) vertex-disjoint cycles.  At most one selected
arc can be \(2\to3\).  Discard that cycle if it occurs, and put \(m=t-1\).
For the remaining arcs, Lemma 2.2 gives

\[
 \prod_{i=1}^{m}q_i^2p_i\mid N.                     \tag{8}
\]

All \(2m\) endpoint primes in (8) are distinct, because the cycles are
vertex-disjoint.  Among products on \(2m\) distinct primes with \(m\) of
them receiving one extra copy, the minimum is obtained by squaring the
smallest \(m\) primes and taking the next \(m\) primes once.  This proves
(6).  (We have relaxed the additional pairing constraints \(q_i<p_i\), so
the result remains a valid lower bound.)

Writing \(\vartheta(x)=\sum_{p\leq x}\log p\), the logarithm of the
right-hand side of (6) is

\[
 2\vartheta(\ell_m)+\vartheta(\ell_{2m})-
 \vartheta(\ell_m)
 =\vartheta(\ell_m)+\vartheta(\ell_{2m})
 =(3+o(1))m\log m.                                  \tag{9}
\]

The prime number theorem and inversion of (9) give (7); bounded \(t\) is
harmless. \(\square\)

This theorem is genuinely arithmetic, but it has a fixed positive constant.
It gives neither \(\nu=o(\log N/\log\log N)\) nor the stronger feedback
bound (3).  Directed Erdős--Pósa supplies a feedback set whose size is some
function of \(\nu\), but no estimate from that theorem converts (7) into the
required little-\(o\), and general digraphs show that a linear relation
between packing and feedback can be sharp.

The constant \(1/3\) is the natural limit of this particular one-upward-edge
charge: a 2-cycle may contribute only the two distinct base primes plus one
guaranteed extra copy of the smaller/upward-tail prime.  Any improvement to
zero must exploit global compatibility of many cycles, not merely charge one
local factor per cycle.

## 4. Exact finite diagnostics

All graph statements in this section use the state-dependent graph defined
in Section 1, not a graph built from every arithmetically possible state.

### 4.1 The rough cubefree atom

The certificate
`ksigma_verification_2026-09-05/cubefree_rough210_collision.json` gives the
exact cubefree collision

\[
\begin{aligned}
 K&=60629697601617236747379985403,\\
 M&=61655391632564660609643619057,\\
 h(K)=h(M)&=
 5276516179938729922490847708056660616574496169354744299520.
\end{aligned}                                       \tag{10}
\]

Both inputs are coprime to \(210\).  The independent standard-library
verifier `verify_cubefree_rough210.py` rebuilds both divisor sums exactly and
also checks the claimed primitive subset-product property.  It returned
`PASS` on 5 September 2026.

The exact transition graph has 17 vertices and 18 arcs.  Its cyclic strongly
connected components are

\[
 \{13,61\},\qquad
 \{11,17,19,43,127,271,307,5419\}.
\]

It has

\[
 \tau=\nu=2.
\]

One minimum feedback set is \(\{11,13\}\).  A maximum disjoint packing is

\[
 (13,61),\qquad
 (11,19,127,5419,271,17,307,43).                    \tag{11}
\]

The full machine-readable graph audit is
`ksigma_verification_2026-09-05/cubefree_rough210_transition_audit.json`.

### 4.2 A four-corner tensor with feedback number three

Tensoring (10) with the disjoint-support identity \(h(12)=h(14)=336\)
gives the four exact cubefree preimages

\[
\begin{split}
727556371219406840968559824836,&\quad
848815766422641314463319795642,\\
739864699590775927315723428684,&\quad
863175482855905248535010666798,
\end{split}
\]

of the common target

\[
1772909436459413253956924829907037967169030712903194084638720.
                                                               \tag{12}
\]

The transition graph has 20 vertices and 52 arcs, with cyclic strongly
connected components

\[
 \{2,3,7\},\quad \{13,61\},\quad
 \{11,17,19,43,127,271,307,5419\}.
\]

Its exact invariants are

\[
 \tau=\nu=3.
\]

A minimum feedback set is \(\{2,11,13\}\), while a disjoint cycle packing is

\[
 (2,7),\quad(13,61),\quad
 (11,19,127,5419,271,17,307,43).                    \tag{13}
\]

This calculation is recorded in
`ksigma_verification_2026-09-05/cubefree_fvs3_tensor_audit.json`.  It is an
exact finite certificate, not asymptotic evidence.  The independent
standard-library script `verify_cubefree_fvs3_tensor.py` reconstructs all
four products, the 52 transition arcs, the three disjoint cycles, acyclicity
after deleting \(\{2,11,13\}\), and the two-coordinate shattered square; it
returned `PASS` on 5 September 2026.

This example also shows that feedback number can overcount the genuine
information in the fiber.  The two exponent coordinates \(\{2,11\}\)
already distinguish all four preimages, so the minimum coordinate separator
has size 2, whereas every directed feedback set has size at least 3.

### 4.3 A cubefree atom avoiding \(2,3,31\), and a failed chain-to-FVS claim

The certificate `avoid_2_3_31_u20000.json` gives

\[
\begin{aligned}
 K={}&297988218233648364240999791517121425214912505,\\
 M={}&338368113000148356341974220844029561466672613,
\end{aligned}
\]

with

\[
 h(K)=h(M)=
147424966926910851646005882187078719136356520640407126230120281498533058410853434392576000.
                                                               \tag{14}
\]

Both inputs are cubefree, use 24 variable base primes, and avoid the bases
\(2,3,31\).  The standard-library verifier `verify_avoid_2_3_31.py` checks
primality of every base, reconstructs both inputs and both products of local
blocks, checks the stored factorization of (14), and rebuilds the transition
graph.  It returned `PASS` on 5 September 2026.

That graph has 24 vertices and 34 arcs.  Its sole nontrivial strongly
connected component is

\[
 \{13,61,97,197,317,379,787,2053,3169,14401\}.
\]

Its directed cycles are

\[
\begin{split}
 &(13,61),\\
 &(97,3169,317,14401,379,61),\\
 &(97,3169,317,14401,379,787,197,2053,13,61).
\end{split}                                         \tag{15}
\]

The unique one-vertex feedback set is \(\{61\}\).  The verifier certifies
acyclicity after deleting 61 by the explicit topological order

\[
\begin{split}
97,3169,317,53,14401,379,787,197,19,2053,127,13,79,
5419,5,271,17,307,43,733,11,367,23.
\end{split}
\]

Now call a coordinate \(q\) **non-chain** for this pair if the two exponent
indices \(v_q(K)+1\) and \(v_q(M)+1\) are incomparable under divisibility.
The exact non-chain set is

\[
 Z=\{17,19,97,127,197,307,317,379\}.                 \tag{16}
\]

Nevertheless, \(D_{\{K,M\}}-Z\) still contains the cycle
\(13\leftrightarrow61\).  At both 13 and 61 the two exponent indices are
comparable.  Thus the plausible assertion

> the set of coordinates with divisibility-incomparable exponent indices is
> a feedback vertex set

is false, even for an exact cubefree collision avoiding the customary small
bases.  The peer chain-packing lemma remains valid as a **global pairwise
incompatibility** statement when its Euler-product hypothesis holds; it
cannot be localized into a claim that every transition cycle contains a
non-chain coordinate.

### 4.4 Finite census

An exhaustive census of all complete exponent-\(<7\) fibers of size at least
3 with \(k<10^7\) (hence complete for the recorded target range) contains
6,498 fibers.  Their exact feedback-size histogram is

\[
 \tau=1:6198,\qquad \tau=2:300,
\]

and the vertex-disjoint packing histogram is identical.  For exponent
\(<5\), the corresponding 4,881 fibers split as 4,637 with \(\tau=1\) and
244 with \(\tau=2\).  These data are recorded in
`bounded_transition_fvs_K1e7_R7.json` and
`bounded_transition_fvs_K1e7_R5.json`.  They are useful diagnostics but do
not establish a uniform theorem.

## 5. VC dimension of powerful-part threshold families

For \(2\leq j\leq R\), define the threshold support

\[
 S_j(k)=\{p\in S:v_p(k)\geq j\},
 \qquad
 \mathcal A_j=\{S_j(k):k\in\mathcal F\}.             \tag{17}
\]

The tuple \((S_2(k),\ldots,S_R(k))\) is precisely another encoding of the
powerful part

\[
 \prod_{v_p(k)\geq2}p^{v_p(k)}.
\]

Gyulev's squarefree-remainder lemma shows that the powerful-part map is
injective on a fiber of \(h\).  Therefore

\[
 |\mathcal F|\leq\prod_{j=2}^{R}|\mathcal A_j|.       \tag{18}
\]

Let \(d_j=\operatorname{VCdim}(\mathcal A_j)\) and \(s=|S|\).  Sauer--Shelah
gives the rigorous conditional estimate

\[
 |\mathcal F|
 \leq
 \prod_{j=2}^{R}\sum_{i=0}^{d_j}\binom{s}{i}.        \tag{19}
\]

Consequently, for every fixed \(R\), a uniform bound

\[
 \max_{2\leq j\leq R}d_j=o_R(s)                     \tag{20}
\]

would imply \(\log|\mathcal F|=o_R(s)\).  Since
\(S\subseteq\{p:p\mid N\}\) and

\[
 \omega(N)\leq(1+o(1))\frac{\log N}{\log\log N},
\]

(20), combined with the standard high-exponent reduction, would yield the
desired Erdős bound.  Thus (20) is a precise alternative missing theorem.

However, VC dimension is not always 1.  In the four-corner tensor (12), the
threshold-2 traces on the coordinates \(\{2,11\}\) realize all four patterns

\[
 \varnothing,\quad\{2\},\quad\{11\},\quad\{2,11\}.
\]

Hence \(\operatorname{VCdim}(\mathcal A_2)\geq2\) in an exact cubefree
fiber.  This is also the coordinate reason the four preimages can be encoded
with two coordinates even though the transition FVS has size three.

There is a general tensor obstruction.

**Lemma 5.1 (tensor shattering).**  Suppose, for \(1\leq i\leq t\), that

\[
 h(a_i)=h(b_i),
\]

that all \(2t\) input supports are pairwise disjoint across distinct \(i\),
and that a distinguished prime \(p_i\) lies in the \(i\)-th support with

\[
 v_{p_i}(a_i)<j\leq v_{p_i}(b_i)
\]

(after interchanging \(a_i,b_i\) if necessary).  Then one fiber has a
threshold-\(j\) family of VC dimension at least \(t\).

**Proof.**  For every \(\varepsilon\in\{0,1\}^t\), choose
\(c_{i,0}=a_i\), \(c_{i,1}=b_i\), and put

\[
 K_\varepsilon=\prod_{i=1}^t c_{i,\varepsilon_i}.
\]

Pairwise coprimality and multiplicativity give

\[
 h(K_\varepsilon)=\prod_{i=1}^t h(a_i),
\]

independent of \(\varepsilon\).  On the distinguished coordinates,
\(S_j(K_\varepsilon)\cap\{p_1,\ldots,p_t\}) is exactly the subset encoded
by \(\varepsilon\).  Hence those \(t\) coordinates are shattered.
\(\square\)

Thus any proof of (20) must control how many pairwise support-disjoint
threshold-toggling collision atoms can coexist.  Sauer--Shelah does not make
that arithmetic control automatic.  The known large Mersenne-type fibers
are one-hot and have VC dimension 1, but tensor products already show that
this behavior is not universal.

## 6. Relation to the peer divisibility-chain argument

The attached six-page note proves, under a uniformly satisfied large-prime
Euler-product condition, that two equal-value inputs cannot have
divisibility-comparable exponent indices at **every** prime.  Random packing
of divisibility chains then gives the legitimate partial estimate

\[
 \log f(N)
 \leq
 \left(\frac12\log\!\left(1+\frac1{\sqrt2}\right)+o(1)\right)
 \frac{\log N}{\log\log N};                          \tag{21}
\]

for cubefree inputs it records the improved constant
\(\tfrac12\log\varphi\).  I checked the six displayed proof sections.  The
argument is consistent as a positive-constant result, and the note itself
correctly states that it does not prove the required zero constant.

The transition and VC calculations above explain exactly where it stops:

1. global pairwise incomparability does not say that non-chain coordinates
   meet every dependency cycle, by (14)--(16);
2. abstract antichains can still have exponential size;
3. exact arithmetic tensor squares can realize VC dimension 2 and make
   feedback number strictly larger than the true separator number;
4. the one-upward-edge arithmetic charge proves only the fixed constant
   \(1/3\) in (7).

## 7. Verdict

The FVS route supplies the exact injection (2).  The new arithmetic content
proved here is the target-divisibility charge (5) and the resulting
vertex-disjoint cycle bound (7).  The exact certificates then rule out two
natural shortcuts from the peer argument to (3).

No step in this note yields

\[
 o\!\left(\frac{\log N}{\log\log N}\right).
\]

A completion through this circle of ideas still requires at least one new
global theorem of one of the following types:

* a little-\(o\) bound for the minimum information separator, not merely for
  a possibly larger graph feedback set;
* a uniform \(o(s)\) VC-dimension bound for all threshold families, together
  with an arithmetic prohibition on large tensor packings; or
* a global incompatibility theorem showing that a positive proportion of
  the locally charged cycles cannot be simultaneously balanced in one
  valuation fiber.

The finite evidence strongly favors hub-like transition cores in the tested
range, but the exact tensor examples show that independent cyclic cores do
occur.  Treating the missing global theorem as already available would be a
gap, not a ready-to-post proof of Erdős Problem 1060.
