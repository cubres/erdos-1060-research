#!/usr/bin/env python3
"""Standard-library certificate for the cubefree primitive no-2-cycle relation."""

from __future__ import annotations

import json
import math
from collections import Counter
from itertools import product
from pathlib import Path


HERE = Path(__file__).parent
DATA = HERE / "cubefree_no_2cycle_collision.json"


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


def sigma_pp(p: int, e: int) -> int:
    direct = sum(p**j for j in range(e + 1))
    assert direct == (p ** (e + 1) - 1) // (p - 1)
    return direct


def block_factor(p: int, e: int) -> Counter[int]:
    out = Counter({p: e})
    out.update(factor(sigma_pp(p, e)))
    return out


def aggregate(blocks: list[list[int]]) -> tuple[int, int, Counter[int]]:
    value = math.prod(p**e for p, e in blocks)
    sigma = math.prod(sigma_pp(p, e) for p, e in blocks)
    factors: Counter[int] = Counter()
    for p, e in blocks:
        factors.update(block_factor(p, e))
    return value, sigma, factors


def h_from_input_factors(f: Counter[int]) -> int:
    return math.prod(p**e for p, e in f.items()) * math.prod(
        sigma_pp(p, e) for p, e in f.items()
    )


def main() -> None:
    data = json.loads(DATA.read_text())
    left, right = data["left_blocks"], data["right_blocks"]
    assert all(e in (1, 2) for _, e in left + right)
    k, sk, lf = aggregate(left)
    m, sm, rf = aggregate(right)
    assert lf == rf
    n = k * sk
    assert n == m * sm
    assert (k, sk, m, sm, n) == (
        data["left_input"], data["left_sigma"], data["right_input"],
        data["right_sigma"], data["common_h"]
    )
    assert lf == Counter({int(p): e for p, e in data["common_h_factorization"].items()})

    # Moser primitivity: test every nontrivial divisor of gcd(k,m).
    left_f, right_f = Counter(dict(left)), Counter(dict(right))
    common = left_f & right_f
    tested = 0
    for selection in product(*[range(e + 1) for e in common.values()]):
        d = Counter({p: e for p, e in zip(common, selection) if e})
        if not d:
            continue
        tested += 1
        assert h_from_input_factors(left_f - d) != h_from_input_factors(right_f - d)
    assert tested == data["nontrivial_common_divisors_checked"] == 15

    # Conformal indecomposability: no nonempty proper subset of the signed
    # local columns has zero valuation vector.
    signed = [(1, p, e) for p, e in left] + [(-1, p, e) for p, e in right]
    full = (1 << len(signed)) - 1
    for mask in range(1, full):
        balance: Counter[int] = Counter()
        for j, (sign, p, e) in enumerate(signed):
            if mask >> j & 1:
                balance.update({q: sign * a for q, a in block_factor(p, e).items()})
        assert any(balance.values())

    # Directed graph among input base primes, retaining every exponent used on
    # either side.  Confirm the absence of reciprocal arrows.
    bases = set(left_f) | set(right_f)
    arrows = set()
    for _, p, e in signed:
        for q in factor(sigma_pp(p, e)):
            if q in bases and q != p:
                arrows.add((p, q))
    assert not any((q, p) in arrows for p, q in arrows)

    print("PASS")
    print(f"K={k}; sigma(K)={sk}")
    print(f"M={m}; sigma(M)={sm}")
    print(f"N={n}")
    print(f"gcd={math.gcd(k,m)}; primitive_divisors_tested={tested}")
    print(f"signed_blocks={len(signed)}; proper_subsets_tested={full-1}; arrows={sorted(arrows)}")


if __name__ == "__main__":
    main()
