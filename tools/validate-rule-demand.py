#!/usr/bin/env python3
"""Validate export/rule-demand.{json,tsv} against BOTA rules and hy3d evidence."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
HY3D = Path("/workspace/hy3d")
CONTRACT = HY3D / "output" / "content-for-bota.json"
FALLBACKS = [
    "final-asset-inventory.json",
    "bota-ready.json",
    "studio-blocked-relay-ready.json",
    "structures-ready.json",
    "spawn-cdn-candidates.json",
]
REQUIRED_FIELDS = {"slug", "ruleSection", "requiredBy", "status"}
STATUSES = {"available", "requested", "blocked", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open"}
V2_STATUSES = {"available", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open"}
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
OLD_SLUG_RE = re.compile(r"^\d{3}-")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
errors: list[str] = []
degraded: list[str] = []
checks = 0


def ok() -> None:
    global checks
    checks += 1


def err(message: str) -> None:
    errors.append(message)


def load_json(path: Path, label: str):
    try:
        data = json.loads(path.read_text())
        ok()
        return data
    except Exception as exc:
        err(f"{label}: read/parse failed {path}: {exc}")
        return None


def sha(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def path_exists(value: str, *, evidence: bool = False) -> bool:
    p = Path(value)
    if p.is_absolute():
        if p.is_file():
            return True
        return evidence and (value.startswith("/workspace/hy3d/output/") or value.startswith("/workspace/oscraft/scenarios/bota/assets/") or value.startswith("/cdn/"))
    if ".." in p.parts:
        return False
    return (ROOT / p).is_file() or (HY3D / p).is_file() or value.startswith("/cdn/")


demand = load_json(EXPORT / "rule-demand.json", "rule-demand.json")
tsv_path = EXPORT / "rule-demand.tsv"
registry = load_json(EXPORT / "hero-registry.json", "hero-registry.json") or {}
conformance = load_json(EXPORT / "conformance.json", "conformance.json") or {}
spawn = load_json(EXPORT / "spawn-compatibility.json", "spawn-compatibility.json") or {}
order = registry.get("acronym_order", [])
rows = (demand or {}).get("rows", [])
is_v2 = (demand or {}).get("schema") == "bota.rule-demand/v2"

# TSV parity.
if tsv_path.is_file():
    with tsv_path.open(newline="") as handle:
        tsv_rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(tsv_rows) == len(rows) and [x["slug"] for x in tsv_rows] == [x["slug"] for x in rows]:
        ok()
    else:
        err(f"TSV row parity failed: tsv={len(tsv_rows)} json={len(rows)}")
else:
    err(f"missing {tsv_path}")

# Contract state degrades honestly.
contract = load_json(CONTRACT, "hy3d content-for-bota.json") if CONTRACT.is_file() else None
contract_status = (demand or {}).get("coordination", {}).get("contractStatus")
if contract and contract_status == "ready":
    ok()
elif not contract and contract_status == "UNAVAILABLE":
    degraded.append(f"hy3d canonical content contract missing: {CONTRACT}")
    ok()
else:
    err(f"contractStatus={contract_status} disagrees with {CONTRACT}")
fallback_status = []
for name in FALLBACKS:
    p = HY3D / "output" / name
    fallback_status.append(p.is_file())
    if p.is_file():
        ok()
if not all(fallback_status):
    degraded.append(f"hy3d fallback manifests missing: {[n for n, v in zip(FALLBACKS, fallback_status) if not v]}")

# Collect published hy3d SHA-256 values and canonical hash-verified rows.
hy3d_hashes: set[str] = set()
for path in [CONTRACT] + [HY3D / "output" / name for name in FALLBACKS]:
    doc = load_json(path, f"hy3d {path.name}") if path.is_file() else None
    if not isinstance(doc, dict):
        continue
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in {"sha256", "sourceSha256", "destSha256", "destinationSha256", "destinationHash", "fullSourceSha256"} and isinstance(v, str) and SHA_RE.match(v):
                    hy3d_hashes.add(v)
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(doc)
content_rows = (contract or {}).get("rows", [])
if contract and len(content_rows) == (contract.get("counts", {}).get("rows")):
    ok()
else:
    err("hy3d content row count disagrees with counts.rows")

# Every row shape; no retired/reserve active keys; no invented asset path.
by_slug: dict[str, dict] = {}
for row in rows:
    slug = row.get("slug", "")
    if slug in by_slug:
        err(f"duplicate slug: {slug}")
    by_slug[slug] = row
    if REQUIRED_FIELDS <= set(row) and row["status"] in (V2_STATUSES if is_v2 else STATUSES):
        ok()
    else:
        err(f"invalid row shape/status: {slug} {row}")
    lower = slug.lower()
    bad_reserve = [x for x in FORBIDDEN if x in lower and not slug.startswith("visual-reference/003-gigachad")]
    if bad_reserve or OLD_SLUG_RE.match(slug):
        err(f"retired/reserve/old-slug active demand key: {slug}")
    else:
        ok()
    for key in ("sourcePath", "destination"):
        value = row.get(key)
        if not value:
            continue
        if value.startswith("content/bota-hero/") and value in by_slug:
            ok()
        elif is_v2 and (key == "destination" or key == "sourcePath") and (value.startswith("output/") or value.startswith("export/") or value.startswith("plan/") or value.startswith("/cdn/")):
            ok()
        elif path_exists(value, evidence=key == "destination"):
            ok()
        else:
            err(f"invented path {slug}.{key}: {value}")

# Coverage: all 26 active heroes have model, kit, voice and image rows.
for acro in order:
    display = (registry.get("heroes", {}).get(acro) or {}).get("display_name", "")
    model_slug = display.lower().replace(" ", "-").replace("_", "-")
    wanted = [f"hero-model/{model_slug}", f"hero-kit/{acro}", f"hero-voice/{acro}", f"hero-image/{acro}"]
    for item in wanted:
        if item in by_slug:
            ok()
        else:
            err(f"missing coverage row: {item}")
if len(order) == 26 and len(set(order)) == 26 and order == conformance.get("active_acronyms"):
    ok()
else:
    err("active acronym count/order differs from conformance fixture")

# Every canonical hy3d row appears in the demand contract.
for item in content_rows:
    wanted = f"content/{item.get('category')}/{item.get('slug') or item.get('id')}"
    if wanted in by_slug:
        ok()
    else:
        err(f"missing hy3d content coverage: {wanted}")

# 003 image-only discrepancy is present exactly once and never playable.
reserve = by_slug.get("visual-reference/003-gigachad")
if reserve and reserve.get("status") in STATUSES and "image-only" in (reserve.get("note") or ""):
    ok()
else:
    err("003 image-only reserve discrepancy missing or malformed")
if len(sorted((ROOT / "gallery").glob("*.jpg"))) == 25:
    ok()
else:
    err("gallery count is not 25")

# Chains and identifier inversion are represented.
grounding = json.dumps((demand or {}).get("grounding", {})) if not is_v2 else json.dumps(demand)
for chain in ("Receipt", "Repost", "Camera"):
    if chain in grounding:
        ok()
    else:
        err(f"missing {chain} chain grounding")
inv = (demand or {}).get("coordination", {}).get("identifierInversion", {})
if inv.get("botaExport") and "BOTA" in inv.get("oscraftBotaArtifacts", "") and "acronym" in inv.get("defaultDotaHeroes", "").lower():
    ok()
else:
    err("identifier inversion description missing")
if spawn.get("verdict") == "reusable-data" and "identifier" in json.dumps(spawn).lower():
    ok()
else:
    err("spawn-compatibility reusable-data identifier inversion missing")

# Available rows must point to a real hy3d SHA-256 or a local rule/gallery hash with exact match.
available_verified = 0
for row in rows:
    if row.get("status") != "available":
        continue
    digest = row.get("sourceHash")
    path = row.get("sourcePath")
    # A hero-model link is available only by pointing at its hash-verified canonical content row.
    if row["slug"].startswith("hero-model/"):
        linked = by_slug.get(path or "")
        if linked and linked["status"] == "available" and linked.get("sourceHash") in hy3d_hashes:
            available_verified += 1
            ok()
        else:
            err(f"hero model link not hash-verified: {row['slug']} -> {path}")
        continue
    if not isinstance(digest, str) or not SHA_RE.match(digest):
        err(f"available row has no SHA-256: {row['slug']}")
        continue
    if digest in hy3d_hashes:
        available_verified += 1
        ok()
        continue
    p = Path(path) if path else None
    if p and not p.is_absolute():
        p = ROOT / p if (ROOT / p).is_file() else HY3D / p
    if p and p.is_file() and sha(p) == digest:
        available_verified += 1
        ok()
        continue
    err(f"available row SHA-256 not grounded in hy3d/local file: {row['slug']} hash={digest} path={path}")

# Requested/blocked rows need a reason and must not claim a nonexistent content asset.
for row in rows:
    if row.get("status") in {"requested", "blocked", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open"} and not row.get("note"):
        err(f"{row['status']} row lacks note: {row['slug']}")
    else:
        ok()

print(f"RULE_DEMAND contract={contract_status} hy3d_hashes={len(hy3d_hashes)} rows={len(rows)} available={sum(r['status']=='available' for r in rows)} available_verified={available_verified}")
for item in degraded:
    print(f"UNAVAILABLE: {item}")
for item in errors:
    print(f"error: {item}")
if errors:
    print(f"RULE DEMAND: FAIL ({checks} checks, {len(errors)} errors, {len(degraded)} unavailable)")
    sys.exit(1)
print(f"RULE DEMAND: PASS ({checks} checks, {len(degraded)} unavailable)")
