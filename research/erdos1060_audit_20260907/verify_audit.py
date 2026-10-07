"""Independent finite checks for the 7 September 2026 audit.

No code is imported from the supplied research packet.  Integer arithmetic is
used throughout.  This verifies specified finite claims, not an asymptotic bound.
"""
from __future__ import annotations

import hashlib
import json
import time
from fractions import Fraction
from math import gcd, isqrt, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def sigma_block(p, e):
    return (p ** (e + 1) - 1) // (p - 1)


def h_block(p, e):
    return p ** e * sigma_block(p, e)


def factor_small(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def direct_fiber(fac):
    assert all(prime(p) and e > 0 for p, e in fac.items())
    n = prod(p ** e for p, e in fac.items())
    # A complete divisor list is a complete candidate list because k | h(k).
    ds = [(1, 1)]
    for p, a in fac.items():
        ds = [(d * p ** e, s * sigma_block(p, e))
              for d, s in ds for e in range(a + 1)]
    return n, len(ds), sorted(d for d, s in ds if d * s == n)


def capped_fiber(fac, cap, seconds=90):
    """Exhaustive local-state search, using only necessary row bounds.

    Each branch fixes one whole prime-power block and subtracts its valuation
    vector.  Interval propagation discards a state only when a valuation row
    cannot be completed even between its independent minimum and maximum.
    Thus it cannot discard a true solution.  All terminal rows are checked.
    """
    ps = tuple(sorted(fac))
    assert all(prime(p) for p in ps)
    n = prod(p ** fac[p] for p in ps)
    domains = []
    for p in ps:
        options = []
        for e in range(min(cap, fac[p]) + 1):
            value = h_block(p, e)
            if n % value:
                continue
            v, rows = value, []
            for q in ps:
                a = 0
                while v % q == 0:
                    v //= q
                    a += 1
                rows.append(a)
            assert v == 1
            options.append((e, p ** e, tuple(rows)))
        domains.append(tuple(options))
    begun, nodes = time.monotonic(), 0
    solutions = []

    def visit(left, remaining, k):
        nonlocal nodes
        nodes += 1
        if nodes > 200_000 or time.monotonic() - begun > seconds:
            raise RuntimeError('Resource limit; the search is incomplete')
        left = [(i, list(opts)) for i, opts in left]
        while left:
            if any(not opts for _, opts in left):
                return
            minima = [tuple(min(o[2][j] for o in opts) for j in range(len(ps)))
                      for _, opts in left]
            maxima = [tuple(max(o[2][j] for o in opts) for j in range(len(ps)))
                      for _, opts in left]
            low = tuple(sum(v[j] for v in minima) for j in range(len(ps)))
            high = tuple(sum(v[j] for v in maxima) for j in range(len(ps)))
            if any(not low[j] <= remaining[j] <= high[j] for j in range(len(ps))):
                return
            changed = False
            for t, (i, opts) in enumerate(left):
                filtered = [o for o in opts if all(
                    low[j] - minima[t][j] <= remaining[j] - o[2][j]
                    <= high[j] - maxima[t][j] for j in range(len(ps)))]
                changed |= len(filtered) != len(opts)
                left[t] = (i, filtered)
            if not changed:
                break
        if not left:
            assert not any(remaining)
            solutions.append(k)
            return
        t = min(range(len(left)), key=lambda a: (len(left[a][1]), -ps[left[a][0]]))
        i, opts = left[t]
        rest = left[:t] + left[t + 1:]
        for e, pe, rows in opts:
            residual = tuple(a - b for a, b in zip(remaining, rows))
            if min(residual) >= 0:
                visit(rest, residual, k * pe)

    visit(list(enumerate(domains)), tuple(fac[p] for p in ps), 1)
    assert len(solutions) == len(set(solutions))
    for k in solutions:
        x, sigma = k, 1
        for p in ps:
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            assert e <= cap
            sigma *= sigma_block(p, e)
        assert x == 1 and k * sigma == n
    return {'target': str(n), 'cap': cap, 'complete': True,
            'nodes': nodes, 'solutions': [str(x) for x in sorted(solutions)]}


def normalization(a, b):
    fa, fb = factor_small(a), factor_small(b)
    ps = sorted(fa.keys() | fb.keys())
    sa = prod(sigma_block(p, e) for p, e in fa.items())
    sb = prod(sigma_block(p, e) for p, e in fb.items())
    assert a * sa == b * sb
    local_gcd = prod(gcd(sigma_block(p, fa.get(p, 0)),
                         sigma_block(p, fb.get(p, 0))) for p in ps)
    sigma_gcd = prod(sigma_block(p, min(fa.get(p, 0), fb.get(p, 0))) for p in ps)
    c = gcd(sa, sb) // local_gcd
    C = prod(p ** (min(fa.get(p, 0), fb.get(p, 0)) + 1
                    - gcd(fa.get(p, 0) + 1, fb.get(p, 0) + 1)) for p in ps)
    return {'inputs': [a, b], 'sigma': [sa, sb], 'c': c, 'C': C,
            'T': c, 'R': sigma_gcd // local_gcd}


def main():
    manifest_root = ROOT / 'inputs/erdos1060_handoff'
    manifest = json.loads((manifest_root / 'MANIFEST.json').read_text())
    for row in manifest['files']:
        p = manifest_root / row['path']
        assert p.stat().st_size == row['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256']
    report = {'input_manifest_files_verified': len(manifest['files']), 'direct_fibers': []}
    examples = [
        ({2: 28, 3: 3, 5: 1, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1}, 7),
        ({2: 31, 3: 2, 5: 3, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1}, 6),
        ({2: 45, 3: 3, 5: 1, 7: 1, 13: 1, 31: 1, 127: 1, 8191: 1, 131071: 1}, 9),
    ]
    for fac, expected in examples:
        n, tested, solutions = direct_fiber(fac)
        assert len(solutions) == expected
        report['direct_fibers'].append({'target': str(n), 'all_divisors_tested': tested,
                                       'solutions': [str(k) for k in solutions]})
        print(f'Direct complete fiber: {expected} solutions, {tested} divisors', flush=True)
    mf = {2:20,3:5,5:1,7:3,11:2,13:2,17:2,19:2,23:1,31:2,43:1,
          61:2,83:1,97:1,127:2,271:1,307:2,331:1,367:1,733:1,5419:1}
    scaled = mf.copy()
    for p, e in {2:4,3:1,7:1}.items():
        scaled[p] += e
    report['capped_fibers'] = []
    for fac, expected in [(mf, 2), (scaled, 4),
                          ({2:7,3:3,5:1,7:2,13:1,19:2,127:1}, 1)]:
        result = capped_fiber(fac, 2)
        assert len(result['solutions']) == expected
        report['capped_fibers'].append(result)
        print(f'Complete cap-two fiber: {expected} solutions, {result["nodes"]} nodes', flush=True)
    report['normalizations'] = [normalization(12, 14), normalization(315, 351)]
    assert report['normalizations'][1]['C'] == 9
    assert report['normalizations'][1]['R'] == 13

    # Independent finite check of the proved three-prime-pattern classification.
    ps = [p for p in range(2, 2001) if prime(p)]
    hits, tests = [], 0
    for p in ps:
        for q in ps:
            if p == q:
                continue
            tests += 1
            n, d = p * (p*p+p+1) * q * (q+1), p+1
            if n % d:
                continue
            value = n // d
            disc = 1 + 4 * value
            root = isqrt(disc)
            if root*root != disc or root % 2 != 1:
                continue
            r = (root-1)//2
            if prime(r) and len({p,q,r}) == 3:
                assert h_block(p,2)*h_block(q,1) == h_block(p,1)*h_block(r,1)
                hits.append([p,q,r])
    assert hits == [[2,3,7]]
    report['pattern_check'] = {'p_q_bound': 2000, 'pairs_tested': tests,
                               'hits': hits, 'r': 'unbounded candidate from exact quadratic'}
    report['scope'] = ('Specified finite checks only. No global census, formal proof-assistant '
                       'certification, novelty assertion, or solution of Erdos 1060.')
    (ROOT / 'verification_results.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: all independent finite checks completed', flush=True)


if __name__ == '__main__':
    main()
