# Research continuation v2: Erdős Problem 1060

Continue the investigation of
\[
h(k)=k\sigma(k),\qquad f(N)=\#\{k\ge1:h(k)=N\}.
\]
The goal is a rigorously verified resolution of the uniform statement
\[
\forall\varepsilon>0\ \exists N_\varepsilon\ \forall N\ge N_\varepsilon:
\quad f(N)\le\exp\!\left(\varepsilon\frac{\log N}{\log\log N}\right).
\tag{EP}
\]
The stronger polylogarithmic bound is optional. Do not substitute an average bound, an almost-all result, \(N^{o(1)}\), or a positive-constant improvement for (EP). Actively investigate both proof and counterexample mechanisms.

This update supersedes the earlier small-range cubefree observations. It supplies a stronger elementary bound, exact counterexamples to tempting shortcuts, and a narrower quantitative bottleneck. The accompanying `proved_additions.md` contains complete proofs and `verify_witnesses.py` provides independent integer checks. Independently audit them; their originality relative to the full literature is not asserted.

Do not make the next deliverable another research plan. Work on the mathematics until you obtain a proved advance, a counterexample to a proposed lemma, or a precisely isolated remaining assertion. Continue revising the approach when a route fails.

## 1. Start from the stronger exponent-coloring lemma

Let \(\operatorname{odd}(t)=t/2^{v_2(t)}\).

**Supplied lemma:** Within a fiber of \(h\), the data
\[
\left(v_2(k),\ \bigl(\operatorname{odd}(v_p(k)+1)\bigr)_{p\text{ odd}}\right)
\]
determine \(k\) uniquely.

Here is the proof to audit. If exponents \(a>b\) have the same color, then \(a+1=2^j(b+1)\) for some \(j\ge1\). Put \(d=a-b\). Then
\[
\frac{h(p^a)}{h(p^b)}=p^d Q_p,
\quad Q_p=\frac{p^{a+1}-1}{p^{b+1}-1}\in2\mathbb Z,
\quad \operatorname{odd}(Q_p)<p^d
\]
for every odd \(p\), because
\[
Q_p<\frac{p^d}{1-p^{-(b+1)}}\le\frac32p^d.
\]
Cancel equal local factors. Let \(A\) and \(B\) be the products of the excess prime powers on the two sides; they are coprime. After taking odd parts of the equality, \(A\) divides the product of the opposite-side odd parts of \(Q_p\), and conversely for \(B\). Multiplication gives \(AB<AB\) unless no exponent differs.

For \(\alpha_p=v_p(N)\), this gives
\[
\boxed{f(N)\le(\alpha_2+1)
\prod_{\substack{p\mid N\\p\text{ odd}}}
\left(\left\lfloor\frac{\alpha_p}{2}\right\rfloor+1\right),}
\tag{1}
\]
with \(\alpha_2=0\) for odd \(N\). The number of colors at an odd prime is the number of odd integers at most \(\alpha_p+1\).

Using \(\log(\lfloor a/2\rfloor+1)\le a\log2/2\) and splitting primes at \(\log N/(\log\log N)^3\), obtain
\[
\log\max(1,f(N))\le
\left(\frac{\log2}{2}+o(1)\right)\frac{\log N}{\log\log N}.
\tag{2}
\]
This improves the \(\log3/3\) consequence of the majorant in Kominers [1]. It is not (EP). The majorant in (1) itself has constant \(\log2/2\) on products of odd prime squares, so optimizing that majorant alone cannot finish the problem.

The reusable mechanism is **cross-divisibility plus strict loss after removing a controlled set of small prime factors**. Investigate ways to make that mechanism global. Do not assume that a chain of pairwise admissible exponent mergers is an admissible color class: every pair in a proposed class must satisfy the needed property.

## 2. Replace the misleading cubefree intuition with exact witnesses

