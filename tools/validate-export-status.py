#!/usr/bin/env python3
"""Validate export/export-status.json against the live BOTA export."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
STATUS_PATH = EXPORT / "export-status.json"
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
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
errors: list[str] = []
checks = 0


def ok() -> None:
    global checks
    checks += 1


def err(message: str) -> None:
    errors.append(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(rel: str):
    try:
        return json.loads((EXPORT / rel).read_text())
    except Exception as exc:
        err(f"{rel}: parse/read failed: {exc}")
        return None


status = load("export-status.json")
conf = load("conformance.json")
decisions = load("decisions.json")
field_index = load("field-index.json")
sums = load("SHA256SUMS.json")

# Schema and pipeline result.
if status and status.get("schema") == "bota.export-status/v1" and status.get("status") == "PASS" and status.get("pipeline", {}).get("exit") == 0:
    ok()
else:
    err("status schema or pipeline result invalid")
if status:
    checks_obj = status.get("checks", {})
    if sorted(checks_obj) == sorted(LABELS) and len(checks_obj) == 15:
        ok()
    else:
        err(f"status check labels differ: {sorted(checks_obj)}")
    for label in LABELS:
        c = checks_obj.get(label, {})
        if c.get("exit") == 0 and c.get("status") == "PASS":
            ok()
        else:
            err(f"status check {label} not passed: {c}")
    if status.get("drift") == []:
        ok()
    else:
        err(f"status reports drift: {status.get('drift')}")

# Counts match live manifests.
expected_counts = (conf or {}).get("expected_counts", {})
live_counts = {
    "heroes": expected_counts.get("active_heroes"),
    "abilities": expected_counts.get("ability_rows"),
    "voice": expected_counts.get("voice_rows"),
    "gallery": expected_counts.get("gallery_images"),
    "decisions": len((decisions or {}).get("decisions", [])),
    "markers": (decisions or {}).get("marker_scan", {}).get("covered"),
    "gatedFields": (field_index or {}).get("count"),
    "hashes": len(sums or {}),
}
if status:
    for key, value in live_counts.items():
        if status.get("counts", {}).get(key) == value:
            ok()
        else:
            err(f"status count {key}: {status.get('counts', {}).get(key)} != live {value}")

# SHA256SUMS integrity and status key-manifest hashes.
if sums:
    bad = [name for name, want in sums.items() if name != "export-status.json" and (not (EXPORT / name).is_file() or sha(EXPORT / name) != want)]
    if bad:
        err(f"SHA256SUMS mismatches: {bad}")
    else:
        ok()
    fixture_hashes = {k: v for k, v in sums.items() if k != "conformance.json"}
    if (conf or {}).get("expected_hashes") == fixture_hashes:
        ok()
    else:
        err("conformance expected_hashes differs from SHA256SUMS excluding self")
if status:
    manifest_hashes = status.get("keyManifests", {})
    for rel in KEY_MANIFESTS:
        if manifest_hashes.get(rel, {}).get("sha256") == sha(EXPORT / rel):
            ok()
        else:
            err(f"status key manifest hash stale: {rel}")

# Canonical immutability and no overlay leak.
imm = (status or {}).get("canonicalImmutability", {})
if imm.get("canonicalEngineUnchanged") is True and imm.get("engineResolvedExists") is False and imm.get("doNotPromote") is True and not (EXPORT / "engine-resolved").exists():
    ok()
else:
    err("canonical immutability or overlay leak invalid")

# Live oscraft conformance status.
live = (status or {}).get("liveOscraftConformance", {})
if live.get("status") == "PASS" and live.get("drift") == 0 and live.get("cross_project_key_diff") == "[]":
    ok()
else:
    err(f"live oscraft conformance invalid: {live}")

# No stale/reserve active keys.
active = set((conf or {}).get("active_acronyms", []))
bad_keys = [k for k in active if k.lower() in FORBIDDEN or re.match(r"^\d{3}-", k) or not re.match(r"^[a-z]{3}$", k)]
if len(active) == 26 and not bad_keys:
    ok()
else:
    err(f"active key hygiene failed: count={len(active)} bad={bad_keys}")

# Staleness: status generatedAt must not be older than any export file newer than status.
status_mtime = STATUS_PATH.stat().st_mtime if STATUS_PATH.exists() else 0
newer = [str(p.relative_to(EXPORT)) for p in EXPORT.rglob("*") if p.is_file() and p.name != "export-status.json" and p.stat().st_mtime > status_mtime + 0.001]
generated = None
if status:
    try:
        generated = dt.datetime.fromisoformat(status["generatedAt"].replace("Z", "+00:00")).timestamp()
    except Exception as exc:
        err(f"generatedAt invalid: {exc}")
if newer:
    err(f"STALE=true newer paths: {newer[:5]}{' …' if len(newer) > 5 else ''}")
else:
    ok()
if generated and generated >= status_mtime - 1:
    ok()
elif generated:
    err("generatedAt is older than status file mtime")

print(f"STATUS_COUNTS heroes={live_counts['heroes']} abilities={live_counts['abilities']} voice={live_counts['voice']} gallery={live_counts['gallery']} decisions={live_counts['decisions']} markers={live_counts['markers']} gatedFields={live_counts['gatedFields']} hashes={live_counts['hashes']}")
print(f"STALE={'true' if newer else 'false'} DRIFT={0 if not (status or {}).get('drift') else len(status['drift'])}")
if errors:
    for e in errors:
        print(f"error: {e}")
    print(f"EXPORT STATUS: FAIL ({checks} checks, {len(errors)} errors)")
    sys.exit(1)
print(f"EXPORT STATUS: PASS ({checks} checks, 0 errors)")
