# Erdős 1060: proved additions and exact counterexamples

Prepared 5 September 2026. This is a partial-results note, not a resolution of Erdős Problem 1060. The arguments below were developed and checked in this investigation. Their originality relative to the entire literature has not been established. No formal proof-assistant verification or independent human referee review is claimed.

Write
\[
h(k)=k\sigma(k),\qquad f(N)=\#\{k\ge1:h(k)=N\},\qquad \alpha_p=v_p(N).
\]
For a positive integer \(t\), let \(\operatorname{odd}(t)=t/2^{v_2(t)}\).

## 1. An exponent-coloring injection

**Theorem 1.** Suppose \(h(k)=h(m)\), \(v_2(k)=v_2(m)\), and
\[
\operatorname{odd}(v_p(k)+1)=\operatorname{odd}(v_p(m)+1)
\quad\text{for every odd prime }p.
\]
Then \(k=m\).

**Proof.** At primes where the exponents agree, cancel the equal local factors in the product formula for \(h\). All remaining primes are odd. At any such prime, let the larger exponent be \(a\), the smaller \(b\), and set \(d=a-b>0\), \(t=b+1\). The hypothesis gives \(a+1=2^j(b+1)\) for an integer \(j\ge1\). Thus
\[
\frac{h(p^a)}{h(p^b)}=p^d Q_p,
\qquad
Q_p=\frac{p^{a+1}-1}{p^{b+1}-1}
=\sum_{i=0}^{2^j-1}p^{it}.
\]
The integer \(Q_p\) is even. Moreover,
\[
Q_p<\frac{p^d}{1-p^{-t}}\le\frac32p^d,
\qquad
\operatorname{odd}(Q_p)\le\frac{Q_p}{2}<p^d.
\tag{1}
\]
Let \(P_+\) be the primes where the exponent in \(k\) is greater and \(P_-\) those where it is smaller. Put
\[
A=\prod_{p\in P_+}p^{|v_p(k)-v_p(m)|},\qquad
B=\prod_{p\in P_-}p^{|v_p(k)-v_p(m)|}.
\]
Then \(\gcd(A,B)=1\). Taking odd parts in the equality of the two products of local ratios gives
\[
A\prod_{p\in P_+}\operatorname{odd}(Q_p)
=B\prod_{p\in P_-}\operatorname{odd}(Q_p).
\]
Consequently,
\[
A\mid\prod_{p\in P_-}\operatorname{odd}(Q_p),\qquad
B\mid\prod_{p\in P_+}\operatorname{odd}(Q_p).
\]
If any prime differs, multiplying these divisibilities and applying (1) gives
\[
AB\le\prod_{p\in P_+\cup P_-}\operatorname{odd}(Q_p)
<\prod_{p\in P_+\cup P_-}p^{|v_p(k)-v_p(m)|}=AB,
\]
a contradiction. Therefore all exponents agree. \(\square\)

**Corollary 2.** For every positive integer \(N\),
\[
\boxed{f(N)\le(\alpha_2+1)
\prod_{\substack{p\mid N\\p\text{ odd}}}
\left(\left\lfloor\frac{\alpha_p}{2}\right\rfloor+1\right).}
\tag{2}
\]
Here \(\alpha_2=0\) when \(N\) is odd.

**Proof.** Every preimage divides \(N\). At an odd prime, the possible colors \(\operatorname{odd}(e+1)\), for \(0\le e\le\alpha_p\), are exactly the odd positive integers at most \(\alpha_p+1\). There are \(\lfloor\alpha_p/2\rfloor+1\) of them. Record the exponent at 2 exactly. Theorem 1 makes this encoding injective within a fiber. \(\square\)

**Corollary 3.** Uniformly for positive integer targets tending to infinity,
\[
\boxed{\log\max(1,f(N))\le
\left(\frac{\log2}{2}+o(1)\right)
\frac{\log N}{\log\log N}.}
\tag{3}
\]

