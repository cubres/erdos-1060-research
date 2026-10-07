# Erdős 1060: feedback obstruction and arithmetic rigidity

This packet does not contain a complete proof of Erdős Problem 1060.

## Written results

`proof.pdf` and `proof.tex` contain:

- An unconditional polynomial construction of vertex-disjoint positive
  two-cycles in the universal prime graph at exponent cap at least five.
- A **conditional** obstruction: Bateman–Horn for t^2+1 and t^2+t+1
  contradicts the proposed universal subpolynomial transversal estimate.
  Neither Bateman–Horn nor its consequence here is proved unconditionally.
- Represented cap-five targets with at least one unpruned feedback vertex
  required per constructed pair. Under that same instance of Bateman–Horn,
  this is at least (1/32+o(1)) log N / log log N. This is NOT a multiplicity
  lower bound and says nothing against the original Erdős conjecture.
- An unconditional two-prime rigidity theorem showing injectivity despite
  these positive cycles, including an unrestricted-exponent result for two close primes under explicit prime-adic hypotheses.
- Five complete target-specific cap-five noncollision checks.

## Reproduce exact finite checks

Use Python 3, with no third-party packages:

    python3 verify.py
    python3 verify_targets.py

`verify.py` produces `verification.json`. It checks both polynomial
identities, all simultaneous prime values for 3 <= t <= 10000, the
cross-valuations, and finite instances of two-prime rigidity.

`verify_targets.py` reads `target_results.json` and produces
`target_verification.json`. It checks all supplied target prime
factorizations, reconstructs every admissible input exponent, and uses
sound exact row-sum tests until every input exponent is forced. All five
selected targets have exactly one cap-five preimage. No branching or
numerical optimizer is used by this checker. The first target's full
unrestricted fiber is separately checked by enumerating all 33,600 target
divisors. Its input divisor sum is also checked by summing all 24 divisors.

The finite checks do not prove an asymptotic prime-value prediction or a
uniform bound for arbitrary targets. No originality, human referee,
formal proof-assistant verification, or background computation is claimed.
