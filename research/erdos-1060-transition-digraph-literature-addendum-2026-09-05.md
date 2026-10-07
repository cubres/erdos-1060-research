# Erdős 1060: transition-digraph literature addendum

**Date:** 5 September 2026  
**Scope:** primary-source audit for a theorem that would turn the bounded-exponent valuation system for
\(h(k)=k\sigma(k)\) into
\[
\log f(n)=o\!\left(\frac{\log n}{\log\log n}\right).
\]

## 1. Exact target and exact graph-theoretic bridge

Fix an exponent cap \(R\), a value \(N\), and a family \(\mathcal F\) of solutions of
\(k\sigma(k)=N\) whose prime exponents are in \(\{0,1,\ldots,R\}\). Let \(S\) be the union of their prime supports and write
\(a_p=v_p(k)\). For each \(p\in S\), the valuation equation is
\[
v_p(N)=a_p+\sum_{q\in S}v_p\!\left(\sigma(q^{a_q})\right).
\tag{1}
\]
Define the **fiber interaction digraph** \(D_{\mathcal F}\) on \(S\) by putting
\(q\to p\) when
\[
a\longmapsto v_p(\sigma(q^a))
\]
is nonconstant on the exponent values actually occurring at \(q\) in \(\mathcal F\).

If \(T\) is a directed feedback vertex set of \(D_{\mathcal F}\), then restriction to the coordinates in \(T\) is injective on \(\mathcal F\). Indeed, topologically order \(S\setminus T\). In (1), all genuinely variable coordinates affecting \(a_p\) have already been recovered, while every missing arc represents a term constant on the fiber. Thus \(a_p\) is recovered successively. Consequently,
\[
|\mathcal F|\le \prod_{p\in T}|A_p|\le (R+1)^{|T|},
\tag{2}
\]
where \(A_p=\{v_p(k):k\in\mathcal F\}\).

This is precisely the classical finite-dynamical-system feedback bound. Gadouleau--Richard--Riis define the guessing number \(g(D,s)\) and give
\(g(D,s)\le k^+(D)\), where \(k^+\) is a minimum transversal of nonnegative directed cycles. In an unsigned dependency graph all cycles count, so this is
\(|\operatorname{Fix}F|\le s^{\tau(D)}\). See their equation (1):

