# Order descent and cyclotomic parity for $k\sigma(k)=n$: two barriers, and Erdős Problem 1060 settled in the extremal regime

**Status of this note.** Erdős Problem 1060 is **not solved here**, and I do not believe it is close. What follows is (i) a strict improvement of the current record constant, (ii) a new structural lemma — the first use of multiplicative-order / primitive-prime-divisor information in this problem that I am aware of, (iii) a **barrier theorem** showing that the method underlying every bound known to me, including my own Theorem 2, provably cannot answer Erdős's question, (iv) exact counterexamples closing the one other elementary route, and (v) the sharpest reformulation that survives both barriers, in terms of a *roughness function* $\rho$, together with six exact certificates suggesting that this route too returns only the bound already known. Finally §7 is **positive**: combining parity of exponents with a cyclotomic congruence obstruction proves that the extremal $n$ for every majorant above has *no preimages at all*, and settles Erdős's first question for all $n$ with $v_p(n)\le3$ and $P^+(n)\le\exp((\log n)^{1/2-\varepsilon})$.

Throughout, $\sigma$ is the sum-of-divisors function,
$$h(k)=k\sigma(k),\qquad f(n)=\#\{k\ge1: h(k)=n\},$$
$v_p$ is the $p$-adic valuation, $L=\log n$, $L_2=\log\log n$, $P^+(m)$ is the largest prime factor of $m$, and $\operatorname{ord}_Q(q)$ is the multiplicative order of $q$ modulo $Q$. $h$ is multiplicative on coprime arguments: $h(ab)=h(a)h(b)$ when $\gcd(a,b)=1$.

**Prior art.** Since $k\mid h(k)$, every preimage of $n$ divides $n$, so $f(n)\le\tau(n)$ and Wigert gives $f(n)\le n^{(\log 2+o(1))/L_2}$. Noppakaew–Pongsriiam [NP23, Thm. 12] proved $h$ is injective on squarefree integers; Kominers [Kom26] combined this with a colouring of exponent patterns to obtain
$$f(n)\le\prod_{p\mid n}v_p(n),\qquad\text{hence}\qquad f(n)\le n^{(\log 3/3+o(1))/L_2},$$
with $\log 3/3=0.36620409\ldots$, and showed (as Knopfmacher had already proved for the majorant $\prod_p v_p(n)$, which is A005361, the number of squarefull divisors) that $\log3/3$ is *sharp for that majorant*. Erdős asks whether $f(n)\le n^{o(1/L_2)}$, perhaps even $f(n)\le(\log n)^{O(1)}$.

---

## 1. The Order-Descent Lemma

Kominers [Kom26, Rem. 4.3] identifies the barrier precisely: the $\{0,1\}$-merging colouring is exactly what squarefree injectivity licenses, and progress requires "new control of disagreements involving at least one exponent outside $\{0,1\}$". The following lemma supplies exactly such control. It is elementary, but it uses the multiplicative order of one prime modulo another, which — to the best of my knowledge, and confirmed by a literature sweep — has not previously been applied to this problem.

> **Lemma 1 (Order Descent).** Let $k\ne k'$ satisfy $h(k)=h(k')=n$. Let $Q$ be the largest prime with $v_Q(k)\ne v_Q(k')$, and suppose $v_Q(k)>v_Q(k')$. Then there is a prime $q<Q$ with $q\mid k'$ such that, writing $e=v_q(k')$ and $t=\operatorname{ord}_Q(q)$,
> $$t\ge2\quad\text{and}\quad t\mid e+1 .$$
> Moreover $t=2$ forces $(q,Q)=(2,3)$. Consequently, **if $Q\ge5$ then**
> $$t\ge3,\qquad e\ge t-1\ge2,\qquad q^{t}>Q,\qquad q^{e}> Q^{(t-1)/t}\ge Q^{2/3},$$
> and $Q$ divides the cyclotomic value $\Phi_t(q)$.

