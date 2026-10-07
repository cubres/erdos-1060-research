Erdős Problem 1060 Research Note

Status Improved Uniform Bound Independent Referee Check and Exact Remaining Gap

Prepared for mathematical review5 September 2026

Executive conclusion

Erdős Problem 1060 is still open. As of 5 September 2026, the problem page continues to label it OPEN, and neither the sources examined here nor the arguments developed in this investigation prove

$\log f(n)=o\!\left(\frac{\log n}{\log\log n}\right),
\qquad
f(n)=\#\{k\ge 1:k\sigma(k)=n\}.$

It would therefore be mathematically incorrect to submit a claimed complete solution.

The investigation did produce several rigorous results that are suitable for circulation as partial progress. The strongest one comes from the peer manuscript supplied on 5 September 2026.

1. A divisibility-comparability obstruction, followed by a random-chain packing argument, gives

$f(n)\le
\exp\!\left((C_1+o(1))\frac{\log n}{\log\log n}\right),$

where

$C_1=\frac12\log\!\left(1+\frac1{\sqrt2}\right)
=0.267399998369785\ldots.$

For cubefree preimages the coefficient improves further to $\frac12\log\varphi=0.240605912529801\ldots$, where $\varphi=(1+\sqrt5)/2$. Every step and edge case of this argument has been independently checked. It strictly improves the coefficients in the supplied Gyulev solution, Kominers's 2026 working paper, and the Rankin refinement below. It is still a positive constant and therefore does not prove the conjecture.

2. Within the broad framework of coordinatewise independent random divisibility chains with an affine lower bound for the state marginals, the constant $C_1$ is optimal. Thus no retuning of that packing distribution, using only the two aggregate exponent budgets in the proof, can make the coefficient tend to zero.

The still broader majorant which counts every powerful $d$ with $h(d)\mid n$ also has values of size

$\exp\!\left(\left(\frac{\log2}{4}+o(1)\right)
\frac{\log n}{\log\log n}\right).$

Therefore a proof must use the exact solvability of the squarefree remainder, not merely count admissible powerful parts more carefully.

3. A natural route to the conjectured polylogarithmic bound is false. The map $k\mapsto k\sigma(k)$ is not injective even on cubefree integers coprime to $210$. Several independently checked collisions are given below, including a conformally indecomposable cubefree certificate.

4. For every fixed $R$, the original problem reduces to bounding fibers on $R$-free integers. A predecessor-graph lemma and a reciprocal-mass projection criterion give genuine, though insufficient, restrictions on such fibers. They identify the remaining obstruction as uniform control of the incomparable exponent transitions in the complete valuation system.

5. The comparable-index lemma admits an exact gcd-normalized extension. For a general collision it produces a rational square $(c/C)^2$, where the denominator $C$ measures precisely the failure of divisibility comparability. The identity $h(315)=h(351)$ gives $C=9$ and $c=16$, so the tempting assertion $C\mid c$ is false.

6. A state-dependent transition digraph gives the rigorous injection

$|\mathcal F|\le R^{\tau(D_{\mathcal F})}.$

Every vertex-disjoint directed cycle can be charged to the target, yielding only

$\nu(D_{\mathcal F})\le
\left(\frac13+o(1)\right)\frac{\log N}{\log\log N}.$

Exact cubefree examples have feedback number $2$, and a four-point tensor fiber has feedback number $3$. Another exact atom shows that the coordinates with divisibility-incomparable exponent indices need not be a feedback set. Thus the graph bridge is valid, but the required sublinear feedback or information-separator theorem remains unproved.

7. A second independent route gives an injective rational comparison map $A_3$ for which the residual Euler tail improves from order $p^{-2}$ to order $p^{-3}$. Its generic rational separation is nevertheless too small by a factor of roughly $N$, and a simultaneous clustering lemma rules out closing this gap from injectivity or short-interval sparsity alone. This sharpens the diagnosis of the exponent-two obstruction but does not prove the conjecture.

An exact census of all relevant $k<10^8$ determines every fiber with $n\le10^{16}$. Its maximum is $5$. A separate complete cubefree census in the same target range finds maximum $2$ and shows that every one of its $1{,}494{,}456$ collision fibers reduces to $12\leftrightarrow14$. Much larger exact cubefree certificates prove that this finite rigidity does not persist literally. The accompanying code also verifies the rough-input collisions, the displayed sixfold and sevenfold fibers in Kominers's manuscript, and the variational constant above.

The problem and the evidence standard

Put

$h(k)=k\sigma(k),
\qquad
f(n)=\#h^{-1}(n).$

Erdős Problem 1060 asks whether

$f(n)\le n^{o(1/\log\log n)}
=\exp\!\left(o\!\left(\frac{\log n}{\log\log n}\right)\right),$

and perhaps even whether $f(n)\le(\log n)^{O(1)}$. The current problem page marks the problem open and cites Problem B11 of Guy's collection as its source.

There are three evidence levels in this note.

A theorem has a complete argument in the note.

A finite computational statement has exact source code and a reproducible certificate or exhaustive range.

A literature statement is attributed to its source. In particular, an exhaustive computation asserted in a source is not called independently verified unless its code or an equivalent computation was available.

This distinction matters here. Kominers gives a much larger census than the one performed in this investigation, but the manuscript's code section still contains the placeholder that the archive is being packaged. The individual fibers in that manuscript can be checked exactly; its exhaustive negative assertions cannot yet be reproduced from the posted material.

Literature map

The following sources are directly relevant.

Richard Guy's Unsolved Problems in Number Theory, Problem B11, records collisions, primitive solutions, the Mersenne-prime construction, and the quantitative conjecture attributed to Erdős. The Springer page is the official bibliographic record. No original Erdős paper containing this exact quantitative formulation was located.

Noppakaew and Pongsriiam prove that $n\mapsto n^a\psi(n)^b$ is globally injective and that $n\mapsto n^a\sigma(n)^b$ is injective on squarefree integers for positive $a,b$. Their Theorems 3 and 12 supply the two injective ingredients used below. Questions 27 and 28 ask about fibers and exact multiplicities of $x\sigma(x)$. See the Journal of Integer Sequences article.

The supplied olympiad solution, credited to Nikola Gyulev, proves $f(n)\le\prod_{p\mid n}v_p(n)$ by encoding a preimage through its powerful part. Scott Duke Kominers independently presents the equivalent coloring argument in his July 2026 working paper and derives the coefficient $\log3/3$. The date and publication details of the Bulgarian source should be established before making a priority claim about this bound.

The supplied peer manuscript, Divisibility-chain packing and the multiplicity of k sigma k, proves the coefficient $C_1$ stated above. The proof is reproduced and independently checked below. A bounded web and literature search found no earlier occurrence of its exact comparable-index obstruction, its finite geometric marginal construction, its tensorized application to $h$, or its constant. This is not a priority proof.

Random divisibility-chain measures and chain-packing arguments are not new in general. Alexeev, Barreto, Li, Lichtman, Price, Shah, Tang, and Tao develop a closely related Markov-chain method for primitive sets in Primitive sets and von Mangoldt chains. Stanley's Two Poset Polytopes and Monma, Schrijver, Todd, and Wei's Convex Resource Allocation Problems on Directed Acyclic Graphs provide broader chain-polytope, generalized LYM, and fractional chain-covering context. The bounded search did not locate in these works the arithmetic obstruction proved here.

OEIS A327153 tabulates $f(n)$. OEIS A337873 lists values with collisions, A337875 concerns primitive outputs, and A212490 records the least known values of exact multiplicity. These are valuable computational references, not asymptotic proofs.

Erdős's 1959 paper Remarks on number theory II proves a related squarefree statement for equal abundancy, $\sigma(a)/a=\sigma(b)/b$, and studies fixed-abundancy counts. It does not prove the analogous assertion for $a\sigma(a)=b\sigma(b)$ that Guy B11 and Noppakaew--Pongsriiam attribute to it; that attribution appears to be a propagated miscitation.

Pollack's Remarks on Fibers of the Sum-of-Divisors Function gives strong structure for typical fibers of $\sigma$. It does not give a uniform estimate for $h$, because $h(k)=n$ makes $\sigma(k)=n/k$ vary with $k$.

Gabdullin, Iudelevich, and Luca study values of $kF(k)$ for several arithmetic functions in Numbers of the form kf(k). Their results concern range size for $\tau$, $\omega$, and $\varphi$, not the maximum fiber of $k\sigma(k)$.

Gadouleau, Richard, and Riis give the general fixed-point/feedback-set inequality underlying the transition-digraph lemma in Fixed points of Boolean networks, guessing graphs, and coding theory. Richard's state-local positive-circuit theorem is stronger for suitable signed systems, but the valuation influences here are not unate and still require one common transversal.

Mills classifies the mutual quadratic divisibilities $x\mid y^2+y+1$ and $y\mid x^2+x+1$ in A System of Quadratic Diophantine Equations. Bibby, Vyncke, and Zelinsky develop the same sigma-chain in the odd-perfect-number setting in On the Third Largest Prime Divisor of an Odd Perfect Number. These works control exponent-two 2-cycles and some overlaps, not arbitrary cycles or a sublinear feedback transversal.

General $S$-unit theorems, Yamada's smooth repunit theorem, and Wang and Xu's polynomial-product paucity theorem have the wrong uniformity for this problem: their bounds are exponential in the growing rank, assume cyclotomic index much larger than the support, or keep the number of factors fixed and average over a box. None supplies a worst-case $\exp(o(s))$ bound for a fixed support of $s$ target primes.

The known lower-bound mechanism is also worth recording. If $M_i=2^{p_i}-1$ are $t$ distinct Mersenne primes, set $P=\sum_i p_i$ and

$v_i=2^{p_i-1}\prod_{j\ne i}M_j.$

Then

$h(v_i)=2^{P-1}\prod_{j=1}^tM_j$

for every $i$. The GIMPS list currently has $52$ known Mersenne primes, so this gives an unconditional value with at least $52$ preimages. It does not conflict with either proposed upper bound because the constructed value is enormous.

