#!/usr/bin/env python3
"""MILP search for collisions violating simple largest-differing-base patterns.

Every candidate is exact-checked.  This is a falsification search, not a proof
when no candidate is found.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, vstack

SEARCH_DIR = Path(
    "/Users/cubres/Documents/ChatGPT/Research/ksigma_rough_collision_search_2026-09-05"
)
sys.path.insert(0, str(SEARCH_DIR))
from search import make_columns, verify


def constrained_solve(columns, fixed_left=(), fixed_right=(), forbid_left=(), forbid_right=(), limit=3):
    rows = sorted({q for _, _, factors in columns for q in factors})
    ri = {q: i for i, q in enumerate(rows)}
    count = len(columns)
    by_key = {(p, e): j for j, (p, e, _) in enumerate(columns)}
    rr, cc, vv = [], [], []
    for j, (_, _, factors) in enumerate(columns):
        for q, a in factors.items():
            i = ri[q]
            rr += [i, i]
            cc += [j, count + j]
            vv += [a, -a]
    valuation = coo_matrix((vv, (rr, cc)), shape=(len(rows), 2 * count)).tocsc()
    mats = [valuation]
    lo = [0.0] * len(rows)
    hi = [0.0] * len(rows)
    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)
    rr, cc, vv = [], [], []
    row = 0
    for indices in by_base.values():
        for off in (0, count):
            for j in indices:
                rr.append(row); cc.append(off + j); vv.append(1)
            lo.append(0); hi.append(1); row += 1
    for j in range(count):
        rr += [row, row]; cc += [j, count + j]; vv += [1, 1]
        lo.append(0); hi.append(1); row += 1
    mats.append(coo_matrix((vv, (rr, cc)), shape=(row, 2 * count)).tocsc())
    lower = np.zeros(2 * count); upper = np.ones(2 * count)
    for key in fixed_left:
        j = by_key[key]; lower[j] = upper[j] = 1
    for key in fixed_right:
        j = by_key[key]; lower[count + j] = upper[count + j] = 1
    for key in forbid_left:
        upper[by_key[key]] = 0
    for key in forbid_right:
        upper[count + by_key[key]] = 0
    result = milp(
        np.ones(2 * count),
        integrality=np.ones(2 * count),
        bounds=Bounds(lower, upper),
        constraints=LinearConstraint(vstack(mats, format="csc"), np.array(lo), np.array(hi)),
        options={"time_limit": limit, "presolve": True},
    )
    if result.x is None:
        return None
    left = [(columns[j][0], columns[j][1]) for j in range(count) if result.x[j] > .5]
    right = [(columns[j][0], columns[j][1]) for j in range(count) if result.x[count+j] > .5]
    return verify(left, right, 1)


def main():
    primes = [11, 13, 17, 19, 23, 31, 37, 43, 61, 79, 97, 127, 181]
    for P in primes:
        columns, _ = make_columns(2, P, 8)
        pkeys = [(P, e) for e in range(1, 9)]
        # Force the largest base to occur on both sides at different exponents.
        for a, b in ((2, 1), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3)):
            hit = constrained_solve(columns, [(P, a)], [(P, b)], limit=2)
            if hit:
                print("BOTH_POSITIVE_HIT", P, a, b, hit)
                return
        # Force a jump of at least two against exponent zero.
        for a in (2, 3, 4, 5):
            hit = constrained_solve(columns, [(P, a)], forbid_right=pkeys, limit=2)
            if hit:
                print("JUMP_HIT", P, a, 0, hit)
                return
        print("NO_HIT_THROUGH", P, flush=True)
    print("NO_BOUNDED_HIT")


if __name__ == "__main__":
    main()
