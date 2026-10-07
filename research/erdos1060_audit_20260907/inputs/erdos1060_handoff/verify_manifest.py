#!/usr/bin/env python3
"""Check the distributed file sizes and SHA-256 hashes; uses only the standard library."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
failures = []
for row in manifest["files"]:
    path = root / row["path"]
    if not path.is_file():
        failures.append(f"Missing: {row['path']}")
        continue
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    if path.stat().st_size != row["bytes"] or sha.hexdigest() != row["sha256"]:
        failures.append(f"Changed: {row['path']}")
if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"PASS: {len(manifest['files'])} files match their recorded sizes and SHA-256 hashes.")
print("File integrity is not mathematical verification. Running original scripts may change their JSON outputs.")
