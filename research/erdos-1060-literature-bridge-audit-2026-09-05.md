# Literature bridge audit for the fixed-exponent fibers of \(h(k)=k\sigma(k)\)

Date checked: 5 September 2026.

## Verdict

I did not find a published theorem that closes the bounded-exponent (fixed-\(R\)) fiber problem. The closest direct theorem is Yamada's count of prime solutions of
\[
\frac{p^q-1}{p-1}=\prod_{i=1}^s m_i^{e_i},
\]
but its decisive hypothesis is \(q>(16/9)\mathrm e\,s^4\). In the fixed-\(R\) regime, \(q=a+1\le R+1\), whereas \(s=\omega(Y)\) is unbounded, so the theorem applies only for bounded \(s\). The other relevant results are fixed-\(S\), fixed-dimension, fixed-number-of-factors, average-over-a-box, or at best exponential in the rank. None yields the uniform sublinear entropy required in the worst case.

This is not merely a complaint about constants. The quantifiers point in the wrong direction in every currently available result checked below.

## Exact success criterion

Let
\[
F_R(Y)=\#\{k:k\sigma(k)=Y,\ v_p(k)\le R\text{ for every }p\}.
\]
Every such \(k\) divides \(Y\). If \(S=\{p:p\mid Y\}\), \(|S|=s\), and \(Y=\prod_{p\in S}p^{b_p}\), then \(k\) corresponds to a vector \((a_p)_{p\in S}\in\{0,1,\ldots,R\}^S\) satisfying
\[
\prod_{p\in S}p^{a_p}\prod_{p\in S}\left(1+p+\cdots+p^{a_p}\right)=Y. \tag{A}
\]
(The second factor is interpreted as \(1\) when \(a_p=0\).)

Put \(L=\log Y\). The primorial lower bound gives
\[
s=\omega(Y)\le (1+o(1))\frac{L}{\log L}.
\]
Consequently, a theorem uniform in the prime set \(S\) and target valuation vector \((b_p)\), of the form
\[
\#\{(a_p)\in\{0,\ldots,R\}^S:\text{(A) holds}\}
   \le \exp(o_R(s)), \tag{B}
\]
would imply
\[
\log F_R(Y)=o_R(L/\log L).
\]
More generally, it is enough to prove \(\log F_R(Y)=o_R(L/\log L)\) directly; (B) is a clean stronger statement. If the separate reduction from arbitrary exponents to fixed \(R\) has been proved with an \(o(L/\log L)\) loss, then (B) really would finish Erdős 1060. None of the literature below proves (B).

## Same radical and multiplicative ratios: the nearest injectivity route

Noppakaew--Pongsriiam, [*Product of Some Polynomials and Arithmetic Functions*](https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf), J. Integer Sequences 26 (2023), Theorem 12, prove that
\[
n\longmapsto n^a\sigma(n)^b
\]
is injective on the squarefree integers for every positive \(a,b\).  For \(a=b=1\), this is exactly the squarefree lemma used in Gyulev's olympiad proof.  The paper does not prove injectivity on a class of integers having the same radical.  On the contrary, its Questions 27--28 explicitly ask about the number of solutions of \(x\sigma(x)=m\).  I found no primary source establishing fixed-radical injectivity.

There is a short constraint which appears useful but is not an injectivity proof.  Put \(I(t)=\sigma(t)/t\).  If \(\operatorname{rad}(m)=\operatorname{rad}(n)=\prod_{p\in S}p\) and \(m\sigma(m)=n\sigma(n)\), then
\[
\left(\frac mn\right)^2=\frac{I(n)}{I(m)}.
\]
For every exponent \(e\ge1\),
\[
1+\frac1p\le I(p^e)<\frac p{p-1};
\]
hence
\[
\max\!\left(\frac mn,\frac nm\right)^2
 <\prod_{p\in S}\frac{p^2}{p^2-1}<\zeta(2),
\qquad
\max\!\left(\frac mn,\frac nm\right)<1.28256. \tag{C}
\]
This closeness does not force equality: integers supported on a fixed prime set can be arbitrarily close.  Nor is \(n\sigma(n)\) monotone within a radical class; for example,
\[
\operatorname{rad}(432)=\operatorname{rad}(486)=6,
\quad 432\sigma(432)=535680>530712=486\sigma(486).
\]
An exhaustive computation found no fixed-radical collision up to \(5\cdot10^7\), but that is only empirical evidence and cannot be used in a proof.

