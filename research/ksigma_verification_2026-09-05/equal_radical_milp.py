#!/usr/bin/env python3
"""Exact finite MILP search for two h(k)=k*sigma(k) inputs of equal radical.

For every prime base p, a selected transition (a,b), a>b>=1, means that p
has exponent a on one side and b on the other.  Either orientation is allowed,
but at most one oriented transition may be used per base.  Prime-valuation
balance is imposed exactly.  Any incumbent is independently reconstructed with
Python arbitrary-precision integers before it is written.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
from sympy import factorint, primerange


def H(p: int, e: int) -> int:
    return p**e * ((p ** (e + 1) - 1) // (p - 1))


def factor_vector(value: int) -> dict[int, int]:
    return {int(q): int(a) for q, a in factorint(value).items()}


def difference(p: int, a: int, b: int) -> dict[int, int]:
    answer = factor_vector(H(p, a))
    for q, e in factor_vector(H(p, b)).items():
        answer[q] = answer.get(q, 0) - e
    return {q: e for q, e in answer.items() if e}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime-bound", type=int, default=1_000)
    parser.add_argument("--max-exponent", type=int, default=3)
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    labels: list[tuple[int, int, int]] = []
    vectors: list[dict[int, int]] = []
    by_base: dict[int, list[int]] = defaultdict(list)
    for p0 in primerange(2, args.prime_bound + 1):
        p = int(p0)
        for a in range(2, args.max_exponent + 1):
            for b in range(1, a):
                by_base[p].append(len(labels))
                labels.append((p, a, b))
                vectors.append(difference(p, a, b))

    # Variable 2*j is the displayed transition, 2*j+1 its reverse.
    row_index: list[int] = []
    col_index: list[int] = []
    coefficient: list[int] = []
    lower: list[float] = []
    upper: list[float] = []

    def add(terms, lo, hi):
        row = len(lower)
        for column, value in terms:
            if value:
                row_index.append(row)
                col_index.append(column)
                coefficient.append(value)
        lower.append(lo)
        upper.append(hi)

    valuation_primes = sorted(set().union(*(set(v) for v in vectors)))
    for q in valuation_primes:
        terms = []
        for j, vector in enumerate(vectors):
            value = vector.get(q, 0)
            if value:
                terms.extend(((2 * j, value), (2 * j + 1, -value)))
        add(terms, 0, 0)
    for indices in by_base.values():
        add(((2 * j + orientation, 1) for j in indices for orientation in (0, 1)), 0, 1)
    add(((j, 1) for j in range(2 * len(labels))), 1, np.inf)

    matrix = coo_matrix(
        (coefficient, (row_index, col_index)),
        shape=(len(lower), 2 * len(labels)),
    ).tocsc()
    objective = np.ones(2 * len(labels))
    print(
        f"bases={len(by_base)} columns={len(labels)} variables={2*len(labels)} "
        f"valuation_rows={len(valuation_primes)} constraints={len(lower)}",
        flush=True,
    )
    result = milp(
        objective,
        integrality=np.ones(2 * len(labels)),
        bounds=Bounds(np.zeros(2 * len(labels)), np.ones(2 * len(labels))),
        constraints=LinearConstraint(matrix, np.array(lower), np.array(upper)),
        options={"time_limit": args.time_limit, "presolve": True, "mip_rel_gap": 0.0},
    )
    print(f"status={result.status}; {result.message}", flush=True)
    if result.x is None:
        raise SystemExit(1)

    left: dict[int, int] = {}
    right: dict[int, int] = {}
    transitions = []
    for j, (p, a, b) in enumerate(labels):
        if result.x[2 * j] > 0.5:
            left[p], right[p] = a, b
            transitions.append((p, a, b))
        elif result.x[2 * j + 1] > 0.5:
            left[p], right[p] = b, a
            transitions.append((p, b, a))
    left_input = 1
    right_input = 1
    left_h = 1
    right_h = 1
    for p in sorted(left):
        left_input *= p ** left[p]
        right_input *= p ** right[p]
        left_h *= H(p, left[p])
        right_h *= H(p, right[p])
    assert left_h == right_h
    assert set(left) == set(right)
    assert left != right
    certificate = {
        "prime_bound": args.prime_bound,
        "max_exponent": args.max_exponent,
        "transition_count": len(transitions),
        "transitions_left_right": transitions,
        "left_input": left_input,
        "right_input": right_input,
        "common_h": left_h,
        "verified_equal_radical": True,
        "verified_equal_h": True,
    }
    print(json.dumps(certificate, indent=2))
    if args.output:
        args.output.write_text(json.dumps(certificate, indent=2) + "\n")


if __name__ == "__main__":
    main()