**Proof.** For every positive integer \(a\),
\[
\log(\lfloor a/2\rfloor+1)\le \frac{a\log2}{2}.
\]
For \(a=2r\), this is \(r+1\le2^r\); for \(a=2r+1\), the even case implies it when \(r\ge1\), and \(a=1\) is immediate. Let \(L=\log N\), \(\ell=\log L\), and \(z=L/\ell^3\). The primes at most \(z\) in (2) contribute at most \(O(z\ell)=O(L/\ell^2)\). For the primes exceeding \(z\), the logarithm of the product is at most
\[
\frac{\log2}{2}\sum_{p>z}\alpha_p
\le\frac{\log2}{2}\frac{L}{\log z}
=\left(\frac{\log2}{2}+o(1)\right)\frac{L}{\ell}.
\]
The factor \(\alpha_2+1\) contributes \(O(\ell)\). This proves (3). \(\square\)

The constant in (3) improves on the \(\log3/3\) obtained from the majorant \(\prod_{p\mid N}\alpha_p\) in Kominers [1]. It still does not prove the conjecture: the constant is positive. The new majorant itself has constant \(\log2/2\) along \(N_y=\prod_{3\le p\le y}p^2\), by the prime number theorem. Optimizing this majorant alone cannot give a zero constant. This statement does not assert a matching lower bound for \(f\).

## 2. An odd cubefree collision with no small input prime

Define
\[
\begin{aligned}
a&=11^2\,13^2\,17\,19\,31\,61\,97\,127^2\,271\,307^2\,331\,367,\\
b&=13\,17^2\,19^2\,23\,31^2\,43\,61^2\,83\,127\,307\,733\,5419.
\end{aligned}
\]
Their decimal values are
\[
a=60629697601617236747379985403,\qquad
b=61655391632564660609643619057.
\]
Exact arithmetic gives
\[
\boxed{h(a)=h(b)=M}
\]
with
\[
M=5276516179938729922490847708056660616574496169354744299520.
\]
All displayed prime bases were checked by trial division. Both inputs are odd and cubefree, all their prime factors are at least 11, and there is no prime having the same positive exponent in both inputs. Thus no common nontrivial unitary prime-power block can be canceled.

Since \(\gcd(ab,42)=1\) and \(h(12)=h(14)=336\), the four integers
\[
12a,\quad14a,\quad12b,\quad14b
\]
are distinct cubefree preimages of \(336M\). This disproves cubefree multiplicity bounds of 2 or 3, odd-cubefree injectivity, and a classification restricting cubefree collisions to coprime scalings of \((12,14)\). It does not disprove a larger absolute cubefree multiplicity bound, let alone the main conjecture.

**Exact checks performed.** A mixed-integer search proposed the witness. The integer products were then checked exactly. Independently, `verify_witnesses.py` constructs and sums every divisor of each input, without using the geometric-sum formula for \(\sigma\). Each of \(a,b\) has 20,736 divisors. The four scaled inputs were checked in the same way.

The exhaustive valuation-based inverse search in `exact_target_search.py` gives
\[
f_2(M)=2,\quad f_2(336M)=4,
\qquad f(M)=2,\quad f(336M)=6.
\]
Here \(f_2\) restricts the inputs to cubefree integers. The full searches used exponent bound 24, at least every exponent in both target factorizations. The two extra preimages of \(336M\) are not cubefree. All six listed witnesses were independently checked by divisor summation. These are not minimality or record claims.

**Why the exhaustive search is complete.** A preimage uses only primes dividing its target. For each such prime, the search considers every exponent up to the requested bound and \(v_p(N)\), retaining only local blocks \(h(p^e)\) dividing \(N\). An exact residual valuation vector tracks the product. A branch is rejected only when a selected block exceeds a remaining valuation, or when even the sum of the maximum possible contributions of all remaining variables cannot supply a required valuation. At the leaf, every residual valuation must be zero. Each exponent vector is visited once. Consequently, all and only the requested preimages are enumerated.

