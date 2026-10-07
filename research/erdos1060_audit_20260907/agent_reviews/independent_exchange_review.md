# Independent arithmetic exchange review

7 September 2026. This document proves partial lemmas, not Erdős 1060. No claim of literature novelty is made. The input dossier's exchange decomposition and denominator identity were checked directly. The argument below keeps all output-prime equations; no graph edge is promoted to an actual exchange.

## 1. A denominator budget for disjoint genuine exchanges

Let h(n)=nσ(n). Fix a reference preimage k₀ with h(k₀)=N. Let I be a collection of nontrivial exact exchanges with pairwise disjoint changed-prime sets Sγ. For an exchange write its old/new prime-power products as uγ,vγ, so h(uγ)=h(vγ). At p∈Sγ put aₚ=vₚ(uγ), bₚ=vₚ(vγ). Define

Hγ=h(uγ)=h(vγ),

Gγ=∏ₚ gcd(σ(p^{aₚ}),σ(p^{bₚ})),

Rγ=σ(gcd(uγ,vγ))/Gγ,

Tγ=gcd(σ(uγ),σ(vγ))/Gγ.

Both Rγ and Tγ are positive integers. The geometric-sum gcd formula gives

gcd(σ(pᵃ),σ(pᵇ)) = σ(p^{gcd(a+1,b+1)−1}).

For completeness, write u=gw,v=gz, gcd(w,z)=1. From wσ(u)=zσ(v), there is an integer t with σ(u)=zt, σ(v)=wt and t=gcd(σ(u),σ(v)). Consequently

(T/R)² = ∏_{p∈S} (1−p^{−(max(aₚ,bₚ)+1)})/(1−p^{−(min(aₚ,bₚ)+1)}).

Every displayed local factor is strictly between 1 and p/(p−1). Therefore

1 < (Tγ/Rγ)² < P(Sγ), where P(S)=∏_{p∈S}p/(p−1).

Because Tγ,Rγ are integers and Tγ>Rγ, Tγ≥Rγ+1. If I is nonempty, multiplying over its disjoint sets gives the strict bound

Σ_{γ∈I} log(1+1/Rγ) < ½ log P(N),

where P(N)=∏_{p|N}p/(p−1). The disjointness is exactly what permits ∏γP(Sγ)≤P(N).

For B≥1 let ν_B count the exchanges in I with Rγ≤B. If ν_B>0, applying the argument to that subcollection gives

ν_B < log P(N)/(2 log(1+1/B)).

For ν_B=0 the non-strict version ν_B≤log P(N)/(2 log(1+1/B)) remains valid for N≥1. Thus, for fixed B, ν_B=O_B(log log log N), using the uniform elementary Mertens consequence P(N)=O(log log N).

In particular, Rγ=1 exactly when the two exponent indices are divisibility-comparable at every changed base. A disjoint collection consisting entirely of these compatible exchanges has

ν < log P(N)/log 4

when nonempty. This is substantially smaller than the elementary support-size budget, but says nothing comparable for unbounded Rγ or for the number of overlapping exchanges.

## 2. Support cost and the first three-base consequence

For every nontrivial exchange, uγ,vγ>1, hence uγ²<Hγ and vγ²<Hγ. Therefore

log Hγ > log(uγvγ)=Σ_{p∈Sγ}(aₚ+bₚ)log p

≥ Σ_{p∈Sγ}log p + 2Σ_{p∈Sγ:aₚbₚ>0}log p.

For disjoint exchanges their old blocks are pairwise coprime unitary factors of k₀, so ∏γHγ divides N. These costs can therefore be summed and bounded by log N.

If P(Sγ)≤4, a compatible exchange is impossible: its integer Tγ>1 would give 4≤Tγ²<P(Sγ)≤4. Hence such an exchange has an incomparable pair of indices, which entails aₚ,bₚ>0 at some changed prime. Its cost is consequently strictly greater than Σ_{Sγ}log p+2log min Sγ.

Every set of at most three distinct primes has Euler product at most 2·(3/2)·(5/4)=15/4<4. Thus a three-base exchange necessarily contains a shared positive base and has exponent-sum cost at least five. This does not establish a uniform multiplicity estimate.

## 3. Complete classification at cap two on exactly three changed bases

**Theorem.** Suppose h(a)=h(b), all prime exponents of a and b are at most two, and a,b differ at exactly three prime bases. Cancel the common full prime-power blocks at every unchanged base. The residual pair is {12,14}.

Thus the original pair is {12d,14d}, with gcd(d,42)=1 and with d cubefree. There is no claim that a general cubefree fiber has at most two elements.

Write

Lₚ=h(p)=p(p+1),

Sₚ=h(p²)=p²(p²+p+1),

