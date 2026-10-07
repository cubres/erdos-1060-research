# Parity and even-exponent route for `h(k)=k sigma(k)`

This note separates the unconditional lemmas from two finite computations.  It
does **not** claim that `h` is injective on odd squares.

## 1. Exact 2-adic budget

Write `k=2^a product_{p odd} p^{e_p}`.  Then

```
v_2(h(k)) = a + sum_{p odd, e_p odd}
                  (v_2(p+1)+v_2(e_p+1)-1).                 (1)
```

Indeed, `sigma(2^a)` is odd.  If `p` is odd, then
`sigma(p^e)` is odd for even `e`; for odd `e`, the 2-adic LTE formula gives

```
v_2(sigma(p^e))
 = v_2(p^{e+1}-1)-v_2(p-1)
 = v_2(p+1)+v_2(e+1)-1.
```

Consequently every preimage of a target `n` has at most `v_2(n)` odd primes
whose input exponent is odd.  More sharply, their set `S` obeys

```
sum_{p in S} v_2(p+1) <= v_2(n).                            (2)
```

Every term omitted from (2) is nonnegative because `v_2(e_p+1)>=1`.

## 2. The odd-square bottleneck is exact

The standard parity criterion for the divisor sum says that `sigma(k)` is odd
if and only if the odd part of `k` is a square.  It follows that

```
h(k) is odd  <=>  k is an odd square.                        (3)
```

Also, every integer all of whose odd-prime exponents are even has the unique
form `k=2^a u^2` with `u` odd, and multiplicativity gives

```
h(k)=2^a(2^{a+1}-1) h(u^2),       v_2(h(k))=a.               (4)
```

Thus equality between two values in this class first forces the two powers of
2 to agree, after which (4) cancels them.  Therefore the following three
statements are equivalent:

1. `h` is injective on odd squares;
2. `h` is injective on integers whose odd-prime exponents are all even;
3. every odd target has at most one preimage.

No proof of these equivalent assertions was found.

## 3. A large unconditional obstruction to a coprime counterexample

Suppose that distinct coprime odd squares `x,y` satisfy `h(x)=h(y)`.  Coprimality
and the equality imply

```
sigma(x)=u y,                 sigma(y)=u x                  (5)
```

for one positive integer `u`.  Every quantity in (5) is odd.  The alternative
`u=1` is impossible, since it would simultaneously give `sigma(x)>x` and
`sigma(y)>y` in opposite directions.  Hence `u>=3`, and

```
9 <= u^2 = I(x)I(y)
   < product_{p | xy} p/(p-1),       I(m)=sigma(m)/m.        (6)
```

The product over a fixed number of odd primes is largest for the smallest odd
primes.  Exact rational multiplication shows that the product over the first
2,696 odd primes is below 9, while adjoining the next prime, 24,247, makes it
at least 9.  Therefore

```
omega(xy) >= 2697.                                            (7)
```

The exact threshold check is in `parity_route_verify.py`.

There is also a useful bridge to a separate hard problem.  By coprimality and
(5),

```
sigma(xy)=sigma(x)sigma(y)=u^2 xy.
```

Thus `xy` would be an odd `u^2`-multiperfect number, with odd multiplier at
least 9.  Chen and Luo's 2013 paper *Odd Multiperfect Numbers* states that no
odd `k`-perfect number is known for any `k>=2` and develops only necessary
structure (DOI `10.1017/S0004972712000858`).  So even the coprime subcase of
odd-square injectivity reaches established open territory.  This does not
prove that odd-square injectivity is equally hard, but it rules out treating
it as an already available elementary lemma.

More generally, cancel from an odd-square collision every local block
`H(p,e)` that occurs identically on both sides.  If the residual input supports
are disjoint, the preceding argument applies to the residual collision.
Therefore any residual collision involving fewer than 2,697 input primes must
contain a prime that occurs on both sides with two *different* even exponents.
This gives a clean dichotomy for any future search: either an odd
multiperfect-number obstruction, or a crossed-exponent obstruction.

## 4. What odd-square injectivity would buy

