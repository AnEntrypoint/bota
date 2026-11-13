#!/usr/bin/env python3
"""Generate export/rule-demand.{json,tsv} from BOTA rules and read-only hy3d evidence.

The generator never writes to /workspace/hy3d. hy3d's canonical
output/content-for-bota.json is authoritative when present; otherwise the
published fallback manifests are used and the contract is UNAVAILABLE.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
HY3D = Path("/workspace/hy3d")
HY3D_OUTPUT = HY3D / "output"
CONTRACT = HY3D_OUTPUT / "content-for-bota.json"
FALLBACKS = [
    "final-asset-inventory.json",
    "bota-ready.json",
    "studio-blocked-relay-ready.json",
    "structures-ready.json",
    "spawn-cdn-candidates.json",
]
SHA_RE = re.compile(r"^[a-f0-9]{64}$")


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def hy3d_path(value: str | None) -> Path | None:
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else HY3D / p


def display_path(value: str | None) -> str | None:
    """Keep absolute evidence paths, but present hy3d-local paths as output/..."""
    if not value:
        return None
    p = Path(value)
    if p.is_absolute():
        try:
            return "output/" + str(p.relative_to(HY3D_OUTPUT))
        except ValueError:
            return value
    if value.startswith("output/"):
        return value
    return f"output/{value}"


def row_evidence(row: dict, name: str) -> dict:
    return {
        "manifest": f"output/{name}",
        "path": display_path(row.get("optimizedPath") or row.get("source") or row.get("model") or row.get("destinationPath")),
        "sha256": row.get("sha256") or row.get("sourceSha256") or row.get("destSha256"),
        "destination": row.get("destinationPath") or row.get("destination") if isinstance(row.get("destination"), str) else None,
        "method": row.get("generationMethod") or row.get("method") or row.get("action") or row.get("status") or "manifest-row",
        "status": row.get("status") or "unspecified",
    }


def verified_hash(row: dict, published_hashes: set[str]) -> bool:
    digest = row.get("sha256") or row.get("sourceSha256") or row.get("destSha256")
    if not isinstance(digest, str) or not SHA_RE.match(digest) or digest not in published_hashes:
        return False
    for value in (row.get("optimizedPath"), row.get("source"), row.get("model"), row.get("destinationPath")):
        p = hy3d_path(value)
        if p and p.is_file() and sha256_file(p) == digest:
            return True
    return bool(row.get("destinationSha256") == digest and row.get("status") == "ready")


def main() -> int:
    registry = read_json(EXPORT / "hero-registry.json") or {}
    kits = (read_json(EXPORT / "hero-kits.json") or {}).get("heroes", {})
    voice = (read_json(EXPORT / "hero-voice.json") or {}).get("heroes", {})
    images = (read_json(EXPORT / "image-references.json") or {}).get("heroes", {})
    order = registry.get("acronym_order", [])
    heroes = registry.get("heroes", {})

    contract = read_json(CONTRACT)
    contract_status = "ready" if isinstance(contract, dict) and contract.get("schema") in {"hy3d.content-for-bota/v1", "hy3d.content-for-bota/v2"} else "UNAVAILABLE"
    fallback_docs = {name: read_json(HY3D_OUTPUT / name) for name in FALLBACKS}
    inventory = fallback_docs["final-asset-inventory.json"] or {}
    ready = fallback_docs["bota-ready.json"] or {}
    relay = fallback_docs["studio-blocked-relay-ready.json"] or {}
    structures = fallback_docs["structures-ready.json"] or {}
    cdn = fallback_docs["spawn-cdn-candidates.json"] or {}

    contract_rows = contract.get("rows", []) if contract_status == "ready" else []
    if not contract_rows:
        contract_rows = inventory.get("items", [])
    by_category: dict[str, list[dict]] = {}
    for item in contract_rows:
        by_category.setdefault(item.get("category", "unclassified"), []).append(item)
    published_hashes: set[str] = set()
    for doc in [contract] + list(fallback_docs.values()):
        if not isinstance(doc, dict):
            continue
        def walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k in {"sha256", "sourceSha256", "destSha256", "destinationSha256", "destinationHash", "fullSourceSha256"} and isinstance(v, str) and SHA_RE.match(v):
                        published_hashes.add(v)
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(doc)
    for row in cdn.get("names", []):
        candidate = row.get("candidate") or {}
        if isinstance(candidate.get("sha256"), str):
            published_hashes.add(candidate["sha256"])

    rows: list[dict] = []

    def add(*, slug: str, kind: str, rule_section: str, required_by: str, status: str,
            source_hash: str | None = None, source_path: str | None = None,
            destination: str | None = None, method: str | None = None,
            evidence: str | None = None, note: str | None = None) -> None:
        rows.append({
            "slug": slug,
            "kind": kind,
            "ruleSection": rule_section,
            "requiredBy": required_by,
            "status": status,
            "sourceHash": source_hash,
            "sourcePath": source_path,
            "destination": destination,
            "method": method,
            "hy3dEvidence": evidence,
            "note": note or "",
        })

    # hy3d canonical content rows: every one is published with hash, destination, method and status.
    for category, items in sorted(by_category.items()):
        for item in items:
            slug = item.get("slug") or item.get("id") or "unnamed"
            evidence = row_evidence(item, "content-for-bota.json" if contract_status == "ready" else "final-asset-inventory.json")
            add(slug=f"content/{category}/{slug}", kind=category,
                rule_section="hy3d output/content-for-bota.json; plan/18-asset-manifest-and-audio.md",
                required_by="hy3d owns all content; BOTA rules consume ready/hash-verified rows only",
                status="available" if verified_hash(item, published_hashes) else "requested",
                source_hash=evidence["sha256"], source_path=evidence["path"],
                destination=evidence["destination"], method=evidence["method"],
                evidence=evidence["manifest"],
                note=f"contract={contract_status}; hy3dStatus={evidence['status']}; no BOTA write to hy3d")

    # BOTA-authored rule artifacts: hero kits and voice text plus grounded gallery portraits.
    hero_content = {x.get("slug", "").replace("_", "-"): x for x in by_category.get("bota-hero", [])}
    for acro in order:
        hero = heroes.get(acro, {})
        display = hero.get("display_name", acro)
        slug = display.lower().replace(" ", "-").replace("_", "-")
        slot = hero.get("slot")
        model = hero_content.get(slug) or (read_json(EXPORT / "hero-registry.json") or {}).get("heroes", {}).get(acro, {})
        model_link = f"content/bota-hero/{slug.replace('-', '_')}"
        add(slug=f"hero-model/{slug}", kind="hero-model", rule_section="plan/07-heroes-and-attributes.md; plan/15-roster-and-archetypes.md",
            required_by=f"active hero {acro} slot {slot}", status="available" if model_link in {x['slug'] for x in rows} else "requested",
            source_hash=None, source_path=model_link, method="hy3d-content-link", evidence="output/content-for-bota.json" if contract_status == "ready" else None,
            note=f"model evidence is the hash-verified hy3d row {model_link}; no invented path")
        add(slug=f"hero-kit/{acro}", kind="hero-kit", rule_section="plan/09-launch-hero-kits.md; plan/10-remaining-hero-kits.md",
            required_by=f"active hero {acro} slot {slot}", status="available",
            source_hash=sha256_file(EXPORT / "hero-kits.json"), source_path="export/hero-kits.json",
            method="bota-rules-export", evidence="export/hero-kits.json",
            note=f"{len((kits.get(acro) or {}).get('abilities', []))} ability rows; rule authority is BOTA")
        add(slug=f"hero-voice/{acro}", kind="hero-voice", rule_section="plan/23-voice-and-banter.md; plan/16-humor-and-tone.md",
            required_by=f"active hero {acro} slot {slot}", status="requested",
            source_hash=sha256_file(EXPORT / "hero-voice.json"), source_path="export/hero-voice.json",
            method="pooled-emails-then-relay", evidence="output/content-for-bota.json" if contract_status == "ready" else None,
            note="rule text is available; audio asset is requested until hy3d publishes its clip hash")
        gallery_path = (images.get(acro) or {}).get("gallery_path") or hero.get("portrait_path")
        gallery_file = ROOT / gallery_path if gallery_path else None
        add(slug=f"hero-image/{acro}", kind="hero-image", rule_section="GALLERY.md; plan/22-art-direction.md",
            required_by=f"active hero {acro} slot {slot}", status="available" if gallery_file and gallery_file.is_file() else "requested",
            source_hash=sha256_file(gallery_file) if gallery_file else None, source_path=gallery_path,
            method="local-gallery", evidence=gallery_path,
            note="one of 25 grounded gallery JPGs")

    # The 27th image remains an image-only reserve, never an active hero asset.
    gigachad = ROOT / "gallery" / "003-gigachad.jpg"
    add(slug="visual-reference/003-gigachad", kind="reserve-image", rule_section="plan/16-humor-and-tone.md; plan/22-art-direction.md",
        required_by="cha ultimate visual punchline; image-only retired/reserve discrepancy",
        status="available" if gigachad.is_file() else "blocked", source_hash=sha256_file(gigachad),
        source_path="gallery/003-gigachad.jpg", method="local-gallery", evidence="export/hero-registry.json#authority.discrepancy",
        note="image-only reserve; no hero, kit, voice, spawn, draft or talent key")

    # Rule-implied props/structures and clips: demands, not invented assets.
    rule_demands = [
        ("tier-1-tower", "structure", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("tier-2-tower", "structure", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("tier-3-tower", "structure", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("tier-4-tower", "structure", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("content-mill-melee", "structure", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("content-mill-ranged", "structure", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("stockpile", "structure", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("spawn-lounge", "structure", "plan/04-map.md; plan/07-heroes-and-attributes.md#respawn"),
        ("safe-spot", "structure", "plan/21-systems-added-back.md#safe-spots"),
        ("trend-pit", "structure", "plan/12-neutrals-boosts-the-trend-and-snapshot.md"),
        ("river-boost-spot", "structure", "plan/12-neutrals-boosts-the-trend-and-snapshot.md"),
        ("jungle-camp", "structure", "plan/12-neutrals-boosts-the-trend-and-snapshot.md"),
        ("lurker-cam", "prop", "plan/11-items.md"),
        ("ring-light", "prop", "plan/11-items.md"),
        ("sticky-note", "prop", "plan/11-items.md"),
        ("drafted-note", "prop", "plan/11-items.md"),
        ("hot-sauce-bottle", "prop", "plan/11-items.md"),
        ("envelope", "prop", "plan/11-items.md"),
        ("old-hoodie", "prop", "plan/11-items.md"),
        ("coffee-can", "prop", "plan/21-systems-added-back.md#coffee"),
        ("delivery-drone", "prop", "plan/16-humor-and-tone.md#announcer-lines"),
        ("padlock", "prop", "plan/03-core-loop-and-win-condition.md#lanes-and-structures"),
        ("stan-sign", "prop", "plan/16-humor-and-tone.md#gags"),
        ("ticker-banner", "prop", "plan/16-humor-and-tone.md#gags"),
        ("receipt-chain", "clip", "plan/16-humor-and-tone.md#rules"),
        ("repost-chain", "clip", "plan/16-humor-and-tone.md#rules"),
        ("camera-chain", "clip", "plan/16-humor-and-tone.md#rules"),
        ("eternal-loop", "clip", "plan/18-asset-manifest-and-audio.md; plan/21-systems-added-back.md"),
        ("transition-wipe", "clip", "plan/16-humor-and-tone.md#rules"),
        ("stan-cheer", "clip", "plan/18-asset-manifest-and-audio.md"),
    ]
    for slug, kind, section in rule_demands:
        add(slug=f"rule-demand/{slug}", kind=kind, rule_section=section,
            required_by="current rules; content owner hy3d publishes hash/path/destination/method",
            status="requested", source_hash=None, source_path=None,
            method="pooled-emails-then-relay", evidence="output/content-for-bota.json" if contract_status == "ready" else None,
            note="rule-implied demand only; no asset path or hash is invented")

    # Spawn CDN names remain comparison evidence; only policy-satisfied names are available.
    for item in cdn.get("names", []):
        name = item.get("name", "")
        candidate = item.get("candidate") or {}
        digest = candidate.get("sha256")
        ready_cdn = item.get("policySatisfied") is True and digest in published_hashes
        add(slug=f"spawn-cdn/{name.lstrip('/')}", kind="spawn-cdn-name",
            rule_section="export/spawn-compatibility.json; wscheppity CDN policy",
            required_by="identifier inversion / reusable-data comparison only",
            status="available" if ready_cdn else "blocked",
            source_hash=digest if ready_cdn else None,
            source_path=display_path(candidate.get("path")) if ready_cdn else None,
            destination=name, method="cdn-name", evidence="output/spawn-cdn-candidates.json",
            note=item.get("reason") or "CDN policy evidence")

    doc = {
        "schema": "bota.rule-demand/v1",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "owner": "bota rules",
        "contentOwner": "hy3d",
        "coordination": {
            "contractPath": "/workspace/hy3d/output/content-for-bota.json",
            "contractStatus": contract_status,
            "fallbackManifests": [f"/workspace/hy3d/output/{x}" for x in FALLBACKS],
            "sequence": "hy3d makes all content first with pooled emails, then with the relay",
            "writePolicy": "read-only toward /workspace/hy3d",
            "identifierInversion": {
                "botaExport": "historical three-letter acronyms stay canonical for this export",
                "oscraftBotaArtifacts": "expected full BOTA character names/slugs",
                "defaultDotaHeroes": "expected acronyms",
                "status": "downstream migration in progress; live validator supports both modes",
            },
        },
        "rulesAuthority": ["plan/", "ROSTER.md", "GALLERY.md", "export/hero-registry.json"],
        "grounding": {
            "galleryImages": 25,
            "activeHeroes": len(order),
            "reserve": {"slot": "003", "displayName": "Gigachad", "status": "image-only retired/reserve", "playable": False},
            "chains": ["Receipt", "Repost", "Camera"],
        },
        "counts": {
            "rows": len(rows),
            "available": sum(x["status"] == "available" for x in rows),
            "requested": sum(x["status"] == "requested" for x in rows),
            "blocked": sum(x["status"] == "blocked" for x in rows),
            "activeHeroKeys": len(order),
            "hy3dHashes": len(published_hashes),
            "hy3dReadyRows": len(contract_rows),
        },
        "rows": rows,
    }
    (EXPORT / "rule-demand.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    fields = ["slug", "kind", "ruleSection", "requiredBy", "status", "sourceHash", "sourcePath", "destination", "method", "hy3dEvidence", "note"]
    with (EXPORT / "rule-demand.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (row.get(k) or "") for k in fields})
    print(f"RULE_DEMAND generated rows={len(rows)} available={doc['counts']['available']} requested={doc['counts']['requested']} blocked={doc['counts']['blocked']} contract={contract_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
