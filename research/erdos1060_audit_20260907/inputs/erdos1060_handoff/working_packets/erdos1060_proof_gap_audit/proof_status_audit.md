# Erdős Problem 1060: proof-status audit and the exact missing factor

## Status

No complete solution to the unrestricted conjecture has been established in this investigation. The requested conclusion is

\[
\log\max\{1,f(N)\}=o(\log N/\log\log N),\qquad
f(N)=\#\{k\ge1:k\sigma(k)=N\}.
\]

The previous compatible-family theorem is conditional on compatibility. Its applicability to sufficiently few parts of every fiber remains unproved. The audit below does not find an error in that conditional theorem. It proves that a direct removal of its hypothesis would invalidate an essential estimate. Neither this note nor its experiments is a counterexample to the Erdős conjecture. No originality claim is made for the identities below.

## 1. An identity valid for every collision

Suppose that distinct positive integers \(a,b\) satisfy \(a\sigma(a)=b\sigma(b)=N\). Put

\[
e_p=v_p(a),\quad f_p=v_p(b),\quad g=\gcd(a,b),
\]

\[
H=\prod_p\gcd\bigl(\sigma(p^{e_p}),\sigma(p^{f_p})\bigr),
\quad R=\frac{\sigma(g)}H,
\quad T=\frac{\gcd(\sigma(a),\sigma(b))}H.
\]

Then \(R,T\) are positive integers, \(T\mid N\), and

\[
\boxed{1<(T/R)^2<\prod_{p:e_p\ne f_p}\frac p{p-1}
\le\mathcal P(N),\qquad
\mathcal P(N)=\prod_{p\mid N}\frac p{p-1}.}
\tag{1}
\]

Moreover,

\[
\boxed{R=1\ \Longleftrightarrow\
e_p+1\text{ and }f_p+1\text{ are divisibility-comparable for every }p.}
\tag{2}
\]

### Proof

For nonnegative integers \(e,f\), the geometric-sum gcd identity gives

\[
\gcd(\sigma(p^e),\sigma(p^f))
=\sigma\bigl(p^{\gcd(e+1,f+1)-1}\bigr).
\tag{3}
\]

Indeed, multiply the two divisor sums by \(p-1\), use
\(\gcd(p^r-1,p^s-1)=p^{\gcd(r,s)}-1\), and divide by \(p-1\).

The right-hand side of (3) divides \(\sigma(p^{\min(e,f)})\), since its exponent index divides \(\min(e,f)+1\). Thus \(H\mid\sigma(g)\). Also \(H\) divides both \(\sigma(a)\) and \(\sigma(b)\), by multiplying the local divisibilities. Therefore \(R,T\) are integers and \(T\mid\sigma(a)\mid N\).

Each factor

\[
\frac{\sigma(p^{\min(e_p,f_p)})}
     {\sigma(p^{\gcd(e_p+1,f_p+1)-1})}
\]

in \(R\) is an integer at least one. It is one precisely when
\(\gcd(e_p+1,f_p+1)=\min(e_p+1,f_p+1)\), equivalently when the two indices are comparable. This proves (2).

Write \(a=gu\), \(b=gv\), where \(\gcd(u,v)=1\). The collision gives
\(u\sigma(a)=v\sigma(b)\), so there is a positive integer \(t\) with

\[
\sigma(a)=vt,\quad\sigma(b)=ut,\quad
 t=\gcd(\sigma(a),\sigma(b)).
\]

Consequently,

\[
\left(\frac TR\right)^2
=\left(\frac t{\sigma(g)}\right)^2
=\frac{\sigma(a)\sigma(b)}{uv\,\sigma(g)^2}
=\prod_{p:e_p\ne f_p}
\frac{\sigma(p^{\max(e_p,f_p)})}
 {p^{|e_p-f_p|}\sigma(p^{\min(e_p,f_p)})}.
\]

If \(A>B\ge0\), then

\[
\frac{\sigma(p^A)}{p^{A-B}\sigma(p^B)}
=\frac{1-p^{-(A+1)}}{1-p^{-(B+1)}}
\in\left(1,\frac p{p-1}\right).
\]

There is at least one differing prime, so multiplication proves (1). □

The quantity that was a small integer in a compatible pair is therefore the **rational number** \(T/R\) for an arbitrary pair. Smallness of the ratio does not bound the integer \(T\).

## 2. The exact replacement for the small-label identity

Suppose additionally that \(e_p=f_p\) for every prime \(p\le Y\). For every prime \(q\le Y\),

\[
\boxed{
\sum_{p>Y}
\left|v_q(\sigma(p^{e_p}))-v_q(\sigma(p^{f_p}))\right|
=2v_q(T).}
\tag{4}
\]

To prove it, put \(A_p=v_q(\sigma(p^{e_p}))\) and
\(B_p=v_q(\sigma(p^{f_p}))\). Equality of the input exponents at \(q\), together with the collision equation, gives

\[
\sum_p A_p=\sum_p B_p=v_q(t).
\]

Also \(v_q(H)=\sum_p\min(A_p,B_p)\). Hence

\[
\sum_p|A_p-B_p|
=2v_q(t)-2v_q(H)=2v_q(T).
\]

The terms with \(p\le Y\) vanish because those input exponents were fixed. This proves (4).

When the pair is compatible, \(R=1\) and \(T<\sqrt{\mathcal P(N)}\), giving the earlier sparse-change bound. In general, the available bound is only

