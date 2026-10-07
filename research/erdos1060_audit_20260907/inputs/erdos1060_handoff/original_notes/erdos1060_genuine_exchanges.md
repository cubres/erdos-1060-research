# Genuine integer exchanges for k sigma(k) = N

6 September 2026

## Status

The unrestricted estimate

\[
\log\max(1,f(N))=o(\log N/\log\log N)
\]

has not been proved in this investigation. This note gives a decomposition into actual integer exchanges, finite verification of that decomposition, and a valid weighted counting inequality. It supplies **no new uniform asymptotic estimate**. The decomposition is an elementary specialization of conformal decomposition in an integer kernel, often described using Graver bases; no novelty claim is made for that general principle.

In particular, an algorithm that first enumerates a complete fiber and then finds its minimal exchanges does not constitute an independent upper bound on all fibers. That is how the finite exchange dictionaries below were obtained. Their local identities and support minimality are then checked separately.

## 1. Exact exchanges

Write
\[
h(k)=k\sigma(k),\quad \mathcal F_E(N)=\{k:h(k)=N,\ v_p(k)\le E\text{ for every }p\}.
\]
The unrestricted fiber is permitted by removing the cap. Assume this fiber is nonempty and choose a reference
\[
k_0=\prod_{p\mid N}p^{a_p}.
\]
An exchange consists of a nonempty set of prime bases \(S\subseteq\{p:p\mid N\}\), together with replacement exponents \(b_p\ne a_p\) for \(p\in S\), satisfying
\[
\boxed{\prod_{p\in S}h(p^{a_p})=\prod_{p\in S}h(p^{b_p}).}\tag{1}
\]
Exponents obey the cap when one is imposed. Put
\[
u=\prod_{p\in S}p^{a_p},\qquad v=\prod_{p\in S}p^{b_p},\qquad d=k_0/u.
\]
Because the full prime-power blocks at the changed bases were removed, both \(u\) and \(v\) are coprime to \(d\). Thus (1) implies
\[
h(dv)=h(d)h(v)=h(d)h(u)=h(k_0)=N.
\]
This exchange therefore produces an actual input, not merely a fractional solution or an internally consistent filling of some valuation rows.

An exchange is **support-minimal** if no proper nonempty subset of its changed bases, with the same replacements, satisfies (1). These are minimal changes of entire local options, not necessarily primitive collisions in Moser's different common-divisor sense.

### Decomposition lemma

Every other input in \(\mathcal F_E(N)\) can be obtained from \(k_0\) by applying a collection of support-minimal exchanges with pairwise disjoint sets of changed bases. Conversely, every such collection produces a member of \(\mathcal F_E(N)\).

**Proof.** Let \(k\) be another member and set
\[
S=\{p:v_p(k)\ne a_p\},\qquad b_p=v_p(k).
\]
Canceling all equal local factors in \(h(k)=h(k_0)\) yields (1) on \(S\). Select an inclusion-minimal nonempty subset satisfying it. Its replacement is an exchange. Dividing the equality on \(S\) by the equality on this subset leaves the same equality on the complementary bases. Repeat. Finiteness gives a disjoint partition into minimal exchanges.

Conversely, all selected local equalities can be multiplied when their changed-base sets are disjoint. Their unchanged complementary prime-power blocks remain coprime to every replacement, so the resulting input has h-value N. Its local exponents remain within the cap. □

In the one-hot indicator model \(Ax=b\), a true difference has a \(+1\) and a \(-1\) in each changed prime block. A conformal integer-kernel summand must take both or neither, because its block-sum row is zero. Consequently conformal decomposition is exactly the disjoint-base decomposition above. The general Graver-basis characterization is described in Dinh Van Le and Tim Römer, *Equivariant lattice bases*, Definition 2.2 and Remark 2.3 [1]. No symmetry-based uniform finiteness theorem from that source is being transferred to the prime-dependent arithmetic matrix.

## 2. Correct finite counting bounds

Let \(\Gamma(k_0)\) be all minimal exchanges based at \(k_0\). Make a graph on these exchanges, joining two when their changed-base sets intersect. Let \(Z(k_0)\) be the number of independent sets, including the empty set. The lemma gives a surjection from these independent sets to the fiber, and therefore
\[
\boxed{f_E(N)\le Z(k_0).}\tag{2}
\]
This need not be a bijection on the basis of the decomposition argument alone. Different decompositions might have the same endpoint. The verifier checks uniqueness of decomposition only in the finite examples examined here.

