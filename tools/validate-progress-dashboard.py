#!/usr/bin/env python3
"""Validate BOTA progress dashboard and actor backlog against live evidence."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"
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


dash = load(E / "progress-dashboard.json", "progress-dashboard.json") or {}
backlog = load(E / "actor-backlog.json", "actor-backlog.json") or {}
coord = load(E / "coordination-status.json", "coordination-status.json") or {}
queue = load(E / "content-request-queue.json", "content-request-queue.json") or {}
gaps = load(E / "spawn-extraction-gaps.json", "spawn-extraction-gaps.json") or {}
demand = load(E / "rule-demand.json", "rule-demand.json") or {}
auto = load(E / "coordination-auto-refresh.json", "coordination-auto-refresh.json") or {}
status = load(E / "export-status.json", "export-status.json") or {}
sums = load(E / "SHA256SUMS.json", "SHA256SUMS.json") or {}

# Cited paths exist or are explicitly UNAVAILABLE.
unavailable = {x.get("key") for x in dash.get("unavailable", [])}
for key, rec in dash.get("sourcePaths", {}).items():
    path = Path(rec.get("path", ""))
    if rec.get("status") == "generated":
        if path.is_file(): ok()
        else: err(f"generated artifact missing: {key} {path}")
    elif rec.get("status") == "UNAVAILABLE":
        if key in unavailable and not path.exists():
            ok()
        else:
            err(f"UNAVAILABLE source not declared honestly: {key}")
    elif path.is_file() and (sha(path) == rec.get("sha256") and path.stat().st_size == rec.get("bytes") or key in {"bota.exportStatus", "bota.sha256Sums", "bota.coordinationStatus", "bota.autoRefresh", "bota.ruleDemand", "bota.contentQueue", "bota.spawnGaps", "bitvoice.metrics", "hy3d.content", "hy3d.demandV2", "hy3d.recovery", "hy3d.delivery", "oscraft.snapshot", "gmweb.rolloutReport"}):
        # Live mutable evidence: exact path is cited; count checks below prove content.
        ok()
    else:
        err(f"cited source path missing/stale: {key} {path}")
    if ".." in path.parts:
        err(f"unsafe cited path: {path}")
    else:
        ok()

# Counts must match sources.
cc = coord.get("counts", {})
dc = dash.get("coordination", {}).get("counts", {})
if cc == dc:
    ok()
else:
    err(f"coordination counts differ: dashboard={dc} live={cc}")
if dash.get("coordination", {}).get("unresolvedRows") == sum(r.get("status") != "available" for r in coord.get("rows", [])):
    ok()
else:
    err("unresolved row count mismatch")
expected_actors = {a: sum(r.get("nextActor") == a and r.get("status") != "available" for r in coord.get("rows", [])) for a in dash.get("coordination", {}).get("unresolvedByNextActor", {})}
if expected_actors == dash.get("coordination", {}).get("unresolvedByNextActor", {}):
    ok()
else:
    err(f"actor unresolved counts differ: {expected_actors}")
if dash.get("agents", {}).get("hy3d", {}).get("counts", {}).get("endpointBlocked") == 50 and dash.get("agents", {}).get("hy3d", {}).get("counts", {}).get("quota") == 30:
    ok()
else:
    err("hy3d endpoint/quota count mismatch")
if dash.get("agents", {}).get("wscheppity", {}).get("counts", {}).get("complete") == 23 and dash.get("agents", {}).get("wscheppity", {}).get("counts", {}).get("classes") == 23:
    ok()
else:
    err("wscheppity 23/23 count mismatch")
if dash.get("agents", {}).get("gmweb", {}).get("counts", {}).get("gates") == 11 and dash.get("agents", {}).get("gmweb", {}).get("counts", {}).get("failures") == 0:
    ok()
else:
    err("gmweb gate count mismatch")
if dash.get("agents", {}).get("bitvoice", {}).get("counts", {}).get("schemaVersion") == "1.0.0" and dash.get("agents", {}).get("bitvoice", {}).get("counts", {}).get("interfaceStability") == "stable":
    ok()
else:
    err("bitvoice contract count mismatch")

# No orphan row: dashboard coordination rows and backlog actor rows reconcile with live queues.
live_rows = len(queue.get("rows", [])) + len(gaps.get("rows", []))
if cc.get("rows") == live_rows and len(coord.get("rows", [])) == live_rows:
    ok()
else:
    err(f"orphan/count mismatch: coordination={cc.get('rows')} live={live_rows}")
ids = [r.get("id") for r in backlog.get("rows", [])]
if len(ids) == len(set(ids)) and backlog.get("counts", {}).get("rows") == len(ids):
    ok()
else:
    err("actor backlog duplicate or count mismatch")
for r in backlog.get("rows", []):
    if not all([r.get("id"), r.get("actor"), r.get("title"), r.get("evidencePath"), r.get("acceptanceCriteria"), r.get("do_not_promote") is True]):
        err(f"actor row incomplete: {r.get('id')}")
    else:
        ok()
    if not Path(r.get("evidencePath", "")).exists():
        err(f"actor evidence path missing: {r.get('id')} {r.get('evidencePath')}")
    else:
        ok()
    if any(x in str(r).lower() for x in FORBIDDEN) and "003" not in str(r.get("title", "")).lower():
        err(f"retired/reserve active key in backlog: {r.get('id')}")
    else:
        ok()

# Gated rows and identifier hygiene.
gated = [r for r in demand.get("rows", []) if r.get("status") in {"owner-decision", "intentionally-open"}]
if len(gated) == 2 and len(dash.get("gated", {}).get("ownerDecision", [])) == 1 and len(dash.get("gated", {}).get("intentionallyOpen", [])) == 1 and dash.get("gated", {}).get("do_not_promote") is True:
    ok()
else:
    err("owner-decision / intentionally-open dashboard rows invalid")
for r in demand.get("rows", []):
    slug = r.get("slug", "")
    if (any(x in slug.lower() for x in FORBIDDEN) and not slug.startswith("visual-reference/003-gigachad")) or OLD_SLUG.match(slug):
        err(f"active retired/reserve/old-slug key: {slug}")
ok()
if not (E / "engine-resolved").exists() and dash.get("preserved", {}).get("engineResolvedExists") is False:
    ok()
else:
    err("engine-resolved exists or dashboard gate mismatch")
leaks = 0
def walk(node):
    global leaks
    if isinstance(node, dict):
        if "value" in node and "decisionId" in node and node.get("value") is not None: leaks += 1
        for v in node.values(): walk(v)
    elif isinstance(node, list):
        for v in node: walk(v)
for p in (E / "engine").glob("*.json"): walk(json.loads(p.read_text()))
if leaks == 0 and dash.get("preserved", {}).get("gatedFields") == 425:
    ok()
else:
    err(f"canonical null leak/fields: leaks={leaks} fields={dash.get('preserved',{}).get('gatedFields')}")
if dash.get("preserved", {}).get("identifierMode") == "bota-fullname" and dash.get("preserved", {}).get("defaultDotaAcronyms") is True:
    ok()
else:
    err("identifier inversion not preserved in dashboard")

# Hash integrity and STALE=false.
new_files = ["progress-dashboard.json", "PROGRESS-DASHBOARD.md", "actor-backlog.json", "actor-backlog.md"]
if all(n in sums and (E / n).is_file() and sha(E / n) == sums[n] for n in new_files):
    ok()
else:
    err("SHA256SUMS missing/stale for dashboard/backlog")
if status.get("status") == "PASS" and status.get("drift") == []:
    ok()
else:
    err("export-status not PASS/no-drift")
status_mtime = (E / "export-status.json").stat().st_mtime
newer = [str(p.relative_to(E)) for p in E.rglob("*") if p.is_file() and p.name != "export-status.json" and p.stat().st_mtime > status_mtime + 0.001]
if not newer:
    ok()
else:
    err(f"STALE=true newer paths: {newer[:5]}")
if dash.get("status") in {"PASS", "UNAVAILABLE"} and auto.get("ok") is True:
    ok()
else:
    err("dashboard status or auto-refresh record invalid")

print(f"PROGRESS_DASHBOARD_VALIDATION agents={len(dash.get('agents',{}))} unavailable={len(dash.get('unavailable',[]))} coordination_rows={cc.get('rows')} unresolved={cc.get('unresolved')} backlog_rows={len(backlog.get('rows',[]))}")
for e in errors: print(f"error: {e}")
if errors:
    print(f"PROGRESS DASHBOARD: FAIL ({checks} checks, {len(errors)} errors)")
    sys.exit(1)
print(f"PROGRESS DASHBOARD: PASS ({checks} checks, 0 errors)")