Even a future proof of fixed-radical injectivity would **not by itself close the Erdős bound**.  Every solution \(k\mid Y\) has one of \(2^{\omega(Y)}\) possible radicals, so that theorem would give only
\[
F_R(Y)\le2^s=\exp((\log2)s),
\]
still exponential rather than \(\exp(o(s))\).  Combining it with Gyulev's bound gives \(F_R(Y)\le\min(2^s,\prod_p v_p(Y))\), which is still exponential at the critical scale: for \(Y=(\prod_{i\le s}p_i)^2\), both displayed bounds equal \(2^s\).

A nearby result about cyclotomic values also stops short.  Madritsch--Ziegler, [*On multiplicatively independent bases in cyclotomic number fields*](https://arxiv.org/abs/1408.3991), Theorem 2.2, originally proved the independence of \(-m+\zeta_d\) and \(-n+\zeta_d\) for fixed \(d\) and \(m>n>C(d)\), with stronger results for special \(d\).  The later theorem of Drungilas--Dubickas, [*Multiplicative dependence of two integers shifted by a root of unity*](https://doi.org/10.1090/proc/14136), Proc. Amer. Math. Soc. 147 (2019), 505--511, settles their conjecture: for positive integers \(m>n\) and \(d\ge3\), the algebraic integers \(m-\zeta_d\) and \(n-\zeta_d\) are multiplicatively independent, except when \((n,d)=(1,6)\).

This still does not imply what is needed.  First, it is pairwise independence, whereas a fiber gives a relation among a growing set of bases; pairwise independence never implies setwise independence.  Indeed Drungilas--Dubickas, [*Multiplicative dependence of shifted algebraic numbers*](https://www.impan.pl/shop/en/publication/transaction/download/product/86849), Colloq. Math. 96 (2003), Theorem 1, show that for every quadratic algebraic \(\alpha\) and every integer cutoff \(t\), the whole set \(\{\alpha+j:j\ge t\}\) has a nontrivial product relation of length at most eight.  Second, the desired rational factors are norms \(\Phi_d(m)=N(m-\zeta_d)\); independence of algebraic elements does not imply independence of their norms.  The loss is real: \(\Phi_3(18)=343=7^3=\Phi_3(2)^3\), although \(18-\zeta_3\) and \(2-\zeta_3\) are multiplicatively independent.  Finally, equation (A) mixes several \(d\)'s and a growing number of prime bases.  None of these papers gives a count, a rank bound, or uniformity in that regime.

Even restricting the bases themselves to primes does not make rational cyclotomic values pairwise independent: \(\Phi_2(3)=4\) and \(\Phi_2(7)=8\), so \(\Phi_2(3)^3=\Phi_2(7)^2\). Thus an argument based on taking norms and assigning an independent generator to every prime base already fails in the lowest cyclotomic degree.

There is also a concrete warning against asserting independence of the normalized local ratios.  Direct factorization gives
\[
451737=3^5\cdot11\cdot13^2,\qquad
1401543=3^4\cdot11^3\cdot13,
\]
and direct evaluation gives
\[
\frac{\sigma(451737)}{451737}
=\frac{799344}{451737}
=\frac{6832}{3861}
=\frac{2480016}{1401543}
=\frac{\sigma(1401543)}{1401543}.
\]
Thus the factors \(I(p^e)=\sigma(p^e)/p^e\), even on one fixed three-prime support, satisfy a nontrivial multiplicative relation.  (This is not an \(n\sigma(n)\) collision.)  Any viable ratio theorem must exploit the additional prime-power factor in \(p^e\sigma(p^e)\) and must prove a quantitative sublinear-entropy statement, not generic multiplicative independence.

## 1. S-unit equations

### Exact results

1. Beukers--Schlickewei, [*The equation \(x+y=1\) in finitely generated groups*](https://dspace.library.uu.nl/bitstream/handle/1874/26372/beukers_07_equation_xplusy.pdf?sequence=1), Acta Arith. 78 (1996), Theorem 1.1: if \(\Gamma\subset(\mathbb C^*)^2\) has rank \(r\), then \(x+y=1\) has at most
   \[
   2^{8r+8}=256^{r+1}
   \]
   solutions in \(\Gamma\).

2. Evertse--Schlickewei--Schmidt, [*Linear equations in variables which lie in a multiplicative group*](https://annals.math.princeton.edu/2002/155-3/p04), Ann. of Math. 155 (2002), Theorem 1.1: for \(\Gamma\subset(K^*)^n\) of rank \(r\), the number of nondegenerate solutions of
   \(a_1x_1+\cdots+a_nx_n=1\) is at most
   \[
   \exp\!\left((6n)^{3n}(r+1)\right).
   \]

3. Amoroso--Viada, [*Small points on subvarieties of a torus*](https://doi.org/10.1215/00127094-2009-056), Duke Math. J. 150 (2009), Theorem 6.2, in the formulation used by Manning--Ostafe--Shparlinski: the nondegenerate count is at most
   \[
   (8n)^{4n^4(n+r+1)}.
   \]

4. Hirata-Kohno--Kawashima--Poels--Washio, [*S-unit equation in two variables and Padé approximations*](https://arxiv.org/abs/2211.14399), Theorem 1.1: for a number field of degree \(m\) and a set of places of cardinality \(s\), \(\lambda x+\mu y=1\) has at most
   \[
   (3.1+5(3.4)^m)45^s
   \]
   solutions. This is a recent sharper binary estimate, but it remains \(\exp(\Theta(s))\).

The local identity
\[
1+p+\cdots+p^a=u,\qquad p,u\in U_S,
\]
is a positive, hence nondegenerate, \(S\)-unit equation. For fixed \(a\le R\), the theorems above give at best \(\exp(C_Rs)\), not \(\exp(o_R(s))\). More importantly, they count local pairs or tuples, while a fiber consists of global choices of one exponent label at every prime. There is no published bounded-loss injection from the global transversals in (A) into the solutions of one fixed-dimensional S-unit equation.

Classical Thue--Mahler gap principles have the same quantitative obstruction. Evertse, [*The number of solutions of the Thue--Mahler equation*](https://eudml.org/doc/153882), J. reine angew. Math. 482 (1997), proves for an irreducible binary form of degree \(n\ge3\) a bound of the shape
\[
2(10^5n)^{t+1}
\]
when the right side is supported on \(t\) prescribed primes. This is uniform in the particular primes but exponential in \(t\), and it concerns one fixed binary form. Splitting a fiber into many such equations cannot reduce this to \(\exp(o(s))\); it incurs an exponential bound before accounting for the growing number of local factors.

### Variable prime sets are the wrong statistic

Shparlinski--Stewart, [*Counting solvable S-unit equations*](https://arxiv.org/abs/2007.15170), define \(N_{a,b,c}(s,H)\) as the number of \(s\)-element prime sets \(S\subset[1,H]\) for which \(au+bv=cw\) has at least one \(S\)-unit solution. Their Theorem 1.1 gives, under its hypotheses, bounds such as
\[
N_{a,b,c}^{\delta}(s,H)\ll_{a,b,c,s,\delta}
H^{s-1}(\log H)^{s+3}(\log\log H)^2.
\]
Their Theorem 1.2 gives stronger bounds when every prime in \(S\) is used. This counts how many supports admit a solution, not how many solutions occur on one adversarially chosen support. All constants may depend on \(s\), so it supplies no maximum-fiber estimate as \(s\to\infty\).

Ostafe--Pomerance--Shparlinski, [*Counting solvable S-unit equations and linear recurrence sequences with zeros*](https://arxiv.org/abs/2503.03985), Theorem 2.1, fixes a number field, a finitely generated group \(\Gamma\), and the number \(k\) of coefficients, and shows that only \(H^{dk-1+o(1)}\) coefficient vectors of height at most \(H\) yield a solvable equation. Again, it counts equations/coefficient vectors for a fixed group, not the number of solutions to one equation, and explicitly fixes the rank and \(k\).

### Lower bounds and the real state of the generic problem

Konyagin--Soundararajan, [*Two S-unit equations with many solutions*](https://arxiv.org/abs/math/0604453), Theorem 1: for every \(\beta<2-\sqrt2\), arbitrarily large sets \(S\) of \(s\) primes have at least \(\exp(s^\beta)\) primitive solutions of \(a+b=c\). Their Theorem 2 constructs \(S\) with at least \(\exp(s^{1/16})\) solutions of \(a+1=c\), and integers \(N\) with
\[
\#\{d:d(d+1)\mid N\}\ge \exp((\log N)^{1/16}).
\]
Ha--Soundararajan, [*Many solutions to the S-unit equation \(a+1=c\)*](https://arxiv.org/abs/1902.07397), Theorem 1, improves the special-equation lower bound to \(\gg\exp(s^{1/4}/\log s)\). They state that no upper bound better than the general exponential estimate is known for this special equation and conjecture a subexponential answer.

These lower bounds do **not** disprove the desired \(\exp(o(s))\) scale; they do show that a polynomial generic S-unit theorem is false. The conjectured generic \(\exp(s^{2/3+\varepsilon})\)-type bound would have the right entropy scale, but it is unproved and, by itself, still needs a bounded-loss injection from (A).

## 2. Direct cyclotomic and sum-of-divisors results

### Yamada: the closest theorem, but opposite parameter regime

Yamada, [*Multiplicative structures of values of the sum-of-divisors function*](https://arxiv.org/abs/math/0512175), Theorem 1.4: with
\(c_7=2^{12}38^2 1500^2\), if the prime \(q\) satisfies
\[
q>\frac{16}{9}\mathrm e\,s^4,
\]
then
\[
\frac{p^q-1}{p-1}=m_1^{e_1}\cdots m_s^{e_s}
\]
has at most
\[
s\left(
\frac{\log c_7+19s\log(s+2)+3\sum_{i=2}^s\log\log m_i}{\log q}+7
\right)
\]
solutions in the prime \(p\) and exponents \(e_i\).

For a local factor \(\sigma(p^a)\), one has \(q=a+1\). Fixed \(R\) means \(q\le R+1\), so Yamada's hypothesis forces
\[
s<\left(\frac{9(R+1)}{16\mathrm e}\right)^{1/4},
\]
a constant depending on \(R\). It therefore says nothing in the hard limit \(s\to\infty\). It also covers only prime \(a+1\), and counts individual bases \(p\), not the exponent-label transversals of an entire fiber. Theorem 1.3 in the same paper gives only
\[
P^+\!\left(\frac{x^q-1}{x-1}\right)>\left(\frac{q-1}{6}-\varepsilon\right)\log\log x,
\]
far too small to force a fresh or unique target prime.

### S-parts of polynomial values

Bugeaud--Evertse--Győry, [*S-parts of values of univariate polynomials, binary forms and decomposable forms at integral points*](https://arxiv.org/abs/1708.08290):

* Theorem 2.1: for a fixed squarefree polynomial \(f\) of degree \(n\ge2\), fixed finite \(S\), and every \(\varepsilon>0\),
  \[
  [f(x)]_S\ll_{f,S,\varepsilon}|f(x)|^{1/n+\varepsilon}.
  \]
  This is ineffective and the constant depends on the whole set \(S\).
* Theorem 2.2: if the splitting field of \(f\) has degree \(d\), \(S=\{p_1,\ldots,p_s\}\), and \(P=\max S\), then
  \[
  [f(x)]_S\le \kappa_2|f(x)|^{1-\kappa_1},\qquad
  \kappa_1=\left(c_1^s\big(P(\log p_1)\cdots(\log p_s)\big)^d\right)^{-1}.
  \]
  Here \(c_1,\kappa_2\) depend only on \(f\). As \(S\) grows, the guaranteed saving \(\kappa_1\) collapses at least exponentially (and generally much faster) in the support parameters; it is much too small to yield an \(o(s)\) entropy bound.
* Theorem 2.3 is a density asymptotic for fixed \(S\) and \(0<\varepsilon<1/n\). Full \(S\)-smoothness corresponds to exponent \(1\), outside that range, and the theorem is not uniform in a growing \(S\).

Thus fixed-\(S\) finiteness cannot be substituted for uniform control when \(S=S(Y)\) grows.

### Primitive divisors do not give private divisors across bases

Bang--Zsigmondy and its extensions (for example Postnikova--Schinzel, [*Primitive divisors of the expression \(a^n-b^n\) in algebraic number fields*](https://www.mathnet.ru/eng/sm3975), and Bilu--Hanrot--Voutier, [*Existence of primitive divisors of Lucas and Lehmer numbers*](https://doi.org/10.1515/crll.2001.080)) ensure, apart from explicit exceptions, a divisor of \(p^d-1\) which is new relative to the earlier exponents for the **same base** \(p\).

That is not a divisor private to the base. Fix \(d\ge2\) and a prime \(q\equiv1\pmod d\). There are \(\varphi(d)\) residue classes of exact multiplicative order \(d\) modulo \(q\). Dirichlet's theorem gives infinitely many prime bases \(p\) in each such class. For every one of them, \(q\mid\Phi_d(p)\), and \(q\) is primitive at exponent \(d\) for that base. Hence the same primitive prime can be shared by infinitely many prime bases. Primitive-divisor theorems provide existence and congruence, not the cross-base injectivity or expansion required by (B).

Likewise, Bugeaud--Corvaja--Zannier, [*An upper bound for the G.C.D. of \(a^n-1\) and \(b^n-1\)*](https://doi.org/10.1007/s00209-002-0449-z), fix multiplicatively independent bases \(a,b\) and let \(n\to\infty\). Fixed \(R\) is the reverse regime: bounded exponent and many varying bases. Its uniformity does not transfer.

## 3. Multiplicative dependence and polynomial-product energy

### Fixed functions at one argument

Ostafe--Sha--Shparlinski--Zannier, [*On multiplicative dependence of values of rational functions and a generalisation of the Northcott theorem*](https://arxiv.org/abs/1706.05874), Theorem 4.2: under a non-generation hypothesis on a **fixed** vector of rational functions, only finitely many \(\alpha\in K^{\mathrm{ab}}\) give a multiplicatively dependent value vector. This concerns several fixed functions evaluated at one common argument. Equation (A) has a bounded list of cyclotomic functions evaluated at many independent prime bases, with the number of bases growing. Also, the functions \(1+X+\cdots+X^a\) have built-in cyclotomic factorizations. The theorem supplies neither a count nor uniformity in the number of bases.

### Independent arguments: close in form, still an average fixed-dimension result

Young, [*On multiplicatively dependent vectors of polynomial values*](https://arxiv.org/abs/2402.13704), Proposition 1.7: for a fixed \(n\)-tuple \(F=(f_1,\ldots,f_n)\) of rational functions and a finite height-bounded set \(T\),
\[
N_F(T^m)\ll |T|^{mn-1}(\log H)^{n^2-1}.
\]
Theorem 1.8 gives stronger power savings for suitable degree-\(\ge3\) polynomials. But \(n\) and \(F\) are fixed, all implied constants depend on them, and the result averages over all argument tuples in a height box. In (A), \(n\asymp s\), the arguments are the fixed adversarial prime set \(S\), and the objects being counted are labels \(a_p\in\{0,\ldots,R\}\), not argument tuples. Even formally putting \(n=s\) makes the displayed logarithmic loss \((\log H)^{s^2-1}\), already far beyond \(\exp(o(s))\), before the nonuniform implied constant is considered.

Afifurrahman--Iverson--Sanjaya, [*Multiplicatively dependent integer vectors on a hyperplane*](https://arxiv.org/abs/2510.10855), published in J. London Math. Soc. 114 (2026), Theorem 1.1, obtains asymptotics of order \(H^{n-2}\) for multiplicatively dependent integer vectors of height \(H\) on a fixed hyperplane (subject to stated cases), with \(n\) fixed. Corollary 4.3 has constants depending on \(n\) and multiplicative rank. This is an average lattice-point theorem in fixed dimension. Applied to \(1+p+\cdots+p^a-u=0\), its ambient count is vastly larger than the \(s\) allowed bases and gives no per-support or transversal bound.

### Equal products of polynomial values

Wang--Xu, [*Paucity phenomena for polynomial products*](https://arxiv.org/abs/2211.02908), Theorem 1.1: for a fixed polynomial \(P\) of degree at least two with at least two distinct roots and fixed \(k\),
\[
A_{P,2k}([N])=k!N^k+O_{P,k,\varepsilon}\left(N^{k-1/(6e_P)+\varepsilon}\right),
\]
where \(e_P\) is the largest root multiplicity. This is a strong interval-average energy theorem, but the number of factors \(k\) is fixed and the error constant is allowed to depend on \(k\). A fiber can involve \(k\asymp s\), and the bases form an arbitrary sparse prime set rather than the full interval. The main term itself is not a useful maximum-fiber bound in this regime. Mixed polynomials \(1+X+\cdots+X^a\) require another uncontrolled grouping by labels.

Manning--Ostafe--Shparlinski, [*Counting matrices over finite rank multiplicative groups*](https://arxiv.org/abs/2502.07100), fixes the matrix dimensions and the group rank. Its linear-equation input has constants depending on both, and its matrix counts save powers of the cardinality of a finite subset. It does not count a product fiber or provide growing-rank uniformity.

## 4. Sigma chains and divisor graphs

Bibby--Vyncke--Zelinsky, [*On the third largest prime divisor of an odd perfect number*](https://arxiv.org/abs/1908.09420), define a \(\sigma_{m,n}\)-pair by
\(q\mid\sigma(p^m)\) and \(p\mid\sigma(q^n)\). Their Lemma 4 excludes odd \(\sigma_{1,2}\)-pairs. Their Lemma 5 classifies positive-integer \(\sigma_{2,2}\) quasisolutions by
\[
5pq=p^2+q^2+p+q+1
\]
and a recurrence; actual prime pairs include \((3,13)\), \((13,61)\), and a pair of size about \(10^{13}\)-\(10^{14}\). The paper explicitly leaves further \(\sigma_{2,2}\) behavior and higher-exponent analogues open; for exponent \(4\), several distinct chains already occur.

The longer-cycle content is also local rather than structural.  Lemma 6 excludes only the asymmetric two-vertex motif
\(p^2\mid q^2+q+1\), \(q\mid p^2+p+1\).  Lemma 7 excludes one particular three-vertex configuration with
\(pr\mid q^2+q+1\), \(q\mid p^2+p+1\), \(p\mid r+1\), and \(r\equiv1\pmod4\).  Lemma 8 shows that overlapping \(\sigma_{2,2}\)-pairs must use \(\{3,13,61\}\).  None of these statements bounds arbitrary directed cycles of length at least three, the number of disjoint cycle atoms, or the size of a feedback vertex set.

Yamada, [*On a problem of De Koninck*](https://arxiv.org/abs/1906.10001), builds a directed multigraph with an arc \(p\to q\) when \(q\mid\sigma(p^e)\), and obtains short-chain conclusions under the very special identity \(\sigma(n)=\operatorname{rad}(n)^2\). The decisive inequalities use that exact abundance identity and the corresponding exponent/parity restrictions. They are absent for the arbitrary target \(Y=k\sigma(k)\).

Thus sigma-chain literature gives useful local congruences and classifications of a few two-cycles, but no uniform feedback-vertex, expansion, or entropy theorem for an arbitrary bounded-exponent divisor-sum graph. Restrictions derived from \(\sigma(N)=2N\) or \(\sigma(n)=\operatorname{rad}(n)^2\) cannot be imported into a fiber of an arbitrary \(Y\).

In particular, none of the checked sigma-chain or Thue--Mahler papers proves a height lower bound \(\log Y\ge c_R\ell^2\) for a directed cycle of length \(\ell\), or sparsity of support-disjoint minimal relation atoms. Yamada's condition \(q>(16/9)\mathrm e\,s^4\) cannot be inverted to obtain such a result when \(q\le R+1\); the fixed-\(S\) Thue--Mahler constants are already exponential in \(|S|\). Establishing either assertion would therefore be a genuinely new theorem rather than an application of the cited gap principles.

## 5. Containers, sunflowers, and multiplicative relation hypergraphs

Saxton--Thomason, [*Hypergraph containers*](https://www.repository.cam.ac.uk/bitstream/1810/246494/1/containers.pdf), Corollary 3.6, requires an \(r\)-uniform hypergraph and a small co-degree function \(\delta(G,\tau)\); it then gives at most
\[
\exp\big(c(r)\log(1/\varepsilon)n\tau\log(1/\tau)\big)
\]
containers, with an admissible explicit \(c(r)=800(r!)^3r\). Balogh--Samotij, [*An efficient container lemma*](https://www.math.tau.ac.il/~samotij/papers/efficient-containers-revised.pdf), improves dependence on large uniformity but still assumes strong inequalities of the form
\[
\Delta_t(H)\le K\left(\frac{q}{10^6r^5}\right)^{t-1}\frac{e(H)}{v(H)}
\]
for every codegree level \(t\).

There are three independent failures here:

1. A fiber of (A) is a set of exact zero-sum valuation transversals, not an independent set for an evident hereditary forbidden-configuration property.
2. Minimal multiplicative relations need not have bounded support merely because all local exponents are bounded, so the uniformity parameter is uncontrolled.
3. No codegree or supersaturation estimate is known for the arithmetic relation hypergraph. Repeated small target primes create hubs, while disjoint/sparse relation atoms destroy uniform spread. Proving the required codegree inequalities would itself contain essentially the missing arithmetic theorem.

This is consistent with Liu--Pach, [*The number of multiplicative Sidon sets of integers*](https://arxiv.org/abs/1808.06182), who explicitly note that the multiplicative collision graph is highly irregular and therefore difficult for hypergraph containers; their enumeration uses different methods and remains exponential in \(\pi(n)\).

The improved sunflower lemma of Alweiss--Lovett--Wu--Zhang, [Ann. of Math. 194 (2021)](https://annals.math.princeton.edu/2021/194-3/p05), gives roughly \((\log w)^w\) thresholds for fixed petal number in a \(w\)-uniform family. Here relation support \(w\) is unbounded, and extracting a sunflower only produces disjoint residual relations; it does not make those residual relations impossible. Hence it gives no \(o(s)\) transversal count.

## What would genuinely bridge the gap

A usable new theorem must be tailored to **bounded labels on a growing, adversarial prime support**, for example:

> For every fixed \(R\), uniformly over finite prime sets \(S\), nonnegative target vectors \(b\in\mathbb Z_{\ge 0}^{S}\), and all auxiliary primes occurring in the cyclotomic factors, the number of label transversals \(a\in\{0,\ldots,R\}^{S}\) satisfying the complete valuation system associated with (A) is \(\exp(o_R(|S|))\).

An equivalent route would be a structural theorem showing that, after deleting \(o_R(s)\) primes, all remaining exponent labels are forced. Such a statement would make the fiber at most
\((R+1)^{o(s)}=\exp(o_R(s))\). Existing primitive-divisor, S-unit, sigma-chain, and container theorems do not prove that deletion statement.

## Bottom line

The literature audit produces no valid published bridge. The exact obstruction is a missing uniform growing-rank/growing-support theorem, not a missing citation to a standard S-unit or container result. Therefore a submission-ready proof may cite these works as motivation or partial tools, but it cannot assert the fixed-\(R\) step unless that new transversal theorem is proved independently.