There is a bibliographic trap here. Guy B11 and Noppakaew--Pongsriiam Question 27 print $v_i=\prod_{j\ne i}M_j$, omitting the factor $2^{p_i-1}$. The printed formula is false already for $M_1=3,M_2=7$; the corrected formula displayed above is the one that makes the calculation valid.

The squarefree and powerful part lemmas

The first proof is included because it corrects two compressed passages in the supplied olympiad text and fixes the notation used later.

Lemma 1 Squarefree injectivity

If $a$ and $b$ are squarefree positive integers and $h(a)=h(b)$, then $a=b$.

Proof

First suppose $a$ and $b$ are coprime. If one is $1$, then both are $1$ because $h(m)>1$ for $m>1$. Otherwise let $P$ be the largest prime divisor of $ab$, and assume $P\mid a$. Since $P\nmid b$ but $P\mid h(b)$, squarefreeness gives

$P\mid\sigma(b)=\prod_{q\mid b}(q+1).$

Thus $P\mid q+1$ for some prime $q\mid b$. We have $q<P$, so $q+1\le P$ and hence $q+1=P$. The only consecutive primes are $2$ and $3$. Therefore the only remaining nontrivial coprime possibility is $\{a,b\}=\{2,3\}$, but $h(2)=6\ne12=h(3)$.

For general squarefree $a,b$, write $d=\gcd(a,b)$, $a=da_1$, and $b=db_1$. The three integers $d,a_1,b_1$ have the required coprimalities, so multiplicativity gives

$h(d)h(a_1)=h(a)=h(b)=h(d)h(b_1).$

The coprime case gives $a_1=b_1=1$, and therefore $a=b$.

Lemma 2 Powerful part injection

Define the powerful part of $k$ by

$F(k)=\prod_{v_p(k)\ge2}p^{v_p(k)}.$

The map $k\mapsto F(k)$ is injective on every fiber of $h$.

Proof

Suppose $h(k)=h(m)$ and $F(k)=F(m)=d$. Write $k=da$ and $m=db$. Then $a$ and $b$ are squarefree and both are coprime to $d$. Multiplicativity gives

$h(d)h(a)=h(k)=h(m)=h(d)h(b).$

Lemma 1 gives $a=b$, and hence $k=m$.

If $n=\prod p^{\alpha_p}$ and $h(k)=n$, then $k\mid n$. For each $p\mid n$, the exponent of $p$ in $F(k)$ is one of

$0,2,3,\ldots,\alpha_p,$

which gives exactly $\alpha_p$ choices. Lemma 2 therefore recovers the Gyulev and Kominers bound

$f(n)\le\prod_{p\mid n}\alpha_p.$

The familiar maximal-order argument yields

$f(n)\le
\exp\!\left(\left(\frac{\log3}{3}+o(1)\right)
\frac{\log n}{\log\log n}\right).$

The coefficient is positive, so this does not prove Problem 1060.

Divisibility chain packing

This section gives a self-contained proof of the strongest unconditional estimate obtained in the investigation. It is the argument in the supplied peer manuscript, with the quantifiers and boundary cases made explicit.

For a prime $p$ and $e\ge0$, write

$H(p,e)=h(p^e)=p^e\frac{p^{e+1}-1}{p-1}.$

Lemma A Comparable exponent indices

Let $S$ be a finite set of primes satisfying

$\prod_{p\in S}\frac p{p-1}\le4.$

Suppose that all prime factors of $u$ and $v$ belong to $S$, that $h(u)=h(v)$, and that for every $p\in S$ the two integers $v_p(u)+1$ and $v_p(v)+1$ are comparable under divisibility. Then $u=v$.

Proof

Cancel every local factor $H(p,e)$ for which the two exponents agree. At each remaining prime, write $a_p>b_p\ge0$ for the larger and smaller exponent and put $d_p=a_p-b_p$. Divisibility comparability gives $b_p+1\mid a_p+1$, and hence

$\frac{H(p,a_p)}{H(p,b_p)}
=p^{d_p}Q_p,
\qquad
Q_p=\frac{p^{a_p+1}-1}{p^{b_p+1}-1}\in\mathbb N.$

Moreover,

$1<\frac{Q_p}{p^{d_p}}
=\frac{1-p^{-(a_p+1)}}{1-p^{-(b_p+1)}}
<\frac1{1-p^{-(b_p+1)}}
\le\frac p{p-1}.$

Let $P_+$ contain the primes at which $u$ has the larger exponent and let $P_-$ contain those at which $v$ has the larger exponent. Set

$A=\prod_{p\in P_+}p^{d_p},\quad
B=\prod_{p\in P_-}p^{d_p},\quad
U=\prod_{p\in P_+}Q_p,\quad
V=\prod_{p\in P_-}Q_p.$

The equality $h(u)=h(v)$ becomes $AU=BV$. Since $A$ and $B$ are coprime, $A\mid V$ and $B\mid U$, so $U=cB$ and $V=cA$ for an integer $c\ge1$. If any exponent differs, the strict inequalities above give

$1<c^2=\frac{UV}{AB}
<\prod_{p\in P_+\cup P_-}\frac p{p-1}
\le4,$

which is impossible for an integer $c$. Thus no exponent differs.

Lemma B Random chains with geometric marginals

Put

$t=\frac1{\sqrt2},\qquad A=\sqrt{t+t^2}.$

For every integer $a\ge0$ there is a probability distribution on divisibility chains $C\subseteq\{1,\ldots,a+1\}$, all containing $1$, such that

$\mathbb P(j+1\in C)\ge A^{-a}t^j
\qquad(0\le j\le a).$

Proof

Make $\{1,\ldots,a+1\}$ a rooted tree by giving every $m>1$ the parent $m/P^+(m)$, where $P^+(m)$ is its largest prime factor. Every root-to-vertex path is a divisibility chain. Prescribe node masses

$q(1)=1,
\qquad
q(m)=A^{-a}t^{m-1}\quad(2\le m\le a+1).$

For $m\ge2$, every child is $mr$ for a prime $r\ge P^+(m)$, so

$\frac{\sum_{w\text{ child of }m}q(w)}{q(m)}
\le\sum_{r=2}^{\infty}t^{m(r-1)}
=\frac{t^m}{1-t^m}\le1.$

For the root it is enough to show $\sum_{p\le a+1}t^{p-1}\le A^a$. The cases $a=0,1$ are immediate. For $a=2,3$ the left side is $t+t^2=A^2\le A^a$. For $a=4,5$ it is $t+t^2+t^4=(t+t^2)^2=A^4\le A^a$, where $t^2=1/2$. For $a\ge6$, every prime except $2$ is odd, whence the left side is at most $t+\sum_{r\ge1}t^{2r}=1+t<A^6\le A^a$; explicitly $A^6-(1+t)=(2t-1)/8>0$.

The terminal mass

$r(m)=q(m)-\sum_{w\text{ child of }m}q(w)$

is therefore nonnegative. These terminal masses telescope to $q(1)=1$. Choose a terminal vertex with probability $r(m)$ and take its root path. The probability that the path contains a node $m$ is the total terminal mass in its subtree, namely $q(m)$. This proves the required marginal bounds.

Theorem A Chain packing bound

Let $N\ge2$, write $\alpha_p=v_p(N)$, and for $z\ge2$ put

$P_z(N)=\prod_{\substack{p\mid N\\p>z}}\frac p{p-1}.$

Whenever $P_z(N)\le4$,

$\log\max\{1,f(N)\}
\le
\sum_{\substack{p\mid N\\p\le z}}\log(\alpha_p+1)
+C_1\frac{\log N}{\log z},$

where

$C_1=\frac12\log\!\left(1+\frac1{\sqrt2}\right).$

Consequently,

$\log\max\{1,f(N)\}
\le
\left(C_1+o(1)\right)\frac{\log N}{\log\log N}$

uniformly as $N\to\infty$.

Proof

Partition the fiber by the exact exponents of the input at primes $p\le z$. There are at most

$T=\prod_{\substack{p\mid N\\p\le z}}(\alpha_p+1)$

parts. In a fixed nonempty part write every input as $k=du$, where $d$ is the common small-prime part. Then $\gcd(d,u)=1$ and

$h(u)=\frac{N}{h(d)}.$

For each $p\mid N$ with $p>z$, independently choose the random chain of Lemma B with cap $a=\alpha_p$. To $k=du$ attach the event

$E_k=\{v_p(u)+1\in C_p\text{ for every }p\mid N,\ p>z\}.$

The events in the fixed part are pairwise disjoint. Indeed, if both $E_k$ and $E_m$ occur, then at every residual prime the two exponent indices lie on one divisibility chain. Lemma A, applied to the residual inputs, forces $k=m$.

By independence and the marginal estimate,

$\mathbb P(E_k)
\ge
A^{-\sum_{p>z}\alpha_p}t^{\Omega(u)}.$

The size budgets give

$\sum_{\substack{p\mid N\\p>z}}\alpha_p\le\frac{\log N}{\log z},
\qquad
\Omega(u)\le\frac{\log u}{\log z}\le\frac{\log N}{2\log z},$

because $u^2\le h(u)\le N$. Since $t<1$,

$\mathbb P(E_k)
\ge
\exp\!\left(-C_1\frac{\log N}{\log z}\right),$

as

$\log A-\frac12\log t
=\frac12\log\frac{t+t^2}{t}
=\frac12\log(1+t)=C_1.$

Summing the probabilities of the disjoint events bounds each part by the reciprocal of this quantity. Multiplying by $T$ proves the finite estimate.

For the uniform conclusion, put $L=\log N$, $w=\log L$, and $z=L/w^3$. The elementary estimate $\pi(x)=O(x/\log x)$ and partial summation give

$\log P_z(N)
\le2\sum_{\substack{p\mid N\\p>z}}\frac1p
=O\!\left(\frac{\log w}{w}\right)=o(1).$

