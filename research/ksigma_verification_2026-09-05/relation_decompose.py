#!/usr/bin/env python3
"""Find conformal exact subrelations inside collision certificates via MILP.

The floating-point MILP is only a search oracle.  Every returned subset is
checked again with exact Python valuation vectors.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

sys.path.insert(0, str(Path(__file__).parent))
from structural_graph import block_factors, factors_from_blocks, product_from_factors


Column = tuple[str, int, int]


def differing_columns(left: dict[int, int], right: dict[int, int]) -> list[Column]:
    result: list[Column] = []
    for p in sorted(set(left) | set(right)):
        le, re = left.get(p, 0), right.get(p, 0)
        if le == re:
            continue
        if le:
            result.append(("L", p, le))
        if re:
            result.append(("R", p, re))
    return result


def exact_balanced(columns: list[Column]) -> bool:
    balance: Counter[int] = Counter()
    for side, p, e in columns:
        sign = 1 if side == "L" else -1
        balance.update({q: sign * a for q, a in block_factors(p, e).items()})
    return all(a == 0 for a in balance.values())


def proper_subrelation(columns: list[Column]) -> list[Column] | None:
    assert exact_balanced(columns)
    if len(columns) <= 2:
        return None
    rows = sorted({q for _, p, e in columns for q in block_factors(p, e)})
    A = np.zeros((len(rows), len(columns)), dtype=float)
    for j, (side, p, e) in enumerate(columns):
        sign = 1 if side == "L" else -1
        f = block_factors(p, e)
        for i, q in enumerate(rows):
            A[i, j] = sign * f.get(q, 0)
    constraints = [LinearConstraint(csc_matrix(A), np.zeros(len(rows)), np.zeros(len(rows)))]
    constraints.append(
        LinearConstraint(
            csc_matrix(np.ones((1, len(columns)))),
            np.array([1.0]),
            np.array([float(len(columns) - 1)]),
        )
    )
    result = milp(
        np.ones(len(columns)),
        integrality=np.ones(len(columns)),
        bounds=Bounds(np.zeros(len(columns)), np.ones(len(columns))),
        constraints=constraints,
        options={"presolve": True},
    )
    if result.x is None:
        return None
    selected = [c for c, x in zip(columns, result.x) if x > 0.5]
    if not (0 < len(selected) < len(columns)) or not exact_balanced(selected):
        raise AssertionError((result.message, selected))
    return selected


def atoms(columns: list[Column]) -> list[list[Column]]:
    sub = proper_subrelation(columns)
    if sub is None:
        return [columns]
    chosen = set(sub)
    complement = [c for c in columns if c not in chosen]
    assert exact_balanced(complement)
    return atoms(sub) + atoms(complement)


def summarize(name: str, left: dict[int, int], right: dict[int, int]) -> None:
    columns = differing_columns(left, right)
    assert exact_balanced(columns)
    pieces = atoms(columns)
    print(f"{name}: total_blocks={len(columns)} atoms={len(pieces)} sizes={[len(x) for x in pieces]}")
    for i, piece in enumerate(pieces, 1):
        lb = [(p, e) for side, p, e in piece if side == "L"]
        rb = [(p, e) for side, p, e in piece if side == "R"]
        value = product_from_factors(factors_from_blocks(lb))
        assert value == product_from_factors(factors_from_blocks(rb))
        print(f"  atom {i}: L={lb} R={rb} h={value}")


def main() -> None:
    cases = [
        ("tensor", {**dict(), **{p: e for p, e in []}}, {}),
        (
            "coprime6",
            {13: 2, 17: 1, 31: 1, 37: 3, 61: 1, 67: 2, 73: 1, 97: 1, 137: 1},
            {5: 1, 7: 2, 23: 1, 31: 3, 37: 2, 61: 2, 67: 1, 137: 2},
        ),
        (
            "coprime30",
            {7: 2, 11: 2, 13: 1, 31: 2, 37: 1, 43: 1, 61: 1, 83: 1, 127: 1},
            {7: 5, 11: 3, 19: 2, 31: 3, 331: 1},
        ),
    ]
    # Fill the tensor pair by direct factorizations without importing a second helper.
    cases[0] = (
        "tensor",
        {2: 6, 3: 2, 5: 1, 7: 1, 31: 1},
        {2: 4, 3: 3, 13: 1, 127: 1},
    )
    rough = json.loads(
        Path(
            "/Users/cubres/Documents/ChatGPT/Research/"
            "ksigma_rough_collision_search_2026-09-05/collision_11_700_e8.json"
        ).read_text()
    )
    cases.append(("coprime210", dict(rough["left_blocks"]), dict(rough["right_blocks"])))
    for args in cases:
        summarize(*args)


if __name__ == "__main__":
    main()
