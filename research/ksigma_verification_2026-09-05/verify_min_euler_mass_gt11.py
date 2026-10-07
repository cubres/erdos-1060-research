#!/usr/bin/env python3
"""Exact verifier for the normalized cubefree collision with bases above 11."""

from __future__ import annotations

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "min_euler_mass_u20000_e2_gt11.json"


def is_prime(n: int) -> bool:
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


def local_block(p: int, e: int) -> int:
    return p**e * ((p ** (e + 1) - 1) // (p - 1))


def prime_factors(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors.add(value)
    return factors


def incidence_cycle_rank(blocks: list[tuple[str, int, int]]) -> tuple[int, int]:
    block_rows = [prime_factors(local_block(p, e)) for _, p, e in blocks]
    row_blocks: dict[int, list[int]] = {}
    for index, rows in enumerate(block_rows):
        for row in rows:
            row_blocks.setdefault(row, []).append(index)
    seen: set[int] = set()
    components = 0
    for start in range(len(blocks)):
        if start in seen:
            continue
        components += 1
        stack = [start]
        while stack:
            block = stack.pop()
            if block in seen:
                continue
            seen.add(block)
            for row in block_rows[block]:
                stack.extend(row_blocks[row])
    edges = sum(map(len, block_rows))
    vertices = len(blocks) + len(row_blocks)
    return components, edges - vertices + components


def block_product(blocks: list[list[int]]) -> int:
    value = 1
    seen: set[int] = set()
    for p, e in blocks:
        assert is_prime(p)
        assert p > 11
        assert p not in seen
        assert 1 <= e <= 2
        seen.add(p)
        value *= local_block(p, e)
    return value


def main() -> None:
    data = json.loads(DATA.read_text())
    left = data["left_blocks"]
    right = data["right_blocks"]
    common = int(data["common_h"])

    assert block_product(left) == common
    assert block_product(right) == common
    assert not (set(map(tuple, left)) & set(map(tuple, right)))

    recorded_factorization = {
        int(p): int(e) for p, e in data["common_h_factorization"].items()
    }
    reconstructed = 1
    for p, e in recorded_factorization.items():
        assert is_prime(p)
        reconstructed *= p**e
    assert reconstructed == common

    left_exponents = dict(left)
    right_exponents = dict(right)
    differing = sorted(
        p
        for p in set(left_exponents) | set(right_exponents)
        if left_exponents.get(p, 0) != right_exponents.get(p, 0)
    )
    assert differing == data["differing_bases"]
    mass = sum(-math.log1p(-1.0 / p) for p in differing)
    product = math.prod(p / (p - 1) for p in differing)
    assert math.isclose(mass, data["euler_mass"], rel_tol=0.0, abs_tol=2e-15)
    assert math.isclose(
        product, data["euler_product"], rel_tol=0.0, abs_tol=2e-15
    )
    side_blocks = (
        [("L", p, e) for p, e in left]
        + [("R", p, e) for p, e in right]
    )
    components, cycle_rank = incidence_cycle_rank(side_blocks)
    assert components == 1 and cycle_rank == 84

    print("PASS exact h equality")
    print(f"common_h={common}")
    print(f"differing_bases={len(differing)}; minimum={min(differing)}")
    print(f"euler_mass={mass:.17g}; euler_product={product:.17g}")
    print(f"incidence_components={components}; cycle_rank={cycle_rank}")


if __name__ == "__main__":
    main()
