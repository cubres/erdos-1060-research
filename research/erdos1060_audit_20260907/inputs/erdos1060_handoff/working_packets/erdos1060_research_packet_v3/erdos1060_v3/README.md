# Erdős 1060 research packet, pass 3

This packet contains a proved partial upper bound, not a solution of the conjecture.

Start with `proved_results_v3.md`, then use `worker_prompt_v3.md` for the next research worker. The older arguments, exact collision witnesses, and inverse enumerators are retained under `prior_v2/`. Their original filenames may refer to version 2.

## New result

The proof note gives the uniform upper-bound constant
`log(3)/2 - log(2)/3 = 0.3182570841474...`, using injective prime-index exponent encodings and an exact entropy inequality. The proof does not rely on numerical optimization. Originality has not been established.

## Exact verification

Run, from this directory:

```sh
python check_certificates.py
```

This uses only the Python standard library. It checks the rational inequalities, every local factorization used in the three stated finite noncollision certificates, recursive Lucas primality certificates for the factors, the exact peeling procedure, and the final determinant. `standalone_check.json` records the successful run performed here.

The prime certificates use the full-factorization Lucas criterion: if all prime factors of n-1 are proved prime, a^(n-1) is 1 modulo n, and a^((n-1)/q) is not 1 modulo n for each prime q dividing n-1, then a has order n-1 modulo n, forcing n to be prime. All arithmetic in the checker is integer/rational arithmetic.

To repeat the prior collision verification:

```sh
python prior_v2/verify_witnesses.py
```

`rechecked_witnesses.json` records the new run of this verifier, which constructs and sums all divisors.

## Exploratory tools

`search_models.py` prepares exact difference-column models and uses a numerical MILP solver for witness discovery. It requires NumPy, SciPy, and SymPy. Every witness is checked with integer products. A numerical infeasibility, timeout, or optimality status is not by itself a mathematical certificate.

`certify_experiments.py` regenerates the certificates, using SymPy to propose factorizations. The standalone checker independently verifies them without SymPy. `entropy_opt.py` records the numerical search which suggested the weights; its optimizer output is not a proof. `cubefree_coordinates.py` is exploratory only: no general diagonal or classification theorem is inferred from its experiments.

The rough search with minimum allowed prime 101 and maximum prime 100000 timed out without a feasible incumbent. It is intentionally labelled inconclusive. The positive control with minimum prime 11 rediscovered the known 29-digit collision. No record or minimality claims are made.

No formal proof-assistant verification, human refereeing, or guarantee of a full solution is claimed.