Indeed, primes exceeding $L$ contribute $O(1/w)$ because there are at most $L/w$ of them, while all primes in $(z,L]$ contribute $O(1/w+\log w/w)$. Thus $P_z(N)<4$ for all sufficiently large $N$. Also

$\sum_{\substack{p\mid N\\p\le z}}\log(\alpha_p+1)
\le z\log\!\left(1+\frac L{\log2}\right)
=O\!\left(\frac L{w^2}\right),$

and $\log z\sim w$. Substitution proves the theorem, with error $O(L\log w/w^2)$.

Corollary A Cubefree inputs

Let $f_2(N)$ count only the preimages in which every prime exponent is at most $2$. Then

$\log\max\{1,f_2(N)\}
\le
\left(\frac12\log\varphi+o(1)\right)
\frac{\log N}{\log\log N},$

where $\varphi=(1+\sqrt5)/2$.

Proof

Put $r=1/\varphi$, so $r+r^2=1$. At each residual input prime choose the chain $\{1,2\}$ with probability $r$ and $\{1,3\}$ with probability $r^2$. The inclusion probabilities for exponent indices $1,2,3$ are $1,r,r^2$, so the event attached to $u$ has probability $r^{\Omega(u)}$. Lemma A again makes the events disjoint. The preceding size bound and the same choice of $z$ give a cost $r^{-L/(2\log z)}$; fixing the small exponents costs only $3^{\pi(z)}=\exp(o(L/\log L))$.

Proposition A Optimality inside the affine independent chain framework

The coefficient $C_1$ cannot be improved by any coordinatewise independent random-chain construction which, for a cap $a$, guarantees marginals

$q_a(e)\ge\exp(-\lambda a-\nu e)$

and then uses only the budgets $\sum a\le B$ and $\sum e\le B/2$.

Proof

Put $x=e^{-\lambda}$ and $t=e^{-\nu}$. At cap $a=2$, the indices $2$ and $3$ form an antichain, so no chain contains both and

$x^2(t+t^2)\le q_2(1)+q_2(2)\le1.$

At cap $a=4$, the indices $2,3,5$ form an antichain, giving

$x^4(t+t^2+t^4)\le1.$

The coefficient produced by the two budgets is $\lambda+\nu/2=\lambda-\frac12\log t$. If $t\ge1/\sqrt2$, the first inequality gives

$\lambda-\frac12\log t\ge\frac12\log(1+t)\ge C_1.$

If $t\le1/\sqrt2$, the second gives

$\lambda-\frac12\log t
\ge\frac14\log(t^{-1}+1+t^2)\ge C_1;$

the last expression decreases up to $t=1/\sqrt2$ on this interval. Lemma B attains equality. For the cubefree construction, the antichain $\{2,3\}$ forces $q(1)+q(2)\le1$; optimizing equal exponential marginals gives $r+r^2=1$, hence the coefficient $\frac12\log\varphi$.

This proposition is a method barrier, not a lower bound for $f(N)$. Arithmetic information beyond comparability and the two aggregate budgets could still improve the theorem.

Exact gcd normalization beyond comparable indices

The peer lemma can be extended without assuming divisibility comparability. The extension is useful because it identifies the obstruction exactly; it also shows why simply repeating the integer-square argument would be invalid.

For $e\ge0$ put

$S_e(p)=1+p+\cdots+p^e.$

Consider a normalized collision $h(u)=h(v)$, meaning that every local block $H(p,e)$ which is identical on the two sides has been cancelled. At a remaining base $p$, let

$a_p^+=\max(v_p(u),v_p(v)),\qquad
a_p^-=\min(v_p(u),v_p(v)),$

and define

$d_p=\gcd(a_p^++1,a_p^-+1),\qquad
r_p=a_p^-+1-d_p.$

The classical identity

$\gcd(S_a(p),S_b(p))=S_{\gcd(a+1,b+1)-1}(p)$

follows from $\gcd(p^m-1,p^n-1)=p^{\gcd(m,n)}-1$. Divide the two local divisor sums by this gcd. Orienting the bases according to which input has the larger exponent gives coprime products $A,B$ of the base-prime powers and products $X,Y$ of the reduced divisor sums such that

$AX=BY,\qquad \gcd(A,B)=1.$

Consequently there is an integer $c\ge1$ with

$X=cB,\qquad Y=cA.$

Set

$C=\prod_p p^{r_p}.$

Proposition B Defect-square identity

Every nontrivial normalized collision satisfies

$\boxed{
\left(\frac cC\right)^2
=\prod_p
\frac{(1-p^{-(a_p^++1)})(1-p^{-(a_p^-+1)})}
{(1-p^{-d_p})^2}.}$

In particular,

$1<\frac cC<\prod_p(1-p^{-d_p})^{-1},$

and therefore

$\prod_p(1-p^{-d_p})^{-1}>1+\frac1C.$

Proof

Multiplying $X=cB$ and $Y=cA$ gives

$c^2=\frac{XY}{AB}.$

For a local pair $a>b$ and $d=\gcd(a+1,b+1)$,

$\frac{S_a(p)}{S_{d-1}(p)}
=p^{a+1-d}\frac{1-p^{-(a+1)}}{1-p^{-d}},$

and likewise for $b$. Since

$(a+1-d)+(b+1-d)-(a-b)=2(b+1-d),$

multiplication over the differing bases gives the boxed identity. Each local factor is greater than one because $d\le b+1<a+1$, while its positive square root is less than $(1-p^{-d})^{-1}$. Finally $c/C>1$ and $c,C$ are positive integers, so $c\ge C+1$.

The condition $r_p=0$ is equivalent to

$a_p^-+1\mid a_p^++1.$

Thus $C=1$ exactly in the comparable-index situation of Lemma A. In that case $d_p=a_p^-+1$ at every differing base, so the corresponding local factor in the boxed product collapses to

$\frac{1-p^{-(a_p^++1)}}{1-p^{-(a_p^-+1)}}
<\frac p{p-1}.$

Consequently

$1<c^2<\prod_{p\in\Delta(u,v)}\frac p{p-1}\le4,$

which is impossible for an integer $c$. Proposition B therefore recovers the peer lemma.

For incomparable indices, however, the denominator is real and cannot be discarded. The exact collision

$h(315)=315\cdot624=196560=351\cdot560=h(351)$

has, after normalization,

$C=3^2=9,\qquad c=16.$

Hence $C\nmid c$. A large independently verified cubefree collision has a reduced denominator of $35$ decimal digits. The defect-square identity is therefore a rigorous extension and a precise diagnosis of the missing step, not a completion of the argument.

The gcd formula for geometric sums is classical. A bounded search of the sources audited here did not locate the defect-square identity packaged in this form, but that is not a priority or originality claim.

A prior unconditional coefficient from the powerful part alone

The extra observation is that a powerful part arising from an actual preimage cannot be an arbitrary allowed divisor.

Theorem 3 Rankin refinement

Let $x_0$ be the unique root in $(0,1)$ of

$3x^3+x^2=3,$

and put

$C=-\frac12\log x_0+
\frac13\log(1+x_0^2+x_0^3).$

Then

$C=0.3632703226483360951\ldots$

and, as $n\to\infty$,

$f(n)\le
\exp\!\left((C+o(1))\frac{\log n}{\log\log n}\right).$

Proof

For $n>1$ and $h(k)=n$,

$n=k\sigma(k)>k^2.$

By Lemma 2, the preimages inject into the set

$\mathcal D(n)=
\left\{d\le\sqrt n:
v_p(d)\in\{0,2,\ldots,\alpha_p\}
\text{ for }p^{\alpha_p}\parallel n\right\}.$

Write $D(n)=\#\mathcal D(n)$, $L=\log n$, $L_2=\log L$, and

$z=\frac{L}{L_2^3}.$

Fix $\lambda\ge0$ and set $t=\lambda/\log z$. The primes $p\le z$ contribute at most

$\left(1+\frac{L}{\log2}\right)^{\pi(z)}
=\exp\!\left(O\!\left(\frac{L}{L_2^2}\right)\right)$

possible local exponent patterns. For the primes $p>z$, Rankin's trick gives

$D(n)\le
\exp\!\left(O\!\left(\frac{L}{L_2^2}\right)\right)
n^{t/2}
\prod_{\substack{p^{\alpha}\parallel n\\p>z}}
\left(1+\sum_{e=2}^{\alpha}p^{-te}\right).$

Define

$S_a(\lambda)=1+\sum_{e=2}^a e^{-\lambda e},
\qquad
B(\lambda)=\sup_{a\ge2}\frac{\log S_a(\lambda)}a.$

Since $p^{-t}\le z^{-t}=e^{-\lambda}$ and

$\sum_{\substack{p^{\alpha}\parallel n\\p>z}}\alpha
\le\frac{L}{\log z},$

we obtain

$\log D(n)\le
\left(\frac\lambda2+B(\lambda)+o(1)\right)
\frac{L}{L_2}.$

It remains to minimize the coefficient. Put $x=e^{-\lambda}$ and $S_a=1+x^2+\cdots+x^a$. For every $\lambda$,

$\frac\lambda2+B(\lambda)
\ge
g_3(\lambda)
:=\frac\lambda2+\frac13\log(1+e^{-2\lambda}+e^{-3\lambda}).$

The function $g_3$ is strictly convex. Its derivative vanishes exactly when

$3-x^2-3x^3=0,$

so its unique minimum occurs at $\lambda_0=-\log x_0$.

We now show that $a=3$ actually attains the supremum in $B(\lambda_0)$. The root satisfies $0.9<x_0<0.91$. For $0\le u\le0.91$, the exponential series and $j!\ge2\cdot3^{j-2}$ for $j\ge2$ give

$e^u\le1+u+\frac{u^2}{2(1-u/3)}<2.505.$

On the other hand,

$S_3(x_0)>1+0.9^2+0.9^3=2.539,$

so $x_0<\log S_3(x_0)$. For $a\ge3$, we have $S_a\ge a x_0^a$, and therefore

