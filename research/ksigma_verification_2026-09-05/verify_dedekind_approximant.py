#!/usr/bin/env python3
"""Exact finite checks for the third-order injective approximant.

The proof in the research note is algebraic.  This script independently checks
its local factorization, denominator bound, exceptional {2,3} valuation map,
and injectivity on an initial interval using exact rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt, prod


LIMIT = 200_000


def smallest_prime_factors(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    for p in range(2, isqrt(limit) + 1):
        if spf[p] != p:
            continue
        for n in range(p * p, limit + 1, p):
            if spf[n] == n:
                spf[n] = p
    return spf


def factor(n: int, spf: list[int]) -> dict[int, int]:
    answer: dict[int, int] = {}
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        answer[p] = e
    return answer


def sigma_from_factor(factors: dict[int, int]) -> int:
    return prod((p ** (e + 1) - 1) // (p - 1) for p, e in factors.items())


def local_a3(p: int, e: int) -> Fraction:
    if e == 0:
        return Fraction(1)
    if e == 1:
        return Fraction(p * (p + 1))
    return Fraction(p ** (2 * e + 1), p - 1)


def a3_from_factor(factors: dict[int, int]) -> Fraction:
    return prod((local_a3(p, e) for p, e in factors.items()), start=Fraction(1))


def theta_from_factor(factors: dict[int, int]) -> Fraction:
    return prod(
        (
            Fraction(p ** (e + 1) - 1, p ** (e + 1))
            for p, e in factors.items()
            if e >= 2
        ),
        start=Fraction(1),
    )


def check_two_three_states(cap: int = 1_000) -> None:
    seen: dict[tuple[int, int], tuple[int, int]] = {}
    for a in range(cap + 1):
        if a == 0:
            va = (0, 0)
        elif a == 1:
            va = (1, 1)
        else:
            va = (2 * a + 1, 0)
        for b in range(cap + 1):
            if b == 0:
                vb = (0, 0)
            elif b == 1:
                vb = (2, 1)
            else:
                vb = (-1, 2 * b + 1)
            total = (va[0] + vb[0], va[1] + vb[1])
            assert total not in seen, (total, seen[total], (a, b))
            seen[total] = (a, b)


def main() -> None:
    check_two_three_states()
    spf = smallest_prime_factors(LIMIT)
    seen: dict[Fraction, int] = {}

    for n in range(1, LIMIT + 1):
        factors = factor(n, spf)
        a3 = a3_from_factor(factors)
        theta = theta_from_factor(factors)
        h = n * sigma_from_factor(factors)
        assert a3 * theta == h

        repeated_bases = prod((p for p, e in factors.items() if e >= 2), start=1)
        unreduced_denominator = prod(
            (p - 1 for p, e in factors.items() if e >= 2), start=1
        )
        assert a3.denominator <= unreduced_denominator
        assert repeated_bases <= isqrt(n)

        assert a3 not in seen, (seen[a3], n, a3)
        seen[a3] = n

    print(
        "PASS third-order factorization, denominator, {2,3} states, "
        f"and A3 injectivity for n <= {LIMIT}"
    )


if __name__ == "__main__":
    main()