*Proof.* Put $\beta=v_Q(k)>\gamma=v_Q(k')$. Since $h(m)=m\sigma(m)$,
$$v_Q(n)=\beta+v_Q(\sigma(k))=\gamma+v_Q(\sigma(k')),$$
so $v_Q(\sigma(k'))-v_Q(\sigma(k))=\beta-\gamma\ge1$.

Write $\sigma(m)=\prod_{p\mid m}\sigma(p^{v_p(m)})$. The prime $Q$ itself contributes nothing, since $\sigma(Q^{a})\equiv1\pmod Q$. Every prime $p>Q$ satisfies $v_p(k)=v_p(k')$ by maximality of $Q$, so such $p$ contribute *equally* to $v_Q(\sigma(k))$ and to $v_Q(\sigma(k'))$ and cancel in the difference. Hence
$$\sum_{p<Q}\Big[v_Q\big(\sigma(p^{v_p(k')})\big)-v_Q\big(\sigma(p^{v_p(k)})\big)\Big]\ \ge\ 1,$$
so some prime $q<Q$ has $v_Q(\sigma(q^{e}))\ge1$ where $e=v_q(k')\ge1$ (as $\sigma(q^0)=1$); in particular $q\mid k'$.

From $Q\mid\sigma(q^{e})$ and $(q-1)\sigma(q^{e})=q^{e+1}-1$ we get $Q\mid q^{e+1}-1$, so $t=\operatorname{ord}_Q(q)$ divides $e+1$.

If $t=1$ then $q\equiv1\pmod Q$; as $1\le q<Q$ this forces $q=1$, absurd. So $t\ge2$.

If $t=2$ then $Q\mid q^2-1=(q-1)(q+1)$ and $Q\nmid q-1$, so $Q\mid q+1$; since $0<q+1\le Q$ we get $q+1=Q$. Two primes differing by $1$ must be $2,3$, so $(q,Q)=(2,3)$.

Hence $Q\ge5$ gives $t\ge3$, so $e+1\ge t$, i.e. $e\ge t-1\ge2$. Also $q^{t}\equiv1\pmod Q$ with $q^t>1$ forces $q^t\ge Q+1>Q$, whence $q>Q^{1/t}$ and $q^{e}\ge q^{t-1}>Q^{(t-1)/t}\ge Q^{2/3}$. Finally, $Q\mid q^t-1=\prod_{d\mid t}\Phi_d(q)$, so $Q\mid\Phi_d(q)$ for some $d\mid t$; then $q^{d}\equiv1\pmod Q$, so $t\mid d$ and hence $d=t$. Thus $Q\mid\Phi_t(q)$. $\blacksquare$

### 1.1 Consequences

> **Corollary 1.1 (squarefree injectivity, reproved).** If $a\ne b$ are squarefree then $h(a)\ne h(b)$.

*Proof.* Suppose $h(a)=h(b)$, $a\ne b$, both squarefree. Let $Q$ be the largest prime where they differ, say $v_Q(a)=1>0=v_Q(b)$. Lemma 1 gives a prime $q<Q$ dividing $b$ with $\operatorname{ord}_Q(q)\mid v_q(b)+1=2$, so $t=2$ and $(q,Q)=(2,3)$; thus $Q=3$. Since $Q$ was the *largest* prime at which $a,b$ differ, they agree at every prime $\ge5$; writing $m=\prod_{p\ge5}p^{v_p(a)}=\prod_{p\ge5}p^{v_p(b)}$ we get $a=a_6m$, $b=b_6m$ with $\gcd(m,6)=1$ and $a_6,b_6\in\{1,2,3,6\}$ (both squarefree). Multiplicativity gives $h(a_6)h(m)=h(b_6)h(m)$, so $h(a_6)=h(b_6)$; and $h(1)=1$, $h(2)=6$, $h(3)=12$, $h(6)=72$ are pairwise distinct, so $a_6=b_6$ and $a=b$. $\blacksquare$

This recovers [NP23, Thm. 12] / [Kom26, Thm. 1.1] — hence also Kominers's $\prod_p v_p(n)$ bound — but Lemma 1 says considerably more: it constrains disagreements at *all* exponents, not just at squarefree ones.

> **Corollary 1.2 (forced powerful part).** If $k\ne k'$ lie in the same fiber and their largest disagreement prime $Q$ satisfies $Q\ge5$, then the one of $k,k'$ with the *smaller* $v_Q$ is divisible by $q^2$ for some prime $q<Q$ with $q^{t}>Q$, where $t=\operatorname{ord}_Q(q)\ge3$; consequently $q^{v_q}>Q^{(t-1)/t}\ge Q^{2/3}$, so its squarefull (powerful) part exceeds $Q^{2/3}$.
>
> *(Note the exponent is $t$, not $3$: one cannot conclude $q^3>Q$. E.g. for the reduced collision $(48,62)=(2^4\cdot3,\,2\cdot31)$ one has $Q=31$, $q=2$, $e=4$, $t=\operatorname{ord}_{31}(2)=5$, and $q^3=8<31<32=q^t$.)*

> **Corollary 1.2$'$.** Since the witness $q$ satisfies $2\le q<Q$, always $Q\ge3$: two distinct preimages of the same $n$ can never disagree only at the prime $2$.

> **Corollary 1.3.** If a fiber $h^{-1}(n)$ contains a squarefree element $k'$, then for every other $k$ in the fiber, the largest prime $Q$ where $k$ and $k'$ disagree satisfies either $Q\le3$ or $v_Q(k')>v_Q(k)$ (i.e. $v_Q(k')=1$, $v_Q(k)=0$).

**Numerical check.** Lemma 1 and Corollaries 1.2–1.3 were verified against all $146$ reduced collisions with both entries $\le10^9$ (see §4): no failures. The observed distribution of $t=\operatorname{ord}_Q(q)$ is
$$t=3\ (48),\;4\ (8),\;5\ (18),\;7\ (18),\;8\ (6),\;9\ (8),\;11\ (6),\;12\ (1),\;13\ (13),\;14\ (3),\;15\ (3),\;17\ (9),\;19\ (5).$$
In particular $t=2$ never occurs, consistent with Corollary 1.2$'$; indeed the smallest top-disagreement prime observed is $Q=7$.

---

## 2. A strict improvement of the record constant

Kominers's bound $f(n)\le\prod_{p\mid n}v_p(n)$ discards a completely elementary piece of information: **every preimage satisfies $k<\sqrt n$**, because $\sigma(k)>k$ for $k>1$. Feeding this back into the colouring gives a strictly better constant.

Recall the colouring of [Kom26, Thm. 1.2]: for $k$ in the fiber set $c_p(k)=*$ if $v_p(k)\in\{0,1\}$, and $c_p(k)=v_p(k)$ if $v_p(k)\ge2$. It is injective on $h^{-1}(n)$, by a three-line argument we include for completeness: if $c(k)=c(k')$ then for every $p$ either $v_p(k)=v_p(k')$ or $\{v_p(k),v_p(k')\}=\{0,1\}$. Put $d=\prod_{p:\,v_p(k)=v_p(k')>0}p^{v_p(k)}$, $a=k/d$, $b=k'/d$. Any $p\mid a$ has $v_p(k)\ne v_p(k')$, hence $v_p(k)=1$; so $a$, and likewise $b$, is squarefree, and $\gcd(d,ab)=1$. Multiplicativity gives $h(d)h(a)=h(k)=h(k')=h(d)h(b)$, so $h(a)=h(b)$, so $a=b$ by Corollary 1.1, so $k=k'$. Since $\log k\ge\sum_{p:\,c_p\ge2}c_p\log p$ and $\log k<\tfrac12\log n$, every colour vector arising from the fiber lies in
$$\mathcal C(n)=\Big\{(c_p)_{p\mid n}\ :\ c_p\in\{*\}\cup\{2,\dots,v_p(n)\},\ \ \sum_{p:\,c_p\ne*}c_p\log p\le\tfrac12\log n\Big\}.$$

> **Theorem 2.** For every $n\ge2$ and every $\mu>0$,
> $$f(n)\ \le\ \#\mathcal C(n)\ \le\ n^{\mu/2}\prod_{p\mid n}\Big(1+\sum_{j=2}^{v_p(n)}p^{-\mu j}\Big).$$
> Consequently, as $n\to\infty$,
> $$\boxed{\ f(n)\ \le\ \exp\Big(\big(c_0+o(1)\big)\frac{\log n}{\log\log n}\Big),\qquad c_0=\tfrac13\log\!\big(1+r^2+r^3\big)-\tfrac12\log r=0.3632703226\ldots\ }$$
> where $r=0.9003299240\ldots$ is the unique root in $(0,1)$ of $3r^3+r^2-3=0$. Moreover $c_0$ is **sharp** for the majorant $\#\mathcal C(n)$, the extremal shape again being $n_y=\prod_{p\le y}p^3$.

Since $c_0=0.36327032\ldots<0.36620410\ldots=\log3/3$, this strictly improves the record. (The gain is small — about $0.8\%$ — and of course still infinitely far from $o(1)$. It should also be said that the $o(1)$ here decays only like $1/\log\log n$: at the extremal shape with $y=10^6$, i.e. $\log n\approx3\cdot10^6$, the true exponent is still about $1.17\,c_0\log n/\log\log n$. The improvement is therefore of theoretical interest only — it is far smaller than the error term at any $n$ one could write down.)

Note that $\#\mathcal C(n)\le\prod_{p\mid n}v_p(n)$ *pointwise and trivially*, since $\mathcal C(n)$ is a subset of the set of all colour vectors, of which there are exactly $\prod_p v_p(n)$ (the colours at $p$ being $*,2,3,\dots,v_p(n)$). So Theorem 2 refines [Kom26, Thm. 1.2] at every $n$, not merely asymptotically; the inequality is often strict, e.g. $\#\mathcal C(1524096000)=122$ against $\prod_p v_p=300$, and $\#\mathcal C(729000000)=84$ against $216$. On a sample of $8000$ integers $n$ in the image of $h$ (all $n=h(k)$, $k\le2\cdot10^5$, including all such $n$ with $f(n)\ge2$), the chain $f(n)\le\#\mathcal C(n)\le\prod_{p\mid n}v_p(n)$ held without exception, with the second inequality strict for $24.3\%$ of them.

*Proof.* The first inequality is the injectivity of the colouring together with $k<\sqrt n$, as above. The second is Chernoff/Rankin: for $\mu>0$,
$$\mathbf 1\Big[\sum_{c_p\ne*}c_p\log p\le\tfrac{L}{2}\Big]\le \exp\Big(\mu\Big(\tfrac L2-\sum_{c_p\ne*}c_p\log p\Big)\Big),$$
and summing over all colour vectors factorises the right-hand side as stated.

For the asymptotic, set $\mu=m^*/L_2$ with $m^*=-\log r=0.104994\ldots$, and put
$$\Psi(m,\alpha)=\frac m2+\frac1\alpha\log\Big(1+\sum_{j=2}^{\alpha}e^{-mj}\Big)\quad(\alpha\ge1),\qquad c_0=\min_{m>0}\ \max_{\alpha\ge1}\Psi(m,\alpha).$$
A direct computation gives that the minimax is attained at $m=m^*$, $\alpha=3$, with value $c_0$; at $m^*$ the next largest values are $\Psi(m^*,2)=0.3493245$ and $\Psi(m^*,4)=0.3430861$, so $\alpha=3$ is the strict maximiser. Stationarity in $\alpha=3$ is exactly $\frac{2r^2+3r^3}{1+r^2+r^3}=\frac32$, i.e. $3r^3+r^2-3=0$, and then $\Psi(m^*,3)=\frac13\log(1+r^2+r^3)-\frac12\log r=c_0$.

Now take logarithms in the displayed bound and split the product at $z=\exp(L_2-3\log L_2)$.

*Small primes $p\le z$.* Each factor is at most $\log v_p(n)\le\log(L/\log2)\ll L_2$, and there are at most $\pi(z)\ll z/\log z\ll L/L_2^{4}$ of them, contributing $\ll L/L_2^{3}=o(L/L_2)$.

*Large primes $p>z$.* Write $u_p=\log p/L_2>1-\varepsilon$ with $\varepsilon=3\log L_2/L_2\to0$. The corresponding factor is $\Lambda(u_p,\alpha_p)$ where $\Lambda(u,\alpha)=\log(1+\sum_{j=2}^{\alpha}e^{-m^*ju})$, and $\Lambda$ is decreasing in $u$, so $\Lambda(u_p,\alpha)\le\Lambda(1-\varepsilon,\alpha)$. By definition of $\Psi$,
$$\frac{\Lambda(1-\varepsilon,\alpha)}{\alpha}=\Psi\big(m^*(1-\varepsilon),\alpha\big)-\frac{m^*(1-\varepsilon)}{2}\le\max_{\alpha}\Psi\big(m^*(1-\varepsilon),\alpha\big)-\frac{m^*}{2}+O(\varepsilon).$$
The maximum over $\alpha$ is effectively over a *finite* range: for all $m$ in a fixed neighbourhood of $m^*$,
$$\Psi(m,\alpha)\le\frac m2+\frac1\alpha\log\Big(1+\frac{e^{-2m}}{1-e^{-m}}\Big)\le\frac{m^*}{2}+O(1)+\frac{C}{\alpha},$$
so $\Psi(m,\alpha)<c_0$ once $\alpha\ge A_0$ for an absolute $A_0$ (recall $m^*/2=0.0525\ldots<c_0$). Hence $\max_{\alpha\ge1}\Psi(m,\alpha)=\max_{1\le\alpha<A_0}\Psi(m,\alpha)$ near $m^*$, a maximum of finitely many continuous functions of $m$, so it is continuous and the right side is $c_0-\frac{m^*}2+O(\varepsilon)$. Hence
$$\sum_{p>z}\Lambda(u_p,\alpha_p)\le\Big(c_0-\frac{m^*}{2}+O(\varepsilon)\Big)\frac{1}{1-\varepsilon}\sum_{p>z}\alpha_p u_p\le\Big(c_0-\frac{m^*}{2}+o(1)\Big)\frac{L}{L_2},$$
using $\sum_p\alpha_p\log p=L$. Adding the $\frac{\mu L}{2}=\frac{m^*}{2}\cdot\frac{L}{L_2}$ term gives $\log f(n)\le(c_0+o(1))L/L_2$.

*Sharpness.* For $n_y=\prod_{p\le y}p^3$ the colours available at each $p$ are $\{*,2,3\}$ with costs $0,2,3$ (in units of $\log p$) and total budget $\frac12\log n_y=\frac32\theta(y)$. Let $H(\bar c)$ denote the maximum of the entropy $-\sum_i x_i\log x_i$ over distributions $(x_*,x_2,x_3)$ subject to $2x_2+3x_3\le\bar c$; the Gibbs solution at $\bar c=\frac32$ is $(x_*,x_2,x_3)\propto(1,r^2,r^3)$ with $3r^3+r^2-3=0$, i.e. $(0.3936\ldots,0.3191\ldots,0.2873\ldots)$, and $H(\tfrac32)=\log(1+r^2+r^3)-\frac32\log r=1.0898110\ldots$.

Two points need care, since the budget is *exactly* tight at $\bar c=\frac32$ and the true costs are $j\log p$, not $j\log y$. Fix $\delta,\eta>0$. Give colour $*$ to every $p\le y^{1-\eta}$ (these number $o(\pi(y))$), and colour the primes $p\in(y^{1-\eta},y]$ — of which there are $(1-o(1))\pi(y)$, each with $\log p\in((1-\eta)\log y,\log y]$ — independently according to the Gibbs distribution for budget $\bar c=\frac32-\delta$. The expected cost is at most $(\frac32-\delta)\theta(y)$, so by Hoeffding all but $o(1)$ of these assignments have cost below $\frac32\theta(y)$, i.e. lie in $\mathcal C(n_y)$ with room to spare. Counting the assignments with the prescribed empirical colour frequencies gives
$$\#\mathcal C(n_y)\ \ge\ \exp\big((H(\tfrac32-\delta)+o(1))\,\pi(y)\big).$$
Since $\log n_y\sim3y$, $\log\log n_y\sim\log y$ and $\pi(y)\sim y/\log y$, this is $\exp\big((H(\frac32-\delta)/3+o(1))\log n_y/\log\log n_y\big)$. Letting $\delta\to0$ and using continuity of $H$ gives $\limsup_y\frac{\log\#\mathcal C(n_y)}{\log n_y/\log\log n_y}\ge H(\frac32)/3=c_0$, matching the upper bound. (The identity $H(\tfrac32)/3=c_0$ is exact, not merely numerical: the two expressions differ by the factor $3$. An independent check is that the exact Chernoff dual rate $G(y)=\min_{\lambda>0}\big[\tfrac32\lambda\,\theta(y)+\sum_{p\le y}\log(1+p^{-2\lambda}+p^{-3\lambda})\big]$ satisfies $G(y)/\pi(y)=1.09063,\,1.09019,\,1.09000,\,1.08992,\,1.08988$ for $y=10^2,\dots,10^6$, descending to $H(\tfrac32)=1.0898110$.) $\blacksquare$

**Remark (effective form).** The proof gives the $o(1)$ explicitly and uniformly: the error is $O(\varepsilon)=O(\log\log\log n/\log\log n)$ from the large primes and $O(1/(\log\log n)^2)$ from the small ones, so for all $n\ge16$,
$$\log f(n)\ \le\ \Big(c_0+O\Big(\frac{\log\log\log n}{\log\log n}\Big)\Big)\frac{\log n}{\log\log n}.$$

**Remark.** The congruence constraints one might hope to add here — e.g. "$v_2(\sigma(q^{\delta}))\ge1$ whenever $\delta$ is odd", giving $\#\{q\text{ odd}:v_q(k)\text{ odd}\}\le v_2(n)$, and its analogues $\#\{q\equiv1\ (\ell):\ \ell\mid v_q(k)+1\}\le v_\ell(n)$ — do **not** improve the constant. The reason is that an adversarial $n$ may inflate $v_2(n)$ (or $v_\ell(n)$) to $\asymp\pi(y)$ at a cost of only $O(\pi(y))$ in $\log n\asymp\pi(y)\log y$, which is negligible; the constraints then become vacuous while the majorant is unchanged. I checked this trade-off explicitly; it is the reason $c_0$ rather than something like $\log2/2$ appears.

---

## 3. A reduction of the strong form of Problem 1060

> **Theorem 3.** Let $M\ge2$ be an integer and suppose $h$ is injective on $\{m\ge1:\gcd(m,M)=1\}$. Then for every $n$,
> $$f(n)\ \le\ \prod_{p\mid M}\big(v_p(n)+1\big)\ \ll_M\ (\log n)^{\omega(M)} .$$

*Proof.* Let $k,k'\in h^{-1}(n)$ with $v_p(k)=v_p(k')$ for every $p\mid M$. Write $k=AB$ and $k'=AB'$ where $A=\prod_{p\mid M}p^{v_p(k)}$ and $\gcd(BB',M)=1$. Then $\gcd(A,B)=\gcd(A,B')=1$, so $h(A)h(B)=h(k)=h(k')=h(A)h(B')$, giving $h(B)=h(B')$ and hence $B=B'$ and $k=k'$. So $k\mapsto(v_p(k))_{p\mid M}$ is injective on the fiber, and $v_p(k)\le v_p(n)$ for each $p\mid M$ since $k\mid n$. $\blacksquare$

The converse is immediate, so: *$h$ is injective on integers coprime to $M$ **iff** any two distinct preimages of any $n$ differ in $v_p$ for some $p\mid M$.*

**Consequence.** Injectivity on $\mathcal R_M$ for *any* fixed $M$ would give $f(n)=O_M((\log n)^{\omega(M)})$ and settle Erdős Problem 1060 in the strong $(\log n)^{O(1)}$ form. §5 shows this fails for $M\mid210$, so the hypothesis is not available — but Theorem 3 remains the engine behind the surviving reformulation of §5.1, where $M$ is allowed to grow with $n$.

---

## 4. Computations

All computations are exhaustive sieves (segmented sieve for $\sigma$, exact 64-bit arithmetic, sort-and-scan for equal $h$-values); source available on request.

**(a) All fibers with $n\le10^{18}$.** Computing $h(k)$ for all $k\le10^9$ (so all fibers with $n\le10^{18}$, since $k<\sqrt n$) yields $32{,}199{,}003$ values of $n$ with $f(n)\ge2$, distributed as

| $f(n)$ | 2 | 3 | 4 | 5 | $\ge6$ |
|---|---|---|---|---|---|
| \# of $n\le10^{18}$ | 31{,}289{,}686 | 899{,}749 | 9{,}245 | 323 | 0 |

with least elements $336$, $333{,}312$, $5{,}418{,}319{,}872$, $1{,}584{,}858{,}562{,}560$ respectively. This independently reproduces $a(2),\dots,a(5)$ of A212490 and confirms $a(6)>10^{18}$ (consistent with Kominers's stronger $a(6)>1.06\cdot10^{20}$).

**(b) Reduced collisions.** Call $(u,v)$, $u\ne v$, $h(u)=h(v)$, *reduced* if $v_p(u)\ne v_p(v)$ for every prime $p\mid uv$. Every collision $(k,k')$ factors as $k=Du$, $k'=Dv$ with $\gcd(D,uv)=1$ and $(u,v)$ reduced (take $D=\prod_{p:\,v_p(k)=v_p(k')>0}p^{v_p(k)}$), so reduced collisions are the "atoms" of the whole phenomenon. Extending the census to $k\le10^9$ (all fibers with $n\le10^{18}$) gives $32{,}199{,}003$ fibers with $f(n)\ge2$, which reduce to exactly **146** distinct reduced collisions (count independently reproduced by a second implementation). Their counts by $\max(u,v)\le K$:

| $K$ | $10^3$ | $10^4$ | $10^5$ | $10^6$ | $10^7$ | $10^8$ | $10^9$ |
|---|---|---|---|---|---|---|---|
| \# reduced | 7 | 11 | 20 | 38 | 59 | 95 | 146 |

The smallest are $(12,14)$, $(48,62)$, $(112,124)$, $(160,189)$, $(192,254)$, $(315,351)$, $(448,508)$.

**(c) Supports.** Writing $\operatorname{supp}(u,v)$ for the set of primes dividing $uv$: of the 146 reduced collisions, $143$ contain $2$; exactly $3$ do not, namely
$$(315,\,351),\qquad(90\,980\,505,\ 93\,972\,879),\qquad(602\,026\,425,\ 630\,574\,875),$$
with factorisations $(3^2\cdot5\cdot7,\ 3^3\cdot13)$, $(3^2\cdot5\cdot7^2\cdot11^3\cdot31,\ 3^4\cdot7\cdot11\cdot13\cdot19\cdot61)$ and $(3^7\cdot5^2\cdot7\cdot11^2\cdot13,\ 3^4\cdot5^3\cdot7^2\cdot31\cdot41)$; and $21$ do not contain $3$. **None avoids both $2$ and $3$**: the least prime of the support is $2$ ($143\times$) or $3$ ($3\times$).

**(d) Direct test of injectivity coprime to 6.** Computing $h(k)$ for every integer $2\le k\le1.2\cdot10^{10}$ with $\gcd(k,6)=1$ ($3{,}999{,}999{,}999$ values; $k=1$ is irrelevant as $h(1)=1$) produced **no collision**. Since $k<\sqrt n$, this proves:

> No $n\le1.44\cdot10^{20}$ has two distinct preimages both coprime to $6$.

*(Arithmetic caveat, and why it is harmless.* Here $h(k)$ can reach $\approx2k^2>2^{64}$, so the stored values are $h(k)\bmod 2^{64}$. This can only produce **false positives**, never false negatives: if $h(u)=h(v)$ exactly then certainly $h(u)\equiv h(v)\bmod2^{64}$, so a genuine collision is always flagged. Exactly one 64-bit repetition was flagged in the whole range, at $k=3{,}838{,}121{,}239$ and $k=7{,}223{,}814{,}737$; in exact arithmetic $h=15{,}716{,}994{,}707{,}614{,}520{,}320$ and $52{,}610{,}482{,}855{,}033{,}623{,}552$ respectively — congruent mod $2^{64}$ but unequal, so spurious. With that one candidate eliminated, the conclusion above is unconditional.)

Equivalently, for all $n\le1.44\cdot10^{20}$ the map $k\mapsto(v_2(k),v_3(k))$ *is* injective on $h^{-1}(n)$, and $f(n)\le(v_2(n)+1)(v_3(n)+1)$ there. This is no longer evidence for a conjecture — §5 exhibits a collision coprime to $6$ — but it does locate the threshold: combining with Proposition 5(1), whose target is $h(u)=1.859\ldots\cdot10^{42}$, the least $n$ with two preimages coprime to $6$ satisfies
$$1.44\cdot10^{20}\ <\ n_{\min}\ \le\ 1.86\cdot10^{42}.$$
It is a useful cautionary data point that the phenomenon first appears somewhere past $10^{20}$: exhaustive search at any feasible scale would have suggested the opposite conclusion.

---

## 5. The finite hitting-set route is closed

Theorem 3 invites the hypothesis that some fixed $M$ works. Writing $\mathcal R_M$ for the integers coprime to $M$, the hypothesis "$h$ is injective on $\mathcal R_M$" is *false* for every $M$ dividing $9699690=2\cdot3\cdot5\cdot7\cdot11\cdot13\cdot17\cdot19$. The first three certificates below were produced in a parallel investigation of this problem and are **verified exactly here** (arbitrary-precision $\sigma$ via divisor sums, independent of how they were found); the last two are new and were found by the method of §5.2.

> **Proposition 5 (counterexamples).** Each pair below satisfies $u\ne v$ and $h(u)=h(v)$.
>
> 1. $u=13^2\cdot17\cdot31\cdot37^3\cdot61\cdot67^2\cdot73\cdot97\cdot137$, $v=5\cdot7^2\cdot23\cdot31^3\cdot37^2\cdot61^2\cdot67\cdot137^2$, with $\gcd(uv,6)=1$;
> 2. $u=7^2\cdot11^2\cdot13\cdot31^2\cdot37\cdot43\cdot61\cdot83\cdot127$, $v=7^5\cdot11^3\cdot19^2\cdot31^3\cdot331$, with $\gcd(uv,30)=1$;
> 3. $u=11^2\cdot13^2\cdot17\cdot19\cdot31\cdot61\cdot97\cdot127^2\cdot271\cdot307^2\cdot331\cdot367$, $v=13\cdot17^2\cdot19^2\cdot23\cdot31^2\cdot43\cdot61^2\cdot83\cdot127\cdot307\cdot733\cdot5419$, with $\gcd(uv,210)=1$; both cubefree.
>
> Numerically, (3) is $u=60629697601617236747379985403$, $v=61655391632564660609643619057$ and
> $$h(u)=h(v)=5276516179938729922490847708056660616574496169354744299520 .$$
> All three pairs are *reduced* in the sense of §4(b): $v_p(u)\ne v_p(v)$ at every prime of the support.

To these I add a fourth, found independently here by integer programming over the atom lattice (see §5.2) and verified exactly:

> **Proposition 5$'$ (a collision coprime to $2310$).** Let
> $$u=19^4\cdot23\cdot31^3\cdot37^2\cdot53\cdot61^2\cdot67\cdot79\cdot97\cdot137\cdot3169,\qquad v=13^2\cdot17\cdot19\cdot23^2\cdot31\cdot37^3\cdot61\cdot67^2\cdot97^2\cdot151\cdot317\cdot911 .$$
> Then $u=5373815401451658881188228991633$, $v=5094355644713259530538832804073$, $\gcd(uv,2310)=1$, the pair is reduced, and
> $$h(u)=h(v)=36610181552812639785382270020985223371406524306622986282598400 .$$
> Hence $h$ is not injective on $\mathcal R_{2310}$ either, and $\rho\big(3.7\cdot10^{61}\big)\ge13$.

> **Proposition 5$''$ (roughness $19$).** With
> $$u=19^3\cdot23\cdot31\cdot37^2\cdot41^2\cdot47\cdot53^2\cdot61^2\cdot67\cdot73\cdot127^2\cdot137^2\cdot199\cdot271^2\cdot281\cdot431^2\cdot449\cdot1801\cdot6143,$$
> $$v=19^2\cdot37^3\cdot41\cdot47^2\cdot53^3\cdot61\cdot67^3\cdot73^2\cdot97\cdot127\cdot137\cdot181\cdot271\cdot397\cdot409\cdot431\cdot1723\cdot5419\cdot24571,$$
> one has $u=31022021036909658303495391817538006725251311464378626419887$, $v=32039206552671412478620058485764169253958249429640910475739$, the pair is reduced, $\gcd(uv,9699690)=1$, and $h(u)=h(v)$ is the $118$-digit number $1.2967\ldots\cdot10^{117}$. Hence $\rho(1.3\cdot10^{117})\ge19$.

**Consequence.** Theorem 3 yields nothing for $M\mid210$. An earlier draft of this note conjectured that $h$ is injective on $\mathcal R_6$; certificate (1) refutes it. (My own exhaustive search, §4(d), only proves there is no such pair below $1.2\cdot10^{10}$, and $u\approx1.2\cdot10^{21}$ in (1) — so the two computations are consistent, and the conjecture was simply wrong. The statistical caveat recorded in that draft — that the census evidence was far too thin to support it — was the correct reading.)

Together with Proposition 4 this closes **both** routes that the elementary theory offers:

| route | bound it would give | status |
|---|---|---|
| count squarefull $d$ with $h(d)\mid n$ | $\ge n^{(\log2/4+o(1))/\log\log n}$ | dead (Proposition 4) |
| project onto a fixed finite prime set $M$ | $\prod_{p\mid M}(v_p(n)+1)$ | dead for $M\mid210$ (Proposition 5); presumably for all $M$ |

It is natural to conjecture that *every* finite $M$ fails, i.e. that for each $z$ there is a reduced collision all of whose primes exceed $z$. I could not prove this, and it is not implied by the three certificates.

### 5.1 What survives: the roughness function

Theorem 3 does not actually need a *fixed* $M$. If $k\mapsto(v_p(k))_{p\le z}$ is injective on every fiber for some $z=z(n)$, the same proof gives $f(n)\le\prod_{p\le z}(v_p(n)+1)$, hence $\log f(n)\ll\pi(z)\log\log n$. So define the **roughness function**
$$\rho(x)\ :=\ \max\big\{P^-(uv)\ :\ u\ne v,\ h(u)=h(v)=n\le x,\ (u,v)\ \text{reduced}\big\},$$
$P^-$ denoting the least prime factor. Then $k\mapsto(v_p(k))_{p\le\rho(n)}$ *is* injective on every fiber of every $n\le x$, and:

> **Proposition 6.** $\displaystyle \log f(n)\ \ll\ \pi(\rho(n))\,\log\log n$. In particular:
> * if $\rho(x)=o\!\big(\log x/\log\log x\big)$ then $f(n)\le n^{o(1/\log\log n)}$ — Erdős's first question;
> * if $\rho(x)=O\big((\log\log x)^{A}\big)$ then $f(n)\le\exp\big(O((\log\log n)^{A+1})\big)$, comfortably inside $(\log n)^{O(1)}$ territory for the relevant ranges;
> * if $\rho(x)\gg\log x/\log\log x$ then this route gives nothing.

*Proof.* Injectivity of $k\mapsto(v_p(k))_{p\le\rho(n)}$ on $h^{-1}(n)$ is immediate: two distinct preimages have a reduced core, whose least prime is $\le\rho(n)$ by definition, and they differ there. Hence $f(n)\le\prod_{p\le\rho(n)}(v_p(n)+1)$ and $\log f(n)\le\pi(\rho(n))\log(\log n/\log2+1)$. $\blacksquare$

**This is the sharpest surviving reformulation I know: Erdős Problem 1060 (first form) reduces to showing $\rho(x)=o(\log x/\log\log x)$.**

Lemma 1 already gives a (very weak) unconditional bound in that direction:

> **Corollary 6.1.** $\rho(x)<x^{1/4}$ for all $x\ge2$.

*Proof.* Let $(u,v)$ be reduced with $h(u)=h(v)=n\le x$ and every prime of $uv$ exceeding $z:=P^-(uv)$. If $z\le3$ there is nothing to prove, so assume $z\ge5$; then the top disagreement prime $Q$ satisfies $Q>z\ge5$, and Lemma 1 supplies a prime $q$ with $q^{e}\mid k'$ for one of $k'\in\{u,v\}$ and $e\ge2$. Since $q>z$, that $k'$ exceeds $z^2$. But $n=h(k')=k'\sigma(k')>k'^2>z^4$, so $z<n^{1/4}\le x^{1/4}$. $\blacksquare$

The gap between $x^{1/4}$ and the required $o(\log x/\log\log x)$ is of course enormous; I record it only because it is the one unconditional handle on $\rho$ that I have, and it comes from Lemma 1 rather than from counting.

### 5.2 What the data says about $\rho$

Writing $L=\log n$, $L_2=\log\log n$ for the collision's own target $n$:

| collision | $P^-(uv)$ | $\log n$ | $L/L_2$ | $P^-/(L/L_2)$ |
|---|---|---|---|---|
| all 146 exhaustive ones ($n\le10^{18}$) | $\le3$ | $\le41$ | | $\le0.62$ |
| Proposition 5(1), coprime to $6$ | $5$ | $97.3$ | $21.3$ | $0.235$ |
| Proposition 5(2), coprime to $30$ | $7$ | $78.2$ | $17.9$ | $0.390$ |
| Proposition 5(3), coprime to $210$ | $11$ | $132.9$ | $27.2$ | $0.405$ |
| Proposition 5$'$, coprime to $2310$ | $13$ | $141.8$ | $28.6$ | $0.454$ |
| Proposition 5$''$, coprime to $9699690$ | $19$ | $269.7$ | $48.2$ | $0.394$ |
| (a second roughness-$19$ certificate) | $19$ | $409.7$ | $68.1$ | $0.279$ |

The ratio does not tend to $0$; across $P^-\in\{3,5,7,11,13,19\}$ it fluctuates in the band $[0.24,\,0.46]$ with no visible trend in either direction. Since every entry is a *feasible* point of an integer program stopped at a time limit, each $\log n$ is only an upper bound for the minimal one at that roughness, so each ratio is a **lower** bound for the extremal ratio: the true curve lies at or above this band.

That is the single most decision-relevant observation in this note. It suggests
$$\rho(x)\ \asymp\ \frac{\log x}{\log\log x},$$
which is exactly the borderline at which Proposition 6 returns $\log f(n)\ll\log n/\log\log n$ — i.e. it **reproduces the known bound and improves nothing**. To answer Erdős's first question one needs the ratio to tend to $0$, and six data points spread over $10^{18}$ to $10^{117}$ give no sign of that. I therefore do not expect this route to succeed either, though of course six points prove nothing about an asymptotic.

Two competing considerations, neither conclusive. *Against* small $\rho$: fix a roughness target $z$ and a prime bound $Y$. Every atom $h(p)=p(p+1)$ with $z<p\le Y$ automatically has all its prime factors $\le Y$, giving $\pi(Y)-\pi(z)$ usable columns; the atoms $h(p^2)=p^2\Phi_3(p)$ contribute a further positive proportion of $\pi(Y)$ (those with $\Phi_3(p)$ being $Y$-smooth). Against an ambient dimension of only $\pi(Y)$, the relation lattice is therefore already nontrivial for $Y$ a modest multiple of $z$ — so *rational* relations with all bases $>z$ are plentiful, and only the $\{-1,0,1\}$ / one-block-per-base structure stands in the way. *For* small $\rho$: in the one rough certificate we have, the auxiliary primes are far larger than the bases ($Y=5419$ against $z=11$), because a sparse relation can only close if the large prime factors of the $\sigma$-values are themselves bases. That is a severe constraint, and it is what makes such certificates hard to find. Which effect wins as $z\to\infty$ decides Erdős's first question, and I do not know.

**Method, and what it costs to go one prime rougher.** These certificates are found by integer programming on the *atom lattice*. Take columns indexed by pairs $(p,e)$ with $p$ above the roughness target and $e\le E$, each column being the exponent vector of $h(p^e)$; iteratively delete any column containing a prime that occurs in no other column (such a prime can never cancel), leaving a *relation core*; then ask a $0/1$ program for $y^\pm$ with $\sum_j(y^+_j-y^-_j)\mathbf v_j=0$, at most one $+$ and one $-$ per base, and at least two blocks used. Any feasible point is exactly a reduced collision with the prescribed roughness.

Raising the target by a single prime is expensive. With bases $\ge13$ and the modest space $p\le8000$, $e\le2$ — essentially the space in which the coprime-to-$210$ certificate lives — the program is **infeasible**. Enlarging to $p\le40000$, $e\le4$ (relation core: $6428$ columns, $3193$ bases, $3282$ primes) produces Proposition 5$'$. So roughness $13$ is attainable, but only after a substantial enlargement of the search space, which is itself the mechanism pushing $\log n$ up.

---

## 6. Where the real difficulty lies

It may be useful to record why the elementary route stops where it does.

Every solution factors as $n=\prod_{p\in S}h(p^{\beta_p})$ over distinct primes $p$, so $f(n)$ counts *factorisations of $n$ into the atoms $h(p^{\beta})=p^{\beta}\sigma(p^{\beta})$ with distinct bases*, and collisions are exactly multiplicative relations among these atoms. Three remarks:

1. **Counting the squarefull part provably cannot work.** Writing $k=da$ with $d$ squarefull and $a$ squarefree coprime to $d$, Corollary 1.1 says $d$ determines $k$, so with
$$F(n):=\#\{d\ \text{squarefull}:\ h(d)\mid n\}$$
we have the chain $f(n)\le F(n)\le\#\mathcal C(n)\le\prod_{p\mid n}v_p(n)$. (For the middle inequality: $h(d)\mid n$ and $h(d)=d\sigma(d)>d^2$ give $d<\sqrt n$, so the colour vector $c_p=v_p(d)$ for $p\mid d$, $c_p=*$ otherwise, lies in $\mathcal C(n)$; distinct $d$ give distinct vectors.) **Every bound in the literature, and Theorem 2, factors through $F$.** The following shows that this is fatal.

> **Proposition 4 (barrier).** Let $y\ge3$, let $T$ be the set of primes in $(y/2,y]$, and put $n_y^{\ast}=\prod_{q\in T}h(q^2)$. Then
> $$F(n_y^{\ast})\ \ge\ 2^{|T|}\ =\ \exp\Big(\big(\tfrac{\log2}{4}+o(1)\big)\frac{\log n_y^{\ast}}{\log\log n_y^{\ast}}\Big).$$
> Consequently no majorant dominating $F$ — in particular neither $\prod_{p\mid n}v_p(n)$ nor $\#\mathcal C(n)$ — can establish $f(n)\le n^{o(1/\log\log n)}$.

*Proof.* For $S\subseteq T$ put $d_S=\prod_{q\in S}q^2$, which is squarefull, and the $d_S$ are distinct. By multiplicativity $h(d_S)=\prod_{q\in S}h(q^2)$, which divides $\prod_{q\in T}h(q^2)=n_y^{\ast}$. Hence $F(n_y^{\ast})\ge2^{|T|}$. For the asymptotics, $h(q^2)=q^2(q^2+q+1)$ gives $\log h(q^2)=4\log q+O(1/q)$, so $\log n_y^{\ast}\sim4(\theta(y)-\theta(y/2))\sim2y$, while $|T|=\pi(y)-\pi(y/2)\sim y/(2\log y)$ and $\log\log n_y^{\ast}\sim\log y$. Therefore
$$\frac{|T|\log2}{\log n_y^{\ast}/\log\log n_y^{\ast}}\ \longrightarrow\ \frac{y\log2/(2\log y)}{2y/\log y}=\frac{\log2}{4}. \qquad\blacksquare$$

**Why the §3 route escapes *this* barrier** (though §5 kills it for its own reasons). The reduction of Theorem 3 does not factor through $F$, and on this very family it behaves completely differently. Each $h(q^2)=q^2(q^2+q+1)$ is odd, so $v_2(n^{\ast}_y)=0$; and $3\mid q^2+q+1$ exactly when $q\equiv1\ (3)$, so $v_3(n^{\ast}_y)=\#\{q\in T:q\equiv1\ (3)\}\sim|T|/2$. Hence the conditional bound of Theorem 3 is
$$(v_2+1)(v_3+1)\ \sim\ \tfrac12|T| \ =\ O\!\Big(\frac{\log n^{\ast}_y}{\log\log n^{\ast}_y}\Big),$$
*linear* in $|T|$ where $F$ is *exponential* in $|T|$ — e.g. at $y=200$, $11$ against $2^{21}=2\,097\,152$. So the two barriers are genuinely independent: Proposition 4 does not touch the §3 route, and Proposition 5 does not touch the colouring route. Each closes the other's escape.

The gap between $F$ and $f$ on these $n$ is enormous, and is exactly the point: for $y=20$ one has $T=\{11,13,17,19\}$, $n^{\ast}_{20}=6\,073\,558\,255\,415\,824\,173$, $F(n^{\ast}_{20})=2^4=16$ — every one of the sixteen subsets really does satisfy $h(d_S)\mid n^{\ast}_{20}$ — and yet $f(n^{\ast}_{20})=1$. So the condition that the *complementary* factor $n/h(d)$ lie in $h(\{\text{squarefree}\})$ is not a side condition to be discarded; it carries all of the content.

2. **Congruence budgets are purchasable.** As noted after Theorem 2, all the $\ell$-adic constraints of the form $\#\{q\equiv1\ (\ell):\ \ell\mid v_q(k)+1\}\le v_\ell(n)$ can be neutralised by an adversarial $n$ at negligible cost in $\log n$, because the relevant $\ell$ are bounded (for exponents $\beta\le3$, only $\ell\in\{2,3\}$ can occur) while $v_\ell(n)$ is cheap to inflate.

3. **What the truth should look like (heuristic).** By Corollary 1.1, $a$ is determined by $h(a)$, so exactly
$$f(n)=\#\big\{d\ \text{squarefull}:\ h(d)\mid n,\ \ n/h(d)=h(a)\ \text{for a squarefree }a\text{ with }\gcd(a,d)=1\big\}.$$
Now the image of the squarefree numbers is *thin*: $\#\{a\ \text{squarefree}: h(a)\le X\}\asymp X^{1/2}$, since $h(a)\asymp a^2$. Modelling membership in $h(\mathcal S)$ as a random event of probability $X^{-1/2}$ at $X=n/h(d)$ gives
$$\mathbf E\,f(n)\ \approx\ \sum_{d}\Big(\frac{h(d)}{n}\Big)^{1/2}\ \approx\ n^{-1/2}\sum_{d}d ,$$
the sums over squarefull $d$ with $h(d)\mid n$. Only $d$ within a bounded factor of $\sqrt n$ contribute appreciably — so $f(n)$ should be governed not by *how many* squarefull $d$ divide appropriately, but by how many of them are of nearly maximal size. On the barrier family $n^{\ast}_y$ this predicts $\prod_{q\in T}(1+q^{-2})=O(1)$, matching the computed $f(n^\ast_{20})=1$ against $F=16$. This is only a heuristic — $h(\mathcal S)$ is not a random set — but it is consistent with $f(n)\le(\log n)^{O(1)}$ and indicates that any successful argument must exploit the thinness of $h(\mathcal S)$, not merely divisibility.

What is missing, and what Lemma 1 is intended as a first step toward, is genuine control of the multiplicative relations among the values $\Phi_t(q)$, $t\ge3$ — equivalently, of how often $\sigma(q^\beta)$ can be built entirely from primes dividing $n$. The literature on smooth values of shifted primes ($p\pm1$) is extensive, but I could find nothing on $y$-smooth values of $(q^{\beta+1}-1)/(q-1)$ for $\beta\ge2$, which is precisely what a real attack on Problem 1060 seems to require.

---

## 7. An attack that works in the extremal regime

Sections 4–6 are negative. This section is not: it proves Erdős's first question for a class of $n$ that includes the extremal shape of every majorant discussed above, and it shows that that extremal shape has **no preimages at all**.

The mechanism is the interaction of two facts that have not, to my knowledge, been combined before:

* **parity** forces almost every exponent of $k$ to be *even*; and
* an *even* exponent makes $\sigma(q^{e})$ a product of cyclotomic values $\Phi_t(q)$ with $t$ **odd**, and the prime factors of $\Phi_t(q)$ are $\equiv1\pmod t$.

The second point is a congruence obstruction on $\sigma(k)$ that an adversarial $n$ cannot switch off, because it is forced by the parity of the exponents rather than by any budget.

> **Lemma 7.1 (parity).** If $h(k)=n$ then $O:=\{q:v_q(k)\ \text{odd}\}$ satisfies $|O|\le v_2(n)+1$.

*Proof.* For odd $q$ with $v_q(k)$ odd, $\sigma(q^{v_q(k)})$ is a sum of $v_q(k)+1$ (an even number of) odd terms, hence even. These factors are coprime to one another's index in the product $\sigma(k)=\prod_q\sigma(q^{v_q(k)})$, so $v_2(\sigma(k))\ge|O\setminus\{2\}|$. As $\sigma(k)\mid n$, $|O\setminus\{2\}|\le v_2(n)$. $\blacksquare$

> **Lemma 7.2 (even exponents are cyclotomically constrained).** Let $q$ be prime, $e\ge2$ even, and let $r$ be a prime with $r\mid\sigma(q^{e})$ and $r>e+1$. Then $\operatorname{ord}_r(q)=:t$ satisfies $3\le t\le e+1$, $t$ is **odd**, and $t\mid r-1$. In particular $r-1$ has an odd prime factor $\le e+1$.

*Proof.* From $r\mid\sigma(q^e)$ and $(q-1)\sigma(q^e)=q^{e+1}-1$ we get $r\mid q^{e+1}-1$, so $t\mid e+1$; as $e+1$ is odd, $t$ is odd. If $t=1$ then $q\equiv1\pmod r$, whence $\sigma(q^e)\equiv e+1\pmod r$ and $r\mid e+1$, contradicting $r>e+1$. So $t\ge3$, and $t\mid r-1$ since $t=\operatorname{ord}_r(q)$. Any prime factor of $t$ is odd and $\le t\le e+1$, and divides $r-1$. $\blacksquare$

For $A\ge1$ put
$$\mathcal G_A\ :=\ \{r\ \text{prime}:\ r>A+1\ \text{and}\ r-1\ \text{has no odd prime factor}\le A+1\}.$$
By Mertens and Dirichlet, $\mathcal G_A$ has relative density $\delta_A=\prod_{3\le\ell\le A+1}\big(1-\tfrac1{\ell-1}\big)>0$ among the primes; e.g. $\mathcal G_2=\mathcal G_3=\{r\ge5:r\equiv2\ (3)\}$, of density $\tfrac12$.

> **Theorem 7.3 (emptiness).** Let $n$ satisfy $v_p(n)\le A$ for all $p$, and put $y=P^+(n)$. If $f(n)\ge1$ then
> $$\#\{r\in\mathcal G_A:\ r\mid n,\ v_r(n)\ \text{odd}\}\ \le\ (A+1)^2\log_2 y+(A+1).$$

*Proof.* Let $h(k)=n$ and set $X=\prod_{q\in O}\sigma(q^{v_q(k)})$. Since $|O|\le v_2(n)+1\le A+1$ (Lemma 7.1) and each $\sigma(q^{v_q(k)})<q^{v_q(k)+1}\le y^{A+1}$, we get $X<y^{(A+1)^2}$ and so $\omega(X)\le\log_2X\le(A+1)^2\log_2y$.

Let $r\in\mathcal G_A$. For $q\notin O$ the exponent $v_q(k)$ is even and $r>A+1\ge v_q(k)+1$, so Lemma 7.2 would force $r-1$ to have an odd prime factor $\le v_q(k)+1\le A+1$ — impossible. Hence $r\nmid\sigma(q^{v_q(k)})$ for every $q\notin O$, and therefore $v_r(\sigma(k))=v_r(X)$.

Now take $r\in\mathcal G_A$ with $r\mid n$ and $v_r(n)$ odd. If $r\nmid X$ then $v_r(\sigma(k))=0$, so $v_r(k)=v_r(n)$ is odd and $r\in O$. Thus every such $r$ lies in the set of prime divisors of $X$ or in $O$, of total size $\le(A+1)^2\log_2y+(A+1)$. $\blacksquare$

> **Corollary 7.4.** For all sufficiently large $y$, $\ f\big(\prod_{p\le y}p^{3}\big)=0$.

*Proof.* Here $A=3$ and every exponent is odd, so the left side of Theorem 7.3 is $\#\{r\le y:r\ge5,\ r\equiv2\ (3)\}\sim\tfrac12\pi(y)$, while the right side is $16\log_2y+4$. $\blacksquare$

**This is the exact $n$ at which Kominers's majorant $\prod_p v_p(n)$, and my $\#\mathcal C(n)$, attain their maximal order** — and it has an empty fiber. Numerically $f(\prod_{p\le y}p^3)=0$ already for every $y\le29$ (exhaustive over all $4^{\pi(y)}$ candidate divisors), long before the asymptotic argument bites at $y\approx4\cdot10^3$.

Pushing the same mechanism further pins $k$ almost completely.

> **Theorem 7.5.** Let $n$ satisfy $v_p(n)\le3$ for all $p$, and put $y=P^+(n)$. Then
> $$f(n)\ \le\ \exp\big(O(\log^2y)\big).$$
> Consequently, if $y\le\exp\big((\log n)^{1/2-\varepsilon}\big)$ for some fixed $\varepsilon>0$ — in particular throughout the extremal regime $y=O(\log n)$ — then
> $$f(n)\le n^{o(1/\log\log n)},$$
> i.e. **Erdős's first question holds for such $n$**, with a great deal to spare.

*Proof.* Write $L=\log n$, $L^{(3)}=\sum_{r\equiv1(3)}v_r(n)\log r$, $\theta_{2(3)}=\sum_{r\equiv2(3),\,r\mid n}\log r$. Let $h(k)=n$ and $e_r=v_r(k)\in\{0,1,2,3\}$.

*(a)* By Theorem 7.3 all but $E_1:=16\log_2y+4$ of the primes $r\equiv2\ (3)$ dividing $n$ have $v_r(n)$ even, hence $v_r(n)=2$.

*(b)* Let $r\equiv1\ (3)$ with $e_r\ne0$. If $e_r$ is odd then $r\in O$, and $|O|\le v_2(n)+1\le4$. If $e_r=2$ then $\Phi_3(r)=r^2+r+1\equiv3\equiv0\pmod 3$, so each such $r$ contributes at least $1$ to $v_3(\sigma(k))\le v_3(n)\le3$; there are at most $3$ of them. So $e_r=0$ for all but at most $7$ primes $r\equiv1\ (3)$.

*(c)* For $r\equiv2\ (3)$, $e_r$ is even unless $r\in O$; so $e_r\in\{0,2\}$ outside a set of size $\le4$. Put $S=\{r\equiv2\ (3):e_r=2\}$. Then $\log k=2\theta_S+O(\log y)$, the error absorbing the $\le11$ exceptional primes of (b),(c) and $r=3$.

*(d)* $\prod_{r\in S}\Phi_3(r)$ divides $\sigma(k)\mid n$, and for $r\equiv2\ (3)$ every prime factor of $\Phi_3(r)$ is $\equiv1\ (3)$. Hence $2\theta_S<\sum_{r\in S}\log\Phi_3(r)\le L^{(3)}$.

*(e)* Since $\sigma(k)/k\ll\log\log n$, $\log k\ge\tfrac12L-O(\log\log\log n)$. With (c), $2\theta_S\ge\tfrac12L-O(\log y)$, and with (d), $L^{(3)}\ge\tfrac12L-O(\log y)$.

*(f)* By (a), $L=2\theta_{2(3)}+L^{(3)}+O(\log^2y)$, so $2\theta_{2(3)}\le\tfrac12L+O(\log^2y)$. Combining with (e),
$$2\big(\theta_{2(3)}-\theta_S\big)\ \le\ O(\log^2y).$$

So the primes $r\equiv2\ (3)$ dividing $n$ at which $e_r=0$ rather than $2$ have total $\log$-mass $O(\log^2y)$. Distinct such sets give distinct squarefree integers below $\exp(O(\log^2y))$, so there are at most $\exp(O(\log^2y))$ of them. The remaining freedom is the $\le11$ exceptional primes of (b),(c) together with their exponents, contributing at most $\binom{\pi(y)}{11}4^{11}=\exp(O(\log y))$ choices. Multiplying, $f(n)\le\exp(O(\log^2y))$.

For the consequence, $\log^2y\le(\log n)^{1-2\varepsilon}=o\big(\log n/\log\log n\big)$. $\blacksquare$

**Scope, honestly.** Theorem 7.5 assumes $v_p(n)\le3$ and controls $P^+(n)$; it does *not* settle Problem 1060. Two gaps remain. (i) *Large $P^+$*: when $n$ has a prime factor of size $n^{c}$ the error terms $O(\log y)$ in (c) swamp $L$, because a single exceptional prime can carry a positive proportion of $\log n$. (ii) *Unbounded exponents*: Theorem 7.3 needs $v_q(k)\le A$ uniformly to bound $\omega(X)$, and $\delta_A\to0$ as $A\to\infty$, so the argument degrades. Removing (ii) is the substantive obstacle; note that a bounded-exponent reduction, if available, would make (ii) the whole game.

What I would stress is the change of character. Proposition 4 says the *counting* is hopeless; Theorem 7.3 says the extremal configurations for that counting **do not occur at all**. The majorants are not merely lossy — they are supported off the fiber.

---

## 8. Summary of claims

| # | Claim | Status |
|---|---|---|
| Lemma 1 | Order-Descent Lemma; $t=2\Rightarrow(q,Q)=(2,3)$ | **proved** (verified on all 146 reduced collisions) |
| Cor. 1.1 | $h$ injective on squarefree integers | **proved** (new proof; result due to [NP23]) |
| Cor. 1.2 | $Q\ge5$ forces a squarefull part $>Q^{2/3}$ (exponent $t$, **not** $3$) | **proved** |
| Thm. 2 | $f(n)\le n^{(c_0+o(1))/\log\log n}$, $c_0=0.3632703\ldots<\log3/3$ | **proved**; $c_0$ sharp for this majorant |
| Thm. 3 | $h$ injective on $\gcd(\cdot,M)=1$ $\Rightarrow f(n)\le\prod_{p\mid M}(v_p(n)+1)$ | **proved** |
| Prop. 4 | barrier: $F(n)\ge n^{(\log2/4+o(1))/\log\log n}$ for suitable $n$, so no majorant through $F$ can succeed | **proved** |
| Prop. 5 | exact collisions coprime to $6$, $30$, $210$ | **verified** (certificates from parallel work, checked exactly here) |
| Prop. 5$'$, 5$''$ | exact collisions coprime to $2310$ and to $9699690$ | **proved here** (found by integer programming, verified exactly) |
| Prop. 6 | $\log f(n)\ll\pi(\rho(n))\log\log n$ — the roughness reformulation | **proved** |
| §4 | census to $n\le10^{18}$; no coprime-to-6 collision for $n\le1.44\cdot10^{20}$ | **computation** |
| — | $\rho(x)=o(\log x/\log\log x)$ | **open**; would give Erdős's first form. Six certificates suggest $\rho\asymp\log x/\log\log x$ instead, i.e. the route returns nothing |
| Lem. 7.1, 7.2 | parity bound $|O|\le v_2(n)+1$; even exponents force $r\equiv1\ (t)$, $t$ odd | **proved** (verified on 1051 cases) |
| Thm. 7.3 | bounded exponents $+$ many odd-exponent primes in $\mathcal G_A$ $\Rightarrow f(n)=0$ | **proved** (verified on 7219 fibers) |
| Cor. 7.4 | $f(\prod_{p\le y}p^3)=0$ — the majorant's extremal point has empty fiber | **proved**; verified exhaustively for $y\le29$ |
| Thm. 7.5 | $v_p(n)\le3\Rightarrow f(n)\le\exp(O(\log^2P^+(n)))$; gives Erdős's first form when $P^+(n)\le\exp((\log n)^{1/2-\varepsilon})$ | **proved** |
| Problem 1060 | $f(n)\le n^{o(1/\log\log n)}$ for **all** $n$ | **still open** (gaps: unbounded exponents; large $P^+$) |

## References

- [Kom26] S. D. Kominers, *On the number of solutions of $k\sigma(k)=n$*, working note, 2026. https://scottkom.com/assets/articles/Kominers_ksigmak.pdf
- [NP23] P. Noppakaew, P. Pongsriiam, *Product of some polynomials and arithmetic functions*, J. Integer Seq. **26** (2023), Art. 23.9.1.
- [Erd59] P. Erdős, *Remarks on number theory II: Some problems on the $\sigma$ function*, Acta Arith. **5** (1959), 171–177.
- [Guy04] R. K. Guy, *Unsolved Problems in Number Theory*, 3rd ed., Springer, 2004, §B11.
- [Kno73] J. Knopfmacher, *A prime-divisor function*, Proc. Amer. Math. Soc. **40** (1973), 373–377. (Maximal order of $\prod_p v_p(n)$; = A005361.)
- [Wir59] E. Wirsing, Math. Ann. **137** (1959), 316–318. (#$\{n\le x:\sigma(n)/n=\alpha\}\le x^{O(1/\log\log x)}$.)
- OEIS A064987, A327153, A337873, A337875, A212490, A005361.
