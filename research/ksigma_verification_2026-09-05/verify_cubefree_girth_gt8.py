#!/usr/bin/env python3
"""Exact standard-library verifier for the cubefree girth-ten certificate."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


DATA = Path(__file__).parent / "cubefree_girth_gt8_collision.json"


def factor(n: int) -> Counter[int]:
    out: Counter[int] = Counter()
    d = 2
    while d*d <= n:
        while n % d == 0:
            out[d] += 1; n //= d
        d = 3 if d == 2 else d+2
    if n > 1: out[n] += 1
    return out


def is_prime(n: int) -> bool:
    return factor(n) == Counter({n: 1})


def sigma_pp(p: int, e: int) -> int:
    value = sum(p**j for j in range(e+1))
    assert value == (p**(e+1)-1)//(p-1)
    return value


def block_factors(p: int, e: int) -> Counter[int]:
    out = Counter({p:e}); out.update(factor(sigma_pp(p,e))); return out


def aggregate(blocks):
    value=math.prod(p**e for p,e in blocks)
    sigma=math.prod(sigma_pp(p,e) for p,e in blocks)
    factors=Counter()
    for p,e in blocks: factors.update(block_factors(p,e))
    return value,sigma,factors


def h_from_factors(factors):
    return math.prod(p**e*sigma_pp(p,e) for p,e in factors.items())


def canonical_cycle(cycle):
    return min(cycle[i:]+cycle[:i] for i in range(len(cycle)))


def all_cycles(vertices, arrows):
    adjacency=defaultdict(set)
    for p,q in arrows: adjacency[p].add(q)
    found=set()
    for start in vertices:
        def visit(path):
            for q in adjacency[path[-1]]:
                if q==start and len(path)>=2: found.add(canonical_cycle(path))
                elif q not in path: visit(path+(q,))
        visit((start,))
    return sorted(found,key=lambda c:(len(c),c))


def exact_solutions_with_mandatory(columns, mandatory):
    """Complete exact 0/1 search for A*x=0 with specified x_j=1.

    Interval propagation is exact because each remaining coordinate is binary;
    every non-forced variable is eventually branched both ways.
    """
    row_count=len(columns[0]); column_count=len(columns)
    row_variables=[[j for j in range(column_count) if columns[j][i]] for i in range(row_count)]
    nodes=0; solutions=[]

    def propagate(assignment):
        assignment=assignment[:]
        while True:
            changed=False
            for i,variables in enumerate(row_variables):
                current=sum(columns[j][i]*assignment[j] for j in variables if assignment[j]>=0)
                unknown=[j for j in variables if assignment[j]<0]
                low=sum(min(0,columns[j][i]) for j in unknown)
                high=sum(max(0,columns[j][i]) for j in unknown)
                if current+low>0 or current+high<0: return None
                forced={}
                if current+low==0:
                    for j in unknown: forced[j]=int(columns[j][i]<0)
                if current+high==0:
                    for j in unknown:
                        value=int(columns[j][i]>0)
                        if j in forced and forced[j]!=value: return None
                        forced[j]=value
                if len(unknown)==1:
                    j=unknown[0]; coefficient=columns[j][i]
                    if (-current)%coefficient: return None
                    value=(-current)//coefficient
                    if value not in (0,1): return None
                    forced[j]=value
                for j,value in forced.items():
                    if assignment[j]>=0 and assignment[j]!=value: return None
                    if assignment[j]<0: assignment[j]=value; changed=True
            if not changed: return assignment

    def search(assignment):
        nonlocal nodes
        nodes += 1
        assignment=propagate(assignment)
        if assignment is None: return
        if all(value>=0 for value in assignment):
            solutions.append(tuple(assignment)); return
        # A deterministic tight-row heuristic; correctness comes from trying
        # both binary values, not from the heuristic.
        best=max(
            (j for j,value in enumerate(assignment) if value<0),
            key=lambda j:sum(
                1/max(1,sum(assignment[k]<0 for k in row_variables[i]))
                for i,c in enumerate(columns[j]) if c
            ),
        )
        for value in (1,0):
            child=assignment[:]; child[best]=value; search(child)

    initial=[-1]*column_count
    for j in mandatory: initial[j]=1
    search(initial)
    return nodes,solutions


def main():
    data=json.loads(DATA.read_text()); left=data["left_blocks"];right=data["right_blocks"]
    blocks=[("L",p,e) for p,e in left]+[("R",p,e) for p,e in right]
    assert all(is_prime(p) and e in (1,2) for _,p,e in blocks)
    k,sk,lf=aggregate(left);m,sm,rf=aggregate(right);n=k*sk
    assert lf==rf and n==m*sm
    assert (k,sk,m,sm,n)==(data["left_input"],data["left_sigma"],data["right_input"],data["right_sigma"],data["common_h"])
    nf=Counter({int(p):e for p,e in data["common_h_factorization"].items()})
    assert lf==nf and math.prod(p**e for p,e in nf.items())==n

    bases={p for _,p,e in blocks}; arrows=set(); realizers=defaultdict(list)
    for j,(_,p,e) in enumerate(blocks):
        for q in factor(sigma_pp(p,e)):
            if q in bases and q!=p: arrows.add((p,q));realizers[p,q].append(j)
    cycles=all_cycles(bases,arrows)
    assert cycles==[tuple(c) for c in data["directed_cycles"]]
    assert min(map(len,cycles))==data["directed_girth"]==10

    # Any nonempty balanced signed subrelation has minimum in-degree one in
    # its in-base sigma graph, hence contains a directed cycle.  Since the
    # full graph has exactly the one cycle above and every edge of that cycle
    # has a unique realizing block, those ten blocks are mandatory.  The
    # following complete exact binary search shows they force all 42 blocks.
    cycle=cycles[0]; mandatory=set()
    for i,p in enumerate(cycle):
        edge=(p,cycle[(i+1)%len(cycle)])
        assert len(realizers[edge])==1
        mandatory.add(realizers[edge][0])
    rows=sorted(nf); columns=[]
    for side,p,e in blocks:
        sign=1 if side=="L" else -1; factors=block_factors(p,e)
        columns.append([sign*factors.get(q,0) for q in rows])
    nodes,solutions=exact_solutions_with_mandatory(columns,mandatory)
    assert nodes==data["atomicity_exact_search_nodes"]==3
    assert len(mandatory)==data["atomicity_cycle_mandatory_columns"]==10
    assert solutions==[(1,)*len(columns)]

    left_f,right_f=Counter(dict(left)),Counter(dict(right));common=left_f&right_f
    assert math.prod(p**e for p,e in common.items())==math.gcd(k,m)==data["gcd"]
    assert common==Counter({int(p):e for p,e in data["gcd_factorization"].items()})
    tests=0
    for choice in itertools.product(*[range(e+1) for e in common.values()]):
        divisor=Counter({p:e for p,e in zip(common,choice) if e})
        if not divisor: continue
        tests+=1
        assert h_from_factors(left_f-divisor)!=h_from_factors(right_f-divisor)
    assert tests==data["nontrivial_common_divisors_checked"]==4095

    print("PASS")
    print(f"K={k}; sigma(K)={sk}")
    print(f"M={m}; sigma(M)={sm}")
    print(f"N={n}")
    print(f"directed_cycles={cycles}; girth=10; arrows={len(arrows)}")
    print(f"atomicity: mandatory={len(mandatory)}, exact_search_nodes={nodes}, only_full_solution=True")
    print(f"gcd={math.gcd(k,m)}; primitive_divisors_tested={tests}")


if __name__=="__main__": main()
