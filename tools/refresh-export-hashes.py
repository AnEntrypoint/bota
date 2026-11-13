#!/usr/bin/env python3
"""Refresh export/SHA256SUMS.json and conformance.json expected_hashes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    names = sorted(
        p.name for p in EXPORT.iterdir()
        if p.is_file() and p.name not in {"SHA256SUMS.json", "export-status.json", "conformance.json"}
        and (p.suffix in {".json", ".tsv", ".md", ".yaml"} or p.name == "export.yaml")
    )
    conf_path = EXPORT / "conformance.json"
    conf = json.loads(conf_path.read_text())
    conf["expected_hashes"] = {name: sha(EXPORT / name) for name in names}
    conf["expected_counts"]["export_hash_files"] = len(names) + 1
    conf["ruleDemand"] = {
        "json": "export/rule-demand.json",
        "tsv": "export/rule-demand.tsv",
        "generator": "python3 tools/build-rule-demand.py",
        "validator": "python3 tools/validate-rule-demand.py",
        "contentContract": "/workspace/hy3d/output/content-for-bota.json",
        "contentOwner": "hy3d",
        "rulesOwner": "bota",
    }
    conf["identifierModes"] = {
        "acronym": "python3 tools/validate-integration-live.py --identifier-mode acronym",
        "bota-fullname": "python3 tools/validate-integration-live.py --identifier-mode bota-fullname --default-dota-acronyms",
        "canonicalExport": "acronym",
        "oscraftTarget": "bota-fullname",
    }
    conf_path.write_text(json.dumps(conf, indent=2, sort_keys=True) + "\n")
    sums = {name: sha(EXPORT / name) for name in names}
    sums["conformance.json"] = sha(conf_path)
    sums = dict(sorted(sums.items()))
    (EXPORT / "SHA256SUMS.json").write_text(json.dumps(sums, indent=2, sort_keys=True) + "\n")
    print(f"HASH_REFRESH files={len(sums)} conformance={sums['conformance.json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
