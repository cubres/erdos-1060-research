# Erdős Problem 1060 — partial bounds, collision certificates and audits

Recovered on **7 October 2026** from the September 5–7 local research and proof-audit work. The problem asks for a uniform little-o estimate for the multiplicity of `k sigma(k)=n`. **The recovered work does not prove that estimate.**

## Results and limitations

The supplied peer manuscript and audit give the partial general coefficient `C1 = (1/2) log(1+1/sqrt(2)) = 0.267399998369785...`; the cubefree coefficient is `(1/2) log(phi)`. These remain positive constants. Attribution to the supplied manuscript is preserved.

The archive also records a three-changed-prime-base classification reducing cubefree exchanges to `12 <-> 14` after cancellation, bounded-denominator packing, exact collision certificates, selected complete fibers, alternative counting routes and their obstructions. None controls the uniform many-prime problem. See [the proof audit](reports/Erdos_1060_Proof_Audit.pdf) and [claim/source ledger](research/research_artifacts/claim-source-ledger.md).

## Start here

- [Full research note](research/report-source.md).
- [September 7 audit source](research/erdos1060_audit_20260907/Erdos_1060_Proof_Audit.tex), [PDF](reports/Erdos_1060_Proof_Audit.pdf) and [audit README](research/erdos1060_audit_20260907/README_AUDIT.md).
- `research/`: research notes, original handoff materials, C++/Python programs and independent review reports.
- `claude-original/`: the recovered original Claude scratch note and its related files.
- `evidence/`: exact JSON datasets, packets, historical outputs and supplied documents, packed in ordinary ZIP archives.
- [Recovery provenance](PROVENANCE.md) and `provenance/recovered-files.json`: sizes, SHA-256 hashes and archive-member locations.

## Reproduce the fresh selected checks

Use Python 3.10+ without `-O`. First extract the preserved data:

```sh
python3 tools/unpack_evidence.py
cd research/erdos1060_audit_20260907
python3 -B verify_audit.py
python3 -B agent_reviews/verify_selected_certificates.py
python3 -B agent_reviews/verify_three_base_exchanges.py
```

All three programs passed in the recovery run. They reproduce selected complete fibers and exact collision/denominator tests, and examine all cap-two three-base exchange patterns on the 669 primes below 5000. Logs are in `verification/`. The unbounded classification rests on its written proof. The historical census through `10^16` was not rerun in this upload and is identified as historical evidence.

These materials were prepared with AI assistance. Internal reviews are not external validation or a priority proof. Bibliographic searches have stated scope and may be outdated. No new license is granted to supplied manuscripts or third-party material. Problem source: [Thomas Bloom's page](https://www.erdosproblems.com/1060). [All recovered Erdős work](https://github.com/cubres/erdos-research-index).
