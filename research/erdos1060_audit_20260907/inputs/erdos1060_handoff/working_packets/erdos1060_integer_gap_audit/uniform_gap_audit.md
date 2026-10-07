# Erdős 1060: real dimension is not integer ambiguity

6 September 2026

## Status and scope

The unrestricted statement

\[
\log\max(1,f(N))=o(\log N/\log\log N),\qquad
f(N)=\#\{k:k\sigma(k)=N\},
\]

has **not** been proved in this investigation. This note supplies an exact
obstruction to an overly optimistic interpretation of the proposed
linear-certificate approach. It does not disprove the conjecture, the validity
of the earlier finite certificate bounds, or the possibility of proving the
needed asymptotic estimate by a stronger integer method.

The specific result is a target with one cubefree preimage whose admissible
linear system, after all single-row integer-support eliminations, has a
three-dimensional real feasible set and a point positive in every surviving
coordinate. Thus zero-budget nonnegative row certificates cannot delete any
of those coordinates. Three elementary uses of the binary restrictions still
force the unique preimage.

The checker also enumerates all divisors of this particular target and confirms
that the unrestricted fiber has the same single member. No input-size cutoff
is used in that separate finite enumeration.

## 1. The exact indicator model

Fix an exponent cap \(E\), and factor \(N=\prod_q q^{\alpha_q}\). The admissible
local exponents are

\[
D_p=\{0\le e\le\min(E,\alpha_p):p^e\sigma(p^e)\mid N\}.
\]

For each admissible pair introduce \(x_{p,e}\in\{0,1\}\), with

\[
\sum_{e\in D_p}x_{p,e}=1,
\qquad
\sum_{p,e}v_q(p^e\sigma(p^e))x_{p,e}=\alpha_q.
\]

Write these equations as \(Ax=b\). They encode the bounded-exponent fiber
exactly. Replacing the binary conditions by \(x\ge0\) is a relaxation, not an
equivalent reformulation. Each coordinate of a nonnegative solution is at most
one by its block-sum equation.

A local option may be safely removed if some individual valuation row cannot
be completed by any choices from the other current domains. Iterating that
operation does not generally impose all the simultaneous integer constraints.

## 2. A general obstruction to zero-budget certificates

**Lemma.** Suppose \(Ax^*=b\) has a solution \(x^*>0\). If row weights \(y\)
satisfy

\[
y^{\mathsf T}A_j\ge0\quad\text{for every column }j,
\qquad y^{\mathsf T}b=0,
\]

then \(y^{\mathsf T}A_j=0\) for every column.

**Proof.** The identity

\[
0=y^{\mathsf T}b=\sum_j(y^{\mathsf T}A_j)x_j^*
\]

is a sum of nonnegative terms. Since every \(x_j^*\) is positive, every column
score must vanish. This works for real as well as rational row weights. □

The lemma concerns zero-budget certificates. It does not exclude
positive-budget bounds, additional integer-valid inequalities, or branching.

## 3. An arithmetic example inside the actual problem

Take

\[
N_0=504654433920=2^7 3^3\cdot5\cdot7^2\cdot13\cdot19^2\cdot127.
\]

The candidate input is

\[
k_0=3\cdot5\cdot7\cdot13\cdot19^2=492765.
\]

Its divisor sum is

\[
\sigma(k_0)=4\cdot6\cdot8\cdot14\cdot381=1024128,
\]

and \(k_0\sigma(k_0)=N_0\).

For cap \(E=2\), the initially admissible domains are

\[
\begin{aligned}
D_2=D_3=D_7=D_{19}&=\{0,1,2\},\\
D_5=D_{13}=D_{127}&=\{0,1\}.
\end{aligned}
\]

There are 18 local-option indicators. The only option removed by iterated
single-row integer-support propagation is exponent zero at 19. In the
19-adic row the equation is

\[
x_{19,1}+2x_{19,2}+x_{7,2}=2.
\]

If \(e_{19}=0\), the other terms supply at most one. Hence this option is
impossible. The exact checker verifies that each of the 17 remaining options
has a completion in each individual valuation row, so this particular
propagation operation is at a fixed point.

The surviving coefficient matrix has 17 columns and exact rational rank 14.
The following parameterization gives all its real solutions. Set

\[
u=x_{7,1},\qquad v=x_{13,1},\qquad t=x_{127,1}.
\]

| Prime | \(x_{p,0}\) | \(x_{p,1}\) | \(x_{p,2}\) |
|---|---:|---:|---:|
| 2 | \(3-2v-4t\) | \(u+3v+6t-4\) | \(2-u-v-2t\) |
| 3 | \(u+2v+5t-3\) | \(3-u-v-5t\) | \(1-v\) |
| 5 | \(t\) | \(1-t\) | inadmissible |
| 7 | \(1-u-t\) | \(u\) | \(t\) |
| 13 | \(1-v\) | \(v\) | inadmissible |
| 19 | removed | \(t\) | \(1-t\) |
| 127 | \(1-t\) | \(t\) | inadmissible |

Substitution verifies the equations. For completeness, exact Gaussian
elimination gives rank 14, and the three parameter directions are independent
because their coordinates at \((7,1),(13,1),(127,1)\) form the identity matrix.
Consequently the parameterization is exhaustive, not just a subfamily of
solutions.

### A positive fractional solution

Choose

\[
(u,v,t)=\left(\frac13,\frac23,\frac13\right).
\]

The resulting probabilities, in increasing order of the surviving exponent
domains, are

