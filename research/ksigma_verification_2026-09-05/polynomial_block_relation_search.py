#!/usr/bin/env python3
"""Search for exact polynomial identities among H(P,e)=P^e sigma(P^e).

Every base P is an irreducible primitive integer polynomial with positive
leading coefficient.  A signed 0/1 relation found here becomes an actual
bounded-exponent h-collision at every specialization for which all selected
base polynomials are distinct positive primes.  The MILP is only a discovery
device; the emitted identity is reconstructed and verified in Z[x].
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


X = sp.symbols("x")


def primitive_key(poly: sp.Expr) -> tuple:
    value = sp.Poly(poly, X).primitive()[1]
    if value.LC() < 0:
        value = -value
    return ("P",) + tuple(int(c) for c in value.all_coeffs())


def add_integer_factors(vector: dict[tuple, int], value: int) -> None:
    for prime, exponent in sp.factorint(abs(int(value))).items():
        key = ("C", int(prime))
        vector[key] = vector.get(key, 0) + int(exponent)


def factor_vector(base: sp.Expr, exponent: int) -> dict[tuple, int]:
    vector = {primitive_key(base): exponent}
    sigma = sum(base**j for j in range(exponent + 1))
    coefficient, factors = sp.factor_list(sigma)
    add_integer_factors(vector, coefficient)
    for factor, multiplicity in factors:
        key = primitive_key(factor)
        vector[key] = vector.get(key, 0) + int(multiplicity)
    return vector


def candidate_bases() -> list[sp.Expr]:
    answer: list[sp.Expr] = []
    specifications = [
        (1, range(-6, 7)),
        (2, range(-6, 7)),
        (3, range(-3, 4)),
    ]
    for degree, coefficient_range in specifications:
        for leading in range(1, 8):
            for coefficients in itertools.product(coefficient_range, repeat=degree):
                poly = sp.Poly(
                    leading * X**degree
                    + sum(coefficients[j] * X**j for j in range(degree)),
                    X,
                )
                if poly.content() != 1 or not poly.is_irreducible:
                    continue
                # A fixed prime divisor rules out simultaneous prime values
                # except possibly finitely many specializations.
                values = [abs(int(poly.eval(j))) for j in range(degree + 1)]
                if sp.gcd(values) != 1:
                    continue
                answer.append(poly.as_expr())
    return list(dict.fromkeys(answer))


def relation_core(columns: list[dict[tuple, int]]) -> list[int]:
    occurrences: dict[tuple, set[int]] = defaultdict(set)
    for j, column in enumerate(columns):
        for row in column:
            occurrences[row].add(j)
    active = set(range(len(columns)))
    queue = deque(row for row, indices in occurrences.items() if len(indices) <= 1)
    while queue:
        row = queue.popleft()
        incident = occurrences[row] & active
        if len(incident) != 1:
            continue
        j = next(iter(incident))
        active.remove(j)
        for other_row in columns[j]:
            if len(occurrences[other_row] & active) == 1:
                queue.append(other_row)
    return sorted(active)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exponent", type=int, default=3)
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    bases = candidate_bases()
    labels: list[tuple[sp.Expr, int]] = []
    columns: list[dict[tuple, int]] = []
    for base in bases:
        for exponent in range(1, args.max_exponent + 1):
            labels.append((base, exponent))
            columns.append(factor_vector(base, exponent))
    core = relation_core(columns)
    labels = [labels[j] for j in core]
    columns = [columns[j] for j in core]
    count = len(columns)
    rows = sorted({row for column in columns for row in column}, key=str)
    row_index = {row: i for i, row in enumerate(rows)}

    rr: list[int] = []
    cc: list[int] = []
    data: list[int] = []
    lower: list[float] = []
    upper: list[float] = []

    def add(terms, lo: float, hi: float) -> None:
        index = len(lower)
        for variable, coefficient in terms:
            if coefficient:
                rr.append(index)
                cc.append(variable)
                data.append(coefficient)
        lower.append(lo)
        upper.append(hi)

    for row in rows:
        terms = []
        for j, column in enumerate(columns):
            coefficient = column.get(row, 0)
            if coefficient:
                terms.extend(((j, coefficient), (count + j, -coefficient)))
        add(terms, 0, 0)

    by_base: dict[sp.Expr, list[int]] = defaultdict(list)
    for j, (base, _) in enumerate(labels):
        by_base[base].append(j)
    for indices in by_base.values():
        add(((j, 1) for j in indices), 0, 1)
        add(((count + j, 1) for j in indices), 0, 1)
    for j in range(count):
        add(((j, 1), (count + j, 1)), 0, 1)
    add(((j, 1) for j in range(2 * count)), 1, 2 * count)

    matrix = coo_matrix(
        (data, (rr, cc)), shape=(len(lower), 2 * count)
    ).tocsc()
    objective = np.ones(2 * count)
    result = milp(
        objective,
        integrality=np.ones(2 * count),
        bounds=Bounds(np.zeros(2 * count), np.ones(2 * count)),
        constraints=LinearConstraint(matrix, np.array(lower), np.array(upper)),
        options={"time_limit": args.seconds, "presolve": True, "mip_rel_gap": 0.0},
    )
    print(
        f"bases={len(bases)} core_columns={count} rows={len(rows)} "
        f"status={result.status} {result.message}",
        flush=True,
    )
    if result.x is None:
        raise SystemExit(1)
    left = [labels[j] for j in range(count) if result.x[j] > 0.5]
    right = [labels[j] for j in range(count) if result.x[count + j] > 0.5]

    def product(blocks: list[tuple[sp.Expr, int]]) -> sp.Expr:
        value = 1
        for base, exponent in blocks:
            value *= base**exponent * sum(base**j for j in range(exponent + 1))
        return sp.expand(value)

    assert left and right and left != right
    assert sp.expand(product(left) - product(right)) == 0
    selected = list(dict.fromkeys(base for base, _ in left + right))
    certificate = {
        "left_blocks": [[str(base), exponent] for base, exponent in left],
        "right_blocks": [[str(base), exponent] for base, exponent in right],
        "selected_base_count": len(selected),
        "identity_degree": int(sp.degree(product(left), X)),
        "verified_polynomial_identity": True,
    }
    print(json.dumps(certificate, indent=2), flush=True)
    if args.output:
        args.output.write_text(json.dumps(certificate, indent=2) + "\n")


if __name__ == "__main__":
    main()
