# Two-base rigidity for k sigma(k)

## Status
This packet proves a local theorem: for any fixed distinct primes p and q, the values k sigma(k) for k=p^a q^b are all distinct as (a,b) ranges over nonnegative integer pairs.

It does NOT prove Erdős Problem 1060 and supplies no new unrestricted asymptotic constant. The zero-constant bound for arbitrary targets and every fixed input exponent cap remains unproved. The fixed prime pair is essential: h(12)=h(14)=336 uses different two-prime supports.

Originality relative to the complete literature has not been established. No independent human referee review or formal proof-assistant verification is claimed.

## Contents
- proof.pdf: complete seven-page mathematical argument, consequences, and scope.
- proof.tex: editable LaTeX source.
- verify.py: standard-library finite regression checker.
- verification.json: output from the checker.

## Run the finite checks
```sh
python3 verify.py
```
Do not pass Python's -O option. The script uses exact integers and fractions and needs no third-party packages. It overwrites verification.json with its results.

The finite tests are not the proof of the unbounded-exponent theorem. The written proof is independent of all finite searches. The input-bounded collision check is not a complete census of larger preimages of every encountered target.

## Mathematical ingredients
The proof compares reduced denominators of two rational prime-power increment ratios. A gap lemma, elementary prime-adic lifting, and a cyclotomic degree estimate force an integer proportionality relation. A strictly increasing real function then excludes equality. The primes 2 and 3 are handled separately, with no unproved conjectures or assumptions about Wieferich pairs.

## Remaining gap
Any two distinct preimages must differ at at least three prime bases. Such a fixed minimum-distance bound alone does not prevent exponentially many exponent vectors. The number and interaction of larger genuine exchanges remain uncontrolled on the scale log N / log log N.