$a\log\frac{S_{a+1}}{S_a}
\le\frac{a x_0^{a+1}}{S_a}
\le x_0
<\log S_3
\le\log S_a.$

Thus $\log S_a/a$ decreases strictly for $a\ge3$. Finally,

$S_3^2-S_2^3
=x_0^2(-1+2x_0-2x_0^2+2x_0^3)>0,$

because the polynomial in parentheses is increasing and already positive at $0.9$. Hence $a=3$ also beats $a=2$. We conclude that

$B(\lambda_0)=\frac13\log(1+x_0^2+x_0^3).$

The lower bound through $g_3$ and equality at $\lambda_0$ prove that the global minimax value is $C$. Since $f(n)\le D(n)$, the theorem follows.

Sharpness of the refined majorant

Theorem 3 still has a fixed positive coefficient. This is not merely a loose optimization.

Proposition 4

The coefficient $C$ is the exact maximal-order coefficient for $D(n)$. In particular, the injection into $\mathcal D(n)$ cannot by itself prove the Erdős conjecture.

Proof

Take

$n_y=\prod_{y<p\le2y}p^3$

and let $r=\pi(2y)-\pi(y)$. Each allowed divisor corresponds to a word $(e_p)$ with letters in $\{0,2,3\}$, subject to

$\sum e_p\log p\le\frac32\sum\log p.$

Let

$F=1+x_0^2+x_0^3$

and first consider the probability distribution on $\{0,2,3\}$ with probabilities

$\frac1F,
\qquad
\frac{x_0^2}{F},
\qquad
\frac{x_0^3}{F}.$

The defining equation for $x_0$ says that the mean exponent is $3/2$. For a fully one-sided count, let $\delta=r^{-1/4}$ and tilt the parameter slightly so that the mean is $3/2-\delta$. The three probabilities remain bounded away from zero and converge to the displayed probabilities. Hoeffding's inequality applied to the weighted exponent sum shows that, with probability $1-o(1)$,

$\sum e_p\log p<\frac32\sum\log p.$

A second concentration estimate for the information content $-\log\Pr((e_p))$ shows that, with probability $1-o(1)$, it is $r(H_\delta+o(1))$, where $H_\delta\to H$. The intersection of these two events therefore contains at least $\exp((H-o(1))r)$ words. Equivalently, this conclusion follows by sorting the corresponding multinomial types and applying Stirling's formula. We obtain

$\log D(n_y)\ge(H-o(1))r,$

where the entropy is

$H=\log F+\frac32(-\log x_0)=3C.$

The prime number theorem gives

$\log n_y=(3+o(1))y,
\qquad
r=(1+o(1))\frac y{\log y},
\qquad
\log\log n_y=(1+o(1))\log y.$

Consequently

$\log D(n_y)\ge
(C-o(1))\frac{\log n_y}{\log\log n_y}.$

Together with Theorem 3, this proves sharpness.

There is a broader barrier for every argument which forgets the squarefree remainder and counts all admissible powerful parts. Put

$G(n)=\#\{d:d\text{ is powerful and }h(d)\mid n\}.$

Gyulev's injection gives $f(n)\le G(n)$, but this majorant itself can have a positive maximal-order coefficient.

Proposition 4A Powerful-divisor barrier

There are arbitrarily large $n$ for which

$G(n)\ge
\exp\!\left(
\left(\frac{\log2}{4}+o(1)\right)
\frac{\log n}{\log\log n}
\right).$

Proof

Let $T_y$ be the primes in $(y/2,y]$ and set

$n_y^*=\prod_{q\in T_y}h(q^2).$

For every subset $U\subseteq T_y$, the powerful integer

$d_U=\prod_{q\in U}q^2$

satisfies $h(d_U)\mid n_y^*$ by multiplicativity. Hence $G(n_y^*)\ge2^{|T_y|}$. The prime number theorem gives

$|T_y|\sim\frac{y}{2\log y},
\qquad
\log n_y^*=\sum_{q\in T_y}\log\bigl(q^2(q^2+q+1)\bigr)\sim2y.$

Substitution proves the claim.

This does not give many actual preimages: the squarefree remainder must still solve an exact equation, and that missing condition can eliminate almost every counted powerful part. The proposition proves that no refinement which continues to dominate $G(n)$ can establish the Erdős little-$o$ estimate. The successful chain-packing theorem uses pairwise arithmetic incompatibility and therefore does not factor solely through this majorant, although it too stops at a positive constant.

A polylogarithmic shortcut and why it fails

For a finite set of primes $T$, write $Q_T=\prod_{p\in T}p$.

Proposition 5 Finite hitting set criterion

The following statements are equivalent.

1. The map $h$ is injective on integers coprime to $Q_T$.

2. In every fiber of $h$, the vector $(v_p(k))_{p\in T}$ determines $k$.

If either statement holds, then

$f(n)\le\prod_{p\in T}(v_p(n)+1)\ll_T(\log n)^{|T|}.$

Proof

Suppose two members $k,m$ of one fiber have the same valuations at all primes in $T$. Let

$d=\prod_{p\in T}p^{v_p(k)},
\qquad
k=da,
\qquad
m=db.$

Then $a,b$ are coprime to $d$, and multiplicativity cancels $h(d)$ to give $h(a)=h(b)$. Thus injectivity on integers coprime to $Q_T$ implies injectivity of the valuation vector. The converse follows by applying the vector statement to a fiber whose members are coprime to $Q_T$. The displayed count is immediate.

This proposition would solve the stronger polylogarithmic conjecture if a suitable fixed $T$ existed. The smallest plausible choices do not work.

Proposition 6 Exact collision away from 6

Let

$K=13^2\cdot17\cdot31\cdot37^3\cdot61\cdot67^2\cdot73\cdot97\cdot137$

and

$M=5\cdot7^2\cdot23\cdot31^3\cdot37^2\cdot61^2\cdot67\cdot137^2.$

Then

$\gcd(KM,6)=1,
\qquad
K\ne M,
\qquad
h(K)=h(M),$

with

$\begin{aligned}
K&=1198387013221054310407,\\
M&=1075370347698293222695,\\
h(K)&=h(M)\\
&=1859441120099263354172212044541787564298240.
\end{aligned}$

Both $K$ and $M$ are fourth-power-free. Thus $h$ is not injective on fourth-power-free integers coprime to $6$.

Proposition 7 Exact collision away from 30

Let

$K_2=7^2\cdot11^2\cdot13\cdot31^2\cdot37\cdot43\cdot61\cdot83\cdot127$

and

$M_2=7^5\cdot11^3\cdot19^2\cdot31^3\cdot331.$

Then

$\gcd(K_2M_2,30)=1,
\qquad
K_2\ne M_2,
\qquad
h(K_2)=h(M_2),$

where

$\begin{aligned}
K_2&=75775710700917227,\\
M_2&=79632166734466577,\\
h(K_2)&=h(M_2)\\
&=8901250382372638700189613616054272.
\end{aligned}$

The exact prime-power certificates appear in the appendix. They were verified by two independent arbitrary-precision calculations and by direct divisor summation. The propositions refute $T=\{2,3\}$ and $T=\{2,3,5\}$. The following larger certificate also refutes $T=\{2,3,5,7\}$. None of these examples proves that every finite hitting set fails.

Proposition 8 Exact collision away from 210

Let

$\begin{aligned}
K_3={}&60629697601617236747379985403,\\
M_3={}&61655391632564660609643619057.
\end{aligned}$

Both integers are cubefree and coprime to $210$, have the same input exponent profile $[1^8,2^4]$, and satisfy

$h(K_3)=h(M_3)
=5276516179938729922490847708056660616574496169354744299520.$

Their prime-power decompositions are

$\begin{aligned}
K_3={}&11^2 13^2 17\,19\,31\,61\,97\,127^2 271\,307^2 331\,367,\\
M_3={}&13\,17^2 19^2 23\,31^2 43\,61^2 83\,127\,307\,733\,5419.
\end{aligned}$

An independently reconstructed certificate gives

$\begin{aligned}
\sigma(K_3)&=87028574917351791526375587840,\\
\sigma(M_3)&=85580774693381738895491727360.
\end{aligned}$

Multiplication gives the common value above. Its exact prime factorization is

$\begin{aligned}
2^{20}3^5 5\,7^3 11^2 13^2 17^2 19^2 23\,31^2 43\,61^2
83\,97\,127^2 271\,307^2 331\,367\,733\,5419.
\end{aligned}$

The certificate was reconstructed using only the listed prime powers, the geometric-series formula for every divisor sum, exact primality checks for every base, and prime-valuation aggregation. It is Moser-primitive: all $127$ nontrivial common divisors were tested. It is also conformally indecomposable: among the $4096$ subset products of the twelve local blocks on each side, the only common products are $1$ and the displayed common value. The mixed-integer model used to discover the identity is not part of its proof.

All three rough-input collisions are primitive in Moser's sense: for every common divisor $d>1$ of the two inputs, dividing both inputs by $d$ destroys the equality. Exhaustive checks cover the $47$, $26$, and $127$ nontrivial divisors of the three respective greatest common divisors. The bounded search did not locate these identities in Guy B11, Noppakaew and Pongsriiam, Kominers, or the current relevant OEIS records; exact-number searches also returned no matches. This is not a proof that the identities are first known.

Reduction to bounded exponents

The failure of small hitting sets suggests separating high exponents from a bounded-exponent core.

Call an integer $R$-free when every prime exponent is smaller than $R$, and define

$f_R(y)=\#\{u:h(u)=y\text{ and }u\text{ is }R\text{-free}\},
\qquad
F_R(Y)=\max_{y\le Y}f_R(y).$

Theorem 9 Bounded exponent reduction

For fixed $R\ge2$, define

$g_R(a)=
\begin{cases}
1,&a<R,\\
a-R+2,&a\ge R.
\end{cases}$

Then

$f(n)\le F_R(n)\prod_{p^a\parallel n}g_R(a).$