Let
\[
\begin{aligned}
a&=11^2\,13^2\,17\,19\,31\,61\,97\,127^2\,271\,307^2\,331\,367,\\
b&=13\,17^2\,19^2\,23\,31^2\,43\,61^2\,83\,127\,307\,733\,5419.
\end{aligned}
\]
Then
\[
a=60629697601617236747379985403,\qquad
b=61655391632564660609643619057,
\]
and
\[
h(a)=h(b)=5276516179938729922490847708056660616574496169354744299520=:M.
\tag{3}
\]
Both are odd and cubefree, every input prime is at least 11, and no prime has the same positive exponent in both inputs. Since \(\gcd(ab,42)=1\),
\[
12a,\quad14a,\quad12b,\quad14b
\]
are four distinct cubefree preimages of \(336M\).

These identities have been checked both by exact local products and by constructing and summing every divisor of each input. The exact inverse program gives \(f_2(M)=2\), \(f_2(336M)=4\); the full multiplicities are 2 and 6, respectively. No minimality or record claim is made.

Therefore do not attempt to prove odd-cubefree injectivity, cubefree multiplicity at most 2 or 3, or that all cubefree collisions come from \((12,14)\). None of these statements is true.

A contrasting supplied theorem is that \(h(r^2)=h(s^2)\) for squarefree \(r,s\) implies \(r=s\). Its proof in the accompanying note uses the facts that primes \(2\pmod3\) cannot divide \(p^2+p+1\), and \(v_3(p^2+p+1)=1\) for primes \(p\equiv1\pmod3\), followed by a strict product comparison. Thus \(f_2(N)\le1\) for odd targets. **Odd inputs and odd targets are different restrictions.** Audit this theorem before using it.

## 3. Focus on the bounded-exponent, rough-input bottleneck

For fixed \(E\), split a preimage into its prime-power factors of exponent exceeding \(E\) and its remaining factors. The former have at most
\[
G_E(N)=\prod_{p\mid N}\left(1+\max\{\alpha_p-E,0\}\right)
\]
possible values. For fixed \(E\),
\[
\log G_E(N)\le(c_E+o_E(1))\frac{\log N}{\log\log N},
\quad c_E=\sup_{a\ge E+1}\frac{\log(a-E+1)}a\longrightarrow0.
\]
Also fix the remaining exponents at primes \(p\le\delta\log N\), for a fixed \(\delta>0\). This costs at most \((E+1)^{\pi(\delta\log N)}\).

Define, with \(P^-(1)=\infty\),
\[
R_{E,\delta}(X)=\max_{1\le M\le X}
\#\{u:h(u)=M,\ v_p(u)\le E,\ P^-(u)>\delta\log X\}.
\]
The precise reduction is
\[
\boxed{f(N)\le G_E(N)(E+1)^{\pi(\delta\log N)}R_{E,\delta}(N).}
\tag{4}
\]
Consequently the following statement, for every fixed \(E\) and \(\delta>0\), suffices:
\[
\boxed{\log R_{E,\delta}(X)=o_{E,\delta}\left(\frac{\log X}{\log\log X}\right).}
\tag{R}
\]
Indeed the three contributions have constants \(c_E\), \(\delta\log(E+1)\), and zero. First choose \(E\), then choose \(\delta\), then take \(N\) sufficiently large.

Statement (R) is a reformulation of the unresolved difficulty, not a proved lemma. Proving only \(E=2\) would not settle every fixed \(E\). A growing cutoff must use the original \(X\), not an inconsistently substituted residual target.

For these rough inputs, with \(y=\delta\log X>1\), one additionally has
\[
\sqrt M\exp\!\left(-\frac{\log X}{4(y-1)\log y}\right)
\le u\le\sqrt M.
\]
This follows from \(\log(\sigma(u)/u)\le\omega(u)/(y-1)\) and \(\log u\le\tfrac12\log X\). The interval has relative width \(O_\delta(1/\log\log X)\). Use this only with a proved arithmetic counting argument; concentration near \(\sqrt M\) by itself is not enough.

## 4. Primary structural route: exact reconstruction with a small cost

For a factored target \(M=\prod q^{\alpha_q}\), define
\[
\mathcal E_p=\{0\le e\le\min(E,\alpha_p):p^e\sigma(p^e)\mid M\}.
\]
Impose roughness by forcing the excluded input primes to exponent zero. A preimage is exactly a choice satisfying every target-prime equation
\[
\boxed{\alpha_q=e_q+\sum_{p\ne q}v_q(\sigma(p^{e_p})).}
\tag{5}
\]
Account also for output primes outside the allowed input support. Never omit a valuation row because that prime cannot appear in the input.

