"""Exact finite-fiber and support-minimal exchange checks.

Python 3.10+, standard library only. No asymptotic theorem is asserted.
A failed or resource-limited enumeration raises an exception rather than
reporting a complete fiber. The atom extraction uses a COMPLETE fiber.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import prod
from pathlib import Path
import json
from branch_solver import ExactSolver, prime, local_sigma


def exponent_vector(k: int, primes: tuple[int, ...]) -> tuple[int, ...]:
    ans = []
    for p in primes:
        e = 0
        while k % p == 0:
            k //= p
            e += 1
        ans.append(e)
    if k != 1:
        raise ValueError('Input has a prime outside the target factorization.')
    return tuple(ans)


def all_divisors_with_sigma(factors: dict[int, int]) -> list[tuple[int, int]]:
    """Complete divisor enumeration using partial geometric-sum recurrence."""
    out = [(1, 1)]
    for p, emax in sorted(factors.items()):
        if not prime(p) or emax < 1:
            raise ValueError('Invalid target factorization.')
        options = []
        pe, sig = 1, 1
        for e in range(emax + 1):
            if e:
                pe *= p
                sig += pe
            options.append((pe, sig))
        out = [(d * pe, s * sig) for d, s in out for pe, sig in options]
    return out


def sum_divisors_independently(primes: tuple[int, ...], vec: tuple[int, ...]) -> tuple[int, int]:
    divisors = [1]
    for p, emax in zip(primes, vec):
        powers = [p ** e for e in range(emax + 1)]
        divisors = [d * pe for d in divisors for pe in powers]
    return len(divisors), sum(divisors)


def unit_subsets(ratios: list[Fraction]) -> list[int]:
    """Meet-in-the-middle: all subset masks whose rational product is one."""
    mid = len(ratios) // 2
    def half(rs: list[Fraction]) -> list[tuple[Fraction, int]]:
        states = [(Fraction(1), 0)]
        for i, r in enumerate(rs):
            states += [(v * r, mask | (1 << i)) for v, mask in states[:]]
        return states
    left = defaultdict(list)
    for val, mask in half(ratios[:mid]):
        left[val].append(mask)
    ans = []
    for val, mask in half(ratios[mid:]):
        for lm in left.get(1 / val, []):
            ans.append(lm | (mask << mid))
    return sorted(ans)


def analyze_reference(primes: tuple[int, ...], vectors: list[tuple[int, ...]],
                      ref: tuple[int, ...]) -> dict:
    moves = [{i: e for i, e in enumerate(v) if e != ref[i]}
             for v in vectors if v != ref]
    atoms = [m for m in moves if not any(
        len(s) < len(m) and all(m.get(i) == e for i, e in s.items())
        for s in moves)]
    encoded = []
    for atom in atoms:
        positions = sorted(atom)
        ratios = [Fraction(primes[i] ** atom[i] * local_sigma(primes[i], atom[i]),
                           primes[i] ** ref[i] * local_sigma(primes[i], ref[i]))
                  for i in positions]
        # This test proves minimality without presupposing fiber completeness.
        assert unit_subsets(ratios) == [0, (1 << len(positions)) - 1]
        old = prod(primes[i] ** ref[i] for i in positions)
        new = prod(primes[i] ** atom[i] for i in positions)
        cost = prod(primes[i] ** ref[i] * local_sigma(primes[i], ref[i])
                    for i in positions)
        assert cost == prod(primes[i] ** atom[i] * local_sigma(primes[i], atom[i])
                            for i in positions)
        encoded.append({'changes': {str(primes[i]): [ref[i], atom[i]] for i in positions},
                        'old_input': str(old), 'new_input': str(new),
                        'local_target': str(cost)})
    images = defaultdict(list)
    def visit(j: int, changes: dict[int, int], selected: tuple[int, ...]) -> None:
        if j == len(atoms):
            v = tuple(changes.get(i, e) for i, e in enumerate(ref))
            assert v in vectors
            images[v].append(selected)
            return
        visit(j + 1, changes, selected)
        if changes.keys().isdisjoint(atoms[j]):
            visit(j + 1, changes | atoms[j], selected + (j,))
    visit(0, {}, ())
    assert set(images) == set(vectors)
    edges = [(i, j) for i, j in combinations(range(len(atoms)), 2)
             if not atoms[i].keys().isdisjoint(atoms[j])]
    return {'reference': str(prod(p ** e for p, e in zip(primes, ref))),
            'atoms': encoded, 'overlap_edges': edges,
            'independent_sets': sum(len(v) for v in images.values()),
            'distinct_images': len(images),
            'maximum_decompositions_of_one_image': max(map(len, images.values())),
            'independent_sets_and_images': [
                {'input': str(prod(p ** e for p, e in zip(primes, vec))),
                 'decompositions': decomps} for vec, decomps in sorted(images.items())]}


def main() -> None:
    mf = {2:20,3:5,5:1,7:3,11:2,13:2,17:2,19:2,23:1,31:2,43:1,
          61:2,83:1,97:1,127:2,271:1,307:2,331:1,367:1,733:1,5419:1}
    scaled = mf.copy()
    for p, e in {2:4,3:1,7:1}.items(): scaled[p] += e
    cases = [
        ('M_cubefree', mf, 2, 2, False),
        ('336M_cubefree', scaled, 2, 4, False),
        ('seven_unrestricted', {2:28,3:3,5:1,7:1,13:1,31:1,127:1,8191:1}, None, 7, True),
        ('six_unrestricted', {2:31,3:2,5:3,7:1,13:1,31:1,127:1,8191:1}, None, 6, True),
        ('nine_unrestricted', {2:45,3:3,5:1,7:1,13:1,31:1,127:1,8191:1,131071:1}, None, 9, True),
    ]
    output = []
    for name, fac, cap, expected, brute in cases:
        solver = ExactSolver(fac, cap, seconds=120, node_limit=100000)
        result = solver.solve()
        assert result['complete']
        sols = [int(x) for x in result['solutions']]
        assert len(sols) == expected
        vecs = [exponent_vector(k, solver.primes) for k in sols]
        result['name'] = name
        if brute:
            divs = all_divisors_with_sigma(fac)
            direct = sorted(d for d, s in divs if d * s == solver.N)
            assert direct == sols
            result['independent_complete_target_divisor_check'] = len(divs)
        result['divisor_sum_witness_checks'] = []
        for k, vec in zip(sols, vecs):
            tau, sig = sum_divisors_independently(solver.primes, vec)
            assert k * sig == solver.N
            result['divisor_sum_witness_checks'].append(
                {'input': str(k), 'divisors_summed': tau, 'sigma': str(sig)})
        result['references'] = [analyze_reference(solver.primes, vecs, ref) for ref in vecs]
        output.append(result)
        print(name, len(sols), 'preimages; all exchange checks passed', flush=True)
    Path(__file__).with_name('verification.json').write_text(json.dumps(output, indent=2) + '\n')
    print('All checks passed. No asymptotic conclusion is asserted.')


if __name__ == '__main__':
    main()
