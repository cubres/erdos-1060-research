#!/usr/bin/env python3
"""Search for an exponent-{1,2} local-block relation with no directed 2-cycle.

The no-2-cycle property is encoded directly as pairwise MILP exclusions.  Any
candidate is then exact-checked and conformally decomposed independently.
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
from search import make_columns, relation_core, verify

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from relation_decompose import atoms, differing_columns


def solve_no_two_cycle(columns, seed, seconds):
    count = len(columns)
    bases = sorted({p for p, _, _ in columns})
    base_set = set(bases)
    rows = sorted({q for _, _, f in columns for q in f})
    ri = {q: i for i, q in enumerate(rows)}

    rr, cc, data = [], [], []
    for j, (_, _, factors) in enumerate(columns):
        for q, a in factors.items():
            i = ri[q]
            rr += [i, i]; cc += [j, count + j]; data += [a, -a]
    matrices = [coo_matrix((data, (rr, cc)), shape=(len(rows), 2 * count)).tocsc()]
    lower = [0.0] * len(rows); upper = [0.0] * len(rows)

    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)
    rr, cc, data = [], [], []
    row = 0
    for p in bases:
        for off in (0, count):
            for j in by_base[p]: rr.append(row); cc.append(off+j); data.append(1)
            lower.append(0); upper.append(1); row += 1
    for j in range(count):
        rr += [row,row]; cc += [j,count+j]; data += [1,1]
        lower.append(0); upper.append(1); row += 1

    # Record which local columns create each directed base-prime edge.
    directed = defaultdict(list)
    for j, (p, e, factors) in enumerate(columns):
        sigma_factors = dict(factors)
        sigma_factors[p] = sigma_factors.get(p, 0) - e
        for q, a in sigma_factors.items():
            if a and q in base_set and q != p:
                directed[p, q].append(j)
    for p in bases:
        for q in bases:
            if p >= q or (p,q) not in directed or (q,p) not in directed:
                continue
            # If a p->q block and q->p block are selected on either side, the
            # relation's directed graph would contain a reciprocal pair.
            for j in directed[p,q]:
                for k in directed[q,p]:
                    for sj in (0,count):
                        for sk in (0,count):
                            rr += [row,row]; cc += [sj+j,sk+k]; data += [1,1]
                            lower.append(0); upper.append(1); row += 1
    matrices.append(coo_matrix((data,(rr,cc)),shape=(row,2*count)).tocsc())
    lo = np.zeros(2*count); hi = np.ones(2*count)
    lo[seed]=hi[seed]=1
    result=milp(
        np.ones(2*count), integrality=np.ones(2*count), bounds=Bounds(lo,hi),
        constraints=LinearConstraint(vstack(matrices,format="csc"),np.array(lower),np.array(upper)),
        options={"time_limit":seconds,"presolve":True},
    )
    if result.x is None: return None,result.message
    left=[(columns[j][0],columns[j][1]) for j in range(count) if result.x[j]>.5]
    right=[(columns[j][0],columns[j][1]) for j in range(count) if result.x[count+j]>.5]
    return verify(left,right,1),result.message


def main():
    for upper in (100, 300, 700, 1500, 3000):
        columns, occurrences = make_columns(2, upper, 2)
        columns = relation_core(columns, occurrences)
        print(f"upper={upper} relation_core={len(columns)}", flush=True)
        # Prioritize columns with smaller bases, but test every surviving base
        # at least once before increasing the range.
        seen_bases=set(); seeds=[]
        for j,(p,e,_) in enumerate(columns):
            if p not in seen_bases:
                seen_bases.add(p); seeds.append(j)
        for pos,j in enumerate(seeds):
            candidate,message=solve_no_two_cycle(columns,j,3.0)
            if candidate is None: continue
            pieces=atoms(differing_columns(dict(candidate["left_blocks"]),dict(candidate["right_blocks"])))
            print("HIT",candidate)
            print("ATOMS",pieces)
            return
        print(f"no hit in {len(seeds)} seeded base tests", flush=True)
    print("NO_BOUNDED_HIT")


if __name__ == "__main__":
    main()