Draw \(p\to q\) when \(q\ne p\) divides \(\sigma(p^e)\) for some admissible exponent. There is a rigorous reconstruction lemma:

**If deleting vertices \(S\) makes this directed graph acyclic, then the number of preimages is at most \(\prod_{p\in S}|\mathcal E_p|\).**

Fix the exponents on \(S\), then use (5) in topological order. Every remaining exponent is forced because \(q\nmid\sigma(q^e)\).

A sufficient target is therefore
\[
\sum_{p\in S}\log|\mathcal E_p|
=o_{E,\delta}(\log X/\log\log X).
\tag{6}
\]
Do not assume such a cheap set exists. Test (6) on generated hard targets. The union graph includes incompatible choices and may exaggerate the true branching. When necessary, replace it with an adaptive decision tree or a more economical reconstruction certificate. Supply a decoder and count the possible certificates, including the cost of locating exceptional primes.

Analyze the witness (3) in detail: its valuation flows, strongly connected components, and how exponent-1 and exponent-2 factors jointly sustain the collision. Any proposed structural theorem must accommodate it. Sparse short cycles do not by themselves imply few solutions; explain how longer cycles, shared factors, and repeated valuation demands are controlled.

## 5. Bring in the relevant descent literature

Read Bibby–Vyncke–Zelinsky [3], especially the definition of \(\sigma_{m,n}\) pairs and Lemmas 4–8. A pair consists of primes with mutual divisibility by the indicated divisor sums, so it models a two-cycle in the dependence graph.

Its quadratic mutual-divisibility classification leads to
\[
5pq=p^2+q^2+p+q+1,
\qquad
(t_1,t_2)=(1,1),\quad
 t_{j+2}=\frac{t_{j+1}^2+t_{j+1}+1}{t_j}.
\]
This is a concrete Vieta-style descent to investigate, rather than a generic instruction to use cyclotomic polynomials. Check all hypotheses, orientations, and small-prime exceptions. Restrictions on two-cycles do not automatically control an entire collision graph.

Read Theorem 6 of Noppakaew–Pongsriiam [2] for a related cross-divisibility/strict-size argument, and Theorem 12 for squarefree injectivity. Seek a reusable lemma, not an unjustified transfer between different arithmetic functions.

The cyclotomic identity
\[
\sigma(p^e)=\prod_{\substack{d\mid e+1\\d>1}}\Phi_d(p)
\]
is available. A primitive prime divisor is not necessarily globally new or larger than its base: 7 is primitive for both \(2^3-1\) and \(11^3-1\). Any assignment of output primes to inputs must account for collisions and valuations.

## 6. Use computation to find the right theorem

Do not prioritize extending a consecutive-input census. The witness (3) has 29-digit inputs but was found by searching bounded prime supports and exponent differences.

For every allowed input prime \(p\) and unequal \(a,b\in\{0,\ldots,E\}\), form the integer column
\[
\nu(h(p^a))-\nu(h(p^b)),
\]
where \(\nu\) includes every prime appearing in any local block. Choose at most one ordered difference per prime, require a nonempty selection, and set the column sum to zero. This is an exact model of collisions after removing common equal-exponent prime-power blocks. A mixed-integer solver can search it; exact integer arithmetic must certify every witness.

The supplied `collision_milp.py` implements this discovery model. Its floating-point infeasibility or optimality messages are not mathematical certificates. The witness remains valid independently of either message. Record prime-support bounds separately from bounds on inputs and targets.

Use `exact_target_search.py` to enumerate complete fibers of selected factored targets. Independently verify all claimed witnesses with divisor summation. Require exact target exhaustion and at most one selected local prime-power block per input prime. Prove every pruning rule.

Experiment with excluding small primes, excluding previously used input supports, and minimizing the support or size of a collision. Compare these searches with the roughness threshold in (R), not just with a fixed numerical minimum prime.

