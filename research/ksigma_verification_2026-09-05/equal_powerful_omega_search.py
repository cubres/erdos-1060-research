#!/usr/bin/env python3
"""Search exact h(k)=h(m) collisions with equal Omega of the powerful part.

For k=prod p^e, the powerful/full part is F(k)=prod_{e>=2} p^e, so
Omega(F(k))=sum_{e>=2} e.  This quantity is a linear row in the local-block
MILP.  ``partition`` equates the number of occurrences of each exponent,
``repeated_partition`` does so only for exponents at least two, and
``radical`` instead requires identical input-prime supports.
MILP is used only to discover candidates; all displayed identities are then
reconstructed exactly.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from math import prod
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


def omega_powerful(blocks):
    return sum(e for _, e in blocks if e >= 2)


def build_problem(columns, mode):
    count = len(columns)
    bases = sorted({p for p, _, _ in columns})
    rows = sorted({q for _, _, factors in columns for q in factors})
    row_index = {q: i for i, q in enumerate(rows)}

    rr, cc, data = [], [], []
    for j, (_, _, factors) in enumerate(columns):
        for q, a in factors.items():
            i = row_index[q]
            rr.extend((i, i)); cc.extend((j, count+j)); data.extend((a, -a))
    matrices = [coo_matrix((data, (rr, cc)), shape=(len(rows), 2*count)).tocsc()]
    lower = [0.0] * len(rows)
    upper = [0.0] * len(rows)

    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)
    rr, cc, data = [], [], []
    row = 0
    for p in bases:
        # At most one exponent for p on each side.
        for offset in (0, count):
            for j in by_base[p]:
                rr.append(row); cc.append(offset+j); data.append(1)
            lower.append(0.0); upper.append(1.0); row += 1
        if mode == "radical":
            # p occurs on the left iff it occurs on the right.
            for j in by_base[p]:
                rr.extend((row, row)); cc.extend((j, count+j)); data.extend((1, -1))
            lower.append(0.0); upper.append(0.0); row += 1

    # Do not use an identical H(p,e) on both sides; it would be a cancellable
    # common local block and could create a trivial seeded solution.
    for j in range(count):
        rr.extend((row, row)); cc.extend((j, count+j)); data.extend((1, 1))
        lower.append(0.0); upper.append(1.0); row += 1

    if mode == "omega":
        for j, (_, e, _) in enumerate(columns):
            weight = e if e >= 2 else 0
            if weight:
                rr.extend((row, row)); cc.extend((j, count+j)); data.extend((weight, -weight))
        lower.append(0.0); upper.append(0.0); row += 1
    elif mode in ("partition", "repeated_partition"):
        first = 1 if mode == "partition" else 2
        largest = max(e for _, e, _ in columns)
        for exponent in range(first, largest+1):
            for j, (_, e, _) in enumerate(columns):
                if e == exponent:
                    rr.extend((row, row)); cc.extend((j, count+j)); data.extend((1, -1))
            lower.append(0.0); upper.append(0.0); row += 1

    # Exclude the empty relation.  Positivity of all local valuation columns
    # then forces at least one selected block on each side.
    for j in range(2*count):
        rr.append(row); cc.append(j); data.append(1)
    lower.append(1.0); upper.append(float(2*count)); row += 1

    matrices.append(coo_matrix((data, (rr, cc)), shape=(row, 2*count)).tocsc())
    return vstack(matrices, format="csc"), np.array(lower), np.array(upper)


def solve(columns, built, seed, seconds):
    count = len(columns)
    matrix, lower, upper = built
    lo = np.zeros(2*count); hi = np.ones(2*count)
    if seed is not None:
        lo[seed] = hi[seed] = 1.0
    result = milp(
        np.ones(2*count), integrality=np.ones(2*count), bounds=Bounds(lo, hi),
        constraints=LinearConstraint(matrix, lower, upper),
        options={"time_limit": seconds, "presolve": True, "mip_rel_gap": 0.0},
    )
    if result.x is None:
        return None, result
    left = [(columns[j][0], columns[j][1]) for j in range(count) if result.x[j] > .5]
    right = [(columns[j][0], columns[j][1]) for j in range(count) if result.x[count+j] > .5]
    return (left, right), result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upper", type=int, default=700)
    parser.add_argument("--max-exponent", type=int, default=8)
    parser.add_argument("--mode", choices=("omega", "radical", "partition", "repeated_partition"), default="omega")
    parser.add_argument("--time-per-seed", type=float, default=30.0)
    parser.add_argument("--all-column-seeds", action="store_true")
    parser.add_argument("--single-solve", action="store_true")
    parser.add_argument("--forbid", default="", help="comma-separated forbidden input base primes")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is None:
        args.output = HERE / f"equal_{args.mode}_collision.json"

    original, occurrences = make_columns(2, args.upper, args.max_exponent)
    forbidden = {int(x) for x in args.forbid.split(",") if x}
    if forbidden:
        filtered = [column for column in original if column[0] not in forbidden]
        occurrences = defaultdict(set)
        for j, (_, _, factors) in enumerate(filtered):
            for q in factors:
                occurrences[q].add(j)
    else:
        filtered = original
    columns = relation_core(filtered, occurrences)
    built = build_problem(columns, args.mode)
    print(
        f"mode={args.mode}; upper={args.upper}; max_exponent={args.max_exponent}; "
        f"original_columns={len(original)}; core_columns={len(columns)}; "
        f"bases={len(set(p for p,e,f in columns))}; forbidden={sorted(forbidden)}", flush=True,
    )
    if args.single_solve:
        seeds = [None]
    elif args.all_column_seeds:
        seeds = list(range(len(columns)))
    else:
        # One seed of every exponent represented in the core, then one per
        # remaining base.  This is a discovery heuristic, not an exhaustive
        # negative search unless --all-column-seeds is supplied.
        seen_exp = set(); seen_base = set(); seeds = []
        for j, (p, e, _) in enumerate(columns):
            if e not in seen_exp:
                seen_exp.add(e); seeds.append(j)
        for j, (p, e, _) in enumerate(columns):
            if p not in seen_base:
                seen_base.add(p); seeds.append(j)
        seeds = list(dict.fromkeys(seeds))

    statuses = Counter()
    for position, seed in enumerate(seeds, 1):
        p, e = (None, None) if seed is None else columns[seed][:2]
        candidate, result = solve(columns, built, seed, args.time_per_seed)
        statuses[result.status] += 1
        if position % 10 == 0 or candidate is not None:
            print(f"solve {position}/{len(seeds)} seed={None if seed is None else (p,e)}: {result.message}", flush=True)
        if candidate is None:
            continue
        left, right = candidate
        certificate = verify(left, right, 1)
        # Exact checks for the extra invariant.
        if args.mode == "omega":
            left_invariant = omega_powerful(left)
            right_invariant = omega_powerful(right)
        elif args.mode == "radical":
            left_invariant = sorted(p for p, _ in left)
            right_invariant = sorted(p for p, _ in right)
        else:
            cutoff = 1 if args.mode == "partition" else 2
            left_invariant = sorted(e for _, e in left if e >= cutoff)
            right_invariant = sorted(e for _, e in right if e >= cutoff)
        assert left_invariant == right_invariant
        certificate.update({
            "constraint": args.mode,
            "left_invariant": left_invariant,
            "right_invariant": right_invariant,
            "left_sigma": certificate["common_h"] // certificate["left_input"],
            "right_sigma": certificate["common_h"] // certificate["right_input"],
            "search_parameters": {
                "upper": args.upper,
                "max_exponent": args.max_exponent,
                "original_columns": len(original),
                "filtered_columns": len(filtered),
                "relation_core_columns": len(columns),
                "forbidden_bases": sorted(forbidden),
                "seed": None if seed is None else [p, e],
                "milp_status": int(result.status),
                "milp_message": result.message,
            },
        })
        args.output.write_text(json.dumps(certificate, indent=2) + "\n")
        print("EXACT_HIT")
        print(json.dumps(certificate, indent=2))
        return 0
    print(f"NO_HIT; statuses={dict(statuses)}; seeds={len(seeds)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
