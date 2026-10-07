# Continuation brief for the receiving agent

You are continuing a research investigation of Erdős Problem 1060. Read the
attached dossier before attempting to extend any previous argument.

Let h(k)=k sigma(k), f(N)=#{k>=1:h(k)=N}. The task is a rigorous proof or disproof
of log max(1,f(N))=o(log N/log log N), uniformly over all sufficiently large N.
An average estimate, an almost-all result, N^{o(1)}, or an improved positive
constant is not the requested conclusion. The polylogarithmic variant is stronger
and is not necessary to answer the primary problem.

The dossier is a complete handoff, NOT a complete solution. Treat its newer
results as supplied working proofs requiring independent audit. No originality,
external peer review, or formal verification is claimed. The computational
checks are exact within their stated finite ranges; none proves an asymptotic
extension. Use original notes only with the supersession/correction map.

Start by checking the all-fixed-cap reduction in Chapter 3, the strongest
unrestricted bound in Chapter 5, the unrestricted fixed-two-prime injectivity
proof in Chapter 9, and the primitive-divisor domain lists in Chapter 10.
Then read the counterexamples in Chapters 8, 11, 16 and 18, and the exact
exchange formulation in Chapter 17. The remaining task concerns genuine
integer choices across a growing number of prime bases.

Retain the exact equations at every target prime q:

    v_q(N) = e_q + sum_{p != q} v_q(sigma(p^{e_p})).

Each input prime chooses one local exponent. Keep rows at output primes that
cannot appear in the input. Local divisibility is not target exhaustion.
Only common equal-exponent prime-power blocks can be canceled automatically
through h; arbitrary gcd cancellation is invalid.

Established reductions: it suffices to show, for EVERY fixed E,

    log max_{M<=X} max(1,f_E(M)) = o_E(log X/log log X),

where f_E restricts input exponents to <=E. This estimate is not supplied as a
proved lemma. Choose E first, then the large-X threshold when combining it with
the high-exponent factor G_E; do not assume uniformity of errors in E.

Do not reuse the following invalid shortcuts:

- Counting powerful D with h(D)|N while ignoring squarefree completion.
- Odd-cubefree injectivity or cubefree multiplicity <=2 or <=3.
- Treating odd inputs as odd targets.
- Assuming primitive divisor witnesses are new across different bases.
- Extending the compatible-family small-integer multiplier to arbitrary pairs:
  the correct multiplier is T/R, with an uncontrolled denominator R.
- Assuming fractional dimension measures genuine binary freedom, or that
  zero-budget nonnegative linear certificates always eliminate it.
- Charging for all potential feedback cycles as though each were a real choice.
  The universal subpolynomial feedback criterion conflicts conditionally with
  the explicit Bateman–Horn family in Chapter 16.
- Inferring unbounded statements from a finite prime-range elimination certificate.
- Enumerating an unknown complete fiber to extract its exchanges, then treating
  that extraction as an independent uniform upper-bound proof.
- Multiplying fixed-pair injectivity statements across interacting prime pairs.

Use the literature map quantitatively. Check theorem hypotheses, parameter
uniformity, and the actual exponent after dividing by log X/log log X.
A theorem for fixed sigma(k)/k, for sigma(k)-k, or for typical sigma-fibers
cannot be substituted without an explicit reduction.

Three possible programs remain genuinely unproved: (1) a uniform packing bound
for support-minimal exact exchanges; (2) an integer reconstruction/rounding
procedure whose total logarithmic surviving branching cost is negligible;
(3) a target-specific feedback argument sharpened by full valuation capacities
and output-factor constraints. Develop a concrete lemma and attack it with the
provided counterexamples before polishing a purported completion. These are
research directions, not presumed true assertions.

The full fixed-two-prime theorem rules out exchanges at only one or two bases.
Its distance-three corollary alone permits exponentially large abstract codes;
it does not already control three-or-more-base exchanges.

Run selected exact checkers to understand the examples. Distinguish discovery
from certification and set explicit resource limits. Use independent proof and
counterexample workers only if actual tools provide them. Never claim a
numerical timeout is a nonexistence certificate.

Return the strongest theorem actually established, its complete proof, relevant
reproducible checks, and a precise statement of any remaining gap. A full-resolution
claim requires the entire quantified uniform bound, not a conditional finishing
lemma. Do not stop because the problem has an open-problem label; equally, do
not turn the user's expectation of a solution into a mathematical premise.
