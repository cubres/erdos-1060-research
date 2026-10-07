#!/usr/bin/env python3
"""Exact prefix census and entropy metrics for the Mersenne hub family.

The exponent list is the 52-entry list used in report-source.md.  This script
does not re-prove primality of the very large Mersenne numbers.  For prefixes
through 12, it does exhaustively test every divisor of the constructed target,
using only Python integers, and verifies that the displayed t inputs are the
complete h-fiber.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


EXPONENTS = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279,
    2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
    23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
    24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
    43112609, 57885161, 74207281, 77232917, 82589933, 136279841,
]


HERE = Path(__file__).parent


def entropy_metrics(exponents):
    total = sum(exponents)
    correction = sum(
        math.log2(1.0 - 2.0**(-p)) for p in exponents if p < 1074
    )
    log2_target = 2 * total - 1 + correction
    log_target = log2_target * math.log(2)
    loglog_target = math.log(log_target)
    log_multiplicity = math.log(len(exponents))
    return {
        "multiplicity": len(exponents),
        "sum_of_exponents": total,
        "log2_target": log2_target,
        "target_bit_length": math.floor(log2_target) + 1,
        "natural_log_target": log_target,
        "natural_log_log_target": loglog_target,
        "natural_log_multiplicity": log_multiplicity,
        "log_multiplicity_over_logN_div_loglogN": (
            log_multiplicity / (log_target / loglog_target)
        ),
    }


def exact_prefix_census(exponents):
    mersennes = [2**p - 1 for p in exponents]
    total = sum(exponents)
    target = 2**(total - 1) * math.prod(mersennes)
    # Every divisor is 2^a times a squarefree product of these Mersenne primes.
    # Carry the satellite product and sum of its exponents; the latter gives
    # its divisor sum, product (M_p+1)=2^(sum p).
    states = [(1, 0)]
    for mersenne, p in zip(mersennes, exponents):
        states += [(product * mersenne, weight + p) for product, weight in states]
    hits = []
    for a in range(total):
        sigma_two_power = 2 ** (a + 1) - 1
        two_power = 2**a
        for satellite_product, weight in states:
            k = two_power * satellite_product
            sigma_k = sigma_two_power * 2**weight
            if k * sigma_k == target:
                hits.append(k)
    expected = sorted(
        2 ** (p - 1) * math.prod(mersennes[j] for j in range(len(exponents)) if j != i)
        for i, p in enumerate(exponents)
    )
    if sorted(hits) != expected:
        raise AssertionError("prefix fiber contains an unexpected or missing preimage")
    return {
        **entropy_metrics(exponents),
        "target": target,
        "divisors_exhaustively_tested": total * (1 << len(exponents)),
        "complete_fiber": sorted(hits),
        "complete_fiber_size": len(hits),
        "constructed_fiber_is_complete": True,
        "pair_atom_support_matching_number": 1,
    }


def main():
    prefixes = [exact_prefix_census(EXPONENTS[:t]) for t in range(2, 13)]
    result = {
        "identity": "For M_i=2^p_i-1, v_i=2^(p_i-1)*product_(j!=i)M_j and h(v_i)=2^(P-1)*product_j M_j.",
        "normalized_pair_atom": "H(2,p_i-1)H(M_j,1)=H(2,p_j-1)H(M_i,1); every such support contains the hub prime 2.",
        "known_exponents": EXPONENTS,
        "known_52_metrics": entropy_metrics(EXPONENTS),
        "exact_complete_prefix_fibers": prefixes,
    }
    output = HERE / "mersenne_hub_fiber_metrics.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: exact complete-fiber divisor census for prefixes t=2,...,12")
    print(json.dumps(result["known_52_metrics"], indent=2))
    for row in prefixes:
        print(
            row["multiplicity"], row["target_bit_length"],
            row["divisors_exhaustively_tested"],
            row["log_multiplicity_over_logN_div_loglogN"],
        )


if __name__ == "__main__":
    main()
