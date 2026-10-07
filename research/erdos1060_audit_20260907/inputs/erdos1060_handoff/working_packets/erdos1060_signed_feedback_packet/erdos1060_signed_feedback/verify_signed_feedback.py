#!/usr/bin/env python3
"""Exact finite checks for the signed-feedback fiber bounds.

Only the Python standard library is used. This is a finite certificate checker,
not a proof of a uniform bound for Erdős Problem 1060.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
from math import isqrt, prod
from pathlib import Path
import json

M = {2:20,3:5,5:1,7:3,11:2,13:2,17:2,19:2,23:1,31:2,
     43:1,61:2,83:1,97:1,127:2,271:1,307:2,331:1,367:1,733:1,5419:1}
N0 = {2:7,3:3,5:1,7:2,13:1,19:2,127:1}
A = {11:2,13:2,17:1,19:1,31:1,61:1,97:1,127:2,271:1,307:2,331:1,367:1}
B = {13:1,17:2,19:2,23:1,31:2,43:1,61:2,83:1,127:1,307:1,733:1,5419:1}

def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))

def sigma_power(p: int, e: int) -> int:
    return sum(p ** j for j in range(e + 1))

def value(f: dict[int, int]) -> int:
    return prod(p ** e for p, e in f.items())

def h(f: dict[int, int]) -> int:
    return value(f) * prod(sigma_power(p, e) for p, e in f.items())

def model(fac: dict[int,int], cap: int = 2):
    ps = sorted(fac)
    assert all(prime(p) for p in ps)
    alpha = tuple(fac[p] for p in ps)
    N = value(fac)
    options = {}
    domains = {}
    for p in ps:
        options[p] = {}
        for e in range(min(cap, fac[p]) + 1):
            local = p ** e * sigma_power(p, e)
            if N % local:
                continue
            rest = local
            vals = []
            for q in ps:
                v = 0
                while rest % q == 0:
                    rest //= q
                    v += 1
                vals.append(v)
            assert rest == 1
            options[p][e] = tuple(vals)
        domains[p] = sorted(options[p])
    return ps, alpha, options, domains

def prune(ps, alpha, options, domains):
    """Delete only an option unsupported by some exact target-valuation row."""
    domains = {p: list(domains[p]) for p in ps}
    removed = []
    while True:
        deletions = set()
        for row, target in enumerate(alpha):
            prefix = [{0}]
            for p in ps:
                vals = {options[p][e][row] for e in domains[p]}
                prefix.append({a+b for a in prefix[-1] for b in vals if a+b <= target})
            if target not in prefix[-1]:
                raise AssertionError('The selected test target became infeasible')
            suffix = [None] * (len(ps)+1)
            suffix[-1] = {0}
            for j in range(len(ps)-1, -1, -1):
                p = ps[j]
                vals = {options[p][e][row] for e in domains[p]}
                suffix[j] = {a+b for a in suffix[j+1] for b in vals if a+b <= target}
            for j,p in enumerate(ps):
                other = {a+b for a in prefix[j] for b in suffix[j+1] if a+b <= target}
                for e in domains[p]:
                    if target-options[p][e][row] not in other:
                        deletions.add((p,e))
        if not deletions:
            return domains, removed
        for p,e in sorted(deletions):
            domains[p].remove(e)
            removed.append([p,e])
            assert domains[p]

def signed_graph(ps, options, domains, cuts=None, exclude=()):
    """Signs are minus the sign of a change in another prime's sigma valuation.

    cuts[p] contains integers c representing the cut e<=c versus e>c.
    Edges supported only by transitions crossing a cut are omitted.
    """
    cuts = cuts or {}
    nodes = [p for p in ps if p not in exclude and len(domains[p]) > 1]
    rows = {p: i for i,p in enumerate(ps)}
    graph = {p:{} for p in nodes}
    for p in nodes:
        for a,b in zip(domains[p], domains[p][1:]):
            if any(a <= c < b for c in cuts.get(p, ())):
                continue
            for q in nodes:
                if p == q:
                    continue
                d = options[p][b][rows[q]] - options[p][a][rows[q]]
                if d:
                    graph[p].setdefault(q,set()).add(-1 if d > 0 else 1)
    return graph

def elementary_cycles(graph):
    """Enumerate vertex-simple directed cycles, once per cyclic rotation."""
    result=[]
    for start in sorted(graph):
        def walk(path, visited):
            tail=path[-1]
            for q in sorted(graph[tail]):
                if q == start and len(path)>1:
                    signs={1}
                    for a,b in zip(path, path[1:]+path[:1]):
                        signs={s*t for s in signs for t in graph[a][b]}
                    result.append({'vertices':path[:], 'signs':sorted(signs)})
                elif q>start and q not in visited:
                    walk(path+[q], visited|{q})
        walk([start], {start})
    return result

def block_count(dom, cuts):
    return 1+sum(any(a<=c<b for c in cuts) for a,b in zip(dom,dom[1:]))

def check_threshold_certificate(fac, cuts):
    ps,alpha,options,start=model(fac)
    domains,removed=prune(ps,alpha,options,start)
    before=elementary_cycles(signed_graph(ps,options,domains))
    after=elementary_cycles(signed_graph(ps,options,domains,cuts))
    assert all(1 not in c['signs'] for c in after)
    bound=prod(block_count(domains[p], cuts.get(p,())) for p in ps)
    return {'initial_options':sum(map(len,start.values())),
            'pruned_options':sum(map(len,domains.values())),
            'deleted_options':removed,
            'cuts':cuts,
            'domains':domains,
            'cycles_before':len(before),
            'positive_cycles_before':sum(1 in c['signs'] for c in before),
            'cycles_after':len(after),
            'positive_cycles_after':0,
            'remaining_negative_cycles':after,
            'certified_upper_bound':bound}

def difference_cycle(fac, left, right):
    """Construct the positive cycle in the proof, using the actual pair."""
    ps,alpha,options,domains=model(fac)
    changed=[p for p in ps if left.get(p,0)!=right.get(p,0)]
    d={p:left.get(p,0)-right.get(p,0) for p in changed}
    predecessor={}
    for q in changed:
        row=ps.index(q)
        terms={p:options[p][left.get(p,0)][row]-options[p][right.get(p,0)][row]
               for p in changed if p!=q}
        assert d[q] == -sum(terms.values())
        p=next(p for p in sorted(terms) if terms[p]*d[q]<0)
        predecessor[q]=p
    path=[];seen={};q=changed[0]
    while q not in seen:
        seen[q]=len(path);path.append(q);q=predecessor[q]
    cycle=list(reversed(path[seen[q]:]))
    signs=[]
    for p,q in zip(cycle,cycle[1:]+cycle[:1]):
        signs.append(1 if d[p]*d[q]>0 else -1)
    assert prod(signs)==1
    return {'vertices':cycle,'signs':signs}

def main():
    assert h(A)==h(B)==value(M)
    # Separate complete-divisor-summation verification of these witnesses.
    divisor_counts=[]
    for fac in (A,B):
        ds=[1]
        for p,e in fac.items():
            assert prime(p)
            ds=[d*p**j for d in ds for j in range(e+1)]
        assert value(fac)*sum(ds)==value(M)
        divisor_counts.append(len(ds))
    m_cert=check_threshold_certificate(M,{2:[0,1],13:[1],19:[1]})
    n_cert=check_threshold_certificate(N0,{2:[0,1],3:[1]})
    assert m_cert['certified_upper_bound']==12
    assert n_cert['certified_upper_bound']==6
    # With 2 and 3 fixed, there is one quadratic pair and four long positive cycles.
    ps,alpha,options,domains=model(M)
    cycles=elementary_cycles(signed_graph(ps,options,domains,exclude=(2,3)))
    positive=[c for c in cycles if 1 in c['signs']]
    long=[c for c in positive if len(c['vertices'])>=3]
    pairs=[c for c in positive if len(c['vertices'])==2]
    assert len(cycles)==6 and len(positive)==5 and len(long)==4
    assert all(17 in c['vertices'] for c in long)
    assert [c['vertices'] for c in pairs]==[[13,61]]
    # Killing the four long positive cycles by fixing 17 and cutting at 61 suffices.
    reduced={p:list(v) for p,v in domains.items()}
    # Omitting fixed vertices is valid regardless of the exponent values fixed.
    g=signed_graph(ps,options,domains,cuts={61:[1]},exclude=(2,3,17))
    assert all(1 not in c['signs'] for c in elementary_cycles(g))
    # A genuine long all-quadratic arithmetic cycle; it is not a collision.
    qcycle=[193,1783,1279,2383,12541,576151,151009,6067]
    quotients=[]
    for p,q in zip(qcycle,qcycle[1:]+qcycle[:1]):
        assert prime(p) and prime(q)
        assert sigma_power(p,2)%q==0
        quotients.append(sigma_power(p,2)//q)
    result={'status':'Exact finite checks, not an unrestricted asymptotic proof',
            'M':m_cert,'N0':n_cert,'M_witness_divisor_counts':divisor_counts,
            'M_actual_pair_positive_cycle':difference_cycle(M,A,B),
            'M_graph_above_3':{'cycles':cycles,'long_positive_hit_vertex':17,
                               'remaining_pair':[13,61], 'certified_bound':54},
            'quadratic_eight_cycle':{'vertices':qcycle,'quotients':quotients}}
    out=Path(__file__).with_name('verification.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'M_upper_bound':12,'N0_upper_bound':6,
                      'M_above_3_bound':54,'checks':'passed'},indent=2))

if __name__=='__main__':
    main()