For an arbitrary preimage `k`, put all of `2^{v_2(k)}` and every odd prime
power occurring to an odd exponent into `A(k)`, and put the remaining prime
powers into `B(k)`.  Then `(A(k),B(k))=1`, `B(k)` is an odd square, and
`h(k)=h(A(k))h(B(k))`.  If odd-square injectivity were known, two preimages
having the same `A(k)` would coincide.

For a target `n` with `t=v_2(n)`, (1) would therefore give the conditional
bound

```
f(n) <= # { (e_p) : e_p is odd, 1<=e_p<=v_p(n),
                    sum_p [v_2(p+1)+v_2(e_p+1)-1] <= t }.     (8)
```

The exponent of 2 in `A(k)` is uniquely determined by the selected odd prime
powers and (1), so no extra factor `t+1` is needed.  In particular, if all
input exponents are below a fixed `R` and `t` is fixed, (8) is polynomial in
`omega(n)`.  This is a real reduction, but it is not uniform enough by itself
when `t` grows like `log n/log log n`.

## 5. Fixed small-prime valuations have a blind spot

Let `T` be any finite set of primes and `Q=product_{q in T}q`.  Dirichlet's
theorem gives infinitely many primes `r == -1 (mod Q)`.  For each such `r`,

```
H(r,2)=r^2(r^2+r+1),          v_q(H(r,2))=0  for every q in T. (9)
```

Indeed `r^2+r+1 == 1 (mod q)`.  If `h(a)=h(b)=N`, choose distinct such primes
away from the input supports and let `c` be any product of their squares.
Then

```
h(ac)=h(bc)=N h(c),
v_q(N h(c))=v_q(N)  for every q in T.                         (10)
```

So a weight supported on any fixed finite collection of target primes is
unchanged along arbitrarily large decorated collision targets.  This does not
disprove a coarse bound depending only on that finite valuation vector, but it
does prove that those valuations cannot charge the even-exponent local blocks
or yield a size-sensitive estimate without an additional injectivity theorem.

## 6. Tensor products and `v_2`

If collision blocks have pairwise disjoint **input** prime supports, their
choices multiply.  Target valuations add, whether or not target supports are
disjoint.  The exact blocks

```
315 <-> 351,       common target 196560,  v_2=4,
1984 <-> 2032,     common target 8062976, v_2=11
```

therefore generate four preimages of

```
1584858562560 = 196560 * 8062976,      v_2=15.
```

There is in fact a fifth preimage, 708660, found by complete divisor
enumeration elsewhere in this verification directory.  Thus any valuation
entropy argument must remain compatible with additive tensorization.  On the
other hand, every even collision block contributes positively to `v_2`;
the only way a collision atom could evade that charge is precisely an
odd-square collision, the unresolved bottleneck in Section 2.

Since `max_q v_q(n) >= v_2(n)`, the same observation applies to the maximum
target valuation: tensoring even collision atoms cannot keep that maximum
bounded.  Conversely, the maximum valuation is easy to inflate without
creating information about the fiber.  Given a collision target `N`, choose an
odd prime `r` outside all of its displayed input supports and multiply every
displayed preimage by `r^{2E}`.  The new target is `N H(r,2E)`, has at least the
same number of preimages, and has maximum prime valuation at least `2E`.
Therefore a large maximum valuation is not itself evidence that the fiber is
complicated; it is useful only as an upper-bound budget.  The computations and
known tensor atoms do not refute the possibility of an upper bound depending
only on that maximum.

## 7. Finite searches (evidence only)

`odd_square_census.cpp` factors every odd root `u<=10^8`, constructs
`h(u^2)` exactly in unsigned 128-bit arithmetic, sorts all 50,000,000 values,
and finds no duplicate.  Thus no odd-square collision was found with both
inputs at most `10^16`.

`parity_class_census.cpp` exhausts all retained preimages `k<10^7` with
`h(k)<=10^14`.  Among 250,724 collision pairs it finds none whose input
exponent vectors agree modulo 2 (equivalently, none with a square quotient).
This stronger observation is also only finite evidence.

Reproduction:

```
clang++ -O3 -std=c++17 odd_square_census.cpp -o odd_square_census
./odd_square_census 100000000

clang++ -O3 -std=c++17 parity_class_census.cpp -o parity_class_census
./parity_class_census 10000000

python3 parity_route_verify.py
```
