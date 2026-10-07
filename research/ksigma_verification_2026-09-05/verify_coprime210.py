#!/usr/bin/env python3
"""Independent standard-library audit of the coprime-to-210 h-collision."""

from __future__ import annotations

import json
import math
from collections import Counter
from itertools import product
from pathlib import Path


CERTIFICATE = Path(
    "/Users/cubres/Documents/ChatGPT/Research/"
    "ksigma_rough_collision_search_2026-09-05/collision_11_700_e8.json"
)


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def factor_trial(n: int) -> Counter[int]:
    result: Counter[int] = Counter()
    d = 2
    while d * d <= n:
        while n % d == 0:
            result[d] += 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        assert is_prime_trial(n)
        result[n] += 1
    return result


def sigma_prime_power_two_ways(p: int, e: int) -> int:
    direct = sum(p**j for j in range(e + 1))
    closed = (p ** (e + 1) - 1) // (p - 1)
    assert direct == closed
    return direct


def rebuild(blocks: list[list[int]]) -> tuple[int, int, Counter[int], list[tuple]]:
    bases = [p for p, _ in blocks]
    assert len(bases) == len(set(bases)), "duplicate base on one side"
    k = 1
    sigma_k = 1
    h_factors: Counter[int] = Counter()
    local_rows: list[tuple] = []
    for p, e in blocks:
        assert is_prime_trial(p), f"composite base {p}"
        assert e >= 1
        local_sigma = sigma_prime_power_two_ways(p, e)
        local_factors = factor_trial(local_sigma)
        assert math.prod(q**a for q, a in local_factors.items()) == local_sigma
        k *= p**e
        sigma_k *= local_sigma
        h_factors[p] += e
        h_factors.update(local_factors)
        local_rows.append((p, e, local_sigma, dict(sorted(local_factors.items()))))
    return k, sigma_k, h_factors, local_rows


def format_factorization(factors: Counter[int]) -> str:
    return " * ".join(
        str(p) if e == 1 else f"{p}^{e}" for p, e in sorted(factors.items())
    )


def h_from_factors(factors: Counter[int]) -> int:
    value = math.prod(p**e for p, e in factors.items())
    sigma_value = math.prod(
        sigma_prime_power_two_ways(p, e) for p, e in factors.items()
    )
    return value * sigma_value


def primitive_divisor_checks(
    left: list[list[int]], right: list[list[int]]
) -> int:
    lf = Counter(dict(left))
    rf = Counter(dict(right))
    common = lf & rf
    choices = [[(p, e) for e in range(a + 1)] for p, a in common.items()]
    tested = 0
    for selected in product(*choices):
        divisor = Counter({p: e for p, e in selected if e})
        if not divisor:
            continue
        tested += 1
        assert h_from_factors(lf - divisor) != h_from_factors(rf - divisor)
    return tested


def main() -> None:
    data = json.loads(CERTIFICATE.read_text())
    left = data["left_blocks"]
    right = data["right_blocks"]
    k, sigma_k, fk, left_rows = rebuild(left)
    m, sigma_m, fm, right_rows = rebuild(right)
    hk = k * sigma_k
    hm = m * sigma_m

    assert k != m
    assert hk == hm
    assert fk == fm
    assert math.prod(p**e for p, e in fk.items()) == hk
    assert math.gcd(k, 210) == math.gcd(m, 210) == 1
    assert all(math.gcd(p, 210) == 1 for p, _ in left + right)
    primitive_tests = primitive_divisor_checks(left, right)
    assert primitive_tests == 49_151

    stored_factors = Counter({int(p): e for p, e in data["common_h_factorization"].items()})
    comparisons = {
        "left_input": k == data["left_input"],
        "right_input": m == data["right_input"],
        "common_h": hk == data["common_h"],
        "common_h_factorization": fk == stored_factors,
    }

    print("LEFT LOCAL SIGMA FACTORS")
    for row in left_rows:
        print(row)
    print("RIGHT LOCAL SIGMA FACTORS")
    for row in right_rows:
        print(row)
    print(f"K={k}")
    print(f"sigma(K)={sigma_k}")
    print(f"M={m}")
    print(f"sigma(M)={sigma_m}")
    print(f"N={hk}")
    print(f"N factors={format_factorization(fk)}")
    print(f"gcd(K,M)={math.gcd(k, m)} factors={format_factorization(factor_trial(math.gcd(k,m)))}")
    print(f"gcd(K,210)={math.gcd(k,210)}")
    print(f"gcd(M,210)={math.gcd(m,210)}")
    print(f"primitive common-divisor tests={primitive_tests}")
    print("stored comparisons=" + repr(comparisons))
    assert all(comparisons.values()), "stored certificate has a transcription mismatch"
    print("PASS")


if __name__ == "__main__":
    main()