## 3. Injectivity on squares of squarefree integers

**Theorem 4.** If \(r,s\) are squarefree and \(h(r^2)=h(s^2)\), then \(r=s\).

**Proof.** Cancel the common square prime-power blocks. We may assume \(\gcd(r,s)=1\). Write \(\Phi(p)=p^2+p+1\).

A prime \(q\equiv2\pmod3\) cannot divide \(\Phi(p)\) for any prime \(p\): otherwise \(p\not\equiv0,1\pmod q\), and the order of \(p\) modulo \(q\) would be 3, contradicting \(3\nmid q-1\). The case \(q=2\) is immediate since \(\Phi(p)\) is odd. Such a \(q\) therefore cannot occur in either remaining input. Every remaining input prime other than 3 is \(1\pmod3\), hence at least 7. For each of these primes, \(v_3(\Phi(p))=1\).

First suppose that 3 occurs in neither input. Set \(A=r^2\), \(B=s^2\),
\[
U=\prod_{p\mid r}\frac{\Phi(p)}3,\qquad
V=\prod_{q\mid s}\frac{\Phi(q)}3.
\]
The 3-adic valuation of the equality forces \(\omega(r)=\omega(s)\), so canceling the common power of 3 yields \(AU=BV\). Since \(\gcd(A,B)=1\), we have \(A\mid V\), \(B\mid U\). Every nonempty product defining \(U\) is strictly smaller than \(A\), and similarly \(V<B\). Unless both inputs are 1, multiplication gives a contradiction.

Now suppose 3 occurs in the first input. Write the two inputs as \(9A\) and \(B\), where \(A,B\) are coprime squares of squarefree integers with prime factors \(1\pmod3\). Put \(r_0=\omega(A)\), \(s_0=\omega(B)\), and define \(U,V\) as above over their respective prime supports. Equality of 3-adic valuations gives \(s_0=r_0+2\). Since \(\sigma(9)=13\), cancellation gives
\[
13AU=BV.
\]
Therefore \(A\mid V\), \(B\mid13U\), and \(AB\le13UV\). For every prime \(p\ge7\),
\[
\frac{\Phi(p)}{3p^2}\le\frac{19}{49}.
\]
If \(r_0\ge1\), then \(r_0+s_0\ge4\), and
\[
1\le\frac{13UV}{AB}\le13\left(\frac{19}{49}\right)^4<1,
\]
a contradiction. If \(r_0=0\), then \(B\mid13\), impossible since \(B\) is a nontrivial square. This completes the proof. \(\square\)

In particular, \(f_2(N)\le1\) for odd targets \(N\). Indeed an odd target forces an odd input, and \(\sigma(p^e)\) is odd for odd \(p\) exactly when \(e\) is even. Under \(e\le2\), every positive input exponent is 2. This must not be confused with injectivity on odd cubefree *inputs*, which Section 2 disproves.

## 4. A precise graph reconstruction lemma

Fix \(N\) and an exponent bound \(E\). Define
\[
\mathcal E_p=\{0\le e\le\min(E,\alpha_p):h(p^e)\mid N\}.
\]
Use as vertices the primes for which some positive exponent is admissible. Draw \(p\to q\), for distinct vertices, whenever \(q\mid\sigma(p^e)\) for some \(e\in\mathcal E_p\). Include all target-prime valuation equations, even for primes that are not input vertices.

**Lemma 5.** If removing a vertex set \(S\) makes this directed graph acyclic, then
\[
f_E(N)\le\prod_{p\in S}|\mathcal E_p|.
\]

**Proof.** Fix the exponents at vertices in \(S\). In a topological ordering of the remaining graph, each successive exponent is forced by
\[
e_q=\alpha_q-\sum_{p\ne q}v_q(\sigma(p^{e_p})).
\]
Every nonzero summand comes from a vertex already processed or from \(S\). There is no self-contribution from \(\sigma(q^{e_q})\), which is \(1\pmod q\). Reject inadmissible forced values and inconsistencies in other target-prime rows. Hence each assignment on \(S\) produces at most one solution. \(\square\)

