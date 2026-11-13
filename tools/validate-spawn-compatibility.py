#!/usr/bin/env python3
"""Read-only validator for BOTA ↔ Spawn compatibility report."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
W = Path("/workspace/wscheppity")
E = B / "export"
errors: list[str] = []
unavailable: list[str] = []
checks = 0


def ok() -> None:
    global checks
    checks += 1


def err(message: str) -> None:
    errors.append(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_status(root: Path) -> str:
    p = subprocess.run(["git", "-C", str(root), "status", "--short"], text=True, capture_output=True)
    return p.stdout


def main() -> int:
    if not W.is_dir():
        print(f"UNAVAILABLE: {W} missing")
        print("SPAWN COMPATIBILITY: FAIL (0 checks, 1 unavailable)")
        return 2
    status_before = git_status(W)
    try:
        report = json.loads((E / "spawn-compatibility.json").read_text())
        md_text = (E / "SPAWN-COMPATIBILITY.md").read_text()
        ok()
    except Exception as exc:
        err(f"compatibility files parse/read failed: {exc}")
        report = None
        md_text = ""

    # Both roots and cited paths.
    ok() if B.is_dir() and W.is_dir() else unavailable.append("project root missing")
    if report:
        for rel in report.get("required_paths", {}).get("wscheppity", []):
            if (W / rel).is_file():
                ok()
            else:
                err(f"wscheppity cited path missing: {rel}")
        for rel in report.get("required_paths", {}).get("bota", []):
            if (B / rel).is_file():
                ok()
            else:
                err(f"bota cited path missing: {rel}")

    # Current wscheppity counts.
    tracked = subprocess.run(["git", "-C", str(W), "ls-files"], text=True, capture_output=True).stdout.splitlines()
    refs = subprocess.run(["git", "-C", str(W), "for-each-ref", "--format=%(refname)"], text=True, capture_output=True).stdout.splitlines()
    def count(prefix: str) -> int:
        return sum(1 for x in tracked if x.startswith(prefix))
    live = {
        "tracked_files": len(tracked), "refs": refs, "scripts": count("scripts/"),
        "places": count("places/"), "scene_cells": sum(1 for x in tracked if x.startswith("places/") and x.endswith(".scene")),
        "world_assets": count("world.assets/"), "templates": count("templates/"),
        "ui_files": count("ui/"), "top_level_dirs": sorted({x.split("/")[0] for x in tracked if "/" in x}),
    }
    if report:
        for key, value in live.items():
            if report.get("wscheppity_counts", {}).get(key) == value:
                ok()
            else:
                err(f"wscheppity count {key}: report={report.get('wscheppity_counts', {}).get(key)} live={value}")

    # BOTA counts and hashes.
    sums = json.loads((E / "SHA256SUMS.json").read_text())
    conf = json.loads((E / "conformance.json").read_text())
    decisions = json.loads((E / "decisions.json").read_text())
    field_index = json.loads((E / "field-index.json").read_text())
    bota_counts = {
        "active_heroes": conf["expected_counts"]["active_heroes"], "abilities": conf["expected_counts"]["ability_rows"],
        "voice": conf["expected_counts"]["voice_rows"], "gallery": len(list((B / "gallery").glob("*.jpg"))),
        "decisions": len(decisions["decisions"]), "covered_markers": decisions["marker_scan"]["covered"],
        "gated_fields": field_index["count"], "hashes": len(sums),
        "engine_files": len(list((E / "engine").glob("*.json"))),
    }
    if report:
        for key, value in bota_counts.items():
            if report.get("bota_counts", {}).get(key) == value:
                ok()
            else:
                err(f"bota count {key}: report={report.get('bota_counts', {}).get(key)} live={value}")
        for name, want in report.get("hash_references", {}).items():
            p = E / name
            if p.is_file() and sums.get(name) == want and sha(p) == want:
                ok()
            else:
                err(f"hash reference mismatch: {name}")

    # Identifier and decision-gate safety.
    active = set(conf.get("active_acronyms", []))
    forbidden = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
    bad = [k for k in active if k.lower() in forbidden or re.match(r"^\d{3}-", k) or not re.match(r"^[a-z]{3}$", k)]
    if len(active) == 26 and not bad and (report or {}).get("decision_gates", {}).get("do_not_promote") is True and not (E / "engine-resolved").exists():
        ok()
    else:
        err(f"identifier/decision-gate safety failed: bad={bad} resolved={(E / 'engine-resolved').exists()}")
    leaks = 0
    def walk(node):
        nonlocal leaks
        if isinstance(node, dict):
            if "value" in node and "decisionId" in node and node.get("value") is not None:
                leaks += 1
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    for f in (E / "engine").glob("*.json"):
        walk(json.loads(f.read_text()))
    if leaks == 0 and field_index["count"] == 425:
        ok()
    else:
        err(f"decision-gated leaks={leaks} fields={field_index['count']}")

    # Verdict and concrete evidence from both sides.
    if (report or {}).get("verdict") == "reusable-data" and "not" in md_text.lower() and "same game" in md_text.lower():
        ok()
    else:
        err("verdict or Markdown explanation invalid")
    if report:
        ws = [x for x in report.get("evidence", []) if x.get("side") == "wscheppity" and ":" in x.get("file", "")]
        bs = [x for x in report.get("evidence", []) if x.get("side") == "bota" and ":" in str(x.get("file", ""))]
        # Validate at least one real wscheppity file:line and one real BOTA file:line with its quoted text.
        def valid_ref(item, root):
            spec = item.get("file", "")
            m = re.match(r"^(.+):(\d+)$", spec)
            if not m:
                return False
            p = root / m.group(1)
            if not p.is_file():
                return False
            lines = p.read_text(errors="ignore").splitlines()
            n = int(m.group(2))
            return 1 <= n <= len(lines) and item.get("quote", "") in lines[n - 1]
        if any(valid_ref(x, W) for x in ws):
            ok()
        else:
            err("no valid concrete wscheppity file:line evidence")
        if any(valid_ref(x, B) for x in bs):
            ok()
        else:
            err("no valid concrete BOTA file:line evidence")

    # No write to wscheppity or oscraft by this tool.
    status_after = git_status(W)
    if status_before == status_after:
        ok()
    else:
        err("wscheppity git status changed during validation")
    inv = (report or {}).get("identifier_inversion", {})
    if (inv.get("status") and "full BOTA" in inv.get("oscraftBotaArtifacts", "") and "acronym" in inv.get("defaultDotaHeroes", "").lower()
            and "acronym|bota-fullname" in inv.get("validator", "") and "reusable-data" in inv.get("effectOnVerdict", "")
            and "identifier inversion" in md_text.lower()):
        ok()
    else:
        err("identifier inversion description missing from compatibility report or Markdown")
    if (report or {}).get("content_coordination", {}).get("contentOwner") == "hy3d" and "rule-demand" in (report or {}).get("content_coordination", {}).get("demand", ""):
        ok()
    else:
        err("content coordination / rule-demand description missing")
    print(f"WSCHEPPITY_STATUS_BEFORE_AFTER={'UNCHANGED' if status_before == status_after else 'CHANGED'} lines={len(status_after.splitlines())}")
    print(f"SPAWN_COUNTS files={live['tracked_files']} refs={len(refs)} scripts={live['scripts']} places={live['places']} scenes={live['scene_cells']} assets={live['world_assets']} templates={live['templates']}")
    print(f"BOTA_COUNTS heroes={bota_counts['active_heroes']} abilities={bota_counts['abilities']} voice={bota_counts['voice']} gallery={bota_counts['gallery']} decisions={bota_counts['decisions']} markers={bota_counts['covered_markers']} gated={bota_counts['gated_fields']} hashes={bota_counts['hashes']}")
    print(f"VERDICT={(report or {}).get('verdict')} CANONICAL_LEAKS={leaks} DO_NOT_PROMOTE={(report or {}).get('decision_gates', {}).get('do_not_promote')}")
    if unavailable:
        for u in unavailable:
            print(f"UNAVAILABLE: {u}")
    if errors or unavailable:
        for e in errors:
            print(f"error: {e}")
        print(f"SPAWN COMPATIBILITY: FAIL ({checks} checks, {len(errors)} errors, {len(unavailable)} unavailable)")
        return 1
    print(f"SPAWN COMPATIBILITY: PASS ({checks} checks, 0 errors, 0 unavailable)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
