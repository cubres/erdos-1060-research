#!/usr/bin/env python3
"""Standard-library audit of the four-corner cubefree tensor certificate.

The lower bound tau >= 3 is certified by three vertex-disjoint directed
cycles.  The matching upper bound is certified by acyclicity after deleting
{2, 11, 13}.  The script also verifies the two-coordinate separator and the
threshold-2 shattered square on {2, 11}.
"""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "cubefree_fvs3_tensor_audit.json"


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


def sigma_prime_power(p: int, e: int) -> int:
    return sum(p**j for j in range(e + 1))


def H(p: int, e: int) -> int:
    return p**e * sigma_prime_power(p, e)


def product(values) -> int:
    answer = 1
    for value in values:
        answer *= value
    return answer


def valuation(n: int, p: int) -> int:
    answer = 0
    while n % p == 0:
        answer += 1
        n //= p
    return answer


def topological_sort(
    vertices: set[int], edges: set[tuple[int, int]]
) -> list[int] | None:
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


def cycle_edges(cycle: list[int]) -> set[tuple[int, int]]:
    return {
        (cycle[i], cycle[(i + 1) % len(cycle)])
        for i in range(len(cycle))
    }


def main() -> None:
    source = json.loads(DATA.read_text())
    blocks = [
        {int(p): int(e) for p, e in corner}
        for corner in source["preimage_blocks"]
    ]
    support = set().union(*(set(corner) for corner in blocks))
    assert len(blocks) == 4
    assert len(support) == 20
    assert all(is_prime(p) for p in support)
    assert all(max(corner.values()) <= 2 for corner in blocks)

    inputs = [product(p**e for p, e in corner.items()) for corner in blocks]
    values = [product(H(p, e) for p, e in corner.items()) for corner in blocks]
    assert inputs == [int(k) for k in source["preimages"]]
    assert len(set(inputs)) == 4
    assert len(set(values)) == 1
    assert values[0] == int(source["common_h"])

    edges: set[tuple[int, int]] = set()
    for q in support:
        states = [corner.get(q, 0) for corner in blocks]
        for p in support:
            sigma_valuations = [
                valuation(sigma_prime_power(q, e), p) if e else 0
                for e in states
            ]
            if len(set(sigma_valuations)) > 1:
                edges.add((q, p))
    assert len(edges) == 52

    cycles = [
        [2, 7],
        [13, 61],
        [11, 19, 127, 5419, 271, 17, 307, 43],
    ]
    assert all(cycle_edges(cycle) <= edges for cycle in cycles)
    assert sum(map(len, cycles)) == len(set().union(*(set(c) for c in cycles)))
    # The disjoint cycles force every FVS to contain at least three vertices.
    assert topological_sort(support - {2, 11, 13}, edges) is not None

    state_pairs = [(corner.get(2, 0), corner.get(11, 0)) for corner in blocks]
    assert len(set(state_pairs)) == 4
    threshold_traces = {
        frozenset(p for p in (2, 11) if corner.get(p, 0) >= 2)
        for corner in blocks
    }
    assert threshold_traces == {
        frozenset(), frozenset({2}), frozenset({11}), frozenset({2, 11})
    }
    # A single cubefree coordinate has only the three states 0, 1, 2, so it
    # cannot distinguish four inputs.  Thus the separator number is exactly 2.

    print("PASS: four exact distinct cubefree preimages have the stored common h")
    print("PASS: transition graph has 20 vertices, 52 arcs, and tau = nu = 3")
    print("PASS: separator number is 2 and threshold-2 VC dimension is at least 2")


if __name__ == "__main__":
    main()
