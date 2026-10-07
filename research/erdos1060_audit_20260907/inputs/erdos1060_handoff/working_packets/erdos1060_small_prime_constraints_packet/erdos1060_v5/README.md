# Erdős 1060: small-prime divisor-sum constraints

Prepared 5 September 2026. This packet establishes a restricted-case theorem,
not a resolution for arbitrary targets. The proofs were developed and checked
in the present investigation. Originality relative to the full literature has
not been established. No independent human referee or formal proof-assistant
review is claimed.

## Main proved result

Write h(k)=k sigma(k), f(N)=#{k:h(k)=N}. Uniformly for sixth-power-free targets,
meaning v_p(N)<=5 for every prime p,

    log max(1,f(N)) = O((log log N / log log log N)^(3/2)).

This is a genuine zero-constant result on that class, much smaller than
log N / log log N. The restriction is on the target, not just the input.
The earlier general constant 0.267399998369785... is unchanged in this pass.

Read `small_prime_constraints.pdf` or its `.tex` source. The only standard
analytic inputs are Chebyshev's estimate and Mertens' product theorem; the
arithmetic uniqueness and counting arguments are proved in full.

## Reusable structural result

For two fixed primes ell_1, ell_2, input exponent indices of the form
ell_1^a ell_2^b are allowed. If the input primes and the divisor sums have no
prime factors <=Y, and the Euler product over the input support is <=Y^2,
then h is injective on this class. The index exponents a,b need not be bounded.
The proof first rules out incomparable indices using output-prime residue
classes, and then uses a Y-rough integer multiplier c: a nontrivial collision
would require both c>Y and c^2<Y^2.

For input exponents <=5, excluding small prime factors of sigma leaves only
exponents 0,2,4, with indices 1,3,5. This is the application in the main theorem.

## Exact target-dependent bound

Let f_5 count input exponents <=5; let B_Y(N)=sum_{q<=Y}v_q(N), and let r_Y(N)
count target primes exceeding Y. Whenever Y>=5 and

    product_{p|N,p>Y} p/(p-1) <= Y^2,

we have

    f_5(N) <= 6^pi(Y) sum_{j<=min(B_Y(N),r_Y(N))} binom(r_Y(N),j) 5^j
           <= 6^pi(Y) (1+5r_Y(N))^B_Y(N).

For sixth-power-free targets, B_Y<=5pi(Y). Choose
Y=2 sqrt(log log N / log log log N) and use Mertens' theorem.

## What remains unresolved

Neither of the following is supplied as a theorem:

* A cheap encoding when the small-prime target valuation budget B_Y is large.
* A corresponding rough-divisor-sum uniqueness/counting theorem for arbitrary
  fixed input exponent bounds. Exponent 6 introduces a third index prime, 7.

The local example sigma(29^2)=13*67, with sigma(67^4) and sigma(67^6) both
coprime to 2*3*5*7, shows why the two-prime residue argument does not automatically
extend to three index primes. It is NOT a collision or a global counterexample.

## Reproduce the exact checks

Run with Python 3:

    python verify_v5.py

Only the standard library is needed. The script checks cached local
factorizations by exact multiplication, proves their prime factors prime using
recursive Lucas certificates, and then verifies:

1. No cubefree collision with all input primes between 251 and 100000.
   All 28617 difference columns, owned by 9539 primes, are eliminated in 32
   rigorously valid rounds. This is a prime-factor bound, not an input bound.
2. A new odd cubefree collision with two 106-digit inputs and a 211-digit target.
   The 47 input primes lie between 17 and 9439. Exact geometric sums and a
   separate certified valuation computation both verify the identity.
   All divisors of these large inputs were NOT enumerated.
3. No duplicate exceptional-block encoding for the 196592 inputs k<=200000
   with prime exponents <=5, at Y=5. This is an input-bounded stress test,
   not a complete census of all encountered target fibers.
4. The local third-index-prime obstruction described above.

The checked output is in `verification_v5.json`. The verifier rewrites it
with the current timing. All certificate data needed for this verification
are included; the numerical optimizer is not a premise in these proofs.

## Exploratory searches

`search_general.py` requires NumPy and SciPy (with `scipy.optimize.milp`). Example:

    python search_general.py 17 10000 1 10
    python search_general.py 101 100000 3 12

Numerical solver behavior and timings may differ between platforms. A timeout
without a witness is inconclusive. A zero optimum for one chosen random
objective is not a noncollision certificate. Only exact witnesses or exact
elimination arguments are used as mathematical evidence.

`general_17_10000_1.json` contains the fully specified new witness. The other
`general_*.json` files are original search records and supply no nonexistence
claims. `peel_thresholds.py` reproduces the cutoff sweep; all paths are relative
to this packet.

## Literature

The proof cites Zach Teitler's *Analytic Number Theory Course Notes*, Sections
6.2 and 6.3, for Chebyshev's and Mertens' estimates. Kominers's working paper,
Noppakaew–Pongsriiam, and Bibby–Vyncke–Zelinsky are included as contextual
references, not as statements of the new restricted-case bound. Full links
are in the PDF bibliography. The current Erdős problem page could not be
retrieved in this pass; no current public proof-status assertion is inferred
from that access failure.
