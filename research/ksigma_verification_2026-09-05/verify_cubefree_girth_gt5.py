#!/usr/bin/env python3
"""Independent exact verifier for the cubefree directed-girth-six collision.

This uses only Python's standard library.  In particular it does not import
the MILP discovery script, SciPy, SymPy, or NetworkX.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).parent
DATA = HERE / "cubefree_girth_gt5_collision.json"


def factor(n: int) -> Counter[int]:
    result: Counter[int] = Counter()
    d = 2
    while d * d <= n:
        while n % d == 0:
            result[d] += 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        result[n] += 1
    return result


def is_prime(n: int) -> bool:
    return n >= 2 and factor(n) == Counter({n: 1})


def sigma_pp(p: int, e: int) -> int:
    direct = sum(p**j for j in range(e + 1))
    assert direct == (p ** (e + 1) - 1) // (p - 1)
    return direct


def block_factors(p: int, e: int) -> Counter[int]:
    result = Counter({p: e})
    result.update(factor(sigma_pp(p, e)))
    return result


def aggregate(blocks: list[list[int]]) -> tuple[int, int, Counter[int]]:
    value = math.prod(p**e for p, e in blocks)
    sigma = math.prod(sigma_pp(p, e) for p, e in blocks)
    factors: Counter[int] = Counter()
    for p, e in blocks:
        factors.update(block_factors(p, e))
    return value, sigma, factors


def h_from_factorization(factors: Counter[int]) -> int:
    return math.prod(p**e * sigma_pp(p, e) for p, e in factors.items())


def canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    return min(cycle[i:] + cycle[:i] for i in range(len(cycle)))


def all_directed_cycles(vertices: set[int], arrows: set[tuple[int, int]]):
    adjacency = defaultdict(set)
    for p, q in arrows:
        adjacency[p].add(q)
    cycles = set()
    for start in vertices:
        def visit(path: tuple[int, ...]) -> None:
            for q in adjacency[path[-1]]:
                if q == start and len(path) >= 2:
                    cycles.add(canonical_cycle(path))
                elif q not in path:
                    visit(path + (q,))
        visit((start,))
    return sorted(cycles, key=lambda x: (len(x), x))


def verify_conformal_atom(signed_vectors: list[dict[int, int]]) -> int:
    """Gray-code exhaust every nonempty proper subset, exactly."""
    width = len(signed_vectors)
    full_mask = (1 << width) - 1
    balance: defaultdict[int, int] = defaultdict(int)
    nonzero_coordinates = 0
    previous_gray = 0
    checked = 0
    for index in range(1, 1 << width):
        gray = index ^ (index >> 1)
        changed = gray ^ previous_gray
        column = changed.bit_length() - 1
        add = 1 if gray & changed else -1
        for q, coefficient in signed_vectors[column].items():
            before = balance[q]
            after = before + add * coefficient
            if before == 0 and after != 0:
                nonzero_coordinates += 1
            elif before != 0 and after == 0:
                nonzero_coordinates -= 1
            balance[q] = after
        previous_gray = gray
        if gray == full_mask:
            assert nonzero_coordinates == 0  # the complete signed relation
            continue
        checked += 1
        assert nonzero_coordinates != 0, f"proper zero subrelation mask={gray}"
    return checked


def main() -> None:
    data = json.loads(DATA.read_text())
    left, right = data["left_blocks"], data["right_blocks"]
    all_blocks = left + right
    assert all(is_prime(p) and e in (1, 2) for p, e in all_blocks)
    assert len({p for p, _ in left}) == len(left)
    assert len({p for p, _ in right}) == len(right)

    k, sigma_k, left_factors = aggregate(left)
    m, sigma_m, right_factors = aggregate(right)
    n = k * sigma_k
    assert left_factors == right_factors
    assert n == m * sigma_m
    assert (k, sigma_k, m, sigma_m, n) == (
        data["left_input"], data["left_sigma"], data["right_input"],
        data["right_sigma"], data["common_h"],
    )
    claimed_factorization = Counter(
        {int(p): e for p, e in data["common_h_factorization"].items()}
    )
    assert left_factors == claimed_factorization
    assert math.prod(p**e for p, e in claimed_factorization.items()) == n

    # Exact Moser primitivity: no nontrivial common divisor d can be divided
    # from both inputs while preserving h(k/d)=h(m/d).
    left_input_f = Counter(dict(left))
    right_input_f = Counter(dict(right))
    common = left_input_f & right_input_f
    gcd_value = math.prod(p**e for p, e in common.items())
    assert gcd_value == math.gcd(k, m) == data["gcd"]
    assert common == Counter({int(p): e for p, e in data["gcd_factorization"].items()})
    primitive_tests = 0
    for exponents in itertools.product(*[range(e + 1) for e in common.values()]):
        divisor_f = Counter({p: e for p, e in zip(common, exponents) if e})
        if not divisor_f:
            continue
        primitive_tests += 1
        assert h_from_factorization(left_input_f - divisor_f) != h_from_factorization(
            right_input_f - divisor_f
        )
    assert primitive_tests == data["nontrivial_common_divisors_checked"] == 31

    # Exact conformal primitivity/atomicity.
    signed_vectors = []
    for sign, blocks in ((1, left), (-1, right)):
        for p, e in blocks:
            signed_vectors.append({q: sign*a for q, a in block_factors(p, e).items()})
    subset_tests = verify_conformal_atom(signed_vectors)
    assert subset_tests == data["proper_signed_subsets_checked"] == (1 << 21) - 2

    # Construct the in-base sigma graph and enumerate every simple directed
    # cycle.  This checks more than merely excluding lengths 2,...,5.
    bases = {p for p, _ in all_blocks}
    arrows = set()
    for p, e in all_blocks:
        for q in factor(sigma_pp(p, e)):
            if q in bases and q != p:
                arrows.add((p, q))
    cycles = all_directed_cycles(bases, arrows)
    assert cycles == [tuple(c) for c in data["directed_cycles"]]
    assert min(map(len, cycles)) == data["directed_girth"] == 6

    print("PASS")
    print(f"K={k}; sigma(K)={sigma_k}")
    print(f"M={m}; sigma(M)={sigma_m}")
    print(f"N={n}")
    print(f"gcd={gcd_value}; primitive_divisors_tested={primitive_tests}")
    print(f"signed_blocks={len(signed_vectors)}; proper_subsets_tested={subset_tests}")
    print(f"arrows={sorted(arrows)}")
    print(f"directed_cycles={cycles}; directed_girth=6")


if __name__ == "__main__":
    main()
