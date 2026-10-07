#!/usr/bin/env python3
"""Finite exact regression, not a proof of the unbounded classification.

Enumerates all cap-two three-base increment equations among primes < 5000.
No incomplete cutoff: all unordered pairs of distinct-base increments are tested.
"""
import json
from fractions import Fraction
from pathlib import Path

LIMIT = 5000
sieve = bytearray(b'\x01') * LIMIT
sieve[:2] = b'\x00\x00'
for n in range(2, int((LIMIT - 1) ** 0.5) + 1):
    if sieve[n]:
        sieve[n * n:LIMIT:n] = b'\x00' * (((LIMIT - 1 - n * n) // n) + 1)
primes = [p for p in range(2, LIMIT) if sieve[p]]

def local_h(p, e):
    return p ** e * sum(p ** j for j in range(e + 1))

options = []
by_value = {}
for p in primes:
    for low, high in ((0, 1), (0, 2), (1, 2)):
        option = (Fraction(local_h(p, high), local_h(p, low)), p, low, high)
        options.append(option)
        by_value.setdefault(option[0], []).append(option)

comparisons = 0
witnesses = set()
for i, (x, p, a, b) in enumerate(options):
    for y, q, c, d in options[i + 1:]:
        if p == q:
            continue
        comparisons += 1
        for z, r, e, f in by_value.get(x * y, ()):
            if r in (p, q):
                continue
            old = p ** b * q ** d * r ** e
            new = p ** a * q ** c * r ** f
            assert local_h(p, b) * local_h(q, d) * local_h(r, e) == (
                local_h(p, a) * local_h(q, c) * local_h(r, f)
            )
            witnesses.add(tuple(sorted((old, new))))

assert witnesses == {(12, 14)}
expected_comparisons = len(options) * (len(options) - 1) // 2 - 3 * len(primes)
assert comparisons == expected_comparisons
result = {
    'scope': 'All cap-two exchanges on exactly three changed bases, each prime < 5000',
    'complete_for_stated_scope': True,
    'prime_count': len(primes),
    'local_increment_count': len(options),
    'distinct_base_pair_comparisons': comparisons,
    'residual_pairs': sorted(witnesses),
    'warning': 'Finite regression only; the unrestricted classification is proved separately in independent_exchange_review.md.',
}
output = Path(__file__).with_name('three_base_regression.json')
output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