A sufficient missing estimate is a set \(S\) whose cost \(\sum_{p\in S}\log|\mathcal E_p|\) is little-o of the required scale. Existence of such a set is **not proved**. The union graph includes edges from mutually incompatible exponent choices and can overestimate the actual difficulty. Failure of this sufficient estimate would not disprove Erdős 1060.

## 5. A sharper rough-input formulation

Let \(L=\log X\). Fix \(E\ge1\) and \(\delta>0\), set \(y=\delta L\), and define
\[
R_{E,\delta}(X)=\max_{1\le M\le X}
\#\{u:h(u)=M,\ v_p(u)\le E,\ P^-(u)>\delta\log X\},
\]
where \(P^-(1)=\infty\). Fixing the exponents at primes \(p\le y\) costs at most \((E+1)^{\pi(y)}\). Together with the high-exponent decomposition from the previous prompt, this gives
\[
f(N)\le G_E(N)(E+1)^{\pi(\delta\log N)}R_{E,\delta}(N),
\]
where
\[
G_E(N)=\prod_{p\mid N}\bigl(1+\max(\alpha_p-E,0)\bigr),
\quad
\log G_E(N)\le(c_E+o_E(1))\frac{\log N}{\log\log N},
\]
\[
c_E=\sup_{a\ge E+1}\frac{\log(a-E+1)}a\longrightarrow0.
\]
By the prime number theorem, the small-prime cost has constant \(\delta\log(E+1)\). Thus it suffices to prove
\[
\log R_{E,\delta}(X)=o_{E,\delta}(\log X/\log\log X)
\]
for every fixed \(E,\delta\). First choose \(E\), then choose \(\delta\), then take \(N\) sufficiently large. This is a reformulation of the missing difficult step, not its proof.

The rough inputs also lie in a short interval. If \(h(u)=M\le X\), \(P^-(u)>y>1\), then \(u\le\sqrt X\), and
\[
\log\frac{\sigma(u)}u
\le\frac{\omega(u)}{y-1}
\le\frac{\log X}{2(y-1)\log y}.
\]
Consequently,
\[
\sqrt M\exp\!\left(-\frac{\log X}{4(y-1)\log y}\right)
\le u\le\sqrt M.
\]
For \(y=\delta\log X\), the relative interval width is \(O_\delta(1/\log\log X)\). Interval concentration alone does not establish a uniform multiplicity bound.

## Source notes

[1] Scott Duke Kominers, *On the Number of Solutions of kσ(k)=n*. Theorem 1.2, Proposition 3.2, Remarks 4.1–4.3.
`https://scottkom.com/assets/articles/Kominers_ksigmak.pdf`

[2] Passawan Noppakaew and Prapanpong Pongsriiam, *Product of Some Polynomials and Arithmetic Functions*, Journal of Integer Sequences 26 (2023), Article 23.9.1. Theorems 6 and 12 are relevant: cross-divisibility plus strict size comparison for a related arithmetic function, and squarefree injectivity, respectively. Neither is being cited as the statement of Theorem 1 above.
`https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf`

[3] Sean Bibby, Pieter Vyncke, Joshua Zelinsky, *On the Third Largest Prime Divisor of an Odd Perfect Number*, arXiv:1908.09420v3. The discussion of σ_{m,n} pairs and Lemmas 4–8 is directly relevant to dependence cycles. Lemma 5 uses a descent for mutual divisibility by quadratic cyclotomic values. Its scope is not a general count of all collision graphs.
`https://arxiv.org/abs/1908.09420`

[4] Paul Pollack and Carl Pomerance, *Some problems of Erdős on the sum-of-divisors function* (2016). Common unitary divisors and primitive friendly pairs are useful structural parallels. Fixed-abundancy or average collision results do not automatically bound a fiber of h.
`https://math.dartmouth.edu/~carlp/btran10.pdf`