Moreover,

$\log\prod_{p^a\parallel n}g_R(a)
\le
\left(c_R+o(1)\right)\frac{\log n}{\log\log n},$

where

$c_R=\max_{a\ge R}\frac{\log(a-R+2)}a
=O\!\left(\frac{\log R}{R}\right).$

Consequently, Problem 1060 would follow if, for every fixed $R$,

$\log F_R(Y)=o\!\left(\frac{\log Y}{\log\log Y}\right).$

Proof

Color the possible exponent of each prime by putting $0,1,\ldots,R-1$ in one class and retaining each exponent $e\ge R$ as its own class. The number of colors at a prime with $p^a\parallel n$ is $g_R(a)$.

Two preimages with the same color vector have the same $R$-full factor $d$. They can be written as $du$ and $dv$, where $u,v$ are $R$-free and coprime to $d$. Cancelling $h(d)$ gives $h(u)=h(v)$. Thus a color class has at most $F_R(n)$ members, proving the first inequality.

For completeness, put $L=\log n$, $w=\log L$, and $z=L/w^3$. At primes $p\le z$ we use $g_R(a)\le a+1\le1+L/\log2$, obtaining

$\sum_{\substack{p^a\parallel n\\p\le z}}\log g_R(a)
\le\pi(z)\log\!\left(1+\frac L{\log2}\right)
=O\!\left(\frac L{w^2}\right).$

At primes $p>z$, the definition of $c_R$ gives $\log g_R(a)\le c_Ra$, and

$\sum_{\substack{p^a\parallel n\\p>z}}a
\le\frac L{\log z}.$

Since $\log z\sim w$, the two estimates yield

$\log\prod_{p^a\parallel n}g_R(a)
\le\left(c_R+o(1)\right)\frac Lw.$

Here $R$ is fixed before $n$ tends to infinity. Finally, $c_R=O((\log R)/R)$; for example, $c_R\le(\log R)/R$ for $R\ge3$.

Given $\varepsilon>0$, choose fixed $R$ with $c_R<\varepsilon/2$. The asserted little-$o$ estimate for $F_R$ then contributes less than $\varepsilon/2$ for all sufficiently large $n$. This proves the final implication.

The new collision in Proposition 6 is already $4$-free. Hence uniform injectivity of $R$-free inputs, which holds at $R=2$ by Lemma 1, already fails at $R=4$.

A reciprocal mass criterion for the fixed exponent step

The bounded-exponent reduction can be sharpened to a concrete sufficient condition. For a finite prime set $D$, define its Euler mass by

$\lambda(D)=\sum_{p\in D}-\log(1-1/p)
=\log\prod_{p\in D}\frac p{p-1}.$

Call a collision normalized after every identical local block $H(p,e)$ occurring on both sides has been cancelled. Its differing-base set is

$\Delta(u,v)=\{p:v_p(u)\ne v_p(v)\}.$

Proposition 10 Euler mass gap criterion

Fix $R$. Suppose that there is an $\eta_R>0$ such that every nontrivial normalized collision of $R$-free inputs satisfies

$\lambda(\Delta(u,v))\ge\eta_R.$

Then, for every fixed $\theta$ with $e^{-\eta_R}<\theta<1$,

$f_R(y)\le R^{\omega(y)^{\theta+o(1)}}$

uniformly as $\omega(y)\to\infty$; fibers with bounded $\omega(y)$ are bounded in terms of $R$ and $\omega(y)$. In particular,

$\log F_R(Y)=o_R\!\left(\frac{\log Y}{\log\log Y}\right),$

for that fixed $R$. If the stated positive-gap hypothesis holds for arbitrarily large fixed values of $R$ (in particular, if it holds for every fixed $R$), then Theorem 9 proves Erdős Problem 1060.

Proof

Write the primes dividing $y$ as $q_1<\cdots<q_s$. For an exact finite version, choose the least $m$ for which

$\sum_{j>m}-\log(1-1/q_j)<\eta_R.$

Two fiber members agreeing at $q_1,\ldots,q_m$ must be equal: after their common local blocks are cancelled, a nontrivial difference would be supported in the displayed tail and would contradict the assumed gap. Projection to these $m$ exponent coordinates is injective, so $f_R(y)\le R^m$.

For the asymptotic form, let $p_j$ be the $j$th prime and take $m=\lfloor s^\theta\rfloor$. Since $q_j\ge p_j$, Mertens's theorem and the prime number theorem give

$\sum_{j>m}-\log(1-1/q_j)
\le
\sum_{j=m+1}^{s}-\log(1-1/p_j)
=\log\frac{\log p_s}{\log p_m}+o(1)
=\log(1/\theta)+o(1)<\eta_R.$

Thus $m=s^{\theta+o(1)}$ and

$\log f_R(y)\le(\log R)s^{\theta+o(1)}.$

To pass to the running maximum, let $x\le Y$. Uniformly,

$\omega(x)=O\!\left(\frac{\log Y}{\log\log Y}\right).$

Choose any fixed $\theta'$ with $\theta<\theta'<1$; the preceding estimate, with the finitely many bounded-support cases absorbed into the constant, gives