For comparison, in the abstract binary system \(x_1+x_2=x_3+x_4\), relative to the zero solution, the four minimal exchanges switch one coordinate from each side. There are seven disjoint collections but only six solutions: \((1,1,1,1)\) has two decompositions. This is an abstract example, not a claimed divisor-sum collision.

Put \(g=|\Gamma(k_0)|\), and let \(\nu\) be the largest size of a pairwise disjoint collection. Distinct individual exchanges have distinct endpoints, and all subcollections of a fixed disjoint collection also have distinct endpoints. Hence
\[
\boxed{\max\{g+1,2^\nu\}\le f_E(N)\le Z(k_0)
\le\sum_{j=0}^{\nu}\binom gj.}\tag{3}
\]
The left inequalities show that numerous true alternatives, or numerous independent true exchanges, would produce genuine multiplicity. Neither kind of implication held for merely potential feedback cycles.

### A weighted bound

For each exchange \(\gamma\), let
\[
H_\gamma=h\!\left(\prod_{p\in S_\gamma}p^{a_p}\right).
\]
This is greater than one: otherwise the old input part would be one and the new input part would also have h-value one, making a nontrivial exchange impossible.

For every disjoint collection \(I\),
\[
\prod_{\gamma\in I}H_\gamma\mid N.
\]
Indeed its old input blocks are pairwise coprime unitary factors of \(k_0\). Thus, for every \(\theta>0\),
\[
\begin{aligned}
f_E(N)&\le Z(k_0)\\
&\le N^\theta\sum_{I\text{ independent}}\prod_{\gamma\in I}H_\gamma^{-\theta}\\
&\le N^\theta\prod_{\gamma\in\Gamma(k_0)}(1+H_\gamma^{-\theta}).
\end{aligned}\tag{4}
\]
The last inequality deliberately discards the overlap restrictions and can be very wasteful. Equation (4) is a proved finite inequality, not a proved asymptotic estimate for its right-hand side.

## 3. A complete seven-preimage example

Take
\[
N_7=106345074572730040320=2^{28}3^3\cdot5\cdot7\cdot13\cdot31\cdot127\cdot8191,
\]
with reference
\[
k_0=5079674880=2^{12}3^2\cdot5\cdot7\cdot31\cdot127.
\]
This target and its seven preimages are given in Kominers [2, Section 5]. The full fiber was rechecked here by evaluating every one of the 7,424 positive divisors of this particular target; this is not a reproduction of the source's separate global minimality census.

The exact minimal exchanges relative to the reference are:

| Label | Old input block | New input block | Changed bases |
|---|---:|---:|---|
| A | \(2^{12}\cdot127\) | \(2^6\cdot8191\) | \(2,127,8191\) |
| B | \(2^{12}\cdot31\) | \(2^4\cdot8191\) | \(2,31,8191\) |
| C | \(3^2\cdot5\cdot7=315\) | \(3^3\cdot13=351\) | \(3,5,7,13\) |
| D | \(2^{12}\cdot7\) | \(2^2\cdot8191\) | \(2,7,8191\) |

Each row gives equal h-values on its two sides. The first, second and fourth identities are the elementary Mersenne construction; the third is \(315\cdot624=351\cdot560=196560\).

A, B and D pairwise overlap. C overlaps D but is disjoint from A and B. The complete independent-set list is
\[
\varnothing,\quad\{A\},\quad\{B\},\quad\{C\},\quad\{D\},\quad\{A,C\},\quad\{B,C\}.
\]
They give the seven distinct inputs
\[
\{5079674880,5119047360,5242895280,5660209152,
5704081344,5804634060,5842083312\}.
\]
The exchange dictionary is complete because the fiber is independently enumerated. Every proper subset of each proposed minimal exchange is separately excluded by exact rational subset-product computation. Thus this is a finite completeness check, not a claim that all exchange dictionaries have four members.

## 4. Other completed checks

The standard-library verifier considers five specified target/cap pairs. The table uses the least preimage as reference.

