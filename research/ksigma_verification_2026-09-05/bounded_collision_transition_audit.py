#!/usr/bin/env python3
"""Exact state-dependent interaction-graph audit for h(k)=k*sigma(k).

The input JSON may contain ``left_blocks`` and ``right_blocks`` directly or
inside ``milp_relation``.  With ``--add-basic-atom`` the two sides are tensored
with both sides of h(12)=h(14), producing the four guaranteed preimages.  All
multiplicative identities and graph arcs are rebuilt with Python integers.

For the supplied sparse certificates all simple directed cycles are enumerated.
The minimum feedback vertex set and maximum vertex-disjoint cycle packing are
then solved by exact branch recursion.  Equality of their sizes is an easily
checkable optimality certificate for the reported cases.
"""

from __future__ import annotations

import argparse
import json
import math
from functools import lru_cache
from pathlib import Path

import networkx as nx
from sympy import isprime


BlockList = list[tuple[int, int]]


def H(p: int, e: int) -> int:
    return p**e * sum(p**j for j in range(e + 1))


def input_value(blocks: BlockList) -> int:
    return math.prod(p**e for p, e in blocks)


def h_value(blocks: BlockList) -> int:
    return math.prod(H(p, e) for p, e in blocks)


def normalize_blocks(raw) -> BlockList:
    answer = sorted((int(p), int(e)) for p, e in raw)
    assert len({p for p, _ in answer}) == len(answer)
    assert all(isprime(p) and e >= 1 for p, e in answer)
    return answer


def exponent(blocks: BlockList, p: int) -> int:
    return dict(blocks).get(p, 0)


def valuation(n: int, p: int) -> int:
    answer = 0
    while n % p == 0:
        n //= p
        answer += 1
    return answer


def interaction_graph(corners: list[BlockList]) -> nx.DiGraph:
    support = sorted({p for blocks in corners for p, _ in blocks})
    graph = nx.DiGraph()
    graph.add_nodes_from(support)
    for q in support:
        states = [exponent(blocks, q) for blocks in corners]
        for p in support:
            values = [
                valuation(sum(q**j for j in range(e + 1)), p) if e else 0
                for e in states
            ]
            if len(set(values)) > 1:
                graph.add_edge(q, p, states=states, valuations=values)
    return graph


def canonical_cycle(cycle: list[int]) -> tuple[int, ...]:
    rotations = [tuple(cycle[i:] + cycle[:i]) for i in range(len(cycle))]
    return min(rotations)


def minimum_cycle_transversal(cycles: list[tuple[int, ...]]) -> tuple[int, ...]:
    universe = sorted({p for cycle in cycles for p in cycle})
    bit = {p: 1 << i for i, p in enumerate(universe)}
    masks = tuple(sorted({sum(bit[p] for p in c) for c in cycles}, key=lambda x: (x.bit_count() if hasattr(x, "bit_count") else bin(x).count("1"), x)))

    @lru_cache(None)
    def solve(active_cycles: tuple[int, ...]) -> tuple[int, int]:
        if not active_cycles:
            return 0, 0
        pivot = active_cycles[0]
        best = (10**9, 0)
        choices = [i for i in range(len(universe)) if pivot >> i & 1]
        for i in choices:
            remaining = tuple(mask for mask in active_cycles if not (mask >> i & 1))
            size, chosen = solve(remaining)
            candidate = (size + 1, chosen | (1 << i))
            if candidate[0] < best[0]:
                best = candidate
        return best

    size, chosen = solve(masks)
    result = tuple(universe[i] for i in range(len(universe)) if chosen >> i & 1)
    assert len(result) == size
    return result


