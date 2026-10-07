"""Exact checks for the fifth continuation of the Erdős 1060 investigation.
Python 3 standard library only. Run beside the JSON files in this packet.
The finite experiment does not replace the asymptotic mathematical proof.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from collections import Counter
from fractions import Fraction
import json
import math
import time

HERE = Path(__file__).resolve().parent
FACTORS = json.loads((HERE / 'factor_cache.json').read_text())
CERTS = json.loads((HERE / 'prime_certificates.json').read_text())

@lru_cache(None)
def certify_prime(n: int) -> bool:
    """Lucas criterion with the complete, recursively certified factorization of n-1."""
    if n == 2:
        return True
    assert n > 2 and n % 2
    cert = CERTS[str(n)]
    a = int(cert['a'])
    factors = {int(q): int(e) for q, e in cert['factors'].items()}
    assert math.prod(q**e for q, e in factors.items()) == n - 1
    assert all(1 < q < n and e > 0 and certify_prime(q) for q, e in factors.items())
    assert pow(a, n - 1, n) == 1
    assert all(pow(a, (n - 1)//q, n) != 1 for q in factors)
    return True


def primes_to(limit: int) -> list[int]:
    marks = bytearray(b'\1') * (limit + 1)
    marks[:2] = b'\0\0'
    for d in range(2, math.isqrt(limit) + 1):
        if marks[d]:
            marks[d*d:limit+1:d] = b'\0' * ((limit-d*d)//d + 1)
    return [p for p in range(2, limit + 1) if marks[p]]

@lru_cache(None)
def local_block(p: int, e: int) -> dict[int, int]:
    if not e:
        return {}
    fs = {int(q): int(v) for q, v in FACTORS[f'{p}:{e}'].items()}
    assert all(v > 0 and certify_prime(q) for q, v in fs.items())
    assert math.prod(q**v for q, v in fs.items()) == p**e * sum(p**i for i in range(e+1))
    return fs


def peeling_certificate() -> dict:
    columns = []
    ps = [p for p in primes_to(100000) if p >= 251]
    for p in ps:
        values = {e: local_block(p, e) for e in (0, 1, 2)}
        for a, b in ((1, 0), (2, 0), (2, 1)):
            va, vb = values[a], values[b]
            row = {q: va.get(q, 0)-vb.get(q, 0) for q in va.keys() | vb.keys()}
            columns.append((p, a, b, {q: v for q, v in row.items() if v}))
    initial = len(columns)
    rounds = []
    while columns:
        owners: dict[int, set[int]] = {}
        for p, a, b, row in columns:
            for q in row:
                owners.setdefault(q, set()).add(p)
        forced = {q for q, ps in owners.items() if len(ps) == 1}
        kept = [c for c in columns if not any(q in forced for q in c[3])]
        if len(kept) == len(columns):
            break
        rounds.append(len(columns)-len(kept))
        columns = kept
    assert not columns, 'The proposed full-peeling certificate failed.'
    assert initial == 28617
    return {'min_input_prime': 251, 'max_input_prime': 100000,
            'allowed_exponents': [0, 1, 2], 'input_primes': len(ps),
            'initial_columns': initial, 'deletions_by_round': rounds,
            'remaining_columns': 0, 'certified': True}


def check_new_witness() -> dict:
    record = json.loads((HERE / 'general_17_10000_1.json').read_text())['witness']
    terms = [(int(p), int(a), int(b)) for p, a, b in record['terms']]
    assert len({p for p, _, _ in terms}) == len(terms)
    assert all(0 <= a <= 2 and 0 <= b <= 2 and a != b for p, a, b in terms)
    assert all(p >= 17 and certify_prime(p) for p, _, _ in terms)
    # Direct geometric-sum product, without factoring the divisor sums.
    a = math.prod(p**e for p, e, _ in terms)
    b = math.prod(p**e for p, _, e in terms)
    sa = math.prod(sum(p**j for j in range(e+1)) for p, e, _ in terms)
    sb = math.prod(sum(p**j for j in range(e+1)) for p, _, e in terms)
    assert a != b and a*sa == b*sb
    assert str(a) == record['a'] and str(b) == record['b']
    assert str(a*sa) == record['target']
    # Separate check in the certified prime-valuation representation.
    net: Counter[int] = Counter()
    for p, ea, eb in terms:
        for q, e in local_block(p, ea).items():
            net[q] += e
        for q, e in local_block(p, eb).items():
            net[q] -= e
    assert all(e == 0 for e in net.values())
    return {'support_size': len(terms), 'least_input_prime': min(p for p, _, _ in terms),
            'largest_input_prime': max(p for p, _, _ in terms),
            'input_decimal_digits': [len(str(a)), len(str(b))],
            'target_decimal_digits': len(str(a*sa)),
            'geometric_sums_verified': True, 'certified_valuation_identity_verified': True,
            'full_divisor_enumeration_used': False}


def check_small_encoding(limit: int = 200000, y: int = 5) -> dict:
    """Independent small-input stress test of the exceptional-block encoding.
    This is an input-bounded test, not a complete enumeration of all encountered fibers.
    """
    spf = list(range(limit+1))
    for p in range(2, math.isqrt(limit)+1):
        if spf[p] == p:
            for m in range(p*p, limit+1, p):
                if spf[m] == m:
                    spf[m] = p
    qsmall = primes_to(y)
    primorial = math.prod(qsmall)
    seen = {}
    checked = 0
    for k in range(1, limit+1):
        n, sigma, encoded = k, 1, 1
        admissible = True
        while n > 1:
            p, e, pp = spf[n], 0, 1
            while n % p == 0:
                n //= p
                e += 1
                pp *= p
            if e > 5:
                admissible = False
                break
            sigp = sum(p**j for j in range(e+1))
            sigma *= sigp
            if p <= y or math.gcd(sigp, primorial) > 1:
                encoded *= pp
        if not admissible:
            continue
        key = (k*sigma, encoded)
        assert key not in seen, ('Unexpected duplicate encoding', seen.get(key), k, key)
        seen[key] = k
        checked += 1
    return {'input_limit': limit, 'y': y, 'input_exponent_cap': 5,
            'checked_inputs': checked, 'duplicate_encodings': 0,
            'complete_target_census': False}


def check_third_type_obstruction() -> dict:
    # These identities show why the two-index-prime residue argument alone
    # does not extend to input exponent 6. They do NOT give a collision.
    p, source, y = 67, 29, 7
    assert source**2 + source + 1 == 13*p
    sig4 = sum(p**j for j in range(5))
    sig6 = sum(p**j for j in range(7))
    qy = math.prod(primes_to(y))
    assert math.gcd(sig4*sig6*(source**2+source+1), qy) == 1
    assert p % 3 == 1 and p % 5 != 1 and p % 7 != 1
    return {'input_prime': p, 'incomparable_indices': [5, 7],
            'incoming_from_prime': source, 'incoming_exponent': 2,
            'small_prime_cutoff': y, 'local_divisor_sums_rough': True,
            'is_collision': False}


def main() -> None:
    started = time.monotonic()
    result = {'exact_peeling': peeling_certificate(),
              'new_witness': check_new_witness(),
              'small_encoding_test': check_small_encoding(),
              'third_type_obstruction': check_third_type_obstruction(),
              'primality_certificates_checked': certify_prime.cache_info().currsize,
              'all_checks_passed': True}
    result['elapsed_seconds'] = time.monotonic()-started
    text = json.dumps(result, indent=2)
    (HERE/'verification_v5.json').write_text(text+'\n')
    print(text)

if __name__ == '__main__':
    main()