Jₚ=Sₚ/Lₚ=p(p²+p+1)/(p+1)=p²+p/(p+1).

The local increment at a changed base is exactly one of Lₚ,Sₚ,Jₚ. The numerator and denominator of Jₚ are coprime, so its reduced denominator is p+1. Also p²<Jₚ<p²+1, and Jₚ is strictly increasing with p, since x²+x/(x+1) has derivative 2x+1/(x+1)²>0.

Orient each changed coordinate from its lower to its higher exponent. Since every increment exceeds one, the collision equates one increment to the product of the other two. The three prime bases are distinct throughout.

### Auxiliary mixed-divisibility lemma

If p<r are primes, r|p²+p+1 and p|r+1, then (p,r)=(2,7).

Indeed, r=lp−1 with l≥2. Set c=(p²+p+1)/r. Modulo p, −c≡1, so c≥p−1. Hence

2p−1≤r≤(p²+p+1)/(p−1)=p+2+3/(p−1).

For p≥5 the lower bound exceeds the upper bound. For p=3 the only prime divisor of 13 is 13, but 3∤14. For p=2 the only possible r is 7, and it works. The large-prime part of this lemma already appears in the supplied signed-feedback chapter; only the small-prime completion is added here.

### Auxiliary mutual-quadratic lemma

If a,b are distinct primes and a|b²+b+1, b|a²+a+1, then a²∤b²+b+1 and b²∤a²+a+1.

First we show that every coprime positive pair x,y with these two mutual divisibilities satisfies

x²+y²+x+y+1=5xy.

If 1<x<y, put z=(x²+x+1)/y. Then 1≤z<x: since y≥x+1, z<x+1, while z=x would force x|1. The new pair z,x is coprime and has the same mutual divisibilities. Indeed yz≡1 (mod x), and y²+y+1≡0 (mod x), so multiplying the latter congruence by z² gives z²+z+1≡0 (mod x). The other divisibility is the definition of z. The integer

m=(x²+y²+x+y+1)/(xy)=(z+y+1)/x

is preserved by replacing (x,y) by (z,x). Descending eventually reaches (1,1) or (1,3), since the companion of 1 divides 3. Both have m=5. This proves the identity.

Now suppose a²|b²+b+1. The identity rewrites b²+b+1=a(5b−a−1), so a|5b−1. If a=5 this is impossible. Otherwise substitute 5b≡1 into 25(b²+b+1)≡0 (mod a), obtaining a|31. Therefore a=31. But the quadratic equation for b has discriminant

21·31²−14·31−3=19744,

strictly between 140²=19600 and 141²=19881, so b cannot be an integer. The assertion with a,b interchanged follows by symmetry.

### No J increments

With no J increments, all local index changes are comparable. The compatible integer-multiplier argument from Section 2 rules out any collision on three bases, since the Euler product is less than four.

### Exactly two J increments

One possible shape is JₚIᵣ=J_q, where Iᵣ is the integer Lᵣ or Sᵣ. The reduced denominator q+1 must divide p+1, implying q≤p. But Iᵣ>1 implies J_q>Jₚ and therefore q>p, a contradiction.

The other shape is JₚJ_q=Iᵣ. If p,q are odd, the product has odd numerator and even denominator, so cannot be an integer. If p=2, q is odd and

J₂J_q=14q(q²+q+1)/(3(q+1)).

Integrality and gcd(q(q²+q+1),q+1)=1 imply q+1|14, hence q=13. But J₂J₁₃=793=13·61. It is odd, so is not Lᵣ for an odd prime; and it is squarefree, so cannot be Sᵣ. The prime 2 is already a different changed base. Thus neither shape is possible.

### Exactly three J increments

Suppose JₚJ_q=Jᵣ. Its reduced denominators imply r+1|(p+1)(q+1). Also r>pq: if r<pq, then Jᵣ<r²+1≤(pq−1)²+1<p²q²<JₚJ_q, and r=pq is composite.

As p,q are distinct primes, (p−1)(q−1)≥2, so (p+1)(q+1)≤2pq<2(r+1). Thus r+1 is a divisor exceeding half of (p+1)(q+1), and must equal it. It follows that r=pq+p+q. But then

Jᵣ>r²>(p²+1)(q²+1)>JₚJ_q,

a contradiction.

### Exactly one J increment

Since Jₚ is not an integer, it cannot stand alone against a product of two integer increments. Therefore the equation is JₚI_q=Iᵣ, with I_q,Iᵣ each L or S. There are four cases.

1. **JₚL_q=Lᵣ.** Since Jₚ>p², comparison at r=pq gives

Jₚq(q+1)>p²q(q+1)>pq(pq+1),

