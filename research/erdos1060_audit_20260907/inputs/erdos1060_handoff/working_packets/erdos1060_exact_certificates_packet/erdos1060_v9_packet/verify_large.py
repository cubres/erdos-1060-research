"""Exact noncollision certificate on input primes in [1001, 10**6].
No primality claim for output row bases is required: exact multiplication
and pairwise coprimality certify their multiplicative independence.
"""
from __future__ import annotations
import json,time
from pathlib import Path
from math import gcd,prod
from verify_v9 import sieve,require,sigma_local


def pairwise_coprime(numbers):
    if not numbers:return True
    require(len(set(numbers))==len(numbers),'Repeated factor row')
    require(all(n>=2 for n in numbers),'Nonpositive factor row')
    levels=[list(numbers)]
    while len(levels[-1])>1:
        a=levels[-1]
        levels.append([a[i]*a[i+1] if i+1<len(a) else a[i] for i in range(0,len(a),2)])
    rem=[levels[-1][0]]
    for level in reversed(levels[:-1]):
        rem=[rem[i//2]%(n*n) for i,n in enumerate(level)]
    return all(r%n==0 and gcd(r//n,n)==1 for n,r in zip(numbers,rem))


def check():
    start=time.monotonic();base=Path(__file__).resolve().parent
    raw=json.loads((base/'prime_graph_1000000.json').read_text())
    lo=1001;hi=int(raw['limit'])
    ps=[p for p in sieve(hi) if p>=lo]
    source={int(p):e for p,e in raw['factors'].items() if int(p)>=lo}
    require(sorted(source)==ps,'Input-prime range is incomplete')
    columns=[];rows=set(ps)
    for p in ps:
        local={}
        for e in (1,2):
            f={int(q):int(v) for q,v in source[p][str(e)].items()}
            require(all(q>=2 and v>0 for q,v in f.items()),'Bad output factor')
            require(prod(q**v for q,v in f.items())==sigma_local(p,e),'Wrong local product')
            rows.update(f)
            f[p]=f.get(p,0)+e
            local[e]=f
        columns.append((p,1,0,local[1]))
        columns.append((p,2,0,local[2]))
        diff={q:local[2].get(q,0)-local[1].get(q,0) for q in local[1].keys()|local[2].keys()
              if local[2].get(q,0)!=local[1].get(q,0)}
        columns.append((p,2,1,diff))
    require(pairwise_coprime(sorted(rows)),'Row bases are not multiplicatively independent')
    initial=len(columns);counts=[]
    while columns:
        owners={};shared=set()
        for p,a,b,col in columns:
            for q in col:
                if q in owners:
                    if owners[q]!=p:shared.add(q)
                else:owners[q]=p
        unique=set(owners)-shared
        keep=[col for col in columns if unique.isdisjoint(col[3])]
        if len(keep)==len(columns):break
        counts.append(len(columns)-len(keep));columns=keep
    require(not columns,'Certificate leaves unresolved columns')
    report={'min_input_prime':lo,'max_input_prime':hi,'input_exponent_cap':2,
            'input_prime_count':len(ps),'factor_row_count':len(rows),
            'initial_difference_columns':initial,'round_deletions':counts,
            'remaining_columns':len(columns),'injectivity_certified':True,
            'scope':'Finite allowed prime range, not an asymptotic theorem or an input-size cutoff',
            'elapsed_seconds':time.monotonic()-start}
    (base/'verification_large.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':check()
