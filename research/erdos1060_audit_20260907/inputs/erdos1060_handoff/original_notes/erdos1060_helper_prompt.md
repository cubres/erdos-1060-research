# Research continuation: Erdős Problem 1060

Continue the existing investigation of
\[
h(k)=k\sigma(k),\qquad f(N)=\#\{k\ge1:h(k)=N\}.
\]
The goal remains a complete, rigorously checked resolution, not merely an attractive conjectural argument. Work toward the proof, but actively search for counterexamples to intermediate claims. Do not assume that a requested conclusion must be true.

Prioritize Sections 4–6: first audit the counterexample and the bounded-exponent reduction, then attack the bounded-exponent problem. Use the literature to address concrete obstacles rather than allowing browsing to replace mathematical work.

## 1. Fix the exact quantitative target

The primary target is: for every \(\varepsilon>0\), there is \(N_\varepsilon\) such that
\[
f(N)\le\exp\!\left(\varepsilon\frac{\log N}{\log\log N}\right)
\qquad(N\ge N_\varepsilon).
\]
The bound must hold for every sufficiently large target, including highly exceptional smooth integers. An almost-all result, an average bound, \(N^{o(1)}\), or a smaller positive constant multiplying \(\log N/\log\log N\) does not establish this target. The optional stronger target is \(f(N)\le(\log N)^C\) for an absolute constant \(C\).

Maintain explicit labels: established literature, newly proved here, conditional, heuristic, and computational observation. Prove the deductions supplied below independently; no claim of their originality is being made. Do not spend the investigation repeatedly reproving the existing product bound.

## 2. Read these sources with specific questions

**Direct sources.** Check the current Erdős problem page and discussion, including dates and actual proof claims:
`https://www.erdosproblems.com/1060`
`https://www.erdosproblems.com/forum/thread/1060`
Read Richard K. Guy, *Unsolved Problems in Number Theory*, third edition, Problem B11, pp. 101–102, for the original formulation and constructions. Report inaccessible sources rather than inventing their contents.

Read Scott Duke Kominers, *On the Number of Solutions of kσ(k)=n*, particularly Theorem 1.2, Proposition 3.2, and Remarks 4.1–4.3:
`https://scottkom.com/assets/articles/Kominers_ksigmak.pdf`
Extract the established bound and its limitation. Separate its elementary proofs from its computer-assisted census. Check whether the promised code archive and any newer version are now available before adopting computational minimality claims.

Read Passawan Noppakaew and Prapanpong Pongsriiam, *Product of Some Polynomials and Arithmetic Functions*, Journal of Integer Sequences 26 (2023), Article 23.9.1, especially Theorems 3 and 12 and Questions 27–28:
`https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf`
Theorem 12 establishes squarefree injectivity in greater generality. Verify displayed constructions: the formula for the Mersenne construction printed in Question 27 appears to omit a factor. Use the directly verified construction in Section 7 below, not the uncorrected formula.

**Primitive collisions and data.** Consult OEIS A327153, A064987, A212490, A337873, A337875, and A337876, including references, history, and available data files. The last two are especially useful for collision structures, not just record multiplicities. Recompute every numerical identity used in a proof. Distinguish “at least r representations” from “exactly r,” and both from “the least target with exactly r.”

**Related decomposition methods.** Read Paul Erdős, *Remarks on number theory II: Some problems on the σ function* (1959), and Paul Pollack–Carl Pomerance, *Some problems of Erdős on the sum-of-divisors function* (2016), especially the discussion of friendly numbers and Section 4:
`https://www.renyi.hu/~p_erdos/1959-21.pdf`
`https://math.dartmouth.edu/~carlp/btran10.pdf`
Investigate their use of common unitary divisors, powerful parts, and parameter counting. Do not transplant a fixed-abundancy theorem: here \(\sigma(k)/k=N/k^2\) changes with \(k\). Any adaptation must explicitly handle that change and deliver the finer required asymptotic scale.

**Prime-factor dependence.** Consult Ford–Konyagin–Luca, *Prime chains and Pratt trees*, and Glasby–Lübeck–Niemeyer–Praeger, *Primitive prime divisors and the n-th cyclotomic polynomial*:
`https://arxiv.org/abs/0904.0473`
`https://arxiv.org/abs/1504.02598`
Look for transferable counting or encoding arguments. Their results are not automatically theorems about the dependence graph in this problem. State every imported theorem with its hypotheses, uniformity, and exceptional cases.