| Prime | Domain | Coordinate values |
|---|---|---|
| 2 | 0, 1, 2 | 1/3, 1/3, 1/3 |
| 3 | 0, 1, 2 | 1/3, 1/3, 1/3 |
| 5 | 0, 1 | 1/3, 2/3 |
| 7 | 0, 1, 2 | 1/3, 1/3, 1/3 |
| 13 | 0, 1 | 1/3, 2/3 |
| 19 | 1, 2 | 1/3, 2/3 |
| 127 | 0, 1 | 2/3, 1/3 |

Every surviving coordinate lies strictly between zero and one. A neighborhood
of this parameter triple is therefore feasible over the reals, proving that
the feasible real set really has dimension three.

By the lemma in Section 2, no nonnegative zero-budget row certificate can
remove any of these 17 surviving columns, no matter how its weights are
chosen.

### The integer fiber is nevertheless a singleton

For a binary solution, \(u,v,t\) are themselves binary. The first entry of the
parameterization gives

\[
x_{2,0}=3-2v-4t\ge0.
\]

If \(t=1\), the right-hand side is at most \(-1\), which is impossible.
Therefore \(t=0\). Next,

\[
x_{2,0}=3-2v\le1
\]

forces \(v=1\). Finally,

\[
x_{2,1}=u-1\ge0
\]

forces \(u=1\). Substitution gives exactly the exponent vector of \(k_0\).
Thus

\[
\boxed{f_2(N_0)=1.}
\]

These are elementary integer-valid deductions. For example,
\(4t+2v+x_{2,0}=3\), together with nonnegativity, implies \(t\le3/4\);
its integrality upgrades this to \(t=0\). That rounding is valid for the binary
problem and is false as an exclusion of all fractional feasible points.

### Separate check of the unrestricted fiber

Every preimage divides \(N_0\). The checker enumerates all

\[
(7+1)(3+1)(1+1)(2+1)(1+1)(2+1)(1+1)=2304
\]

divisors of \(N_0\), using the full target exponent bounds rather than cap two,
and evaluates their \(h\)-values exactly. It finds

\[
\boxed{f(N_0)=1,\qquad h^{-1}(N_0)=\{492765\}.}
\]

This complete finite enumeration is not used to justify the three-dimensional
cubefree parameterization or the binary proof above.

## 4. Exactly what this does and does not rule out

It rules out the shortcut that sufficient zero-budget nonnegative linear
certificates must remove all fractional degrees of freedom whenever an
arithmetic fiber has a unique integer preimage. They cannot remove a single
one of the surviving coordinates in this example.

It does **not** disprove a uniform subexponential bound on residual nullity:
three is a small constant. It also does not invalidate the earlier bound
\(f_E(N)\le2^{m-r}\), which gives \(1\le8\) here. It does not rule out the
positive-budget certificate formulation or more powerful sound domain
reductions. Global integer reasoning already resolves this particular case.

What remains missing is a uniform theorem controlling the integer choices
that survive all proposed reductions. Solving more particular targets, or
finding more row weights, does not prove such a theorem.

## 5. The actual objects that need counting

For any one feasible binary assignment \(x^{(0)}\), put

\[
\Lambda_N=\{z\in\mathbb Z^m:Az=0\}.
\]

The exact fiber is in bijection with

\[
\Lambda_N\cap\prod_{j=1}^m[-x_j^{(0)},1-x_j^{(0)}].
\]

Indeed, an integer point in this box gives a binary vector
\(x=x^{(0)}+z\), and \(Ax=b\) holds precisely when \(Az=0\). Conversely,
every binary solution gives such a lattice point.

This is an exact reformulation, **not a new upper bound**. It explains why the
real dimension can exaggerate the ambiguity. A useful finishing argument
must exploit special arithmetic properties of the divisor-sum matrix to
bound these box-constrained integer points, or prove a uniformly inexpensive
branching/rounding procedure. No such bound is supplied here.

The existing reduction would finish Erdős 1060 if one proved, for every fixed
cap \(E\),

\[
\log\max_{M\le X}\max(1,f_E(M))=o_E(\log X/\log\log X).
\]

That estimate is still not established. It must not be inserted as an
unproved lemma into a purported completion.

## 6. Verification and literature check

Run

```text
python3 verify_fractional_obstruction.py
```

The script uses only the Python standard library. It rebuilds all admissible
options; repeats single-row exact-support pruning; computes rational rank;
checks the affine parameterization on a basis; checks the positive rational
point; exhausts all eight binary parameter triples; and independently sums
all 48 divisors of the indicated input. It then enumerates all 2,304 target
divisors to check the unrestricted fiber. It writes `verification.json`.

The finite model and the zero-/positive-budget certificate bounds are from
the preceding internal note, `erdos1060_exact_certificates.tex`. Their validity
is not being challenged; the required uniform estimate was explicitly
unproved there.

A related external source inspected in this pass was Marley Young,
*On multiplicatively dependent vectors of polynomial values*,
arXiv:2402.13704v1, especially Proposition 1.7 and Theorem 1.8:
https://arxiv.org/html/2402.13704v1 . Its results count bounded-height tuples for
specified collections of polynomials; their parameters and constants do not
immediately supply a uniform bound for the maximal fiber here when the
number of input primes grows. No applicable completion theorem was obtained
from that source. Direct retrieval of the current Erdős problem page failed,
so no current global status is inferred from that failed lookup.

**Conclusion:** this is a finite exact obstruction and an audit of the proposed
completion mechanism, not a solution of the unrestricted conjecture. No
originality, independent human referee review, or proof-assistant certification
is claimed.
