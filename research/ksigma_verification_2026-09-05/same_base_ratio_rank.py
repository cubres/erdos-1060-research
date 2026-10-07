#!/usr/bin/env python3
"""Exact finite rank audit for same-radical exponent changes in k*sigma(k).

For H(p,e)=p**e*sigma(p**e), use H(p,1) as the baseline at each prime and
form the prime-valuation column

    R(p,e) = H(p,e) / H(p,1),             e >= 2.

A multiplicative relation among the R(p,e) is exactly a rational linear
relation among these valuation columns.  The leaf-peeling certificate emitted
here proves linear independence whenever every column is removed: at the time
a column is removed, its recorded pivot row is nonzero in that column and zero
in every other active column.

The calculation is exact (integer factorization and integer valuations only).
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path

from sympy import factorint, primerange


def add_factorization(dst: dict[int, int], value: int, sign: int) -> None:
    for q, a in factorint(value).items():
        dst[int(q)] = dst.get(int(q), 0) + sign * int(a)


def ratio_column(p: int, e: int) -> dict[int, int]:
    """Return v_q(H(p,e)/H(p,1)) as a sparse integer dictionary."""
    assert e >= 2
    col: dict[int, int] = {p: e - 1}
    # sigma(p^e) and sigma(p)=p+1.  Factoring the two integers separately is
    # intentional: cancellation is then performed exactly in the dictionary.
    sigma_e = (p ** (e + 1) - 1) // (p - 1)
    add_factorization(col, sigma_e, +1)
    add_factorization(col, p + 1, -1)
    return {q: a for q, a in col.items() if a}


def peel(columns: list[dict[int, int]]) -> tuple[list[tuple[int, int]], list[int]]:
    row_to_columns: dict[int, set[int]] = defaultdict(set)
    for j, col in enumerate(columns):
        for q in col:
            row_to_columns[q].add(j)

    active = [True] * len(columns)
    queue = deque(q for q, js in row_to_columns.items() if len(js) == 1)
    order: list[tuple[int, int]] = []
    while queue:
        q = queue.popleft()
        js = row_to_columns[q]
        if len(js) != 1:
            continue
        j = next(iter(js))
        if not active[j]:
            continue
        active[j] = False
        order.append((j, q))
        for r in columns[j]:
            incident = row_to_columns[r]
            incident.discard(j)
            if len(incident) == 1:
                queue.append(r)
    core = [j for j, is_active in enumerate(active) if is_active]
    return order, core


def verify_peeling_certificate(
    columns: list[dict[int, int]], order: list[tuple[int, int]], core: list[int]
) -> None:
    active = set(range(len(columns)))
    for j, q in order:
        assert j in active
        assert columns[j].get(q, 0) != 0
        assert all(columns[k].get(q, 0) == 0 for k in active if k != j)
        active.remove(j)
    assert active == set(core)


def column_rank_mod_prime(
    columns: list[dict[int, int]], indices: list[int], modulus: int
) -> int:
    """Sparse Gaussian elimination on columns over F_modulus.

    A full column rank result modulo a prime is also a rigorous full-rank
    certificate over Q, since the corresponding integer minor is nonzero.
    """
    basis: dict[int, dict[int, int]] = {}
    for j in indices:
        vec = {q: a % modulus for q, a in columns[j].items() if a % modulus}
        while vec:
            pivot = min(vec)
            if pivot not in basis:
                inv = pow(vec[pivot], -1, modulus)
                vec = {q: (a * inv) % modulus for q, a in vec.items()}
                basis[pivot] = {q: a for q, a in vec.items() if a}
                break
            factor = vec[pivot]
            old = basis[pivot]
            for q, a in old.items():
                value = (vec.get(q, 0) - factor * a) % modulus
                if value:
                    vec[q] = value
                else:
                    vec.pop(q, None)
    return len(basis)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime-bound", type=int, default=100_000)
    parser.add_argument("--max-exponent", type=int, default=2)
    parser.add_argument("--json", type=Path)
    parser.add_argument(
        "--modulus",
        type=int,
        default=1_000_003,
        help="prime modulus used to rank a nonempty residual core",
    )
    parser.add_argument(
        "--include-order",
        action="store_true",
        help="include the (potentially large) full peeling certificate in JSON",
    )
    args = parser.parse_args()
    if args.prime_bound < 2 or args.max_exponent < 2:
        parser.error("prime-bound and max-exponent must both be at least 2")

    labels: list[tuple[int, int]] = []
    columns: list[dict[int, int]] = []
    for p0 in primerange(2, args.prime_bound + 1):
        p = int(p0)
        for e in range(2, args.max_exponent + 1):
            labels.append((p, e))
            columns.append(ratio_column(p, e))

    order, core = peel(columns)
    verify_peeling_certificate(columns, order, core)
    core_rank_mod = column_rank_mod_prime(columns, core, args.modulus) if core else 0
    proved_full_rank = not core or core_rank_mod == len(core)
    all_rows = set().union(*(set(col) for col in columns)) if columns else set()
    result = {
        "prime_bound": args.prime_bound,
        "max_exponent": args.max_exponent,
        "prime_count": len(labels) // (args.max_exponent - 1),
        "column_count": len(columns),
        "valuation_row_count": len(all_rows),
        "peeled_column_count": len(order),
        "core_column_count": len(core),
        "empty_core": not core,
        "core_labels_sample": [labels[j] for j in core[:50]],
        "core_rank_modulus": args.modulus,
        "core_rank_mod_prime": core_rank_mod,
        "proved_full_column_rank_over_Q": proved_full_rank,
        "deduction": (
            "all valuation columns are linearly independent over Q"
            if proved_full_rank
            else "peeling plus this modular rank test does not prove full rank"
        ),
    }
    if args.include_order:
        result["peeling_order"] = [
            {"base": labels[j][0], "exponent": labels[j][1], "pivot_prime": q}
            for j, q in order
        ]
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.json:
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
