#!/usr/bin/env python3
"""Bounded, read-only coordination watcher for BOTA content/extraction queues.

Default: 10 minutes, 10 second poll. --once: one pass and exit.
Writes only export/coordination-status.json and export/coordination-status.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"
HY3D = Path("/workspace/hy3d")
WS = Path("/workspace/wscheppity")
EXTRA = Path("/workspace/extra")
OS = Path("/workspace/oscraft/scenarios/bota")
HY3D_FILES = {
    "content": HY3D / "output/content-for-bota.json",
    "demandV2": HY3D / "output/content-demand-v2.json",
    "generation": HY3D / "output/generation-status.json",
    "recovery": HY3D / "output/studio-recovery-watch.json",
    "probes": HY3D / "output/spawn-cdn-probes.json",
}
WS_FILES = {
    "extraction": WS / ".local/extraction-manifest.json",
    "cdnAll": WS / ".local/cdn/manifest-all.json",
    "cdnActive": WS / ".local/cdn/manifest.json",
    "httpDir": WS / ".local/cdn/http",
}
EXTRA_FILES = {
    "extraction": EXTRA / ".local/extraction-manifest.json",
    "contract": EXTRA / ".local/extraction-contract.json",
    "cdnAll": EXTRA / ".local/cdn/manifest-all.json",
    "cdnActive": EXTRA / ".local/cdn/manifest.json",
    "httpDir": EXTRA / ".local/cdn/http",
}
OS_FILES = {
    "identifiers": OS / "IDENTIFIERS.md",
    "crossContract": OS / "cross-contract-snapshot.json",
    "ui": OS / "bota_ui.json",
}
STATUSES = {"available", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open", "UNAVAILABLE"}
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
OLD_SLUG = re.compile(r"^\d{3}-")


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def file_sha(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def manifest_state(path: Path) -> dict:
    b = path.read_bytes() if path.is_file() else None
    return {
        "path": str(path),
        "status": "ready" if b is not None else "UNAVAILABLE",
        "bytes": len(b) if b is not None else None,
        "sha256": hashlib.sha256(b).hexdigest() if b is not None else None,
    }


def glob_state(folder: Path, pattern: str) -> dict:
    paths = sorted(folder.glob(pattern)) if folder.is_dir() else []
    return {"path": str(folder / pattern), "status": "ready" if paths else "UNAVAILABLE", "count": len(paths), "samples": [str(p) for p in paths[:5]]}


def resolve_local(value: str | None, *bases: Path) -> Path | None:
    if not value:
        return None
    p = Path(value)
    if p.is_absolute():
        return p
    for base in bases:
        q = base / p
        if q.is_file():
            return q
    return None


def hash_verified(row: dict, *bases: Path) -> tuple[bool, str | None, str | None]:
    digest = row.get("sha256") or row.get("localSha256") or row.get("sourceHash")
    if not isinstance(digest, str) or not SHA_RE.match(digest):
        return False, None, None
    for key in ("file", "sourcePath", "localPath", "optimizedPath", "destinationPath"):
        p = resolve_local(row.get(key), *bases)
        if p and p.is_file():
            b = p.read_bytes()
            if len(b) > 0 and hashlib.sha256(b).hexdigest() == digest and (row.get("bytes") in {None, len(b)}):
                return True, str(p), digest
    return False, None, None


def http_evidence(name: str, manifest_row: dict, http_dir: Path) -> dict | None:
    reqs = manifest_row.get("requests") if isinstance(manifest_row, dict) else None
    rel_file = str(manifest_row.get("file") or "")
    digest = manifest_row.get("sha256") if isinstance(manifest_row, dict) else None
    if not isinstance(reqs, list):
        # Fall back to a per-hash HTTP JSON record when present.
        if isinstance(digest, str):
            p = http_dir / f"{digest}{Path(rel_file).suffix}.json"
            doc = read_json(p) if p.is_file() else None
            if isinstance(doc, dict):
                reqs = doc.get("requests")
    get = next((x for x in reqs or [] if isinstance(x, dict) and str(x.get("method", "")).upper() == "GET" and x.get("status") == 200), None)
    if not get:
        return None
    ct = get.get("contentType") or ((get.get("headers") or {}).get("Content-Type"))
    size = get.get("bytes") or get.get("contentLength")
    if ct and isinstance(size, int) and size > 0:
        http_path = str(http_dir / f"{digest or 'unknown'}{Path(rel_file).suffix}.json") if digest else str(http_dir)
        return {
            "httpPath": http_path,
            "manifestPath": str(WS_FILES["cdnAll"]),
            "status": get.get("status"),
            "contentType": ct,
            "bodySize": size,
            "sha256": manifest_row.get("sha256"),
            "name": name,
        }
    return None


def build_snapshot() -> tuple[dict, int]:
    peer = {}
    for key, p in HY3D_FILES.items(): peer[f"hy3d.{key}"] = manifest_state(p)
    peer["hy3d.contentGaps"] = glob_state(HY3D / "output", "content-gaps*.json")
    for key, p in WS_FILES.items():
        peer[f"wscheppity.{key}"] = glob_state(p, "*") if key == "httpDir" else manifest_state(p)
    for key, p in EXTRA_FILES.items():
        peer[f"extra.{key}"] = glob_state(p, "*") if key == "httpDir" else manifest_state(p)
    for key, p in OS_FILES.items(): peer[f"oscraft.{key}"] = manifest_state(p)

    content = read_json(HY3D_FILES["content"]) or {}
    demand_v2 = read_json(HY3D_FILES["demandV2"]) or {}
    generation = read_json(HY3D_FILES["generation"]) or {}
    recovery = read_json(HY3D_FILES["recovery"]) or {}
    probes = read_json(HY3D_FILES["probes"]) or {}
    ws_extraction = read_json(WS_FILES["extraction"]) or {}
    ws_all = read_json(WS_FILES["cdnAll"]) or {}
    ws_active = read_json(WS_FILES["cdnActive"]) or {}
    extra_extraction = read_json(EXTRA_FILES["extraction"]) or {}
    extra_contract = read_json(EXTRA_FILES["contract"]) or {}
    extra_all = read_json(EXTRA_FILES["cdnAll"]) or {}
    extra_active = read_json(EXTRA_FILES["cdnActive"]) or {}
    os_ui = read_json(OS_FILES["ui"]) or {}
    os_snapshot = read_json(OS_FILES["crossContract"]) or {}
    os_ids = OS_FILES["identifiers"].read_text() if OS_FILES["identifiers"].is_file() else ""

    # Evidence indexes.
    hy_items = {x.get("slug"): x for x in (demand_v2.get("items") or content.get("rows") or []) if isinstance(x, dict) and x.get("slug")}
    hy_requested = {x.get("slug"): x for x in demand_v2.get("requested", []) if isinstance(x, dict)}
    hy_endpoint = {x.get("slug"): x for x in demand_v2.get("endpointBlocked", []) if isinstance(x, dict)}
    hy_owner = {x.get("slug"): x for x in demand_v2.get("ownerDecision", []) if isinstance(x, dict)}
    hy_open = {x.get("slug"): x for x in demand_v2.get("intentionallyOpen", []) if isinstance(x, dict)}
    ws_by_name = {x.get("name"): x for x in ws_all.get("assets", []) if isinstance(x, dict) and x.get("name")}
    ws_active_by_name = {x.get("name"): x for x in ws_active.get("assets", []) if isinstance(x, dict) and x.get("name")}
    http_dir = WS_FILES["httpDir"]
    http_by_name: dict[str, dict] = {}
    for hp in sorted(http_dir.glob("*.json")):
        hd = read_json(hp)
        if isinstance(hd, dict) and isinstance(hd.get("name"), str):
            http_by_name.setdefault(hd["name"], {"doc": hd, "path": str(hp)})
    extra_by_name = {x.get("name"): x for x in extra_all.get("assets", []) if isinstance(x, dict) and x.get("name")}
    extra_http_by_name: dict[str, dict] = {}
    for hp in sorted(EXTRA_FILES["httpDir"].glob("*.json")):
        hd = read_json(hp)
        if isinstance(hd, dict) and isinstance(hd.get("name"), str):
            extra_http_by_name.setdefault(hd["name"], {"doc": hd, "path": str(hp)})

    queue = read_json(E / "content-request-queue.json") or {}
    gaps = read_json(E / "spawn-extraction-gaps.json") or {}
    out_rows = []

    def emit(qrow: dict, queue_name: str) -> None:
        slug = qrow.get("demandSlug", "")
        prior = qrow.get("status")
        evidence_paths = [x for x in str(qrow.get("evidence") or "").split("; ") if x]
        status = "UNAVAILABLE"
        next_actor = qrow.get("nextActor") or "bota"
        evidence = {"paths": evidence_paths, "reason": "no matching live evidence"}
        validation = {}
        decision_id = None
        if queue_name == "hy3d-content":
            base_peer = HY3D_FILES["content"]
            if not base_peer.is_file() or not HY3D_FILES["generation"].is_file():
                evidence = {"paths": [str(base_peer), str(HY3D_FILES["generation"])], "reason": "peer path missing"}
            else:
                item = hy_items.get(slug)
                ok, local_path, digest = hash_verified(item or {}, HY3D, ROOT, WS)
                if ok and item and item.get("status") in {"available", "ready"}:
                    status, next_actor = "available", "bota"
                    evidence = {"paths": [str(HY3D_FILES["content"]), local_path], "sha256": digest}
                    validation = item.get("validation", {})
                elif slug in hy_owner:
                    status, next_actor, decision_id = "owner-decision", "owner", "forever_eternal_loop_clip"
                    evidence = {"paths": [str(HY3D_FILES["demandV2"]), "export/decision-packet.json#forever_eternal_loop_clip"], "decisionId": decision_id}
                elif slug in hy_open:
                    status, next_actor, decision_id = "intentionally-open", "bota", "presentation_cue_intentionally_open"
                    evidence = {"paths": [str(HY3D_FILES["demandV2"]), "plan/16-humor-and-tone.md:8"], "decisionId": decision_id}
                elif slug in hy_endpoint or slug in hy_requested:
                    src = hy_endpoint.get(slug) or hy_requested.get(slug) or {}
                    relay_evidence = bool(recovery.get("recovery") is False or generation.get("studioDiagnosis", {}).get("httpStatus") == 500)
                    status = "requested-relay" if prior == "requested-relay" and relay_evidence else "requested-pooled-email"
                    next_actor = "hy3d"
                    evidence = {"paths": [str(HY3D_FILES["demandV2"]), str(HY3D_FILES["generation"]), str(HY3D_FILES["recovery"])], "quota": demand_v2.get("quota", {}).get("total"), "classification": src.get("classification") or src.get("method")}
                    validation = {"recovery": recovery.get("recovery"), "quota": demand_v2.get("quota", {}).get("total")}
                else:
                    status, next_actor = "UNAVAILABLE", "hy3d"
                    evidence = {"paths": [str(HY3D_FILES["demandV2"])], "reason": "queue row has no matching live hy3d demand evidence"}
        elif queue_name == "extra-extraction" or str(slug).startswith("extra-cdn/") or qrow.get("peer") == "extra":
            name = qrow.get("sourceUrl") or ("/" + str(slug).removeprefix("extra-cdn/"))
            if not EXTRA_FILES["cdnAll"].is_file() or not EXTRA_FILES["extraction"].is_file():
                evidence = {"paths": [str(EXTRA_FILES["cdnAll"]), str(EXTRA_FILES["extraction"])], "reason": "extra peer path missing"}
            else:
                item = extra_by_name.get(name)
                ok, local_path, digest = hash_verified(item or {}, EXTRA, ROOT)
                if ok:
                    status, next_actor = "available", "extra"
                    evidence = {"paths": [str(EXTRA_FILES["cdnAll"]), local_path, str(EXTRA_FILES["extraction"])], "sha256": digest}
                    validation = {"bytes": item.get("bytes"), "sha256Match": True, "peer": "extra"}
                else:
                    hdrec = extra_http_by_name.get(name)
                    get = None
                    if hdrec:
                        get = next((x for x in hdrec["doc"].get("requests", []) if isinstance(x, dict) and str(x.get("method", "")).upper() == "GET"), None)
                    elif item:
                        get = next((x for x in item.get("requests", []) if isinstance(x, dict) and str(x.get("method", "")).upper() == "GET"), None)
                    if get or item:
                        status, next_actor = "spawn-generated", "extra"
                        evidence = {"paths": [str(EXTRA_FILES["extraction"]), str(EXTRA_FILES["cdnAll"]), hdrec["path"] if hdrec else str(EXTRA_FILES["httpDir"])], "http": {"status": (get or {}).get("status"), "contentType": (get or {}).get("contentType"), "bodySize": (get or {}).get("bytes") or (item or {}).get("bytes"), "sha256": (item or {}).get("sha256")}}
                        validation = {"exactGeneratedOnDemandEvidence": True, "peer": "extra", "httpStatus": (get or {}).get("status"), "contentType": (get or {}).get("contentType"), "bodySize": (get or {}).get("bytes") or (item or {}).get("bytes"), "sha256": (item or {}).get("sha256")}
                    else:
                        status, next_actor = "UNAVAILABLE", "extra"
                        evidence = {"paths": [str(EXTRA_FILES["cdnAll"]), str(EXTRA_FILES["httpDir"])], "reason": "no extra CDN or HTTP evidence"}
        else:
            name = qrow.get("sourceUrl") or ("/" + slug.removeprefix("spawn-cdn/"))
            if not WS_FILES["cdnAll"].is_file() or not WS_FILES["extraction"].is_file():
                evidence = {"paths": [str(WS_FILES["cdnAll"]), str(WS_FILES["extraction"])], "reason": "peer path missing"}
            else:
                item = ws_by_name.get(name) or ws_active_by_name.get(name)
                ok, local_path, digest = hash_verified(item or {}, WS, ROOT, HY3D)
                if ok:
                    status, next_actor = "available", "bota"
                    evidence = {"paths": [str(WS_FILES["cdnAll"]), local_path], "sha256": digest}
                    validation = {"bytes": item.get("bytes"), "sha256Match": True}
                else:
                    he = http_evidence(name, item or {}, http_dir)
                    exact_http = None
                    hdrec = http_by_name.get(name)
                    if hdrec:
                        hd = hdrec["doc"]
                        get = next((x for x in hd.get("requests", []) if isinstance(x, dict) and str(x.get("method", "")).upper() == "GET"), None)
                        exact_http = {"path": hdrec["path"], "status": get.get("status") if get else None, "contentType": (get or {}).get("contentType"), "bodySize": (get or {}).get("bytes"), "sha256": hd.get("sha256")}
                    if he or exact_http:
                        status, next_actor = "spawn-generated", "wscheppity"
                        evidence = {"paths": [str(WS_FILES["cdnAll"]), str(http_dir)], "http": he or exact_http}
                        validation = {"httpStatus": (he or exact_http).get("status"), "contentType": (he or exact_http).get("contentType"), "bodySize": (he or exact_http).get("bodySize"), "sha256": (he or {}).get("sha256") or (exact_http or {}).get("sha256"), "exactGeneratedOnDemandEvidence": True}
                    else:
                        status, next_actor = "UNAVAILABLE", "wscheppity"
                        evidence = {"paths": [str(WS_FILES["cdnAll"]), str(http_dir)], "reason": "peer path present but no exact HTTP record for CDN name"}
        out_rows.append({
            "stableId": qrow.get("stableId"), "queue": queue_name, "demandSlug": slug,
            "priorStatus": prior, "status": status, "nextActor": next_actor,
            "ruleCitation": qrow.get("ruleCitation"), "evidence": evidence,
            "validation": validation, "decisionId": decision_id,
            "identifierSafe": not any(x in slug.lower() for x in FORBIDDEN) and not OLD_SLUG.match(slug),
        })

    for r in queue.get("rows", []): emit(r, "hy3d-content")
    for r in gaps.get("rows", []): emit(r, "extra-extraction" if r.get("peer") == "extra" or str(r.get("demandSlug", "")).startswith("extra-cdn/") else "wscheppity-extraction")

    counts = {s: sum(r["status"] == s for r in out_rows) for s in STATUSES}
    actor_counts = {a: sum(r["nextActor"] == a for r in out_rows if r["status"] not in {"available", "intentionally-open"}) for a in ["hy3d", "wscheppity", "extra", "owner", "bota"]}
    identifier = {
        "mode": "bota-fullname" if os_ui.get("identifierMode") == "bota-fullname" and "bota-fullname" in os_ids else "UNAVAILABLE",
        "defaultDotaAcronyms": bool(os_snapshot.get("identifierMode", {}).get("defaultDota") == "default-dota-acronyms"),
        "botaFullnameIds": os_snapshot.get("counts", {}).get("botaFullnameIds"),
        "defaultAcronymIds": os_snapshot.get("counts", {}).get("defaultAcronymIds"),
        "paths": [str(OS_FILES["identifiers"]), str(OS_FILES["crossContract"]), str(OS_FILES["ui"])],
    }
    peer_counts = {
        "hy3d": {"contractRows": content.get("counts", {}).get("rows"), "demandV2Rows": demand_v2.get("counts", {}).get("rows"), "requested": demand_v2.get("counts", {}).get("requested"), "quota": demand_v2.get("quota", {}).get("total"), "recovery": recovery.get("recovery"), "probeCount": probes.get("count")},
        "wscheppity": {"summary": ws_extraction.get("summary", {}), "allNames": ws_all.get("uniqueNames") or ws_all.get("count"), "ok": ws_all.get("ok"), "bad": ws_all.get("bad"), "httpFiles": peer["wscheppity.httpDir"]["count"]},
        "extra": {"manifestStatus": peer["extra.extraction"]["status"], "contractStatus": peer["extra.contract"]["status"], "cdnAllStatus": peer["extra.cdnAll"]["status"], "httpStatus": peer["extra.httpDir"]["status"], "summary": extra_extraction.get("summary", {}), "cdnNames": extra_all.get("uniqueNames") or extra_all.get("count"), "cdnOk": extra_all.get("ok"), "cdnBad": extra_all.get("bad"), "httpFiles": peer["extra.httpDir"]["count"], "firstClassPeer": True},
        "oscraft": identifier,
    }
    resolved = [r for r in out_rows if r["status"] == "available"]
    unresolved = [r for r in out_rows if r["status"] != "available"]
    unexplained = [r for r in out_rows if r["status"] == "UNAVAILABLE"]
    doc = {
        "schema": "bota.coordination-status/v1",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "readOnly": True,
        "bounded": {"defaultMinutes": 10, "defaultPollSeconds": 10, "once": ARGS.once},
        "peerManifests": peer,
        "peerCounts": peer_counts,
        "counts": {
            "rows": len(out_rows), "resolved": len(resolved), "unresolved": len(unresolved), "unexplainedUnavailable": len(unexplained),
            **counts, "hy3dQueue": len(queue.get("rows", [])), "spawnGaps": len(gaps.get("rows", [])),
        },
        "nextActorQueueCounts": actor_counts,
        "identifierMode": identifier["mode"],
        "defaultDotaAcronyms": identifier["defaultDotaAcronyms"],
        "engineResolvedExists": (E / "engine-resolved").exists(),
        "rows": out_rows,
    }
    lines = [
        "# BOTA live coordination status", "",
        f"Generated: `{doc['generatedAt']}`", f"Mode: `{identifier['mode']}`; default Dota acronyms: `{str(identifier['defaultDotaAcronyms']).lower()}`; engine-resolved absent: `{str(not doc['engineResolvedExists']).lower()}`.", "",
        "## Counts", "",
        f"- Rows: `{len(out_rows)}`; resolved/available: `{len(resolved)}`; unresolved evidence-backed: `{len(unresolved)-len(unexplained)}`; unexplained UNAVAILABLE: `{len(unexplained)}`.",
        f"- Statuses: " + ", ".join(f"`{k}={v}`" for k, v in counts.items()) + ".",
        f"- Next actors: " + ", ".join(f"`{k}={v}`" for k, v in actor_counts.items()) + ".", "",
        "## Peer evidence", "",
        f"- hy3d: contract rows `{peer_counts['hy3d']['contractRows']}`, demand-v2 rows `{peer_counts['hy3d']['demandV2Rows']}`, requested `{peer_counts['hy3d']['requested']}`, quota `{peer_counts['hy3d']['quota']}`, recovery `{peer_counts['hy3d']['recovery']}`.",
        f"- wscheppity: CDN names `{peer_counts['wscheppity']['allNames']}`, ok `{peer_counts['wscheppity']['ok']}`, bad `{peer_counts['wscheppity']['bad']}`, HTTP files `{peer_counts['wscheppity']['httpFiles']}`.",
        f"- extra: extraction `{peer_counts['extra']['manifestStatus']}`, contract `{peer_counts['extra']['contractStatus']}`, CDN names `{peer_counts['extra']['cdnNames']}`, ok `{peer_counts['extra']['cdnOk']}`, bad `{peer_counts['extra']['cdnBad']}`, HTTP files `{peer_counts['extra']['httpFiles']}`, first-class peer `{str(peer_counts['extra']['firstClassPeer']).lower()}`.",
        f"- extra root: `{EXTRA}`; nested git repo (read-only) may be `/workspace/extra/game-16`.",
        f"- oscraft: BOTA fullname IDs `{identifier['botaFullnameIds']}`, default acronym IDs `{identifier['defaultAcronymIds']}`.", "",
        "## Exact evidence paths", "",
    ]
    for k, v in peer.items(): lines.append(f"- `{k}`: `{v['path']}` — `{v['status']}`" + (f", count `{v['count']}`" if "count" in v else ""))
    lines += ["", "## Unresolved rows", ""]
    for r in unresolved[:30]: lines.append(f"- `{r['demandSlug']}` → `{r['status']}` / `{r['nextActor']}`; evidence `{json.dumps(r['evidence'], sort_keys=True)}`")
    if len(unresolved) > 30: lines.append(f"- … and `{len(unresolved)-30}` more; see `coordination-status.json`.")
    (E / "coordination-status.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    (E / "coordination-status.md").write_text("\n".join(lines) + "\n")
    # Keep only the watcher's two output hashes current; no conformance/engine writes.
    sums_path = E / "SHA256SUMS.json"
    if sums_path.is_file():
        sums = json.loads(sums_path.read_text())
        sums["coordination-status.json"] = file_sha(E / "coordination-status.json")
        sums["coordination-status.md"] = file_sha(E / "coordination-status.md")
        conf_path = E / "conformance.json"
        conf = json.loads(conf_path.read_text())
        conf.setdefault("expected_hashes", {})["coordination-status.json"] = sums["coordination-status.json"]
        conf["expected_hashes"]["coordination-status.md"] = sums["coordination-status.md"]
        conf_path.write_text(json.dumps(conf, indent=2, sort_keys=True) + "\n")
        sums["conformance.json"] = file_sha(conf_path)
        sums_path.write_text(json.dumps(sums, indent=2, sort_keys=True) + "\n")
    print(f"COORDINATION once={str(ARGS.once).lower()} rows={len(out_rows)} resolved={len(resolved)} unresolved={len(unresolved)} unexplained={len(unexplained)}")
    print("STATUS_COUNTS " + " ".join(f"{k}={v}" for k, v in counts.items()))
    print("NEXT_ACTORS " + " ".join(f"{k}={v}" for k, v in actor_counts.items()))
    return doc, len(unexplained)


parser = argparse.ArgumentParser(description="Bounded read-only BOTA coordination watcher")
parser.add_argument("--once", action="store_true", help="run one pass and exit")
parser.add_argument("--minutes", type=float, default=10, help="bounded runtime in minutes (default 10)")
parser.add_argument("--poll-seconds", type=float, default=10, help="poll interval (default 10)")
ARGS = parser.parse_args()


def main() -> int:
    deadline = time.monotonic() + max(0.0, ARGS.minutes) * 60
    last_code = 0
    while True:
        doc, unexplained = build_snapshot()
        drift = doc["counts"]["rows"] != doc["counts"]["hy3dQueue"] + doc["counts"]["spawnGaps"]
        last_code = 1 if unexplained or drift or doc["identifierMode"] != "bota-fullname" or not doc["defaultDotaAcronyms"] or doc["engineResolvedExists"] else 0
        if ARGS.once:
            print("COORDINATION_STATUS " + ("PASS" if last_code == 0 else "FAIL"))
            return last_code
        if time.monotonic() >= deadline:
            print("COORDINATION_WATCH bounded exit")
            return last_code
        time.sleep(max(0.1, ARGS.poll_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
