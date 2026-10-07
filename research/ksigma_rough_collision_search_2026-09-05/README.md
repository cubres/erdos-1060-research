# Rough-input collision search

This directory contains a bounded search for exact collisions of
`h(k) = k*sigma(k)` whose input integers avoid prescribed small primes.

The search factors the local blocks `H(p,e)=p^e sigma(p^e)`, peels columns
having a globally private prime factor, and asks a binary MILP for two legal
products of the remaining blocks with identical prime-valuation vectors.
Every hit is reconstructed and verified with exact Python integers and SymPy;
the floating-point MILP is not treated as a proof certificate.

Example search excluding input primes `2,3,5,7`:

```sh
python3 search.py \
  --lower 11 --upper 1500 --max-exponent 8 \
  --time-per-seed 20 --seed-bases 8 \
  --forbidden-product 210 --output collision.json
```

The region is finite: base primes are between `lower` and `upper`, local
exponents are between 1 and `max-exponent`, and only the displayed fixed-left
seed runs are attempted. A no-hit result therefore applies only to that
explicit model and seed schedule.

Verify a saved hit independently with exact arithmetic:

```sh
python3 verify_certificate.py collision_11_700_e8.json --forbidden-product 210
```