**Nearby but different inverse problems.** Check Akande, *The number of preimages of iterates of φ and σ*, and Gabdullin–Iudelevich–Luca, *Numbers of the form kf(k)*:
`https://arxiv.org/abs/2401.04073`
`https://arxiv.org/abs/2201.09287`
The first concerns prescribed values of σ and its iterates; the latter studies value-set questions for other arithmetic functions. Identify a concrete transferable lemma before spending substantial time on either.

An unrefereed working report is also relevant:
`https://erdosproblemaday.com/report/1060`
Use it as a source of leads, not an authority. In particular, its proposed powerful-core divisibility bound must be tested against the counterexample in Section 4.

Time-box the initial literature search. Thereafter, search for specific missing lemmas, their hypotheses, or counterexamples—not indefinitely for a paper whose title resembles the question.

## 3. Preserve the exact information in the olympiad argument

For a positive integer \(k\), write
\[
k=D(k)S(k),\qquad
D(k)=\prod_{v_p(k)\ge2}p^{v_p(k)},\qquad
S(k)=\prod_{v_p(k)=1}p.
\]
Then \(D(k)\) is powerful, \(S(k)\) is squarefree, and \(\gcd(D(k),S(k))=1\). Hence
\[
h(k)=h(D(k))h(S(k)).
\]
Squarefree injectivity means that a fixed powerful core determines at most one preimage. The known bound is therefore
\[
f(N)\le\prod_{p\mid N}v_p(N).
\]
The exact reduction retains substantially more information:
\[
f(N)=\#\left\{D:\begin{array}{l}
D\text{ powerful},\ h(D)\mid N,\\
N/h(D)=S\sigma(S)\text{ for a squarefree }S,\\
\gcd(D,S)=1
\end{array}\right\}.
\]
Count cores which actually admit this completion, not merely cores which divide the target.

The published majorant yields
\[
f(N)\le\exp\!\left(\left(\frac{\log3}{3}+o(1)\right)\frac{\log N}{\log\log N}\right).
\]
Its positive constant is sharp for \(g(N)=\prod_{p\mid N}v_p(N)\), along \(N=\prod_{p\le y}p^3\). It is not established to be sharp for \(f\). A sharper analysis of this majorant alone therefore cannot reach the required zero constant.

There is a constructive squarefree inverse. If the largest prime factor \(q\) of the residual is at least 5, a squarefree preimage must contain \(q\); remove \(q(q+1)\) and continue, rejecting nonintegral steps and repeated primes. The terminal possibilities are
\[
(S,h(S))=(1,1),(2,6),(3,12),(6,72).
\]
Prove the algorithm's correctness and use it to test proposed cores exactly.

## 4. Eliminate a tempting but false intermediate target

Define
\[
B(N)=\#\{D:\ D\text{ powerful and }h(D)\mid N\}.
\]
Although \(f(N)\le B(N)\), the desired little-o bound is FALSE for \(B\).

For \(y\ge3\), let
\[
N_y=\prod_{3\le p\le y}h(p^2)
=h\!\left(\prod_{3\le p\le y}p^2\right).
\]
Every subset \(T\) of these primes supplies the distinct core
\(D_T=\prod_{p\in T}p^2\), with \(h(D_T)\mid N_y\). Thus
\[
B(N_y)\ge2^{\pi(y)-1}.
\]
The prime number theorem gives
\[
\log N_y=(4+o(1))y,\qquad
\log B(N_y)\ge
\left(\frac{\log2}{4}+o(1)\right)
\frac{\log N_y}{\log\log N_y}.
\]
These counterexamples are odd targets and are themselves in the image of \(h\). Thus restricting the relaxed bound to represented targets or odd targets does not fix it.

The missing completion condition matters dramatically here: among these particular subset cores, only the full subset can have a squarefree completion. A proper subset leaves an odd residual greater than 1, whereas \(h(S)\) is even for every squarefree \(S>1\).

Use this family to stress-test every relaxation. A bound which forgets exact completion cannot be assumed to retain the conjectured scale.

## 5. Main proposed reduction: isolate bounded exponents

