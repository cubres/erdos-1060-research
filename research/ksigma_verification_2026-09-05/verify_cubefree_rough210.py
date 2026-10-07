#!/usr/bin/env python3
"""Standard-library verifier for cubefree_rough210_collision.json.

It checks primality and uniqueness of every input base, reconstructs both
inputs and divisor sums, verifies the common h-value and its stated prime
factorization, checks coprimality to 210, and exhaustively rules out every
proper conformal subrelation among the 12 local blocks on each side.
"""

from __future__ import annotations

import json
import itertools
import math
import pathlib
import sys
from collections import Counter


DEFAULT_CERTIFICATE = pathlib.Path(__file__).with_name(
    "cubefree_rough210_collision.json"
)


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


def factor_small(n: int) -> Counter[int]:
    """Trial-factor the local sigma values (all are small in this certificate)."""
    answer: Counter[int] = Counter()
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            answer[divisor] += 1
            n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        answer[n] += 1
    return answer


def sigma_prime_power(p: int, exponent: int) -> int:
    return (p ** (exponent + 1) - 1) // (p - 1)


def reconstruct(blocks: list[tuple[int, int]]):
    value = 1
    divisor_sum = 1
    h_factors: Counter[int] = Counter()
    local_h = []
    for p, exponent in blocks:
        value *= p**exponent
        local_sigma = sigma_prime_power(p, exponent)
        divisor_sum *= local_sigma
        h_factors[p] += exponent
        h_factors.update(factor_small(local_sigma))
        local_h.append(p**exponent * local_sigma)
    return value, divisor_sum, value * divisor_sum, h_factors, local_h


def subset_products(values: list[int]) -> list[int]:
    products = [1] * (1 << len(values))
    for mask in range(1, len(products)):
        low_bit = mask & -mask
        index = low_bit.bit_length() - 1
        products[mask] = products[mask ^ low_bit] * values[index]
    return products


def h_from_factorization(factors: dict[int, int]) -> int:
    return math.prod(
        p**exponent * sigma_prime_power(p, exponent)
        for p, exponent in factors.items()
        if exponent
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    certificate_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CERTIFICATE
    with certificate_path.open(encoding="utf-8") as stream:
        data = json.load(stream)

    left = [tuple(pair) for pair in data["left_blocks"]]
    right = [tuple(pair) for pair in data["right_blocks"]]

    for name, blocks in (("left", left), ("right", right)):
        bases = [p for p, _ in blocks]
        require(len(bases) == len(set(bases)), f"{name}: repeated input base")
        require(all(is_prime(p) for p in bases), f"{name}: a base is not prime")
        require(all(exponent in (1, 2) for _, exponent in blocks),
                f"{name}: input is not cubefree")

    left_value, left_sigma, left_h, left_factors, left_local_h = reconstruct(left)
    right_value, right_sigma, right_h, right_factors, right_local_h = reconstruct(right)

    require(left_value == data["left_input"], "left input decimal is wrong")
    require(right_value == data["right_input"], "right input decimal is wrong")
    require(left_sigma == data["left_sigma"], "left sigma decimal is wrong")
    require(right_sigma == data["right_sigma"], "right sigma decimal is wrong")
    require(left_value != right_value, "the two inputs are not distinct")
    require(left_h == right_h == data["common_h"], "common h decimal is wrong")
    require(math.gcd(left_value, 210) == math.gcd(right_value, 210) == 1,
            "an input is not coprime to 210")
    require(math.gcd(left_value, right_value) == data["gcd_inputs"],
            "stated input gcd is wrong")
    require(math.gcd(left_value, left_sigma) == data["left_gcd_input_sigma"],
            "stated left gcd(k,sigma(k)) is wrong")
    require(math.gcd(right_value, right_sigma) == data["right_gcd_input_sigma"],
            "stated right gcd(k,sigma(k)) is wrong")

    # Moser-primitivity asks whether dividing both inputs by any common
    # divisor d>1 leaves another collision.  Here the common divisor is
    # squarefree on seven bases, so all 2^7-1 cases can be checked literally.
    left_input_factors = dict(left)
    right_input_factors = dict(right)
    common_bases = sorted(set(left_input_factors).intersection(right_input_factors))
    common_divisors_checked = 0
    for choices in itertools.product((0, 1), repeat=len(common_bases)):
        if not any(choices):
            continue
        reduced_left = left_input_factors.copy()
        reduced_right = right_input_factors.copy()
        for p, remove in zip(common_bases, choices):
            if remove:
                reduced_left[p] -= 1
                reduced_right[p] -= 1
        common_divisors_checked += 1
        require(h_from_factorization(reduced_left) != h_from_factorization(reduced_right),
                "a nontrivial common divisor preserves the collision")
    require(data["moser_primitive"] is True,
            "certificate does not declare Moser-primitivity")
    require(common_divisors_checked == data["nontrivial_common_divisors_checked"],
            "wrong number of common divisors checked")

    declared_factors = Counter(
        {int(prime): exponent for prime, exponent in data["common_h_factorization"].items()}
    )
    require(left_factors == right_factors == declared_factors,
            "local factor accumulation disagrees with the stated factorization")
    reconstructed_h = math.prod(p**exponent for p, exponent in declared_factors.items())
    require(reconstructed_h == left_h, "stated prime factorization has wrong product")
    require(all(is_prime(p) for p in declared_factors),
            "stated factorization contains a composite base")

    # A proper conformal subrelation would be an equality between products of
    # nonempty proper subsets of the displayed local H(p,e) blocks. There are
    # only 2^12 subsets on each side, so this is a literal exhaustive check.
    left_products = subset_products(left_local_h)
    right_products = subset_products(right_local_h)
    common_products = set(left_products).intersection(right_products)
    require(common_products == {1, left_h},
            "a nontrivial proper conformal subrelation exists")
    require(left_products.count(left_h) == right_products.count(right_h) == 1,
            "the full relation is not represented uniquely on a side")

    print("PASS: exact cubefree h-collision, both inputs coprime to 210")
    print(f"K = {left_value}")
    print(f"sigma(K) = {left_sigma}")
    print(f"M = {right_value}")
    print(f"sigma(M) = {right_sigma}")
    print(f"N = K*sigma(K) = M*sigma(M) = {left_h}")
    print(f"PASS: Moser-primitive; {common_divisors_checked} common divisors checked")
    print("PASS: 4096 subsets per side; only common products are 1 and N")


if __name__ == "__main__":
    main()
