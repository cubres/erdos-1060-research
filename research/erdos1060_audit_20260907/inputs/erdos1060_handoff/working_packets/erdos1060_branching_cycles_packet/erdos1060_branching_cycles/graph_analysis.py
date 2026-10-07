import json
from pathlib import Path
from branch_solver import ExactSolver, local_sigma, target_from_input


def sccs(adj):
    index=0;indices={};low={};stack=[];on=set();out=[]
    def visit(v):
        nonlocal index
        indices[v]=low[v]=index;index+=1;stack.append(v);on.add(v)
        for w in sorted(adj[v]):
            if w not in indices:visit(w);low[v]=min(low[v],low[w])
            elif w in on:low[v]=min(low[v],indices[w])
        if low[v]==indices[v]:
            component=[]
            while True:
                w=stack.pop();on.remove(w);component.append(w)
                if w==v:break
            out.append(sorted(component))
    for v in sorted(adj):
        if v not in indices:visit(v)
    return sorted(out,key=lambda c:(-len(c),c))


def target_graph(solver):
    assert solver.E==2
    inds=[i for i,p in enumerate(solver.primes) if p>3 and any(e>0 for e,vec in solver.options[i])]
    vertex={solver.primes[i] for i in inds}
    adj={p:set() for p in vertex}
    for i in inds:
        p=solver.primes[i]
        for e,vs in solver.options[i]:
            if e==0:continue
            for q,v in zip(solver.primes,vs):
                if q!=p and q in vertex and v:adj[p].add(q)
    comps=sccs(adj)
    large=[c for c in comps if len(c)>=3]
    pairs=[c for c in comps if len(c)==2]
    for p,q in pairs:
        assert local_sigma(p,2)%q==0 and local_sigma(q,2)%p==0
        assert 5*p*q==p*p+q*q+p+q+1
    r=len(pairs)
    # Disjoint pairs give stronger inequalities, but this elementary integer bound suffices.
    assert 2**(r*(r+1))<=solver.N
    return {'vertices':len(vertex),'components':comps,'long_component_vertices':sum(map(len,large)),
            'two_cycles':pairs,'arcs':{str(p):sorted(qs) for p,qs in sorted(adj.items())}}


if __name__=='__main__':
    data=json.load(open(Path(__file__).resolve().parent/'branch_results.json'))
    out=[]
    for r in data:
        fs={int(p):e for p,e in r['target_factorization'].items()}
        s=ExactSolver(fs,2)
        g=target_graph(s);g['name']=r['name'];out.append(g)
        print(r['name'],g['vertices'],[len(c) for c in g['components']],g['long_component_vertices'],g['two_cycles'])
    # Source case with a genuine quadratic two-cycle but a forced outgoing valuation.
    ff=target_from_input({13:1,61:2});s=ExactSolver(ff,2)
    g=target_graph(s);g['name']='two_cycle_example';out.append(g)
    print(g['name'],g['components'],s.solve()['solutions'])
    open(Path(__file__).resolve().parent/'graph_results.json','w').write(json.dumps(out,indent=2)+'\n')
