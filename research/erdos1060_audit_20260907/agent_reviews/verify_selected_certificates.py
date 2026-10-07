"""Independent, exact finite checks supporting the lemma audit.

This script does not prove an asymptotic theorem. It uses explicit small-prime
factorizations and Python integers; it does not import the supplied verifiers.
"""
from fractions import Fraction
from itertools import product
from math import gcd, isqrt, prod
import json


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def value(factors):
    return prod(p**e for p, e in factors.items())


def sigma(factors):
    return prod((p ** (e + 1) - 1) // (p - 1) for p, e in factors.items())


def h(factors):
    return value(factors) * sigma(factors)


def vp(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def fiber(factors):
    n = value(factors)
    ps = sorted(factors)
    found = []
    for exponents in product(*(range(factors[p] + 1) for p in ps)):
        f = dict(zip(ps, exponents))
        k = value(f)
        if k * k <= n and h(f) == n:
            found.append(k)
    return sorted(found)


def main():
    a = {11: 2, 13: 2, 17: 1, 19: 1, 31: 1, 61: 1, 97: 1,
         127: 2, 271: 1, 307: 2, 331: 1, 367: 1}
    b = {13: 1, 17: 2, 19: 2, 23: 1, 31: 2, 43: 1, 61: 2,
         83: 1, 127: 1, 307: 1, 733: 1, 5419: 1}
    target = {2: 20, 3: 5, 5: 1, 7: 3, 11: 2, 13: 2, 17: 2,
              19: 2, 23: 1, 31: 2, 43: 1, 61: 2, 83: 1, 97: 1,
              127: 2, 271: 1, 307: 2, 331: 1, 367: 1, 733: 1, 5419: 1}
    assert all(prime(p) for p in set(a) | set(b) | set(target))
    assert h(a) == h(b) == value(target)
    ps = sorted(set(a) | set(b))
    common = {p: min(a.get(p, 0), b.get(p, 0)) for p in ps}
    local_gcd_product = prod(gcd(sigma({p: a.get(p, 0)}),
                                sigma({p: b.get(p, 0)})) for p in ps)
    r = sigma(common) // local_gcd_product
    t = gcd(sigma(a), sigma(b)) // local_gcd_product
    euler = prod(Fraction(p, p - 1) for p in target)
    labels_changed = [p for p in ps if any(
        vp(sigma({p: a.get(p, 0)}), q) != vp(sigma({p: b.get(p, 0)}), q)
        for q in (2, 3))]
    variations = {q: sum(abs(vp(sigma({p: a.get(p, 0)}), q) -
                                 vp(sigma({p: b.get(p, 0)}), q)) for p in ps)
                  for q in (2, 3)}
    assert r == 394214768640 and t == 436988805120
    assert Fraction(t, r) == Fraction(378, 341)
    assert 4 < euler < 8 < 9
    assert len(labels_changed) == 16
    assert variations == {2: 40, 3: 10}
    assert all(variations[q] == 2 * vp(t, q) for q in variations)
    n0 = {2: 7, 3: 3, 5: 1, 7: 2, 13: 1, 19: 2, 127: 1}
    n7 = {2: 28, 3: 3, 5: 1, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1}
    assert all(prime(p) for p in set(n0) | set(n7))
    f0, f7 = fiber(n0), fiber(n7)
    assert f0 == [492765]
    assert f7 == [5079674880, 5119047360, 5242895280, 5660209152,
                  5704081344, 5804634060, 5842083312]
    exchange_pairs = [({2: 12, 127: 1}, {2: 6, 8191: 1}),
                      ({2: 12, 31: 1}, {2: 4, 8191: 1}),
                      ({3: 2, 5: 1, 7: 1}, {3: 3, 13: 1}),
                      ({2: 12, 7: 1}, {2: 2, 8191: 1})]
    for left, right in exchange_pairs:
        assert h(left) == h(right)
        changed = sorted(set(left) | set(right))
        for mask in range(1, (1 << len(changed)) - 1):
            subset = [p for j, p in enumerate(changed) if mask >> j & 1]
            assert h({p: left.get(p, 0) for p in subset}) != h(
                {p: right.get(p, 0) for p in subset})
    # No supplied logs or supplied checking routines are premises.
    result = {"large_collision": {"a": value(a), "b": value(b),
               "N": value(target), "R": r, "T": t,
               "ratio": str(Fraction(t, r)), "changed_small_prime_labels": len(labels_changed),
               "variations": variations},
              "N0_full_fiber": f0, "N7_full_fiber": f7,
              "N7_minimal_exchanges_checked": len(exchange_pairs),
              "status": "PASS: finite identities and finite fibers only"}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
