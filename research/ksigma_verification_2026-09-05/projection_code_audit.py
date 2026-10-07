#!/usr/bin/env python3
"""Audit a possible coordinate-code route to f(n)<=max_p v_p(n).

For each stored complete fiber, choose input-prime coordinates T so that
k -> (v_p(k))_{p in T} is injective.  The code cost is
prod_{p in T} |{v_p(k): k in fiber}|.  We exhaust all coordinate subsets and
compare the minimum cost with the largest target exponent.
"""

import argparse
import itertools
import json
import math
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = json.loads(args.input.read_text())
    worst = None
    violations = []
    for fiber in data["fibers"]:
        factorizations = fiber["preimage_factorizations"]
        primes = sorted({int(p) for f in factorizations for p in f})
        vectors = [
            [int(f.get(str(p), 0)) for p in primes] for f in factorizations
        ]
        best = None
        for size in range(1, len(primes) + 1):
            for indices in itertools.combinations(range(len(primes)), size):
                if len({tuple(v[i] for i in indices) for v in vectors}) < len(vectors):
                    continue
                counts = [len({v[i] for v in vectors}) for i in indices]
                candidate = (
                    math.prod(counts),
                    size,
                    [primes[i] for i in indices],
                    counts,
                )
                if best is None or candidate < best:
                    best = candidate
            if best is not None and 2 ** (size + 1) >= best[0]:
                break
        maximum_alpha = max(int(a) for a in fiber["target_factorization"].values())
        row = {
            "target": fiber["target"],
            "fiber_size": len(vectors),
            "maximum_target_exponent": maximum_alpha,
            "minimum_code_cost": best[0],
            "coordinate_set": best[2],
            "coordinate_alphabet_sizes": best[3],
            "cost_over_maximum_target_exponent": best[0] / maximum_alpha,
        }
        if worst is None or row["cost_over_maximum_target_exponent"] > worst["cost_over_maximum_target_exponent"]:
            worst = row
        if best[0] > maximum_alpha:
            violations.append(row)
    result = {
        "input": str(args.input),
        "fiber_count": len(data["fibers"]),
        "scope": data["scope"],
        "violations": violations,
        "worst_case": worst,
        "finite_evidence_only": True,
    }
    print(json.dumps(result, indent=2))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