def maximum_disjoint_cycle_packing(cycles: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    ordered = sorted(cycles, key=lambda c: (len(c), c))

    @lru_cache(None)
    def solve(i: int, used: frozenset[int]) -> tuple[tuple[int, ...], ...]:
        if i == len(ordered):
            return ()
        best = solve(i + 1, used)
        cycle = ordered[i]
        if used.isdisjoint(cycle):
            candidate = (cycle,) + solve(i + 1, used | frozenset(cycle))
            if len(candidate) > len(best):
                best = candidate
        return best

    return [tuple(c) for c in solve(0, frozenset())]


def read_corners(path: Path, add_basic_atom: bool) -> tuple[list[BlockList], dict]:
    source = json.loads(path.read_text())
    relation = source.get("milp_relation", source)
    left = normalize_blocks(relation["left_blocks"])
    right = normalize_blocks(relation["right_blocks"])
    if not add_basic_atom:
        return [left, right], source
    basic_left = [(2, 2), (3, 1)]
    basic_right = [(2, 1), (7, 1)]
    rough_support = {p for p, _ in left + right}
    assert rough_support.isdisjoint({2, 3, 7})
    corners = [
        sorted(rough + basic)
        for rough in (left, right)
        for basic in (basic_left, basic_right)
    ]
    return corners, source


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--add-basic-atom", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    corners, source = read_corners(args.certificate, args.add_basic_atom)
    common_h = h_value(corners[0])
    assert all(h_value(blocks) == common_h for blocks in corners)
    assert len({input_value(blocks) for blocks in corners}) == len(corners)
    if not args.add_basic_atom:
        claimed = source.get("milp_relation", source).get("common_h")
        if claimed is not None:
            assert int(claimed) == common_h

    graph = interaction_graph(corners)
    cycles = sorted(
        {canonical_cycle(list(cycle)) for cycle in nx.simple_cycles(graph)},
        key=lambda c: (len(c), c),
    )
    fvs = minimum_cycle_transversal(cycles)
    reduced = graph.copy()
    reduced.remove_nodes_from(fvs)
    assert nx.is_directed_acyclic_graph(reduced)
    packing = maximum_disjoint_cycle_packing(cycles)
    assert len(packing) <= len(fvs)

    variable_bases = sorted(
        p
        for p in graph.nodes
        if len({exponent(blocks, p) for blocks in corners}) > 1
    )
    mass = sum(-math.log1p(-1.0 / p) for p in variable_bases)
    cyclic_sccs = sorted(
        (
            sorted(component)
            for component in nx.strongly_connected_components(graph)
            if len(component) > 1
            or any(graph.has_edge(p, p) for p in component)
        ),
        key=lambda c: (len(c), c),
    )
    edges = []
    for q, p, data in sorted(graph.edges(data=True)):
        edges.append(
            {
                "from": q,
                "to": p,
                "source_states": data["states"],
                "sigma_valuations": data["valuations"],
            }
        )
    result = {
        "source_certificate": str(args.certificate.resolve()),
        "construction": (
            "four-corner tensor with h(12)=h(14)"
            if args.add_basic_atom
            else "two supplied collision sides"
        ),
        "finite_exact_certificate": True,
        "maximum_input_exponent": max(e for blocks in corners for _, e in blocks),
        "preimage_blocks": corners,
        "preimages": [input_value(blocks) for blocks in corners],
        "common_h": common_h,
        "variable_bases": variable_bases,
        "roughness_minimum_variable_base": min(variable_bases),
        "euler_mass": mass,
        "euler_product": math.exp(mass),
        "all_radicals_equal": len({math.prod(p for p, _ in blocks) for blocks in corners}) == 1,
        "interaction_graph": {
            "vertex_count": graph.number_of_nodes(),
            "edge_count": graph.number_of_edges(),
            "edges": edges,
            "cyclic_strong_components": cyclic_sccs,
            "directed_cycle_count": len(cycles),
            "directed_cycles": cycles,
            "directed_girth": min(map(len, cycles)) if cycles else 0,
            "minimum_feedback_vertex_set_size": len(fvs),
            "minimum_feedback_vertex_set_witness": fvs,
            "maximum_vertex_disjoint_cycle_packing_size": len(packing),
            "maximum_vertex_disjoint_cycle_packing_witness": packing,
            "packing_equals_transversal": len(packing) == len(fvs),
        },
    }
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n")


if __name__ == "__main__":
    main()
