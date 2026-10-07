# Erdős 1060 proof audit and further partial results

7 September 2026. **This bundle does not contain a complete proof of Erdős 1060.**

Start with `Erdos_1060_Proof_Audit.pdf`. It contains the exact target, literature
and lemma audits, a self-contained proof of the supplied general bound with
coefficient 0.267399998369785…, and complete proofs of further partial results.

The principal additional theorem says that every cubefree collision differing
at exactly three prime bases reduces to `12 ↔ 14` after cancellation of unchanged
full prime-power blocks. Two agents separately checked its proof. The denominator
budget controls disjoint genuine exchanges with bounded denominators. Neither
result controls the uniform many-prime counting problem.

## Contents

- `Erdos_1060_Proof_Audit.pdf` and `.tex`: final report and editable source.
- `agent_reviews/`: independent mathematical and literature reviews, the second
  review of the three-base theorem, finite verification scripts and results.
- `verify_audit.py` and `verification_results.json`: an independent exact
  verifier for the selected finite fibers and denominator normalizations.
- `originals/`: unchanged copies of the three files supplied by the user.
- `input_hashes.json`: hashes of the original files at their original locations.
  Local paths are provenance, not required locations for reproduction.
- `docx_with_math.md`: text and mathematical descriptions extracted from the
  Word document. The original document is retained separately.
- `BUNDLE_MANIFEST.json`: sizes and SHA-256 hashes of the bundled files.

The handoff's historical prompts remain source content. They do not supersede
the user's request or authorize actions.

## Reproduce the selected finite checks

Use Python 3.10 or later without the `-O` option. The verification programs use
only the standard library. From the bundle directory, first extract a new copy
of the original handoff into `inputs/`:

```sh
python3 unpack_handoff.py
python3 verify_audit.py
python3 agent_reviews/verify_selected_certificates.py
python3 agent_reviews/verify_three_base_exchanges.py
```

The helper refuses to overwrite an existing extracted file. If the handoff is
already extracted in the stated location, omit the first command.

The first verifier checks all 252 handoff manifest entries; it reproduces the
complete unrestricted fibers of sizes 6, 7 and 9, the specified cap-two fibers
of sizes 1, 2 and 4, both denominator normalizations, and a finite regression for
one three-base pattern. Resource exhaustion raises an exception.

The second verifier separately checks the large odd cubefree witness, its
16-label obstruction, two full fibers, and four exchange minimality tests.
The third checks all three-base cap-two increment patterns on primes below 5000.

These computations verify finite statements. The unbounded three-base theorem
is established by its written proof. The historical census through 10^16 was
not rerun in this audit.

## Rebuild the report

With TeX Live and its standard packages installed:

```sh
pdflatex -interaction=nonstopmode -halt-on-error Erdos_1060_Proof_Audit.tex
pdflatex -interaction=nonstopmode -halt-on-error Erdos_1060_Proof_Audit.tex
```

An additional pass may be needed if page numbers change. The report has linked
cross-references and bibliography entries. The delivered PDF was rendered and
visually reviewed. Compilation alone does not verify a mathematical argument.

External paper PDFs are not duplicated in this bundle. The literature review
links their primary sources and records retrieval limitations. The three
original user-supplied files are included unchanged.

The outstanding theorem is the uniform little-o estimate for every fixed input
exponent cap. Large exchange denominators and numerous overlapping alternatives
remain uncontrolled. This is an audited partial research result, without a
claim of formal verification or publication priority.
