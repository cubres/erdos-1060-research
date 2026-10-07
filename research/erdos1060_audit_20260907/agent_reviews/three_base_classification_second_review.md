# Second independent review: cubefree exchanges on three changed bases

Date: 7 September 2026.

Reviewed proof: Section 3 of `independent_exchange_review.md`, produced by the separate `independent_proof` agent. I first derived the transition cases independently and then compared every case and auxiliary lemma with that proof. No computational census was used as a premise.

## Accepted theorem

Let `h(n)=n sigma(n)`. If `h(a)=h(b)`, both inputs are cubefree, and exactly three prime bases have different exponents, then

\[
\{a,b\}=\{12d,14d\},\qquad \gcd(d,42)=1,
\]

where `d` is cubefree. Equivalently, canceling every common full local block at unchanged bases leaves exactly `{12,14}`.

I found no omitted transition pattern or prime-ordering case. This is a verified restricted theorem in the current investigation; no literature-priority assertion or implication that Erdős 1060 is solved follows.

## Coverage of the cases

At a changed base `p`, the ratio of the higher to lower local value is

\[
L_p=p(p+1),\quad S_p=p^2(p^2+p+1),\quad
J_p=S_p/L_p=p^2+\frac p{p+1}.
\]

The denominator of `J_p` in lowest terms is exactly `p+1`: `p^2+p+1` is 1 modulo `p+1`, and `p` is coprime to `p+1`. Every ratio exceeds one. With three changed bases, any equality therefore has one ratio on one side and two on the other.

| Number of `J` ratios | All possible shapes | Independent audit |
|---|---|---|
| 0 | One integer ratio equals two integer ratios | Every index pair is comparable; the Euler product of three primes is at most `15/4<4`, so the integer-square obstruction rules this out. |
| 1 | `J_p` alone, or `J_p I_q=I_r`, with each `I` equal to `L` or `S` | The first is nonintegral; all four forms in the second case are handled below. |
| 2 | `J_p I_r=J_q`, or `J_p J_q=I_r` | Denominator divisibility contradicts monotonicity in the first form. Parity and the exceptional calculation `J_2 J_13=793` rule out the second. |
| 3 | `J_p J_q=J_r` | `r>pq` and denominator divisibility force `r+1=(p+1)(q+1)`, contradicting the size of the ratios. |

For the one-`J` forms:

- `J_p L_q=L_r` implies `r>pq`, then `r | p^2+p+1` and `p | r+1`. The mixed-divisibility lemma forces `(p,r)=(2,7)`, and then `q=3`.
- `J_p S_q=L_r` implies `r>pq^2>q^2+q+1`, then the same mixed pair `(2,7)`, incompatible with `r>2q^2`.
- `J_p S_q=S_r` is excluded by 2-adic valuations unless `q=2`; then denominator and valuation constraints force `p=3`, but `28J_3=273` is squarefree.
- `J_p L_q=S_r` has all small-prime cases explicitly excluded. For odd primes, monotonicity places `r` strictly between `p` and `q`. Both possible orders are handled, as detailed next.

## The delicate mixed form

Suppose `J_p L_q=S_r`, all three primes odd. Integrality gives

\[
p+1\mid q(q+1).
\]

If `p<q`, monotonicity of both `J_x` and `L_x`, together with `S_x=J_xL_x`, gives `p<r<q`. Since `q>p+1`, the integer `p+1` is coprime to the prime `q`; thus `c=(q+1)/(p+1)` is an integer. The equation becomes

\[
r^2(r^2+r+1)=c p q(p^2+p+1).
\]

The prime `q` divides `r^2+r+1`. If `r|c`, then `r|q+1`, contradicting the mixed-divisibility lemma for the odd pair `r<q`. Hence `r` does not divide `c`, so `r^2|p^2+p+1`. This is impossible because `p<r` are distinct odd primes and `p^2+p+1<r^2`.

If `p>q`, monotonicity gives `q<r<p`. From `p+1|q(q+1)` and `p+1>q+1`, it follows that `q|p+1`: otherwise coprimality with the prime `q` would give `p+1|q+1`, a contradiction. Put

\[
c=(p+1)/q,\qquad t=(q+1)/c.
\]

Here `c` is a positive even integer and divides `q+1`. Therefore `t` is a positive integer with `t<r`, and the equation becomes

\[
r^2(r^2+r+1)=t p(p^2+p+1).
\]

It follows that `r^2|p^2+p+1`, while `p|r^2+r+1`. This contradicts the mutual-quadratic lemma. All divisibility deductions retain the full equation, including the multiplicity two at the base `r`.

## Review of the auxiliary lemmas

The mixed-divisibility lemma, including its small-prime exceptions, is correct. For `p<r`, `r|p^2+p+1` and `p|r+1` imply

\[
2p-1\le r\le p+2+\frac3{p-1}.
\]

This excludes `p>=5`; `p=3` fails directly, and `p=2` gives exactly `r=7`.

The mutual-quadratic lemma is also correct with its supplied self-contained descent. For a coprime positive pair `1<x<y` with the two mutual divisibilities, put `z=(x^2+x+1)/y`. The inequalities give `1<=z<x`; `z=x` would imply `x|1`. The pair `(z,x)` is coprime and satisfies the same two divisibilities. The integer

\[
m=\frac{x^2+y^2+x+y+1}{xy}=\frac{z+y+1}{x}
\]

is invariant. Descent terminates at `(1,1)` or `(1,3)`, both with `m=5`. Consequently, for distinct mutual-divisibility primes `a,b`,

\[
a^2+b^2+a+b+1=5ab.
\]

If `a^2|b^2+b+1`, then `a|5b-1`. Multiplying the latter quadratic congruence by 25 gives `a|31`, hence `a=31`. The discriminant for `b` is then `19744`, strictly between `140^2` and `141^2`. This contradiction excludes a squared cross contribution in either direction. Every descent and discriminant step checks exactly.

## Consequences and limitation

After fixing the input exponent at 2 alone, two distinct cubefree solutions of the same target differ at at least four prime bases. The existing fixed-two-prime theorem excludes distances one and two, and the new classification excludes distance three in such a part, because every pair `12d` and `14d` has different exponents at 2. Fixing the exponent at 3 or at 7 would work as well.

For exchanges whose changed bases all exceed 7 and whose Euler product is at most four, at least four bases change and at least one has positive exponent on both sides. The latter base contributes exponent sum at least three. Therefore the exchange target satisfies

\[
\log H>\sum_{p\in S}(a_p+b_p)\log p>6\log y
\]

when all changed primes exceed `y>=7`. A nonempty disjoint collection then has size strictly less than `log N/(6 log y)`.

This improves a finite support charge but retains a positive constant when `y` is comparable to `log N`. It also does not bound the number of overlapping alternative exchanges. The unrestricted little-o theorem remains unproved.