- Maximilien Gadouleau, Adrien Richard and Søren Riis, “Fixed points of Boolean networks, guessing graphs, and coding theory,” *SIAM J. Discrete Math.* 29 (2015), 2312--2335. [DOI](https://doi.org/10.1137/140988358), [arXiv](https://arxiv.org/abs/1409.6144).
- Søren Riis, “Information flows, graphs and their guessing numbers,” *Electronic J. Combin.* 14 (2007), R44. [DOI](https://doi.org/10.37236/962), [journal page](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v14i1r44).

Therefore a sufficient missing arithmetic statement is
\[
\tau(D_{\mathcal F})=o_R\!\left(\frac{\log N}{\log\log N}\right)
\quad\text{uniformly in every bounded-exponent fiber }\mathcal F.
\tag{3}
\]
The literature below does not prove (3).

## 2. Stronger signed and state-local feedback theorems do not remove (3)

Aracena's Theorem 9 applies to a **regulatory/unate Boolean network**: every essential influence has one globally consistent sign. If \(P\) meets every positive directed circuit, then restriction of fixed points to \(P\) is injective and
\(|\operatorname{Fix}F|\le2^{|P|}\). See Julio Aracena, “Maximum number of fixed points in regulatory Boolean networks,” *Bull. Math. Biol.* 70 (2008), 1398--1409: [DOI](https://doi.org/10.1007/s11538-008-9304-7), [PubMed](https://pubmed.ncbi.nlm.nih.gov/18306974/).

Richard proves a genuinely stronger local theorem for maps on products of finite integer intervals. His Theorem 3 says: if **one common set** \(I\) meets every positive circuit of every discrete-derivative local graph \(\mathbf G_F(x,v)\), then
\[
|\operatorname{Fix}F|\le\prod_{i\in I}|X_i|.
\]
His Theorem 5 uses smaller threshold-local graphs and bounds even the number of asynchronous attractors by
\(\prod_{i\in I}(|T_i|+1)\). Crucially, one needs a single transversal valid for all states; a different small transversal at each state is insufficient. See Adrien Richard, “Positive circuits and maximal number of fixed points in discrete dynamical systems,” *Discrete Appl. Math.* 157 (2009), 3281--3288: [DOI](https://doi.org/10.1016/j.dam.2009.06.017), [full text](https://arxiv.org/html/0807.4229).

The valuation functions are not unate. For example,
\[
v_3(\sigma(2^a))=0,1,0,1\qquad(a=0,1,2,3).
\]
Thus the same influence both rises and falls. In the signed conventions of Gadouleau--Richard--Riis it must receive the unconstrained label \(0\), and a cycle containing such an arc is nonnegative. The signed theorem then gives no automatic improvement over the ordinary feedback set.

Nor can bounded coordinate degree, bounded in/out-degree, sparsity, or fixed signs imply a sublinear transversal. On \(2m\) variables over an \(s\)-letter alphabet, set
\[
F_{2j-1}(x)=x_{2j},\qquad F_{2j}(x)=x_{2j-1}\quad(1\le j\le m).
\]
The coordinate maps have degree one, all arcs are positive, maximum in/out-degree is one, and there are only \(2m\) arcs. Yet the graph is a disjoint union of \(m\) positive 2-cycles,
\[
\tau=\tau^+=m,\qquad |\operatorname{Fix}F|=s^m.
\]
So the feedback exponent is attained exactly. Any improvement has to use special arithmetic information, not generic finite-dynamical-system structure.

The directed Erdős--Pósa theorem has the same limitation. Reed--Robertson--Seymour--Thomas prove that for every \(r\), a digraph either contains \(r\) vertex-disjoint directed circuits or has a bounded-size directed feedback vertex set. It supplies a function of the packing number, not a sublinear bound in the number of vertices; disjoint unions of cycles show why none is possible. See “Packing directed circuits,” *Combinatorica* 16 (1996), 535--554: [DOI](https://doi.org/10.1007/BF01271272), [author PDF](https://thomas.math.gatech.edu/PAP/younger.pdf). To use it here one would first need a new arithmetic proof that the fiber graph has only \(o_R(\log N/\log\log N)\) vertex-disjoint cycles, with sufficiently quantitative control.

## 3. Mills and the sum-of-divisors graph: exact reach and exact stopping point

Mills studies
\[
x\mid y^2+ay+1,\qquad y\mid x^2+ax+1
\tag{4}
\]
for fixed integer \(a\). His Theorem 1 gives at most \(8(2|a|+3)^2\) chains when \(a\ne\pm2\); Theorem 2 puts every chain in a second-order linear recurrence; and Theorem 3 says that the positive solutions for \(a=1\) are precisely consecutive terms of
\[
1,1,3,13,61,291,\ldots,
\qquad u_{j+2}=5u_{j+1}-u_j-1.
\]
See W. H. Mills, “A System of Quadratic Diophantine Equations,” *Pacific J. Math.* 3 (1953), 209--220: [primary PDF](https://msp.org/pjm/1953/3-1/pjm-v3-n1-p15-p.pdf).

This is exactly the exponent-two mutual divisibility relation
\(p\mid\sigma(q^2)\), \(q\mid\sigma(p^2)\), hence a classification of the relevant **2-cycle** quasisolutions. It says nothing about a directed circuit of length at least three, about mixed exponents, or about a common transversal for many circuits.

Bibby--Vyncke--Zelinsky make the graph interpretation explicit. Their Lemma 5 gives the same quasichain and \(4t_j<t_{j+1}<5t_j\) for \(j>3\). Lemmas 6--8 exclude certain weighted or overlapping \(\sigma_{2,2}\) motifs; in particular two overlapping \(\sigma_{2,2}\) prime pairs force \(\{3,13,61\}\). But they do not classify arbitrary directed cycles. They explicitly leave open even whether infinitely many \(\sigma_{2,2}\) prime pairs exist. See Sean Bibby, Pieter Vyncke and Joshua Zelinsky, “On the Third Largest Prime Divisor of an Odd Perfect Number,” *INTEGERS* 21 (2021), A115: [arXiv/full text](https://arxiv.org/html/1908.09420), [journal PDF](https://math.colgate.edu/~integers/v115/v115.pdf), [DOI record](https://doi.org/10.5281/zenodo.10842315).

Factor-chain arguments for odd perfect numbers assume the global identity \(\sigma(M)=2M\) and branch inside the prime support of one hypothetical perfect number. Those hypotheses are absent from a general fiber of \(k\sigma(k)\); the cited papers do not contain an arbitrary-cycle or feedback-transversal theorem.

## 4. Pratt trees and primitive divisors do not control these cycles

Ford--Konyagin--Luca define a Pratt chain by
\(p_1\prec p_2\prec\cdots\prec p_r\), meaning \(p_{j+1}\equiv1\pmod{p_j}\), and obtain distributional bounds for its height and for counts of primes with a given height. See Kevin Ford, Sergei Konyagin and Florian Luca, “Prime chains and Pratt trees”: [arXiv](https://arxiv.org/abs/0904.0473), [author PDF](https://www.ford126.web.illinois.edu/wwwpapers/chains.pdf).

An edge in the present graph instead gives \(p\mid\Phi_d(q)\) for some \(d\mid e+1\) (apart from the usual primes dividing \(d\)). It implies \(\operatorname{ord}_p(q)=d\) and hence \(d\mid p-1\), not \(q\mid p-1\). The base prime and divisor prime can occur in either size order. Thus these edges do not embed into Pratt chains, and “almost all primes” height statements cannot control an adversarial fiber.

Likewise, Zsigmondy-type primitive divisor theorems are local in one base: a primitive divisor of \(q^d-1\) is new relative to smaller powers of that same \(q\). It is not private relative to other bases. Indeed, for any prime \(r\equiv1\pmod d\), choose a residue of exact order \(d\) modulo \(r\); Dirichlet's theorem gives infinitely many prime bases \(q\) in that residue class, all satisfying \(r\mid\Phi_d(q)\). Primitive divisors therefore do not by themselves give support-disjoint atoms or a sublinear cycle transversal.

## 5. Cyclotomic multiplicative dependence: the closest positive and negative results

### 5.1 Pairwise independence is not setwise independence

Drungilas--Dubickas prove that for positive integers \(m>n\) and \(d\ge3\), the algebraic numbers \(m-\zeta_d\) and \(n-\zeta_d\) are multiplicatively independent, except when \((n,d)=(1,6)\). See “Multiplicative dependence of two integers shifted by a root of unity,” *Proc. Amer. Math. Soc.* 147 (2019), 505--511: [DOI](https://doi.org/10.1090/proc/14136), [JSTOR record](https://www.jstor.org/stable/e26562814).

This controls only pairs. Their earlier theorem points in the opposite direction for larger sets: for every quadratic algebraic \(\alpha\) and every integer threshold \(t\), \(\alpha\) is \(\mathbb Z_t\)-dependent with a relation of total length at most eight. See Paulius Drungilas and Artūras Dubickas, “Multiplicative dependence of shifted algebraic numbers,” *Colloq. Math.* 96 (2003), 75--81, Theorem 1: [DOI](https://doi.org/10.4064/cm96-1-7), [primary PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/86849).

Taking \(\alpha=-\zeta_3\) and norms produces nontrivial identities
\[
\prod_i\Phi_3(x_i)=\prod_j\Phi_3(y_j),\qquad x_i,y_j\ge t,
\]
of total length at most eight for arbitrarily large integer arguments. Therefore a blanket setwise-independence claim for fixed-degree cyclotomic values is false. The theorem does **not** require or guarantee that the arguments \(x_i,y_j\) are prime; imposing simultaneous primality on its polynomially related parameters is far beyond its proof. Hence it is negative evidence for an unrestricted polynomial-value route, not a counterexample to the prime-argument statement needed here.

### 5.2 Fixed-tuple theorems have the wrong quantifiers

Ostafe--Sha--Shparlinski--Zannier, Theorem 4.2, fix a tuple
\(\boldsymbol\varphi=(\varphi_1,\ldots,\varphi_s)\in K(X)^s\). If its components cannot multiplicatively generate a power of a linear fractional function, then only finitely many common arguments \(\alpha\in K^{\rm ab}\) make \(\boldsymbol\varphi(\alpha)\) multiplicatively dependent. Their Lemma 2.1 bounds relation exponents by a constant depending on the entire fixed tuple. See [Theorem 4.2 and Lemma 2.1](https://arxiv.org/html/1706.05874).

Our factors have many distinct prime arguments \(q_i\), and the number of factors grows with \(\omega(N)\). There is no common argument and no uniform dependence on the growing tuple dimension. This theorem cannot give \(\exp(o(s))\) multiplicity.

### 5.3 Product-paucity theorems are fixed-length average results

Wang--Xu prove the strongest directly neighboring statement found. If \(P\in\mathbb Z[X]\) has degree \(d\ge2\), at least two distinct complex roots, and maximum root multiplicity \(e_P\), then for fixed \(k\)
\[
A_{P,2k}([X])=k!X^k+O_{P,k,\varepsilon}
 \left(X^{k-1/(6e_P)+\varepsilon}\right),
\]
where \(A_{P,2k}\) counts solutions of
\(\prod_{i=1}^kP(x_i)=\prod_{j=1}^kP(y_j)\). See Victor Y. Wang and Max Wenqiang Xu, “Paucity phenomena for polynomial products,” *Bull. Lond. Math. Soc.* 56 (2024), 2718--2726: [arXiv](https://arxiv.org/abs/2211.02908), [DOI](https://doi.org/10.1112/blms.13095).

Heap--Sahay--Wooley similarly prove, for a fixed factor count \(k\) and irrational \(\theta\), that products of \(x_i+\theta\) are almost always represented only by permutations. For algebraic \(\theta\) of degree \(2\le d<k\), their Theorem 1.2 gives
\[
\sum_\nu\tau_k(\nu;X,\theta)^2
=T_k(X)+O_{k,\theta,\varepsilon}(X^{k-d+1+\varepsilon}).
\]
See Winston Heap, Anurag Sahay and Trevor Wooley, “A paucity problem associated with a shifted integer analogue of the divisor function”: [arXiv](https://arxiv.org/abs/2108.00287), [author PDF](https://www.math.purdue.edu/~twooley/publ/20210731shiftdiv.pdf).

Neither result is a maximum-fiber theorem. Both average over all arguments in a box, keep \(k\) fixed as \(X\to\infty\), and allow constants depending on \(k\). Erdős 1060 requires an adversarial value \(N\), mixed polynomials
\[
H_e(X)=X^e(1+X+\cdots+X^e),\qquad 0\le e\le R,
\]
prime arguments, and a number of factors growing like the support size. Even a uniform energy asymptotic would not by itself rule out one exceptional large fiber without a sufficiently strong maximum-multiplicity conversion. These theorems do not yield (3).

The older arithmetic-progression product theorem of Saradha--Shorey--Tijdeman is also too rigid: it treats two consecutive arithmetic-progression blocks of values of one fixed polynomial, with fixed steps and fixed length ratio. See “On values of a polynomial at arithmetic progressions with equal products,” *Acta Arith.* 72 (1995), 67--76: [DOI](https://doi.org/10.4064/aa-72-1-67-76), [primary record](https://eudml.org/doc/206785) (and the authors' [1998 correction](https://eudml.org/doc/207150)). Arbitrary prime arguments and mixed cyclotomic factors do not satisfy its hypotheses.

## 6. Smooth cyclotomic values and S-unit equations: quantitative failure

Yamada considers exactly
\[
\Phi_q(p)=\frac{p^q-1}{p-1}=m_1^{e_1}\cdots m_s^{e_s},
\]
with \(p,q\) prime and fixed allowed prime bases \(m_i\). His Theorem 1.4, with
\(c_7=2^{12}38^2 1500^2\), assumes
\[
q>\frac{16}{9}e\,s^4
\]
and then bounds the number of solutions by
\[
s\left(
\frac{\log c_7+19s\log(s+2)+3\sum_{i=2}^s\log\log m_i}{\log q}+7
\right).
\]
See Tomohiro Yamada, “Multiplicative structures of values of the sum-of-divisors function”: [arXiv](https://arxiv.org/abs/math/0512175), especially Theorem 1.4.

For bounded exponent \(R\), the cyclotomic index \(q\le R+1\) is fixed while the support size \(s\) grows. The displayed hypothesis then fails once \(s\) is larger than a constant depending on \(R\). The proof's Lemma 7.2 only gives
\[
\log p_2>\frac{3(q-1)^2}{4qs^2}\log p_1;
\]
its multiplier tends to zero with \(s\), so it is not a hidden large-support gap principle.

General S-unit bounds also have the wrong scale. Evertse--Schlickewei--Schmidt show that the number of nondegenerate solutions of
\(a_1x_1+\cdots+a_mx_m=1\) in a rank-\(r\) subgroup is at most
\[
\exp\!\left((6m)^{3m}(r+1)\right).
\]
See “Linear equations in variables which lie in a multiplicative group,” *Ann. Math.* 155 (2002), 807--836: [journal/DOI](https://annals.math.princeton.edu/2002/155-3/p04), [arXiv](https://arxiv.org/abs/math/0409604). With fixed equation length this is \(\exp(Cr)\), not \(\exp(o(r))\); if the equation length grows, the dependence is much worse. The sharper two-variable Beukers--Schlickewei bound \(2^{8r+8}\) is still exponential in rank.

This is not merely a loose technical neighborhood: large specially chosen sets of \(s\) primes can support many solutions of \(a+1=c\). Konyagin--Soundararajan obtain more than \(\exp(s^{1/16})\), and Ha--Soundararajan improve this to
\(\gg\exp(s^{1/4}/\log s)\). See [Konyagin--Soundararajan](https://arxiv.org/abs/math/0604453) and [Ha--Soundararajan](https://arxiv.org/abs/1902.07397). These lower bounds are compatible with \(\exp(o(s))\), but they underline that a uniform subexponential rank theorem would be a substantial new result, not an immediate corollary of existing S-unit technology.

## 7. Same-radical injectivity does not supply the missing estimate

No primary source was found proving that \(n\mapsto n\sigma(n)\) is injective on every fixed radical (same prime support). Noppakaew--Pongsriiam prove only squarefree injectivity in Theorem 12 and then explicitly ask in Questions 27--28 about fiber sizes of \(x\sigma(x)\). See “Product of Some Polynomials and Arithmetic Functions,” *J. Integer Sequences* 26 (2023), Article 23.9.1: [primary PDF](https://cs.uwaterloo.ca/journals/JIS/VOL26/Pongsriiam/pong43.pdf).

Even if fixed-radical injectivity were proved, it would give at best one solution per support, hence \(2^{\omega(N)}\) possibilities. Since the extremal size of \(\omega(N)\) is of order \(\log N/\log\log N\), this only recovers
\[
\log f(N)=O\!\left(\frac{\log N}{\log\log N}\right),
\]
not the required little-\(o\). It could be a useful structural lemma, but it is not by itself the missing theorem.

## 8. Bottom line

The literature supplies an exact and rigorous bridge:
\[
|\mathcal F|\le(R+1)^{\tau(D_{\mathcal F})},
\]
and even signed/state-local variants. It does **not** supply the necessary arithmetic estimate
\(\tau(D_{\mathcal F})=o_R(\log N/\log\log N)\), a comparable bound on vertex-disjoint arithmetic cycles, or a uniform maximum-fiber theorem for growing products of cyclotomic values at prime arguments.

The most useful exact reductions and warnings are:

1. Mills and Bibby--Vyncke--Zelinsky rigorously control exponent-two 2-cycles and a few overlapping motifs, but not arbitrary circuits.
2. Drungilas--Dubickas pairwise independence cannot be promoted to setwise independence; their 2003 theorem actually creates bounded-length product relations among arbitrarily large quadratic/cyclotomic values at unrestricted integer arguments.
3. Wang--Xu and Heap--Sahay--Wooley prove strong fixed-length average paucity, not a growing-length adversarial maximum-fiber bound.
4. Yamada's exact smooth-repunit theorem requires cyclotomic index \(q\gg s^4\), the reverse of the fixed-\(R\), growing-support regime.
5. Generic feedback, directed Erdős--Pósa, primitive-divisor, Pratt-tree, and S-unit theorems all need an additional arithmetic global input.

Accordingly, none of these sources completes Erdős Problem 1060. A proof claiming completion through this route must independently establish (3), or replace it with a quantitatively equivalent global multiplicative-relation theorem. As of this audit, the problem is still listed **OPEN** at [Erdős Problems #1060](https://www.erdosproblems.com/1060).
