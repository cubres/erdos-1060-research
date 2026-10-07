#!/usr/bin/env python3
"""Exact rank and binary-cell audit for the rough-210 cubefree collision.

All arithmetic assertions are checked with Python integers.  SymPy is used
only for exact integer factorization and an exact determinant/rank check.
The 2^17 binary words in the specified local-state box are also enumerated.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import product
from pathlib import Path

from sympy import Matrix, factorint


ROOT = Path(__file__).resolve().parent.parent
CERTIFICATE = ROOT / "ksigma_verification_2026-09-05/cubefree_rough210_collision.json"


def sigma_prime_power(p: int, e: int) -> int:
    return (p ** (e + 1) - 1) // (p - 1)


def block(p: int, e: int) -> int:
    return 1 if e == 0 else p**e * sigma_prime_power(p, e)


def valuation_vector(p: int, e: int) -> Counter[int]:
    return Counter({int(q): int(a) for q, a in factorint(block(p, e)).items()})


def main() -> None:
    data = json.loads(CERTIFICATE.read_text())
    left = {int(p): int(e) for p, e in data["left_blocks"]}
    right = {int(p): int(e) for p, e in data["right_blocks"]}
    bases = sorted(set(left) | set(right))
    assert len(bases) == 17
    assert all(left.get(p, 0) != right.get(p, 0) for p in bases)

    left_h = 1
    right_h = 1
    for p in bases:
        left_h *= block(p, left.get(p, 0))
        right_h *= block(p, right.get(p, 0))
    assert left_h == right_h == int(data["common_h"])

    # Columns are nu(H(p,right state))-nu(H(p,left state)).
    columns: list[dict[int, int]] = []
    all_rows: set[int] = set()
    for p in bases:
        a = valuation_vector(p, left.get(p, 0))
        b = valuation_vector(p, right.get(p, 0))
        column = {
            q: b.get(q, 0) - a.get(q, 0)
            for q in set(a) | set(b)
            if b.get(q, 0) != a.get(q, 0)
        }
        columns.append(column)
        all_rows.update(column)

    rows = sorted(all_rows)
    matrix = Matrix([[column.get(q, 0) for column in columns] for q in rows])
    assert matrix * Matrix([1] * len(bases)) == Matrix.zeros(len(rows), 1)

    # A compact exact lower-rank certificate: this 16 by 16 minor is -12.
    minor_column_bases = bases[:-1]
    minor_row_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 31, 43, 83, 97, 127, 271, 367]
    minor = Matrix(
        [
            [columns[bases.index(p)].get(q, 0) for p in minor_column_bases]
            for q in minor_row_primes
        ]
    )
    determinant = int(minor.det())
    assert determinant == -12
    rank = int(matrix.rank())
    assert rank == 16

    support_degrees = {
        q: sum(column.get(q, 0) != 0 for column in columns) for q in rows
    }
    assert min(support_degrees.values()) >= 2

    # Exhaust the explicitly specified binary box.  Bit 0 selects the left
    # local state and bit 1 the right local state.
    hits: list[dict[str, object]] = []
    target = left_h
    for bits in product((0, 1), repeat=len(bases)):
        value = 1
        input_value = 1
        for bit, p in zip(bits, bases):
            e = right.get(p, 0) if bit else left.get(p, 0)
            value *= block(p, e)
            input_value *= p**e
        if value == target:
            hits.append({"bits": "".join(map(str, bits)), "input": input_value})
    assert len(hits) == 2
    assert {int(hit["input"]) for hit in hits} == {
        int(data["left_input"]),
        int(data["right_input"]),
    }

    result = {
        "source_certificate": str(CERTIFICATE),
        "exact_integer_arithmetic": True,
        "binary_coordinate_count": len(bases),
        "bases": bases,
        "valuation_rows": rows,
        "valuation_row_count": len(rows),
        "rank_over_Q": rank,
        "nullity": len(bases) - rank,
        "kernel_vector": [1] * len(bases),
        "minor_column_bases": minor_column_bases,
        "minor_row_primes": minor_row_primes,
        "minor_determinant": determinant,
        "support_degrees": support_degrees,
        "minimum_support_degree": min(support_degrees.values()),
        "initial_private_witness_rows": [],
        "binary_words_exhausted": 2 ** len(bases),
        "target_hits": hits,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
