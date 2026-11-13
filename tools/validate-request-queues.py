#!/usr/bin/env python3
"""Validate BOTA v2 rule demand and peer request queues."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"
HY3D = Path("/workspace/hy3d")
WS = Path("/workspace/wscheppity")
EXTRA = Path("/workspace/extra")
STATUSES = {"available", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open"}
ACTORS = {"hy3d", "wscheppity", "extra", "owner", "bota"}
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
OLD_SLUG = re.compile(r"^\d{3}-")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
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
        err(f"{label}: JSON parse/read failed {path}: {exc}"); return None


def tsv_rows(path: Path, label: str):
    try:
        with path.open(newline="") as h:
            rows = list(csv.DictReader(h, delimiter="\t"))
        ok(); return rows
    except Exception as exc:
        err(f"{label}: TSV parse/read failed {path}: {exc}"); return []


def sha(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def real_path(value: str | None) -> bool:
    if not value:
        return False
    p = Path(value)
    return p.is_file() if p.is_absolute() else (ROOT / p).is_file() or (HY3D / p).is_file() or (WS / p).is_file()


def published_hashes() -> set[str]:
    out: set[str] = set()
    paths = [
        HY3D / "output/content-for-bota.json", HY3D / "output/final-asset-inventory.json",
        HY3D / "output/generation-status.json", HY3D / "output/studio-blocked-diagnosis.json",
        WS / ".local/extraction-manifest.json", WS / ".local/cdn/manifest.json", WS / ".local/cdn/manifest-all.json", EXTRA / ".local/extraction-manifest.json", EXTRA / ".local/cdn/manifest.json", EXTRA / ".local/cdn/manifest-all.json",
    ]
    for p in paths:
        if not p.is_file():
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        def walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k in {"sha256", "sourceSha256", "destSha256", "destinationSha256", "destinationHash", "localSha256"} and isinstance(v, str) and SHA_RE.match(v):
                        out.add(v)
                    walk(v)
            elif isinstance(node, list):
                for v in node: walk(v)
        walk(d)
    return out


prior = load(E / "rule-demand-prior.json", "prior")
demand = load(E / "rule-demand.json", "demand")
queue = load(E / "content-request-queue.json", "content-request-queue")
gaps = load(E / "spawn-extraction-gaps.json", "spawn-extraction-gaps")
demand_tsv = tsv_rows(E / "rule-demand.tsv", "rule-demand.tsv")
queue_tsv = tsv_rows(E / "content-request-queue.tsv", "content-request-queue.tsv")
hashes = load(E / "SHA256SUMS.json", "SHA256SUMS.json")
sums = published_hashes()

# JSON/TSV row parity.
if demand and len(demand_tsv) == len(demand.get("rows", [])) and [x["slug"] for x in demand_tsv] == [x["slug"] for x in demand["rows"]]:
    ok()
else:
    err("rule-demand TSV parity failed")
if queue and len(queue_tsv) == len(queue.get("rows", [])) and [x["stableId"] for x in queue_tsv] == [x["stableId"] for x in queue["rows"]]:
    ok()
else:
    err("content-request-queue TSV parity failed")

# Every prior requested/blocked row is exactly once in a queue or now available.
prior_non = [r for r in (prior or {}).get("rows", []) if r.get("status") in {"requested", "blocked"}]
drows = (demand or {}).get("rows", [])
dmap = {r["slug"]: r for r in drows}
hy_ids = {r.get("demandSlug") for r in (queue or {}).get("rows", [])}
ws_ids = {r.get("demandSlug") for r in (gaps or {}).get("rows", [])}
for r in prior_non:
    slug = r["slug"]
    row = dmap.get(slug)
    if not row:
        err(f"prior row missing from v2 demand: {slug}"); continue
    in_q = int(slug in hy_ids) + int(slug in ws_ids)
    if row["status"] == "available":
        # Verified extraction evidence may remain in the wscheppity evidence index;
        # it is not an open queue item. Actionable queues are non-available only.
        actionable_q = {r.get("demandSlug") for r in (queue or {}).get("rows", []) if r.get("status") != "available"} | {r.get("demandSlug") for r in (gaps or {}).get("rows", []) if r.get("status") != "available"}
        if slug in actionable_q:
            err(f"available prior row also in an actionable queue: {slug}")
        else:
            ok()
    elif in_q != 1:
        err(f"prior non-available row not represented exactly once: {slug} queues={in_q} status={row['status']}")
    else:
        ok()
# Exact once also checks queue duplicates.
for label, rows in [("hy3d", (queue or {}).get("rows", [])), ("wscheppity", (gaps or {}).get("rows", []))]:
    ids = [r.get("stableId") for r in rows]
    slugs = [r.get("demandSlug") for r in rows]
    if len(ids) == len(set(ids)) and len(slugs) == len(set(slugs)):
        ok()
    else:
        err(f"{label} queue has duplicate stableId or demandSlug")

# Queue row shape, stable IDs, actor, citation, evidence, acceptance and no invented hashes.
def validate_queue_row(label: str, r: dict) -> None:
    required = ["stableId", "queue", "priority", "demandSlug", "status", "nextActor", "ruleCitation", "ruleQuote", "evidence", "validation", "acceptanceCriteria", "note"]
    shape_ok = all((r.get(k) is not None and r.get(k) != "" and r.get(k) != []) for k in required)
    if r.get("status") == "spawn-generated" and not r.get("sourcePath") and r.get("sourceUrl"):
        shape_ok = True  # exact HTTP/URL evidence is sufficient; local bytes are the gap.
    if shape_ok and r["status"] in STATUSES and r["nextActor"] in ACTORS:
        ok()
    else:
        err(f"{label} row shape invalid: {r.get('stableId')}")
    sid = r.get("stableId", "")
    if sid.startswith(("queue:", "ws:", "extra:")) and re.match(r"^[a-z]+:[a-f0-9]{16}$", sid):
        ok()
    else:
        err(f"{label} unstable id: {sid}")
    citation = r.get("ruleCitation", "")
    m = re.match(r"^(plan/[^:]+):(\d+)$", citation)
    if m and (ROOT / m.group(1)).is_file() and r.get("ruleQuote"):
        lines = (ROOT / m.group(1)).read_text().splitlines()
        if 1 <= int(m.group(2)) <= len(lines) and r["ruleQuote"] in lines[int(m.group(2)) - 1]:
            ok()
        else:
            err(f"{label} citation quote mismatch: {sid} {citation}")
    else:
        err(f"{label} invalid plan citation: {sid} {citation}")
    if r.get("evidence") and isinstance(r.get("validation"), dict) and r["validation"] and r.get("acceptanceCriteria"):
        ok()
    else:
        err(f"{label} missing evidence/validation/acceptance: {sid}")
    # No active retired/reserve/old-slug key except the explicit 003 visual reference.
    slug = r.get("demandSlug", "")
    bad = [x for x in FORBIDDEN if x in slug.lower() and "visual-reference/003-gigachad" not in slug]
    if not bad and not OLD_SLUG.match(slug):
        ok()
    else:
        err(f"{label} retired/reserve/old-slug active key: {slug}")
    digest = r.get("sourceHash") or ((r.get("validation") or {}).get("sha256") if isinstance(r.get("validation"), dict) else None)
    if digest:
        if isinstance(digest, str) and SHA_RE.match(digest) and digest in sums:
            ok()
        else:
            err(f"{label} invented asset hash: {sid} {digest}")
    else:
        ok()

for r in (queue or {}).get("rows", []): validate_queue_row("hy3d", r)
for r in (gaps or {}).get("rows", []): validate_queue_row("wscheppity", r)

# Demand rows: status valid, available rows grounded, spawn-generated rows have no fake hash.
for r in drows:
    if r.get("status") in STATUSES and r.get("nextActor") in ACTORS:
        ok()
    else:
        err(f"demand invalid status/actor: {r.get('slug')} {r.get('status')} {r.get('nextActor')}")
    digest = r.get("sourceHash")
    if r.get("status") == "available":
        linked = dmap.get(r.get("sourcePath", ""))
        if isinstance(digest, str) and SHA_RE.match(digest) and (digest in sums or (real_path(r.get("sourcePath")) and sha(Path(r["sourcePath"]) if Path(r.get("sourcePath","")).is_absolute() else ROOT / r["sourcePath"]) == digest)):
            ok()
        elif linked and linked.get("status") == "available" and linked.get("sourceHash") in sums:
            ok()
        else:
            err(f"available demand hash not grounded: {r.get('slug')} {digest}")
    elif r.get("status") == "spawn-generated":
        if not digest:
            ok()
        else:
            err(f"spawn-generated row has an invented hash: {r.get('slug')}")
    else:
        ok()

# Counts reconcile and SHA256SUMS covers all new top-level export files.
if demand:
    counts = demand.get("counts", {})
    live = {s: sum(r["status"] == s for r in drows) for s in STATUSES}
    if all(counts.get(s) == live[s] for s in STATUSES) and counts.get("rows") == len(drows):
        ok()
    else:
        err(f"demand counts do not reconcile: {counts} vs {live}")
if queue and gaps:
    qc = queue.get("counts", {}); gc = gaps.get("counts", {})
    if qc.get("rows") == len(queue.get("rows", [])) and gc.get("rows") == len(gaps.get("rows", [])):
        ok()
    else:
        err("queue/gap counts do not reconcile")
    all_names = {r.get("sourceUrl") for r in gaps.get("rows", []) if r.get("sourceUrl") and r.get("peer") != "extra"}
    extra_names = {r.get("sourceUrl") for r in gaps.get("rows", []) if r.get("sourceUrl") and r.get("peer") == "extra"}
    if gc.get("allCdnNames") == len(all_names) and gc.get("extraCdnNames") == len(extra_names) and gc.get("rows") == len(gaps.get("rows", [])) and gc.get("rows") == gc.get("wscheppityRows", 0) + gc.get("extraRows", 0):
        ok()
    else:
        err("spawn-extraction-gaps does not cover all CDN names by peer")
for name in ["rule-demand.json", "rule-demand.tsv", "content-request-queue.json", "content-request-queue.tsv", "spawn-extraction-gaps.json", "rule-demand-prior.json"]:
    if hashes and name in hashes and (E / name).is_file() and sha(E / name) == hashes[name]:
        ok()
    else:
        err(f"SHA256SUMS missing/stale for {name}")

print("REQUEST_QUEUE_COUNTS " + " ".join(f"{s}={sum(r['status']==s for r in drows)}" for s in sorted(STATUSES)))
print(f"PRIOR_RECONCILIATION rows={len(prior_non)} hy3d_queue={len((queue or {}).get('rows',[]))} spawn_gaps={len((gaps or {}).get('rows',[]))} demand_rows={len(drows)}")
for e in errors: print(f"error: {e}")
if errors:
    print(f"REQUEST QUEUES: FAIL ({checks} checks, {len(errors)} errors)")
    sys.exit(1)
print(f"REQUEST QUEUES: PASS ({checks} checks, 0 errors)")
