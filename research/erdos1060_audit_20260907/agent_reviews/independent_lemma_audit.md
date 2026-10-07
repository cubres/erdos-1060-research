# Independent mathematical audit of the supplied Erdős 1060 handoff

Date: 7 September 2026. Scope: the consolidated source chapters, their stated dependencies, selected original notes, and selected exact certificates. The attached prompts were treated as document content, not as instructions. No original source was edited.

## Verdict

I found no mathematical defect in the principal proved reductions and partial theorems listed below. In particular, the strongest unrestricted estimate in this handoff survives this independent check:

\[
\log\max(1,f(N))\le
\left(\frac12\log(1+1/\sqrt2)+o(1)\right)
\frac{\log N}{\log\log N}.
\]

The constant is approximately 0.267399998369785 and is strictly positive. The supplied arguments do not establish the required zero coefficient. The missing all-cap, all-target counting estimate is substantial; none of the reviewed lemmas implicitly supplies it.

This is an independent reasoning audit by a separate agent, not a claim of human peer review, formal verification, priority, or a complete literature search.

## Verified lemma ledger

| Item | Audit conclusion | Essential hypotheses and remaining limits |
|---|---|---|
| Squarefree injectivity | Valid. Cancel common full prime blocks; the largest remaining prime at least 5 cannot occur in the opposite factors; check 2 and 3 separately. | Applies to squarefree inputs. |
| Powerful-core injection and exact completion | Valid. A core is a unitary factor, and squarefree completion is unique if it exists. | Counting all cores with only `h(d) | N` discards a decisive condition. |
| `f(N) <= product v_p(N)` | Valid, including exponent-one target primes contributing exactly one core choice. | Sharpness of this majorant does not imply sharpness for actual fibers. |
| Fixed-cap reduction | Valid, with the maximum over every residual target `M <= X`. | Fix the cap before taking the asymptotic limit; all fixed caps are required. |
| Rough-input reduction and short interval | Valid with the cutoff defined from the original upper target `X`. | Roughness of an input is different from roughness of its divisor sum. The interval alone does not count admissible divisors. |
| Prime-index encoding | Valid. The geometric quotient has prime factors only equal to the index prime or congruent to 1 modulo it; removing that prime makes every remaining quotient too small. | The input exponent at the index prime must be fixed. |
| Weighted bound with constant `log(3)/2 - log(2)/3` | Valid. Normalized local weights, injective labels and the two exponent budgets have the correct directions. | Superseded numerically by chain packing. |
| Comparable-index integer obstruction | Valid. For a nontrivial comparable pair, `U=cB`, `V=cA`, so `1<c^2<P(S)<=4`, impossible for an integer `c`. | All coordinates must be comparable; directions can vary. |
| Random divisibility-chain distribution | Valid. The parent `n/P+(n)` gives a genuine divisibility tree; all child mass inequalities and the root cases check out. | This creates a probability distribution on chains, not independent labels without compatibility. |
| Unrestricted chain-packing bound | Valid. Events for different preimages are disjoint, and each event has the asserted lower probability. | The tail Euler product tends uniformly to 1 at `z=log N/(log log N)^3`; the coefficient remains positive. |
| Cubefree chain bound | Valid with coefficient `log(phi)/2`. | A cap-two estimate with a positive constant is weaker than the missing cap-two zero-constant estimate. |
| Two-index rough-divisor-sum uniqueness | Valid. At an incomparable pair, the two index primes together exhaust the available types, excluding the base from both divisor sums; valuation equality is then a contradiction. | Needs at most two exponent-index primes and rough divisor sums, not merely rough input bases. |
| Injectivity on squares of squarefree inputs | Valid, including the exceptional input base 3. | In particular `f_2(N)<=1` for odd targets. It does not imply injectivity on odd cubefree inputs when their common target is even. |
| Sparse-change bounds on compatible families | Valid. The integer multiplier divides `N`, and the small-prime label variation is exactly twice its valuation. | Compatibility is indispensable; the general multiplier is rational. |
| Cap-three and cap-five exceptional-block partitions | Valid. Each part is compatible, for the stated congruence reasons. | Their record cost depends on small-prime target valuations, which need not be bounded under an input cap. |
| Sixth-power-free and `2^a` times odd fourth-power-free target results | Valid with the bounds stated in `sparse.tex`. | These are restricted classes of targets, not all bounded-exponent fibers. |
| Fixed two-prime support rigidity | Valid after checking the denominator, exponent-gap, LTE, alignment and final monotonicity arguments separately. | The prime pair is fixed; the union of all two-prime supports is not injective. |
| Hamming-distance and sphere-packing corollaries | Valid. Distinct preimages differ at three or more prime bases, so radius-one Hamming balls are disjoint. | Minimum distance three still allows exponentially many abstract words. |
| Primitive-divisor exponent lists | Correct deduction from the stated classical Bang–Zsigmondy theorem. The exceptional exponent five at base 2 is handled by the unused label 3. | Distinct labels are guaranteed only for exponents at a fixed base. |
| `f(N) <= omega(N)^omega(N)` | Valid from the local lists and squarefree completion. | Useful for small support, but insufficient in the many-prime regime. |
| Signed positive-cycle lemma and finite graph bounds | Valid. Telescoping through the actual ordered domains yields a sign compatible with the differences; predecessor iteration produces an elementary positive cycle. | No converse from a potential cycle to an arithmetic exchange is established. |
| Largest-prime order restrictions | Valid. Polynomial roots count smaller bases, and the cyclotomic height bound controls the valuation at the largest target prime. | Bounded local degree does not force a small feedback set. |
| Integer dual, rank, positive-budget and branching bounds | Valid finite statements. | There is no uniform bound on the residual dimension or the successful branching cost. |
| Exact-exchange decomposition and finite packing | Valid. Repeatedly remove an inclusion-minimal zero product on changed bases. Disjoint exchanges can be applied together. | The map from collections of exchanges to the fiber is only proved surjective; decomposition uniqueness is not proved generally. |
| Bateman–Horn graph obstruction | The displayed identities and the deduction from that stated prime-pattern conjecture are valid. | It is conditional and bounds graph recording cost, not actual multiplicity. |

