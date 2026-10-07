# Erdős 1060: signed-feedback counting criteria

This packet contains proved partial counting criteria and exact finite checks.
It does not contain a solution of the unrestricted Erdős conjecture.
The strongest unrestricted asymptotic bound in the prior investigation is not
improved by this note.

## Files

- `erdos1060_signed_feedback.pdf`: mathematical note.
- `erdos1060_signed_feedback.tex`: editable LaTeX source.
- `verify_signed_feedback.py`: independent, exact standard-library checker.
- `verification.json`: its recorded output.

Run `python3 verify_signed_feedback.py` to reproduce the finite checks.
No external Python packages, floating-point solver claims, or assumed large
prime factorizations are needed. Trial division verifies the displayed prime
bases, and the known large collision is separately verified by summing all
divisors of both inputs.

## Proven scope

The signed graph is built from changes of local divisor-sum valuations, with
sign reversed because the input exponent is the negative of the other local
contributions plus the target valuation. Two distinct solutions force a
positive elementary circuit. Cutting only those circuits gives a valid
reconstruction bound even when negative circuits remain.

For cubefree inputs the note derives a uniform *parameterized* bound involving
`tau_+(N)`, the minimum number of vertices meeting every positive elementary
circuit of length at least three. The required asymptotic estimate on this
parameter is not proved. The resulting zero-constant corollary is restricted
to the stated graph-defined target classes.

The criterion specializes established positive-feedback mathematics, notably
Adrien Richard's Theorem 2 (author preprint, 2009). The number-theoretic
classification of mutual quadratic pairs is from Bibby--Vyncke--Zelinsky,
Lemma 5. No originality or formal proof-assistant certification is claimed.

## Finite assertions

After sound exact row pruning, threshold cuts certify `f_2(M) <= 12` and
`f_2(N0) <= 6`. These are weaker than their previously established exact counts
2 and 1, respectively, and are not multiplicity records. They demonstrate a
different certificate method. The above-three graph for M has four long
positive circuits all meeting 17 and one quadratic pair {13,61}, giving the
separate unpruned bound 54. An eight-prime quadratic circuit is also checked;
it is a divisibility cycle, not a collision.
