#!/usr/bin/env python3
"""Independently verify the reduced cubefree equal-saturation-profile atom."""

import json
from collections import Counter
from pathlib import Path

from sympy import divisor_sigma, factorint, isprime


HERE = Path(__file__).parent
CERTIFICATE = HERE / "equal_saturation_profile_u5000_e2.json"


def block_value(block: tuple[int, int]) -> int:
    p, e = block
    return p**e * int(divisor_sigma(p**e))


def product(blocks: list[tuple[int, int]]) -> int:
    answer = 1
    for block in blocks:
        answer *= block_value(block)
    return answer


def profile(blocks: list[tuple[int, int]], target: int):
    target_factors = factorint(target)
    return sorted((e, target_factors[p] == e) for p, e in blocks)


def subset_products(blocks: list[tuple[int, int]]) -> set[int]:
    values = [block_value(block) for block in blocks]
    answer = set()
    for mask in range(1 << len(values)):
        value = 1
        for i, local in enumerate(values):
            if mask >> i & 1:
                value *= local
        answer.add(value)
    return answer


def main() -> None:
    data = json.loads(CERTIFICATE.read_text())
    left = [tuple(map(int, block)) for block in data["left_blocks"]]
    right = [tuple(map(int, block)) for block in data["right_blocks"]]
    assert not (set(left) & set(right))
    assert all(isprime(p) and e in (1, 2) for p, e in left + right)
    target = product(left)
    assert target == product(right) == int(data["common_h"])
    assert profile(left, target) == profile(right, target)
    assert Counter(profile(left, target)) == Counter(
        {(1, True): 2, (1, False): 4, (2, True): 3, (2, False): 2}
    )
    common_subproducts = subset_products(left) & subset_products(right)
    assert common_subproducts == {1, target}
    print("PASS exact common h")
    print("PASS cubefree and no identical local state")
    print("PASS equal saturation histograms")
    print("PASS conformal atomicity by exhaustive subset products")


if __name__ == "__main__":
    main()
