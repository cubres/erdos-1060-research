# Erdős 1060: exact certificates and longer feedback cycles

## Status

This packet **does not prove** the unrestricted estimate

\[
\log\max(1,f(N))=o(\log N/\log\log N).
\]

It contains complete proofs of the stated cycle exclusions and certificate-counting lemmas, and exact finite checks. No new unrestricted asymptotic bound is claimed. No claim of originality, independent human review, or formal proof-assistant certification is made.

## Contents

`erdos1060_exact_certificates.pdf` and `.tex` contain the mathematical note.

`dual_certificate.json` certifies the complete cubefree fiber of the previously known 58-digit target. Exact row-support elimination reduces 53 indicators to 48; integer row weights remove 10 more; the residual 38-column matrix has rational rank 37. Setting one indicator to zero or one gives the two preimages. The weights have maximum absolute value 137. This is a new form of certification for an already known count, not a new multiplicity record.

`verify_v9.py` uses only the Python standard library. It independently reconstructs the local domains, applies exact necessary-condition propagation, checks the integer dual inequalities and zero budget, and computes exact rational ranks. It separately constructs and sums every divisor of each of the two resulting inputs. It also checks five dense represented targets and the complete prime graph through 100,000.

`verify_large.py` certifies injectivity on cubefree inputs all of whose prime factors lie in [1001, 1,000,000]. It verifies the full allowed input-prime range, local factor products, and pairwise coprimality of factor-row bases, then removes all 234,990 difference columns in 35 sound elimination rounds. These are prime-factor restrictions, not an input-size cutoff or an asymptotic claim.

`prime_graph_100000.json` and `prime_graph_1000000.json` supply the factor data. `dense_probes.json` specifies the five represented targets. The `verification_*.json` files are recorded successful checker outputs; rerunning the checkers validates them rather than trusting their contents.

`core_search_251_1.json` records a 30-second unsuccessful numerical search on the surviving core for primes [251, 1,000,000]. It proves neither existence nor nonexistence. `peel_large_results.json` records exploratory threshold runs; only the class explicitly verified by `verify_large.py` is asserted as a certified noncollision result here.

## Verification

From this directory, run:

```sh
python3 verify_v9.py
python3 verify_large.py
```

Both programs require only the Python standard library. On the working machine, the runs took approximately 4 and 24 seconds, respectively; other machines may differ. They raise an error on a failed certificate and write updated verification reports after success. `verify_v9.py --skip-graph` checks the main dual certificate and dense targets without the larger finite-graph check.

## Optional discovery reproduction

The supplied certificate is independent of numerical optimization. To rediscover one with SciPy, install NumPy and SciPy in a suitable environment and run:

```sh
python3 discover_certificate.py
python3 -c 'from pathlib import Path; from verify_v9 import check_dual; print(check_dual(Path("rediscovered_certificate.json")))'
```

Numerical dual multipliers are converted to rational numbers and every certificate inequality is checked exactly before anything is asserted. Different solver versions can return different valid weights. This discovery script is tailored to the supplied example.

`generate_prime_data.py` optionally regenerates the local factor data using SymPy. The verification programs check the arithmetic independently; a factorizer's output is not accepted on trust.

## Remaining gap

The exact certificate theorem bounds a fiber using the number of free binary coordinates after safe exclusions, or a combination of that dimension and a positive-score budget. There is **no proved uniform little-o bound** for these quantities, nor for the older adaptive branching cost, at every fixed exponent cap. Without such a theorem or another argument, the reduction to Erdős 1060 is incomplete.
