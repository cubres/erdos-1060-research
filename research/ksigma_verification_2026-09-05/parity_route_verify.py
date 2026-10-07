#!/usr/bin/env python3
"""Exact arithmetic checks used in the parity route for h(n)=n*sigma(n)."""

from fractions import Fraction
from math import prod


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    return [p for p in range(2, limit + 1) if sieve[p]]


def factor(n: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for p in primes_through(int(n**0.5) + 1):
        if p * p > n:
            break
        while n % p == 0:
            result[p] = result.get(p, 0) + 1
            n //= p
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def sigma(n: int) -> int:
    return prod((p ** (e + 1) - 1) // (p - 1) for p, e in factor(n).items())


def valuation(n: int, p: int) -> int:
    exponent = 0
    while n % p == 0:
        exponent += 1
        n //= p
    return exponent


def main() -> None:
    # The exact Euler-product threshold in the coprime odd-square lemma.
    product_bound = Fraction(1, 1)
    crossing = None
    for index, p in enumerate(primes_through(24_247)[1:], 1):
        previous = product_bound
        product_bound *= Fraction(p, p - 1)
        if product_bound >= 9:
            crossing = (index, p, previous, product_bound)
            break
    assert crossing is not None
    index, p, previous, product_bound = crossing
    assert index == 2_697 and p == 24_247
    assert previous < 9 <= product_bound

    # Two support-disjoint collision blocks and their tensor product.
    first = (315, 351)
    second = (1_984, 2_032)
    first_target = first[0] * sigma(first[0])
    second_target = second[0] * sigma(second[0])
    assert first_target == first[1] * sigma(first[1]) == 196_560
    assert second_target == second[1] * sigma(second[1]) == 8_062_976
    tensor_target = first_target * second_target
    tensor_inputs = sorted(a * b for a in first for b in second)
    assert tensor_target == 1_584_858_562_560
    assert tensor_inputs == [624_960, 640_080, 696_384, 713_232]
    assert all(k * sigma(k) == tensor_target for k in tensor_inputs)
    assert valuation(tensor_target, 2) == 15
    assert max(factor(tensor_target).values()) == 15

    print(
        "odd-prime Euler product first reaches 9 at "
        f"index={index}, prime={p}; preceding product<9"
    )
    print(
        f"tensor target={tensor_target}, generated_preimages={tensor_inputs}, "
        "v2=15, maximum_target_valuation=15"
    )


if __name__ == "__main__":
    main()
