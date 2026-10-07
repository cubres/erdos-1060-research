#!/usr/bin/env python3
"""Analyze exact finite bounded-exponent fibers as finite coordinate codes.

Input is the text produced by bounded_fiber_census.cpp.  That census is
complete for targets n<=K^2.  This script uses arbitrary-precision arithmetic
and exact factorizations.  Its "atom hypergraph" is deliberately conservative:
the edges are the inclusion-minimal supports of actual pairwise transitions in
the fiber.  A transversal of these edges is exactly a set of prime coordinates
whose exponent vectors separate all displayed preimages.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import re
from collections import Counter
from pathlib import Path

from sympy import factorint, divisor_sigma


FIBER = re.compile(r"fiber n=(\d+) f=(\d+) k=(\[.*\])$")
SUMMARY = re.compile(r"summary K=(\d+) exact_n_max=(\d+) R=(\d+)")


def factor_input(k: int) -> dict[int, int]:
    return {int(p): int(e) for p, e in factorint(k).items()}


def exact_h(k: int) -> int:
    return k * int(divisor_sigma(k))


def minimal_edges(edges: set[frozenset[int]]) -> list[frozenset[int]]:
    return sorted(
        (edge for edge in edges if not any(other < edge for other in edges)),
        key=lambda edge: (len(edge), sorted(edge)),
    )


def minimum_transversal(edges: list[frozenset[int]]) -> tuple[int, list[int]]:
    if not edges:
        return 0, []
    best: list[int] | None = None

    def visit(remaining: list[frozenset[int]], chosen: list[int]) -> None:
        nonlocal best
        if best is not None and len(chosen) >= len(best):
            return
        if not remaining:
            best = chosen[:]
            return
        edge = min(remaining, key=len)
        # High incidence first substantially reduces the exact search tree.
        incidence = Counter(p for e in remaining for p in e)
        for p in sorted(edge, key=lambda q: (-incidence[q], q)):
            visit([e for e in remaining if p not in e], chosen + [p])

    visit(edges, [])
    assert best is not None
    return len(best), sorted(best)


def positive_target_profile(factors: dict[int, int], nfac: dict[int, int]):
    return sorted((nfac[p], e) for p, e in factors.items())


def pair_metrics(a: dict[int, int], b: dict[int, int]):
    different = frozenset(p for p in set(a) | set(b) if a.get(p, 0) != b.get(p, 0))
    upward_edges: set[tuple[int, int]] = set()
    for p in different:
        for e in {a.get(p, 0), b.get(p, 0)} - {0}:
            sigma_factors = factorint(int(divisor_sigma(p**e)))
            for q in different:
                if q > p and q in sigma_factors:
                    upward_edges.add((p, q))
    upward_sources = frozenset(p for p, _ in upward_edges)
    dyadic_crossings = set()
    for p, q in upward_edges:
        lo, hi = p.bit_length() - 1, q.bit_length() - 1
        dyadic_crossings.update(range(lo + 1, hi + 1))
    return {
        "different": different,
        "upward_edges": upward_edges,
        "upward_sources": upward_sources,
        "dyadic_crossings": dyadic_crossings,
    }


def analyze(n: int, ks: list[int], R: int) -> dict:
    factors = [factor_input(k) for k in ks]
    assert len(set(ks)) == len(ks)
    assert all(exact_h(k) == n for k in ks)
    assert all(max(f.values(), default=0) < R for f in factors)
    nfac = {int(p): int(e) for p, e in factorint(n).items()}

    pair_data = []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            metrics = pair_metrics(factors[i], factors[j])
            pair_data.append((i, j, metrics))
    edges = {m["different"] for _, _, m in pair_data}
    atoms = minimal_edges(edges)
    tau, witness = minimum_transversal(atoms)
    common = set.intersection(*(set(e) for e in atoms)) if atoms else set()

    # An "upward-active" coordinate is the tail of an upward dependency edge
    # p->q lying wholly inside that actual transition support.
    atom_upward = []
    atom_crossings = []
    for edge in atoms:
        matching = [m for _, _, m in pair_data if m["different"] == edge]
        sources = set().union(*(m["upward_sources"] for m in matching))
        crossings = set().union(*(m["dyadic_crossings"] for m in matching))
        atom_upward.append(sources)
        atom_crossings.append(crossings)
    common_upward = set.intersection(*atom_upward) if atom_upward else set()
    common_crossings = set.intersection(*atom_crossings) if atom_crossings else set()

    profiles = [positive_target_profile(f, nfac) for f in factors]
    radicals = [math.prod(f) for f in factors]
    exponent_signatures = [sorted(f.values()) for f in factors]
    return {
        "target": n,
        "target_factorization": nfac,
        "preimages": ks,
        "preimage_factorizations": factors,
        "R": R,
        "fiber_size": len(ks),
        "coordinate_count": len(set().union(*(set(f) for f in factors))),
        "minimal_transition_supports": [sorted(e) for e in atoms],
        "minimal_transition_support_sizes": [len(e) for e in atoms],
        "transversal_number": tau,
        "transversal_witness": witness,
        "common_active_coordinate": sorted(common),
        "upward_active_sets": [sorted(s) for s in atom_upward],
        "common_upward_active_coordinate": sorted(common_upward),
        "dyadic_crossing_sets": [sorted(s) for s in atom_crossings],
        "common_dyadic_crossing": sorted(common_crossings),
        "log_f_over_tau_log_R": math.log(len(ks)) / (tau * math.log(R)) if tau else 0.0,
        "tau_over_log_n_over_loglog_n": tau / (math.log(n) / math.log(math.log(n))),
        "equal_positive_target_profile_pairs": sum(
            profiles[i] == profiles[j]
            for i in range(len(ks)) for j in range(i + 1, len(ks))
        ),
        "equal_radical_pairs": sum(
            radicals[i] == radicals[j]
            for i in range(len(ks)) for j in range(i + 1, len(ks))
        ),
        "equal_exponent_signature_pairs": sum(
            exponent_signatures[i] == exponent_signatures[j]
            for i in range(len(ks)) for j in range(i + 1, len(ks))
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    lines = args.input.read_text().splitlines()
    summary = next((SUMMARY.match(line) for line in lines if SUMMARY.match(line)), None)
    if summary is None:
        raise ValueError("missing census summary")
    K, exact_n_max, R = map(int, summary.groups())
    fibers = []
    for line in lines:
        match = FIBER.match(line)
        if match:
            n, f, raw = match.groups()
            ks = list(map(int, ast.literal_eval(raw)))
            assert len(ks) == int(f)
            fibers.append(analyze(int(n), ks, R))

    extrema = {}
    for key in (
        "fiber_size",
        "transversal_number",
        "log_f_over_tau_log_R",
        "tau_over_log_n_over_loglog_n",
        "coordinate_count",
    ):
        if fibers:
            item = max(fibers, key=lambda row: row[key])
            extrema[key] = {"value": item[key], "target": item["target"]}
    counterexamples = {
        "no_common_active_coordinate": next(
            (row["target"] for row in fibers if not row["common_active_coordinate"]), None
        ),
        "no_common_upward_active_coordinate": next(
            (row["target"] for row in fibers if not row["common_upward_active_coordinate"]), None
        ),
        "no_common_dyadic_crossing": next(
            (row["target"] for row in fibers if not row["common_dyadic_crossing"]), None
        ),
        "transversal_at_least_2": next(
            (row["target"] for row in fibers if row["transversal_number"] >= 2), None
        ),
        "equal_positive_target_profile": next(
            (row["target"] for row in fibers if row["equal_positive_target_profile_pairs"]), None
        ),
        "equal_radical": next((row["target"] for row in fibers if row["equal_radical_pairs"]), None),
        "equal_exponent_signature": next(
            (row["target"] for row in fibers if row["equal_exponent_signature_pairs"]), None
        ),
    }
    output = {
        "scope": {
            "input_bound_exclusive": K,
            "complete_target_bound_inclusive": exact_n_max,
            "bounded_exponent_parameter_R": R,
            "analyzed_fibers": "all complete R-free fibers of size at least 3 in the census",
            "finite_evidence_only": True,
        },
        "fiber_count_analyzed": len(fibers),
        "extrema": extrema,
        "first_counterexamples_or_null": counterexamples,
        "fibers": fibers,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: output[k] for k in ("scope", "fiber_count_analyzed", "extrema", "first_counterexamples_or_null")}, indent=2))


if __name__ == "__main__":
    main()
