#!/usr/bin/env python3
"""Exact checks for local-gcd-descent-2026-09-05.md.

All algebraic identities are checked with Python integers/Fraction.  Primality
of the Mills pair is checked separately by verify_mills_phi3_prime_cycle.py.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent


def S(p: int, e: int) -> int:
    return (p ** (e + 1) - 1) // (p - 1)


def H(p: int, e: int) -> int:
    return p**e * S(p, e)


def valuation(value: int, prime: int) -> int:
    answer = 0
    while value % prime == 0:
        value //= prime
        answer += 1
    return answer


def input_and_h(blocks: list[list[int]]) -> tuple[int, int]:
    value = 1
    image = 1
    for p, e in blocks:
        value *= p**e
        image *= H(p, e)
    return value, image


def defect_data(
    left_blocks: list[list[int]], right_blocks: list[list[int]]
) -> tuple[int, int, int, Fraction]:
    left = dict(left_blocks)
    right = dict(right_blocks)
    A = B = X = Y = C = 1
    product_w = Fraction(1)

    for p in set(left) | set(right):
        left_e = left.get(p, 0)
        right_e = right.get(p, 0)
        if left_e == right_e:
            continue
        high = max(left_e, right_e)
        low = min(left_e, right_e)
        delta = high - low
        d = gcd(high + 1, low + 1)
        common = S(p, d - 1)
        U = S(p, high) // common
        V = S(p, low) // common
        assert gcd(U, V) == 1
        assert U % p and V % p
        C *= p ** (low + 1 - d)

        if left_e > right_e:
            A *= p**delta
            X *= U
            Y *= V
        else:
            B *= p**delta
            X *= V
            Y *= U

        product_w *= (
            Fraction(p ** (high + 1) - 1, p ** (high + 1))
            * Fraction(p ** (low + 1) - 1, p ** (low + 1))
            / Fraction(p**d - 1, p**d) ** 2
        )

    assert A * X == B * Y
    assert gcd(A, B) == 1
    assert X % B == 0 and Y % A == 0
    c = X // B
    assert c == Y // A
    assert Fraction(c * c, C * C) == product_w
    assert c > C
    return C, c, gcd(C, c), product_w


def main() -> None:
    left_315 = [[3, 3], [13, 1]]
    right_315 = [[3, 2], [5, 1], [7, 1]]
    left_value, left_h = input_and_h(left_315)
    right_value, right_h = input_and_h(right_315)
    assert (left_value, right_value, left_h, right_h) == (
        351,
        315,
        196_560,
        196_560,
    )
    assert defect_data(left_315, right_315) == (
        9,
        16,
        1,
        Fraction(256, 81),
    )

    certificate = json.loads(
        (HERE / "min_euler_mass_u20000_e2_gt11.json").read_text()
    )
    _, left_h = input_and_h(certificate["left_blocks"])
    _, right_h = input_and_h(certificate["right_blocks"])
    assert left_h == right_h == int(certificate["common_h"])
    C, c, common, _ = defect_data(
        certificate["left_blocks"], certificate["right_blocks"]
    )
    assert C == 30_479_507_950_175_015_606_654_562_325_060_211_569
    assert c == 42_614_134_766_498_560_938_681_337_852_723_200_000
    assert common == 391
    assert C % common == 0 and len(str(C // common)) == 35

    p = 22_419_767_768_701
    q = 107_419_560_853_453
    assert (p * p + p + 1) % q == 0
    assert (q * q + q + 1) % p == 0
    assert (q + 1) % p and (p + 1) % q
    # The two T-columns, restricted to valuation rows p and q, are identical.
    def t_column(base: int, row: int) -> int:
        return (
            int(base == row)
            + valuation(base * base + base + 1, row)
            - valuation(base + 1, row)
        )

    assert [[t_column(base, row) for base in (p, q)] for row in (p, q)] == [
        [1, 1],
        [1, 1],
    ]

    print("PASS local gcd, defect-square, denominator, and Mills-row checks")


if __name__ == "__main__":
    main()