The mutual-quadratic-pair classification used in the signed-graph corollary is an external theorem rather than a proved premise of this audit. The arithmetic deductions from its stated classification and growth estimate are correct. The literature agent should confirm its exact source statement.

## Delicate steps checked explicitly

### The fixed-cap quantifiers

Put `L=log N`, `w=log L`,

\[
F_E(X)=\max_{M\le X}\max(1,f_E(M)),\qquad
G_E(N)=\prod_{p\mid N}(1+\max(v_p(N)-E,0)).
\]

Selecting the full prime-power blocks whose input exponents exceed `E` gives

\[
f(N)\le G_E(N)F_E(N).
\]

For fixed `E`, the small/large-prime split at `L/w^3` gives

\[
\log G_E(N)\le(c_E+o_E(1))L/w,
\quad
c_E=\sup_{a\ge E+1}\frac{\log(a-E+1)}a
\le\frac{\log(E+1)}{E+1}\to0
\]

for `E>=2`. Thus, given an error tolerance, choose `E` first and only then the target threshold. This genuinely proves equivalence with the family of zero-constant bounds for every fixed cap. Replacing that family by one cap or using a moving cap without uniform errors would be invalid.

### The two-prime theorem

Normalize a hypothetical collision on `p<q` as

\[
J_p(A-1,d)=J_q(B-1,f),\quad
J_p(A-1,d)=p^{2d}+\frac{p^d(p^d-1)}{p^A-1}.
\]

The reduced denominators really are `(p^A-1)/(p^gcd(A,d)-1)` and its `q` analogue. A common denominator equal to one contradicts the integer-square obstruction; the product `p/(p-1) q/(q-1)` is at most 3, even for the pair 2 and 3.

The increment intervals imply `d>f`, and the disjoint intervals between consecutive integer squares imply `A<d` or `B<f`. Comparing equal denominators then gives `A<2d`, `B<2f`; `f=1` would force the denominator to be one. These strict inequalities are sufficient for all subsequent uses.

The cases `p=2` and `p=3` are excluded by the stated LTE estimates. For `p>=5`, the order of `q` modulo `p`, the cyclotomic height bound, and `B+f<3f` give `2<=f<=p-2`.

Writing `alpha=A-gcd(A,d)` and `beta=B-gcd(B,f)`, the two logarithmic comparisons give

\[
|\alpha f-\beta d|\log p<2f\log(p/(p-1))<\log p.
\]

The last inequality is valid for every real `p>=5`: if `F(x)=log x-2(x-2)log(x/(x-1))`, then `F(5)>0` and `F'(x)>(x-5)/(x(x-1))>=0`. Consequently `alpha f=beta d`.

