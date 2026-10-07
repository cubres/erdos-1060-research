# Erdős 1060: complete research handoff

Handoff edition: 7 September 2026. Main PDF: **93 pages**.

This is a complete handoff of the supplied investigation, not a proof of Erdős 1060.
The main uniform estimate remains unproved. The newer deductions are working
proofs, not independently refereed theorems; audit them before extending them.
Finite certificates do not establish asymptotic claims. No originality is claimed.

## Start with the PDF

Open `erdos1060_research_handoff.pdf`. It is searchable and contains a linked table
of contents, numbered propositions and equations, source links, and PDF bookmarks.
It includes full mathematical arguments rather than only a summary of the chat.

A useful reading order is:

1. Chapters 1–3: exact problem, result ledger, and quantified fixed-cap reduction.
2. Chapters 5, 9 and 10: strongest unrestricted bound in the record, full fixed-two-prime
   rigidity proof, and primitive-divisor exponent lists.
3. Chapters 8, 11, 16 and 18: mandatory counterexamples and limits of the attempted
   proof completions. In particular, potential graph cycles are not genuine choices.
4. Chapter 17: exact exchanges satisfying every target valuation, and what their
   decomposition still does not count uniformly.
5. Chapters 19–21: literature audit, computational inventory, and next-agent brief.

Chapter 21 and `NEXT_AGENT_PROMPT.md` supersede the early helper prompts.
Do not revive their disproved small-range cubefree classification suggestion.

## Exact target

Let h(k)=k sigma(k), f(N)=#{k>=1:h(k)=N}. Prove or refute:

    for every epsilon > 0, there is N_epsilon such that for every N >= N_epsilon,
    log(max(1,f(N))) <= epsilon * log(N)/log(log(N)).

The stronger polylogarithmic conjecture is separate. Another positive constant,
an almost-all result, or N^{o(1)} does not prove this target.

## Files

- `source/`: compilable consolidated LaTeX, chapter sources and bibliography.
- `original_notes/`: 31 original supplied proof/source/prompt/data files,
  preserved without mathematical editing. Old notes can be superseded by later ones.
- `original_packets/`: the 16 original ZIP archives, unchanged.
- `working_packets/`: extracted usable directories. Scripts write outputs locally.
- `checks/rechecks.json`: handoff rerun statuses, script hashes and log filenames.
- `checks/*.log`: complete recorded output of the reruns.
- `examples_catalogue.json`: exact target factorizations, witnesses and selected fibers.
- `original_packet_manifest.json`: hashes and sizes of the original archives.
- `MANIFEST.json`: sizes and SHA-256 hashes of every distributed file except itself.
- `verify_manifest.py`: standard-library integrity check.

Fifteen exact verification programs passed during this compilation. The larger
`verify_large.py` rerun was interrupted by an execution limit before returning a
result. Its original certificate is retained, but no fresh verification is claimed.
The checks do not amount to formal proof-assistant verification or human peer review.

## Reproduce a small check

Use Python 3.10 or later, without `-O` (the historical verifiers use assertions).
From the archive root:

```sh
python3 verify_manifest.py
cd working_packets/erdos1060_integer_gap_audit
python3 verify_fractional_obstruction.py
```

Other focused checks, each run from the indicated directory:

```sh
cd working_packets/erdos1060_two_prime_rigidity_packet/erdos1060_two_prime_rigidity
python3 verify.py
```

```sh
cd working_packets/erdos1060_genuine_exchanges_packet/erdos1060_genuine_exchanges
python3 verify_exchanges.py
```

```sh
cd working_packets/erdos1060_literature_audit_packet/erdos1060_literature_audit
python3 verify_order_lists.py
```

The `cd` paths above are relative to the archive root, not to each preceding command.
The Appendix and `checks/rechecks.json` give every other checked script location.
Inspect discovery scripts before running them; some use external packages or have
large search costs. Begin with exact verification, not an unbounded optimizer run.
Set explicit time and memory limits for large graph/collision searches.

## Rebuild the PDF

Use a normal TeX Live installation providing standard LaTeX packages:

```sh
cd source
pdflatex -interaction=nonstopmode -halt-on-error dossier.tex
pdflatex -interaction=nonstopmode -halt-on-error dossier.tex
```

An initial third run can be useful if your TeX version changes line/page breaks.
The output is `source/dossier.pdf`. `latexmk -pdf dossier.tex` is another option.
Latin Modern and the mathematical fonts are supplied by the TeX installation;
no standalone font files are distributed here.

## Evidence and provenance

The PDF groups complete working proofs by dependency, normalizes notation and
references, corrects typographical duplications, and identifies superseded results.
The original notes and ZIPs remain available for comparison. Conditional claims,
especially those using Bateman–Horn, remain conditional. Every finite experiment
retains its exact input/target/prime-factor range. Timeouts prove nothing.

The bibliography distinguishes primary theorem inputs from source leads and
quantitative audits of results for different functions. The main problem page
could not be retrieved during compilation; no comprehensive current public-status
claim is inferred from that access failure.

Do not report a complete solution until the entire uniform implication has been
proved, including the remaining many-prime counting estimate.
