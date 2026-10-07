"""Exact single-row-support propagation for h(k)=k*sigma(k).
No floating point, SAT solver, or unproved pruning rule is used.
"""
from __future__ import annotations
from math import prod, isqrt
from typing import Iterable
import json,time
from pathlib import Path


def prime(n: int)->bool:
    if n<2:return False
    if n%2==0:return n==2
    return all(n%d for d in range(3,isqrt(n)+1,2))


def trial_factors(n: int)->dict[int,int]:
    out={};p=2
    while p*p<=n:
        if n%p==0:
            e=0
            while n%p==0:n//=p;e+=1
            out[p]=e
        p=3 if p==2 else p+2
    if n>1:out[n]=1
    return out


def local_sigma(p:int,e:int)->int:
    return (p**(e+1)-1)//(p-1)


def target_from_input(fac:dict[int,int])->dict[int,int]:
    out={}
    for p,e in fac.items():
        assert prime(p) and e>=0
        out[p]=out.get(p,0)+e
        for q,v in trial_factors(local_sigma(p,e)).items():out[q]=out.get(q,0)+v
    return {p:e for p,e in out.items() if e}


class BudgetExceeded(RuntimeError):pass


class ExactSolver:
    def __init__(self, factors:dict[int,int], E:int|None=None, node_limit:int=10000, seconds:float=30):
        if not all(isinstance(p,int) and isinstance(e,int) and prime(p) and e>0 for p,e in factors.items()):
            raise ValueError('factors must be a prime factorization with positive integer exponents')
        if E is not None and (not isinstance(E,int) or E<0):
            raise ValueError('E must be a nonnegative integer or None')
        if node_limit<1 or seconds<=0:
            raise ValueError('node_limit and seconds must be positive')
        self.primes=tuple(sorted(factors));self.alpha=tuple(factors[p] for p in self.primes)
        self.N=prod(p**e for p,e in factors.items());self.E=E
        self.options=[]
        for p,a in zip(self.primes,self.alpha):
            options=[]
            for e in range(min(a,E) +1 if E is not None else a+1):
                x=p**e*local_sigma(p,e)
                if self.N%x:continue
                rem=x;vv=[]
                for q in self.primes:
                    v=0
                    while rem%q==0:rem//=q;v+=1
                    vv.append(v)
                assert rem==1
                options.append((e,tuple(vv)))
            self.options.append(tuple(options))
        self.start=tuple(tuple(range(len(opts))) for opts in self.options)
        self.limit=node_limit;self.deadline=time.monotonic()+seconds
        self.stats={'nodes':0,'propagation_calls':0,'support_tests':0,'options_pruned':0,
                    'lookahead_rejections':0,'branch_nodes':0,'max_success_depth':0,
                    'max_success_cost_product':1,'max_success_branches':[], 'leaves':0}
        self.solutions=[]

    def check_budget(self):
        if self.stats['nodes']>self.limit or time.monotonic()>self.deadline:raise BudgetExceeded

    @staticmethod
    def sumset(S:set[int],values:Iterable[int],cap:int)->set[int]:
        V=set(values)
        return {s+v for s in S for v in V if s+v<=cap}

    def propagate(self,state):
        self.stats['propagation_calls']+=1
        ds=[list(s) for s in state]
        changed=True
        while changed:
            self.check_budget();changed=False
            for q,alpha in enumerate(self.alpha):
                # Only variables that have a nonzero possible contribution need enter this row.
                active=[i for i,d in enumerate(ds) if any(self.options[i][o][1][q] for o in d)]
                values=[{self.options[i][o][1][q] for o in ds[i]} for i in active]
                prefix=[{0}]
                for v in values:prefix.append(self.sumset(prefix[-1],v,alpha))
                if alpha not in prefix[-1]:return None
                suffix=[set() for _ in range(len(active)+1)];suffix[-1]={0}
                for t in range(len(active)-1,-1,-1):suffix[t]=self.sumset(suffix[t+1],values[t],alpha)
                for t,i in enumerate(active):
                    if len(ds[i])==1:continue
                    others={a+b for a in prefix[t] for b in suffix[t+1] if a+b<=alpha}
                    kept=[o for o in ds[i] if alpha-self.options[i][o][1][q] in others]
                    self.stats['support_tests']+=len(ds[i])
                    if not kept:return None
                    if len(kept)<len(ds[i]):
                        self.stats['options_pruned']+=len(ds[i])-len(kept)
                        ds[i]=kept;changed=True
        return tuple(tuple(d) for d in ds)

    def solve(self):
        self._visit(self.start,[],1)
        self.solutions.sort()
        assert len(self.solutions)==len(set(self.solutions))
        return self.result(True)

    def result(self,complete:bool):
        return {'complete':complete,'target':str(self.N),'target_factorization':dict(zip(self.primes,self.alpha)),
                'exponent_cap':self.E,'initial_options':{str(p):[self.options[i][o][0] for o in self.start[i]] for i,p in enumerate(self.primes)},
                'solutions':[str(x) for x in sorted(self.solutions)],'stats':self.stats}

    def _visit(self,state,path,cost):
        self.stats['nodes']+=1;self.check_budget()
        state=self.propagate(state)
        if state is None:return
        while True:
            ambiguous=[i for i,d in enumerate(state) if len(d)>1]
            if not ambiguous:
                exps=[self.options[i][d[0]][0] for i,d in enumerate(state)]
                k=prod(p**e for p,e in zip(self.primes,exps))
                sig=prod(local_sigma(p,e) for p,e in zip(self.primes,exps))
                assert k*sig==self.N
                self.solutions.append(k);self.stats['leaves']+=1
                self.stats['max_success_depth']=max(self.stats['max_success_depth'],len(path))
                if cost>self.stats['max_success_cost_product']:
                    self.stats['max_success_cost_product']=cost;self.stats['max_success_branches']=path
                return
            candidates=[];restart=False
            for i in ambiguous:
                children=[]
                for o in state[i]:
                    candidate=list(state);candidate[i]=(o,)
                    propagated=self.propagate(tuple(candidate))
                    if propagated is not None:children.append((o,propagated))
                    else:self.stats['lookahead_rejections']+=1
                if len(children)<len(state[i]):
                    if not children:return
                    changed=list(state);changed[i]=tuple(o for o,_ in children)
                    state=self.propagate(tuple(changed))
                    if state is None:return
                    restart=True;break
                # Public, deterministic choice. No completed-fiber data enters the score.
                score=(max(sum(len(d)>1 for d in child) for _,child in children),
                       sum(sum(len(d)-1 for d in child) for _,child in children),
                       len(children),self.primes[i])
                candidates.append((score,i,children))
            if restart:continue
            _,i,children=min(candidates,key=lambda t:t[0]);break
        self.stats['branch_nodes']+=1
        branches=len(children)
        for o,child in children:
            step={'prime':self.primes[i],'exponent':self.options[i][o][0],'arity':branches}
            self._visit(child,path+[step],cost*branches)

