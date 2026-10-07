# Erdős 1060: v4 partial result and audit

The complete proof is `chain_packing_proof.pdf`; its editable source is
`chain_packing_proof.tex`. It establishes the uniform upper bound

    log max(1,f(N)) <= (C1+o(1)) log N / log log N,
    C1 = (1/2) log(1+1/sqrt(2)) = 0.267399998369785...

It does NOT establish the zero constant in Erdős's conjecture. The proof
is self-contained apart from the definition and elementary properties
of the divisor-sum function; it includes the elementary prime-counting
estimate it needs. No experimental statement is a premise of the theorem.
No priority, human-referee review, or formal proof-assistant check is claimed.

## Exact audit

Run:

    python check_v4.py

This script uses only the Python standard library. It checks algebra and
chain-mass comparisons in the exact ordered field Q(sqrt(2)), verifies a
known collision by enumerating and summing all divisors of both inputs,
and verifies every retained valuation-difference column in
`rough_columns.json` by exact rational arithmetic and trial-division
primality checks. The columns are a retained search model from the v3
experiment, not a fresh complete census of integers. The successful output
is recorded in `verification_v4.json`.

## Inconclusive searches

`search_rough_v4.py` and `search_rough_cuts_v4.py` require NumPy and SciPy.
They search the retained model with input-prime bounds 101 and 100000,
using exponent choices 0,1,2. The second search requires both a support
change and a 1-versus-2 exponent transition. Any discovered witness is
checked exactly; infeasibility or timeout messages are not proof
certificates. The returned 12-second and 30-second search results are
included. Neither run found a feasible witness. A preceding process was
terminated externally at a 60-second wall limit before producing an
output file. This is also inconclusive.

## Relationship to previous work

The earlier prime-index entropy proof in this conversation gave the
positive constant 0.3182570841474. The new argument instead uses an
integer-square obstruction to simultaneous divisibility comparability,
then a probability distribution on finite divisibility chains. The
remaining difficulty is controlling the arithmetic correlations omitted
by this packing condition. The last mathematical section of the proof
explains explicitly why exponential abstract models still survive it.

Primary literature references are included in the proof. The current
Erdős problem-page retrieval failed; no assertion about the status of
all public proof claims is inferred from that failure.