If \(h(a_i)=h(b_i)=M_i\) and the prime supports of \(a_ib_i\) are pairwise disjoint, the choices multiply to give \(2^r\) preimages of \(\prod_iM_i\). A family with \(\log\prod_iM_i=O(r\log r)\) would refute (EP). No such family is supplied. Determine whether independent collisions are forced to be too expensive; do not confuse scaling one collision with independent replication.

Only common unitary prime-power blocks can be canceled automatically through \(h\). Arbitrary gcd cancellation is invalid.

## 7. Preserve these obstruction tests

Do not replace exact squarefree completion by the relaxed count
\[
B(N)=\#\{D\text{ powerful}:h(D)\mid N\}.
\]
For \(N_y=\prod_{3\le p\le y}h(p^2)\), every subset of the input primes supplies such a \(D\), so
\[
\log B(N_y)\ge\left(\frac{\log2}{4}+o(1)\right)
\frac{\log N_y}{\log\log N_y}.
\]
These targets are odd and represented. Yet a proper subset leaves an odd residual greater than 1, which cannot equal \(h(S)\) for squarefree \(S>1\). Completion information is essential.

Retain the Mersenne construction in its correct form: for distinct Mersenne primes \(M_i=2^{r_i}-1\), set \(R=\sum_i r_i\) and \(k_i=2^{r_i-1}\prod_{j\ne i}M_j\). Then \(h(k_i)=2^{R-1}\prod_jM_j\). Do not assume infinitely many Mersenne primes.

Fixed-abundancy estimates for \(\sigma(k)/k\), including related work by Erdős and Pollack–Pomerance [4], do not immediately apply because here that ratio equals \(N/k^2\) and varies across the fiber.

## 8. Workflow and final proof audit

First independently audit the supplied lemmas and witnesses. Then investigate (R), beginning with the exact cubefree dependence structure but retaining a route to arbitrary fixed \(E\). Alternate proof attempts with targeted counterexample searches. State the strongest unproved intermediate assertion explicitly and attack it before polishing surrounding arguments.

Use genuine parallel workers for literature verification, structural proof attempts, counterexamples, and independent refereeing only when those tools exist. Otherwise perform separate audit passes and report them accurately.

Check every quantifier, parameter dependence, coprimality assumption, valuation capacity, and implication from a counting lemma to (EP). A new positive constant is useful partial progress, not a solution. A hypothetical cheap reconstruction scheme is not a theorem until its decoder and cost bound are proved.

Do not stop merely because the problem has an open-problem label, and do not label an argument complete merely because a complete proof was requested. Prepare a ready-to-post resolution claim only after the entire argument to (EP) survives the audit. Otherwise provide the strongest proved result, its full proof, reproducible computations, and the remaining mathematical statement without disguising the gap.

## Sources, in priority order

[1] Scott Duke Kominers, *On the Number of Solutions of kσ(k)=n*, especially Theorem 1.2, Proposition 3.2 and Remarks 4.1–4.3.
`https://scottkom.com/assets/articles/Kominers_ksigmak.pdf`

[2] Passawan Noppakaew and Prapanpong Pongsriiam, *Product of Some Polynomials and Arithmetic Functions*, Journal of Integer Sequences 26 (2023), Article 23.9.1. Theorems 6 and 12.
`https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf`

[3] Sean Bibby, Pieter Vyncke, Joshua Zelinsky, *On the Third Largest Prime Divisor of an Odd Perfect Number*, arXiv:1908.09420v3. The σ-pair and descent sections.
`https://arxiv.org/abs/1908.09420`

[4] Paul Pollack and Carl Pomerance, *Some problems of Erdős on the sum-of-divisors function* (2016). Common unitary divisors and primitive friendly pairs, with the necessary distinction between different collision problems.
`https://math.dartmouth.edu/~carlp/btran10.pdf`

Check the current problem page and discussion for actual proof claims and their dates, reporting access failures rather than inferring status:
`https://www.erdosproblems.com/1060`
`https://www.erdosproblems.com/forum/thread/1060`

Use OEIS A327153, A064987, A212490, A337875, and A337876 for verified examples and references, not as substitutes for structural arguments. Consult Guy, *Unsolved Problems in Number Theory*, Problem B11, for historical context. Add further literature only to address an identified mathematical obstacle.
