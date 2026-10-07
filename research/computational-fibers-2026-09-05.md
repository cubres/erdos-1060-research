# Exact finite audit of bounded-exponent fibers of \(k\sigma(k)\)

**Date:** 5 September 2026  
**Purpose:** test the proposed cubefree reciprocal-mass and feedback-vertex-set
routes to Erdős Problem 1060.  Every positive certificate below is rebuilt with
arbitrary-precision integers.  Every census assertion is finite.  Nothing in
this note is presented as an asymptotic proof.

## 1. Definitions used in the audit

Put

\[
H(p,e)=p^e\sigma(p^e),\qquad h(k)=k\sigma(k)=\prod_{p^e\parallel k}H(p,e).
\]

For a fiber \(\mathcal F\), let \(S\) be the union of its input-prime supports.
Its **state-dependent interaction digraph** \(D_{\mathcal F}\) has vertex set
\(S\), and has the arc \(q\to p\) exactly when

\[
a\longmapsto v_p(\sigma(q^a))
\]

is nonconstant on the exponent states \(a=v_q(k)\) actually occurring among
\(k\in\mathcal F\).  This is the graph in the feedback-set reconstruction
lemma; it is not the larger graph of all local blocks that merely divide the
target.  The directed feedback vertex number is denoted \(\tau(D_{\mathcal
F})\).

For a pair \(u,v\), identical local states are cancelled and

\[
\Delta(u,v)=\{p:v_p(u)\ne v_p(v)\},\qquad
\lambda(\Delta)=\sum_{p\in\Delta}-\log(1-1/p).
\]

The `R` convention in the census is \(v_p(k)<R\).  Thus `R=3` means
cubefree inputs, `R=5` permits exponents at most four, and `R=7` permits
exponents at most six.

## 2. Complete cubefree census through \(N=10^{16}\)

The program
[`cubefree_fiber_transition_census.cpp`](ksigma_verification_2026-09-05/cubefree_fiber_transition_census.cpp)
enumerates every cubefree \(k<K\), computes \(\sigma(k)\) by an exact linear
sieve, sorts by \(h(k)\), normalizes every collision, constructs
\(D_{\mathcal F}\), and solves directed FVS exactly by branching on a directed
cycle.  The retained target range is complete: if \(k>1\), then

\[
h(k)=k\sigma(k)>k^2;
\]

hence \(h(k)\le K^2\) implies \(k<K\).

For \(K=10^8\), so for every \(N\le10^{16}\), the exact result is:

- retained cubefree preimages: **69,650,098**;
- fiber histogram: **66,661,186** targets with one preimage and **1,494,456**
  targets with two preimages;
- collision fibers/pairs: **1,494,456**; maximum fiber size: **2**;
- distinct normalized collision signatures: **one**;
- that signature is
  `2:1:2;3:0:1;7:1:0`, up to reversing the two sides;
- every collision therefore has the form
  \[
  14d\longleftrightarrow12d,\qquad (d,42)=1,
  \]
  with the same prime exponents in \(d\) on the two sides;
- every interaction graph has the four arcs
  \[
  2\to3,\quad2\to7,\quad3\to2,\quad7\to2,
  \]
  directed FVS number one, and directed girth two;
- there are **no** same-radical pairs, coprime-input pairs, collisions avoiding
  the base prime \(2\), or normalized supports different from \(\{2,3,7\}\).

For all these pairs,

\[
\lambda(\Delta)=\log\left(\frac21\frac32\frac76\right)
=\log(7/2)=1.2527629684953678\ldots.
\]

The main output is
[`cubefree_fiber_transition_K1e8.txt`](ksigma_verification_2026-09-05/cubefree_fiber_transition_K1e8.txt).
An independently written census,
[`bounded_fiber_census.cpp`](ksigma_verification_2026-09-05/bounded_fiber_census.cpp),
reproduced the retained count, complete fiber histogram, collision count, and
maximum multiplicity in
[`bounded_fiber_K1e8_R3.txt`](ksigma_verification_2026-09-05/bounded_fiber_K1e8_R3.txt).
The first implementation was also compiled with AddressSanitizer and
UndefinedBehaviorSanitizer and compared byte-for-byte with the optimized build
at \(K=10^5\).

