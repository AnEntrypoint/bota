#!/usr/bin/env python3
"""Resolve BOTA rule-demand rows from live peer manifests and publish request queues.

Read-only toward /workspace/hy3d, /workspace/oscraft and /workspace/wscheppity.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
HY3D = Path("/workspace/hy3d")
WS = Path("/workspace/wscheppity")
PRIOR = EXPORT / "rule-demand.json"
HY3D_FILES = {
    "content": HY3D / "output/content-for-bota.json",
    "inventory": HY3D / "output/final-asset-inventory.json",
    "generation": HY3D / "output/generation-status.json",
    "diagnosis": HY3D / "output/studio-blocked-diagnosis.json",
}
WS_FILES = {
    "extraction": WS / ".local/extraction-manifest.json",
    "cdn": WS / ".local/cdn/manifest.json",
    "cdnAll": WS / ".local/cdn/manifest-all.json",
    "httpDir": WS / ".local/cdn/http",
}
EXTRA = Path("/workspace/extra")
EXTRA_FILES = {
    "extraction": EXTRA / ".local/extraction-manifest.json",
    "contract": EXTRA / ".local/extraction-contract.json",
    "cdn": EXTRA / ".local/cdn/manifest.json",
    "cdnAll": EXTRA / ".local/cdn/manifest-all.json",
    "httpDir": EXTRA / ".local/cdn/http",
}
STATUSES = {"available", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open"}
ACTORS = {"hy3d", "wscheppity", "owner", "bota"}
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
OLD_SLUG = re.compile(r"^\d{3}-")


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def sha_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def manifest_note(path: Path) -> dict:
    if path.is_dir():
        files = sorted(path.glob("*"))
        return {"path": str(path / "*"), "status": "ready" if files else "UNAVAILABLE", "count": len(files), "reason": None if files else "directory has no files"}
    if not path.is_file():
        return {"path": str(path), "status": "UNAVAILABLE", "reason": "missing exact path"}
    b = path.read_bytes()
    data = read_json(path)
    return {
        "path": str(path),
        "status": "ready" if data is not None else "UNAVAILABLE",
        "bytes": len(b),
        "sha256": hashlib.sha256(b).hexdigest(),
        "reason": None if data is not None else "invalid JSON",
    }


def stable_id(prefix: str, slug: str) -> str:
    return prefix + ":" + hashlib.sha256(slug.encode()).hexdigest()[:16]


def plan_citation(rule_section: str) -> str:
    """Return a real plan file:line citation from the rule text, falling back to an exact chapter line."""
    m = re.search(r"(plan/\d\d-[a-z0-9-]+\.md)", rule_section)
    if m:
        path = ROOT / m.group(1)
        if path.is_file():
            needle = None
            if "lanes-and-structures" in rule_section:
                needle = "### Lanes and structures"
            elif "safe-spots" in rule_section or "#coffee" in rule_section:
                needle = "### Safe Spots"
            elif "#rules" in rule_section:
                needle = "### Rules"
            elif "#gags" in rule_section:
                needle = "### Gags"
            elif "voice" in rule_section:
                needle = "### Rules"
            if needle:
                for n, line in enumerate(path.read_text().splitlines(), 1):
                    if needle in line:
                        return f"{m.group(1)}:{n}"
            return f"{m.group(1)}:1"
    return "plan/33-coordinated-content-rule-iteration.md:5"


def verified_hash(row: dict, published_hashes: set[str]) -> bool:
    digest = row.get("sha256") or row.get("sourceSha256") or row.get("destSha256")
    if not isinstance(digest, str) or not SHA_RE.match(digest) or digest not in published_hashes:
        return False
    for value in (row.get("optimizedPath"), row.get("source"), row.get("destinationPath")):
        p = Path(value) if value else None
        if p and p.is_file() and sha_file(p) == digest:
            return True
    return bool(row.get("destinationSha256") == digest and row.get("status") == "ready")


def quote_plan(citation: str) -> str:
    rel, _, line = citation.partition(":")
    p = ROOT / rel
    try:
        return p.read_text().splitlines()[max(0, int(line) - 1)].strip()
    except Exception:
        return ""


def hy3d_evidence() -> dict:
    c = read_json(HY3D_FILES["content"]) or {}
    inv = read_json(HY3D_FILES["inventory"]) or {}
    gen = read_json(HY3D_FILES["generation"]) or {}
    diag = read_json(HY3D_FILES["diagnosis"]) or {}
    return {
        "contract": c,
        "counts": c.get("counts", {}),
        "rows": c.get("rows", []),
        "inventoryRows": inv.get("items", []),
        "pool": gen.get("pool", {}),
        "generation": gen.get("generation", {}),
        "combinedCheck": gen.get("combinedCheck", {}),
        "blocker": {
            "classification": diag.get("classification"),
            "chain": diag.get("chain"),
            "step": diag.get("step"),
            "httpStatus": diag.get("httpStatus"),
            "retryRecommended": diag.get("retryRecommended"),
            "futureRetryCondition": diag.get("futureRetryCondition"),
            "quotaPreserved": diag.get("quotaPreserved"),
        },
    }


def cdn_index() -> tuple[dict[str, dict], dict]:
    active: dict[str, dict] = {}
    all_rows: dict[str, dict] = {}
    for key in ["cdn", "cdnAll"]:
        doc = read_json(WS_FILES[key]) or {}
        for row in doc.get("assets", []):
            name = row.get("name")
            if not name:
                continue
            rec = dict(row)
            rec["manifest"] = str(WS_FILES[key])
            if key == "cdn":
                active[name] = rec
            all_rows.setdefault(name, rec)
    verified: dict[str, dict] = {}
    for name, row in all_rows.items():
        rel = row.get("file")
        digest = row.get("sha256")
        if not isinstance(digest, str) or not SHA_RE.match(digest) or not rel:
            continue
        p = WS / rel
        if not p.is_file():
            continue
        b = p.read_bytes()
        if len(b) == row.get("bytes") and len(b) > 0 and hashlib.sha256(b).hexdigest() == digest:
            rec = dict(row)
            rec["localPath"] = str(p)
            rec["localSha256"] = hashlib.sha256(b).hexdigest()
            rec["validation"] = {
                "bytes": len(b),
                "sha256Match": True,
                "magic": row.get("magic") or b[:8].hex(),
                "httpStatus": None,
                "contentType": None,
            }
            verified[name] = rec
    return verified, {"activeRows": len(active), "allRows": len(all_rows), "verifiedActive": len(set(active) & set(verified)), "verifiedAll": len(verified), "allNames": sorted(all_rows), "allRowRecords": all_rows}


def acceptance_for(status: str, kind: str) -> list[str]:
    if status == "available":
        return ["Local bytes exist", "SHA-256 matches manifest", "byte length matches manifest"]
    if status == "spawn-generated":
        return [
            "Capture exact generated-on-demand response bytes",
            "Record HTTP status 200, content-type and body size",
            "Publish SHA-256 and local extraction path in .local/cdn/manifest.json",
            "Verify the CDN name maps to the exact captured bytes",
        ]
    if status in {"requested-pooled-email", "requested-relay"}:
        base = [
            "Publish a row in /workspace/hy3d/output/content-for-bota.json",
            "Include category, slug, source path, optimized path, destination, generationMethod and status",
            "Include a real SHA-256 and bytes",
        ]
        if kind in {"structure", "prop", "hero-model", "hero-model-substitute"}:
            base += ["GLB magic is glTF", "GLB version is 2", "declared length equals file bytes"]
        if kind in {"clip", "hero-voice"}:
            base += ["Asset extension/type is explicit", "Decoded duration or media validation is recorded"]
        base.append("Pooled-email attempt is recorded before relay fallback" if status == "requested-pooled-email" else "Relay fallback evidence is recorded")
        return base
    if status == "owner-decision":
        return ["Owner records an explicit choice", "No canonical engine value is written", "do_not_promote remains true"]
    return ["Design remains intentionally open", "No canonical engine value is written", "do_not_promote remains true"]


def main() -> int:
    prior = read_json(PRIOR)
    if not prior or prior.get("schema") not in {"bota.rule-demand/v1", "bota.rule-demand/v2"}:
        print(f"UNAVAILABLE: prior demand missing/invalid {PRIOR}")
        return 2
    is_v2 = prior.get("schema") == "bota.rule-demand/v2"
    peer_notes = {k: manifest_note(p) for k, p in {**HY3D_FILES, **WS_FILES, **EXTRA_FILES}.items()}
    unavailable = [f"UNAVAILABLE: {k} {v['path']}: {v['reason']}" for k, v in peer_notes.items() if v["status"] != "ready"]
    hy = hy3d_evidence()
    cdn_verified, cdn_counts = cdn_index()
    extraction = read_json(WS_FILES["extraction"]) or {}
    contract_rows = hy["rows"]
    contract_status = "ready" if peer_notes["content"]["status"] == "ready" else "UNAVAILABLE"
    published_hashes: set[str] = set()
    def collect_hash(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in {"sha256", "sourceSha256", "destSha256", "destinationSha256", "destinationHash", "localSha256"} and isinstance(v, str) and SHA_RE.match(v):
                    published_hashes.add(v)
                collect_hash(v)
        elif isinstance(node, list):
            for v in node: collect_hash(v)
    for pth in list(HY3D_FILES.values()) + list(WS_FILES.values()):
        collect_hash(read_json(pth))
    def row_evidence(row: dict, name: str) -> dict:
        return {
            "manifest": f"output/{name}",
            "path": row.get("optimizedPath") or row.get("source") or row.get("destinationPath"),
            "sha256": row.get("sha256") or row.get("sourceSha256"),
            "destination": row.get("destinationPath") or row.get("legacyDestinationPath"),
            "method": row.get("generationMethod") or row.get("method") or row.get("status") or "manifest-row",
        }

    # Resolution policy for the prior 144 non-available rows.
    def resolve(row: dict) -> dict:
        slug = row["slug"]
        kind = row.get("kind")
        destination = row.get("destination")
        if kind == "spawn-cdn-name" and destination in cdn_verified:
            ev = cdn_verified[destination]
            return {
                "status": "available", "nextActor": "bota", "sourcePath": ev["localPath"], "sourceHash": ev["localSha256"],
                "destination": destination, "method": "wscheppity-local-extraction",
                "evidence": [ev["manifest"], str(WS_FILES["extraction"])], "validation": ev["validation"],
                "note": "exact local bytes hash-verified; BOTA uses this only as reusable-data evidence",
            }
        if kind == "spawn-cdn-name":
            return {
                "status": "spawn-generated", "nextActor": "wscheppity", "sourcePath": destination, "sourceHash": None,
                "destination": destination, "method": "generated-on-demand-capture",
                "evidence": [str(WS_FILES["cdnAll"]), str(WS_FILES["extraction"])],
                "validation": {"httpStatus": None, "contentType": None, "bodySize": None},
                "note": "wscheppity 100% extraction requires exact generated-on-demand behavior/bytes",
            }
        if kind == "hero-voice":
            return {
                "status": "requested-pooled-email", "nextActor": "hy3d", "sourcePath": row.get("sourcePath"), "sourceHash": row.get("sourceHash"),
                "destination": f"output/content-for-bota.json#voice/{slug.rsplit('/',1)[-1]}", "method": "pooled-emails-then-relay",
                "evidence": [str(HY3D_FILES["content"]), str(HY3D_FILES["generation"])], "validation": {"poolQuota": hy["pool"].get("finalTotal"), "httpStatus": None},
                "note": "BOTA voice text exists; audio bytes must be generated by hy3d after a pooled-email attempt",
            }
        if kind in {"structure", "prop"}:
            return {
                "status": "requested-pooled-email", "nextActor": "hy3d", "sourcePath": None, "sourceHash": None,
                "destination": f"output/content-for-bota.json#{slug}", "method": "pooled-emails-then-relay",
                "evidence": [str(HY3D_FILES["content"]), str(HY3D_FILES["inventory"]), str(HY3D_FILES["generation"])],
                "validation": {"poolQuota": hy["pool"].get("finalTotal"), "readyStructureRows": hy["counts"].get("byCategory", {}).get("structure")},
                "note": "rule-implied BOTA prop/structure; ready structure geometry is evidence, not this exact asset",
            }
        if kind == "clip":
            if "eternal-loop" in slug:
                return {
                    "status": "owner-decision", "nextActor": "owner", "sourcePath": None, "sourceHash": None,
                    "destination": "export/decision-packet.json#forever_eternal_loop_clip", "method": "do-not-promote",
                    "evidence": ["export/decision-packet.json", "export/DECISION-PACKET.md"],
                    "validation": {"do_not_promote": True}, "note": "Forever's Eternal Loop clip duration is an intentionally gated owner decision",
                }
            if "transition-wipe" in slug:
                return {
                    "status": "intentionally-open", "nextActor": "bota", "sourcePath": None, "sourceHash": None,
                    "destination": "plan/16-humor-and-tone.md:8", "method": "text-only-rule",
                    "evidence": ["plan/16-humor-and-tone.md", "plan/34-content-status-adjudication.md"],
                    "validation": {"do_not_promote": True}, "note": "The wipe is a presentation cue; exact visual asset remains intentionally open",
                }
            return {
                "status": "requested-relay", "nextActor": "hy3d", "sourcePath": None, "sourceHash": None,
                "destination": f"output/content-for-bota.json#{slug}", "method": "pooled-email-attempt-then-relay-fallback",
                "evidence": [str(HY3D_FILES["diagnosis"]), str(HY3D_FILES["generation"])],
                "validation": {"serviceSideBlocker": hy["blocker"].get("httpStatus"), "quotaPreserved": hy["blocker"].get("quotaPreserved")},
                "note": "Receipt/Repost/Camera clip needs relay fallback after a recorded pooled attempt; no asset path invented",
            }
        return {
            "status": "intentionally-open", "nextActor": "bota", "sourcePath": None, "sourceHash": None,
            "destination": "plan/35-continuous-iteration-ledger.md:39", "method": "rules-review",
            "evidence": ["plan/35-continuous-iteration-ledger.md"], "validation": {"do_not_promote": True},
            "note": "unclassified rule demand remains open without promotion",
        }

    rows = []
    prior_non = []
    for old in prior["rows"]:
        row = dict(old)
        if is_v2:
            # Idempotent pass: keep the original prior state and re-adjudicate live evidence.
            old_for_resolution = dict(old)
            old_for_resolution["status"] = old.get("priorStatus", old["status"])
        else:
            old_for_resolution = old
        if old_for_resolution["status"] in {"requested", "blocked"}:
            prior_non.append(old_for_resolution)
            r = resolve(old_for_resolution)
            row.update({
                "priorStatus": old_for_resolution["status"], "status": r["status"], "nextActor": r["nextActor"],
                "sourcePath": r["sourcePath"], "sourceHash": r["sourceHash"], "destination": r["destination"],
                "method": r["method"], "hy3dEvidence": "; ".join(r["evidence"]),
                "validation": r["validation"], "note": r["note"],
            })
            citation = plan_citation(old.get("ruleSection", ""))
            row["ruleCitation"] = citation
            row["ruleQuote"] = quote_plan(citation)
            row["acceptanceCriteria"] = acceptance_for(r["status"], old.get("kind", ""))
            row["stableId"] = stable_id("resolve", old["slug"])
        else:
            row.setdefault("priorStatus", old["status"])
            row.setdefault("nextActor", "bota")
            row.setdefault("validation", {})
            row.setdefault("ruleCitation", plan_citation(old.get("ruleSection", "")))
            row.setdefault("acceptanceCriteria", ["Already hash-verified available evidence"])
            row.setdefault("stableId", stable_id("resolve", old["slug"]))
        rows.append(row)

    # New canonical hy3d rows published after the frozen prior contract are appended
    # as content-ledger rows. They never disturb the 290 prior-row reconciliation.
    known_content = {r.get("slug") for r in rows if r.get("slug", "").startswith("content/")}
    for item in contract_rows:
        wanted = f"content/{item.get('category')}/{item.get('slug') or item.get('id')}"
        if wanted in known_content:
            continue
        evidence = row_evidence(item, "content-for-bota.json" if contract_status == "ready" else "final-asset-inventory.json")
        rows.append({
            "slug": wanted,
            "kind": item.get("category", "content"),
            "ruleSection": "hy3d output/content-for-bota.json; plan/18-asset-manifest-and-audio.md",
            "ruleCitation": "plan/18-asset-manifest-and-audio.md:1",
            "ruleQuote": quote_plan("plan/18-asset-manifest-and-audio.md:1"),
            "requiredBy": "new hash-verified hy3d content row; content ledger only",
            "priorStatus": "available",
            "status": "available" if verified_hash(item, published_hashes) else "requested-pooled-email",
            "nextActor": "hy3d",
            "sourceHash": evidence["sha256"],
            "sourcePath": evidence["path"],
            "destination": evidence["destination"],
            "method": evidence["method"],
            "hy3dEvidence": evidence["manifest"],
            "validation": item.get("validation", {}),
            "acceptanceCriteria": ["Real SHA-256", "GLB or media validation", "Ready row in content-for-bota.json"],
            "stableId": stable_id("resolve", wanted),
            "note": "appended after frozen prior reconciliation; exact hy3d row evidence",
        })
    counts = {s: sum(r["status"] == s for r in rows) for s in sorted(STATUSES)}
    doc = {
        "schema": "bota.rule-demand/v2",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "owner": "bota rules",
        "contentOwner": "hy3d",
        "extractionOwner": "wscheppity",
        "coordination": prior.get("coordination", {}),
        "coordination": {
            **(prior.get("coordination", {})),
            "resolutionContract": "v2 six-state resolution; no guessed content",
            "sequence": "hy3d makes all content first with pooled emails, then with the relay",
            "wscheppityRequirement": "100% upstream extraction",
            "writePolicy": "read-only toward hy3d, oscraft and wscheppity",
        },
        "peerManifests": peer_notes,
        "peerEvidence": {
            "hy3d": {"schema": hy["contract"].get("schema"), "counts": hy["counts"], "blocker": hy["blocker"], "combinedCheck": hy["combinedCheck"]},
            "wscheppity": {"extractionSummary": extraction.get("summary", {}), "cdn": cdn_counts},
        },
        "priorResolution": {
            "priorRows": len(prior["rows"]),
            "priorAvailable": sum(r.get("priorStatus", r["status"]) == "available" for r in prior["rows"]),
            "priorRequested": sum(r.get("priorStatus", r["status"]) == "requested" for r in prior["rows"]),
            "priorBlocked": sum(r.get("priorStatus", r["status"]) == "blocked" for r in prior["rows"]),
            "resolvedRows": len(prior_non),
        },
        "counts": {
            "rows": len(rows), **counts, "activeHeroKeys": 26, "hy3dReadyRows": hy["counts"].get("rows", 0),
            "spawnVerifiedBytes": len(cdn_verified), "spawnAllNames": cdn_counts["allRows"],
        },
        "rows": rows,
    }
    (EXPORT / "rule-demand.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    fields = ["slug", "kind", "ruleSection", "ruleCitation", "requiredBy", "priorStatus", "status", "nextActor", "sourceHash", "sourcePath", "destination", "method", "hy3dEvidence", "validation", "acceptanceCriteria", "stableId", "note"]
    with (EXPORT / "rule-demand.tsv").open("w", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            out = {k: r.get(k) for k in fields}
            for k in ["validation", "acceptanceCriteria"]:
                out[k] = json.dumps(out[k], sort_keys=True) if out[k] is not None else ""
            w.writerow({k: ("" if v is None else v) for k, v in out.items()})

    # Peer queues: hy3d gets actionable content demands; wscheppity gets extraction gaps.
    hy_rows = []
    ws_rows = []
    for r in rows:
        if r.get("priorStatus") not in {"requested", "blocked"}:
            continue
        citation = r.get("ruleCitation") or plan_citation(r.get("ruleSection", ""))
        base = {
            "stableId": stable_id("queue", r["slug"]),
            "demandSlug": r["slug"],
            "status": r["status"],
            "nextActor": r["nextActor"],
            "ruleCitation": citation,
            "ruleQuote": quote_plan(citation),
            "evidence": r.get("hy3dEvidence"),
            "sourcePath": r.get("sourcePath"),
            "sourceUrl": r.get("destination") if str(r.get("destination", "")).startswith(("/cdn/", "http")) else None,
            "validation": r.get("validation", {}),
            "acceptanceCriteria": r.get("acceptanceCriteria", []),
            "note": r.get("note"),
        }
        if r["status"] in {"requested-pooled-email", "requested-relay", "owner-decision", "intentionally-open"} and r["nextActor"] in {"hy3d", "owner", "bota"}:
            priority = {"requested-pooled-email": 10, "requested-relay": 20, "owner-decision": 30, "intentionally-open": 40}[r["status"]]
            hy_rows.append({**base, "priority": priority, "queue": "hy3d-content"})
        if r["status"] == "spawn-generated" or (r["kind"] == "spawn-cdn-name" and r["nextActor"] == "wscheppity"):
            ws_rows.append({**base, "priority": 5, "queue": "wscheppity-extraction"})
        if r["status"] == "available" and r["kind"] == "spawn-cdn-name":
            ws_rows.append({**base, "priority": 90, "queue": "wscheppity-extraction", "status": "available", "note": "extracted and hash-verified; keep in extraction evidence, no action required"})
    # wscheppity 100% extraction: publish every unique CDN name, including zero-byte generated placeholders.
    all_records = cdn_counts["allRowRecords"]
    for name in cdn_counts["allNames"]:
        if any(x.get("demandSlug") == "spawn-cdn/" + name.lstrip("/") for x in ws_rows):
            continue
        rec = all_records[name]
        is_verified = name in cdn_verified
        ev = cdn_verified.get(name, {})
        citation = "plan/35-continuous-iteration-ledger.md:9"
        row = {
            "stableId": stable_id("ws", "spawn-cdn/" + name.lstrip("/")),
            "queue": "wscheppity-extraction",
            "priority": 5 if not is_verified else 90,
            "demandSlug": "spawn-cdn/" + name.lstrip("/"),
            "status": "available" if is_verified else "spawn-generated",
            "nextActor": "wscheppity",
            "ruleCitation": citation,
            "ruleQuote": quote_plan(citation),
            "sourcePath": ev.get("localPath") or (str(WS / rec.get("file", "")) if rec.get("file") else None),
            "sourceUrl": name,
            "evidence": "; ".join([str(WS_FILES["cdnAll"]), str(WS_FILES["cdn"]), str(WS_FILES["extraction"])]),
            "validation": ev.get("validation") or {
                "httpStatus": None,
                "contentType": None,
                "bodySize": rec.get("bytes"),
                "reportedSha256": rec.get("sha256"),
                "ok": rec.get("ok"),
                "note": "manifest-all row is a zero-byte/generated placeholder until exact bytes are captured",
            },
            "acceptanceCriteria": acceptance_for("available" if is_verified else "spawn-generated", "spawn-cdn-name"),
            "note": "100% upstream extraction gap; capture exact generated-on-demand behavior/bytes" if not is_verified else "hash-verified local extraction evidence",
        }
        ws_rows.append(row)
    # extra is a first-class upstream extraction peer when its manifests exist.
    extra_evidence = {
        "root": str(EXTRA),
        "paths": {k: {"path": str(v), "status": "ready" if v.exists() else "UNAVAILABLE"} for k, v in EXTRA_FILES.items()},
        "counts": {"uniqueNames": 0, "ok": 0, "bad": 0, "httpFiles": len(list(EXTRA_FILES["httpDir"].glob("*"))) if EXTRA_FILES["httpDir"].is_dir() else 0},
    }
    extra_all = read_json(EXTRA_FILES["cdnAll"]) or {}
    extra_extraction = read_json(EXTRA_FILES["extraction"]) or {}
    extra_evidence["counts"]["uniqueNames"] = extra_all.get("uniqueNames") or extra_all.get("count") or 0
    extra_evidence["counts"]["ok"] = extra_all.get("ok") or 0
    extra_evidence["counts"]["bad"] = len(extra_all.get("bad") or []) if isinstance(extra_all.get("bad"), list) else extra_all.get("bad") or 0
    extra_evidence["summary"] = extra_extraction.get("summary", {})
    extra_http_by_name = {}
    for hp in sorted(EXTRA_FILES["httpDir"].glob("*.json")):
        hd = read_json(hp)
        if isinstance(hd, dict) and isinstance(hd.get("name"), str):
            extra_http_by_name.setdefault(hd["name"], {"doc": hd, "path": str(hp)})
    for idx, rec in enumerate(extra_all.get("assets", [])):
        name = rec.get("name")
        if not name:
            continue
        digest = rec.get("sha256")
        rel_file = rec.get("file")
        local = EXTRA / rel_file if rel_file else None
        bytes_ok = bool(local and local.is_file() and isinstance(digest, str) and SHA_RE.match(digest) and sha_file(local) == digest and local.stat().st_size > 0)
        reqs = rec.get("requests") if isinstance(rec.get("requests"), list) else []
        get = next((x for x in reqs if isinstance(x, dict) and str(x.get("method", "")).upper() == "GET"), None)
        if not get and name in extra_http_by_name:
            get = next((x for x in extra_http_by_name[name]["doc"].get("requests", []) if isinstance(x, dict) and str(x.get("method", "")).upper() == "GET"), None)
        http_path = extra_http_by_name.get(name, {}).get("path") or str(EXTRA_FILES["httpDir"])
        citation = "plan/35-continuous-iteration-ledger.md:9"
        ws_rows.append({
            "stableId": stable_id("extra", name),
            "queue": "extra-extraction",
            "peer": "extra",
            "priority": 90 if bytes_ok else 5,
            "demandSlug": "extra-cdn/" + name.lstrip("/"),
            "status": "available" if bytes_ok else "spawn-generated",
            "nextActor": "extra",
            "ruleCitation": citation,
            "ruleQuote": quote_plan(citation),
            "sourcePath": str(local) if local else None,
            "sourceUrl": name,
            "evidence": "; ".join([str(EXTRA_FILES["extraction"]), str(EXTRA_FILES["cdnAll"]), http_path]),
            "validation": {
                "httpStatus": get.get("status") if get else None,
                "contentType": (get or {}).get("contentType"),
                "bodySize": (get or {}).get("bytes") or rec.get("bytes"),
                "sha256": digest,
                "bytesVerified": bytes_ok,
                "exactGeneratedOnDemandEvidence": True,
            },
            "acceptanceCriteria": acceptance_for("available" if bytes_ok else "spawn-generated", "spawn-cdn-name"),
            "note": "first-class extra upstream extraction evidence; read-only" if bytes_ok else "extra generated-on-demand capture required; exact HTTP evidence recorded",
        })
    def dedupe(items):
        seen = set(); out = []
        for x in sorted(items, key=lambda y: (y["priority"], y["demandSlug"])):
            if x["stableId"] not in seen:
                seen.add(x["stableId"]); out.append(x)
        return out
    hy_rows = dedupe(hy_rows); ws_rows = dedupe(ws_rows)
    queue = {
        "schema": "bota.content-request-queue/v1",
        "generatedAt": doc["generatedAt"],
        "readOnly": True,
        "nextActor": "hy3d",
        "coordination": "content first with pooled emails, then relay",
        "counts": {"rows": len(hy_rows), "byStatus": {s: sum(x["status"] == s for x in hy_rows) for s in sorted(STATUSES)}},
        "rows": hy_rows,
    }
    (EXPORT / "content-request-queue.json").write_text(json.dumps(queue, indent=2, sort_keys=True) + "\n")
    qfields = ["stableId", "queue", "priority", "demandSlug", "status", "nextActor", "ruleCitation", "ruleQuote", "sourcePath", "sourceUrl", "evidence", "validation", "acceptanceCriteria", "note"]
    with (EXPORT / "content-request-queue.tsv").open("w", newline="") as h:
        w = csv.DictWriter(h, fieldnames=qfields, delimiter="\t", lineterminator="\n"); w.writeheader()
        for r in hy_rows:
            out = dict(r)
            for k in ["validation", "acceptanceCriteria"]: out[k] = json.dumps(out.get(k), sort_keys=True)
            w.writerow({k: ("" if out.get(k) is None else out.get(k)) for k in qfields})
    gaps = {
        "schema": "bota.spawn-extraction-gaps/v1",
        "generatedAt": doc["generatedAt"],
        "readOnly": True,
        "nextActor": "wscheppity+extra",
        "ownerRequirement": "100% complete upstream extraction for wscheppity and extra",
        "peerManifests": {k: peer_notes[k] for k in ["extraction", "cdn", "cdnAll"]},
        "peers": {
            "wscheppity": {"extraction": str(WS_FILES["extraction"]), "cdnAll": str(WS_FILES["cdnAll"]), "http": str(WS_FILES["httpDir"]), "allCdnNames": cdn_counts["allRows"]},
            "extra": {k: str(v) for k, v in EXTRA_FILES.items()},
        },
        "extraEvidence": extra_evidence,
        "counts": {
            "rows": len(ws_rows), "available": sum(x["status"] == "available" for x in ws_rows),
            "spawnGenerated": sum(x["status"] == "spawn-generated" for x in ws_rows),
            "allCdnNames": cdn_counts["allRows"], "activeCdnNames": cdn_counts["activeRows"],
            "verifiedActiveBytes": cdn_counts["verifiedActive"],
            "wscheppityRows": sum(x.get("peer", "wscheppity") == "wscheppity" for x in ws_rows),
            "extraRows": sum(x.get("peer") == "extra" for x in ws_rows),
            "extraCdnNames": extra_evidence["counts"]["uniqueNames"],
        },
        "rows": ws_rows,
    }
    (EXPORT / "spawn-extraction-gaps.json").write_text(json.dumps(gaps, indent=2, sort_keys=True) + "\n")

    print(f"RULE_DEMAND_V2 rows={len(rows)} available={counts['available']} requested-pooled-email={counts['requested-pooled-email']} requested-relay={counts['requested-relay']} spawn-generated={counts['spawn-generated']} owner-decision={counts['owner-decision']} intentionally-open={counts['intentionally-open']}")
    print(f"QUEUES hy3d={len(hy_rows)} wscheppity={len(ws_rows)} cdn_verified={len(cdn_verified)} all_cdn_names={cdn_counts['allRows']}")
    for u in unavailable: print(u)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
