# Erdős 1060: literature audit and primitive-divisor exponent lists

This packet does **not** contain a complete proof of Erdős Problem 1060.

The proved additional result is

    f(N) <= product_{p|N} |B_p(N)| <= omega(N)^omega(N), N > 1,

where B_p(N) = {0} union {e >= 2 : p^e sigma(p^e) divides N}.
It follows from the Bang–Zsigmondy theorem and squarefree injectivity.
The bound is uniform in the target exponents and values of its prime divisors;
it does not improve the previously established unrestricted asymptotic constant.

## Files

- `literature_and_exponent_lists.pdf`: complete proof, quantitative literature audit, scope, and references.
- `literature_and_exponent_lists.tex`: editable LaTeX source.
- `verify_order_lists.py`: exact standard-library verifier.
- `verification.json`: recorded successful verification results.

## Reproduce

Run with Python 3.10 or later:

    python3 verify_order_lists.py

Do not use `python -O`, since the checker uses assertions. The verifier:

1. Checks the supplied target prime factorizations.
2. Reconstructs local exponent domains from multiplicative-order lists.
3. Compares those lists with direct exponent scans.
4. Checks distinct primitive-divisor labels within each fixed base, including the exceptional label for (2,5).
5. Enumerates every divisor of each of four targets and verifies their complete unrestricted fibers.
6. Independently constructs and sums every divisor of each returned input.
7. Performs 48,590 local-domain regression comparisons from seed inputs 2 through 10,000.
8. Enumerates all inputs whose h-values are supported on {2,3} and on {2,3,7}, using the proved finite lists.

The finite checks do not prove Bang–Zsigmondy or the asymptotic conjecture.
The analytic proof explicitly uses the classical primitive-divisor theorem.
No formal proof-assistant verification or independent human referee review is claimed.
