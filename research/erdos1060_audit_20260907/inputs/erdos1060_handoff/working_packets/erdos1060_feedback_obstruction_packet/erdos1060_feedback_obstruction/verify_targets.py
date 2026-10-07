#!/usr/bin/env python3
"""Independently repeat exact domain propagation for five represented targets.

No optimizer and no search cutoff are used. At every deletion a local option
fails an exact necessary single-row sumset test. At termination every domain
must be a singleton. The first target is separately checked by enumerating all
its divisors without an exponent cap.
"""
from __future__ import annotations
import json
from pathlib import Path
from math import isqrt, prod


def prime(n: int) -> bool:
    if n<2:return False
    if n%2==0:return n==2
    return all(n%d for d in range(3,isqrt(n)+1,2))


def sigma(p: int, e: int) -> int:
    return sum(p**j for j in range(e+1))


def valuation(n: int, p: int) -> int:
    v=0
    while n%p==0:n//=p;v+=1
    return v


def run() -> dict:
    base=Path(__file__).resolve().parent
    given=json.loads((base/'target_results.json').read_text())
    out=[]
    for record in given:
        target=int(record['target'])
        factor={int(p):e for p,e in record['target_factorization'].items()}
        seed={int(p):e for p,e in record['input_factorization'].items()}
        assert all(prime(p) and e>0 for p,e in factor.items())
        assert prod(p**e for p,e in factor.items())==target
        seed_k=prod(p**e for p,e in seed.items())
        assert seed_k*prod(sigma(p,e) for p,e in seed.items())==target
        ps=sorted(factor)
        domains={p:[e for e in range(min(5,factor[p])+1)
                    if target%(p**e*sigma(p,e))==0] for p in ps}
        columns={(p,e):[valuation(p**e*sigma(p,e),q) for q in ps]
                 for p in ps for e in domains[p]}
        initial=sum(map(len,domains.values()))
        rounds=0
        while True:
            rounds+=1; deleted=0
            for row,q in enumerate(ps):
                alpha=factor[q]
                active=[p for p in ps if any(columns[p,e][row] for e in domains[p])]
                for p in active:
                    if len(domains[p])==1:continue
                    possible={0}
                    for other in active:
                        if other==p:continue
                        values={columns[other,e][row] for e in domains[other]}
                        possible={a+b for a in possible for b in values if a+b<=alpha}
                    old=domains[p]
                    domains[p]=[e for e in old if alpha-columns[p,e][row] in possible]
                    assert domains[p], 'Unexpected empty domain'
                    deleted+=len(old)-len(domains[p])
            if not deleted:break
        assert all(len(domain)==1 for domain in domains.values())
        forced={p:domains[p][0] for p in ps if domains[p][0]}
        assert forced==seed
        assert prod(p**e for p,e in forced.items())*prod(sigma(p,e) for p,e in forced.items())==target
        out.append({'pair_count':record['pair_count'],'target_digits':len(str(target)),
                    'initial_options':initial,'remaining_options':len(ps),
                    'deletion_rounds_including_final_check':rounds,
                    'complete_cap5_multiplicity':1,'branching_used':False})
    first=given[0]
    N=int(first['target'])
    fac={int(p):e for p,e in first['target_factorization'].items()}
    possibilities=[(1,1)]
    for p,e in fac.items():
        possibilities=[(k*p**j,s*sigma(p,j)) for k,s in possibilities for j in range(e+1)]
    answers=[k for k,s in possibilities if k*s==N]
    assert answers==[int(first['intended_input'])]
    seed={int(p):e for p,e in first['input_factorization'].items()}
    divisors=[1]
    for p,e in seed.items():divisors=[d*p**j for d in divisors for j in range(e+1)]
    assert sum(divisors)*answers[0]==N
    result={'complete_selected_cap5_fibers':out,
            'first_target_unrestricted_divisor_enumeration':{
                'target':str(N),'target_divisors_examined':len(possibilities),
                'answers':[str(k) for k in answers],
                'input_divisors_directly_summed':len(divisors)}}
    (base/'target_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':print(json.dumps(run(),indent=2))
