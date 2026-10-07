# Erdős 1060 refined research packet

Prepared 5 September 2026. This packet contains a continuation prompt, elementary partial results, large exact collision witnesses, and reproducible search and verification programs. It does not claim a solution of Erdős Problem 1060, a first discovery in the literature, or a minimal/record collision.

## What to give the next chatbot

Send `refined_helper_prompt.md` as the continuation prompt. Attach `proved_additions.md` and the programs or this whole packet when file processing is available. The prompt states the essential mathematical facts even without the programs.

The main additions to the earlier prompt are an exponent-coloring injection and its uniform constant log(2)/2; an explicit odd cubefree collision with all input primes at least 11; a four-way cubefree collision built from it; injectivity on squares of squarefree integers; a rigorously proved graph reconstruction lemma; and a rough-input reduction with carefully separated parameters.

## Exact verification, no third-party packages

Use Python 3.10 or later. Do not use `python -O`, which disables assertions.

```bash
python verify_witnesses.py
python exact_target_search.py --E 2
python exact_target_search.py --E 2 --scaled
python exact_target_search.py --E 24
python exact_target_search.py --E 24 --scaled
```

The independent verifier constructs and sums every divisor of each listed input. It does not use the geometric-sum formula used by the search. It verifies equality and cubefreeness, not the completeness of an inverse enumeration.

The inverse search uses the supplied, trial-division-checked target factorization and exact residual prime valuations. Its completeness argument appears in `proved_additions.md`. The fixed targets have maximum prime exponent at most 24, so the E=24 runs enumerate the full fibers.

Results:

| Target | Cubefree preimages | All preimages |
|---|---:|---:|
| M, defined in the note | 2 | 2 |
| 336 M | 4 | 6 |

There are four cubefree preimages of the scaled target, not four preimages in total. The two other preimages contain a cube. This distinction is intentional.

The full-fiber JSON logs contain complete lists for these two targets only. Neither the numerical size of a target nor the maximum input prime implies a global census bound.

## Exploratory collision search

The exact verification programs require only the standard library. The optional discovery program requires NumPy, SciPy, and SymPy. The package versions present in the environment used here are recorded in `requirements_search.txt`.

```bash
python -m pip install -r requirements_search.txt
python collision_milp.py --min-prime 5 --prime-limit 10000 \
  --max-exponent 2 --time-limit 30 --output new_search.json
```

The solver searches prime supports and exponent differences rather than scanning all integers up to a bound. Its time limit applies to optimization, not the preliminary factorization of the local blocks. Large exponent bounds or prime ranges can consume substantial memory and time. Start with the supplied defaults. Trial-division primality testing in the exact programs is suitable for the small prime bases in this packet, not a fast primality certificate for arbitrary enormous primes.

A floating-point mixed-integer solver is a discovery tool. Its “infeasible” and “optimal” statuses are not exact mathematical certificates and are not used to claim global nonexistence or minimality. Recompute every returned candidate with exact integers. Equivalent runs may return a different collision or terminate at their time limit.

`min5_cubefree_milp_10000.json` records the run that produced the main witness. The two other MILP logs record exploratory runs, including an uncertified negative solver result. They are not additional theorems. The search code was subsequently given input validation and a clearer disclaimer without changing its mathematical model.

## Files

- `refined_helper_prompt.md`: ready-to-send continuation prompt.
- `proved_additions.md`: complete elementary arguments and scope of computational claims.
- `collision_milp.py`: optional floating-point discovery model with exact witness checks.
- `exact_target_search.py`: exact bounded-exponent inverse enumeration.
- `verify_witnesses.py`: independent full-divisor-summation checks.
- `independent_verification.json`: saved verification output.
- `exact_f2_M.json`, `exact_f2_336M.json`: complete cubefree fibers.
- `exact_full_M.json`, `exact_full_336M.json`: complete unrestricted fibers.
- `*milp*.json`: exploratory solver logs, not exact infeasibility or optimality certificates.
- `requirements_search.txt`: tested package versions for the optional search.

Source references are included in the two mathematical Markdown documents. No third-party paper or font files are redistributed.
