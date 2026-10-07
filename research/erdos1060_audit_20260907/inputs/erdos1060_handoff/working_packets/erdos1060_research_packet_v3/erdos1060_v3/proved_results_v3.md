# Erdős 1060: prime-index encodings, an entropy bound, and exact finite certificates

Prepared 5 September 2026.

**Status.** This is a partial-results note, not a resolution of Erdős Problem 1060. The arguments below were developed and checked during this investigation. Their originality relative to the full mathematical literature has not been established. No independent human referee review or formal proof-assistant verification is claimed. The numerical optimizer was used for discovery, not as a premise in the entropy proof.

Let
\[
 h(k)=k\sigma(k),\qquad f(N)=\#\{k\ge1:h(k)=N\},\qquad \alpha_p=v_p(N).
\]
All logarithms are natural. The target remains
\[
 \log\max(1,f(N))=o\!\left(\frac{\log N}{\log\log N}\right).
\tag{EP}
\]
The new bound proved here is
\[
\boxed{\log\max(1,f(N))\le
 \left(\frac{\log3}{2}-\frac{\log2}{3}+o(1)\right)
 \frac{\log N}{\log\log N}.}
\tag{1}
\]
The constant is approximately \(0.3182570841474\). It improves the \(\log2/2\) bound in the previous note and the \(\log3/3\) bound in Kominers [1], but is still positive.

## 1. An injective encoding for every prime index

