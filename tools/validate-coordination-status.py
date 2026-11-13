#!/usr/bin/env python3
"""Validate export/coordination-status.json against live peer evidence."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"
HY3D = Path("/workspace/hy3d")
WS = Path("/workspace/wscheppity")
OS = Path("/workspace/oscraft/scenarios/bota")
EXTRA = Path("/workspace/extra")
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
        err(f"{label}: parse/read failed {path}: {exc}"); return None


def sha(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


status = load(E / "coordination-status.json", "coordination-status.json")
queue = load(E / "content-request-queue.json", "content-request-queue.json") or {}
gaps = load(E / "spawn-extraction-gaps.json", "spawn-extraction-gaps.json") or {}
hy_contract = load(HY3D / "output/content-for-bota.json", "hy3d content") or {}
hy_demand = load(HY3D / "output/content-demand-v2.json", "hy3d demand-v2") or {}
ws_all = load(WS / ".local/cdn/manifest-all.json", "ws cdn-all") or {}
ws_extract = load(WS / ".local/extraction-manifest.json", "ws extraction") or {}
os_ui = load(OS / "bota_ui.json", "oscraft ui") or {}
os_snapshot = load(OS / "cross-contract-snapshot.json", "oscraft snapshot") or {}
active_roster = load(E / "active-roster.json", "bota active roster") or {}
extra_all = load(EXTRA / ".local/cdn/manifest-all.json", "extra cdn-all") or {}
extra_active = load(EXTRA / ".local/cdn/manifest.json", "extra cdn-active") or {}
identifiers = (OS / "IDENTIFIERS.md").read_text() if (OS / "IDENTIFIERS.md").is_file() else ""

rows = (status or {}).get("rows", [])
counts = (status or {}).get("counts", {})

if len(rows) == len(queue.get("rows", [])) + len(gaps.get("rows", [])) and counts.get("rows") == len(rows):
    ok()
else:
    err(f"row count mismatch: status={len(rows)} queues={len(queue.get('rows',[]))+len(gaps.get('rows',[]))}")
live_status = {s: sum(r.get("status") == s for r in rows) for s in ["available", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open", "UNAVAILABLE"]}
if all(counts.get(k) == v for k, v in live_status.items()):
    ok()
else:
    err(f"status counts do not reconcile: {counts} vs {live_status}")
if (status or {}).get("peerCounts", {}).get("hy3d", {}).get("contractRows") == hy_contract.get("counts", {}).get("rows"):
    ok()
else:
    err("hy3d contract row count mismatch")
if (status or {}).get("peerCounts", {}).get("wscheppity", {}).get("allNames") in {ws_all.get("uniqueNames"), ws_all.get("count")}:
    ok()
else:
    err("wscheppity CDN name count mismatch")

expected_ids = [r.get("stableId") for r in queue.get("rows", [])] + [r.get("stableId") for r in gaps.get("rows", [])]
actual_ids = [r.get("stableId") for r in rows]
if sorted(expected_ids) == sorted(actual_ids) and len(actual_ids) == len(set(actual_ids)):
    ok()
else:
    err("orphan or duplicate queue rows in coordination status")

published_hashes = set()
for doc in [hy_contract, hy_demand, ws_all, extra_all, extra_active]:
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in {"sha256", "destinationSha256", "destinationHash", "sourceSha256", "localSha256"} and isinstance(v, str) and SHA_RE.match(v): published_hashes.add(v)
                walk(v)
        elif isinstance(node, list):
            for v in node: walk(v)
    walk(doc)
for r in rows:
    slug = r.get("demandSlug", "")
    st = r.get("status")
    ev = r.get("evidence", {})
    if not any(x in slug.lower() for x in FORBIDDEN) and not OLD_SLUG.match(slug) and r.get("identifierSafe") is True:
        ok()
    else:
        err(f"active retired/reserve/old-slug key: {slug}")
    if not r.get("stableId") or not r.get("nextActor") or not r.get("ruleCitation") or not ev.get("paths"):
        err(f"row lacks stableId/nextActor/citation/evidence paths: {slug}")
    else:
        ok()
    if st == "available":
        digest = ev.get("sha256") or r.get("validation", {}).get("sha256")
        paths = [Path(x) for x in ev.get("paths", []) if Path(x).is_file()]
        if isinstance(digest, str) and SHA_RE.match(digest) and digest in published_hashes and any(sha(p) == digest for p in paths):
            ok()
        else:
            err(f"available hash does not match a real file: {slug} {digest}")
    elif st == "spawn-generated":
        v = r.get("validation", {})
        http = ev.get("http") or {}
        if v.get("exactGeneratedOnDemandEvidence") and "status" in http and "contentType" in http and "bodySize" in http and "sha256" in http and ev.get("paths"):
            ok()
        else:
            err(f"spawn-generated lacks exact HTTP evidence: {slug}")
    elif st in {"owner-decision", "intentionally-open"}:
        if r.get("decisionId") and "decision-packet.json" in json.dumps(ev) or (st == "intentionally-open" and r.get("decisionId") and "plan/" in json.dumps(ev)):
            ok()
        else:
            err(f"{st} lacks decision id/citation: {slug}")
    elif st in {"requested-pooled-email", "requested-relay"}:
        if r.get("nextActor") == "hy3d" and any("hy3d" in x for x in ev.get("paths", [])):
            ok()
        else:
            err(f"{st} lacks hy3d evidence: {slug}")
    elif st == "UNAVAILABLE":
        err(f"unexplained UNAVAILABLE row: {slug}")
    else:
        err(f"unknown status {st}: {slug}")

if (status or {}).get("identifierMode") == "bota-fullname" and os_ui.get("identifierMode") == "bota-fullname" and "bota-fullname" in identifiers:
    ok()
else:
    err("oscraft BOTA identifier mode mismatch")
if (status or {}).get("defaultDotaAcronyms") is True and os_snapshot.get("identifierMode", {}).get("defaultDota") == "default-dota-acronyms" and os_snapshot.get("counts", {}).get("botaFullnameIds") == active_roster.get("activeHeroCount"):
    ok()
else:
    err("oscraft default Dota acronym expectation mismatch")
if not (E / "engine-resolved").exists() and (status or {}).get("engineResolvedExists") is False:
    ok()
else:
    err("engine-resolved exists or status gate mismatch")

print("COORDINATION_STATUS_COUNTS " + " ".join(f"{k}={v}" for k, v in live_status.items()))
print(f"COORDINATION_ROWS rows={len(rows)} resolved={counts.get('resolved')} unresolved={counts.get('unresolved')} unexplained={counts.get('unexplainedUnavailable')}")
for e in errors: print(f"error: {e}")
if errors:
    print(f"COORDINATION STATUS: FAIL ({checks} checks, {len(errors)} errors)")
    sys.exit(1)
print(f"COORDINATION STATUS: PASS ({checks} checks, 0 errors)")
