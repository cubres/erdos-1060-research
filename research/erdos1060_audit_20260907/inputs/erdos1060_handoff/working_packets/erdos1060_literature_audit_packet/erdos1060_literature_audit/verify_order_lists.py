#!/usr/bin/env python3
"""Exact tests of primitive-divisor exponent lists for k*sigma(k)=N.

Uses only the Python standard library. The general theorem depends on the
Bang--Zsigmondy theorem; finite tests here are regression checks, not its proof.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
from math import isqrt, prod
from pathlib import Path
import json


def factor(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError('factor expects a positive integer')
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def is_prime(p: int) -> bool:
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def sigma_power(p: int, e: int) -> int:
    return (pow(p, e + 1) - 1) // (p - 1)


def block(p: int, e: int) -> int:
    return pow(p, e) * sigma_power(p, e)


def order(p: int, q: int) -> int:
    if p % q == 0:
        raise ValueError('multiplicative order requires a nonzero residue')
    d = q - 1
    for ell in factor(d):
        while d % ell == 0 and pow(p, d // ell, q) == 1:
            d //= ell
    assert pow(p, d, q) == 1
    return d


def candidate_indices(p: int, support: tuple[int, ...]) -> set[int]:
    candidates = {0, 1}
    if p == 2:
        candidates.add(5)
    for q in support:
        if q != p:
            d = order(p, q)
            if d >= 3:
                candidates.add(d - 1)
    return candidates


def domains(n: int, fac: dict[int, int]) -> dict[int, list[int]]:
    support = tuple(sorted(fac))
    out = {}
    for p, a in sorted(fac.items()):
        choices = sorted(e for e in candidate_indices(p, support)
                         if e <= a and n % block(p, e) == 0)
        scan = [e for e in range(a + 1) if n % block(p, e) == 0]
        assert choices == scan, (n, p, choices, scan)
        powerful = [e for e in choices if e >= 2]
        # Produce distinct witnesses for the higher-exponent choices.
        witnesses = {}
        for e in powerful:
            if (p, e) == (2, 5):
                assert 3 in fac
                witnesses[e] = 3
            else:
                qs = [q for q in support if q != p and order(p, q) == e + 1]
                assert qs, (n, p, e)
                q = min(qs)
                assert q >= 5 and sigma_power(p, e) % q == 0
                witnesses[e] = q
        assert len(set(witnesses.values())) == len(witnesses)
        assert 1 + len(powerful) <= len(fac)
        out[p] = choices
    return out


def h_from_factor(fac: dict[int, int]) -> int:
    return prod(block(p, e) for p, e in fac.items())


def complete_divisor_fiber(n: int, fac: dict[int, int]) -> list[int]:
    count = prod(a + 1 for a in fac.values())
    if count > 200000:
        raise RuntimeError('explicit divisor resource limit exceeded')
    ps = sorted(fac)
    ans = []
    for es in product(*(range(fac[p] + 1) for p in ps)):
        if prod(block(p, e) for p, e in zip(ps, es)) == n:
            k = prod(p**e for p, e in zip(ps, es))
            # Independent check: enumerate and sum every divisor of the input.
            divs = [1]
            for p, e in zip(ps, es):
                divs = [d * p**j for d in divs for j in range(e + 1)]
            assert k * sum(divs) == n
            ans.append(k)
    return sorted(ans)


def support_example(support: tuple[int, ...]) -> dict:
    # All supported preimages, with no height/exponent cutoff, by the theorem.
    choices = {}
    for p in support:
        keep = []
        for e in sorted(candidate_indices(p, support)):
            rest = sigma_power(p, e)
            for q in support:
                while rest % q == 0:
                    rest //= q
            if rest == 1:
                keep.append(e)
        choices[p] = keep
    fibers: dict[int, list[int]] = defaultdict(list)
    for es in product(*(choices[p] for p in support)):
        k = prod(p**e for p, e in zip(support, es))
        n = prod(block(p, e) for p, e in zip(support, es))
        fibers[n].append(k)
    return {'support': list(support), 'local_exponents': choices,
            'number_of_inputs': sum(map(len, fibers.values())),
            'max_fiber_size': max(map(len, fibers.values())),
            'fibers': {str(n): sorted(ks) for n, ks in sorted(fibers.items())}}


def run() -> dict:
    targets = {
        'N7': {2: 28, 3: 3, 5: 1, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1},
        'N6': {2: 31, 3: 2, 5: 3, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1},
        'N9': {2: 45, 3: 3, 5: 1, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1, 131071: 1},
        'N0': {2: 7, 3: 3, 5: 1, 7: 2, 13: 1, 19: 2, 127: 1},
    }
    summary = {}
    for name, fac in targets.items():
        assert all(is_prime(p) for p in fac)
        n = prod(p**a for p, a in fac.items())
        ds = domains(n, fac)
        core_options = {p: [0] + [e for e in es if e >= 2] for p, es in ds.items()}
        fiber = complete_divisor_fiber(n, fac)
        summary[name] = {
            'target': str(n), 'factorization': fac, 'local_domains': ds,
            'powerful_core_options': core_options,
            'local_core_bound': prod(map(len, core_options.values())),
            'original_product_bound': prod(fac.values()),
            'omega_bound': len(fac)**len(fac),
            'number_of_target_divisors_tested': prod(a + 1 for a in fac.values()),
            'full_fiber': [str(k) for k in fiber], 'f': len(fiber),
        }
        assert len(fiber) <= summary[name]['local_core_bound']
    # Regression over small represented targets, using direct sigma sums.
    limit = 10000
    sigmas = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            sigmas[m] += d
    local_tests = 0
    for k in range(2, limit + 1):
        fac = factor(k)
        for p, a in factor(sigmas[k]).items():
            fac[p] = fac.get(p, 0) + a
        ds = domains(k * sigmas[k], fac)
        local_tests += len(ds)
        for p, e in factor(k).items():
            assert e in ds[p]
    report = {
        'scope': 'Finite regression plus complete listed fibers; not a proof of Erdos 1060',
        'targets': summary,
        'supported_input_examples': [support_example((2, 3)), support_example((2, 3, 7))],
        'regression_seed_input_bound': limit,
        'regression_represented_targets_with_repetition': limit - 1,
        'regression_local_domain_comparisons': local_tests,
        'primitive_witness_reuse_example': {
            'q': 7, 'bases': [2, 11],
            'orders': [order(2, 7), order(11, 7)],
        },
    }
    return report


if __name__ == '__main__':
    result = run()
    path = Path(__file__).with_name('verification.json')
    path.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Exact checks passed; wrote', path)
    for label, data in result['targets'].items():
        print(label, 'f =', data['f'], 'new local bound =', data['local_core_bound'],
              'product bound =', data['original_product_bound'])
    print('Compared', result['regression_local_domain_comparisons'], 'local domains')
