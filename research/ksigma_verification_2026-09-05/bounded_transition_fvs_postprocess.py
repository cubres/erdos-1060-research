#!/usr/bin/env python3
"""Compute exact directed-FVS metrics for bounded-transition census JSON.

The input rows already contain every complete fiber of size at least three in
the stated finite range.  We rebuild the state-dependent interaction digraph
from each row's exponent vectors.  The graphs here have at most eight vertices,
so exhaustive simple-cycle enumeration and exact branch recursion are tiny.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import networkx as nx

from bounded_collision_transition_audit import (
    canonical_cycle,
    interaction_graph,
    maximum_disjoint_cycle_packing,
    minimum_cycle_transversal,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--omit-fibers", action="store_true")
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    histogram: Counter[int] = Counter()
    packing_histogram: Counter[int] = Counter()
    packing_equals_fvs_count = 0
    maximum = None
    maximum_scale = None
    strict_fvs_over_separator = None
    analyzed = []
    for row in source["fibers"]:
        corners = [
            sorted((int(p), int(e)) for p, e in factors.items())
            for factors in row["preimage_factorizations"]
        ]
        graph = interaction_graph(corners)
        cycles = sorted(
            {canonical_cycle(list(c)) for c in nx.simple_cycles(graph)},
            key=lambda c: (len(c), c),
        )
        fvs = minimum_cycle_transversal(cycles)
        packing = maximum_disjoint_cycle_packing(cycles)
        reduced = graph.copy()
        reduced.remove_nodes_from(fvs)
        assert nx.is_directed_acyclic_graph(reduced)
        assert len(packing) <= len(fvs)
        if len(packing) == len(fvs):
            packing_equals_fvs_count += 1
        # A directed FVS separates the fiber by the recovery lemma, so it must
        # be at least the exact coordinate-separator number already computed.
        assert row["transversal_number"] <= len(fvs)
        histogram[len(fvs)] += 1
        packing_histogram[len(packing)] += 1
        record = {
            "target": row["target"],
            "fiber_size": row["fiber_size"],
            "preimages": row["preimages"],
            "preimage_factorizations": row["preimage_factorizations"],
            "interaction_vertex_count": graph.number_of_nodes(),
            "interaction_edge_count": graph.number_of_edges(),
            "interaction_edges": sorted([list(e) for e in graph.edges()]),
            "directed_cycles": cycles,
            "directed_girth": min(map(len, cycles)),
            "minimum_directed_fvs_size": len(fvs),
            "minimum_directed_fvs_witness": fvs,
            "maximum_vertex_disjoint_cycle_packing_size": len(packing),
            "maximum_vertex_disjoint_cycle_packing_witness": packing,
            "coordinate_separator_number": row["transversal_number"],
            "coordinate_separator_witness": row["transversal_witness"],
        }
        analyzed.append(record)
        if maximum is None or len(fvs) > maximum[0]:
            maximum = (len(fvs), record)
        scale = len(fvs) * math.log(math.log(row["target"])) / math.log(row["target"])
        if maximum_scale is None or scale > maximum_scale[0]:
            maximum_scale = (scale, record)
        if strict_fvs_over_separator is None and len(fvs) > row["transversal_number"]:
            strict_fvs_over_separator = record

    output = {
        "source": str(args.input.resolve()),
        "scope": source["scope"],
        "finite_evidence_only": True,
        "fiber_count": len(analyzed),
        "directed_fvs_histogram": dict(sorted(histogram.items())),
        "cycle_packing_histogram": dict(sorted(packing_histogram.items())),
        "packing_equals_fvs_count": packing_equals_fvs_count,
        "maximum_directed_fvs": maximum[1] if maximum else None,
        "maximum_fvs_times_loglog_over_log": {
            "value": maximum_scale[0],
            "fiber": maximum_scale[1],
        } if maximum_scale else None,
        "first_strict_fvs_over_coordinate_separator": strict_fvs_over_separator,
    }
    if not args.omit_fibers:
        output["fibers"] = analyzed
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: output[k] for k in output if k != "fibers"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
