#!/usr/bin/env python3
"""MILP search for cubefree h-collisions with no short in-base cycle.

The finite candidate universe consists of H(p,e)=p^e sigma(p^e), with p at
most ``upper`` and e in {1,2}, after exact degree-one peeling.  A directed
edge p->q is present when a selected p-block has q | sigma(p^e) and q is
also a selected input base.  For each potential simple directed cycle of
length at most ``forbid_through``, we add every necessary column-choice
inequality.  Thus a feasible solution has directed girth larger than the
requested cutoff.  MILP is discovery only; exact verification is separate.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from math import gcd, prod
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


def canonical_cycle(vertices: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize a directed cycle up to cyclic rotation (not reversal)."""
    return min(vertices[i:] + vertices[:i] for i in range(len(vertices)))


def potential_cycles(bases, directed, length_bound):
    adjacency = defaultdict(set)
    for p, q in directed:
        adjacency[p].add(q)
    found = set()
    for start in bases:
        def visit(path):
            p = path[-1]
            for q in adjacency[p]:
                if q == start and len(path) >= 2:
                    found.add(canonical_cycle(tuple(path)))
                elif q not in path and len(path) < length_bound:
                    visit(path + [q])
        visit([start])
    return sorted((c for c in found if len(c) <= length_bound), key=lambda c: (len(c), c))


def selected_blocks(solution, columns):
    count = len(columns)
    left = [(columns[j][0], columns[j][1]) for j in range(count) if solution[j] > .5]
    right = [(columns[j][0], columns[j][1]) for j in range(count) if solution[count+j] > .5]
    return left, right


def graph_arrows(blocks):
    bases = {p for p, _ in blocks}
    arrows = set()
    for p, e in blocks:
        sigma = (p ** (e + 1) - 1) // (p - 1)
        q = 2
        while q * q <= sigma:
            if sigma % q == 0:
                if q in bases and q != p:
                    arrows.add((p, q))
                while sigma % q == 0:
                    sigma //= q
            q = 3 if q == 2 else q + 2
        if sigma > 1 and sigma in bases and sigma != p:
            arrows.add((p, sigma))
    return arrows


def exact_cycles(blocks, length_bound=None):
    bases = sorted({p for p, _ in blocks})
    arrows = graph_arrows(blocks)
    bound = len(bases) if length_bound is None else min(length_bound, len(bases))
    return potential_cycles(bases, {edge: [0] for edge in arrows}, bound)


def build_problem(columns, forbid_through):
    count = len(columns)
    bases = sorted({p for p, _, _ in columns})
    base_set = set(bases)
    rows = sorted({q for _, _, factors in columns for q in factors})
    row_index = {q: i for i, q in enumerate(rows)}

    # Exact valuation balance A x_L - A x_R = 0.
    rr, cc, data = [], [], []
    for j, (_, _, factors) in enumerate(columns):
        for q, a in factors.items():
            i = row_index[q]
            rr.extend((i, i)); cc.extend((j, count+j)); data.extend((a, -a))
    matrices = [coo_matrix((data, (rr, cc)), shape=(len(rows), 2*count)).tocsc()]
    lower = [0.0] * len(rows)
    upper = [0.0] * len(rows)

    # At most one exponent of a base on each side; never use the same block
    # on both sides (that common block would simply cancel).
    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)
    rr, cc, data = [], [], []
    row = 0
    for p in bases:
        for offset in (0, count):
            for j in by_base[p]:
                rr.append(row); cc.append(offset+j); data.append(1)
            lower.append(0.0); upper.append(1.0); row += 1
    for j in range(count):
        rr.extend((row, row)); cc.extend((j, count+j)); data.extend((1, 1))
        lower.append(0.0); upper.append(1.0); row += 1

    # Potential edge realizers.  There are at most two local columns per
    # source because this is the cubefree search.
    directed = defaultdict(list)
    for j, (p, e, factors) in enumerate(columns):
        for q in factors:
            if q != p and q in base_set:
                directed[p, q].append(j)
    cycles = potential_cycles(bases, directed, forbid_through)

    # A cycle is present iff, for each of its edges, one realizing column is
    # selected on either side.  Enumerate one column realizer per edge.  Since
    # cycle sources are distinct, these columns are distinct.  Writing
    # z_j=x_Lj+x_Rj gives sum z_j <= length-1.
    forbidden_column_sets = set()
    for cyc in cycles:
        edge_choices = [directed[cyc[i], cyc[(i+1) % len(cyc)]] for i in range(len(cyc))]
        for choice in itertools.product(*edge_choices):
            forbidden_column_sets.add(tuple(sorted(choice)))
    for choice in sorted(forbidden_column_sets, key=lambda x: (len(x), x)):
        for j in choice:
            rr.extend((row, row)); cc.extend((j, count+j)); data.extend((1, 1))
        lower.append(0.0); upper.append(float(len(choice)-1)); row += 1
    matrices.append(coo_matrix((data, (rr, cc)), shape=(row, 2*count)).tocsc())
    matrix = vstack(matrices, format="csc")
    return matrix, np.array(lower), np.array(upper), cycles, forbidden_column_sets


