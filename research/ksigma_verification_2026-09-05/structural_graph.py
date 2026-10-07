#!/usr/bin/env python3
"""Exact incidence-graph diagnostics for h(k)=k*sigma(k) collisions.

This uses only Python integers and trial division.  It deliberately defines two
different graphs:

* a pair-relation graph, made only from blocks that differ between two inputs;
* the full candidate graph G(n), made from every H(p,e) that can divide n.

The latter is the graph relevant to the rigorous cycle-rank fiber bound.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Hashable, Iterable


def factor_trial(n: int) -> Counter[int]:
    assert n >= 1
    result: Counter[int] = Counter()
    d = 2
    while d * d <= n:
        while n % d == 0:
            result[d] += 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        result[n] += 1
    return result


def sigma_pp(p: int, e: int) -> int:
    return sum(p**j for j in range(e + 1))


def block_factors(p: int, e: int) -> Counter[int]:
    result = Counter({p: e})
    result.update(factor_trial(sigma_pp(p, e)))
    return result


def product_from_factors(f: Counter[int]) -> int:
    return math.prod(p**e for p, e in f.items())


def factors_from_blocks(blocks: Iterable[tuple[int, int]]) -> Counter[int]:
    result: Counter[int] = Counter()
    for p, e in blocks:
        result.update(block_factors(p, e))
    return result


def input_from_blocks(blocks: Iterable[tuple[int, int]]) -> int:
    return math.prod(p**e for p, e in blocks)


class DSU:
    def __init__(self) -> None:
        self.parent: dict[Hashable, Hashable] = {}

    def add(self, x: Hashable) -> None:
        self.parent.setdefault(x, x)

    def find(self, x: Hashable) -> Hashable:
        p = self.parent[x]
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent[x]

    def union(self, a: Hashable, b: Hashable) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


@dataclass
class Component:
    columns: list[tuple]
    rows: list[int]
    edge_count: int

    @property
    def cycle_rank(self) -> int:
        return self.edge_count - len(self.columns) - len(self.rows) + 1


def graph_components(
    column_factors: dict[tuple, Counter[int]], all_rows: Iterable[int] = ()
) -> list[Component]:
    dsu = DSU()
    edges: list[tuple[tuple, tuple[str, int]]] = []
    for col, factors in column_factors.items():
        cnode = ("c",) + col
        dsu.add(cnode)
        for q in factors:
            rnode = ("r", q)
            dsu.add(rnode)
            dsu.union(cnode, rnode)
            edges.append((cnode, rnode))
    for q in all_rows:
        dsu.add(("r", q))

    columns_by_root: dict[Hashable, list[tuple]] = defaultdict(list)
    rows_by_root: dict[Hashable, list[int]] = defaultdict(list)
    edge_count: Counter[Hashable] = Counter()
    for node in dsu.parent:
        root = dsu.find(node)
        if node[0] == "c":
            columns_by_root[root].append(node[1:])
        else:
            rows_by_root[root].append(node[1])
    for cnode, _ in edges:
        edge_count[dsu.find(cnode)] += 1

    result = []
    for root in {dsu.find(x) for x in dsu.parent}:
        result.append(
            Component(
                sorted(columns_by_root[root]),
                sorted(rows_by_root[root]),
                edge_count[root],
            )
        )
    return sorted(result, key=lambda c: (-len(c.columns), c.columns))


def pair_components(
    left: dict[int, int], right: dict[int, int]
) -> list[Component]:
    columns: dict[tuple, Counter[int]] = {}
    for p in sorted(set(left) | set(right)):
        le, re = left.get(p, 0), right.get(p, 0)
        if le == re:
            continue
        if le:
            columns[("L", p, le)] = block_factors(p, le)
        if re:
            columns[("R", p, re)] = block_factors(p, re)

    components = graph_components(columns)
    # Each connected component must itself be a signed exact relation.
    for component in components:
        balance: Counter[int] = Counter()
        left_blocks, right_blocks = [], []
        for side, p, e in component.columns:
            sign = 1 if side == "L" else -1
            balance.update({q: sign * a for q, a in block_factors(p, e).items()})
            (left_blocks if side == "L" else right_blocks).append((p, e))
        assert all(a == 0 for a in balance.values()), (component, balance)
        assert product_from_factors(factors_from_blocks(left_blocks)) == product_from_factors(
            factors_from_blocks(right_blocks)
        )
    return components


def divides_factors(a: Counter[int], b: Counter[int]) -> bool:
    return all(e <= b.get(p, 0) for p, e in a.items())


def candidate_graph(nf: Counter[int]) -> tuple[dict[tuple[int, int], Counter[int]], list[Component]]:
    columns: dict[tuple[int, int], Counter[int]] = {}
    for p, a in sorted(nf.items()):
        for e in range(1, a + 1):
            bf = block_factors(p, e)
            if divides_factors(bf, nf):
                columns[(p, e)] = bf
    return columns, graph_components(columns, nf)


def cycle_rank(components: Iterable[Component]) -> int:
    return sum(component.cycle_rank for component in components)


def summarize_pair(name: str, left: dict[int, int], right: dict[int, int]) -> None:
    lf = factors_from_blocks(left.items())
    rf = factors_from_blocks(right.items())
    assert lf == rf
    comps = pair_components(left, right)
    print(f"PAIR {name}")
    print(
        "  inputs=",
        input_from_blocks(left.items()),
        input_from_blocks(right.items()),
        "differing_components=",
        len(comps),
        "cycle_rank=",
        cycle_rank(comps),
    )
    for i, c in enumerate(comps, 1):
        print(
            f"  component {i}: blocks={len(c.columns)} rows={len(c.rows)} "
            f"edges={c.edge_count} mu={c.cycle_rank} columns={c.columns}"
        )


def summarize_fiber(name: str, n: int, fiber: list[int]) -> None:
    nf = factor_trial(n)
    cols, comps = candidate_graph(nf)
    mu = cycle_rank(comps)
    assert len(fiber) <= 2**mu
    print(f"FIBER {name}: n={n} f={len(fiber)}")
    print(
        f"  candidate_blocks={len(cols)} components={len(comps)} "
        f"cycle_rank={mu} 2^mu={2**mu}"
    )
    print(
        "  component data=",
        [(len(c.columns), len(c.rows), c.edge_count, c.cycle_rank) for c in comps],
    )


def main() -> None:
    named_pairs = [
        ("336", {2: 2, 3: 1}, {2: 1, 7: 1}),
        ("27776", {2: 4, 7: 1}, {2: 2, 31: 1}),
        ("196560", {3: 2, 5: 1, 7: 1}, {3: 3, 13: 1}),
        ("disjoint tensor", factor_trial(624960), factor_trial(713232)),
        (
            "coprime6",
            {13: 2, 17: 1, 31: 1, 37: 3, 61: 1, 67: 2, 73: 1, 97: 1, 137: 1},
            {5: 1, 7: 2, 23: 1, 31: 3, 37: 2, 61: 2, 67: 1, 137: 2},
        ),
        (
            "coprime30",
            {7: 2, 11: 2, 13: 1, 31: 2, 37: 1, 43: 1, 61: 1, 83: 1, 127: 1},
            {7: 5, 11: 3, 19: 2, 31: 3, 331: 1},
        ),
    ]
    rough_path = Path(
        "/Users/cubres/Documents/ChatGPT/Research/"
        "ksigma_rough_collision_search_2026-09-05/collision_11_700_e8.json"
    )
    rough = json.loads(rough_path.read_text())
    named_pairs.append(
        (
            "coprime210",
            dict(rough["left_blocks"]),
            dict(rough["right_blocks"]),
        )
    )
    for name, left, right in named_pairs:
        summarize_pair(name, left, right)

    fibers = [
        ("f2", 336, [12, 14]),
        ("f3", 333312, [336, 372, 434]),
        ("f4", 5418319872, [41664, 42672, 47244, 55118]),
        ("f5", 1584858562560, [624960, 640080, 696384, 708660, 713232]),
        (
            "f6",
            7089671638182002688000,
            [42330624000, 42658728000, 43690794000, 48371950500, 53261158400, 56433942250],
        ),
        (
            "f7",
            106345074572730040320,
            [5079674880, 5119047360, 5242895280, 5660209152, 5704081344, 5804634060, 5842083312],
        ),
    ]
    for args in fibers:
        summarize_fiber(*args)


if __name__ == "__main__":
    main()
