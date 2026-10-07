#!/usr/bin/env python3
"""Search for exact collisions of h(k)=k*sigma(k) with rough inputs.

The search represents each local block H(p,e)=p^e sigma(p^e) by its
prime-valuation vector.  A collision is a signed zero-sum of these columns,
with at most one exponent chosen for each base prime on either side.

The MILP is only a discovery device.  Every reported result is reconstructed
and checked with Python integers and SymPy before it is written.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from math import gcd, prod
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix, vstack


def block_value(p: int, e: int) -> int:
    return p**e * ((p ** (e + 1) - 1) // (p - 1))


def make_columns(lower: int, upper: int, max_exponent: int):
    columns = []
    occurrences = defaultdict(set)
    for p in sp.primerange(lower, upper + 1):
        for e in range(1, max_exponent + 1):
            factors = {int(q): int(a) for q, a in sp.factorint(block_value(p, e)).items()}
            idx = len(columns)
            columns.append((int(p), e, factors))
            for q in factors:
                occurrences[q].add(idx)
    return columns, occurrences


def relation_core(columns, occurrences):
    """Peel any column containing a valuation row of current degree one."""
    active = set(range(len(columns)))
    degree = {q: len(indices) for q, indices in occurrences.items()}
    queue = deque(q for q, d in degree.items() if d <= 1)
    while queue:
        q = queue.popleft()
        if degree[q] != 1:
            continue
        candidates = occurrences[q] & active
        if len(candidates) != 1:
            degree[q] = len(candidates)
            continue
        idx = next(iter(candidates))
        active.remove(idx)
        for r in columns[idx][2]:
            degree[r] -= 1
            if degree[r] == 1:
                queue.append(r)
    return [columns[i] for i in sorted(active)]


def verify(left, right, forbidden_product: int):
    k = prod(p**e for p, e in left)
    m = prod(p**e for p, e in right)
    hk = prod(block_value(p, e) for p, e in left)
    hm = prod(block_value(p, e) for p, e in right)
    if k == m or hk != hm:
        raise AssertionError("candidate is not a nontrivial exact collision")
    if gcd(k * m, forbidden_product) != 1:
        raise AssertionError("candidate uses a forbidden input prime")
    return {
        "left_blocks": left,
        "right_blocks": right,
        "left_input": k,
        "right_input": m,
        "common_h": hk,
        "common_h_factorization": {
            str(q): int(a) for q, a in sp.factorint(hk).items()
        },
    }


def solve(columns, seed_index: int, time_limit: float):
    primes = sorted({p for p, _, _ in columns})
    rows = sorted({q for _, _, factors in columns for q in factors})
    row_index = {q: i for i, q in enumerate(rows)}
    count = len(columns)

    rr, cc, data = [], [], []
    for j, (_, _, factors) in enumerate(columns):
        for q, a in factors.items():
            i = row_index[q]
            rr.extend((i, i))
            cc.extend((j, count + j))
            data.extend((a, -a))
    from scipy.sparse import coo_matrix

    valuation = coo_matrix((data, (rr, cc)), shape=(len(rows), 2 * count)).tocsc()
    matrices = [valuation]
    lower = [0.0] * len(rows)
    upper = [0.0] * len(rows)

    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)
    constraint_rr, constraint_cc, constraint_data = [], [], []
    constraint_count = 0
    for p in primes:
        indices = by_base[p]
        for offset in (0, count):
            for j in indices:
                constraint_rr.append(constraint_count)
                constraint_cc.append(offset + j)
                constraint_data.append(1)
            lower.append(0.0)
            upper.append(1.0)
            constraint_count += 1
    for j in range(count):
        constraint_rr.extend((constraint_count, constraint_count))
        constraint_cc.extend((j, count + j))
        constraint_data.extend((1, 1))
        lower.append(0.0)
        upper.append(1.0)
        constraint_count += 1
    choice_constraints = coo_matrix(
        (constraint_data, (constraint_rr, constraint_cc)),
        shape=(constraint_count, 2 * count),
    ).tocsc()
    matrices.append(choice_constraints)

    matrix = vstack(matrices, format="csc")
    variable_lower = np.zeros(2 * count)
    variable_upper = np.ones(2 * count)
    variable_lower[seed_index] = 1.0
    variable_upper[seed_index] = 1.0
    result = milp(
        np.zeros(2 * count),
        integrality=np.ones(2 * count),
        bounds=Bounds(variable_lower, variable_upper),
        constraints=LinearConstraint(matrix, np.array(lower), np.array(upper)),
        options={"time_limit": time_limit, "presolve": True},
    )
    if result.x is None:
        return None, result.message
    left = [(columns[j][0], columns[j][1]) for j in range(count) if result.x[j] > 0.5]
    right = [
        (columns[j][0], columns[j][1])
        for j in range(count)
        if result.x[count + j] > 0.5
    ]
    return (left, right), result.message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lower", type=int, default=11)
    parser.add_argument("--upper", type=int, default=1500)
    parser.add_argument("--max-exponent", type=int, default=8)
    parser.add_argument("--time-per-seed", type=float, default=20.0)
    parser.add_argument("--seed-bases", type=int, default=8)
    parser.add_argument("--forbidden-product", type=int, default=210)
    parser.add_argument("--output", type=Path, default=Path("collision.json"))
    args = parser.parse_args()

    columns, occurrences = make_columns(args.lower, args.upper, args.max_exponent)
    original_count = len(columns)
    columns = relation_core(columns, occurrences)
    print(f"columns={original_count}; relation_core={len(columns)}")
    seed_primes = sorted({p for p, _, _ in columns})[: args.seed_bases]
    seed_indices = [j for j, (p, _, _) in enumerate(columns) if p in seed_primes]
    for position, seed in enumerate(seed_indices, 1):
        p, e, _ = columns[seed]
        print(f"seed {position}/{len(seed_indices)}: H({p},{e})")
        candidate, message = solve(columns, seed, args.time_per_seed)
        print(message)
        if candidate is None:
            continue
        certificate = verify(*candidate, args.forbidden_product)
        certificate["search_parameters"] = vars(args) | {
            "output": str(args.output),
            "original_columns": original_count,
            "relation_core_columns": len(columns),
            "fixed_left_seed": [p, e],
        }
        args.output.write_text(json.dumps(certificate, indent=2) + "\n")
        print(json.dumps(certificate, indent=2))
        return 0
    print("NO_HIT_IN_BOUNDED_SEED_RUN")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
