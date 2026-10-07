#!/usr/bin/env python3
"""Search for a normalized equal-target-profile extension of a known relation.

This is a finite MILP discovery tool.  It fixes the two oriented sides of an
exact h-relation, permits additional local blocks in a bounded prime/exponent
universe, forbids an identical block on both sides, and enforces equality of
the positive target profiles.  Any hit is reconstructed and checked with
arbitrary-precision integers by target_profile_milp.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, milp

HERE = Path(__file__).parent
SEARCH_DIR = HERE.parent / "ksigma_rough_collision_search_2026-09-05"
sys.path.insert(0, str(SEARCH_DIR))
sys.path.insert(0, str(HERE))

from search import make_columns, relation_core, verify
from target_profile_milp import make_model, positive_profile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--upper", type=int, default=7000)
    parser.add_argument("--max-exponent", type=int, default=2)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--profile-mode", choices=("exact", "saturation"), default="exact")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    seed = json.loads(args.certificate.read_text())
    fixed_left = [tuple(map(int, block)) for block in seed["left_blocks"]]
    fixed_right = [tuple(map(int, block)) for block in seed["right_blocks"]]

    original, occurrences = make_columns(2, args.upper, args.max_exponent)
    columns = relation_core(original, occurrences)
    objective, integrality, old_bounds, constraints, statistics = make_model(
        columns, None, args.profile_mode
    )
    count = len(columns)
    index = {(p, e): j for j, (p, e, _) in enumerate(columns)}
    missing = [block for block in fixed_left + fixed_right if block not in index]
    if missing:
        raise ValueError(f"fixed blocks absent from relation core: {missing}")

    lower = np.array(old_bounds.lb, copy=True)
    upper = np.array(old_bounds.ub, copy=True)
    for block in fixed_left:
        j = index[block]
        lower[j] = upper[j] = 1
    for block in fixed_right:
        j = index[block]
        lower[count + j] = upper[count + j] = 1

    print(
        f"upper={args.upper}; max_exponent={args.max_exponent}; "
        f"original_columns={len(original)}; core_columns={count}; "
        f"fixed_left={len(fixed_left)}; fixed_right={len(fixed_right)}; "
        + "; ".join(f"{key}={value}" for key, value in statistics.items()),
        flush=True,
    )
    result = milp(
        objective,
        integrality=integrality,
        bounds=Bounds(lower, upper),
        constraints=constraints,
        options={"time_limit": args.time_limit, "presolve": True, "mip_rel_gap": 0.0},
    )
    print(f"status={result.status}; {result.message}", flush=True)
    if result.x is None:
        return 1

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
            raise AssertionError("candidate fails exact target-profile equality")
    else:
        def saturation(profile):
            return sorted((e, a == e) for a, e in profile)
        if saturation(left_profile) != saturation(right_profile):
            raise AssertionError("candidate fails saturation-profile equality")
    if set(left) & set(right):
        raise AssertionError("candidate contains an identical local block")
    certificate.update(
        {
            "left_positive_target_profile": left_profile,
            "right_positive_target_profile": right_profile,
            "fixed_seed_certificate": str(args.certificate),
            "search_parameters": {
                "upper": args.upper,
                "max_exponent": args.max_exponent,
                "original_columns": len(original),
                "relation_core_columns": count,
                **statistics,
                "milp_status": int(result.status),
                "milp_message": result.message,
            },
        }
    )
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print("EXACT_NORMALIZED_TARGET_PROFILE_HIT")
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
