#!/usr/bin/env python3
"""Search exact one-hub collision families.

If H(r,a_i)/H(q_i,b_i) is the same reduced rational number for t distinct
satellite bases q_i, then

  r^a_i * product_{j != i} q_j^b_j,  i=1,...,t,

are t preimages of one target.  Every pairwise normalized collision uses the
same hub base r, so the support-hypergraph matching number is one even when t
is large.  The Mersenne-prime construction is the ratio 1/2 at r=2.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).parent


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def block(p: int, exponent: int) -> int:
    return p**exponent * ((p ** (exponent + 1) - 1) // (p - 1))


def family_certificate(hub, ratio, members):
    # Keep at most one member per satellite base and require different hub
    # exponents, as an input cannot use two powers of the same base.
    members = sorted(members)
    satellites = [q for _, q, _ in members]
    if len(set(satellites)) != len(satellites):
        return None
    if len({a for a, _, _ in members}) != len(members):
        return None
    satellite_blocks = [block(q, b) for _, q, b in members]
    target = block(hub, members[0][0]) * math.prod(satellite_blocks[1:])
    inputs = []
    for i, (a, _, _) in enumerate(members):
        value = hub**a
        for j, (_, q, b) in enumerate(members):
            if i != j:
                value *= q**b
        inputs.append(value)
        check = block(hub, a) * math.prod(
            satellite_blocks[j] for j in range(len(members)) if j != i
        )
        assert check == target
    log_target = math.log(target)
    entropy_scale = log_target / math.log(log_target)
    return {
        "hub": hub,
        "ratio_numerator": ratio[0],
        "ratio_denominator": ratio[1],
        "members": [[a, q, b] for a, q, b in members],
        "multiplicity": len(members),
        "common_target": target,
        "inputs": inputs,
        "target_natural_log": log_target,
        "log_multiplicity": math.log(len(members)),
        "log_multiplicity_over_logN_div_loglogN": math.log(len(members)) / entropy_scale,
        "normalized_atom_matching_number": 1,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-upper", type=int, default=50)
    parser.add_argument("--hub-max-exponent", type=int, default=30)
    parser.add_argument("--satellite-upper", type=int, default=10000)
    parser.add_argument("--satellite-max-exponent", type=int, default=4)
    parser.add_argument("--minimum-size", type=int, default=3)
    parser.add_argument("--output", type=Path, default=HERE / "hub_families.json")
    args = parser.parse_args()

    hubs = primes_through(args.hub_upper)
    satellites = primes_through(args.satellite_upper)
    satellite_columns = [
        (q, b, block(q, b))
        for q in satellites
        for b in range(1, args.satellite_max_exponent + 1)
    ]
    certificates = []
    raw_groups = 0
    for hub in hubs:
        groups = defaultdict(list)
        for a in range(1, args.hub_max_exponent + 1):
            hub_block = block(hub, a)
            for q, b, satellite_block in satellite_columns:
                if q == hub:
                    continue
                divisor = math.gcd(hub_block, satellite_block)
                ratio = (hub_block // divisor, satellite_block // divisor)
                groups[ratio].append((a, q, b))
        for ratio, members in groups.items():
            if len(members) < args.minimum_size:
                continue
            raw_groups += 1
            certificate = family_certificate(hub, ratio, members)
            if certificate is not None and certificate["multiplicity"] >= args.minimum_size:
                certificates.append(certificate)
        print(f"hub={hub}: retained_families={sum(c['hub']==hub for c in certificates)}", flush=True)

    certificates.sort(key=lambda c: (-c["multiplicity"], c["common_target"]))
    result = {
        "search": {
            "hub_upper": args.hub_upper,
            "hub_max_exponent": args.hub_max_exponent,
            "satellite_upper": args.satellite_upper,
            "satellite_max_exponent": args.satellite_max_exponent,
            "minimum_size": args.minimum_size,
            "raw_ratio_groups_at_least_minimum_size": raw_groups,
        },
        "families": certificates,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"families={len(certificates)}")
    for certificate in certificates[:20]:
        print(
            "hub", certificate["hub"], "ratio",
            f"{certificate['ratio_numerator']}/{certificate['ratio_denominator']}",
            "size", certificate["multiplicity"], "members", certificate["members"],
            "entropy_ratio", certificate["log_multiplicity_over_logN_div_loglogN"],
        )


if __name__ == "__main__":
    main()
