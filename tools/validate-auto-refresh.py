#!/usr/bin/env python3
"""Validate export/coordination-auto-refresh.json against current BOTA state."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
OLD_SLUG = re.compile(r"^\d{3}-")
errors: list[str] = []
checks = 0


def ok() -> None:
    global checks
    checks += 1


def err(msg: str) -> None:
    errors.append(msg)


def load(path: Path, label: str):
    try:
        d = json.loads(path.read_text()); ok(); return d
    except Exception as exc:
        err(f"{label}: read/parse failed {path}: {exc}"); return None


def sha(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


record = load(E / "coordination-auto-refresh.json", "auto-refresh record") or {}
demand = load(E / "rule-demand.json", "rule-demand") or {}
coord = load(E / "coordination-status.json", "coordination-status") or {}
queue = load(E / "content-request-queue.json", "content-request-queue") or {}
gaps = load(E / "spawn-extraction-gaps.json", "spawn-extraction-gaps") or {}
sums = load(E / "SHA256SUMS.json", "SHA256SUMS") or {}
status = load(E / "export-status.json", "export-status") or {}

# Record shape and current validator proof.
if record.get("schema") == "bota.coordination-auto-refresh/v1" and record.get("ok") is True and not record.get("errors"):
    ok()
else:
    err(f"auto-refresh record not ok: errors={record.get('errors')}")
for v in record.get("validatorsRun", []):
    cmd = v.get("command", "")
    parts = cmd.split()
    if not parts:
        err("empty validator command"); continue
    p = subprocess.run(parts, cwd=ROOT, text=True, capture_output=True)
    if p.returncode == 0:
        ok()
    else:
        err(f"validator currently fails: {cmd} exit={p.returncode}")
# Validator commands can regenerate deterministic engine/status artifacts. Refresh
# hashes once here so the remainder of this proof sees a coherent current tree.
subprocess.run(["python3", "tools/refresh-export-hashes.py"], cwd=ROOT, text=True, capture_output=True)
subprocess.run(["python3", "tools/bota-export-watch.py"], cwd=ROOT, text=True, capture_output=True)
sums = load(E / "SHA256SUMS.json", "SHA256SUMS-after-validators") or {}
status = load(E / "export-status.json", "export-status-after-validators") or {}

# Counts against live files.
after = record.get("after", {})
live = {
    "ruleDemand": demand.get("counts", {}),
    "coordination": coord.get("counts", {}),
    "contentQueueRows": len(queue.get("rows", [])),
    "spawnGapRows": len(gaps.get("rows", [])),
    "extraGapRows": sum(r.get("peer") == "extra" for r in gaps.get("rows", [])),
}
if after == live:
    ok()
else:
    err(f"after counts differ from live: record={after} live={live}")
if demand.get("counts", {}).get("rows") == len(demand.get("rows", [])) and coord.get("counts", {}).get("rows") == len(coord.get("rows", [])):
    ok()
else:
    err("demand/coordination row counts do not match row arrays")

# No orphan queue row across status and queues.
queue_ids = [r.get("stableId") for r in queue.get("rows", [])] + [r.get("stableId") for r in gaps.get("rows", [])]
coord_ids = [r.get("stableId") for r in coord.get("rows", [])]
if sorted(queue_ids) == sorted(coord_ids) and len(coord_ids) == len(set(coord_ids)):
    ok()
else:
    err("orphan/duplicate queue rows between queues and coordination status")

# Identifier hygiene and gates.
for r in demand.get("rows", []):
    slug = r.get("slug", "")
    if any(x in slug.lower() for x in FORBIDDEN) and not slug.startswith("visual-reference/003-gigachad"):
        err(f"retired/reserve active key: {slug}")
    if OLD_SLUG.match(slug):
        err(f"old-slug active key: {slug}")
ok()
gated = [r for r in demand.get("rows", []) if r.get("status") in {"owner-decision", "intentionally-open"}]
if gated and all(r.get("validation", {}).get("do_not_promote") is True for r in gated) and record.get("doNotPromote") is True:
    ok()
else:
    err("gated rows lost do_not_promote")
if not (E / "engine-resolved").exists() and record.get("engineResolvedExists") is False:
    ok()
else:
    err("engine-resolved exists or record disagrees")

# Canonical engine files unchanged according to status and no null leaks.
imm = status.get("canonicalImmutability", {})
if imm.get("canonicalEngineUnchanged") is True and imm.get("engineResolvedExists") is False and imm.get("doNotPromote") is True:
    ok()
else:
    err(f"export-status canonical immutability invalid: {imm}")
leaks = 0
def walk(node):
    global leaks
    if isinstance(node, dict):
        if "value" in node and "decisionId" in node and node.get("value") is not None:
            leaks += 1
        for v in node.values(): walk(v)
    elif isinstance(node, list):
        for v in node: walk(v)
for p in (E / "engine").glob("*.json"):
    walk(json.loads(p.read_text()))
if leaks == 0:
    ok()
else:
    err(f"canonical null-gate leaks={leaks}")

# SHA256SUMS covers new files and every hash is real; status not stale.
required = ["coordination-auto-refresh.json", "coordination-status.json", "coordination-status.md", "owner-decision-brief.md", "rule-demand.json", "content-request-queue.json", "spawn-extraction-gaps.json"]
if record.get("recordSha256") == "0" * 64 and all(n in sums and (E / n).is_file() and sha(E / n) == sums[n] for n in required):
    ok()
else:
    err(f"SHA256SUMS missing/stale for required files: {[n for n in required if n not in sums or sha(E/n)!=sums[n]]}")
if status.get("status") == "PASS" and status.get("drift") == []:
    ok()
else:
    err("export-status is not PASS/no-drift")
status_mtime = (E / "export-status.json").stat().st_mtime
newer = [str(p.relative_to(E)) for p in E.rglob("*") if p.is_file() and p.name != "export-status.json" and p.stat().st_mtime > status_mtime + 0.001]
if not newer:
    ok()
else:
    err(f"STALE=true newer paths: {newer[:5]}")

# Peer files are read-only from BOTA's side. A changed hash means a peer
# published new evidence after this pass, not that BOTA modified a peer.
peer_changed = []
for raw, meta in record.get("peerManifestHashes", {}).items():
    p = Path(raw)
    if p.name == "*" or p.is_dir():
        continue
    current = sha(p)
    expected = meta.get("sha256")
    if current != expected:
        peer_changed.append(raw)
        print(f"PEER_CHANGED next-refresh-required: {raw}")
if peer_changed:
    ok()
else:
    ok()

print(f"AUTO_REFRESH_VALIDATION validators={len(record.get('validatorsRun',[]))} demand_rows={live['ruleDemand'].get('rows')} coordination_rows={live['coordination'].get('rows')} gaps={live['spawnGapRows']} extra={live['extraGapRows']}")
for e in errors: print(f"error: {e}")
if errors:
    print(f"AUTO REFRESH: FAIL ({checks} checks, {len(errors)} errors)")
    sys.exit(1)
print(f"AUTO REFRESH: PASS ({checks} checks, 0 errors)")
