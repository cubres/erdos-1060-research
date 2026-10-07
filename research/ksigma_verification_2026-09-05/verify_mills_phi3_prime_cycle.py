#!/usr/bin/env python3
"""Verify a very small-mass prime 2-cycle for Phi_3(X)=X^2+X+1.

This is not an h-collision and not a counterfamily.  It is an exact quantitative
warning for proofs that try to charge substantial Euler mass merely for the
existence of a cyclotomic dependency cycle: any such local charge would have to
be smaller than the value certified below unless it uses additional structure.
"""

from __future__ import annotations

from decimal import Decimal, getcontext


P = 22_419_767_768_701
Q = 107_419_560_853_453
PREVIOUS = 4_679_277_990_051
NEXT = 514_678_036_498_563


def is_prime_below_2_64(n: int) -> bool:
    """Deterministic Miller--Rabin for n < 2^64."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small:
        if n % prime == 0:
            return n == prime
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    # This base set is deterministic throughout the unsigned 64-bit range.
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        value = pow(base % n, d, n)
        if value in (1, n - 1):
            continue
        for _ in range(s - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False
    return True


def phi3(value: int) -> int:
    return value * value + value + 1


def main() -> None:
    assert P < Q < 2**64
    assert is_prime_below_2_64(P)
    assert is_prime_below_2_64(Q)
    assert phi3(P) == PREVIOUS * Q
    assert phi3(Q) == P * NEXT
    assert PREVIOUS + Q == 5 * P - 1
    assert P + NEXT == 5 * Q - 1
    assert phi3(P) % Q == 0
    assert phi3(Q) % P == 0

    numerator = P * Q
    denominator = (P - 1) * (Q - 1)
    # Product p/(p-1) over the two bases is less than 1+6e-14.
    assert (numerator - denominator) * 10**14 < 6 * denominator
    getcontext().prec = 60
    product = Decimal(numerator) / Decimal(denominator)
    mass = product.ln()
    print("PASS primality and mutual Phi_3 divisibility")
    print(f"p={P}; q={Q}")
    print(f"Euler product={product}")
    print(f"Euler mass={mass}")


if __name__ == "__main__":
    main()
