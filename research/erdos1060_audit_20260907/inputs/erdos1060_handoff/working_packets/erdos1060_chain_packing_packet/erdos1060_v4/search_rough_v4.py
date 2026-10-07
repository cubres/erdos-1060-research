"""Numerical collision discovery; exact arithmetic certifies only found witnesses."""
from pathlib import Path
import json, math, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
raw=json.load(open(Path(__file__).with_name('rough_columns.json')))
cols=[(p,a,b,{int(q):v for q,v in d.items()}) for p,a,b,d in raw['cols']]
qs=sorted({q for _,_,_,d in cols for q in d});ps=sorted({p for p,_,_,_ in cols})
qi={q:i for i,q in enumerate(qs)};pi={p:i for i,p in enumerate(ps)}
variables=[];rr=[];cc=[];dd=[]
for p,a,b,d in cols:
 for sign in (1,-1):
  j=len(variables);variables.append((p,a,b) if sign==1 else (p,b,a))
  for q,v in d.items():rr.append(qi[q]);cc.append(j);dd.append(sign*v)
  rr.extend([len(qs)+pi[p],len(qs)+len(ps)]);cc.extend([j,j]);dd.extend([1,1])
mat=coo_matrix((dd,(rr,cc)),shape=(len(qs)+len(ps)+1,len(variables))).tocsc()
lb=np.r_[np.zeros(len(qs)),np.zeros(len(ps)),1];ub=np.r_[np.zeros(len(qs)),np.ones(len(ps)),np.inf]
start=time.monotonic()
res=milp(np.zeros(len(variables)),integrality=np.ones(len(variables)),bounds=Bounds(0,1),constraints=LinearConstraint(mat,lb,ub),options={'time_limit':12,'mip_rel_gap':0.05,'threads':1})
out={'status':int(res.status),'message':str(res.message),'elapsed_seconds':time.monotonic()-start,'input_prime_bounds':[101,100000],'number_variables':len(variables),'model_note':'A solver status is not an exact infeasibility certificate.'}
if res.x is not None:
 chosen=[t for t,x in zip(variables,res.x) if x>.5];a=math.prod(p**e for p,e,f in chosen);b=math.prod(p**f for p,e,f in chosen)
 h=lambda p,e:p**e*sum(p**i for i in range(e+1))
 ha=math.prod(h(p,e) for p,e,f in chosen);hb=math.prod(h(p,f) for p,e,f in chosen)
 out.update(chosen=chosen,a=str(a),b=str(b),target=str(ha),exact_valid=(ha==hb and a!=b and len(set(p for p,e,f in chosen))==len(chosen)),roughness_ratio=min(p for p,e,f in chosen)/math.log(ha),support=len(chosen))
Path(__file__).with_name('rough_search_v4_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
