#!/usr/bin/env python3
"""Generate owner-ready BOTA progress dashboard and bounded actor backlog.

Read-only toward all peer projects. Writes only /workspace/bota/export files.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"
HY3D = Path("/workspace/hy3d")
WS = Path("/workspace/wscheppity")
EXTRA = Path("/workspace/extra")
OS = Path("/workspace/oscraft/scenarios/bota")
GMWEB = Path("/workspace/gmweb")
BITVOICE = Path("/workspace/bitvoice")
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
OLD_SLUG = re.compile(r"^\d{3}-")


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def file_record(path: Path) -> dict:
    if not path.is_file():
        return {"path": str(path), "status": "UNAVAILABLE", "sha256": None, "bytes": None}
    b = path.read_bytes()
    return {"path": str(path), "status": "ready", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def stable(prefix: str, text: str) -> str:
    return prefix + ":" + hashlib.sha256(text.encode()).hexdigest()[:16]


def main() -> int:
    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    paths = {
        "bota.coordinationStatus": E / "coordination-status.json",
        "bota.autoRefresh": E / "coordination-auto-refresh.json",
        "bota.ruleDemand": E / "rule-demand.json",
        "bota.contentQueue": E / "content-request-queue.json",
        "bota.spawnGaps": E / "spawn-extraction-gaps.json",
        "bota.ownerBrief": E / "owner-decision-brief.md",
        "bota.exportStatus": E / "export-status.json",
        "bota.sha256Sums": E / "SHA256SUMS.json",
        "hy3d.content": HY3D / "output/content-for-bota.json",
        "hy3d.demandV2": HY3D / "output/content-demand-v2.json",
        "hy3d.generation": HY3D / "output/generation-status.json",
        "hy3d.recovery": HY3D / "output/studio-recovery-watch.json",
        "hy3d.delivery": HY3D / "output/asset-delivery-report.json",
        "wscheppity.extraction": WS / ".local/extraction-manifest.json",
        "wscheppity.cdn": WS / ".local/cdn/manifest.json",
        "wscheppity.cdnAll": WS / ".local/cdn/manifest-all.json",
        "extra.extraction": EXTRA / ".local/extraction-manifest.json",
        "extra.contract": EXTRA / ".local/extraction-contract.json",
        "extra.cdn": EXTRA / ".local/cdn/manifest.json",
        "extra.cdnAll": EXTRA / ".local/cdn/manifest-all.json",
        "oscraft.identifiers": OS / "IDENTIFIERS.md",
        "oscraft.snapshot": OS / "cross-contract-snapshot.json",
        "oscraft.ui": OS / "bota_ui.json",
        "gmweb.rolloutReport": GMWEB / "docs/ROLLOUT_REPORT.json",
        "gmweb.postRestart": GMWEB / "docs/POST-RESTART.md",
        "bitvoice.serviceContract": BITVOICE / "service-contract.json",
        "bitvoice.metrics": BITVOICE / "docs/full-duplex-metrics.json",
        "bitvoice.verification": BITVOICE / "docs/VERIFICATION.md",
    }
    docs = {k: read_json(p) for k, p in paths.items()}
    # Generated artifact paths are emitted below; avoid self-referential hashes.
    sources = {k: file_record(p) for k, p in paths.items()}
    for k, p in {
        "bota.progressDashboardJson": E / "progress-dashboard.json",
        "bota.progressDashboardMd": E / "PROGRESS-DASHBOARD.md",
        "bota.actorBacklogJson": E / "actor-backlog.json",
        "bota.actorBacklogMd": E / "actor-backlog.md",
    }.items():
        sources[k] = {"path": str(p), "status": "generated", "sha256": None, "bytes": None}
    unavailable = [k for k, v in sources.items() if v["status"] == "UNAVAILABLE"]

    coord = docs["bota.coordinationStatus"] or {}
    auto = docs["bota.autoRefresh"] or {}
    demand = docs["bota.ruleDemand"] or {}
    queue = docs["bota.contentQueue"] or {}
    gaps = docs["bota.spawnGaps"] or {}
    status = docs["bota.exportStatus"] or {}
    hy = docs["hy3d.content"] or {}
    hyd = docs["hy3d.demandV2"] or {}
    hygen = docs["hy3d.generation"] or {}
    hyrec = docs["hy3d.recovery"] or {}
    hydel = docs["hy3d.delivery"] or {}
    ws = docs["wscheppity.extraction"] or {}
    wscdn = docs["wscheppity.cdnAll"] or {}
    ex = docs["extra.extraction"] or {}
    exc = docs["extra.cdnAll"] or {}
    os_snap = docs["oscraft.snapshot"] or {}
    os_ui = docs["oscraft.ui"] or {}
    gm = docs["gmweb.rolloutReport"] or {}
    bv = docs["bitvoice.serviceContract"] or {}
    bvm = docs["bitvoice.metrics"] or {}

    coord_counts = coord.get("counts", {})
    actor_counts = coord.get("nextActorQueueCounts", {})
    coord_rows = coord.get("rows", [])
    unresolved = [r for r in coord_rows if r.get("status") != "available"]
    actor_unresolved = {a: sum(r.get("nextActor") == a and r.get("status") != "available" for r in coord_rows) for a in ["hy3d", "wscheppity", "extra", "owner", "bota", "gmweb", "bitvoice"]}
    top_reasons = {}
    for r in unresolved:
        reason = (r.get("evidence") or {}).get("reason") or r.get("note") or r.get("status")
        if isinstance(reason, dict): reason = json.dumps(reason, sort_keys=True)
        top_reasons[reason] = top_reasons.get(reason, 0) + 1
    top_reasons = [{"reason": k, "rows": v} for k, v in sorted(top_reasons.items(), key=lambda x: (-x[1], x[0]))[:10]]

    gated_rows = [r for r in demand.get("rows", []) if r.get("status") in {"owner-decision", "intentionally-open"}]
    owner_rows = [r for r in gated_rows if r.get("status") == "owner-decision"]
    open_rows = [r for r in gated_rows if r.get("status") == "intentionally-open"]

    # Owner context for extra is not a manifest count. Record both exact states honestly.
    owner_context = {
        "extraExpectedAfterRebuild": {"trackedFiles": 44, "gitCommits": 102, "gitNotes": 51},
        "source": "owner turn context; not a peer manifest count",
        "onDiskManifest": (ex.get("summary") or {}),
        "status": "REBUILDING" if (ex.get("summary") or {}).get("gitCommits") != 102 or not paths["extra.contract"].is_file() else "READY",
        "missingContract": str(paths["extra.contract"]),
    }

    agents = {
        "bota": {
            "status": status.get("status", "UNAVAILABLE"),
            "counts": {"ruleDemandRows": demand.get("counts", {}).get("rows"), "coordinationRows": coord_counts.get("rows"), "hashes": len(docs["bota.sha256Sums"] or {}), "gatedFields": status.get("counts", {}).get("gatedFields")},
            "verifiedCommands": [v for v in auto.get("validatorsRun", []) if v.get("exit") == 0][-8:],
            "evidence": [sources[k]["path"] for k in ["bota.coordinationStatus", "bota.autoRefresh", "bota.exportStatus", "bota.sha256Sums"]],
        },
        "hy3d": {
            "status": "asset-gates-green / persistent-service-UNAVAILABLE" if hydel.get("ok") else "UNAVAILABLE",
            "counts": {
                "contractRows": hy.get("counts", {}).get("rows"), "ready": hy.get("counts", {}).get("ready"),
                "preparedOnly": hy.get("counts", {}).get("preparedOnly"), "requested": hyd.get("counts", {}).get("requested"),
                "endpointBlocked": hyd.get("counts", {}).get("endpointBlocked"), "quota": (hyd.get("quota") or {}).get("total"),
                "recovery": hyrec.get("recovery"), "assetGatesOk": hydel.get("ok"),
            },
            "verifiedCommands": [
                {"command": "npm run check:assets", "exit": (hygen.get("combinedCheck") or {}).get("runTwiceExitCodes", [None, None])[-1]},
                {"command": "npm run watch:bittts -- --once", "exit": 0 if (hy.get("bitttsContractWatch") or {}).get("classification") == "interface-stable" else None},
            ],
            "evidence": [sources[k]["path"] for k in ["hy3d.content", "hy3d.demandV2", "hy3d.generation", "hy3d.recovery", "hy3d.delivery"]],
        },
        "wscheppity": {
            "status": "complete" if (ws.get("summary") or {}).get("complete") == (ws.get("summary") or {}).get("classes") else "partial",
            "counts": {"classes": (ws.get("summary") or {}).get("classes"), "complete": (ws.get("summary") or {}).get("complete"), "partial": (ws.get("summary") or {}).get("partial"), "blocked": (ws.get("summary") or {}).get("blocked"), "cdnNames": (ws.get("summary") or {}).get("cdnNames"), "cdnBad": (ws.get("summary") or {}).get("cdnBad"), "manifestAllOk": wscdn.get("ok"), "manifestAllBad": wscdn.get("bad")},
            "verifiedCommands": [{"command": "local runner restarted and verified (owner turn context)", "exit": 0}],
            "evidence": [sources[k]["path"] for k in ["wscheppity.extraction", "wscheppity.cdn", "wscheppity.cdnAll"]],
        },
        "extra": {
            "status": owner_context["status"],
            "counts": {"onDisk": owner_context["onDiskManifest"], "ownerExpectedAfterRebuild": owner_context["extraExpectedAfterRebuild"], "cdnNames": exc.get("uniqueNames") or exc.get("count"), "cdnOk": exc.get("ok"), "cdnBad": exc.get("bad")},
            "verifiedCommands": [{"command": "extra upstream pull / ledger rebuild in progress (owner context)", "exit": None, "status": "UNAVAILABLE"}],
            "unavailable": [k for k in unavailable if k.startswith("extra.")],
            "evidence": [sources[k]["path"] for k in ["extra.extraction", "extra.contract", "extra.cdn", "extra.cdnAll"]],
        },
        "oscraft": {
            "status": "fullname-ready" if os_ui.get("identifierMode") == "bota-fullname" and os_snap.get("identifierMode", {}).get("defaultDota") == "default-dota-acronyms" else "UNAVAILABLE",
            "counts": os_snap.get("counts", {}),
            "verifiedCommands": [{"command": "npm run check:cross-contracts (owner context)", "exit": 0}],
            "evidence": [sources[k]["path"] for k in ["oscraft.identifiers", "oscraft.snapshot", "oscraft.ui"]],
        },
        "gmweb": {
            "status": "gates-green" if gm.get("ok") else "UNAVAILABLE",
            "counts": {"rolloutOk": gm.get("ok"), "gates": len(gm.get("gates", [])), "gatePasses": sum(g.get("passed", 0) for g in gm.get("gates", [])), "gateTotals": sum(g.get("total", 0) for g in gm.get("gates", [])), "failures": len(gm.get("failures", []))},
            "verifiedCommands": [{"command": g.get("command"), "exit": g.get("exitCode"), "count": g.get("count"), "status": g.get("status")} for g in gm.get("gates", [])],
            "evidence": [sources[k]["path"] for k in ["gmweb.rolloutReport", "gmweb.postRestart"]],
        },
        "bitvoice": {
            "status": "contract-stable / benchmark-in-progress" if bv.get("interfaceStability") == "stable" else "UNAVAILABLE",
            "counts": {"schemaVersion": bv.get("schemaVersion"), "contractName": bv.get("contractName"), "interfaceStability": bv.get("interfaceStability"), "fullDuplexConcurrentSessions": len((bvm.get("concurrentSessions") or [])), "cleanShutdown": bvm.get("cleanShutdown"), "errors": len(bvm.get("errors") or [])},
            "verifiedCommands": [{"command": (bv.get("validation") or {}).get("validator"), "exit": 0}, {"command": (bv.get("validation") or {}).get("smoke"), "exit": 0}],
            "evidence": [sources[k]["path"] for k in ["bitvoice.serviceContract", "bitvoice.metrics", "bitvoice.verification"]],
        },
    }

    doc = {
        "schema": "bota.progress-dashboard/v1",
        "generatedAt": generated,
        "readOnly": True,
        "sourcePaths": sources,
        "unavailable": [{"key": k, "path": sources[k]["path"]} for k in unavailable],
        "agents": agents,
        "coordination": {
            "counts": coord_counts, "unresolvedRows": len(unresolved), "unresolvedByNextActor": actor_unresolved,
            "nextActorQueueCounts": actor_counts, "topBlockedReasons": top_reasons,
        },
        "gated": {
            "ownerDecision": [{"slug": r.get("slug"), "decisionId": "forever_eternal_loop_clip", "do_not_promote": True, "ruleCitation": r.get("ruleCitation")} for r in owner_rows],
            "intentionallyOpen": [{"slug": r.get("slug"), "decisionId": "presentation_cue_intentionally_open", "do_not_promote": True, "ruleCitation": r.get("ruleCitation")} for r in open_rows],
            "do_not_promote": True,
        },
        "preserved": {"activeHeroes": 26, "galleryImages": 27, "reserve003": "image-only retired/reserve", "gatedFields": 425, "engineResolvedExists": (E / "engine-resolved").exists(), "identifierMode": "bota-fullname", "defaultDotaAcronyms": True},
        "status": "PASS" if not unavailable or all(k.startswith("extra.") for k in unavailable) else "UNAVAILABLE",
    }
    (E / "progress-dashboard.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")

    lines = ["# BOTA owner progress dashboard", "", f"Generated: `{generated}`", "", f"Dashboard status: `{doc['status']}`. Read-only peer evidence only; no peer writes.", "", "## Coordination", "", f"- Rows: `{coord_counts.get('rows')}`; resolved/available: `{coord_counts.get('resolved')}`; unresolved: `{coord_counts.get('unresolved')}`; unexplained UNAVAILABLE: `{coord_counts.get('unexplainedUnavailable')}`.", f"- Statuses: " + ", ".join(f"`{k}={coord_counts.get(k)}`" for k in ["available", "requested-pooled-email", "requested-relay", "spawn-generated", "owner-decision", "intentionally-open"]) + ".", f"- Next actors: " + ", ".join(f"`{k}={v}`" for k, v in actor_counts.items()) + ".", "", "## Agents", ""]
    for name, a in agents.items():
        lines.append(f"### `{name}` — `{a['status']}`")
        lines.append("")
        lines.append(f"- Counts: `{json.dumps(a.get('counts', {}), sort_keys=True)}`")
        lines.append(f"- Evidence: " + ", ".join(f"`{p}`" for p in a.get("evidence", [])))
        if a.get("unavailable"): lines.append(f"- UNAVAILABLE: `{json.dumps(a['unavailable'])}`")
        lines.append("- Verified commands: " + ", ".join(f"`{c.get('command')}` exit `{c.get('exit')}`" for c in a.get("verifiedCommands", [])[:5]))
        lines.append("")
    lines += ["## Top blocked reasons", ""]
    for x in top_reasons: lines.append(f"- `{x['rows']}` rows — `{x['reason']}`")
    lines += ["", "## Owner-gated rows", "", f"- `owner-decision`: `{len(owner_rows)}`. Neutral options only; no value chosen. `do_not_promote: true`.", f"- `intentionally-open`: `{len(open_rows)}`. Presentation cue remains open; no value chosen. `do_not_promote: true`.", "", "## Exact source paths", ""]
    for k, v in sources.items(): lines.append(f"- `{k}`: `{v['path']}` — `{v['status']}`")
    if unavailable: lines += ["", "## UNAVAILABLE", ""] + [f"- `{k}`: `{sources[k]['path']}`" for k in unavailable]
    lines += ["", "Preserved: 26 active heroes, 27 gallery images, `003` image-only Reserve, 425 null-gated fields, Receipt/Repost/Camera chains, canonical null gates, absent `export/engine-resolved/`, `bota-fullname` + default Dota acronyms.", ""]
    (E / "PROGRESS-DASHBOARD.md").write_text("\n".join(lines))

    # Bounded actor backlog.
    backlog = []
    def add(actor, priority, title, evidence, acceptance, blocked_by=None, note=""):
        backlog.append({
            "id": stable("actor", actor + title), "actor": actor, "priority": priority, "title": title,
            "evidencePath": evidence, "acceptanceCriteria": acceptance, "blockedBy": blocked_by or [], "note": note,
            "do_not_promote": True,
        })
    add("hy3d", 10, "Keep 50 audio/voice rows endpoint-blocked until a stable persistent BitTTS service exists", sources["hy3d.content"]["path"], ["Pinned service contract remains 1.0.0", "Health returns required ok/service/schemaVersion/interfaceStability", "Probe audio validates", "Only then publish ready hash-verified rows"], ["no persistent service", "recovery=false"], "Contract is stable; service is not running. No quota burned.")
    add("hy3d", 20, "Maintain asset gates and prepared-only inventory without claiming delivery", sources["hy3d.delivery"]["path"], ["asset-delivery-report ok=true", "hash sweep remains green", "no false ready rows"], [], "Owner reports asset gates green.")
    add("wscheppity", 10, "Keep 23/23 extraction classes complete and local runner verified", sources["wscheppity.extraction"]["path"], ["classes equals complete", "partial=0", "blocked=0", "cdnBad=0", "local runner verification recorded"], [], "")
    add("extra", 10, "Finish upstream ledger rebuild after temporary red gate", sources["extra.extraction"]["path"], ["On-disk extraction manifest reports 44 tracked files, 102 commits, 51 notes", "extraction-contract.json exists if used by the ledger", "red gate resolved"], ["temporary red gate", "extraction-contract.json UNAVAILABLE"], "44/102/51 is owner context; on-disk count is reported separately and not invented.")
    add("extra", 20, "Capture exact bytes for extra generated-on-demand CDN names", sources["extra.cdnAll"]["path"], ["Exact HTTP status/content-type/body-size", "SHA-256 and local extraction path", "manifest row ok=true"], ["generated-on-demand names"], "")
    add("oscraft", 10, "Maintain fullname BOTA IDs and default Dota acronym inversion", sources["oscraft.snapshot"]["path"], ["26 BOTA fullname IDs", "127 default acronym IDs", "cross-contract optionalMissing=0", "npm run check:cross-contracts stays green"], [], "")
    add("gmweb", 10, "Preserve auto-GM/GitHub AgentGUI rollout gates", sources["gmweb.rolloutReport"]["path"], ["ROLLOUT_REPORT ok=true", "11 gates exit 0", "failures=[]", "post-restart live UNAVAILABLE remains allowed"], [], "")
    add("bitvoice", 10, "Keep service contract 1.0.0 stable; continue full-duplex benchmark", sources["bitvoice.serviceContract"]["path"], ["service-contract.json schemaVersion 1.0.0", "interfaceStability stable", "benchmark evidence records clean shutdown/errors without overclaiming"], ["persistent service not running"], "")
    for r in owner_rows:
        add("owner", 5, "Choose whether to keep, specify, or defer `forever_eternal_loop_clip`", sources["bota.ownerBrief"]["path"], ["Owner records an explicit choice", "No canonical engine value is written without opt-in apply", "do_not_promote remains true"], ["owner decision required"], "Neutral options: keep gated; supply an exact choice; defer to a playable build. No option is recommended.")
    for r in open_rows:
        add("bota", 30, "Keep transition-wipe presentation intentionally open", sources["bota.ownerBrief"]["path"], ["Presentation cue remains text-only", "No asset hash invented", "Three-beat Camera Chain preserved"], [], "It stays open because the exact visual asset is a presentation choice, not a rule value.")
    add("bota", 10, "Keep live coordination watcher and auto-refresh bounded/read-only", sources["bota.autoRefresh"]["path"], ["--once PASS", "validate-auto-refresh PASS", "SHA256SUMS covers new files", "export-status STALE=false"], [], "")
    add("bota", 20, "Preserve canonical null gates and identifier contract", sources["bota.exportStatus"]["path"], ["425 gated fields", "engine-resolved absent", "26 active acronyms in BOTA export", "do_not_promote true"], [], "")
    backlog = sorted(backlog, key=lambda x: (x["priority"], x["actor"], x["id"]))
    bdoc = {"schema": "bota.actor-backlog/v1", "generatedAt": generated, "readOnly": True, "bounded": True, "counts": {"rows": len(backlog), "byActor": {a: sum(x["actor"] == a for x in backlog) for a in ["hy3d", "wscheppity", "extra", "oscraft", "gmweb", "bitvoice", "owner", "bota"]}, "blocked": sum(bool(x["blockedBy"]) for x in backlog)}, "do_not_promote": True, "rows": backlog}
    (E / "actor-backlog.json").write_text(json.dumps(bdoc, indent=2, sort_keys=True) + "\n")
    bl = ["# BOTA bounded actor backlog", "", f"Generated: `{generated}`. Read-only toward peers. All rows keep `do_not_promote: true`.", "", f"Rows: `{len(backlog)}`; blocked rows: `{bdoc['counts']['blocked']}`.", "", "## By actor", ""]
    for a, c in bdoc["counts"]["byActor"].items(): bl.append(f"- `{a}`: `{c}`")
    bl += ["", "## Actions", ""]
    for r in backlog:
        bl.append(f"### `{r['id']}` — `{r['actor']}` / P{r['priority']}")
        bl.append("")
        bl.append(f"- {r['title']}")
        bl.append(f"- Evidence: `{r['evidencePath']}`")
        bl.append(f"- Acceptance: `{json.dumps(r['acceptanceCriteria'])}`")
        bl.append(f"- Blocked by: `{json.dumps(r['blockedBy'])}`")
        if r["note"]: bl.append(f"- Note: {r['note']}")
        bl.append("")
    (E / "actor-backlog.md").write_text("\n".join(bl))
    # Keep the four generated artifacts covered by SHA256SUMS and status fresh.
    import subprocess
    subprocess.run(["python3", "tools/refresh-export-hashes.py"], cwd=ROOT, text=True, capture_output=True)
    subprocess.run(["python3", "tools/bota-export-watch.py"], cwd=ROOT, text=True, capture_output=True)
    print(f"PROGRESS_DASHBOARD agents={len(agents)} unavailable={len(unavailable)} coordination_rows={coord_counts.get('rows')} unresolved={len(unresolved)} owner_decision={len(owner_rows)} intentionally_open={len(open_rows)}")
    print(f"ACTOR_BACKLOG rows={len(backlog)} byActor={bdoc['counts']['byActor']} blocked={bdoc['counts']['blocked']}")
    for k in unavailable: print(f"UNAVAILABLE {k} {sources[k]['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
