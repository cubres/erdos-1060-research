import json
import time
from pathlib import Path
from branch_solver import ExactSolver, BudgetExceeded, prime, target_from_input
import random
A={11:2,13:2,17:1,19:1,31:1,61:1,97:1,127:2,271:1,307:2,331:1,367:1}
qs=[p for p in range(10007,12000) if p%3==2 and prime(p)]
random.seed(1060)
small=[p for p in range(11,251) if prime(p)]
tests=[]
for count in [0,5,10,20,40]:
 f=A.copy();f.update({p:1 for p in qs[:count]})
 tests.append((f'scaled_seed_{count}',f,2))
for i in range(12):
 ps=random.sample(small,12+(i%3)*6)
 E=2+(i%2)
 f={p:random.randint(1,E) for p in ps}
 tests.append((f'represented_random_{i}',f,E))
out=[]
for name,ff,E in tests:
 fact=target_from_input(ff);s=ExactSolver(fact,E,seconds=12,node_limit=2000)
 start=time.monotonic()
 try:r=s.solve()
 except BudgetExceeded:r=s.result(False)
 r['name']=name;r['input_factorization']=ff;r['elapsed_seconds']=time.monotonic()-start
 r['target_digits']=len(str(s.N));out.append(r)
 open(Path(__file__).resolve().parent/'stress_results.json','w').write(json.dumps(out,indent=2)+'\n')
 print(name,r['target_digits'],r['complete'],len(r['solutions']),r['stats']['max_success_depth'],r['stats']['max_success_cost_product'],round(r['elapsed_seconds'],3),flush=True)