$\log F_R(Y)
=O_R\!\left(
\left(\frac{\log Y}{\log\log Y}\right)^{\theta'}
\right)
=o_R\!\left(\frac{\log Y}{\log\log Y}\right).$

This proves the claimed consequence.

The hypothesis of Proposition 10 is the precise unproved arithmetic bridge. Lemma A proves it with $\eta=\log4$ only in the sector where every pair of exponent indices is divisibility-comparable. It says nothing about the incomparable transition between input exponents $1$ and $2$.

There is a useful family-level formulation. For a subfamily $\mathcal A$ of an $R$-free fiber, let

$Z(\mathcal A)=\{p:\{v_p(k)+1:k\in\mathcal A\}\text{ is not a divisibility chain}\}.$

Projecting onto $Z(\mathcal A)$ and the first $\lfloor s^\theta\rfloor$ target primes, and applying Lemma A to any two members with the same projection, gives for every fixed $\theta>1/4$

$|\mathcal A|
\le R^{|Z(\mathcal A)|+s^{\theta+o(1)}}.$

Therefore, for a given fixed $R$, a uniform estimate

$\left|Z\bigl(\{u:h(u)=y,\ u\text{ is }R\text{-free}\}\bigr)\right|
=o_R\!\left(\frac{\log y}{\log\log y}\right)$

would prove the required fixed-$R$ fiber bound. Such estimates for arbitrarily large fixed $R$ would finish the problem through Theorem 9. No argument proving them is currently known.

The gap hypothesis is compatible with, but not suggested strongly by, current computation. An exact normalized cubefree collision has been found with every input prime at least $17$, $38$ differing bases, and

$\lambda(\Delta)=0.40790302090549446\ldots,
\qquad
\prod_{p\in\Delta}\frac p{p-1}
=1.5036613303846937\ldots.$

Its two inputs are

$\begin{aligned}
u={}&17\cdot19\cdot23\cdot31\cdot37\cdot43\cdot47^2\cdot67\cdot71\cdot79\cdot101\cdot127^2\cdot139\cdot149^2\\
&\cdot307^2\cdot313\cdot367\cdot631\cdot643\cdot1009\cdot1279^2\cdot3037\cdot4783\cdot5113\cdot5419\cdot6073\cdot10303^2\cdot12637,
\end{aligned}$

and

$\begin{aligned}
v={}&17^2\cdot19^2\cdot23^2\cdot37^2\cdot43^2\cdot47\cdot61\cdot71^2\cdot89\cdot101^2\cdot103\cdot127\cdot149\cdot157\\
&\cdot229\cdot271\cdot307\cdot733\cdot1279\cdot2383\cdot2557\cdot3037^2\cdot5419^2\cdot5827\cdot6073^2\cdot10303.
\end{aligned}$

Direct arbitrary-precision multiplication independently verifies $h(u)=h(v)$, primality of every displayed base, the absence of a common exact local block, and the stated mass. The search timed out after finding this incumbent, so it is not claimed to minimize the mass even in its finite search universe. In particular it neither proves nor refutes the existence of a positive $\eta_R$.

A second exact cubefree certificate has $75$ differing bases, every one at least $19$, and

$\lambda(\Delta)=0.4273540761303973\ldots.$

It rigorously rules out any assertion that every normalized cubefree collision uses an input base at most $17$. Like the preceding identity, it is a finite witness and gives neither an unbounded-roughness sequence nor a vanishing-mass sequence.

A predecessor graph for bounded exponents

The next lemma is a structural improvement, but not a solution.

Fix $R$ and a target $y$. Form a graph on the primes dividing $y$. For $q<P$, join $q$ to $P$ if

$P\mid\sigma(q^e)$

for some $1\le e<R$.

Theorem 10 Predecessor graph bound

Put

$C_R=1+2+\cdots+(R-1)=\frac{R(R-1)}2.$

The predecessor graph is $C_R$-degenerate. If $p^a\parallel y$, then

$\log\#\{u:h(u)=y\text{ and }u\text{ is }R\text{-free}\}
\le
\frac{C_R}{C_R+1}
\sum_{p^a\parallel y}\log\min(R,a+1).$

Proof

For fixed $P$ and $e$, the nonzero polynomial

$1+X+\cdots+X^e$

has at most $e$ roots modulo $P$. Because a lower predecessor satisfies $q<P$, every residue contains at most one possible prime $q$. Thus $P$ has at most $C_R$ lower neighbors. Ordering vertices by size proves degeneracy and gives a coloring with $C_R+1$ independent color classes.

Now take two distinct $R$-free preimages and let $P$ be their largest differing base prime. All local factors $h(q^{e_q})$ with $q>P$ are identical on the two sides and can be cancelled. Taking the $P$-adic valuation of the remaining identity shows that the different base exponent at $P$ must be balanced by $P\mid\sigma(q^e)$ for a smaller differing base prime $q$. Hence the set of differing primes cannot lie inside an independent set of the predecessor graph.

It follows that, for any independent set $I$, the exponents outside $I$ determine the entire preimage. Give vertex $p$ the weight

$w_p=\log\min(R,v_p(y)+1).$

One color class has at least $1/(C_R+1)$ of the total weight. Projecting away from that independent class leaves at most the exponential of the remaining weight possible vectors, which proves the displayed bound.

This bound saves a fixed proportion for fixed $R$, but $C_R$ grows quadratically. It does not establish the required little-$o$ estimate. The missing ingredient is a global restriction on independent balanced cycles, rather than a local bound on the number of predecessors.

The simplest acyclicity hope is false. For example,

$61\mid13^2+13+1,
\qquad
13\mid61^2+61+1.$

The exact identities in Propositions 6 and 7 exhibit larger balanced cycles.

State-dependent transition graphs

There is a sharper family-level graph which records only dependencies that actually vary inside one fiber. Retaining the convention above, let $\mathcal F$ be a family of $R$-free preimages of $N$, so every input exponent is $<R$. Let $S$ be the union of their input-prime supports, and put

$A_q=\{v_q(k):k\in\mathcal F\}.$

Define a directed graph $D_{\mathcal F}$ on $S$ by placing an arc $q\to p$ when

$e\longmapsto v_p(\sigma(q^e))$

is nonconstant on $A_q$. Every fiber member satisfies

$v_p(N)=v_p(k)+\sum_{q\in S}v_p(\sigma(q^{v_q(k)})).$

Proposition 11 Feedback-set reconstruction

If $T$ is a directed feedback vertex set of $D_{\mathcal F}$, then the exponent coordinates on $T$ determine the member of $\mathcal F$. Hence

$|\mathcal F|\le\prod_{p\in T}|A_p|\le R^{|T|}.$

Proof

After the coordinates on $T$ are fixed, topologically order $D_{\mathcal F}-T$. Compare two fiber members which agree on $T$. In the valuation equation at a vertex $p$, every contribution which can vary comes from the tail of an incoming arc, hence from a coordinate already recovered in the topological order. All other contributions are constant on the fiber and cancel. The equation therefore determines $v_p(k)$ successively.

Thus a uniform estimate

$\tau(D_{\mathcal F})
=o_R\!\left(\frac{\log N}{\log\log N}\right)$

would solve the fixed-$R$ problem. If such estimates held for arbitrarily large fixed $R$, Theorem 9 would then prove Erdős 1060. No theorem supplying this arithmetic estimate was located in the bounded search.

One can charge vertex-disjoint cycles to the target, but the resulting scale still has a positive constant. An upward arc $q\to p$, with $q<p$, implies that $p\mid\sigma(q^e)$ for some occurring state $e$. If $e=1$, then $p\mid q+1$ forces $(q,p)=(2,3)$. Otherwise $e\ge2$, and the corresponding local block shows

$q^2p\mid N.$

Every directed cycle contains an upward arc. If $t$ vertex-disjoint directed cycles are selected, at most one uses the exceptional arc $2\to3$. Selecting one upward arc from each other cycle gives $2(t-1)$ distinct endpoint primes. If $\ell_j$ denotes the $j$th prime, rearrangement yields

$N\ge
\left(\prod_{j=1}^{t-1}\ell_j^2\right)
\left(\prod_{j=t}^{2t-2}\ell_j\right).$

The prime number theorem therefore gives the rigorous bound

$\nu(D_{\mathcal F})
\le\left(\frac13+o(1)\right)
\frac{\log N}{\log\log N}.$

This is not little-$o$, and a packing bound is not automatically a comparably small feedback-set bound. Even if $\tau=\nu$ were known in this special graph class, the displayed estimate would retain a positive coefficient.

The distinction is visible in exact cubefree examples. The coprime-to-$210$ collision of Proposition 8 has two vertex-disjoint cyclic strongly connected components and

$\tau=\nu=2.$

Tensoring it with the disjoint-support identity $h(12)=h(14)=336$ gives four exact cubefree preimages of one target and a transition graph with

$\tau=\nu=3.$

The two coordinates $\{2,11\}$ nevertheless distinguish those four preimages, so a feedback set can be strictly larger than the true information separator.

A further exact cubefree collision avoids the input bases $2,3,31$:

$\begin{aligned}
K={}&297988218233648364240999791517121425214912505,\\
M={}&338368113000148356341974220844029561466672613,
\end{aligned}$

and

$h(K)=h(M)=
147424966926910851646005882187078719136356520640407126230120281498533058410853434392576000.$

Its state-dependent graph has $24$ vertices, $34$ arcs, and the unique minimum feedback set $\{61\}$. The set of bases at which the two exponent indices are divisibility-incomparable is

$\{17,19,97,127,197,307,317,379\},$

but deleting this entire set leaves the directed 2-cycle $13\leftrightarrow61$. Hence the tempting claim that the non-chain coordinates form a feedback set is false. This does not weaken Lemma A, which is a global pairwise incompatibility statement; it blocks a proposed localization of that lemma.

Other verified structural routes and their limits

A VC-dimension reformulation

For $2\le j\le R$ define

$S_j(k)=\{p:v_p(k)\ge j\},
\qquad
\mathcal A_j=\{S_j(k):k\in\mathcal F\}.$

The tuple $(S_2(k),\ldots,S_R(k))$ encodes the powerful part, so Gyulev's lemma makes it injective on a fiber. If $s$ is the union-support size and $d_j=\operatorname{VCdim}(\mathcal A_j)$, Sauer--Shelah gives

$|\mathcal F|
\le\prod_{j=2}^{R}|\mathcal A_j|
\le\prod_{j=2}^{R}\sum_{i=0}^{d_j}{s\choose i}.$

For fixed $R$, the uniform statement $\max_j d_j=o_R(s)$ would therefore prove the fixed-exponent estimate. It is another exact formulation of the missing global theorem, not an automatic consequence of powerful-part injectivity.

Indeed, the four-point tensor fiber described above shatters the two coordinates $\{2,11\}$ at threshold $2$, so its VC dimension is at least $2$. More generally, $t$ pairwise support-disjoint collision atoms, each toggling a distinguished exponent across a fixed threshold, tensor to $2^t$ equal-value inputs and shatter those $t$ distinguished coordinates. A VC proof must therefore establish an arithmetic prohibition on linearly many disjoint atoms; Sauer--Shelah by itself does not do so.

An injective third-order approximant and its metric barrier

Dedekind's function

$\psi(n)=n\prod_{p\mid n}(1+p^{-1})$

gives the injective comparison map $D(n)=n\psi(n)$; this is a special case of Noppakaew and Pongsriiam's injectivity theorem for $n^a\psi(n)^b$. Locally,

$h(n)=D(n)\rho(n),
\qquad
\rho(n)=\prod_{p^e\parallel n}
\frac{1-p^{-(e+1)}}{1-p^{-2}}.$

After the states at primes $p\le z$ have been fixed, this puts two members of one $h$-fiber into a $D$-ratio interval of logarithmic width

$O\!\left(\sum_{p>z}p^{-2}\right)
=O\!\left(\frac1{z\log z}\right).$

There is an exact one-power improvement. Define the positive rational-valued multiplicative-by-local-states map

$A_3(p^0)=1,
\qquad A_3(p)=p(p+1),
\qquad A_3(p^e)=\frac{p^{2e+1}}{p-1}\quad(e\ge2).$

Proposition 12 Third-order powerful-part approximation

The map $A_3:\mathbb N\to\mathbb Q_{>0}$ is injective, and

$h(n)=A_3(n)\vartheta(n),
\qquad
\vartheta(n)=\prod_{\substack{p^e\parallel n\\e\ge2}}
(1-p^{-(e+1)}).$

If $h(k)=h(m)=N$ and $k,m$ agree at every prime at most $z$, then

$\left|\log\frac{A_3(k)}{A_3(m)}\right|
\le\sum_{p>z}-\log(1-p^{-3})
=O\!\left(\frac1{z^2\log z}\right).$

Proof

The factorization is immediate in states zero and one. For $e\ge2$,

$\frac{p^{2e+1}}{p-1}(1-p^{-(e+1)})
=p^e\frac{p^{e+1}-1}{p-1}=h(p^e).$

For injectivity, cancel every identical local state from an equality $A_3(u)=A_3(v)$ and let $P$ be the largest remaining base. If $P\ge5$, a factor from a smaller base $q$ has zero $P$-adic valuation: a repeated-state factor has numerator supported at $q$ and denominator dividing $q-1$, while a state-one factor is $q(q+1)$; with $q<P$, the latter can be divisible by $P$ only in the exceptional pair $(q,P)=(2,3)$. At base $P$, the possible $P$-adic valuations are

$0,1,5,7,9,\ldots$

for states $0,1,2,3,4,\ldots$, so the state is determined, a contradiction.

It remains only to distinguish bases $2$ and $3$. Their respective contributions to $(v_2,v_3)$ are

$(0,0),(1,1),(2a+1,0)\ (a\ge2),$

and

$(0,0),(2,1),(-1,2b+1)\ (b\ge2).$

The sum determines the two states: when $b\ge2$, its second coordinate has parity detecting whether $a=1$, then determines $b$, and its first coordinate determines $a$; the cases $b=0,1$ follow directly from the displayed lists. Hence $A_3$ is injective. Cancelling the common small-prime factors of $\vartheta$ gives the stated tail; partial summation and $\pi(x)=O(x/\log x)$ give the final estimate.

This sharper tail still does not yield a separation proof. A reduced denominator of $A_3(k)$ divides

$\prod_{\substack{p^e\parallel k\\e\ge2}}(p-1)
\le\prod_{\substack{p^e\parallel k\\e\ge2}}p
\le\sqrt k\le N^{1/4}.$

Also $\zeta(3)^{-1}\le\vartheta(k)\le1$, so $N\le A_3(k)\le\zeta(3)N$. Two distinct such rational values therefore have only the generic spacing

$\left|\log\frac{A_3(k)}{A_3(m)}\right|
\ge\frac1{\zeta(3)N^{3/2}}.$

Comparing this with the tail would require roughly $z>N^{3/4+o(1)}$, whereas every repeated input base already satisfies $p\le N^{1/4}$. Thus the comparison becomes effective only after the tail is trivially empty.

The weakness is structural, not just a poor estimate. Fix finitely many positive multiplicative functions $F_j$ satisfying $|\log F_j(p)|=O(\log p)$ on primes. For every fixed $B>0$ and all large $x$, there are

$\exp\!\left((\log2+o(1))\frac x{\log x}\right)$

distinct squarefree integers, all supported on primes in $(x,2x]$, whose $F_j$-values lie simultaneously in multiplicative boxes of logarithmic width $x^{-B}$. Indeed, take all subset products of the $(1+o(1))x/\log x$ primes in that interval. Each logarithmic coordinate occupies an interval of length $O(x)$; subdivision into intervals of length $x^{-B}$ creates only polynomially many boxes, so one box contains the asserted number of subsets. This applies to any fixed collection of the standard $n^a\psi(n)^b$ and Jordan-function approximants. These inputs are not claimed to share an $h$-value; the conclusion is that injectivity plus generic short-interval spacing cannot substitute for the exact common-target arithmetic.

Finally, the obvious local truncation cannot be iterated. Define multiplicatively

$T_s(p^e)=\sum_{j=0}^{\min(s-1,e)}p^{2e-j}.$

The products of the top one and two terms of every local block are $T_1(n)=n^2$ and $T_2(n)=D(n)$, respectively, but every truncation retaining three or more terms already has

$T_s(12)=h(12)=336=h(14)=T_s(14).$

Thus the exponent-two correction $1-p^{-3}$ is precisely where the known injective-approximant route meets the same bounded-exponent obstruction as the valuation graph.

The exact parity identity

Write

$k=2^a\prod_{p\text{ odd}}p^{e_p}.$

The lifting-the-exponent formula gives the exact identity

$v_2(h(k))
=a+\sum_{\substack{p\text{ odd}\\e_p\text{ odd}}}
\bigl(v_2(p+1)+v_2(e_p+1)-1\bigr).$

Indeed, $\sigma(2^a)$ is odd; for odd $p$, the divisor sum $\sigma(p^e)$ is odd when $e$ is even, while for odd $e$,

$v_2(\sigma(p^e))
=v_2(p^{e+1}-1)-v_2(p-1)
=v_2(p+1)+v_2(e+1)-1.$

Thus every preimage of $n$ contains at most $v_2(n)$ odd primes to odd input exponent. This is useful bookkeeping, but it leaves the even-exponent sector. In fact

$h(k)\text{ is odd}\quad\Longleftrightarrow\quad k\text{ is an odd square}.$

Hence injectivity on odd squares is equivalent to saying that every odd target has at most one preimage. No proof of that assertion is known here.

There is a rigorous warning against assuming it. If distinct coprime odd squares $x,y$ satisfied $h(x)=h(y)$, then

$\sigma(x)=uy,\qquad\sigma(y)=ux$

for an odd integer $u\ge3$, and therefore

$\sigma(xy)=u^2xy.$

Thus $xy$ would be an odd multiperfect number. Moreover

$9\le u^2
<\prod_{p\mid xy}\frac p{p-1}.$

Exact multiplication of the odd-prime Euler product shows that this forces $\omega(xy)\ge2697$. Chen and Luo's Odd Multiperfect Numbers records that no odd $k$-perfect number is known for any $k\ge2$. This does not prove that odd-square injectivity is equally hard, but it shows that it is not an available elementary lemma.

A profile bound that would be sufficient

For $n=\prod p^{\alpha_p}$ and $h(k)=n$, define the target profile of $k$ as the histogram of the pairs

$(\alpha_p,v_p(k))\qquad(p\mid n).$

If $r_a=\#\{p:v_p(n)=a\}$, the number of possible profiles is at most

$Q(n)=\prod_{a\ge1}{r_a+a\choose a}.$

This quantity already has the desired zero coefficient. Writing $L=\log n$ and $T=\lfloor L^{1/3}\rfloor$, the factors with $a\le T$ contribute $O(T^2\log L)$ to $\log Q(n)$. For $a>T$, use ${r_a+a\choose a}\le(a+1)^{r_a}$, the monotonicity of $\log(a+1)/a$, and $\sum ar_a\le L/\log2$ to obtain

$\log Q(n)
=O(L^{2/3}\log L)
=o\!\left(\frac L{\log L}\right).$

Therefore injectivity of the profile on a fiber would prove Erdős 1060. Raw profile injectivity is false. Let

$A=60629697601617236747379985403,
\quad
B=61655391632564660609643619057,$

the cubefree collision from Proposition 8, and put $r=5503$. Then $r$ is prime and

$x=Ar=333645225901699653820832059672709,$

$y=Br=339289620154003327334868835670671$

have equal $h$-values and identical target profiles. The exact state $(5503,1)$ is common to both sides. After that common block is cancelled, the two residual profiles differ. Consequently this example does not refute the following normalized version:

Remove the exact local blocks common to every member of a fiber. On the residual fiber, the target-profile map is injective.

That normalized assertion would still imply the conjecture through the bound for $Q(n)$, and it survived the finite searches described in the reproducibility directory. It has not been proved. Treating it as a theorem would simply rename the missing step.

Longer sigma cycles

The valuation graph cannot be reduced to two-cycles. Exact cubefree collision certificates in the accompanying files have directed girth $6$, $8$, and $10$ after the indicated shorter cycles are forbidden. One girth-$10$ certificate has valuation-matrix rank $33$ and nullity $9$. These computations are exact counterexamples to arguments that bound every dependency by classifying mutual pairs such as $13\leftrightarrow61$; they are not asymptotic lower bounds for $f(n)$.

Exact computation through ten to the sixteenth

For $k>1$, $\sigma(k)\ge k+1$, so

$h(k)>k^2.$

Therefore enumerating every $k<10^8$, retaining $h(k)\le10^{16}$, and sorting the exact values determines every fiber with target at most $10^{16}$. A linear sieve computed all divisor sums; unsigned 128-bit multiplication guarded the construction, and every retained value fit in unsigned 64-bit storage.

The rerun produced $81{,}034{,}585$ retained preimages and the following collision histogram.

Fiber size

Number of target values

2

2,309,142

3

64,798

4

644

5

18

Thus

$\max_{n\le10^{16}} f(n)=5.$

A separate implementation enumerated every cubefree input $k<10^8$ and therefore every cubefree preimage of every $N\le10^{16}$. It retained $69{,}650{,}098$ inputs. There are $1{,}494{,}456$ two-point collision fibers and no larger cubefree fiber. After cancelling identical local blocks, every one of those collisions has the single signature

$2:1\leftrightarrow2,\qquad
3:0\leftrightarrow1,\qquad
7:1\leftrightarrow0,$

namely the identity $12\leftrightarrow14$, possibly multiplied by a common cubefree factor coprime to $42$. An independently written bounded-exponent census reproduces the retained count, fiber histogram, collision count, and maximum. The large rough certificates above show that this is a complete finite-range theorem, not a global classification.

For the same target range, complete censuses with input exponents at most $4$ and at most $6$ retain respectively $78{,}702{,}167$ and $80{,}497{,}691$ preimages; their maximum fiber sizes are $4$ and $5$. Exact transition-graph processing of every fiber of size at least $3$ gives maximum feedback number $2$ in both samples. These observations are finite diagnostics only.

The least target values of exact multiplicities $2$ through $5$ are

Exact multiplicity

Least target

Complete fiber

2

336

12, 14

3

333312

336, 372, 434

4

5418319872

41664, 42672, 47244, 55118

5

1584858562560

624960, 640080, 696384, 708660, 713232

The census agrees exactly with the A327153 b-file through $n=65537$. It found no violation, in this finite range, of either experimental inequality

$f(n)\le \max\{1,v_2(n)\}
\qquad\text{or}\qquad
f(n)\le\max_{p\mid n}v_p(n).$

Neither inequality is claimed as a theorem. The literal inequality $f(n)\le v_2(n)$ is false for odd values in the range, for example $f(117)=1>0=v_2(117)$. The rough-input collisions lie far outside the census range and show why small-prime projection evidence must not be extrapolated.

Complete divisor enumeration independently confirms

$f(7089671638182002688000)=6$

and

$f(106345074572730040320)=7.$

Kominers's manuscript additionally asserts an exhaustive census up to

$106345074593168029584$

and uses it to identify the least sevenfold value and exclude sixfold values below the cutoff. The posted PDF does not yet provide the advertised code archive, so those exhaustive minimality and absence assertions remain source claims in this report. The two displayed fibers themselves are independently verified.

Failed shortcuts and useful warnings

Several plausible compressions fail exactly.

The support of repeated primes is not injective. We have $h(112)=h(124)=27776$, while both powerful supports are $\{2\}$.

Even the total number of prime factors of the powerful part is not injective. The fiber

$h(35684740)=h(42608146)=3351219307843680$

has powerful parts $196=2^2\cdot7^2$ and $2401=7^4$, both with $\Omega=4$.

Local primitive-divisor arguments do not produce a descending tree. The two-cycle $13\leftrightarrow61$ above already blocks this.

General bounds for $S$-unit equations depend too strongly on the number of primes in $S$, which can be of order $\log n/\log\log n$.

Average estimates for fibers of $\sigma$, or for the range of $kF(k)$, do not imply a worst-case pointwise estimate for $f(n)$.

Independent collision blocks can multiply. The disjoint-support collisions $1984\leftrightarrow2032$ and $315\leftrightarrow351$ generate four of the five preimages of $1584858562560$.

Fractional chain covers do not remove the positive exponential rate. For $R\ge3$, the indices $2$ and $3$ are incomparable. On $s$ sufficiently large primes, every coordinatewise chain box meets the abstract cube $\{2,3\}^s$ in at most one word, so even a fractional cover has total weight at least $2^s$. The fixed-weight slice still has $\binom{s}{\lfloor s/2\rfloor}=\exp((\log2+o(1))s)$ words. These are abstract exponent words, not actual preimages; the point is that comparability alone cannot finish the proof.

Gcd-normalizing incomparable exponent indices does not restore the integer-square gap. Proposition B produces the rational square $(c/C)^2$, and $h(315)=h(351)$ has $c/C=16/9$.

The non-chain coordinate set need not hit every transition cycle, and minimum feedback sets need not be minimum information separators. Both failures occur in the exact cubefree certificates above.

A one-edge charge for every vertex-disjoint transition cycle gives the positive coefficient $1/3$, not zero. Generic directed feedback and Erdős--Pósa theorems do not supply the missing arithmetic little-$o$ estimate.

A short-interval argument cannot suffice. For rough inputs the equality places every $k$ close to $\sqrt n$, but suitably chosen integers can have exponentially many divisors in a fixed logarithmic interval. One must use the prime-valuation equations, not only divisor spacing.

These failures point to a specific remaining task. One needs a uniform theorem showing that the balanced prime-divisibility graph attached to a fiber has sublinear effective cycle rank, or an equivalent global restriction on simultaneous relations among

$\sigma(p^e)=\frac{p^{e+1}-1}{p-1}.$

Local degree bounds, finitely many small-prime valuations, and the size condition $k<\sqrt n$ are each insufficient on their own.

Post-ready partial result

The following statement is ready to post as a partial result. It must not be advertised as a solution of Problem 1060, and authorship or priority should not be assigned without the peer manuscript author's approval and a conventional literature check.

Theorem. Let $f(N)=\#\{k\ge1:k\sigma(k)=N\}$. Then

$\log\max\{1,f(N)\}
\le
\left(\frac12\log\!\left(1+\frac1{\sqrt2}\right)+o(1)\right)
\frac{\log N}{\log\log N}.$

The coefficient is $0.267399998369785\ldots$. If only cubefree preimages are counted, it may be replaced by $\frac12\log\varphi=0.240605912529801\ldots$.

The complete proof of this partial theorem is Theorem A and Corollary A above. Proposition A establishes optimality only inside the specified affine independent-chain framework. A public version should cite the random-divisibility-chain and fractional-chain precedents listed in the literature map and should state that no complete priority search has been performed.

Research verdict

The requested complete proof was not obtained. The open problem survived a literature review, several independent proof attempts, adversarial finite computation, and exact counterexample searches. The strongest asymptotic result established in this note is the independently checked chain-packing coefficient $C_1=0.267399998369785\ldots$. The investigation also gives the exact defect-square identity, the bounded-exponent and Euler-mass reductions, the feedback-set reconstruction lemma, the $1/3$ vertex-disjoint-cycle bound, the injective third-order approximant and its metric barrier, the VC, parity, and profile diagnostics, and several exact rough-input collision identities.

The exact missing step can now be approached through several alternative sufficient statements. For every fixed $R$, it would be enough to prove a positive Euler-mass gap for normalized $R$-free collisions, a sublinear bound for the true information-separator size, a uniform $o(s)$ bound for the powerful-threshold VC dimensions, or an injective global-core-normalized target profile. These statements are not asserted to be equivalent. A sublinear transition feedback set is sufficient but is stronger than a sublinear information separator; the tensor example separates the two parameters. No derivation of these statements from the cited literature or from the peer manuscript was located in the bounded search. Any proposed completion should be tested first against the coprime-to-$6$, coprime-to-$30$, coprime-to-$210$, prime-greater-than-$17$, FVS-three tensor, and $C\nmid c$ certificates recorded here.

Appendix Exact certificates

For $H(p,e)=p^e\sigma(p^e)$, the coprime-to-$6$ collision is certified by the following factorizations of the divisor-sum factor.

Left block

Factorization of $\sigma(p^e)$

Right block

Factorization of $\sigma(p^e)$

$13^2$

$3\cdot61$

$5$

$2\cdot3$

$17$

$2\cdot3^2$

$7^2$

$3\cdot19$

$31$

$2^5$

$23$

$2^3\cdot3$

$37^3$

$2^2\cdot5\cdot19\cdot137$

$31^3$

$2^6\cdot13\cdot37$

$61$

$2\cdot31$

$37^2$

$3\cdot7\cdot67$

$67^2$

$3\cdot7^2\cdot31$

$61^2$

$3\cdot13\cdot97$

$73$

$2\cdot37$

$67$

$2^2\cdot17$

$97$

$2\cdot7^2$

$137^2$

$7\cdot37\cdot73$

$137$

$2\cdot3\cdot23$

Adding the base-power valuations on either side gives

$2^{12}3^5 5\,7^4 13^2 17\,19\,23\,31^3 37^4 61^2 67^2 73\,97\,137^2.$

For the collision coprime to $30$, the left divisor sums are

$57=3\cdot19,
\quad133=7\cdot19,
\quad14=2\cdot7,
\quad993=3\cdot331,$

$38=2\cdot19,
\quad44=2^2\cdot11,
\quad62=2\cdot31,
\quad84=2^2\cdot3\cdot7,
\quad128=2^7.$

The right divisor sums are

$19608=2^3\cdot3\cdot19\cdot43,
\quad1464=2^3\cdot3\cdot61,$

$381=3\cdot127,
\quad30784=2^6\cdot13\cdot37,
\quad332=2^2\cdot83.$

Together with the base powers, both sides give

$2^{14}3^3 7^5 11^3 13\,19^3 31^3 37\,43\,61\,83\,127\,331.$

Appendix Reproducibility

The exact checks are in the directories ksigma_verification_2026-09-05 and ksigma_rough_collision_search_2026-09-05.

clang++ -std=c++20 -O3 -Wall -Wextra -Wpedantic census.cpp -o census./census 100000000python3 spot_checks.pypython3 rankin_constant.pypython3 verify_cubefree_rough210.pypython3 verify_min_euler_mass_gt11.pypython3 parity_route_verify.pypython3 verify_cubefree_girth_gt8.pypython3 verify_local_gcd_descent.pypython3 verify_avoid_2_3_31.pypython3 verify_cubefree_fvs3_tensor.py

The census command takes substantial memory because it sorts more than eighty-one million retained preimages. The spot-check program uses complete divisor enumeration for named target values and direct arbitrary-precision arithmetic for the first two rough-input collisions. The rough-$210$ command reconstructs that cubefree certificate, checks Moser-primitivity, and exhausts all subset products to check conformal indecomposability. The three added standard-library verifiers check the defect-square calculations, the 24-vertex graph and its unique feedback vertex, and the four-corner tensor with feedback number three and separator number two. Floating-point mixed-integer optimization was used only for discovery; exact integer arithmetic certifies every displayed equality.

References

1. T. F. Bloom, Erdős Problem 1060, accessed 5 September 2026.

2. R. K. Guy, Unsolved Problems in Number Theory, third edition, Springer, 2004, Problem B11.

3. P. Erdős, Remarks on number theory II Some problems on the sigma function, Acta Arithmetica 5, 1959, 171 to 177.

4. P. Noppakaew and P. Pongsriiam, Product of Some Polynomials and Arithmetic Functions, Journal of Integer Sequences 26, 2023, Article 23.9.1.

5. S. D. Kominers, On the Number of Solutions of k sigma k equals n, working paper, 2026.

6. A. Karttunen and OEIS Foundation, OEIS A327153 and linked sequences.

7. P. Pollack, Remarks on Fibers of the Sum-of-Divisors Function, 2015.

8. M. R. Gabdullin, V. V. Iudelevich, and F. Luca, Numbers of the form kf(k), International Journal of Number Theory 19, 2023, 1191 to 1204.

9. GIMPS, List of Known Mersenne Prime Numbers, accessed 5 September 2026.

10. Divisibility-chain packing and the multiplicity of k sigma k, unpublished peer manuscript supplied 5 September 2026.

11. B. Alexeev, K. Barreto, Y. Li, J. D. Lichtman, L. Price, J. I. Shah, Q. Tang, and T. Tao, Primitive sets and von Mangoldt chains Erdős Problem 1196 and beyond, arXiv 2605.00301, 2026.

12. R. P. Stanley, Two Poset Polytopes, Discrete and Computational Geometry 1, 1986, 9 to 23.

13. C. L. Monma, A. Schrijver, M. J. Todd, and V. K. Wei, Convex Resource Allocation Problems on Directed Acyclic Graphs, Mathematics of Operations Research 15, 1990, 736 to 748.

14. Y. G. Chen and Q. Q. Luo, Odd Multiperfect Numbers, Bulletin of the Australian Mathematical Society 88, 2013, 56 to 63.

15. M. Gadouleau, A. Richard, and S. Riis, Fixed points of Boolean networks, guessing graphs, and coding theory, SIAM Journal on Discrete Mathematics 29, 2015, 2312 to 2335.

16. A. Richard, Positive circuits and maximal number of fixed points in discrete dynamical systems, Discrete Applied Mathematics 157, 2009, 3281 to 3288.

17. B. Reed, N. Robertson, P. Seymour, and R. Thomas, Packing directed circuits, Combinatorica 16, 1996, 535 to 554.

18. W. H. Mills, A System of Quadratic Diophantine Equations, Pacific Journal of Mathematics 3, 1953, 209 to 220.

19. S. Bibby, P. Vyncke, and J. Zelinsky, On the Third Largest Prime Divisor of an Odd Perfect Number, INTEGERS 21, 2021, A115.

20. T. Yamada, Multiplicative structures of values of the sum-of-divisors function, 2005 preprint.

21. V. Y. Wang and M. W. Xu, Paucity phenomena for polynomial products, Bulletin of the London Mathematical Society 56, 2024, 2718 to 2726.

22. P. Drungilas and A. Dubickas, Multiplicative dependence of shifted algebraic numbers, Colloquium Mathematicum 96, 2003, 75 to 81.