def solve(columns, built, seed, seconds):
    matrix, lower, upper, _, _ = built
    count = len(columns)
    lo = np.zeros(2*count); hi = np.ones(2*count)
    lo[seed] = hi[seed] = 1.0
    result = milp(
        np.ones(2*count),
        integrality=np.ones(2*count),
        bounds=Bounds(lo, hi),
        constraints=LinearConstraint(matrix, lower, upper),
        options={"time_limit": seconds, "presolve": True, "mip_rel_gap": 0.0},
    )
    if result.x is None:
        return None, result
    return selected_blocks(result.x, columns), result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upper", type=int, default=700)
    parser.add_argument("--forbid-through", type=int, default=5)
    parser.add_argument("--time-per-seed", type=float, default=10.0)
    parser.add_argument(
        "--start-seed",
        type=int,
        default=1,
        help="one-based position in the deterministic seed list at which to resume",
    )
    parser.add_argument("--all-column-seeds", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "cubefree_girth_gt5_collision.json")
    args = parser.parse_args()

    original, occurrences = make_columns(2, args.upper, 2)
    columns = relation_core(original, occurrences)
    built = build_problem(columns, args.forbid_through)
    cycles, forbidden_sets = built[3], built[4]
    by_length = Counter(map(len, cycles))
    print(
        f"upper={args.upper}; original_columns={len(original)}; core_columns={len(columns)}; "
        f"bases={len(set(p for p,e,f in columns))}; potential_short_cycles={dict(by_length)}; "
        f"cycle_column_constraints={len(forbidden_sets)}",
        flush=True,
    )

    if args.all_column_seeds:
        seeds = list(range(len(columns)))
    else:
        # One seed for every column lying on a potential cycle longer than the
        # forbidden cutoff, followed by one per remaining base.
        directed = defaultdict(list)
        base_set = {p for p, _, _ in columns}
        for j, (p, e, factors) in enumerate(columns):
            for q in factors:
                if q != p and q in base_set:
                    directed[p, q].append(j)
        long_cycles = potential_cycles(sorted(base_set), directed, min(len(base_set), args.forbid_through+3))
        preferred = []
        for cyc in long_cycles:
            if len(cyc) <= args.forbid_through:
                continue
            for i in range(len(cyc)):
                preferred.extend(directed[cyc[i], cyc[(i+1) % len(cyc)]])
        seen = set(); seeds = []
        for j in preferred + list(range(len(columns))):
            p = columns[j][0]
            key = j if j in preferred else ("base", p)
            if key not in seen:
                seen.add(key); seeds.append(j)

    statuses = Counter()
    for position, seed in enumerate(seeds, 1):
        if position < args.start_seed:
            continue
        p, e, _ = columns[seed]
        candidate, result = solve(columns, built, seed, args.time_per_seed)
        statuses[result.status] += 1
        if position % 20 == 0 or candidate is not None:
            print(f"seed {position}/{len(seeds)} H({p},{e}): {result.message}", flush=True)
        if candidate is None:
            continue
        left, right = candidate
        # HiGHS can return an incumbent at the time limit whose rounded binary
        # coordinates violate the exact valuation equalities.  Discovery is
        # floating point, so reject such incumbents and let the integer
        # certificate remain the authority.
        try:
            verify(left, right, 1)
        except AssertionError:
            statuses["exact_reject"] += 1
            print(f"seed {position}/{len(seeds)} H({p},{e}): exact verifier rejected rounded incumbent", flush=True)
            continue
        signed = differing_columns(dict(left), dict(right))
        pieces = atoms(signed)
        # The minimum objective normally returns one atom.  If numerical MILP
        # stopped early, independently keep only atomic components which still
        # meet the girth condition.
        for piece in pieces:
            atom_left = [(q, a) for side, q, a in piece if side == "L"]
            atom_right = [(q, a) for side, q, a in piece if side == "R"]
            atom_blocks = atom_left + atom_right
            short = exact_cycles(atom_blocks, args.forbid_through)
            if short:
                continue
            exact = verify(atom_left, atom_right, 1)
            all_cycles = exact_cycles(atom_blocks)
            exact.update({
                "directed_girth": min(map(len, all_cycles)) if all_cycles else None,
                "directed_cycles": [list(c) for c in all_cycles],
                "conformally_indecomposable": True,
                "search_parameters": {
                    "upper": args.upper,
                    "max_exponent": 2,
                    "forbid_through": args.forbid_through,
                    "original_columns": len(original),
                    "relation_core_columns": len(columns),
                    "seed": [p, e],
                    "milp_status": int(result.status),
                    "milp_message": result.message,
                },
            })
            args.output.write_text(json.dumps(exact, indent=2) + "\n")
            print("EXACT_HIT")
            print(json.dumps(exact, indent=2))
            return 0
    print(f"NO_HIT; statuses={dict(statuses)}; seeds={len(seeds)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
