# Erdős 1060: prime-order constraints and universal feedback certificates

Status: **partial results, not a complete proof**. No asymptotic estimate for the universal feedback numbers has been proved. No originality, independent human-referee review, or proof-assistant certification is claimed.

## Contents

- `proof.pdf`, `proof.tex`: complete proofs of the stated reductions, local prime-order restrictions, and descriptions of the finite certificates. The uniform growth condition in Corollary 2.3 is explicitly hypothetical.
- `prime_graph.py`: constructs the exact universal underlying graph from multiplicative-order roots modulo sieved primes. No large divisor-sum factorization is required.
- `certificates.json`: explicit deletion sets and remaining cycle blocks. These are verified upper bounds, not optimality certificates.
- `verify.py`: standalone exact verifier, using only the Python standard library.
- `verification.json`: output from the completed verification run.

Run:

```sh
python3 verify.py
```

The verifier reconstructs all graphs in the certificate, including the cap-two graph on primes from 5 through 1,000,000. It checks that the remaining cycle blocks are pure quadratic odd cycles or pairs and that contracting them produces a directed acyclic graph. This proves absence of additional cycles. For the higher-cap acyclic certificates it performs a full topological-sort check.

As a separate check of the construction, it compares every graph edge with direct divisor-sum divisibility for all pairs of primes at most 500, at caps 1 through 6. It verifies a positive nine-cycle and the sharp largest-target-prime valuation example by exact arithmetic.

The deletion sets were discovered using deterministic greedy graph heuristics, followed by restoration tests. The verifier does not require that discovery code, NetworkX, SciPy, internet access, floating-point optimization, or precomputed prime factorizations.

## What is NOT concluded

Finite bounds of 2, 7, 12, and 29 for the long-positive-cycle transversals at the four tabulated cutoffs do not prove any asymptotic growth law. In particular, they do not prove A_E(x)=x^{o(1)}, do not prove the required uniform bound on tau_+(N), and do not settle the Erdős conjecture. The universal criterion may be stronger than necessary because its graph combines mutually incompatible exponent choices.

All cutoffs refer to **input prime factors**, not to the sizes of input integers. The nine-cycle is a graph example, not a claimed collision. The sharp largest-prime example gives a represented target but no asserted multiplicity for its full fiber.
