import numpy as np
from scipy.optimize import minimize, minimize_scalar, differential_evolution
from math import log

def colors(a,l):
 out=[]
 for e in range(a+1):
  x=e+1
  while x%l==0:x//=l
  out.append(x)
 vals=sorted(set(out));return np.array([[int(v==c) for v in out] for c in vals])

col={a:(colors(a,2),colors(a,3)) for a in range(1,16)}

def loc(a,t,la):
 M2,M3=col[a];idx=np.arange(a+1)
 def fg(p):
  c2=np.maximum(M2@p,1e-100);c3=np.maximum(M3@p,1e-100)
  val=t*np.dot(c2,np.log(c2))+(1-t)*np.dot(c3,np.log(c3))+la*np.dot(p,idx)
  grad=t*M2.T@(np.log(c2)+1)+(1-t)*M3.T@(np.log(c3)+1)+la*idx
  return val,grad
 res=minimize(fg,np.ones(a+1)/(a+1),jac=True,method='SLSQP',bounds=[(1e-12,1)]*(a+1),constraints={'type':'eq','fun':lambda p:sum(p)-1,'jac':lambda p:np.ones_like(p)},options={'ftol':1e-11,'maxiter':150})
 return -res.fun/a,res.x

def objective(x):
 t,la=x
 return max(loc(a,t,la)[0] for a in range(1,9))+la/2
res=minimize(objective,[.75,.1],method='Nelder-Mead',options={'xatol':1e-8,'fatol':1e-9,'maxiter':200})
print(res.x,res.fun)
for a in range(1,16):
 val,p=loc(a,*res.x);print(a,val,val+res.x[1]/2, np.round(p,6))
