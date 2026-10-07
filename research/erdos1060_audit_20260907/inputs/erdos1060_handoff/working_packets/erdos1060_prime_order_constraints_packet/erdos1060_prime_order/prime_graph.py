"""Exact universal divisor-sum graph, using roots modulo sieved primes."""
from math import isqrt
from collections import deque

def prime_sieve(n):
 b=bytearray(b'\x01')*(n+1)
 if n>=0:b[0]=0
 if n>=1:b[1]=0
 for p in range(2,isqrt(n)+1):
  if b[p]:b[p*p:n+1:p]=b'\x00'*((n-p*p)//p+1)
 return b,[p for p in range(2,n+1) if b[p]]

def pdivisors(n):
 ans=[];d=2
 while d*d<=n:
  if n%d==0:
   ans.append(d)
   while n%d==0:n//=d
  d+=1
 if n>1:ans.append(n)
 return ans

def roots_order(q,d):
 assert (q-1)%d==0
 fac=pdivisors(d)
 for a in range(2,q):
  r=pow(a,(q-1)//d,q)
  if pow(r,d,q)==1 and all(pow(r,d//l,q)!=1 for l in fac):
   from math import gcd
   return [pow(r,j,q) for j in range(1,d) if gcd(j,d)==1]
 raise AssertionError((q,d))

def graph(X,E,exclude=()):
 flags,ps=prime_sieve(X); exc=set(exclude)
 ps=[p for p in ps if p not in exc]; S=set(ps)
 G={p:set() for p in ps}
 for q in ps:
  roots=set([1]) if q<=E+1 else set()
  for d in range(2,E+2):
   if (q-1)%d==0:roots.update(roots_order(q,d))
  for r in roots:
   for p in range(r,X+1,q):
    if flags[p] and p in S:G[p].add(q)
 return G

def topo(G,removed=()):
 removed=set(removed);deg={p:0 for p in G if p not in removed}
 for p in deg:
  for q in G[p]:
   if q in deg:deg[q]+=1
 que=deque(p for p in deg if deg[p]==0);order=[]
 while que:
  p=que.popleft();order.append(p)
  for q in G[p]:
   if q not in deg:continue
   deg[q]-=1
   if not deg[q]:que.append(q)
 return order if len(order)==len(deg) else None