For fixed \(E\ge1\), define
\[
f_E(M)=\#\{u\ge1:h(u)=M,\ v_p(u)\le E\text{ for every prime }p\},
\qquad F_E(X)=\max_{1\le M\le X}f_E(M).
\]
Prove that it suffices to establish, for EVERY fixed \(E\),
\[
\log F_E(X)=o_E\!\left(\frac{\log X}{\log\log X}\right).
\tag{BE}
\]
Here is the reduction to verify. Split a preimage as
\[
k=D_EU_E,\qquad D_E=\prod_{v_p(k)>E}p^{v_p(k)}.
\]
The factors are coprime, every exponent in \(U_E\) is at most \(E\), and \(h(U_E)=N/h(D_E)\). Writing \(\alpha_p=v_p(N)\), the number of possible \(D_E\) is at most
\[
G_E(N)=\prod_{p\mid N}\left(1+\max\{\alpha_p-E,0\}\right).
\]
Consequently,
\[
f(N)\le G_E(N)F_E(N).
\tag{1}
\]
Set
\[
c_E=\sup_{a\in\mathbb Z,\ a\ge E+1}
\frac{\log(a-E+1)}a.
\]
The elementary small-prime/large-prime argument gives, for fixed \(E\),
\[
\log G_E(N)\le(c_E+o_E(1))\frac{\log N}{\log\log N}.
\tag{2}
\]
For completeness, split at \(z=\log N/(\log\log N)^3\). The primes at most \(z\) contribute \(O(\log N/(\log\log N)^2)\); for larger primes use \(\log(1+\max\{a-E,0\})\le c_Ea\) and \(\sum\alpha_p\log p=\log N\).

For \(E\ge2\),
\[
0\le c_E\le\frac{\log(E+1)}{E+1}\longrightarrow0.
\]
Given \(\varepsilon\), first fix \(E\) making \(c_E\) small, THEN choose \(N\) sufficiently large to apply (BE) and (2). This proves the primary target through (1). Do not let \(E\) vary with \(N\) without controlling all error terms. For \(E=1\), \(G_1(N)=\prod_{p\mid N}\alpha_p\) and \(F_1(N)=1\), so this framework recovers the olympiad bound exactly.

Conversely, the original target implies (BE). This is an equivalent reformulation when required for every fixed \(E\), not a solution disguised as a lemma. Its value is that unbounded prime-power exponents can be separated off at arbitrarily small asymptotic cost.

Start structurally with \(E=2\), then \(E=3\). Injectivity already fails for \(E=2\), because \(h(12)=h(14)\). What is needed is control of multiplicity. A bound \(f_E(M)\ll_E(\log M)^{C_E}\), or even \(f_E(M)\le C_E\), would suffice, but neither is supplied as a theorem. Proving only one fixed value of \(E\) would be partial progress.

## 6. Two concrete structural routes for the bounded-exponent problem

**Route A: exact valuation constraints and short certificates.** For each prime \(p\mid N\), form
\[
\mathcal E_p=\{0\le e\le\min(E,\alpha_p):p^e\sigma(p^e)\mid N\}.
\]
For a solution, the chosen exponents satisfy, for every prime \(q\mid N\),
\[
\alpha_q=e_q+\sum_{p\mid N}v_q\!\left(\sigma(p^{e_p})\right).
\tag{3}
\]
Membership in \(\mathcal E_p\) excludes factors outside the target. Together with (3), these conditions are exact, not heuristic.

Study the dependence relation \(p\to q\) when \(q\mid\sigma(p^e)\). At exponent 1 the arrows descend apart from the small-prime exception; higher exponents create upward links. Seek a proved reconstruction rule from a small set of choices, or a decision tree whose TOTAL logarithmic branching cost is \(o_E(\log N/\log\log N)\).

Explicitly account for cycles, reused output primes, valuation capacities, and the cost of identifying the exceptional choices. “Only a few branches” is not an estimate. A proposed certificate must have both a decoder and a proved count. Showing that almost all primes behave well does not control the exceptional targets required here.

Use
\[
\sigma(p^e)=\prod_{\substack{d\mid e+1\\d>1}}\Phi_d(p)
\]
when helpful, but do not infer globally fresh prime factors from Zsigmondy's theorem. For example, 7 is a primitive divisor for both \(2^3-1\) and \(11^3-1\). Primitivity for one base is not uniqueness across different bases, and does not force a prime divisor to exceed that base.

**Route B: integer coordinates adapted to squarefree inputs.** Independently prove that the numbers \(h(p)=p(p+1)\), over primes \(p\), form a multiplicative integer basis of the positive rational numbers. Thus every positive rational \(x\) has a unique finite expression
\[
x=\prod_p h(p)^{b_p(x)},\qquad b_p(x)\in\mathbb Z.
\]
For primes at least 5, all prime factors of \(p+1\) are smaller than \(p\), giving triangular elimination. The initial block is invertible over the integers because
\[
2=h(3)/h(2),\qquad 3=h(2)^2/h(3).
\]
A residual \(R\) has a squarefree preimage exactly when every \(b_p(R)\) is 0 or 1; coprimality with a proposed core adds \(b_p(R)=0\) for \(p\mid D\).

