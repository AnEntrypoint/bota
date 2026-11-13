#!/usr/bin/env python3
"""Validate deterministic, contract-safe generated engine data."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
ENGINE = EXPORT / "engine"
FILES = ["heroes.json", "abilities.json", "voice.json", "portraits.json", "manifest.json"]
MARKER_RE = re.compile(r"GUESS|UNVERIFIED|AMBIGUOUS")
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
errors: list[str] = []
checks = 0


def ok() -> None:
    global checks
    checks += 1


def err(message: str) -> None:
    errors.append(message)


def load(path: Path, label: str):
    try:
        data = json.loads(path.read_text())
        ok()
        return data
    except Exception as exc:
        err(f"{label}: parse/read failed: {exc}")
        return None


conformance = load(EXPORT / "conformance.json", "conformance.json")
sums = load(EXPORT / "SHA256SUMS.json", "SHA256SUMS.json")
decisions = load(EXPORT / "decisions.json", "decisions.json")
contract = load(EXPORT / "integration-contract.json", "integration-contract.json")
engine = {name: load(ENGINE / name, f"engine/{name}") for name in FILES}
ACTIVE = (conformance or {}).get("active_acronyms", [])
gated_ids = set((decisions or {}).get("unresolvable_owner_decisions", [])) | set((decisions or {}).get("intentionally_open", []))
known_ids = {d.get("id") for d in (decisions or {}).get("decisions", [])}

# Required engine files and exact active key sets.
for name, data in engine.items():
    if data is None:
        continue
    heroes = data.get("heroes")
    if name != "manifest.json":
        if not isinstance(heroes, dict) or sorted(heroes) != sorted(ACTIVE):
            err(f"engine/{name}: heroes keys differ from 26 active acronyms")
        else:
            ok()
        for key in heroes or {}:
            if not re.match(r"^[a-z]{3}$", key) or key.lower() in FORBIDDEN or re.match(r"^\d{3}-", key):
                err(f"engine/{name}: forbidden active key {key}")
        if all(re.match(r"^[a-z]{3}$", k) and k.lower() not in FORBIDDEN for k in (heroes or {})):
            ok()

# Engine heroes cross-reference the other three generated surfaces.
heroes = engine.get("heroes.json") or {}
for a in ACTIVE:
    h = heroes.get("heroes", {}).get(a, {})
    for field, expected in [("abilities", "abilities.json"), ("voice", "voice.json"), ("portrait", "portraits.json")]:
        if expected not in str(h.get(field, "")):
            err(f"engine heroes.{a}.{field} does not reference {expected}")
        else:
            ok()
    if h.get("slot") != (conformance or {}).get("acronym_to_slot", {}).get(a):
        err(f"engine heroes.{a}.slot mismatch")
    else:
        ok()

# Counts: 26 heroes, 104 abilities, 50 voice rows, 27 gallery, 12 decisions, 169 markers.
abilities = engine.get("abilities.json") or {}
ability_rows = sum(len(v) for v in abilities.get("heroes", {}).values())
with (EXPORT / "voice.tsv").open(newline="") as handle:
    import csv
    voice_rows = len(list(csv.DictReader(handle, delimiter="\t")))
live_counts = {
    "active_heroes": len(ACTIVE), "ability_rows": ability_rows, "voice_rows": voice_rows,
    "gallery_images": len(list((ROOT / "gallery").glob("*.jpg"))),
    "active_gallery_images": len((engine.get("portraits.json") or {}).get("heroes", {})),
    "decisions": len((decisions or {}).get("decisions", [])),
    "covered_markers": (decisions or {}).get("marker_scan", {}).get("covered"),
    "raw_markers": (decisions or {}).get("marker_scan", {}).get("markers"),
    "export_hash_files": len(sums or {}),
    "engine_files": len(list(ENGINE.glob("*.json"))),
    "decision_packet_fields": (load(EXPORT / "field-index.json", "field-index.json") or {}).get("count"),
    "decision_packet_decisions": len((load(EXPORT / "decision-packet.json", "decision-packet.json") or {}).get("decisions", [])),
}
for key, expected in (conformance or {}).get("expected_counts", {}).items():
    if live_counts.get(key) != expected:
        err(f"count {key}: {live_counts.get(key)} != {expected}")
    else:
        ok()

# Source hashes in engine manifest match SHA256SUMS.json.
manifest = engine.get("manifest.json") or {}
source_hashes = manifest.get("source_hashes", {})
for name, digest in source_hashes.items():
    if (sums or {}).get(name) != digest:
        err(f"engine manifest source hash mismatch for {name}")
    else:
        ok()
if len(source_hashes) != 7:
    err(f"engine manifest has {len(source_hashes)} source hashes, expected 7")
else:
    ok()

# Recursive canonical-value scan: marker strings are only legal in provenance fields.
allowed_marker_keys = {"status", "statement", "options", "source", "options_ref", "generated_from", "rule", "confidence_policy"}
gated_count = 0
def walk(node, path_parts, in_gate=False):
    global gated_count
    if isinstance(node, dict):
        # A gate object must be null-valued, carry decisionId/status/source and do_not_promote.
        if "value" in node and "decisionId" in node:
            gated_count += 1
            in_gate = True
            did = node.get("decisionId")
            if node.get("value") is not None:
                err(f"gated field promoted a value: {'.'.join(path_parts)}")
            elif did not in known_ids:
                err(f"gated field unknown decisionId {did}: {'.'.join(path_parts)}")
            elif node.get("do_not_promote") is not True:
                err(f"gated field lacks do_not_promote: {'.'.join(path_parts)}")
            elif not all(k in node for k in ["status", "options", "source"]):
                err(f"gated field lacks status/options/source: {'.'.join(path_parts)}")
            else:
                ok()
        for k, v in node.items():
            walk(v, path_parts + [k], in_gate)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path_parts + [str(i)], in_gate)
    elif isinstance(node, str) and MARKER_RE.search(node):
        key = path_parts[-1] if path_parts else ""
        if key not in allowed_marker_keys and not in_gate and "GUESS/UNVERIFIED/AMBIGUOUS" not in node:
            err(f"marker used as canonical value at {'.'.join(path_parts)}: {node[:80]}")
for name, data in engine.items():
    if data:
        walk(data, [f"engine/{name}"])

# Every owner-decision and intentionally-open ID is represented with do_not_promote.
blob = json.dumps(engine)
for did in sorted(gated_ids):
    if did not in blob or f'"decisionId": "{did}"' not in blob:
        err(f"gated decision {did} not represented in engine output")
    else:
        ok()

# 003 discrepancy and no retired active key.
retired = heroes.get("retired_visual_reference", {})
if retired.get("slot") == "003" and retired.get("status") == "image-only retired/reserve" and retired.get("not_a_hero_key") is True and retired.get("do_not_promote") is True:
    ok()
else:
    err("engine heroes.json does not preserve 003 image-only retired/reserve note")

# Contract paths resolve to the engine output files.
for rel in (contract or {}).get("authority", {}).get("required_files", []):
    if not (ROOT / rel).is_file():
        err(f"contract required file missing: {rel}")

print(f"ENGINE_COUNTS: heroes={live_counts['active_heroes']} abilities={live_counts['ability_rows']} voice={live_counts['voice_rows']} gallery={live_counts['gallery_images']} decisions={live_counts['decisions']} markers={live_counts['covered_markers']}/{live_counts['raw_markers']} hashes={live_counts['export_hash_files']}")
print(f"ENGINE_GATED_FIELDS={gated_count}")
if errors:
    for e in errors:
        print(f"error: {e}")
    print(f"ENGINE VALIDATION: FAIL ({checks} checks, {len(errors)} errors)")
    sys.exit(1)
print(f"ENGINE VALIDATION: PASS ({checks} checks, 0 errors)")
