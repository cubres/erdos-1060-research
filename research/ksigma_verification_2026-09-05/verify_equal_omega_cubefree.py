#!/usr/bin/env python3
"""Standard-library verifier for the cubefree equal-Omega(F) collision."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


DATA = Path(__file__).parent / "equal_omega_e2_u700.json"


def factor(n: int) -> Counter[int]:
    out: Counter[int] = Counter()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] += 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out[n] += 1
    return out


def is_prime(n: int) -> bool:
    return factor(n) == Counter({n: 1})


def sigma_pp(p: int, e: int) -> int:
    direct = sum(p**j for j in range(e + 1))
    assert direct == (p ** (e + 1) - 1) // (p - 1)
    return direct


def block_factors(p: int, e: int) -> Counter[int]:
    out = Counter({p: e})
    out.update(factor(sigma_pp(p, e)))
    return out


def aggregate(blocks: list[list[int]]) -> tuple[int, int, Counter[int]]:
    value = math.prod(p**e for p, e in blocks)
    sigma = math.prod(sigma_pp(p, e) for p, e in blocks)
    factors: Counter[int] = Counter()
    for p, e in blocks:
        factors.update(block_factors(p, e))
    return value, sigma, factors


def h_from_factors(factors: Counter[int]) -> int:
    return math.prod(p**e * sigma_pp(p, e) for p, e in factors.items())


def check_atom(signed_vectors: list[dict[int, int]]) -> int:
    """Exhaust all proper signed-column subsets via an exact Gray code."""
    width = len(signed_vectors)
    full = (1 << width) - 1
    balance: defaultdict[int, int] = defaultdict(int)
    nonzero = 0
    previous = 0
    checked = 0
    for index in range(1, 1 << width):
        gray = index ^ (index >> 1)
        changed = gray ^ previous
        j = changed.bit_length() - 1
        direction = 1 if gray & changed else -1
        for q, a in signed_vectors[j].items():
            before = balance[q]
            after = before + direction*a
            if before == 0 and after != 0:
                nonzero += 1
            elif before != 0 and after == 0:
                nonzero -= 1
            balance[q] = after
        previous = gray
        if gray == full:
            assert nonzero == 0
        else:
            checked += 1
            assert nonzero != 0, f"proper zero subrelation mask={gray}"
    return checked


def main() -> None:
    data = json.loads(DATA.read_text())
    left, right = data["left_blocks"], data["right_blocks"]
    assert all(is_prime(p) and e in (1, 2) for p, e in left + right)
    assert len({p for p, _ in left}) == len(left)
    assert len({p for p, _ in right}) == len(right)

    k, sigma_k, left_hf = aggregate(left)
    m, sigma_m, right_hf = aggregate(right)
    n = k*sigma_k
    assert left_hf == right_hf
    assert n == m*sigma_m
    assert (k, sigma_k, m, sigma_m, n) == (
        data["left_input"], data["left_sigma"], data["right_input"],
        data["right_sigma"], data["common_h"],
    )
    nf = Counter({int(p): e for p, e in data["common_h_factorization"].items()})
    assert left_hf == nf
    assert math.prod(p**e for p, e in nf.items()) == n

    left_powerful = Counter({p: e for p, e in left if e >= 2})
    right_powerful = Counter({p: e for p, e in right if e >= 2})
    left_omega = sum(left_powerful.values())
    right_omega = sum(right_powerful.values())
    assert left_omega == right_omega == data["left_invariant"] == data["right_invariant"] == 8

    # Moser primitivity.
    left_f, right_f = Counter(dict(left)), Counter(dict(right))
    common = left_f & right_f
    assert math.prod(p**e for p, e in common.items()) == math.gcd(k, m) == data["gcd"]
    assert common == Counter({int(p): e for p, e in data["gcd_factorization"].items()})
    primitive_tests = 0
    for choice in itertools.product(*[range(e + 1) for e in common.values()]):
        divisor = Counter({p: e for p, e in zip(common, choice) if e})
        if not divisor:
            continue
        primitive_tests += 1
        assert h_from_factors(left_f - divisor) != h_from_factors(right_f - divisor)
    assert primitive_tests == data["nontrivial_common_divisors_checked"] == 127

    signed = []
    for sign, blocks in ((1, left), (-1, right)):
        for p, e in blocks:
            signed.append({q: sign*a for q, a in block_factors(p, e).items()})
    subset_tests = check_atom(signed)
    assert subset_tests == data["proper_signed_subsets_checked"] == (1 << 21) - 2

    print("PASS")
    print(f"K={k}; sigma(K)={sigma_k}; F(K)={dict(left_powerful)}; Omega(F(K))={left_omega}")
    print(f"M={m}; sigma(M)={sigma_m}; F(M)={dict(right_powerful)}; Omega(F(M))={right_omega}")
    print(f"N={n}")
    print(f"gcd={math.gcd(k,m)}; primitive_divisors_tested={primitive_tests}")
    print(f"signed_blocks={len(signed)}; proper_subsets_tested={subset_tests}")


if __name__ == "__main__":
    main()