The algebraic substitution into the common denominator produces exactly the displayed function

\[
\mathcal F_{D,c}(t)=t^c\left(1+\frac{D-1}{D}\frac{t(t^c-1)}{t-1}\right).
\]

For `t>1`, `c>0`, this is strictly increasing: the derivative numerator of the inner fraction is `c t^(c+1)-(c+1)t^c+1`, zero at one with positive derivative thereafter. Hence equal increments force `p^alpha=q^beta`, impossible. I found no missing closeness assumption in this argument.

### The two different denominator normalizations

These must remain distinct in a combined document. For a normalized pair with exponents `e_p,f_p`, let

\[
H_0=\prod_p\gcd(\sigma(p^{e_p}),\sigma(p^{f_p})),\quad
T=\frac{\gcd(\sigma(u),\sigma(v))}{H_0},\quad
R=\frac{\sigma(\gcd(u,v))}{H_0}.
\]

The handoff's identity controls `T/R`. The DOCX instead defines

\[
C=\prod_p p^{\min(e_p,f_p)+1-\gcd(e_p+1,f_p+1)}
\]

and controls a different rational square `(T/C)^2`. Their exact relation is

\[
\frac RC=
\prod_p\frac{1-p^{-(\min(e_p,f_p)+1)}}
{1-p^{-\gcd(e_p+1,f_p+1)}}.
\]

For `315` and `351`, the divisor sums are 624 and 560, their gcd is 16, the input gcd is 9, and `H_0=1`. Thus `(T,R)=(16,13)`, whereas the DOCX pair `(c,C)` is `(16,9)`. Both statements are correct. Neither denominator can be discarded.

## Exact counterexamples independently rechecked

The new script `verify_selected_certificates.py` imports none of the supplied checking code. It uses exact integer arithmetic, trial division to check the displayed base primes, and complete divisor enumeration for the two small targets.

It rechecks:

1. The 29-digit odd cubefree inputs with common target
   `5276516179938729922490847708056660616574496169354744299520`.
2. For that pair, `R=394214768640`, `T=436988805120`, reduced ratio `378/341`, 16 changed `(v_2(sigma),v_3(sigma))` labels, and total variations 40 and 10. Its target Euler product lies strictly between 4 and 8. This refutes the proposed compatibility-free radius bound of 2 even after fixing the input exponents at 2 and 3.
3. The entire fiber of `504654433920`, which is `{492765}`.
4. The entire seven-member fiber of `106345074572730040320`, and the four listed minimal exchanges, including every proper subset test for their specified replacements.

These are finite arithmetic facts. They do not certify a census through `10^16`, every displayed large certificate, or any asymptotic theorem. The analytic checks above are based on the written arguments rather than recorded computational PASS messages.

## Exchange target-cost lemma and its precise limit

Let an actual nontrivial exchange change the prime bases `S` and satisfy `h(u)=h(v)=H`, with the full old and new local prime-power blocks. Since `u!=v`, the larger input is greater than one and

\[
H>\max(u^2,v^2)\ge uv\ge\prod_{p\in S}p.
\]

The final inequality holds because every changed base has positive exponent on at least one side. The fixed-two-prime theorem gives `|S|>=3`.

For a nonempty disjoint collection of exchanges relative to one reference preimage, their old full blocks are coprime unitary factors, so the product of their `H` values divides `N`. If all changed bases exceed `y>1`,

\[
\log N>\sum_\gamma\sum_{p\in S_\gamma}\log p
>3\nu\log y,
\qquad
\nu<\frac{\log N}{3\log y}.
\]

This charge is rigorous. At `y` comparable to `log N`, it gives a positive constant on the exact scale of the open problem. It does not give little-o. It also bounds the number of disjoint exchanges, not the total number of alternative minimal exchanges or of admissible collections. Converting it directly into a zero-constant fiber bound would introduce an unsupported counting step.

## Remaining gap

The following claims remain unproved, and no reviewed theorem supplies them:

- The uniform zero-constant bound for every fixed input cap.
- A positive Euler-mass gap for all normalized bounded-exponent collisions.
- A sufficiently small number of compatible parts in every fiber.
- Uniformly small cost of exact branching, integer rounding, or exchange packing.
- A globally fresh primitive-divisor assignment across different input bases.

Small-prime target valuations, incomparable transitions, and many-prime exchanges remain uncontrolled together. The existing complete partial proofs can be consolidated faithfully, but a complete proof of Erdős 1060 cannot be asserted from this material.