This is strong finite rigidity, but not a proof that all cubefree collisions
are lifts of \(12\leftrightarrow14\): exact large counterexamples below show
that such a global assertion is false.

## 3. Rough cubefree collisions and reciprocal mass

The script
[`bounded_collision_transition_audit.py`](ksigma_verification_2026-09-05/bounded_collision_transition_audit.py)
reconstructs each displayed input and \(h\)-value with Python integers,
rebuilds every state-local arc from exact valuations, enumerates every simple
directed cycle, and computes both a minimum FVS and a maximum packing of
vertex-disjoint cycles.

Three exact collision certificates are especially relevant.

| certificate | least differing base | \(|\Delta|\) | \(\lambda(\Delta)\) | directed girth | \(\tau(D)\) |
|---|---:|---:|---:|---:|---:|
| [`cubefree_rough210_collision.json`](ksigma_verification_2026-09-05/cubefree_rough210_collision.json) | 11 | 17 | 0.4519989263271031 | 2 | 2 |
| [`min_euler_mass_u20000_e2_gt11.json`](ksigma_verification_2026-09-05/min_euler_mass_u20000_e2_gt11.json) | 17 | 38 | 0.40790302090549446 | 9 | 1 |
| [`rough_gt17_u50000_e2_disjoint_trial.json`](ksigma_verification_2026-09-05/rough_gt17_u50000_e2_disjoint_trial.json) | 19 | 75 | 0.4273540761303973 | 5 | 1 |

The second row is only the best incumbent from its stated time-limited
optimization, not a proved minimum.  The third row is an exact relation found
by a seeded finite optimization; its exact equality is unconditional, while
no global minimality is claimed.  In particular, the third row rigorously
rules out any theorem saying that every normalized cubefree collision must use
one of the primes at most \(17\).  It does **not** show that roughness is
unbounded.

The recomputed graph records are
[`cubefree_rough210_transition_audit.json`](ksigma_verification_2026-09-05/cubefree_rough210_transition_audit.json),
[`cubefree_rough17_transition_audit.json`](ksigma_verification_2026-09-05/cubefree_rough17_transition_audit.json),
and
[`cubefree_rough19_transition_audit.json`](ksigma_verification_2026-09-05/cubefree_rough19_transition_audit.json).

No sequence with least differing prime tending to infinity, and no sequence
with \(\lambda(\Delta)\to0\), was found.  Consequently these calculations
neither prove nor disprove the proposed uniform positive reciprocal-mass gap.
They do show that any eventual constant cannot exceed
\(0.40790302090549446\ldots\) on the evidence currently in hand.

## 4. Exact counterexamples to small-hub feedback claims

The rough-210 relation has two disjoint cyclic strongly connected components:

\[
\{13,61\},\qquad
\{11,17,19,43,127,271,307,5419\}.
\]

It contains the vertex-disjoint cycles

\[
(13,61),\qquad
(11,19,127,5419,271,17,307,43).
\]

Thus every directed FVS has size at least two.  Deleting \(\{11,13\}\)
makes the graph acyclic, so

\[
\tau(D)=2
\]

exactly.  This is a single normalized cubefree relation, not merely the
product of two separately displayed relations.

Its input-base support is disjoint from \(\{2,3,7\}\).  Tensoring it with
\(h(12)=h(14)=336\) gives the four exact cubefree preimages

\[
\begin{aligned}
&727556371219406840968559824836,\\
&848815766422641314463319795642,\\
&739864699590775927315723428684,\\
&863175482855905248535010666798,
\end{aligned}
\]

all mapping to

\[
1772909436459413253956924829907037967169030712903194084638720.
\]

