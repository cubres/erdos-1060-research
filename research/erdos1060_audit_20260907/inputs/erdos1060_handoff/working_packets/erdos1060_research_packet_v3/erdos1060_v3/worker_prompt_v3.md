# Research takeover: Erdős 1060 after the prime-index/entropy improvement

Work on the mathematics, not another plan for working on the mathematics. The objective is to resolve the uniform assertion
\[
 h(k)=k\sigma(k),\quad f(N)=\#\{k:h(k)=N\},\qquad
 \log\max(1,f(N))=o(\log N/\log\log N).
\tag{EP}
\]
The optional stronger claim is \(f(N)\le(\log N)^{O(1)}\). A positive-constant bound, an almost-all estimate, or an average result is not (EP). Investigate a counterexample mechanism as seriously as a proof mechanism. Do not promise success in advance or turn a missing lemma into a theorem by naming it.

The attached `proved_results_v3.md` contains complete arguments for the new results below; the older notes and computations are retained in `prior_v2/`. Audit the proofs before using them. Originality relative to all literature is not established. The packet's `check_certificates.py` is a standard-library-only exact checker, not a formal proof-assistant development.

## A. New proved starting point

For every prime \(\ell\), write \(t_{\ell'}=t/\ell^{v_\ell(t)}\). Within a fiber of \(h\), the data
\[
 v_\ell(k),\qquad ((v_p(k)+1)_{\ell'})_{p\ne\ell}
\]
determine \(k\) uniquely.

The key proof mechanism is worth understanding. If two local exponents have the same label, then \(a+1=\ell^j(b+1)\). The local ratio is
\[
 h(p^a)/h(p^b)=p^{a-b}Q_p,
 \quad Q_p=(p^{a+1}-1)/(p^{b+1}-1)\in\mathbb Z.
\]
Every prime divisor of \(Q_p\) is either \(\ell\) or \(1\pmod\ell\), by a multiplicative-order argument. After cancellation, any differing input prime must therefore be \(1\pmod\ell\). Removing the \(\ell\)-part gives \((Q_p)_{\ell'}<p^{a-b}\). The two products of excess input prime powers are coprime, so cross-divisibility yields a strict contradiction. The exponent at \(\ell\) must be fixed; do not omit that condition.

Combining the \(\ell=2,3\) encodings on the SAME random preimage gives the fully proved improvement
\[
\boxed{\log\max(1,f(N))\le(C_0+o(1))\frac{\log N}{\log\log N},
\quad C_0=\tfrac12\log3-\tfrac13\log2\approx0.3182570841474.}
\]
It uses the local entropy inequality, valid for every distribution on \(J\in\{0,\ldots,a\}\),
\[
 \tfrac23 H((J+1)_{2'})+\tfrac13 H((J+1)_{3'})
 \le\tfrac a2\log(3/2)+\tfrac{\log2}{3}\mathbb EJ,
\]
together with \(k\le\sqrt N\). The note proves the inequality analytically, including exact rational checks for the few small cases. No numerical optimizer is needed for the theorem.

**Do not repeatedly optimize this same marginal-entropy relaxation.** With cap \(a=2\) and \(J\) uniform on \(0,1,2\), both label entropies are \(2C_0\), and \(\mathbb EJ=a/2\). For prime indices \(\ell\ge5\), the label entropy is larger. Thus these coordinatewise bounds and the two size budgets alone cannot beat \(C_0\). This is a barrier for that relaxation, not a lower bound for actual fibers. The missing information is arithmetic dependence between primes.

## B. The precise unresolved target

For each fixed \(E\ge1\) and \(\delta>0\), define
\[
 R_{E,\delta}(X)=\max_{M\le X}
 \#\{u:h(u)=M,\ v_p(u)\le E,\ P^-(u)>\delta\log X\},
\]
with \(P^-(1)=\infty\). It suffices to prove
\[
 \boxed{\log R_{E,\delta}(X)=o_{E,\delta}(\log X/\log\log X)}.
\tag{R}
\]
The established reduction is
\[
 f(N)\le G_E(N)(E+1)^{\pi(\delta\log N)}R_{E,\delta}(N),
\quad G_E(N)=\prod_{p\mid N}(1+\max(v_p(N)-E,0)).
\]
Here
\[
 \log G_E(N)\le(c_E+o_E(1))\frac{\log N}{\log\log N},
 \quad c_E=\sup_{a\ge E+1}\frac{\log(a-E+1)}a\to0.
\]
First choose \(E\), then \(\delta\), then the large-target threshold. The cutoff uses the original \(X\), not a changing residual target. (R) is not already proved. A result for one fixed \(E\) does not settle every fixed \(E\).

## C. Priority route: exact valuation constraints and inexpensive certificates

For a fixed target \(M\), let
\[
 \mathcal E_p=\{0\le e\le\min(E,v_p(M)):h(p^e)\mid M\}.
\]
Force disallowed small input primes to exponent zero. The complete equations are
\[
 v_q(M)=e_q+\sum_{p\ne q}v_q(\sigma(p^{e_p}))
 \qquad\text{for every prime }q\mid M.
\]
Do not remove an equation because its prime is too small to be an allowed input. Do not replace exact target exhaustion by divisibility.

For every \(a>b\) in \(\mathcal E_p\), form the exact valuation-difference column
\[
 c_{p,a,b}=\nu(h(p^a))-\nu(h(p^b)).
\]
A collision selects at most one column at each input prime, with coefficient \(+1\) or \(-1\), and sums to zero.

A proved elimination rule is available: if a row is nonzero only in columns belonging to one input prime, no collision can use a column nonzero in that row. Delete those columns and repeat. If all columns disappear, or the residual columns are linearly independent over \(\mathbb Q\), there is no collision.

More generally, first discard the columns at an input-prime set \(S\), then apply this rule and exact rank tests. If no nonzero collision remains, fixing the exponents at \(S\) uniquely determines a preimage. Therefore the count is at most \(\prod_{p\in S}|\mathcal E_p|\).

A sufficient missing estimate is a certificate with
\[
 \sum_{p\in S}\log|\mathcal E_p|
 =o_{E,\delta}(\log X/\log\log X).
\]
Try to prove it, but first stress-test it on represented difficult targets. The model contains incompatible potential choices, so this certificate condition may be stronger than necessary. If it fails, develop an adaptive decision tree or a different encoding: supply an actual decoder and a proved total logarithmic branching cost. Count the cost of identifying exceptional primes as well as assigning their exponents.

The earlier directed-graph reconstruction lemma remains valid: deleting a feedback vertex set and fixing its exponents allows topological reconstruction. Compare it against difference-column peeling rather than assuming either criterion is always sufficient at low cost.

## D. Exact experiments and what they do not prove

The new exact finite certificates establish:

* No collision between distinct odd cubefree integers with the SAME radical and all prime factors at most 100,000. All 9,591 exponent-1-versus-2 columns peel away.
* No collision among odd integers with exponents in \(\{0,2,4\}\) and prime factors at most 10,000. The 3,684 columns reduce to three with a minor of determinant 18.
* The same conclusion for exponents \(\{0,2,4,6\}\) and prime factors at most 1,000, with the same final minor.

These bounds are on prime factors, not on input size. Complete prime factorizations and recursive primality certificates are provided. Verify them, then investigate whether the elimination pattern has an arithmetic explanation. Do not silently extrapolate any finite certificate to unbounded primes.

The positive-control search rediscovered the previous odd cubefree collision
\[
\begin{aligned}
 a&=11^2 13^2 17\,19\,31\,61\,97\,127^2\,271\,307^2\,331\,367,\\
 b&=13\,17^2 19^2 23\,31^2 43\,61^2 83\,127\,307\,733\,5419,
\end{aligned}
\]
with common target
\[
 M=5276516179938729922490847708056660616574496169354744299520.
\]
Its inputs are respectively
\(60629697601617236747379985403\) and
\(61655391632564660609643619057\).
The full-divisor-summation verifier was rerun successfully. Since \(\gcd(ab,42)=1\), the four integers \(12a,14a,12b,14b\) are cubefree preimages of \(336M\). Thus odd-cubefree injectivity, cubefree multiplicity at most 2 or 3, and the old small-range classification are false.

In contrast, the previous note proves injectivity on squares of squarefree integers, and hence cubefree multiplicity at most 1 for odd TARGETS. Odd inputs and odd targets are not the same restriction.

A search over cubefree inputs with primes from 101 through 100,000 timed out without a witness after 25 seconds. This is inconclusive, not a negative certificate. Numerical solver infeasibility or optimality is not a proof unless independently certified.

## E. Preserve the known obstructions

Do not count merely powerful \(D\) with \(h(D)\mid N\). For
\(N_y=\prod_{3\le p\le y}h(p^2)\), every subset supplies such a \(D\), giving a positive maximal-order constant. The missing squarefree-completion condition is essential, even for odd represented targets.

Do not treat a primitive prime divisor as globally new or larger than its base. For example, 7 is primitive for both \(2^3-1\) and \(11^3-1\). Do not cancel an arbitrary gcd through \(h\); common unitary blocks can be canceled.

As a disproof route, seek pairwise prime-support-disjoint collisions \(h(a_i)=h(b_i)=M_i\) with bounded input exponents. They yield \(2^r\) preimages of \(\prod_iM_i\). A family with \(\log\prod_{i\le r}M_i=O(r\log r)\) would refute (EP). No such family is supplied. Repeated scaling of one collision is not independent replication.

## F. Read literature for specific missing ingredients

Read Kominers, *On the Number of Solutions of kσ(k)=n*, especially Remark 4.3, for the existing exponent-coloring limitation. Read Noppakaew–Pongsriiam, *Product of Some Polynomials and Arithmetic Functions*, Theorems 6 and 12, for related cross-divisibility methods and squarefree injectivity.

Read Bibby–Vyncke–Zelinsky, *On the Third Largest Prime Divisor of an Odd Perfect Number*, especially the σ-pair lemmas and quadratic mutual-divisibility descent. A classification of two-cycles is not automatically a bound on longer cycles or on all compatible exponent assignments.

Read Pollack–Pomerance–Thompson, *Divisor-sum fibers*, Theorem 1.4 and its construction. It concerns \(s(n)=\sigma(n)-n\), not \(h\), and shows why narrow relative intervals alone do not bound multiplicity. Check whether any structural construction can actually transfer; squarefree injectivity blocks a naive transfer. Pollack–Pomerance's fixed-abundancy results also cannot simply be imported, because \(\sigma(k)/k=N/k^2\) varies across our fiber.

Exact source links are in the proof note. The current Erdős problem page failed to load in this pass. Check actual newer proof claims when access permits, without assuming their validity or claiming exhaustive literature coverage.

## G. Execute and audit

Start by auditing the prime-index lemma and the entropy proof; then spend the main effort on the cross-prime constraints behind (R), not re-deriving the constant. Alternate a concrete proof attempt with targeted counterexample searches. State the strongest missing implication explicitly, and attack that implication before polishing a manuscript.

Use actual parallel workers for proof, counterexamples, and literature only when the tools exist. Otherwise report separate audit passes honestly. Return the strongest theorem established with its complete proof and reproducible computations. A complete resolution claim is appropriate only if the entire quantified implication to (EP) has been proved. If a gap remains, expose it as a mathematical statement; do not repackage a sufficient unproved certificate bound as a solution.
