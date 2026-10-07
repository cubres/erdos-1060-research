#!/usr/bin/env python3
"""Independently verify a JSON collision certificate with exact integers."""

from __future__ import annotations

import argparse
import json
from math import gcd, prod
from pathlib import Path

import sympy as sp


def sigma_prime_power(p: int, e: int) -> int:
    return (p ** (e + 1) - 1) // (p - 1)


def input_from_blocks(blocks) -> int:
    return prod(int(p) ** int(e) for p, e in blocks)


def h_from_blocks(blocks) -> int:
    return prod(
        int(p) ** int(e) * sigma_prime_power(int(p), int(e))
        for p, e in blocks
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--forbidden-product", type=int, default=210)
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text())

    left = [(int(p), int(e)) for p, e in data["left_blocks"]]
    right = [(int(p), int(e)) for p, e in data["right_blocks"]]
    k = input_from_blocks(left)
    m = input_from_blocks(right)
    block_h_left = h_from_blocks(left)
    block_h_right = h_from_blocks(right)

    assert k == int(data["left_input"])
    assert m == int(data["right_input"])
    assert k != m
    assert gcd(k, args.forbidden_product) == 1
    assert gcd(m, args.forbidden_product) == 1
    assert block_h_left == block_h_right == int(data["common_h"])

    # This is deliberately independent of the block-product equality above.
    direct_left = k * int(sp.divisor_sigma(k))
    direct_right = m * int(sp.divisor_sigma(m))
    assert direct_left == direct_right == block_h_left
    assert {str(q): int(a) for q, a in sp.factorint(block_h_left).items()} == data[
        "common_h_factorization"
    ]

    print("PASS")
    print(f"K={k}")
    print(f"M={m}")
    print(f"N={block_h_left}")
    print(f"gcd(K,{args.forbidden_product})={gcd(k, args.forbidden_product)}")
    print(f"gcd(M,{args.forbidden_product})={gcd(m, args.forbidden_product)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
