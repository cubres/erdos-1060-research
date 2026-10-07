#!/usr/bin/env python3
"""Exact verifier for a normalized cubefree collision with all bases > 17."""

from __future__ import annotations

import json
import math
from pathlib import Path


DATA = Path(__file__).with_name("rough_gt17_u50000_e2_disjoint_trial.json")


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def local_block(prime: int, exponent: int) -> int:
    return prime**exponent * (
        (prime ** (exponent + 1) - 1) // (prime - 1)
    )


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


def product(blocks: list[list[int]]) -> int:
    seen: set[int] = set()
    answer = 1
    for prime, exponent in blocks:
        assert is_prime(prime)
        assert prime > 17
        assert prime not in seen
        assert exponent in (1, 2)
        seen.add(prime)
        answer *= local_block(prime, exponent)
    return answer


def main() -> None:
    data = json.loads(DATA.read_text())
    atom = data["atoms"][0]
    left = atom["left_blocks"]
    right = atom["right_blocks"]
    common = int(atom["common_h"])
    assert product(left) == common == product(right)
    assert not (set(map(tuple, left)) & set(map(tuple, right)))

    factorization = {
        int(prime): int(exponent)
        for prime, exponent in atom["common_h_factorization"].items()
    }
    reconstructed = 1
    for prime, exponent in factorization.items():
        assert is_prime(prime)
        reconstructed *= prime**exponent
    assert reconstructed == common

    left_by_base = dict(left)
    right_by_base = dict(right)
    differing = sorted(set(left_by_base) | set(right_by_base))
    assert all(left_by_base.get(p, 0) != right_by_base.get(p, 0) for p in differing)
    mass = sum(-math.log1p(-1.0 / p) for p in differing)
    euler_product = math.prod(p / (p - 1) for p in differing)
    side_blocks = (
        [("L", p, e) for p, e in left]
        + [("R", p, e) for p, e in right]
    )
    components, cycle_rank = incidence_cycle_rank(side_blocks)
    assert components == 1 and cycle_rank == 198
    print("PASS exact normalized cubefree h-collision")
    print(
        f"differing_bases={len(differing)}; min={min(differing)}; "
        f"max={max(differing)}"
    )
    print(f"euler_mass={mass:.17g}; euler_product={euler_product:.17g}")
    print(f"incidence_components={components}; cycle_rank={cycle_rank}")


if __name__ == "__main__":
    main()