For a prime \(\ell\), put \(t_{\ell'}=t/\ell^{v_\ell(t)}\).

**Theorem 1.** Suppose \(h(k)=h(m)\), \(v_\ell(k)=v_\ell(m)\), and
\[
 (v_p(k)+1)_{\ell'}=(v_p(m)+1)_{\ell'}
 \qquad\text{for every prime }p\ne\ell.
\]
Then \(k=m\).

**Proof.** Cancel local factors at primes whose exponents agree. At a remaining prime \(p\), write the larger exponent as \(a\), the smaller as \(b\), and put \(t=b+1\), \(d=a-b\). The label equality implies
\[
 a+1=t\ell^j\quad(j\ge1).
\]
Consequently
\[
 \frac{h(p^a)}{h(p^b)}=p^d Q_p,
 \qquad Q_p=\frac{p^{t\ell^j}-1}{p^t-1}\in\mathbb Z.
\tag{2}
\]
Every prime factor \(q\) of \(Q_p\) is either \(\ell\) or is \(1\pmod\ell\). Indeed, \(q\ne p\). If \(p^t\equiv1\pmod q\), the geometric sum defining \(Q_p\) gives \(q\mid\ell^j\), so \(q=\ell\). Otherwise the order of \(p\) modulo \(q\) divides \(t\ell^j\) but not \(t\); its \(\ell\)-adic valuation is therefore greater than \(v_\ell(t)\). In particular, \(\ell\mid q-1\).

Let \(P_+\) be the primes with larger exponent in \(k\), and \(P_-\) those with larger exponent in \(m\). Set
\[
 A=\prod_{p\in P_+}p^{d_p},\quad B=\prod_{p\in P_-}p^{d_p},
 \quad U=\prod_{p\in P_+}Q_p,\quad V=\prod_{p\in P_-}Q_p.
\]
Then
\[
 AU=BV,\qquad \gcd(A,B)=1.
\tag{3}
\]
A differing input prime \(p\) divides the opposite product of \(Q\)'s, by (3). Since \(p\ne\ell\), it follows that every differing input prime is \(1\pmod\ell\).

For such a prime, \(\ell\mid Q_p\), and
\[
 Q_p<\frac{p^{d_p}}{1-p^{-t}}
 \le\frac{p}{p-1}p^{d_p}.
\]
Because \(p\equiv1\pmod\ell\) and \(p\ne\ell\),
\[
 (Q_p)_{\ell'}\le Q_p/\ell<p^{d_p}.
\tag{4}
\]
For clarity, \(p\ge\ell+1\) gives
\(p/[\ell(p-1)]\le(\ell+1)/\ell^2<1\).

Taking \(\ell\)-free parts of (3), and using that \(A,B\) are coprime to \(\ell\), gives
\[
 A\mid\prod_{p\in P_-}(Q_p)_{\ell'},\qquad
 B\mid\prod_{p\in P_+}(Q_p)_{\ell'}.
\]
If any exponent differs, multiplication and (4) imply
\[
 AB\le\prod_{p\in P_+\cup P_-}(Q_p)_{\ell'}
 <\prod_{p\in P_+\cup P_-}p^{d_p}=AB,
\]
a contradiction. Thus all exponents agree. \(\square\)

The case \(\ell=2\) is the previous note's exponent-label lemma. The case \(\ell=3\) supplies a different encoding, which can be combined with it.

**Corollary 2.** For every prime \(\ell\),
\[
 f(N)\le(\alpha_\ell+1)
 \prod_{\substack{p\mid N\\p\ne\ell}}
 \left(\alpha_p+1-\left\lfloor\frac{\alpha_p+1}{\ell}\right\rfloor\right).
\]
The labels arising from \(0\le e\le\alpha_p\) are exactly the positive integers at most \(\alpha_p+1\) not divisible by \(\ell\).

## 2. The local entropy inequality

For a finite random variable \(Y\), use entropy
\(H(Y)=-\sum_y\Pr(Y=y)\log\Pr(Y=y)\), with \(0\log0=0\).

Two elementary facts are used. Entropy of a vector is at most the sum of coordinate entropies. Also, for arbitrary positive weights \(w_y\),
\[
 H(Y)\le\log\sum_y w_y-\mathbb E\log w_Y.
\tag{5}
\]
The latter follows from Jensen's inequality applied to
\(\sum_y P_y\log(w_y/P_y)\); zero-probability terms are omitted.

Put
\[
 c=\tfrac12\log(3/2),\qquad \lambda=\tfrac13\log2.
\]

**Lemma 3.** If the integer-valued random variable \(J\) takes values in \(\{0,\ldots,a\}\), then
\[
\boxed{
 \frac23 H((J+1)_{2'})+\frac13 H((J+1)_{3'})
 \le ca+\lambda\mathbb EJ.}
\tag{6}
\]

**Proof.** Write the binary entropy function as
\(\eta(t)=-t\log t-(1-t)\log(1-t)\).
Its tangent at \(t=1/3\) gives
\[
 \eta(t)\le\log(3/2)+t\log2.
\tag{7}
\]
For \(a=0\), (6) is immediate. For \(a=1\), the 2-free label is constant and the 3-free label distinguishes the two exponents. Thus (7), divided by 3, proves (6), since \(\frac13\log(3/2)\le c\).

For \(a=2\), put \(p_i=\Pr(J=i)\). The 2-free label separates exponent 2 from exponents 0 and 1; the 3-free label separates exponent 1 from exponents 0 and 2. Hence the left-hand side of (6) is
\[
 \tfrac23\eta(p_2)+\tfrac13\eta(p_1)
 \le\log(3/2)+\tfrac13\log2\,(2p_2+p_1)
 =2c+\lambda\mathbb EJ.
\]
Equality holds when \(p_0=p_1=p_2=1/3\).

For \(a\ge3\), let \(t=2^{-1/3}=e^{-\lambda}\) and define
\[
 Z_\ell(a)=\sum_{\substack{1\le r\le a+1\\\ell\nmid r}}t^{r-1}.
\]
A label \(r=(J+1)_{\ell'}\) has minimum possible exponent \(r-1\). Applying (5) with weights \(t^{r-1}\) gives
\[
 H((J+1)_{\ell'})\le\log Z_\ell(a)+\lambda\mathbb EJ.
\]
It therefore suffices to prove
\[
 Z_2(a)^2Z_3(a)\le(3/2)^{3a/2}.
\tag{8}
\]
There are only three checks:

For \(a=3\), \(Z_2=1+t^2\), \(Z_3=3/2+t\).

For \(a=4,5\), \(Z_2=1+t^2+t^4\), \(Z_3=3/2+t+t^4\). The case \(a=5\) follows from \(a=4\).

For \(a\ge6\),
\[
 Z_2(a)\le\frac1{1-t^2},\qquad Z_3(a)\le\frac{1+t}{1-t^3}=2(1+t).
\]
Here are entirely rational verifications, to avoid relying on decimal approximations. Cubing proves
\[
 t<\frac{397}{500},\qquad t^2<\frac{63}{100},\qquad t^4<\frac{397}{1000}.
\]
Consequently the three required comparisons follow respectively from
\[
 \left[\left(\frac{163}{100}\right)^2\frac{1147}{500}\right]^2
 <\left(\frac32\right)^9,
\]
\[
 \left(\frac{2027}{1000}\right)^2\frac{2691}{1000}
 <\left(\frac32\right)^6,
\]
\[
 \left(\frac{100}{37}\right)^2\frac{897}{250}
 <\left(\frac32\right)^9.
\]
All three are rational integer comparisons after clearing denominators. The supplied standard-library checker also verifies them exactly. This proves (8), hence (6). \(\square\)

## 3. The uniform bound

**Theorem 4.** For every \(N\ge2\) and every real \(z\ge3\),
\[
\boxed{
 \log\max(1,f(N))
 \le\sum_{\substack{p\mid N\\p\le z}}\log(\alpha_p+1)
 +C_0\frac{\log N}{\log z},
 \quad C_0=\frac{\log3}{2}-\frac{\log2}{3}.}
\tag{9}
\]
In particular, (1) holds uniformly as \(N\to\infty\).

**Proof.** The empty fiber is harmless. Partition the preimages according to their exact exponents at primes \(p\le z\). There are at most
\(\prod_{p\mid N,p\le z}(\alpha_p+1)\) parts.

Choose \(K\) uniformly from a nonempty part \(\mathcal F\), and put \(J_p=v_p(K)\). The exponents at 2 and 3 have been fixed. By Theorem 1, each of the two large-prime label vectors
\[
 ((J_p+1)_{2'})_{p>z},\qquad ((J_p+1)_{3'})_{p>z}
\]
is individually injective on \(\mathcal F\). Thus each vector has entropy \(\log|\mathcal F|\), and entropy subadditivity gives both inequalities
\[
 \log|\mathcal F|\le\sum_{p>z}H((J_p+1)_{\ell'})
 \qquad(\ell=2,3).
\]
These concern the SAME random preimage. Average them with weights \(2/3,1/3\) and apply Lemma 3:
\[
 \log|\mathcal F|\le c\sum_{p>z}\alpha_p
                      +\lambda\sum_{p>z}\mathbb EJ_p.
\]
The target and input size constraints give
\[
 \sum_{p>z}\alpha_p\le\frac{\log N}{\log z},
 \qquad
 \sum_{p>z}\mathbb EJ_p
 \le\frac{\mathbb E\log K}{\log z}
 \le\frac{\log N}{2\log z}.
\]
The last step uses \(K^2\le K\sigma(K)=N\). Hence
\[
 \log|\mathcal F|\le(c+\lambda/2)\frac{\log N}{\log z}
 =C_0\frac{\log N}{\log z}.
\]
Multiplying the maximal part size by the number of parts proves (9).

For the asymptotic assertion set \(L=\log N\), \(u=\log L\), and \(z=L/u^3\), which is at least 3 for sufficiently large \(N\). Since every \(\alpha_p\le L/\log2\), the small-prime sum is at most \(O(z\log L)=O(L/u^2)\). Also \(\log z=u-3\log u\sim u\). This proves (1). No prime number theorem is needed in this argument. \(\square\)

## 4. A barrier for this particular relaxation

The improved constant must not be confused with a route that already reaches zero.

Take the single-coordinate cap \(a=2\), with \(J\) uniform on \(\{0,1,2\}\). Then
\[
 \mathbb EJ=1=a/2,
\]
and both the 2-free and 3-free label entropies equal
\[
 \eta(1/3)=\log3-\tfrac23\log2=2C_0.
\]
For every prime \(\ell\ge5\), the \(\ell\)-free labels distinguish all three exponents, and their entropy is \(\log3\), which is larger.

Therefore a method that uses only these coordinatewise prime-index label entropy bounds, convex combinations of them, and the two aggregate budgets
\(\sum\alpha_p\le L/\log z\) and \(\sum\mathbb EJ_p\le L/(2\log z)\)
cannot have constant below \(C_0\). The uniform three-point law is feasible for that relaxation and saturates the proved inequality.

This is NOT a lower bound for \(f\), and does not assert that such marginals occur in a large arithmetic fiber. It identifies the information missing from the relaxation: correlations forced by the exact prime-valuation equations. Optimizing more weights in the same relaxation cannot prove (EP).

## 5. Exact difference-column certificates

For an allowed input prime \(p\) and two admissible exponents \(a>b\), form
\[
 c_{p,a,b}=\nu(h(p^a))-\nu(h(p^b)),
\]
where \(\nu\) records every prime valuation appearing in the local factors.

A nontrivial collision, after canceling equal-exponent local blocks, selects at most one such column per input prime, with coefficient \(+1\) or \(-1\), and has column sum zero. Conversely such a selection gives a collision.

**Lemma 5: exact peeling.** If a valuation row is nonzero only in columns belonging to one input prime \(p\), no valid collision can use a column nonzero in that row. Delete those columns and repeat. These deletions preserve all possible collisions.

**Proof.** The selected column at \(p\) would be the sole nonzero contributor to that row. Its sign cannot make its nonzero entry vanish. At most one column can be selected at \(p\). Apply this argument inductively through the deletions. \(\square\)

If all columns are deleted, there is no collision. If the remaining columns are linearly independent over \(\mathbb Q\), there is likewise no collision.

A target-specific reconstruction version is also useful. For a target \(M\), let
\[
 \mathcal E_p=\{0\le e\le\min(E,v_p(M)):h(p^e)\mid M\},
\]
with disallowed input primes forced to exponent zero. Choose input primes \(S\), discard their difference columns, and apply peeling. If all remaining columns disappear, or the residual columns are linearly independent, then fixing the exponents on \(S\) permits at most one preimage. Hence
\[
 \#\{\text{allowed preimages of }M\}\le\prod_{p\in S}|\mathcal E_p|.
\tag{10}
\]
Every target-prime row must be retained, including primes too small to be allowed in the input.

The required cheap set \(S\) is NOT proved to exist. Potential columns from incompatible choices can make this certificate more demanding than the actual fiber. Failure to find such a certificate does not disprove the conjecture.

## 6. Experiments actually completed in this pass

These are PRIME-FACTOR bounds, not consecutive-input bounds. They cover inputs vastly larger than the numerical prime cutoff.

**A. Same-radical odd cubefree inputs, prime factors at most 100,000.** A collision between two such inputs can differ only by exponents 1 versus 2. All 9,591 difference columns disappear under exact peeling. Thus no nontrivial collision exists in this finite-prime class.

**B. Odd inputs with every exponent in \(\{0,2,4\}\), prime factors at most 10,000.** There are 3,684 initial columns. Exact peeling leaves only
\[
 c_{3,4,0},\quad c_{7,2,0},\quad c_{11,2,0}.
\]
Their rows at primes \(3,7,11\) form the matrix
\[
 \begin{pmatrix}4&1&0\\0&2&1\\2&0&2\end{pmatrix},
 \qquad\det=18\ne0.
\]
Therefore no nontrivial collision exists in this class.

**C. Odd inputs with every exponent in \(\{0,2,4,6\}\), prime factors at most 1,000.** The 1,002 initial columns reduce to the same three columns and determinant certificate. Again there is no collision in this class.

All factorizations used in A–C were checked by exact multiplication, and all prime factors were certified using recursive Lucas primality certificates. The packet includes 18,000-plus such certificates, including factors larger than \(10^{15}\). `check_certificates.py` independently repeats the factorization checks, primality-certificate checks, peeling, determinant computation, and rational entropy inequalities using only the Python standard library. It has been run successfully. This is a reproducible computational certificate, not formal proof-assistant verification.

**D. Positive control.** The numerical search with allowed exponents \(0,1,2\), input primes from 11 through 10,000, rediscovered the previous 29-digit collision:
\[
 a=60629697601617236747379985403,
 \quad b=61655391632564660609643619057,
\]
\[
 h(a)=h(b)=5276516179938729922490847708056660616574496169354744299520.
\]
The exact products were checked, and the separate complete-divisor-summation verifier from the previous packet was rerun. No minimality is inferred from the optimizer's status.

**E. Inconclusive rough search.** With exponents \(0,1,2\), input primes from 101 through 100,000, exact peeling reduced 28,701 columns to 537. A 25-second numerical mixed-integer search ended without a feasible incumbent. This proves neither existence nor nonexistence of collisions in that class.

None of A–C proves an unbounded-prime injectivity theorem. D remains a counterexample to odd-cubefree injectivity and to the former small-range classification heuristic.

## 7. The remaining asymptotic bottleneck

Retain the previous reduction. For fixed \(E\ge1\), \(\delta>0\), define
\[
 R_{E,\delta}(X)=\max_{M\le X}\#\{u:h(u)=M,\ v_p(u)\le E,
                                      \ P^-(u)>\delta\log X\}.
\]
It suffices to prove, for every fixed \(E,\delta\),
\[
 \log R_{E,\delta}(X)=o_{E,\delta}(\log X/\log\log X).
\tag{R}
\]
This remains unproved here. In particular, a sufficient new task is to show that the rough, bounded-exponent target models admit certificates (10) of logarithmic cost
\[
 \sum_{p\in S}\log|\mathcal E_p|=o_{E,\delta}(\log X/\log\log X),
\]
or to replace them by a rigorously cheaper adaptive reconstruction scheme. The existence of these cheap certificates is not a supplied lemma.

The reduction uses
\[
 f(N)\le G_E(N)(E+1)^{\pi(\delta\log N)}R_{E,\delta}(N),
\quad G_E(N)=\prod_{p\mid N}(1+\max(\alpha_p-E,0)),
\]
and
\[
 \log G_E(N)\le(c_E+o_E(1))\frac{\log N}{\log\log N},
 \quad c_E=\sup_{a\ge E+1}\frac{\log(a-E+1)}a\longrightarrow0.
\]
First choose \(E\), then \(\delta\), then the asymptotic threshold for \(N\). Proving only a single fixed exponent bound does not establish (EP).

## 8. Literature checked and how it changes the strategy

[1] Scott Duke Kominers, *On the Number of Solutions of kσ(k)=n*. Theorem 1.2 and Corollary 1.3 supply the \(\prod v_p(N)\) and \(\log3/3\) bounds. Remark 4.3 discusses the limitations of squarefree-based exponent coloring.
https://scottkom.com/assets/articles/Kominers_ksigmak.pdf

[2] Passawan Noppakaew and Prapanpong Pongsriiam, *Product of Some Polynomials and Arithmetic Functions*, Journal of Integer Sequences 26 (2023), Article 23.9.1. Theorem 12 supplies squarefree injectivity in greater generality; Theorem 6 contains a related cross-divisibility/size argument for a different arithmetic function. Neither is being cited as the statement of Theorem 1 of this note.
https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf

[3] Sean Bibby, Pieter Vyncke, Joshua Zelinsky, *On the Third Largest Prime Divisor of an Odd Perfect Number*, arXiv:1908.09420. The σ-pair sections and quadratic mutual-divisibility descent are relevant to short dependence cycles. A theorem about two-cycles is not a theorem controlling all collision graphs.
https://arxiv.org/abs/1908.09420

[4] Paul Pollack, Carl Pomerance, Lola Thompson, *Divisor-sum fibers*, Theorem 1.4. For the DIFFERENT function \(s(n)=\sigma(n)-n\), there are infinitely many targets with \(\exp(c\log m/\log\log m)\) preimages in an arbitrarily prescribed fixed-relative-width interval; their proof permits \(c=1/7\). This is a warning against treating interval concentration as a counting theorem. It is not a counterexample for \(h\), nor a theorem about shrinking intervals of the exact width in (R).
https://math.dartmouth.edu/~carlp/divisor-sum-fibers-5.3.pdf

[5] Paul Pollack and Carl Pomerance, *Some problems of Erdős on the sum-of-divisors function*. Common unitary factors and primitive friendly pairs remain useful parallels. Fixed-abundancy bounds do not directly bound a fiber of \(h\), because \(\sigma(k)/k=N/k^2\) varies across that fiber.
https://math.dartmouth.edu/~carlp/btran10.pdf

Direct retrieval of the current Erdős problem page failed in this pass. Accordingly, this note does not infer the current status of every public proof claim from that page. No claim that the above partial improvement is unprecedented is made.
