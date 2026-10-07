#!/usr/bin/env python3
"""Exact checks for the v4 chain-packing proof. Python standard library only.

The proof is analytic and does not rely on testing a finite range.
These checks verify its algebra, a finite collection of constructed chain
measures, and a known collision used as a positive control.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from decimal import Decimal, localcontext
from pathlib import Path
import json
import math

@dataclass(frozen=True)
class Q2:
    """The real number a+b*sqrt(2), represented exactly."""
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    @staticmethod
    def coerce(x: object) -> Q2:
        if isinstance(x, Q2): return x
        return Q2(Fraction(x))

    def __add__(self, other: object) -> Q2:
        o=self.coerce(other)
        return Q2(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self) -> Q2: return Q2(-self.a,-self.b)
    def __sub__(self, other: object) -> Q2: return self + (-self.coerce(other))
    def __rsub__(self, other: object) -> Q2: return self.coerce(other) + (-self)
    def __mul__(self, other: object) -> Q2:
        o=self.coerce(other)
        return Q2(self.a*o.a+2*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __pow__(self, e: int) -> Q2:
        if not isinstance(e,int) or e<0: raise ValueError('nonnegative integer power required')
        out=Q2(Fraction(1)); base=self
        while e:
            if e&1: out=out*base
            base=base*base; e//=2
        return out
    def sign(self) -> int:
        a,b=self.a,self.b
        sg=lambda x:(x>0)-(x<0)
        if not a: return sg(b)
        if not b: return sg(a)
        if (a>0)==(b>0): return sg(a)
        return sg(a*a-2*b*b) if a>0 else sg(2*b*b-a*a)
    def __le__(self, other: object) -> bool: return (self-self.coerce(other)).sign()<=0
    def __lt__(self, other: object) -> bool: return (self-self.coerce(other)).sign()<0


def is_prime(n: int) -> bool:
    if n<2: return False
    return all(n%d for d in range(2,math.isqrt(n)+1))


def sigma_by_divisor_enumeration(factorization: dict[int,int]) -> tuple[int,int,int]:
    divisors=[1]
    for p,e in factorization.items():
        if not is_prime(p) or e<0: raise ValueError('invalid prime factorization')
        divisors=[d*p**j for d in divisors for j in range(e+1)]
    n=math.prod(p**e for p,e in factorization.items())
    assert len(set(divisors))==len(divisors)
    assert all(n%d==0 for d in divisors)
    return n,sum(divisors),len(divisors)


def main() -> None:
    one=Q2(Fraction(1));t=Q2(Fraction(0),Fraction(1,2));D=t+t*t
    assert t*t==Q2(Fraction(1,2))
    assert one<D
    assert D**2==t+t**2+t**4
    assert D**3-(1+t)==(2*t-1)*Fraction(1,8)
    assert 1+t<D**3
    # Root mass: S_a <= A^a is equivalent to S_a^2 <= D^a.
    caps=200
    primes=[p for p in range(2,caps+2) if is_prime(p)]
    S=Q2();checks=0
    for a in range(caps+1):
        if a+1 in primes: S=S+t**a
        assert S*S<=D**a,('root mass',a)
        checks+=1
    # Check child masses using the canonical parent n/P^+(n).
    child_checks=0
    for n in range(2,caps+2):
        factors=[p for p in primes if n%p==0]
        largest=max(factors)
        children=[n*p for p in primes if p>=largest and n*p<=caps+1]
        ratio=sum((t**(m-n) for m in children),Q2())
        assert ratio<=one,('child mass',n)
        child_checks+=1

    fa={11:2,13:2,17:1,19:1,31:1,61:1,97:1,127:2,271:1,307:2,331:1,367:1}
    fb={13:1,17:2,19:2,23:1,31:2,43:1,61:2,83:1,127:1,307:1,733:1,5419:1}
    a,sa,da=sigma_by_divisor_enumeration(fa)
    b,sb,db=sigma_by_divisor_enumeration(fb)
    assert a!=b and a*sa==b*sb
    support=sorted(fa.keys()|fb.keys())
    euler=math.prod(Fraction(p,p-1) for p in support)
    assert euler<4
    incomparable=[p for p in support if (fa.get(p,0)+1)%(fb.get(p,0)+1) and (fb.get(p,0)+1)%(fa.get(p,0)+1)]
    assert incomparable
    # Exhaustively verify local chain/comparability implication at small caps.
    ratio_checks=0
    for p in (2,3,5,11,101):
        for b0 in range(9):
            for a0 in range(b0+1,13):
                if (a0+1)%(b0+1): continue
                numerator=p**(a0+1)-1;denominator=p**(b0+1)-1
                assert numerator%denominator==0
                Q=numerator//denominator; power=p**(a0-b0)
                assert power<Q
                assert Fraction(Q,power)<Fraction(p,p-1)
                ratio_checks+=1
    modelpath=Path(__file__).with_name('rough_columns.json')
    model_checks=0
    model_euler=None
    if modelpath.exists():
        model=json.loads(modelpath.read_text())
        checked=set()
        input_primes=set()
        for p,e,f,column in model['cols']:
            input_primes.add(p)
            rhs=Fraction(1)
            for q,d in column.items():
                q=int(q)
                if q not in checked:
                    assert is_prime(q),('model output prime',q)
                    checked.add(q)
                rhs*=Fraction(q)**d
            assert is_prime(p)
            local=lambda a:p**a*sum(p**j for j in range(a+1))
            assert rhs==Fraction(local(e),local(f)),('valuation column',p,e,f)
            model_checks+=1
        model_euler=math.prod(Fraction(p,p-1) for p in input_primes)
        assert model_euler<4
    with localcontext() as ctx:
        ctx.prec=55
        root2=Decimal(2).sqrt()
        C=(1+1/root2).ln()/2
        Ccube=((1+Decimal(5).sqrt())/2).ln()/2
    result={
        'all_checks_passed':True,
        'root_mass_checks':checks,
        'child_mass_checks':child_checks,
        'local_ratio_checks':ratio_checks,
        'retained_valuation_columns_checked':model_checks,
        'model_input_euler_product':float(model_euler) if model_euler is not None else None,
        'new_constant':str(C),
        'cubefree_constant':str(Ccube),
        'known_witness':{'a':str(a),'b':str(b),'target':str(a*sa),'divisor_counts':[da,db],
                        'support_euler_product':str(euler),'euler_product_decimal':float(euler),
                        'incomparable_index_primes':incomparable},
        'scope':'Finite checks and witness verification, not a substitute for the all-parameter proof.'
    }
    out=Path(__file__).with_name('verification_v4.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
