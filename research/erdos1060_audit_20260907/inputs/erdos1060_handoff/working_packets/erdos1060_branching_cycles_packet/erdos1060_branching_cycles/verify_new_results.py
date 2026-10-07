"""Independent exact checks for the branching/cycle continuation.
Run from this directory with: python verify_new_results.py
"""
import json
import time
from math import isqrt, prod
from branch_solver import ExactSolver, local_sigma, prime, target_from_input, trial_factors
from graph_analysis import target_graph
from pathlib import Path


def sigma_direct(n):
    total=0
    for d in range(1,isqrt(n)+1):
        if n%d==0:
            total+=d
            if d*d!=n:total+=n//d
    return total


def brute_fiber(fac,E):
    # Every input divides N. Enumerate all divisors under sqrt(N), without propagation.
    N=prod(p**a for p,a in fac.items())
    divs=[1]
    for p,a in fac.items():
        divs=[d*p**e for d in divs for e in range(min(a,E)+1) if d*p**e<=isqrt(N)]
    return sorted(d for d in divs if d*sigma_direct(d)==N)


def geometric_checks():
    # Exhaustively check the small mutual-divisibility assertions in an input-prime window.
    ps=[p for p in range(2,2001) if prime(p)]
    mixed=[];twos=[];triples=[]
    for i,p in enumerate(ps):
        for q in ps[i+1:]:
            if (q+1)%p==0:
                for e in (1,2,3):
                    if local_sigma(p,e)%q==0:
                        mixed.append([p,q,e]);assert q<=7
            if local_sigma(p,2)%q==0 and local_sigma(q,2)%p==0:
                twos.append([p,q]);assert p*p+q*q+p+q+1==5*p*q
    # Root supply lemma: every smaller base has q-adic valuation exactly one.
    roots_checked=0
    for q in ps:
        if q<=3:continue
        roots=[p for p in ps if p<q and local_sigma(p,2)%q==0]
        assert len(roots)<=2
        if len(roots)==2:assert sum(roots)==q-1
        for p in roots:
            assert local_sigma(p,2)%(q*q)!=0
            roots_checked+=1
    return {'prime_cutoff':2000,'small_mixed_pairs':mixed,'quadratic_pairs':twos,'root_incidences':roots_checked}


def main():
    start=time.monotonic();compared=0;pairtargets=0
    for k in range(1,1501):
        ff=trial_factors(k)
        if any(e>2 for e in ff.values()):continue
        nf=target_from_input(ff);s=ExactSolver(nf,2,seconds=5)
        r=s.solve();want=brute_fiber(nf,2);got=list(map(int,r['solutions']))
        assert got==want,(k,got,want)
        assert len(got)<=r['stats']['max_success_cost_product']
        graph=target_graph(s)
        # exact graph bound, before the asymptotic replacement of pair count
        b=graph['long_component_vertices'];c=len(graph['two_cycles'])
        assert len(got)<=9*3**b*2**c
        compared+=1;pairtargets+=len(got)>1
    # Reproduce all recorded large targets. This is a second execution, not a second independent search algorithm.
    result_checks=[]
    for name in ['branch_results.json','stress_results.json']:
        for old in json.load(open(Path(__file__).resolve().parent/name)):
            assert old['complete']
            nf={int(p):a for p,a in old['target_factorization'].items()}
            s=ExactSolver(nf,old['exponent_cap'],seconds=20);new=s.solve()
            assert new['solutions']==old['solutions']
            assert len(new['solutions'])<=new['stats']['max_success_cost_product']
            result_checks.append({'name':old['name'],'multiplicity':len(new['solutions']),
                                 'max_branch_product':new['stats']['max_success_cost_product']})
    out={'all_checks_passed':True,'independent_small_target_checks':compared,
         'checks_with_multiple_solutions':pairtargets,'input_seed_limit':1500,
         'small_check_scope':'For each qualifying seed input, the entire bounded-exponent target fiber was independently enumerated as divisors of N.',
         'large_runs_reproduced':result_checks,'local_lemmas':geometric_checks(),
         'elapsed_seconds':time.monotonic()-start,
         'status':'No unrestricted asymptotic bound has been proved. No originality claim.'}
    (Path(__file__).resolve().parent/'verification_v8.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