The interaction graph of this four-point subfiber contains three
vertex-disjoint cycles, one in each of the cyclic components

\[
\{2,3,7\},\quad\{13,61\},\quad
\{11,17,19,43,127,271,307,5419\}.
\]

Deleting \(\{2,11,13\}\) makes it acyclic.  Therefore its exact FVS number is
three.  The full fiber at this target, whether or not it has additional
preimages, has FVS at least three because its interaction graph contains this
subgraph.  The exact certificate is
[`cubefree_fvs3_tensor_audit.json`](ksigma_verification_2026-09-05/cubefree_fvs3_tensor_audit.json).

These examples disprove universal “one hub coordinate,” FVS-one, and FVS-at-
most-two shortcuts.  They do not disprove the needed asymptotic estimate
\(\tau(D)=o_R(\log N/\log\log N)\), since they provide no growing family of
support-disjoint atoms.

## 5. Same-radical tests

For cubefree inputs with the same radical, every changed exponent is a switch
between one and two.  Hence a collision would give a nontrivial relation among

\[
T(p)=\frac{H(p,2)}{H(p,1)}
=\frac{p(p^2+p+1)}{p+1}.
\]

[`same_base_ratio_core_sieve.cpp`](ksigma_verification_2026-09-05/same_base_ratio_core_sieve.cpp)
constructs the exact prime-valuation support of all \(T(p)\) for prime
\(p\le10^8\).  It repeatedly removes a column having a valuation row occurring
in no other active column.  Such a row is an exact pivot, so removal preserves
linear independence.  Factoring \(p^2+p+1\) is exact: its non-3 prime divisors
are \(1\pmod3\), they are sieved through \(10^8\), and the residual is either
one or a single prime larger than \(10^8\), since two such factors would exceed
\(p^2+p+1\).

All **5,761,455** columns peel and the core is empty.  Therefore the valuation
columns are linearly independent over \(\mathbb Q\), proving the following
finite statement:

> There is no nontrivial same-radical cubefree collision all of whose input
> base primes are at most \(10^8\), regardless of the sizes of the two inputs.

The output is
[`same_base_ratio_core_p100000000_e2.json`](ksigma_verification_2026-09-05/same_base_ratio_core_p100000000_e2.json).
This does not prove global same-radical injectivity.  For larger exponent caps,
floating-point MILP searches found no same-radical relation for bases at most
\(10^4\) and exponents at most three, or bases at most \(2000\) and exponents
at most four; those infeasibility reports are heuristic solver evidence, not
formal certificates.

## 6. Larger fixed caps in the same complete target range

The complete \(N\le10^{16}\) bounded-exponent censuses give:

| `R` | allowed exponents | retained preimages | collision fibers | collision pairs | maximum fiber |
|---:|---:|---:|---:|---:|---:|
| 5 | \(0,1,2,3,4\) | 78,702,167 | 2,125,920 | 2,223,688 | 4 |
| 7 | \(0,1,\ldots,6\) | 80,497,691 | 2,362,689 | 2,493,937 | 5 |

The detailed transition computation was run on every complete fiber of size
at least three (48,881 fibers for `R=5`, 65,022 for `R=7`).  Its exact FVS
histograms are:

| `R` | FVS 1 | FVS 2 | FVS \(\ge3\) | maximum |
|---:|---:|---:|---:|---:|
| 5 | 46,434 | 2,447 | 0 | 2 |
| 7 | 62,006 | 3,016 | 0 | 2 |

For every graph in these two finite samples, the computed FVS size equals the
maximum number of vertex-disjoint directed cycles.  The first FVS-two example
is the three-point fiber

\[
h(5040)=h(5580)=h(5616)=97493760,
\]

whose graph contains the disjoint 2-cycles \((2,31)\) and \((3,5)\), and is
made acyclic by deleting \(\{2,3\}\).