| Target/cap | Exact fiber size | Minimal exchanges | Disjoint collections | Largest endpoint decomposition count |
|---|---:|---:|---:|---:|
| The previous 29-digit-input target M, cap two | 2 | 1 | 2 | 1 |
| 336M, cap two | 4 | 2 | 4 | 1 |
| N7, unrestricted | 7 | 4 | 7 | 1 |
| The specified six-preimage target, unrestricted | 6 | 5 | 6 | 1 |
| The specified nine-preimage target, unrestricted | 9 | 5 | 9 | 1 |

Here
\[
M=5276516179938729922490847708056660616574496169354744299520.
\]
For 336M, the two disjoint exchanges are the previously known 17-base exchange for M and the exchange \(12\leftrightarrow14\). They generate its four cubefree preimages.

The six- and nine-preimage targets are
\[
N_6=7089671638182002688000
=2^{31}3^2 5^3\cdot7\cdot13\cdot31\cdot127\cdot8191,
\]
\[
N_9=1826980530660612389572800675840
=2^{45}3^3\cdot5\cdot7\cdot13\cdot31\cdot127\cdot8191\cdot131071.
\]
Their full fibers were independently checked by evaluating all 12,288 and 23,552 target divisors respectively. No minimality or record claim is made.

The dictionary depends on the reference: for N7, the reference 5804634060 has six minimal exchanges instead of four. The verifier checks every reference in all five fibers. In these finite tests every endpoint happens to have a unique disjoint decomposition; no general uniqueness claim follows.

### Reproduction

Run `python3 verify_exchanges.py` in the accompanying folder with Python 3.10 or later, without Python's `-O` option. The program uses only the standard library. It:

1. Completely enumerates the requested finite fibers using the exact valuation solver, which has explicit resource limits and raises an error on an incomplete search.
2. Independently scans every target divisor for N6, N7 and N9.
3. Constructs and sums every divisor of every returned input to verify its divisor sum.
4. Extracts all minimal exchanges from each complete fiber.
5. Independently checks each exchange's minimality by meet-in-the-middle exact rational subset products.
6. Enumerates all disjoint collections, checks their endpoints, and confirms coverage of the complete fiber.

It writes `verification.json`. The checker has been run successfully. It is exact computational verification, not formal proof-assistant certification or independent human referee review.

## 5. The missing uniform estimate is not supplied

The established fixed-cap reduction would finish Erdős 1060 if, for every fixed E,
\[
\log\max_{M\le X}\max(1,f_E(M))=o_E(\log X/\log\log X).
\]
The exchange lemma proves a decomposition and valid counting bounds. It does not bound the number, overlaps, or target costs of the genuine exchanges uniformly as N varies. Proving that all these dictionaries give small enough packing counts is an additional arithmetic theorem, not a consequence of conformal decomposition.

Nor can one claim a complete proof by first enumerating the unknown fiber, constructing its exchange dictionary, and then reporting the size of that dictionary. The finite computation is informative about particular targets, but circular as a uniform upper-bound argument.

A sufficient way to use (4) would be to find parameters with
\[
\theta_N\log N=o(\log N/\log\log N),\qquad
\sum_{\gamma\in\Gamma(k_0)}\log(1+H_\gamma^{-\theta_N})
=o(\log N/\log\log N).
\]
Neither estimate has been established here. In particular, the second can be much stronger than necessary because it discards overlap constraints. These are not being introduced as proved finishing lemmas.

**Conclusion:** the requested complete proof is not obtained. This continuation replaces potential graph choices by exact integer exchanges and verifies the distinction on finite fibers, but establishes no improved unrestricted multiplicity bound.

## Sources

[1] Dinh Van Le and Tim Römer, *Equivariant lattice bases*, arXiv:2309.07246v1, Definition 2.2 and Remark 2.3. The cited general fact is conformal decomposition in an integer kernel; the arithmetic specialization is proved above.
https://arxiv.org/html/2309.07246v1

[2] Scott Duke Kominers, *On the Number of Solutions of k sigma(k)=n*, Section 5. The specified seven- and six-preimage targets are literature examples; this note reproduces their individual complete fibers, not the much larger minimality census.
https://www.scottkom.com/assets/articles/Kominers_ksigmak.pdf

[3] The previous internal note, *Universal feedback versus actual arithmetic ambiguity for k sigma(k)=N*, 6 September 2026. It establishes the two-prime rigidity results and the conditional obstruction to counting all potential positive cycles, while explicitly leaving the unrestricted problem unproved.
