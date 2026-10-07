from functools import lru_cache
from collections import defaultdict
from sympy import factorint, primerange

@lru_cache(None)
def prime_coordinate(p):
    if p==2:return {2:-1,3:1}
    if p==3:return {2:2,3:-1}
    ans=defaultdict(int,{p:1})
    for q,v in factorint(p+1).items():
        for r,w in prime_coordinate(int(q)).items():ans[r]-=int(v)*w
    return {r:w for r,w in ans.items() if w}

def block_coordinate(p,e):
    ans=defaultdict(int)
    for q,v in factorint(p**e*((p**(e+1)-1)//(p-1))).items():
        for r,w in prime_coordinate(int(q)).items():ans[r]+=int(v)*w
    return {r:w for r,w in ans.items() if w}

if __name__=='__main__':
    ps=list(map(int,primerange(5,10000)))
    bad=[]
    for p in ps:
        c=block_coordinate(p,2)
        if c.get(p)!=2:bad.append((p,c.get(p),c))
    print('Non-2 diagonals',len(bad),bad[:10])
