# Independent primary-literature review for Erdős Problem 1060

Checked 7 September 2026. This is a targeted literature audit, not a proof of the conjecture and not a claim that every existing paper has been located. The supplied bibliography and 5 September notes were treated as leads, not evidence. No attachment scripts were executed.

Write \(h(k)=k\sigma(k)\), \(f(N)=\#h^{-1}(N)\), and \(T(N)=\log N/\log\log N\). The requested statement is \(\log f(N)=o(T(N))\), uniformly over targets with nonempty fibers. A bound \(\exp(C T(N))\) with a fixed positive constant is insufficient. The polylogarithmic bound is a separate, stronger question.

## 1. Current direct sources

**Kominers, *On the Number of Solutions of \(k\sigma(k)=n\)*, working paper, 2026.**

Author's [current research list](https://www.scottkom.com/research/mathematics/) labels the paper a working paper. The [10-page manuscript](https://www.scottkom.com/assets/articles/Kominers_ksigmak.pdf) was reaccessed. Theorem 1.2 gives
\[
 f(N)\leq\prod_{p\mid N}v_p(N),
\]
and Corollary 1.3 gives
\[
 \log f(N)\leq\left(\frac{\log3}{3}+o(1)\right)T(N).
\]
Proposition 3.2 proves sharpness of that constant for the *majorant*, attained along cubed primorials; it does not prove a matching lower bound for \(f\). Its squarefree-injectivity proof and coloring proof were inspected directly and are elementary. Remark 4.1 explicitly separates fixed-abundancy fibers. Remark 4.2 gives the corrected Mersenne construction. The manuscript's status footnote concerns July 2026, not all subsequent work. This is the strongest directly applicable general upper bound verified in this audit.

**Problem database status.** The [indexed problem page](https://www.erdosproblems.com/1060) returned OPEN and the exact little-o question, with a stronger polylog suggestion. The retrieved index says the page was edited 28 September 2025 and crawled roughly two months ago; direct access is unreliable. Its own warning says the curator may not know all relevant literature. Thus the defensible conclusion is that the retrieved listing is open and this targeted search found no closing theorem, not that a complete live literature census proves global nonexistence of a solution.

**Noppakaew–Pongsriiam, J. Integer Sequences 26 (2023), Article 23.9.1.** Theorem 12 in the [original journal PDF](https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf) proves injectivity of \(n^a\sigma(n)^b\) on squarefree inputs for all positive integers \(a,b\). It does not prove fixed-radical injectivity or bounded-exponent injectivity. Questions 27–28 ask about \(x\sigma(x)=m\) multiplicities. The displayed Mersenne formula in Question 27 is defective; see Section 3 below. That defect does not affect Theorem 12.

## 2. Nearby theorems and why they do not transfer

| Primary source inspected | Exact relevant information | Applicability to 1060 |
|---|---|---|
| Pollack, [*On the greatest common divisor of a number and its sum of divisors, II*](https://www.pollack-math.net/gcdnsigmasequel.pdf), §1.1 | Wirsing's count of \(n\leq x\) satisfying \(\sigma(n)=\lambda n\) is \(x^{O(1/\log\log x)}\), with the implied constant independent of \(\lambda\). The paper explains denominator-driven reconstruction. | Still a positive constant on the critical logarithmic scale. Moreover, if \(h(k)=N\), the abundancy is \(N/k^2\), which differs for every distinct preimage. |
| Pollack, [*On the greatest common divisor of a number and its sum of divisors*](https://www.pollack-math.net/combined3.pdf), Theorem 4.1 | The number of \(n\leq x\) with prescribed reduced denominator \(b(n)=n/\gcd(n,\sigma(n))\) is at most \(x^{C/\sqrt{\log\log x}}\), for absolute \(C\). | Its logarithm divided by \(\log x/\log\log x\) grows like \(C\sqrt{\log\log x}\). No target reduction cancels this loss. |
| Pollack–Pomerance, [*Some problems of Erdős on the sum-of-divisors function*](https://math.dartmouth.edu/~carlp/btran10.pdf), Theorem 1.5 | Primitive friendly pairs in \([1,x]\) number at most \(x^{1/2+o(1)}\). Friendly means equal abundancies; primitive means no nontrivial common unitary divisor. | Both the equation and the primitive definition differ from genuine minimal exchanges in an \(h\)-fiber. It is not a uniform maximum-fiber theorem. |
| Pollack, [*Remarks on fibers of the sum-of-divisors function*](https://www.pollack-math.net/preimages-maier3.pdf), Theorem 2 and Remarks 5–6 | Almost all values of \(\sigma\) have all preimages sharing their largest prime factor. Remark 6 extends the conclusion to any fixed number of largest prime factors. | Exceptional values remain. A maximum over all adversarial targets cannot discard them. Also the function is \(\sigma\), not \(h\). |
| Pollack–Pomerance–Thompson, [*Divisor-sum fibers*](https://math.dartmouth.edu/~carlp/divisor-sum-fibers-5.3.pdf), Theorem 1.4 | For any fixed positive \(\alpha,\epsilon\), infinitely many \(m\) have at least \(\exp(c\log m/\log\log m)\) preimages under \(s(n)=\sigma(n)-n\) in \((\alpha(1-\epsilon)m,\alpha(1+\epsilon)m)\); \(c=1/7\) works. | A warning against generic interval arguments. This is a different function, and the relative interval width is fixed rather than tending to zero. It gives no lower bound for \(f\). |
| Ford–Konyagin–Luca, [*Prime chains and Pratt trees*](https://arxiv.org/pdf/0904.0473), Theorem 1 | For increasing prime chains \(p_i\mid p_{i+1}-1\), \(N(x;p)\leq x\exp(\log x(\log_3x+O(1))/\log_2x)\), hence \(O_\epsilon(x^{1+\epsilon})\). | The direction and growth of these chains are essential. Edges \(q\mid\sigma(p^a)\) can go either way in size and form cycles. No transfer theorem was found. |
| Akande, [*The number of preimages of iterates of \(\varphi\) and \(\sigma\)*](https://arxiv.org/pdf/2401.04073), Theorem 1 | For fixed iteration count \(j\), \(\beta<j-1\), and \(a\in\{\varphi,\sigma\}\), \(\#\{m:a^{\circ j}(m)=n\}\leq n/L_{j,\beta+1}(n)^{1+o(1)}\), where \(L_{j,u}(n)=\exp(\log n(\log_3n)^u/(\log_2n)^j)\). | The input/output relation is an iterate, not the product \(k\sigma(k)\). The upper bound remains \(n^{1-o(1)}\), much larger than the divisor bound relevant here. |
| Gabdullin–Iudelevich–Luca, [*Numbers of the form \(kf(k)\)*](https://arxiv.org/abs/2201.09287), abstract and definitions | Studies the number of *distinct values* at most \(x\) for \(f=\tau,\omega,\varphi\). In particular the \(\varphi\) value count is asymptotic to \(c_0\sqrt{x}\). | No maximum fiber for \(k\sigma(k)\) is asserted. A value-set asymptotic cannot be substituted for one. |
| Evertse–Schlickewei–Schmidt, [*Linear equations in variables which lie in a multiplicative group*](https://arxiv.org/pdf/math/0409604), Theorem 1.1 | In dimension \(d\) and rank \(r\), the number of nondegenerate solutions is at most \(\exp((6d)^{3d}(r+1))\). The paper explicitly distinguishes rank of a subgroup of \((K^*)^d\) from rank of a scalar group whose direct power is used. | Even at fixed \(d\), this remains exponential in growing rank. No bounded-loss encoding of a whole exponent transversal as one fixed-dimensional nondegenerate equation was found. |
| Hirata-Kohno–Kawashima–Poëls–Washio, [*S-unit equation in two variables and Padé approximations*](https://arxiv.org/pdf/2211.14399), theorem statement also in [author's 2024 seminar abstract](https://ntrg.math.unideb.hu/Hirata-Kohno2024abstract.pdf) | For number-field degree \(m\) and \(s\) places, the binary \(S\)-unit equation has at most \((3.1+5(3.4)^m)45^s\) solutions. | Sharper than older exponential bounds, but still \(\exp(C s)\), not \(\exp(o(s))\). |
| Wang–Xu, [*Paucity phenomena for polynomial products*](https://arxiv.org/pdf/2211.02908), Theorem 1.1 | For fixed polynomial \(P\) of degree at least two with at least two distinct roots, \(A_{P,2j}([X])=j!X^j+O_{P,j,\epsilon}(X^{j-1/(6e_P)+\epsilon})\). | An interval-average product-energy count with constants depending on the number of factors. Here the prime support is fixed adversarially and its size grows. No per-support fiber conclusion follows. |

For Yamada's particularly close-looking theorem, see the more detailed parameter and statement audit below.

## 3. Historical-source defects verified directly

The [Guy chapter sample](https://www.kulturkaufhaus.de/annot/564C42696D677C7C393738303338373230383630327C7C504446.pdf?sq=1), third edition, B11, pp. 96–97, was downloaded and page 97 visually inspected. It records the little-o question and the possible polylog strengthening. It also gives Moser's primitive definition: a collision cannot be reduced to a collision by simultaneously dividing both members by any common integer greater than one.

Two problems in that discussion require care:

1. The Mersenne display really says \(n_i=A/M_i\), with \(A=\prod M_j\). It cannot produce a common \(n_i\sigma(n_i)\). For \(M_1=3,M_2=7\), the values are \(h(7)=56\) and \(h(3)=12\). Noppakaew–Pongsriiam reproduce the defective display. The corrected formula is
   \[
   n_i=2^{p_i-1}\prod_{j\ne i}(2^{p_j}-1),\qquad
   h(n_i)=2^{\sum p_j-1}\prod_j(2^{p_j}-1).
   \]
   This always involves prime 2 and does not give a family with arbitrarily large least input prime and fixed exponent cap.

2. Guy attributes a \(cx+o(x)\) asymptotic for product-collision pairs to Erdős. But [Erdős 1959](https://www.renyi.hu/~p_erdos/1959-21.pdf), Theorem 2, p. 175, visibly concerns \(\sigma(a)/a=\sigma(b)/b\). Its Theorem 1 likewise concerns values of the abundancy ratio. Therefore the original paper does not directly substantiate the product-pair attribution. This audit does not prove the product-pair asymptotic false; it marks the citation/transfer as unverified.

Local evidence copies and page renders are in `literature_sources/` beside this report. PDFs were obtained directly from the URLs above; no content was modified.

## 4. Yamada: exact parameter mismatch and a local statement caveat

In [*Multiplicative structures of values of the sum-of-divisors function*](https://arxiv.org/pdf/math/0512175), Theorem 1.4 requires a prime
\[
 q>\frac{16}{9}\mathrm e\,s^4
\]
and bounds prime-base solutions of
\[
 \sigma(p^{q-1})=\prod_{i=1}^s m_i^{e_i}
\]
by
\[
 s\left(\frac{\log c_7+19s\log(s+2)+3\sum_{i=2}^s\log\log m_i}{\log q}+7\right),
 \quad c_7=2^{12}38^2 1500^2.
\]
For fixed input exponent cap \(R\), one has \(q\leq R+1\), so this hypothesis allows only bounded \(s\). It does not address the difficult growing-support regime.

Lemma 7.1 is printed with arbitrary positive integers \(e,q\) and distinct primes \(p_0,p_1,p_2\); page 12 was downloaded, rendered, and visually checked. In that literal generality it is false: choose \((p_0,e,q,p_1,p_2)=(2,5,8,3,5)\). Both required eighth-power congruences hold modulo 32; yet \(H_1=\log32/\log3>3\), \(H_2=\log32/\log5>2\), and \(3H_1H_2/4>4.5>\gcd(8,1)\). The proof's root-count step needs restrictions. This counterexample is not a refutation of Theorem 1.4, whose special prime-index regime differs.

## 5. A safe local lemma proved for this audit

This is an elementary auxiliary observation; no novelty is claimed. A separate `independent_proof` agent checked the lemma, its two-base corollary, and the divisor-sum application on 7 September 2026 and confirmed the argument under the stated hypotheses.

**Lemma.** Let \(\ell\) be an odd prime, let \(d,e\geq1\) with \(\gcd(d,\ell)=1\), and let \(p_1,\ldots,p_t\) be distinct primes different from \(\ell\), all satisfying \(p_i^d\equiv1\pmod{\ell^e}\). If \(A_i\geq0\) and
\[
 \sum_{i=1}^t A_i\log p_i\leq e\log\ell,
\]
then
\[
 \prod_{i=1}^t(\lfloor A_i\rfloor+1)\leq\gcd(d,\ell-1).
\]

**Proof.** The products \(\prod_i p_i^{a_i}\), with integers \(0\leq a_i\leq\lfloor A_i\rfloor\), are distinct by unique factorization. They are at most \(\ell^e\), and equality is impossible because none contains \(\ell\), so their residues modulo \(\ell^e\) are also distinct. Every product is a \(d\)-th root of unity modulo \(\ell^e\). The unit group is cyclic of order \(\ell^{e-1}(\ell-1)\); it has exactly \(\gcd(d,\ell-1)\) such roots because \(\gcd(d,\ell)=1\). Counting gives the result. □

For two bases, choose \(A_i=e\log\ell/(2\log p_i)\). This yields the safe bound
\[
 e\log\ell\leq2\sqrt{\gcd(d,\ell-1)\log p_1\log p_2}.
\]
If \(\ell^{e}\) divides both \(\sigma(p_1^{a_1})\) and \(\sigma(p_2^{a_2})\), with \(a_i\leq R\) and \(\ell>R+1\), the hypothesis holds for \(d=\operatorname{lcm}(a_1+1,a_2+1)\). This controls some shared high valuations, but its two-base consequence is weak for small caps such as \(R=2\). It has not produced an entropy bound.

## 6. Two avenues worth isolating, with their missing steps

1. **Use exact residue counts together with target valuation capacities.** The lemma above gives a rigorous restriction on several small input bases sharing a large target prime power. Combine it with the actual exponent-change signs in a collision; a divisibility graph alone loses this information. The missing assertion is a quantitative saving for *whole admissible exponent vectors*, uniform over the target support. The current root-count lemma alone is only local and does not provide that assertion.

2. **Adapt factored-congruence counting to genuine exchanges.** Wang–Xu's proof and the prime-chain sieve suggest counting small arithmetic certificates with congruence constraints. An application here must preserve prime support, bounded exponents, the exact target, and track constants as the certificate size grows. A useful theorem would bound certificate choices by \(\exp(o(T(N)))\), or establish a decomposition with that total cost. No checked literature source supplies this growing-support theorem. Merely showing that individual exchanges are finite, rare on average, or large in support does not establish the required fiber count.

Neither avenue is a completed route. The verified literature and source corrections do not produce the complete self-contained proof requested by the user.
