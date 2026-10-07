"""Exact factor/peeling exploration for even input exponents, not a general theorem."""
import json,time,sys,math
from pathlib import Path
from collections import defaultdict
from itertools import combinations
from sympy import primerange,factorint,isprime
BASE=Path(__file__).resolve().parent
P=int(sys.argv[1]) if len(sys.argv)>1 else 5000
cap=int(sys.argv[2]) if len(sys.argv)>2 else 6
small=list(primerange(1,cap+2))
cache=json.loads((BASE/'erdos1060_v5/factor_cache.json').read_text())
outcache=BASE/f'new_even_cache_{P}_{cap}.json'
new=json.loads(outcache.read_text()) if outcache.exists() else {}
cache.update(new)
cols=[];cnt=0;t0=time.monotonic()
for p in primerange(cap+2,P+1):
    local={0:{}}
    for e in range(2,cap+1,2):
        sig=sum(p**i for i in range(e+1))
        if any(sig % q==0 for q in small):continue
        key=f'{p}:{e}'
        if key in cache:d={int(q):int(a) for q,a in cache[key].items()}
        else:
            dd=factorint(sig);d={int(q):int(a) for q,a in dd.items()};d[p]=d.get(p,0)+e
            assert math.prod(q**a for q,a in d.items())==p**e*sig
            assert all(isprime(q) for q in d)
            new[key]={str(q):a for q,a in d.items()}
        local[e]=d
    for b,a in combinations(local,2):
        d={q:local[a].get(q,0)-local[b].get(q,0) for q in local[a].keys()|local[b].keys()}
        d={q:v for q,v in d.items() if v}
        cols.append((p,a,b,d))
    cnt+=1
    if cnt%25==0:
        print('factor',cnt,p,len(new),'seconds',round(time.monotonic()-t0,2),flush=True)
        outcache.write_text(json.dumps(new))
start=len(cols);rounds=[]
while cols:
    owners=defaultdict(set)
    for p,a,b,d in cols:
        for q in d:owners[q].add(p)
    rows={q for q,ps in owners.items() if len(ps)==1}
    keep=[c for c in cols if rows.isdisjoint(c[3])]
    if len(keep)==len(cols):break
    rounds.append(len(cols)-len(keep));cols=keep
result={'upper_input_prime':P,'input_exponents':list(range(0,cap+1,2)),
        'excluded_sigma_primes':small,'initial_columns':start,'rounds':rounds,
        'remaining_columns':cols,'elapsed_seconds':time.monotonic()-t0,
        'note':'Factor primality checked by sympy; no formal certificate, no inference beyond finite range.'}
outcache.write_text(json.dumps(new))
(BASE/f'even_rough_{P}_{cap}.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='remaining_columns'},indent=2),flush=True)
print('remaining',len(cols),cols[:8],flush=True)
