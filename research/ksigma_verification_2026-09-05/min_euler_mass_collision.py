#!/usr/bin/env python3
"""Search exactly for a bounded-exponent h-collision of small Euler mass.

The MILP objective is floating point, but every incumbent is reconstructed and
verified in arbitrary-precision integer arithmetic.  The computation is only a
counterexample search; absence of an incumbent is not used as a theorem.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

SEARCH_DIR = Path(
    "/Users/cubres/Documents/ChatGPT/Research/ksigma_rough_collision_search_2026-09-05"
)
sys.path.insert(0, str(SEARCH_DIR))
from search import make_columns, relation_core, verify


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upper", type=int, default=7000)
    ap.add_argument("--max-exponent", type=int, default=2)
    ap.add_argument("--forbid-through", type=int, default=7)
    ap.add_argument("--seconds", type=float, default=300.0)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    original, _ = make_columns(2, args.upper, args.max_exponent)
    filtered = [c for c in original if c[0] > args.forbid_through]
    occurrences = defaultdict(set)
    for j, (_, _, factors) in enumerate(filtered):
        for q in factors:
            occurrences[q].add(j)
    columns = relation_core(filtered, occurrences)
    n = len(columns)
    bases = sorted({p for p, _, _ in columns})
    rows = sorted({q for _, _, f in columns for q in f})
    ri = {q: i for i, q in enumerate(rows)}
    bi = {p: i for i, p in enumerate(bases)}
    # Variables are left blocks, right blocks, and union-of-base indicators.
    nv = 2 * n + len(bases)
    rr: list[int] = []
    cc: list[int] = []
    data: list[float] = []
    lo: list[float] = []
    hi: list[float] = []

    def add(terms, lower, upper):
        row = len(lo)
        for variable, coefficient in terms:
            if coefficient:
                rr.append(row)
                cc.append(variable)
                data.append(coefficient)
        lo.append(lower)
        hi.append(upper)

    for q in rows:
        terms = []
        for j, (_, _, factors) in enumerate(columns):
            a = factors.get(q, 0)
            if a:
                terms.extend(((j, a), (n + j, -a)))
        add(terms, 0, 0)

    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)
    for p, js in by_base.items():
        add(((j, 1) for j in js), 0, 1)
        add(((n + j, 1) for j in js), 0, 1)
        y = 2 * n + bi[p]
        for j in js:
            add(((j, 1), (y, -1)), -np.inf, 0)
            add(((n + j, 1), (y, -1)), -np.inf, 0)
    # Identical local states cancel, so exclude them on opposite sides.
    for j in range(n):
        add(((j, 1), (n + j, 1)), 0, 1)
    add(((j, 1) for j in range(2 * n)), 1, 2 * n)

    matrix = coo_matrix((data, (rr, cc)), shape=(len(lo), nv)).tocsc()
    objective = np.zeros(nv)
    for p in bases:
        objective[2 * n + bi[p]] = -math.log1p(-1.0 / p)
    result = milp(
        objective,
        integrality=np.ones(nv),
        bounds=Bounds(np.zeros(nv), np.ones(nv)),
        constraints=LinearConstraint(matrix, np.array(lo), np.array(hi)),
        options={"time_limit": args.seconds, "presolve": True, "mip_rel_gap": 0.0},
    )
    print(
        f"columns={n} bases={len(bases)} rows={len(rows)} status={result.status} "
        f"message={result.message}",
        flush=True,
    )
    if result.x is None:
        raise SystemExit(1)
    left = [
        (columns[j][0], columns[j][1]) for j in range(n) if result.x[j] > 0.5
    ]
    right = [
        (columns[j][0], columns[j][1])
        for j in range(n)
        if result.x[n + j] > 0.5
    ]
    cert = verify(left, right, 1)
    dl, dr = dict(left), dict(right)
    differing = sorted(set(dl) | set(dr))
    differing = [p for p in differing if dl.get(p, 0) != dr.get(p, 0)]
    mass = sum(-math.log1p(-1.0 / p) for p in differing)
    out = {
        "left_blocks": left,
        "right_blocks": right,
        "common_h": cert["common_h"],
        "common_h_factorization": cert["common_h_factorization"],
        "differing_bases": differing,
        "euler_mass": mass,
        "euler_product": math.exp(mass),
        "search": {
            "upper": args.upper,
            "max_exponent": args.max_exponent,
            "forbid_through": args.forbid_through,
            "core_columns": n,
            "status": int(result.status),
        },
    }
    print(json.dumps(out, indent=2))
    if args.output:
        args.output.write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