so r>pq. In the cleared equation p(p²+p+1)q(q+1)=(p+1)r(r+1), this implies r>p,q+1, hence r|p²+p+1. The p-adic equation gives p|r+1. The mixed lemma forces p=2,r=7; then q(q+1)=12, so q=3. This is exactly h(12)=h(14)=336.

2. **JₚS_q=Lᵣ.** Comparison at r=pq² gives

Jₚq²(q²+q+1)>p²q²(q²+q+1)>pq²(pq²+1),

hence r>pq²>q²+q+1 and r>p. The strict middle comparison holds because p(q+1)>1; the last strict inequality holds for distinct primes p,q (for q≥3 use 2q²>q²+q+1, and for q=2 use p≥3). Thus r must divide p²+p+1, while p|r+1. The mixed lemma again gives p=2,r=7, contrary to r>2q²≥18. No solution occurs.

3. **JₚS_q=Sᵣ.** If p,q,r are odd, the left side has negative 2-adic valuation and the right side valuation zero, impossible. If p=2, the left side has 2-adic valuation one and the right side zero. If r=2, the left side exceeds S₂=28 (both other primes are odd). Therefore q=2. The equation is 28Jₚ=Sᵣ. Its 2-adic equation requires v₂(p+1)=2. Its integrality requires p+1|28. The only prime satisfying both is p=3. But 28J₃=273=3·7·13 is squarefree and cannot be Sᵣ. No solution occurs.

4. **JₚL_q=Sᵣ.** If p=2, the left side has positive 2-adic valuation and the right side zero. If q=2, integrality requires p+1|6, hence p=5; but 6J₅=155 is squarefree. If r=2, the other primes are odd and JₚL_q>9·12>28. Thus p,q,r are all odd.

If p<q, monotonicity and Sₓ=JₓLₓ give p<r<q. Integrality gives p+1|q(q+1), and q>p+1, so c=(q+1)/(p+1) is an integer. The equation becomes Sᵣ=cpq(p²+p+1). In particular q|r²+r+1. If r|c, then r|q+1, contradicting the mixed lemma for the odd pair r<q. Thus r∤c, and r² must divide p²+p+1, impossible since p<r and p²+p+1<r².

If p>q, the same monotonicity gives q<r<p. From p+1|q(q+1) and p+1>q+1 we infer q|p+1. Write c=(p+1)/q, which is even, and t=(q+1)/c, an integer. The equation becomes Sᵣ=tp(p²+p+1). Since t≤(q+1)/2<r, we obtain r²|p²+p+1. Also p|r²+r+1. This contradicts the mutual-quadratic lemma.

All cases have now been considered. The only residual pair is {12,14}, proving the theorem.

## 4. Precisely what the packing number does not control

A small maximum number ν of disjoint exchanges does not imply f(N)≤2^ν. The supplied actual N₆ fiber has six points and five minimal exchanges relative to its least point, with no two disjoint; thus ν=1 and f(N₆)=6>2. The complete supplied N₇ dictionary has ν=2 and f(N₇)=7>4. These are concrete arithmetic examples, independently verified by the parent audit.

Even without such examples, a graph with g vertices all adjacent has ν=1 but g+1 independent sets. Therefore an upper bound on disjoint packing cardinality must be accompanied by a bound on the count or structure of overlapping alternatives. The denominator budget supplies neither.

## 5. Conditional bounded-denominator injectivity

For local indices i=a+1,j=b+1, g=gcd(i,j), the local denominator factor is

Rₚ=σ(p^{min(a,b)})/σ(p^{g−1})=(p^{min(i,j)}−1)/(p^g−1).

It equals one when the indices are comparable. Otherwise min(i,j) is a multiple of g at least 2g, so Rₚ≥1+p^g≥p+1.

Consequently, suppose a family F within one fiber satisfies the **pairwise** bound R(k,m)≤B for all k,m∈F. If y≥B and ∏_{p|N,p>y}p/(p−1)≤4, recording the exact input exponents at p≤y determines each member uniquely. Indeed, two members with the same record have no differing small base; a remaining incomparable base p>y would contribute Rₚ≥p+1>B, impossible. The residual pair is therefore compatible and is excluded by the Euler-product bound at most four.

At cap E this proves |F|≤∏_{p|N,p≤y}(min(E,vₚ(N))+1). The pairwise hypothesis is essential: bounding R(k,k₀) only relative to a reference does not imply it, since local states 1 and 2 both have denominator one against state 0, but have denominator p+1 against each other.

This criterion and the disjoint denominator budget are only partial reductions. There is no proof here that arbitrary fixed-cap fibers satisfy a useful uniform bound on these denominators or overlapping exchange counts. The unrestricted little-o assertion remains unproved.