\[
T<R\sqrt{\mathcal P(N)},
\]

and \(R\) is uncontrolled by that argument.

## 3. The smallest illustration

For \(a=12\), \(b=14\),

\[
N=336,\quad g=2,\quad H=1,\quad R=3,\quad T=4.
\]

Thus the multiplier is \(T/R=4/3\), not an integer. The indices at the input prime 2 are 3 and 2, which are incomparable. This illustrates why the integer-square contradiction cannot be applied to arbitrary collisions.

## 4. The failure persists after fixing all small input exponents

Use the previously supplied collision

\[
\begin{aligned}
a={}&11^2 13^2 17\,19\,31\,61\,97\,127^2 271\,307^2 331\,367,\\
b={}&13\,17^2 19^2 23\,31^2 43\,61^2 83\,127\,307\,733\,5419.
\end{aligned}
\]

Then

\[
a=60629697601617236747379985403,
\quad b=61655391632564660609643619057,
\]

\[
h(a)=h(b)=
5276516179938729922490847708056660616574496169354744299520=:N.
\]

Both inputs are odd and cubefree, and all input primes exceed 7. Exact arithmetic gives

\[
H=1,\quad
R=394214768640,\quad T=436988805120,\quad
\boxed{T/R=378/341.}
\]

Their relevant factorizations are

\[
R=2^{19}3^2\cdot5\cdot7^2\cdot11\cdot31,
\qquad
T=2^{20}3^5\cdot5\cdot7^3.
\]

The exact target Euler product is

\[
\mathcal P(N)=
\frac{7228777887289039394175783661}
     {1051444089041931542200320000}.
\]

In particular \(4<\mathcal P(N)<8<9\). The cutoff \(Y=3\) satisfies
\(Y>\sqrt{\mathcal P(N)}\), and both inputs have identical exponents at 2 and 3, namely zero.

For labels

\[
\lambda_p(k)=
\bigl(v_2(\sigma(p^{v_p(k)})),v_3(\sigma(p^{v_p(k)}))\bigr),
\]

there are **16 changed base labels** between these inputs:

\[
13,17,19,23,31,43,61,83,97,127,271,307,331,367,733,5419.
\]

Dropping compatibility from the old radius estimate would allow at most

\[
\left\lfloor\frac{\log\mathcal P(N)}{\log2}\right\rfloor=2.
\]

Thus that proposed extension is false even for odd cubefree inputs with every small input exponent fixed.

The actual coordinatewise variation agrees with (4): it is 40 at prime 2 and 10 at prime 3. These equal \(2v_2(T)\) and \(2v_3(T)\), respectively. There is no contradiction with the conditional compatible-family theorem.

## 5. What the experiments certify

Run

```sh
python verify_gap.py --limit 200000 --output verification.json
```

The program uses only the Python standard library. It checks the displayed collision twice: by products of local divisor sums, and by constructing and summing all divisors of each input (20,736 divisors per input). It trial-divides every displayed prime base, verifies the supplied target factorization, and verifies all Euler-product comparisons using exact fractions.

It also computes sigma by a divisor-sum sieve for every input at most 200,000. Among 6,809 collision pairs with both inputs in that range, it verifies (1)–(4); 242 pairs are compatible and 6,567 are not. These counts include scaled copies and are not primitive-collision counts. The input-bounded sweep is not an exhaustive census of larger preimages of every target encountered.

The finite checkers from the preceding sparse-changes and chain-packing packets were also rerun successfully. These checks are not formal proof-assistant certification or a substitute for the written analytic proofs.

A further numerical search restricted to cubefree input primes between 31 and 100,000 was terminated by an external execution timeout before returning a mathematical certificate. It supports no nonexistence or existence conclusion.

## 6. The remaining statement is still unproved

Let \(C(N)\) be the minimum number of compatible subfamilies needed to partition a nonempty fiber. The preceding theorem gives

\[
\log f(N)\le\log C(N)+O((\log\log N)^{3/2}).
\]

Since the error term is negligible compared with \(\log N/\log\log N\), a uniform estimate

\[
\log C(N)=o(\log N/\log\log N)
\]

would prove the conjecture. But it has not been proved. In fact \(C(N)\le f(N)\), so, with the preceding compatible-family bound, this target is equivalent to the original assertion on the asymptotic scale in question. It identifies the unresolved part of the argument; it is not an independently established finishing lemma.

This audit supplies a general pair identity and an exact counterexample to a direct proof extension. It supplies **no improved unrestricted multiplicity bound and no complete solution**.

## Sources consulted

The previous internal note, `erdos1060_sparse_changes_proof.tex`, contains the compatible-family theorem and states its scope explicitly.

Scott Duke Kominers, *On the Number of Solutions of k sigma(k)=n*, especially Theorem 1.2 and Remark 4.3, supplies a positive-constant general bound and explains the limitations of squarefree-only exponent coloring. It does not supply the missing zero-constant theorem.
https://www.scottkom.com/assets/articles/Kominers_ksigmak.pdf

Zach Teitler, *Analytic Number Theory Notes*, Section 6.3, supplies the Mertens estimates used in the previous compatible-family asymptotics.
https://zteitler.github.io/analytic-number-theory-notes/sec-mertens.html

Direct access to the current Erdős problem page returned HTTP 403 in this pass. No current global status is inferred from that failed retrieval, and no verified full solution was found in the accessible literature inspected.
