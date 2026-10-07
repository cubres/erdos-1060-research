#!/usr/bin/env python3
"""Exact standard-library verifier for the equal exponent-partition collision."""

from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path

DATA=Path(__file__).parent/'equal_partition_u300.json'

def factor(n):
 out=Counter();d=2
 while d*d<=n:
  while n%d==0:out[d]+=1;n//=d
  d=3 if d==2 else d+2
 if n>1:out[n]+=1
 return out
def prime(n):return factor(n)==Counter({n:1})
def spp(p,e):
 s=sum(p**j for j in range(e+1));assert s==(p**(e+1)-1)//(p-1);return s
def bf(p,e):
 f=Counter({p:e});f.update(factor(spp(p,e)));return f
def agg(B):
 k=math.prod(p**e for p,e in B);s=math.prod(spp(p,e) for p,e in B);f=Counter()
 for p,e in B:f.update(bf(p,e))
 return k,s,f
def h(F):return math.prod(p**e*spp(p,e) for p,e in F.items())
def atom(vectors):
 width=len(vectors);full=(1<<width)-1;bal=defaultdict(int);nz=0;old=0;checked=0
 for i in range(1,1<<width):
  gray=i^(i>>1);change=gray^old;j=change.bit_length()-1;direction=1 if gray&change else -1
  for q,a in vectors[j].items():
   before=bal[q];after=before+direction*a
   if before==0 and after!=0:nz+=1
   elif before!=0 and after==0:nz-=1
   bal[q]=after
  old=gray
  if gray==full:assert nz==0
  else:checked+=1;assert nz!=0,f'proper zero subrelation {gray}'
 return checked

def main():
 D=json.loads(DATA.read_text());L=D['left_blocks'];R=D['right_blocks']
 assert all(prime(p) and e>=1 for p,e in L+R)
 k,sk,lf=agg(L);m,sm,rf=agg(R);n=k*sk
 assert lf==rf and n==m*sm
 assert (k,sk,m,sm,n)==(D['left_input'],D['left_sigma'],D['right_input'],D['right_sigma'],D['common_h'])
 nf=Counter({int(p):e for p,e in D['common_h_factorization'].items()});assert lf==nf;assert math.prod(p**e for p,e in nf.items())==n
 lp=sorted(e for p,e in L);rp=sorted(e for p,e in R)
 assert lp==rp==D['left_invariant']==D['right_invariant']==[1,1,1,1,1,2,2,3,5]
 assert [e for e in lp if e>=2]==[2,2,3,5] and lp.count(1)==rp.count(1)==5
 LF,RF=Counter(dict(L)),Counter(dict(R));common=LF&RF
 assert math.prod(p**e for p,e in common.items())==math.gcd(k,m)==D['gcd']
 assert common==Counter({int(p):e for p,e in D['gcd_factorization'].items()})
 tests=0
 for choice in itertools.product(*[range(e+1) for e in common.values()]):
  d=Counter({p:e for p,e in zip(common,choice) if e})
  if not d:continue
  tests+=1;assert h(LF-d)!=h(RF-d)
 assert tests==D['nontrivial_common_divisors_checked']==143
 vectors=[]
 for sign,B in ((1,L),(-1,R)):
  for p,e in B:vectors.append({q:sign*a for q,a in bf(p,e).items()})
 subsets=atom(vectors);assert subsets==D['proper_signed_subsets_checked']==(1<<18)-2
 print('PASS')
 print(f'K={k}; sigma(K)={sk}; exponents={lp}')
 print(f'M={m}; sigma(M)={sm}; exponents={rp}')
 print(f'N={n}')
 print(f'gcd={math.gcd(k,m)}; primitive_divisors_tested={tests}')
 print(f'signed_blocks={len(vectors)}; proper_subsets_tested={subsets}')
if __name__=='__main__':main()
