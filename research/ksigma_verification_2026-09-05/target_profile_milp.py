#!/usr/bin/env python3
"""Exact finite MILP search for equal-target-profile h-collisions.

For a common target n and an input k, the positive target profile is the
multiset of (v_p(n),v_p(k)) over p|k.  In a fixed fiber it determines the
full profile over p|n, since the missing pairs have second coordinate zero.

The target exponent v_p(n) is itself a linear function of selected local
blocks.  Binary one-hot variables select its value, and conjunction variables
record a selected H(p,e) block together with that value.  Consequently profile
equality is enforced exactly by linear equations, not checked heuristically
after an unconstrained collision search.  A returned MILP candidate is always
reconstructed with arbitrary-precision integers.
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


HERE = Path(__file__).parent


def positive_profile(blocks, target):
    answer = []
    for p, e in blocks:
        remaining = target
        a = 0
        while remaining % p == 0:
            remaining //= p
            a += 1
        answer.append((a, e))
    return sorted(answer)


def make_model(columns, seed, profile_mode="exact"):
    count = len(columns)
    bases = sorted({p for p, _, _ in columns})
    valuation_primes = sorted({q for _, _, factors in columns for q in factors})
    by_base = defaultdict(list)
    for j, (p, _, _) in enumerate(columns):
        by_base[p].append(j)

    # Binary variable layout. x chooses local blocks on the two sides.
    next_variable = 2 * count
    z = {}
    possible_target_exponents = {}
    for p in bases:
        # Under the at-most-one-exponent-per-input-base restriction, this is
        # an exact superset of all attainable values of the p-row.  Keeping a
        # contiguous range makes the one-hot link transparent and rigorous.
        maximum = 0
        for source_base, indices in by_base.items():
            maximum += max(columns[j][2].get(p, 0) for j in indices)
        possible_target_exponents[p] = range(maximum + 1)
        for a in possible_target_exponents[p]:
            z[p, a] = next_variable
            next_variable += 1

    # w(side,j,a)=1 iff column j is selected on that side and the target
    # exponent at its input base is a.  Values a<e are impossible because the
    # local block itself contributes p^e.
    w = {}
    for side in (0, 1):
        for j, (p, e, _) in enumerate(columns):
            for a in possible_target_exponents[p]:
                if a >= e:
                    w[side, j, a] = next_variable
                    next_variable += 1

    row_indices = []
    column_indices = []
    coefficients = []
    lower = []
    upper = []

    def add_constraint(terms, lo, hi):
        row = len(lower)
        for variable, coefficient in terms:
            if coefficient:
                row_indices.append(row)
                column_indices.append(variable)
                coefficients.append(coefficient)
        lower.append(lo)
        upper.append(hi)

    # Equality of every prime valuation in the two H-products.
    for q in valuation_primes:
        terms = []
        for j, (_, _, factors) in enumerate(columns):
            coefficient = factors.get(q, 0)
            if coefficient:
                terms.extend(((j, coefficient), (count + j, -coefficient)))
        add_constraint(terms, 0, 0)

    # One common one-hot target exponent for every potential input base,
    # linked to the left product's valuation row. Product equality makes it
    # automatically equal to the right row as well.
    for p in bases:
        add_constraint(((z[p, a], 1) for a in possible_target_exponents[p]), 1, 1)
        terms = [(z[p, a], a) for a in possible_target_exponents[p]]
        for j, (_, _, factors) in enumerate(columns):
            if factors.get(p, 0):
                terms.append((j, -factors[p]))
        add_constraint(terms, 0, 0)

    # Each input prime has at most one exponent on a side.
    for p in bases:
        for side in (0, 1):
            offset = side * count
            add_constraint(((offset + j, 1) for j in by_base[p]), 0, 1)

    # Identical local blocks cannot simply be placed on both sides.
    for j in range(count):
        add_constraint(((j, 1), (count + j, 1)), 0, 1)

    # Exclude the empty equality. Positivity then forces both sides nonempty.
    add_constraint(((j, 1) for j in range(2 * count)), 1, 2 * count)

    # Exact conjunction link: sum_a w(side,j,a)=x(side,j), and w<=z.
    for side in (0, 1):
        offset = side * count
        for j, (p, e, _) in enumerate(columns):
            allowed = [a for a in possible_target_exponents[p] if a >= e]
            terms = [(w[side, j, a], 1) for a in allowed]
            terms.append((offset + j, -1))
            add_constraint(terms, 0, 0)
            for a in allowed:
                add_constraint(((w[side, j, a], 1), (z[p, a], -1)), -np.inf, 0)

    # Equal histograms.  The default is the full pair (target exponent a,
    # input exponent e).  ``saturation`` retains only e and whether a=e;
    # this is useful for falsifying a much stronger prospective invariant.
    largest_input_exponent = max(e for _, e, _ in columns)
    largest_target_exponent = max(r.stop - 1 for r in possible_target_exponents.values())
    if profile_mode == "exact":
        for e in range(1, largest_input_exponent + 1):
            for a in range(e, largest_target_exponent + 1):
                terms = []
                for j, (p, column_e, _) in enumerate(columns):
                    if column_e != e or a not in possible_target_exponents[p]:
                        continue
                    key_left = (0, j, a)
                    key_right = (1, j, a)
                    if key_left in w:
                        terms.extend(((w[key_left], 1), (w[key_right], -1)))
                if terms:
                    add_constraint(terms, 0, 0)
    elif profile_mode == "saturation":
        for e in range(1, largest_input_exponent + 1):
            # Equality of the total number of input states of exponent e.
            terms = []
            for j, (_, column_e, _) in enumerate(columns):
                if column_e == e:
                    terms.extend(((j, 1), (count + j, -1)))
            if terms:
                add_constraint(terms, 0, 0)
            # Equality of the number for which the target exponent is exactly e.
            terms = []
            for j, (p, column_e, _) in enumerate(columns):
                if column_e != e or e not in possible_target_exponents[p]:
                    continue
                terms.extend(((w[0, j, e], 1), (w[1, j, e], -1)))
            if terms:
                add_constraint(terms, 0, 0)
    else:
        raise ValueError(f"unknown profile mode: {profile_mode}")

    matrix = coo_matrix(
        (coefficients, (row_indices, column_indices)),
        shape=(len(lower), next_variable),
    ).tocsc()
    variable_lower = np.zeros(next_variable)
    variable_upper = np.ones(next_variable)
    if seed is not None:
        matches = [j for j, (p, e, _) in enumerate(columns) if (p, e) == seed]
        if not matches:
            raise ValueError(f"seed {seed} is absent from the relation core")
        variable_lower[matches[0]] = variable_upper[matches[0]] = 1

    # Minimize relation size; z/w variables have zero objective coefficient.
    objective = np.zeros(next_variable)
    objective[:2 * count] = 1
    return (
        objective,
        np.ones(next_variable),
        Bounds(variable_lower, variable_upper),
        LinearConstraint(matrix, np.array(lower), np.array(upper)),
        {
            "variables": next_variable,
            "constraints": len(lower),
            "one_hot_variables": len(z),
            "conjunction_variables": len(w),
            "largest_target_exponent_bound": largest_target_exponent,
            "profile_mode": profile_mode,
        },
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upper", type=int, default=100)
    parser.add_argument("--max-exponent", type=int, default=5)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--seed", nargs=2, type=int, metavar=("P", "E"))
    parser.add_argument("--profile-mode", choices=("exact", "saturation"), default="exact")
    parser.add_argument("--output", type=Path, default=HERE / "equal_target_profile.json")
    args = parser.parse_args()

    original, occurrences = make_columns(2, args.upper, args.max_exponent)
    columns = relation_core(original, occurrences)
    seed = tuple(args.seed) if args.seed else None
    objective, integrality, bounds, constraints, statistics = make_model(
        columns, seed, args.profile_mode
    )
    print(
        f"upper={args.upper}; max_exponent={args.max_exponent}; "
        f"original_columns={len(original)}; core_columns={len(columns)}; "
        + "; ".join(f"{key}={value}" for key, value in statistics.items()),
        flush=True,
    )
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=constraints,
        options={"time_limit": args.time_limit, "presolve": True, "mip_rel_gap": 0.0},
    )
    print(f"status={result.status}; {result.message}", flush=True)
    if result.x is None:
        return 1

    count = len(columns)
    left = [(columns[j][0], columns[j][1]) for j in range(count) if result.x[j] > 0.5]
    right = [
        (columns[j][0], columns[j][1])
        for j in range(count)
        if result.x[count + j] > 0.5
    ]
    certificate = verify(left, right, 1)
    left_profile = positive_profile(left, certificate["common_h"])
    right_profile = positive_profile(right, certificate["common_h"])
    if args.profile_mode == "exact":
        if left_profile != right_profile:
            raise AssertionError("MILP candidate fails exact target-profile equality")
    else:
        def saturation(profile):
            return sorted((e, a == e) for a, e in profile)
        if saturation(left_profile) != saturation(right_profile):
            raise AssertionError("MILP candidate fails saturation-profile equality")
    certificate.update({
        "left_positive_target_profile": left_profile,
        "right_positive_target_profile": right_profile,
        "left_sigma": certificate["common_h"] // certificate["left_input"],
        "right_sigma": certificate["common_h"] // certificate["right_input"],
        "search_parameters": {
            "upper": args.upper,
            "max_exponent": args.max_exponent,
            "seed": seed,
            "original_columns": len(original),
            "relation_core_columns": len(columns),
            **statistics,
            "milp_status": int(result.status),
            "milp_message": result.message,
        },
    })
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(f"{args.profile_mode.upper()}_TARGET_PROFILE_HIT")
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
