#!/usr/bin/env python3
"""Independent exact audit of ``avoid_2_3_31_u20000.json``.

Only the Python standard library is used.  Besides rebuilding the collision,
the script certifies the stated one-vertex feedback set: it exhibits a
directed cycle, removes vertex 61, and checks an explicit topological order of
the remaining state-dependent transition graph.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "avoid_2_3_31_u20000.json"


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def factor(n: int) -> dict[int, int]:
    answer: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            answer[d] = answer.get(d, 0) + 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        answer[n] = answer.get(n, 0) + 1
    return answer


def sigma_prime_power(p: int, e: int) -> int:
    return sum(p**j for j in range(e + 1))


def H(p: int, e: int) -> int:
    return p**e * sigma_prime_power(p, e)


def product(values) -> int:
    answer = 1
    for value in values:
        answer *= value
    return answer


def topological_sort(
    vertices: set[int], edges: set[tuple[int, int]]
) -> list[int] | None:
    """Return a topological order, or None when the induced digraph is cyclic."""
    successors = {q: [] for q in vertices}
    indegree = {q: 0 for q in vertices}
    for q, p in edges:
        if q in vertices and p in vertices:
            successors[q].append(p)
            indegree[p] += 1
    stack = [q for q in vertices if indegree[q] == 0]
    order: list[int] = []
    while stack:
        q = stack.pop()
        order.append(q)
        for p in successors[q]:
            indegree[p] -= 1
            if indegree[p] == 0:
                stack.append(p)
    return order if len(order) == len(vertices) else None


def strongly_connected_components(
    vertices: set[int], edges: set[tuple[int, int]]
) -> list[set[int]]:
    """Kosaraju's algorithm, included to keep the audit standard-library only."""
    forward = {q: [] for q in vertices}
    reverse = {q: [] for q in vertices}
    for q, p in edges:
        forward[q].append(p)
        reverse[p].append(q)

    seen: set[int] = set()
    finish: list[int] = []

    def visit(q: int) -> None:
        seen.add(q)
        for p in forward[q]:
            if p not in seen:
                visit(p)
        finish.append(q)

    for q in vertices:
        if q not in seen:
            visit(q)

    seen.clear()
    components: list[set[int]] = []

    def collect(q: int, component: set[int]) -> None:
        seen.add(q)
        component.add(q)
        for p in reverse[q]:
            if p not in seen:
                collect(p, component)

    for q in reversed(finish):
        if q not in seen:
            component: set[int] = set()
            collect(q, component)
            components.append(component)
    return components


def main() -> None:
    source = json.loads(DATA.read_text())
    assert source["forbidden_bases"] == [2, 3, 31]
    assert len(source["atoms"]) == 1
    atom = source["atoms"][0]
    left = {int(p): int(e) for p, e in atom["left_blocks"]}
    right = {int(p): int(e) for p, e in atom["right_blocks"]}
    support = sorted(set(left) | set(right))

    assert len(support) == 24
    assert all(is_prime(p) for p in support)
    assert set(support).isdisjoint({2, 3, 31})
    assert max([*left.values(), *right.values()]) == 2
    assert not (set(left.items()) & set(right.items()))

    left_input = product(p**e for p, e in left.items())
    right_input = product(p**e for p, e in right.items())
    left_h = product(H(p, e) for p, e in left.items())
    right_h = product(H(p, e) for p, e in right.items())
    assert left_input == int(atom["left_input"])
    assert right_input == int(atom["right_input"])
    assert left_h == right_h == int(atom["common_h"])

    claimed_factorization = {
        int(p): int(e) for p, e in atom["common_h_factorization"].items()
    }
    assert product(p**e for p, e in claimed_factorization.items()) == left_h
    assert all(is_prime(p) for p in claimed_factorization)

    edges: set[tuple[int, int]] = set()
    for q in support:
        a, b = left.get(q, 0), right.get(q, 0)
        left_sigma = factor(sigma_prime_power(q, a)) if a else {}
        right_sigma = factor(sigma_prime_power(q, b)) if b else {}
        for p in support:
            if left_sigma.get(p, 0) != right_sigma.get(p, 0):
                edges.add((q, p))

    assert len(edges) == 34
    cyclic_components = [
        component
        for component in strongly_connected_components(set(support), edges)
        if len(component) > 1
    ]
    assert cyclic_components == [
        {13, 61, 97, 197, 317, 379, 787, 2053, 3169, 14401}
    ]

    # A cycle proves that the minimum FVS is nonempty.
    assert (13, 61) in edges and (61, 13) in edges

    # This explicit order proves that deleting 61 makes the graph acyclic.
    topological_order = [
        97, 3169, 317, 53, 14401, 379, 787, 197, 19, 2053, 127,
        13, 79, 5419, 5, 271, 17, 307, 43, 733, 11, 367, 23,
    ]
    assert set(topological_order) == set(support) - {61}
    position = {p: i for i, p in enumerate(topological_order)}
    assert all(
        position[q] < position[p]
        for q, p in edges
        if q != 61 and p != 61
    )
    assert topological_sort(set(support) - {61}, edges) is not None

    # Checking every one-vertex deletion proves that {61} is the unique
    # minimum feedback set, rather than merely one feedback-set witness.
    one_vertex_feedback_sets = [
        q
        for q in support
        if topological_sort(set(support) - {q}, edges) is not None
    ]
    assert one_vertex_feedback_sets == [61]

    nonchain = {
        q
        for q in support
        if (left.get(q, 0) + 1) % (right.get(q, 0) + 1)
        and (right.get(q, 0) + 1) % (left.get(q, 0) + 1)
    }
    assert nonchain == {17, 19, 97, 127, 197, 307, 317, 379}
    assert 13 not in nonchain and 61 not in nonchain

    print("PASS: exact cubefree collision avoiding bases 2, 3, and 31")
    print(f"left input = {left_input}")
    print(f"right input = {right_input}")
    print(f"common h = {left_h}")
    print("PASS: transition graph has 24 vertices, 34 arcs, and unique FVS {61}")
    print("PASS: deleting all non-chain coordinates leaves the cycle 13 <-> 61")


if __name__ == "__main__":
    main()