if __name__=='__main__':
    A={11:2,13:2,17:1,19:1,31:1,61:1,97:1,127:2,271:1,307:2,331:1,367:1}
    B={13:1,17:2,19:2,23:1,31:2,43:1,61:2,83:1,127:1,307:1,733:1,5419:1}
    M=target_from_input(A);assert M==target_from_input(B)
    targets=[('small',target_from_input({2:2,3:1}),2),('big_cubefree',M,2),('big_full',M,None)]
    scaled=M.copy()
    for p,e in trial_factors(336).items():scaled[p]=scaled.get(p,0)+e
    targets.extend([('scaled_cubefree',scaled,2),('scaled_full',scaled,None),
                    ('seven_full',{2:28,3:3,5:1,7:1,13:1,31:1,127:1,8191:1},None)])
    out=[]
    for name,target,E in targets:
        s=ExactSolver(target,E,seconds=30);start=time.monotonic()
        try:result=s.solve()
        except BudgetExceeded:result=s.result(False)
        result['name']=name;result['elapsed_seconds']=time.monotonic()-start
        out.append(result)
        print(name,result['complete'],len(result['solutions']),result['stats'],flush=True)
        open(Path(__file__).resolve().parent/'branch_results.json','w').write(json.dumps(out,indent=2)+'\n')
