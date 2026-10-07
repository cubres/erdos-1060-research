#!/usr/bin/env python3
"""Independent exact checks for h(k)=k*sigma(k) fibers.

Uses only the Python standard library.  Large target fibers are checked by
enumerating every divisor of the target n, which is complete because h(k)=n
implies k|n.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from math import isqrt, prod
from urllib.request import Request, urlopen


def factor_trial(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out[p] = e
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = 1
    return out


def sigma_from_factor(factors: dict[int, int]) -> int:
    return prod((p ** (e + 1) - 1) // (p - 1) for p, e in factors.items())


def h_from_factor(factors: dict[int, int]) -> int:
    return prod(p**e for p, e in factors.items()) * sigma_from_factor(factors)


def check_primitive_pair(
    left: dict[int, int], right: dict[int, int]
) -> int:
    """Test Moser primitivity over every nontrivial common divisor."""
    common = {p: min(e, right.get(p, 0)) for p, e in left.items()}
    common = {p: e for p, e in common.items() if e}
    tested = 0
    choices = [[(p, e) for e in range(a + 1)] for p, a in common.items()]
    for selected in product(*choices):
        divisor = {p: e for p, e in selected if e}
        if not divisor:
            continue
        tested += 1
        left_q = {
            p: e - divisor.get(p, 0)
            for p, e in left.items()
            if e - divisor.get(p, 0)
        }
        right_q = {
            p: e - divisor.get(p, 0)
            for p, e in right.items()
            if e - divisor.get(p, 0)
        }
        assert h_from_factor(left_q) != h_from_factor(right_q)
    return tested


def sigma(n: int) -> int:
    return sigma_from_factor(factor_trial(n))


def divisors(factors: dict[int, int]):
    terms = [[p**e for e in range(a + 1)] for p, a in factors.items()]
    for powers in product(*terms):
        yield prod(powers)


def complete_fiber(n: int, factors: dict[int, int]) -> list[int]:
    assert prod(p**e for p, e in factors.items()) == n
    return sorted(d for d in divisors(factors) if d * sigma(d) == n)


def vp(n: int, p: int) -> int:
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def check_oeis_prefix() -> None:
    limit = 65_537
    counts = [0] * (limit + 1)
    for k in range(1, isqrt(limit) + 1):
        h = k * sigma(k)
        if h <= limit:
            counts[h] += 1
    request = Request(
        "https://oeis.org/A327153/b327153.txt",
        headers={"User-Agent": "ksigma-verification/1.0 (research spot-check)"},
    )
    raw = urlopen(request, timeout=30).read().decode()
    oeis = {}
    for line in raw.splitlines():
        if not line or line.startswith("#"):
            continue
        n_text, a_text = line.split()
        oeis[int(n_text)] = int(a_text)
    assert len(oeis) >= limit
    mismatches = [(n, counts[n], oeis[n]) for n in range(1, limit + 1)
                  if counts[n] != oeis[n]]
    assert not mismatches, mismatches[:10]
    print(f"OEIS A327153 prefix matched exactly for n=1..{limit}")


def check_named_fibers() -> None:
    cases = [
        (
            5_418_319_872,
            {2: 16, 3: 1, 7: 1, 31: 1, 127: 1},
            [41_664, 42_672, 47_244, 55_118],
        ),
        (
            1_584_858_562_560,
            {2: 15, 3: 3, 5: 1, 7: 1, 13: 1, 31: 1, 127: 1},
            [624_960, 640_080, 696_384, 708_660, 713_232],
        ),
        (
            3_351_219_307_843_680,
            {2: 5, 3: 3, 5: 1, 7: 4, 13: 1, 19: 1, 467: 1, 2801: 1},
            [35_684_740, 42_608_146],
        ),
        (
            7_089_671_638_182_002_688_000,
            {2: 31, 3: 2, 5: 3, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1},
            [42_330_624_000, 42_658_728_000, 43_690_794_000,
             48_371_950_500, 53_261_158_400, 56_433_942_250],
        ),
        (
            106_345_074_572_730_040_320,
            {2: 28, 3: 3, 5: 1, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1},
            [5_079_674_880, 5_119_047_360, 5_242_895_280, 5_660_209_152,
             5_704_081_344, 5_804_634_060, 5_842_083_312],
        ),
    ]
    for n, factors, expected in cases:
        got = complete_fiber(n, factors)
        assert got == expected, (n, got, expected)
        assert len({(vp(k, 2), vp(k, 3)) for k in got}) == len(got)
        theorem_bound = prod(factors.values())
        assert len(got) <= theorem_bound
        print(
            f"complete divisor audit: n={n}, f(n)={len(got)}, "
            f"preimages={got}, product(alpha)={theorem_bound}"
        )


def check_counterexamples() -> None:
    examples = [
        (27_776, [112, 124]),
        (196_560, [315, 351]),
        (3_351_219_307_843_680, [35_684_740, 42_608_146]),
    ]
    for n, ks in examples:
        assert all(k * sigma(k) == n for k in ks)
        print(f"collision verified: n={n}, k={ks}")

    full_omegas = []
    full_parts = []
    for k in examples[-1][1]:
        factors = factor_trial(k)
        full = {p: e for p, e in factors.items() if e >= 2}
        full_parts.append(prod(p**e for p, e in full.items()))
        full_omegas.append(sum(full.values()))
    assert full_parts == [196, 2401]
    assert full_omegas == [4, 4]
    print("Omega(full part) is not injective: full parts 196 and 2401 both have Omega=4")

    block_a = [1984, 2032]
    block_b = [315, 351]
    assert len({k * sigma(k) for k in block_a}) == 1
    assert len({k * sigma(k) for k in block_b}) == 1
    products = sorted(a * b for a in block_a for b in block_b)
    target = (block_a[0] * sigma(block_a[0])) * (block_b[0] * sigma(block_b[0]))
    assert target == 1_584_858_562_560
    assert all(k * sigma(k) == target for k in products)
    assert products == [624_960, 640_080, 696_384, 713_232]
    print(f"disjoint-block tensor verified: target={target}, four products={products}")


def check_coprime_to_six_counterexample() -> None:
    fk = {13: 2, 17: 1, 31: 1, 37: 3, 61: 1,
          67: 2, 73: 1, 97: 1, 137: 1}
    fm = {5: 1, 7: 2, 23: 1, 31: 3, 37: 2,
          61: 2, 67: 1, 137: 2}
    fn = {2: 12, 3: 5, 5: 1, 7: 4, 13: 2, 17: 1, 19: 1, 23: 1,
          31: 3, 37: 4, 61: 2, 67: 2, 73: 1, 97: 1, 137: 2}
    k = prod(p**e for p, e in fk.items())
    m = prod(p**e for p, e in fm.items())
    n = prod(p**e for p, e in fn.items())
    assert k == 1_198_387_013_221_054_310_407
    assert m == 1_075_370_347_698_293_222_695
    assert k % 6 == m % 6 == 1
    assert sigma_from_factor(fk) == 1_551_619_885_383_613_624_320
    assert sigma_from_factor(fm) == 1_729_116_972_658_938_949_632
    assert sum(divisors(fk)) == sigma_from_factor(fk)
    assert sum(divisors(fm)) == sigma_from_factor(fm)
    assert k * sigma_from_factor(fk) == m * sigma_from_factor(fm) == n
    assert n == 1_859_441_120_099_263_354_172_212_044_541_787_564_298_240
    common = 31 * 37**2 * 61 * 67 * 137
    from math import gcd
    assert gcd(k, m) == common == 23_762_402_441
    assert check_primitive_pair(fk, fm) == 47
    print(
        "coprime-to-6 collision verified: "
        f"K={k}, M={m}, gcd(K,M)={common}, N={n}, primitive_tests=47"
    )

    # A stronger projection counterexample: both inputs avoid 2, 3, and 5.
    fk2 = {7: 2, 11: 2, 13: 1, 31: 2, 37: 1,
           43: 1, 61: 1, 83: 1, 127: 1}
    fm2 = {7: 5, 11: 3, 19: 2, 31: 3, 331: 1}
    fn2 = {2: 14, 3: 3, 7: 5, 11: 3, 13: 1, 19: 3, 31: 3,
           37: 1, 43: 1, 61: 1, 83: 1, 127: 1, 331: 1}
    k2 = prod(p**e for p, e in fk2.items())
    m2 = prod(p**e for p, e in fm2.items())
    n2 = prod(p**e for p, e in fn2.items())
    assert k2 == 75_775_710_700_917_227
    assert m2 == 79_632_166_734_466_577
    assert k2 % 30 in (1, 7, 11, 13, 17, 19, 23, 29)
    assert m2 % 30 in (1, 7, 11, 13, 17, 19, 23, 29)
    assert sigma_from_factor(fk2) == 117_468_385_318_158_336
    assert sigma_from_factor(fm2) == 111_779_582_892_097_536
    assert sum(divisors(fk2)) == sigma_from_factor(fk2)
    assert sum(divisors(fm2)) == sigma_from_factor(fm2)
    assert k2 * sigma_from_factor(fk2) == m2 * sigma_from_factor(fm2) == n2
    assert n2 == 8_901_250_382_372_638_700_189_613_616_054_272
    assert gcd(k2, m2) == 5_697_769 == 7**2 * 11**2 * 31**2
    assert check_primitive_pair(fk2, fm2) == 26
    print(
        "coprime-to-30 collision verified: "
        f"K={k2}, M={m2}, gcd(K,M)={gcd(k2, m2)}, N={n2}, "
        "primitive_tests=26"
    )


if __name__ == "__main__":
    check_oeis_prefix()
    check_named_fibers()
    check_counterexamples()
    check_coprime_to_six_counterexample()