The full summary records are
[`bounded_transition_fvs_K1e8_R5.json`](ksigma_verification_2026-09-05/bounded_transition_fvs_K1e8_R5.json)
and
[`bounded_transition_fvs_K1e8_R7.json`](ksigma_verification_2026-09-05/bounded_transition_fvs_K1e8_R7.json).
They were produced by
[`bounded_transition_fvs_postprocess.py`](ksigma_verification_2026-09-05/bounded_transition_fvs_postprocess.py)
from the exact per-fiber census records.  Size-two fibers were not expanded in
this particular post-processing pass; the cubefree pass in Section 2 did
include every collision fiber.

## 7. What the computation changes, and what remains open

The exact data support four conclusions.

1. Cubefree fibers are extraordinarily rigid at ordinary sizes: through
   \(10^{16}\), every collision is just a coprime common-factor lift of
   \(12\leftrightarrow14\).
2. This rigidity does not persist globally in that literal form: separate
   verified cubefree atoms show, respectively, avoidance of every base prime
   through \(17\), directed girth ten, and FVS greater than one.
3. Same-radical cubefree injectivity has very strong exact finite support—up
   to base primes \(10^8\)—but remains an unproved infinite statement and, by
   itself, would not give the required zero exponential constant.
4. The feedback-set route remains viable only in its true asymptotic form.
   Small universal hub bounds are false.  No construction found here makes
   FVS linear in \(\log N/\log\log N\), and no proof found here makes it
   little-o.

In particular, the computations do **not** complete Erdős Problem 1060 and do
not establish the reciprocal-mass gap.  They sharply identify the two
remaining arithmetic questions: whether normalized fixed-cap collisions can
have \(\lambda(\Delta)\to0\), and whether one can pack a linear number of
state-dependent directed cycles into one bounded-exponent fiber.

## 8. Reproduction commands and hashes

Representative commands:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  ksigma_verification_2026-09-05/cubefree_fiber_transition_census.cpp \
  -o ksigma_verification_2026-09-05/cubefree_fiber_transition_census

./ksigma_verification_2026-09-05/cubefree_fiber_transition_census 100000000 \
  > ksigma_verification_2026-09-05/cubefree_fiber_transition_K1e8.txt

./ksigma_verification_2026-09-05/bounded_fiber_census 100000000 3 \
  > ksigma_verification_2026-09-05/bounded_fiber_K1e8_R3.txt

./ksigma_verification_2026-09-05/same_base_ratio_core_sieve 100000000 \
  > ksigma_verification_2026-09-05/same_base_ratio_core_p100000000_e2.json

python3 ksigma_verification_2026-09-05/bounded_collision_transition_audit.py \
  ksigma_verification_2026-09-05/cubefree_rough210_collision.json \
  --output ksigma_verification_2026-09-05/cubefree_rough210_transition_audit.json

python3 ksigma_verification_2026-09-05/bounded_collision_transition_audit.py \
  ksigma_verification_2026-09-05/cubefree_rough210_collision.json \
  --add-basic-atom \
  --output ksigma_verification_2026-09-05/cubefree_fvs3_tensor_audit.json
```

SHA-256 checksums of the principal new records:

```text
c9c3e0f784d9deb085a51bc746c2b60dffda76f80a54616d5e9d3258949337b7  cubefree_fiber_transition_census.cpp
e901985978ae599d54aee60f80aa2ccd32e4003732a058948c99db850f74c0d0  cubefree_fiber_transition_K1e8.txt
3824be6181bfa915aeb9842baa17a2784cc097297c5fe55ba176f56221f9876f  bounded_fiber_K1e8_R3.txt
92f299ce5a9915ba552f700cc1be16d0c8ccff5f1bd070af08731de70e0bd820  same_base_ratio_core_p100000000_e2.json
9c088041c5a5affe92dcc108c5a39826ca3ee5fd11d5186f8bc1de5b05653b89  cubefree_rough210_transition_audit.json
b9981c1f8037fd05b50de2e05149322a747da89dce0bdbae5c6e1e412de53f68  cubefree_fvs3_tensor_audit.json
```
