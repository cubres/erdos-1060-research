"""Exact certificate checker. Python standard library only.

Reconstructs graphs from modular roots, not previously factored divisor sums.
The output proves finite graph assertions only, not an asymptotic estimate.
"""
from collections import deque
from math import gcd, isqrt, prod
from pathlib import Path
import json
from prime_graph import graph, prime_sieve, topo

BASE=Path(__file__).resolve().parent

def sigma_power(p,e):
    return sum(p**j for j in range(e+1))

def check_blocks(G,removed,blocks):
    removed=set(removed)
    assert removed <= G.keys()
    live=set(G)-removed
    owner={p:p for p in live}
    seen=set()
    for B in blocks:
        B=set(B);assert len(B)>=2 and B<=live and not B&seen
        seen.update(B);label=min(B)
        for p in B:owner[p]=label
        # The only internal cycle is an odd all-quadratic cycle, or a pair.
        incoming={p:0 for p in B}
        for p in B:
            out=G[p]&B
            assert len(out)==1
            q=next(iter(out));incoming[q]+=1
            assert sigma_power(p,2)%q==0 and (p+1)%q!=0
        assert all(v==1 for v in incoming.values())
        p=next(iter(B));walk=set()
        while p not in walk:
            walk.add(p);p=next(iter(G[p]&B))
        assert walk==B
        assert len(B)==2 or len(B)%2==1
    contracted={owner[p]:set() for p in live}
    for p in live:
        for q in G[p]:
            if q in live and owner[q]!=owner[p]:contracted[owner[p]].add(owner[q])
    assert topo(contracted) is not None
    return len(contracted)

def trial_prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))

checks={'status':'finite certificates only; no uniform growth bound proved'}
# Independent direct divisibility comparison at several exponent caps.
small=[]
for E in range(1,7):
    G=graph(500,E)
    for p in G:
        exact={q for q in G if p!=q and any(sigma_power(p,e)%q==0 for e in range(1,E+1))}
        assert G[p]==exact
    small.append({'cap':E,'cutoff':500,'vertices':len(G),'edges':sum(map(len,G.values()))})
checks['direct_small_graph_comparisons']=small

cert=json.loads((BASE/'certificates.json').read_text())
results=[]
for C in cert['cap_two_positive_certificates']:
    X=C['X'];G=graph(X,2,exclude=(2,3))
    S=C['positive_long_cycle_transversal'];blocks=C['remaining_cyclic_components']
    n=check_blocks(G,S,blocks)
    pairs=[B for B in blocks if len(B)==2]
    assert pairs==[[13,61]]
    # Selecting a vertex from the remaining pair removes all positive cycles;
    # odd all-quadratic cycles are permitted to remain.
    results.append({'cap':2,'cutoff':X,'vertices_above_3':len(G),
        'edges_above_3':sum(map(len,G.values())),
        'long_positive_transversal_size':len(S),
        'all_positive_transversal_upper_bound':len(S)+3,
        'remaining_components':blocks,'contracted_vertices':n,
        'finite_fiber_bound':'18 * 3^'+str(len(S))})
checks['cap_two_certificates']=results
results=[]
for C in cert['higher_cap_acyclic_certificates']:
    G=graph(C['X'],C['E']);S=C['feedback_vertices']
    assert topo(G,S) is not None
    results.append({'cap':C['E'],'cutoff':C['X'],'vertices':len(G),
        'edges':sum(map(len,G.values())),'all_cycle_transversal_size':len(S)})
checks['higher_cap_certificates']=results

cycle=[2179,226201,49831,6229,4021,2011,14821,14389,4357]
assert all(trial_prime(p) for p in cycle)
assert min(cycle)**2>max(cycle)
C=[];sign=1
for p,q in zip(cycle,cycle[1:]+cycle[:1]):
    if (p+1)%q==0:
        label='linear';quotient=(p+1)//q;edge_sign=1
    else:
        assert sigma_power(p,2)%q==0
        label='quadratic';quotient=sigma_power(p,2)//q;edge_sign=-1
    sign*=edge_sign
    C.append({'p':p,'q':q,'type':label,'quotient':quotient,'selected_sign':edge_sign})
assert sign==1
checks['positive_cycle_avoiding_sqrt_cutoff']={'vertices':cycle,'edges':C,
    'min_squared':min(cycle)**2,'max_vertex':max(cycle),
    'scope':'universal graph, not a claimed collision'}

k=(29*37*67)**2
N=prod(p**2*sigma_power(p,2) for p in (29,37,67))
factors={3:2,7:3,13:1,29:2,31:1,37:2,67:4}
assert all(trial_prime(p) for p in factors)
assert N==prod(p**e for p,e in factors.items())
assert N==k*prod(sigma_power(p,2) for p in (29,37,67))
checks['sharp_largest_prime_cap_two']={'k':k,'N':N,'target_factors':factors,'largest_prime_exponent':4}
(BASE/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
