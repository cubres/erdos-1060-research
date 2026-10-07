#!/usr/bin/env python3
"""Search for h-collisions whose two inputs have the same prime signature."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, vstack

SEARCH_DIR = Path(__file__).parent.parent / "ksigma_rough_collision_search_2026-09-05"
sys.path.insert(0, str(SEARCH_DIR))
from search import make_columns, relation_core, verify  # noqa: E402


def build(columns, max_exponent):
    n = len(columns)
    bases = sorted({p for p, _, _ in columns})
    rows = sorted({q for _, _, factors in columns for q in factors})
    row_index = {q: i for i, q in enumerate(rows)}

    rr, cc, data = [], [], []
    for j, (_, _, factors) in enumerate(columns):
        for q, a in factors.items():
            i = row_index[q]
            rr.extend((i, i)); cc.extend((j, n + j)); data.extend((a, -a))
    matrices = [coo_matrix((data, (rr, cc)), shape=(len(rows), 2 * n)).tocsc()]
    lower = [0.0] * len(rows); upper = [0.0] * len(rows)

    rr, cc, data = [], [], []
    row = 0
    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)
    for p in bases:
        for offset in (0, n):
            for j in by_base[p]:
                rr.append(row); cc.append(offset + j); data.append(1)
            lower.append(0.0); upper.append(1.0); row += 1
    for j in range(n):
        rr.extend((row, row)); cc.extend((j, n + j)); data.extend((1, 1))
        lower.append(0.0); upper.append(1.0); row += 1
    # Equal multiplicity of every exponent on the two sides.
    for e in range(1, max_exponent + 1):
        for j, (_, exponent, _) in enumerate(columns):
            if exponent == e:
                rr.extend((row, row)); cc.extend((j, n + j)); data.extend((1, -1))
        lower.append(0.0); upper.append(0.0); row += 1
    # Exclude the empty relation.
    for j in range(2 * n):
        rr.append(row); cc.append(j); data.append(1)
    lower.append(2.0); upper.append(float(2 * n)); row += 1
    matrices.append(coo_matrix((data, (rr, cc)), shape=(row, 2 * n)).tocsc())
    return vstack(matrices, format="csc"), np.array(lower), np.array(upper)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upper", type=int, default=3000)
    parser.add_argument("--max-exponent", type=int, default=8)
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("equal_exponent_pattern_collision.json"))
    args = parser.parse_args()

    original, occurrences = make_columns(2, args.upper, args.max_exponent)
    columns = relation_core(original, occurrences)
    n = len(columns)
    print(f"upper={args.upper} e={args.max_exponent} original={len(original)} "
          f"core={n} bases={len({p for p, _, _ in columns})}", flush=True)
    matrix, lower, upper = build(columns, args.max_exponent)
    objective = np.ones(2 * n)
    result = milp(objective, integrality=np.ones(2 * n),
                  bounds=Bounds(np.zeros(2 * n), np.ones(2 * n)),
                  constraints=LinearConstraint(matrix, lower, upper),
                  options={"time_limit": args.seconds, "presolve": True, "mip_rel_gap": 0.0})
    print(result.message, flush=True)
    if result.x is None:
        return 1
    left = [(columns[j][0], columns[j][1]) for j in range(n) if result.x[j] > .5]
    right = [(columns[j][0], columns[j][1]) for j in range(n) if result.x[n + j] > .5]
    certificate = verify(left, right, 1)
    assert sorted(e for _, e in left) == sorted(e for _, e in right)
    certificate["prime_signature"] = sorted(e for _, e in left)
    certificate["search"] = {
        "upper": args.upper, "max_exponent": args.max_exponent,
        "original_columns": len(original), "core_columns": n,
        "status": int(result.status), "message": result.message,
    }
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(certificate, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
