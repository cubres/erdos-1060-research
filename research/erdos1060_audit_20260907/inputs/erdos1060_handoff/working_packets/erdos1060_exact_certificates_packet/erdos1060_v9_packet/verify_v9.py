"""Check exact certificates for a partial investigation of Erdos Problem 1060.

Uses Python's standard library only. No solver status, floating-point rank,
probable-prime test, or known list of preimages is used to prove completeness.
This does not certify the asymptotic conjecture.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from math import isqrt, prod
from pathlib import Path
import json
import time


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sieve(n: int) -> list[int]:
    flags = bytearray(b'\1') * (n + 1)
    if n >= 0: flags[0] = 0
    if n >= 1: flags[1] = 0
    for p in range(2, isqrt(n) + 1):
        if flags[p]: flags[p*p:n+1:p] = b'\0' * ((n-p*p)//p + 1)
    return [p for p in range(2, n+1) if flags[p]]


def prime(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    return all(n % d for d in range(3, isqrt(n)+1, 2))


def sigma_local(p: int, e: int) -> int:
    # Addition, rather than the division formula used in certificate discovery.
    return sum(p**j for j in range(e+1))


def vector(n: int, primes: list[int]) -> tuple[int, ...]:
    values = []
    for p in primes:
        v = 0
        while n % p == 0:
            n //= p
            v += 1
        values.append(v)
    require(n == 1, 'Local block contains a prime outside the target')
    return tuple(values)


def local_model(factors: dict[int, int], cap: int):
    require(all(prime(p) and isinstance(e,int) and e>0 for p,e in factors.items()),
            'Invalid target factorization')
    primes = sorted(factors)
    alpha = [factors[p] for p in primes]
    target = prod(p**factors[p] for p in primes)
    domains = []
    vectors = {}
    for p in primes:
        domain = []
        for e in range(min(cap, factors[p])+1):
            block = p**e * sigma_local(p,e)
            if target % block == 0:
                domain.append(e)
                vectors[p,e] = vector(block,primes)
        domains.append(domain)
    return primes,alpha,target,domains,vectors


def propagate(primes, alpha, domains, vectors):
    """Independent exact single-row support elimination.

    A deletion is made only if no sum from the other variables' CURRENT
    domains can complete that one integer valuation equation.
    """
    ds = [list(d) for d in domains]
    deletions = 0
    rounds = 0
    while True:
        changed = False
        rounds += 1
        for r,capacity in enumerate(alpha):
            for i,p in enumerate(primes):
                sums = {0}
                for j,q in enumerate(primes):
                    if i == j: continue
                    vals = {vectors[q,e][r] for e in ds[j]}
                    sums = {a+b for a in sums for b in vals if a+b <= capacity}
                keep = [e for e in ds[i] if capacity-vectors[p,e][r] in sums]
                require(bool(keep), 'Propagation proves this target infeasible')
                if keep != ds[i]:
                    deletions += len(ds[i])-len(keep)
                    ds[i] = keep
                    changed = True
        if not changed: return ds,deletions,rounds


def rref(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a: return a,[]
    rank = 0
    pivots = []
    for c in range(len(a[0])):
        pivot = next((i for i in range(rank,len(a)) if a[i][c]),None)
        if pivot is None: continue
        a[rank],a[pivot] = a[pivot],a[rank]
        v = a[rank][c]
        a[rank] = [x/v for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][c]:
                v = a[i][c]
                a[i] = [x-v*y for x,y in zip(a[i],a[rank])]
        pivots.append(c)
        rank += 1
        if rank == len(a): break
    return a,pivots


def solve_unique(rows, rhs):
    n = len(rows[0])
    red,pivots = rref([list(row)+[b] for row,b in zip(rows,rhs)])
    require(n not in pivots,'Inconsistent affine system')
    require(len(pivots)==n,'System is not uniquely determined')
    answer = [Fraction(0)]*n
    for i,p in enumerate(pivots): answer[p]=red[i][-1]
    require(all(sum(Fraction(c)*x for c,x in zip(row,answer))==b
                for row,b in zip(rows,rhs)), 'Linear solve failed')
    return answer


def divisor_sum(factors: dict[int,int]):
    divisors = [1]
    for p,e in factors.items():
        divisors = [d*p**j for d in divisors for j in range(e+1)]
    require(len(set(divisors))==len(divisors),'Repeated divisor')
    return sum(divisors),len(divisors)


def check_dual(path: Path):
    c = json.loads(path.read_text())
    factors = {int(p):int(e) for p,e in c['target_factorization'].items()}
    primes,alpha,target,domains,vectors = local_model(factors,c['cap'])
    initial = sum(map(len,domains))
    ds,removed,rounds = propagate(primes,alpha,domains,vectors)
    desc = [(p,e) for p,domain in zip(primes,ds) for e in domain]
    require(desc==[tuple(v) for v in c['propagated_options']],
            'Independently propagated domains differ from certificate')
    cols = [list(vectors[p,e])+[int(p==q) for q in primes] for p,e in desc]
    rhs = alpha+[1]*len(primes)
    prices = c['dual_prices']+c['block_offsets']
    require(all(isinstance(v,int) for v in prices),'Prices must be exact integers')
    scores = [sum(v*w for v,w in zip(prices,col)) for col in cols]
    require(scores==c['scores'],'Incorrect score list')
    require(min(scores)>=0,'Negative score')
    require(sum(v*w for v,w in zip(prices,rhs))==0,'Nonzero target budget')
    keep = [j for j,x in enumerate(scores) if x==0]
    kept_desc = [desc[j] for j in keep]
    require(kept_desc==[tuple(v) for v in c['remaining_options']],
            'Incorrect retained options')
    rows = [[cols[j][i] for j in keep] for i in range(len(rhs))]
    _,pivots = rref(rows)
    rank = len(pivots)
    require(rank==c['rank']==len(keep)-1,'Residual nullity is not one')
    free = kept_desc.index(tuple(c['free_option']))
    free_row = [int(i==free) for i in range(len(keep))]
    answers = []
    for t in (0,1):
        x = solve_unique(rows+[free_row],rhs+[t])
        require(all(v in (0,1) for v in x),'Not a binary assignment')
        fs = {p:e for (p,e),value in zip(kept_desc,x) if value and e}
        k = prod(p**e for p,e in fs.items())
        sig,count = divisor_sum(fs)
        require(k*sig==target,'Divisor-summation witness check failed')
        answers.append({'indicator':t,'input':str(k),'divisor_count':count})
    claimed = {v['input'] for v in c['solutions']}
    require({v['input'] for v in answers}==claimed,'Witness list differs')
    return {'target':str(target),'cap':c['cap'],'initial_options':initial,
            'propagation_deletions':removed,'propagation_rounds':rounds,
            'propagated_options':len(desc),'dual_removed':len(desc)-len(keep),
            'retained_options':len(keep),'rank':rank,'nullity':len(keep)-rank,
            'free_indicator':list(c['free_option']),'complete_fiber':answers,
            'completeness':'Exact propagation, nonnegative integer dual scores, rank and two endpoint checks'}


def check_dense(path: Path):
    results = []
    for case in json.loads(path.read_text()):
        factors = {int(p):int(e) for p,e in case['target_factorization'].items()}
        fs = {int(p):int(e) for p,e in case['input'].items()}
        ps,alpha,N,ds,vs = local_model(factors,2)
        require(prod(p**e*sigma_local(p,e) for p,e in fs.items())==N,
                'Dense test witness is invalid')
        ds,deleted,rounds = propagate(ps,alpha,ds,vs)
        require(all(len(d)==1 for d in ds),'Dense test not forced by propagation')
        require({p:d[0] for p,d in zip(ps,ds) if d[0]}==fs,
                'Forced assignment differs from witness')
        results.append({'prime_cutoff':case['cutoff'],'target_digits':len(str(N)),
                        'cap':2,'complete_multiplicity':1,'deletions':deleted})
    return results


def check_graph(path: Path):
    data = json.loads(path.read_text())
    bound = int(data['limit'])
    prime_list = sieve(bound)
    allowed = [p for p in prime_list if p>3]
    facts = {int(p):{int(e):{int(q):int(v) for q,v in f.items()}
                    for e,f in blocks.items()}
             for p,blocks in data['factors'].items()}
    require(sorted(facts)==allowed,'Not the complete specified input prime range')
    output_factors = set(q for blocks in facts.values() for f in blocks.values() for q in f)
    small_primes = sieve(isqrt(max(output_factors)))
    for q in output_factors:
        require(q>=2 and all(q==p or q%p for p in small_primes if p*p<=q),
                'A supplied output factor is composite')
    S=set(allowed);adj={};linear={};quad={}
    for p in allowed:
        require(set(facts[p])=={1,2},'Missing exponent block')
        for e in (1,2):
            require(all(v>0 for v in facts[p][e].values()),'Invalid valuation')
            require(prod(q**v for q,v in facts[p][e].items())==sigma_local(p,e),
                    'Incorrect local factorization')
        linear[p]={q for q in facts[p][1] if q in S}
        quad[p]={q for q in facts[p][2] if q in S}
        adj[p]=linear[p]|quad[p]
    pos={p:i for i,p in enumerate(allowed)}
    descendants={}
    for p in allowed:
        bits=0
        for q in linear[p]:
            require(q<p,'Linear edge is not decreasing')
            bits|=(1<<pos[q])|descendants[q]
        descendants[p]=bits
    checked=0
    for p in allowed:
        for q in quad[p]:
            require(not (descendants[q]>>pos[p])&1,'One-quadratic cycle detected')
            checked+=1
    triangles=set()
    for p in allowed:
        for q in adj[p]:
            for r in adj[q]:
                if r!=p and p in adj[r]:
                    tr=(p,q,r)
                    triangles.add(min(tr,tr[1:]+tr[:1],tr[2:]+tr[:2]))
    result=[]
    for tr in sorted(triangles):
        types=[2 if tr[(i+1)%3] in quad[tr[i]] else 1 for i in range(3)]
        require(types.count(2)>=2,'Forbidden triangle')
        result.append({'primes':tr,'edge_types':types})
    return {'prime_cutoff':bound,'prime_count':len(allowed),
            'quadratic_edges_checked':checked,'triangles':result,
            'scope':'Complete finite prime range only; not a global classification'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-graph',action='store_true')
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('verification_v9.json'))
    args=parser.parse_args()
    base=Path(__file__).resolve().parent
    start=time.monotonic()
    report={'status':'Partial results only; the unrestricted conjecture is not proved',
            'dual':check_dual(base/'dual_certificate.json'),
            'dense_targets':check_dense(base/'dense_probes.json')}
    if not args.skip_graph: report['finite_graph']=check_graph(base/'prime_graph_100000.json')
    report['elapsed_seconds']=round(time.monotonic()-start,4)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
