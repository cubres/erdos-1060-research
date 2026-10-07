# Erdős 1060: sparse-change reconstruction, continuation v6

## Status

This packet contains proved partial results, not a complete proof of
`log max(1,f(N)) = o(log N / log log N)` for unrestricted targets.
The mathematical proof is independent of the finite experiments.
Originality relative to the complete literature has not been established.
No formal proof-assistant certification or independent human referee review
is claimed.

## Main results

Write `h(k)=k sigma(k)`, let `f_E(N)` restrict input prime exponents to at
most E, and put `w=log log N` for sufficiently large N.

A family within one fiber is called compatible when, at each input prime,
every two exponent indices `v_p(k)+1` are comparable by divisibility.
Compatible families have logarithmic size `O_E(w log w)` for fixed E,
even with no target exponent bound, and `O(w^(3/2))` without any input
exponent bound.

The parameterized applications are

    log max(1,f_3(N)) = O((v_3(N)+log w)w),
    log max(1,f_5(N)) = O((v_2(N)+v_3(N)+v_5(N)+log w)w).

Full-fiber consequences:

* `log max(1,f(N)) = O(w log w)` for `N=2^a m`, where m is odd and
  fourth-power-free, with no restriction on a.
* `log max(1,f(N)) = O(w log w / log log w)` for sixth-power-free targets.

These restricted classes satisfy the zero-constant conjectured bound.
The unrestricted partition into sufficiently few compatible families is
not proved. Large exceptional valuation budgets and higher-index
interactions remain unhandled.

## Contents

- `erdos1060_sparse_changes_proof.pdf`: complete mathematical arguments,
  limitations, and finite certificate explanation.
- `erdos1060_sparse_changes_proof.tex`: editable LaTeX source.
- `verify_v6.py`: exact verifier using only Python's standard library.
- `finite_model_5000_6.json`: permitted input primes 7 < p <= 5000,
  exponents <= 6, divisor sum coprime to 2*3*5*7.
- `finite_model_1000_10.json`: permitted input primes 11 < p <= 1000,
  exponents <= 10, divisor sum coprime to 2*3*5*7*11.
- `verification_v6.json`: results of an actual successful checker run.
- `explore_even.py`: optional discovery script, requiring SymPy; the
  discovery script is not a premise of the exact certificate verification.

## Reproduce the certificates

Use Python 3.10 or later. No packages or internet are needed for validation.
From the extracted packet directory, run:

    python3 verify_v6.py

Do not invoke Python with `-O`: the checker deliberately uses assertions.
The script reconstructs all admissible local blocks, checks their products,
checks that every two distinct factor-row bases are coprime, reconstructs
the difference columns, and repeats the exact elimination proof. It also
runs small regression tests and writes `verification_v6.json`.

The first certificate deletes all 2035 columns in three rounds of sizes
2003, 30, 2. The second deletes all 1005 columns in rounds of sizes 998, 7.
These are finite prime-factor range results, not bounds on the inputs'
integer sizes and not an unbounded-prime theorem. A product-tree
coprimality check establishes multiplicative independence of all factor
row bases; no unproved large-factor primality assumptions are required.

To rebuild the PDF with an ordinary LaTeX installation:

    pdflatex erdos1060_sparse_changes_proof.tex
    pdflatex erdos1060_sparse_changes_proof.tex

Only the proof, source, checker, models, and reported results are needed.
No font files are distributed.
