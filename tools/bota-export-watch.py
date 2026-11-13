#!/usr/bin/env python3
"""Read-only BOTA export drift watch; writes export/export-status.json only."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
STATUS = EXPORT / "export-status.json"
LABELS = [
    "sync-roster", "build-gallery", "build-engine-data-1", "build-engine-data-2",
    "engine-byte-identical", "validate-export", "validate-decisions",
    "validate-integration", "validate-integration-live", "validate-engine-data",
    "validate-decision-packet", "validate-apply-mechanism", "sha256-integrity",
    "identifier-scan", "git-status-report-only",
]
KEY_MANIFESTS = [
    "SHA256SUMS.json", "conformance.json", "integration-contract.json",
    "engine/manifest.json", "decisions.json", "decision-packet.json", "field-index.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(rel: str):
    try:
        return json.loads((EXPORT / rel).read_text())
    except Exception as exc:
        return {"__error__": f"{rel}: {exc}"}


def main() -> int:
    proc = subprocess.run(["bash", "tools/check-bota-export.sh"], cwd=ROOT, text=True, capture_output=True)
    output = proc.stdout + "\n" + proc.stderr
    checks = {}
    for label in LABELS:
        m = re.search(rf"^\[{re.escape(label)}\] EXIT=(\d+) (PASS|FAIL)", output, re.M)
        checks[label] = {"exit": int(m.group(1)), "status": m.group(2)} if m else {"exit": None, "status": "MISSING"}
    canonical_unchanged = "CANONICAL_ENGINE_UNCHANGED=true" in output
    engine_resolved_exists = (EXPORT / "engine-resolved").exists()
    live_line = re.search(r"LIVE INTEGRATION: (PASS|FAIL) \((\d+) checks, (\d+) unavailable, (\d+) drift\)", output)
    live = {
        "status": live_line.group(1) if live_line else "UNKNOWN",
        "checks": int(live_line.group(2)) if live_line else None,
        "unavailable": int(live_line.group(3)) if live_line else None,
        "drift": int(live_line.group(4)) if live_line else None,
        "cross_project_key_diff": re.search(r"CROSS_PROJECT_KEY_DIFF=(\[.*?\])", output).group(1) if re.search(r"CROSS_PROJECT_KEY_DIFF=(\[.*?\])", output) else "UNKNOWN",
    }
    manifests = {rel: {"sha256": sha(EXPORT / rel), "bytes": (EXPORT / rel).stat().st_size} for rel in KEY_MANIFESTS}
    conf = load("conformance.json")
    decisions = load("decisions.json")
    packet = load("decision-packet.json")
    field_index = load("field-index.json")
    hashes = load("SHA256SUMS.json")
    counts = conf.get("expected_counts", {}) if isinstance(conf, dict) else {}
    drift = []
    if proc.returncode != 0:
        drift.append(f"pipeline exit {proc.returncode}")
    for label, result in checks.items():
        if result["exit"] != 0 or result["status"] != "PASS":
            drift.append(f"{label}: {result}")
    if not canonical_unchanged:
        drift.append("canonical engine changed")
    if engine_resolved_exists:
        drift.append("export/engine-resolved exists")
    if live["status"] != "PASS" or live["drift"] != 0:
        drift.append(f"live integration {live}")
    if any("__error__" in v for v in [conf, decisions, packet, field_index, hashes]):
        drift.append("key manifest parse failure")
    status = {
        "schema": "bota.export-status/v1",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "pipeline": {"command": "bash tools/check-bota-export.sh", "exit": proc.returncode, "totalChecks": len(LABELS)},
        "checks": checks,
        "counts": {
            "heroes": counts.get("active_heroes"), "abilities": counts.get("ability_rows"),
            "voice": counts.get("voice_rows"), "gallery": counts.get("gallery_images"),
            "decisions": len(decisions.get("decisions", [])) if isinstance(decisions, dict) else None,
            "markers": decisions.get("marker_scan", {}).get("covered") if isinstance(decisions, dict) else None,
            "gatedFields": field_index.get("count") if isinstance(field_index, dict) else None,
            "hashes": len(hashes) if isinstance(hashes, dict) else None,
        },
        "canonicalImmutability": {
            "canonicalEngineUnchanged": canonical_unchanged,
            "engineResolvedExists": engine_resolved_exists,
            "doNotPromote": True,
        },
        "liveOscraftConformance": live,
        "keyManifests": manifests,
        "drift": drift,
        "status": "PASS" if proc.returncode == 0 and not drift else "DRIFT",
    }
    STATUS.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n")
    print(f"WATCH_STATUS={status['status']} PIPELINE_EXIT={proc.returncode} CHECKS={len(checks)} DRIFT={len(drift)}")
    print(f"COUNTS heroes={status['counts']['heroes']} abilities={status['counts']['abilities']} voice={status['counts']['voice']} gallery={status['counts']['gallery']} decisions={status['counts']['decisions']} markers={status['counts']['markers']} gatedFields={status['counts']['gatedFields']} hashes={status['counts']['hashes']}")
    print(f"CANONICAL_ENGINE_UNCHANGED={'true' if canonical_unchanged else 'false'} ENGINE_RESOLVED_EXISTS={str(engine_resolved_exists).lower()}")
    print(f"LIVE={live['status']} drift={live['drift']} key_diff={live['cross_project_key_diff']}")
    print(f"STATUS_FILE=export/export-status.json")
    return 0 if status["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
