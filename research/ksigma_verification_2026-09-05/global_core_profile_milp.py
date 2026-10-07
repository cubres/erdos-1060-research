#!/usr/bin/env python3
"""Exact finite search against global-core full-profile injectivity.

The model chooses three representations of one H-product.  No exact local
block may occur in all three, so their global common block core is empty.
The first two representations are required to be distinct but to have equal
histograms of (target valuation, input exponent).  Thus any incumbent is a
literal counterexample to the proposed global-core-normalized invariant.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

SEARCH_DIR = Path(
    "/Users/cubres/Documents/ChatGPT/Research/ksigma_rough_collision_search_2026-09-05"
)
sys.path.insert(0, str(SEARCH_DIR))
from search import make_columns, relation_core, verify


def profile(blocks, target):
    valuations = {}
    for p, _ in blocks:
        x, a = target, 0
        while x % p == 0:
            x //= p
            a += 1
        valuations[p] = a
    return sorted((valuations[p], e) for p, e in blocks)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upper", type=int, default=1_000)
    ap.add_argument("--max-exponent", type=int, default=2)
    ap.add_argument("--time-limit", type=float, default=600.0)
    ap.add_argument("--seed", nargs=2, type=int, metavar=("P", "E"))
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    original, occurrences = make_columns(2, args.upper, args.max_exponent)
    columns = relation_core(original, occurrences)
    n = len(columns)
    bases = sorted({p for p, _, _ in columns})
    rows = sorted({q for _, _, f in columns for q in f})
    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)

    # x(side,j), side=0,1,2.
    next_var = 3 * n
    possible = {}
    z = {}
    for p in bases:
        maximum = sum(
            max(columns[j][2].get(p, 0) for j in js)
            for js in by_base.values()
        )
        possible[p] = range(maximum + 1)
        for a in possible[p]:
            z[p, a] = next_var
            next_var += 1
    # Conjunctions for the two profiles being compared.
    w = {}
    for side in (0, 1):
        for j, (p, e, _) in enumerate(columns):
            for a in possible[p]:
                if a >= e:
                    w[side, j, a] = next_var
                    next_var += 1
    # XOR variables certifying that sides 0 and 1 are distinct.
    d = list(range(next_var, next_var + n))
    next_var += n

    rr, cc, data, lo, hi = [], [], [], [], []

    def add(terms, lower, upper):
        row = len(lo)
        for variable, coefficient in terms:
            if coefficient:
                rr.append(row)
                cc.append(variable)
                data.append(coefficient)
        lo.append(lower)
        hi.append(upper)

    # All three selected H-products have the same valuation vector.
    for q in rows:
        for side in (1, 2):
            terms = []
            for j, (_, _, factors) in enumerate(columns):
                a = factors.get(q, 0)
                if a:
                    terms.extend(((j, a), (side * n + j, -a)))
            add(terms, 0, 0)

    for p in bases:
        for side in (0, 1, 2):
            add(((side * n + j, 1) for j in by_base[p]), 0, 1)

    # Empty global exact-state core.
    for j in range(n):
        add(((j, 1), (n + j, 1), (2 * n + j, 1)), 0, 2)

    # Each representation is nonempty.
    for side in (0, 1, 2):
        add(((side * n + j, 1) for j in range(n)), 1, n)

    # d_j = xor(x_0j,x_1j), and at least one difference.
    for j in range(n):
        add(((j, 1), (n + j, -1), (d[j], -1)), -np.inf, 0)
        add(((j, -1), (n + j, 1), (d[j], -1)), -np.inf, 0)
        add(((d[j], 1), (j, -1), (n + j, -1)), -np.inf, 0)
        add(((d[j], 1), (j, 1), (n + j, 1)), -np.inf, 2)
    add(((d[j], 1) for j in range(n)), 1, n)

    # Exact target exponent, linked to side 0.
    for p in bases:
        add(((z[p, a], 1) for a in possible[p]), 1, 1)
        terms = [(z[p, a], a) for a in possible[p]]
        for j, (_, _, factors) in enumerate(columns):
            if factors.get(p, 0):
                terms.append((j, -factors[p]))
        add(terms, 0, 0)

    # w(side,j,a) is the exact conjunction of x(side,j) and z(p,a).
    for side in (0, 1):
        for j, (p, e, _) in enumerate(columns):
            allowed = [a for a in possible[p] if a >= e]
            terms = [(w[side, j, a], 1) for a in allowed]
            terms.append((side * n + j, -1))
            add(terms, 0, 0)
            for a in allowed:
                add(((w[side, j, a], 1), (z[p, a], -1)), -np.inf, 0)

    largest_e = max(e for _, e, _ in columns)
    largest_a = max(r.stop - 1 for r in possible.values())
    for e in range(1, largest_e + 1):
        for a in range(e, largest_a + 1):
            terms = []
            for j, (p, ej, _) in enumerate(columns):
                if ej == e and a in possible[p]:
                    terms.extend(((w[0, j, a], 1), (w[1, j, a], -1)))
            if terms:
                add(terms, 0, 0)

    matrix = coo_matrix((data, (rr, cc)), shape=(len(lo), next_var)).tocsc()
    lower = np.zeros(next_var)
    upper = np.ones(next_var)
    if args.seed:
        seed = tuple(args.seed)
        hits = [j for j, (p, e, _) in enumerate(columns) if (p, e) == seed]
        if not hits:
            raise ValueError(f"seed {seed} was peeled or absent")
        lower[hits[0]] = upper[hits[0]] = 1
    objective = np.zeros(next_var)
    objective[: 3 * n] = 1
    print(
        f"original={len(original)} core={n} bases={len(bases)} rows={len(rows)} "
        f"variables={next_var} constraints={len(lo)} largest_target={largest_a}",
        flush=True,
    )
    result = milp(
        objective,
        integrality=np.ones(next_var),
        bounds=Bounds(lower, upper),
        constraints=LinearConstraint(matrix, np.array(lo), np.array(hi)),
        options={"time_limit": args.time_limit, "presolve": True, "mip_rel_gap": 0.0},
    )
    print(f"status={result.status}; {result.message}", flush=True)
    if result.x is None:
        raise SystemExit(1)

    sides = [
        [
            (columns[j][0], columns[j][1])
            for j in range(n)
            if result.x[side * n + j] > 0.5
        ]
        for side in (0, 1, 2)
    ]
    cert01 = verify(sides[0], sides[1], 1)
    cert02 = verify(sides[0], sides[2], 1) if sides[0] != sides[2] else cert01
    target = cert01["common_h"]
    profiles = [profile(side, target) for side in sides]
    assert profiles[0] == profiles[1]
    assert sides[0] != sides[1]
    assert not (set(sides[0]) & set(sides[1]) & set(sides[2]))
    certificate = {
        "sides": sides,
        "common_h": target,
        "equal_profile": profiles[0],
        "third_profile": profiles[2],
        "global_common_exact_states": [],
        "search": {
            "upper": args.upper,
            "max_exponent": args.max_exponent,
            "original_columns": len(original),
            "core_columns": n,
            "status": int(result.status),
        },
    }
    print(json.dumps(certificate, indent=2))
    if args.output:
        args.output.write_text(json.dumps(certificate, indent=2) + "\n")


if __name__ == "__main__":
    main()