This converts completion into an exact integer-vector constraint. Investigate the vectors \(b(h(p^e))\) for bounded \(e\), their dependencies, and whether they admit a useful sparse encoding. As a sanity check,
\[
h(4)=h(2)h(7)/h(3)
\]
recovers the collision between 12 and 14. A coordinate change alone is not progress: specify and prove the counting advantage sought from it.

## 7. Compute to discover or destroy lemmas

Inspect actual hardware and software, set explicit time and memory limits, and use exact arithmetic. Prefer targeted inverse searches to blindly extending the record census.

Implement two independent checks: direct divisor enumeration for a factored target, and a prime-power search using (3) or powerful-core completion. Each prime may contribute at most one selected prime-power block. Track the remaining valuation vector and require exact exhaustion; nonnegative leftover valuations are not enough. Prove every pruning rule and the enumeration's completeness.

For collision structure, cancel
\[
C=\prod_{v_p(a)=v_p(b)>0}p^{v_p(a)}.
\]
This is a common unitary divisor, so \(h(a/C)=h(b/C)\). Do not simply cancel \(\gcd(a,b)\) through \(h\): the required coprimality can fail. Also do not conflate “no common unitary divisor” with every alternative definition of a primitive collision without proving equivalence.

Mandatory sanity checks include
\[
h(12)=h(14)=336,
\quad h(315)=h(351)=196560,
\quad h(160)=h(189)=60480.
\]
The second rules out injectivity on odd inputs; it says nothing by itself about odd TARGETS. The third rules out the claim that distinct preimages must have a common prime factor.

Test multiplicative replication. If \(h(a_i)=h(b_i)=N_i\), \(a_i
e b_i\), and the supports of \(a_ib_i\) are pairwise disjoint, independently choosing \(a_i\) or \(b_i\) produces \(2^r\) preimages of \(\prod_{i=1}^rN_i\). Bounded input exponents remain bounded. A family with \(\log\prod_iN_i=O(r\log r)\) would contradict the primary target. No such family is supplied; use this as a diagnostic for why independent collisions must be scarce or expensive. Repeated coprime scaling of a single collision is not an independent family.

Verify the correct Mersenne construction. For distinct primes \(M_i=2^{r_i}-1\), put
\[
R=\sum_i r_i,\qquad
k_i=2^{r_i-1}\prod_{j\ne i}M_j.
\]
Then
\[
h(k_i)=2^{R-1}\prod_jM_j
\]
for every \(i\). Any proposed universal bound must accommodate these families. Do not assume the infinitude of Mersenne primes.

Search deliberately among products of small prime powers, targets arising from many geometric sums, and fibers with many bounded-exponent preimages. For each potential lemma, search for its smallest counterexample before building a proof on it. Measure \(f_E\), not just \(f\), and record the precise cancellation patterns.

Exploratory computations supplied with this continuation examined inputs \(k\le5{,}000{,}000\). Among cubefree collisions it found only the reduced pair \((12,14)\) after cancelling common unitary prime powers; it found no cubefree fiber of size 3 in that input range. Two implementations, using divisor-sum and multiplicative formulas for sigma respectively, agreed on this observation. Treat it solely as a lead to independently reproduce and challenge. It does not prove a classification or a uniform bound.

For any global census through a target bound \(X\), justify completeness using \(h(k)>k^2\) for \(k>1\). A scan through \(k\le K\) certifies complete fibers only for targets at most \(K^2\), not for every larger value encountered during the scan.

## 8. Use independent verification and finish with an honest theorem ledger

When genuine parallel-agent tools are available, assign separate workers to literature verification, the bounded-exponent proof, counterexample/computational search, and independent refereeing. Otherwise perform these as explicitly separated passes; do not invent agents or claim independent verification that did not occur.

Have the referee attack the strongest intermediate lemma before polishing the exposition. Check hidden dependence on \(E\), \(\varepsilon\), \(N\), and the prime support; misuse of multiplicativity; unjustified squarefree completion; accidental assumptions that prime factors are distinct; and transitions from average behavior to a uniform maximum. Challenge the argument on the Section 4 family and every verified collision above.

Continue beyond a reading list or the known majorant: develop the leading route until it produces a proved lemma, an explicit counterexample, or an exact unresolved implication, then update the strategy. Do not abandon the investigation merely because the problem is labelled open, and do not produce a proof claim merely because one was requested.

The final report should state the strongest theorem actually established and its full proof; identify precisely whether it resolves the quantified primary target; give any remaining gap as a standalone mathematical statement; distinguish known results from new deductions; and attach reproducible code for computational claims. Prepare a ready-to-post proof claim only after the complete implication to the target survives the independent audit. If a gap remains, give a clearly labelled partial-results note instead of presenting it as a solution.
