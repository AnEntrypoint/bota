#!/usr/bin/env python3
"""Bounded auto-refresh for BOTA coordination queues.

Default: 10 minutes / 10s poll. --once: one automation-ready pass.
Writes only /workspace/bota/export/coordination-auto-refresh.json.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"
RECORD = E / "coordination-auto-refresh.json"
HY3D = Path("/workspace/hy3d")
WS = Path("/workspace/wscheppity")
EXTRA = Path("/workspace/extra")
OS = Path("/workspace/oscraft/scenarios/bota")
PEER_PATHS = [
    HY3D / "output/content-for-bota.json", HY3D / "output/content-demand-v2.json",
    HY3D / "output/generation-status.json", HY3D / "output/studio-recovery-watch.json",
    HY3D / "output/spawn-cdn-probes.json",
    WS / ".local/extraction-manifest.json", WS / ".local/cdn/manifest.json", WS / ".local/cdn/manifest-all.json",
    EXTRA / ".local/extraction-manifest.json", EXTRA / ".local/extraction-contract.json",
    EXTRA / ".local/cdn/manifest.json", EXTRA / ".local/cdn/manifest-all.json",
    OS / "IDENTIFIERS.md", OS / "cross-contract-snapshot.json", OS / "bota_ui.json",
]
PEER_DIRS = [WS / ".local/cdn/http", EXTRA / ".local/cdn/http"]
VALIDATORS = [
    ["python3", "tools/validate-coordination-status.py"],
    ["python3", "tools/validate-rule-demand.py"],
    ["python3", "tools/validate-request-queues.py"],
    ["python3", "tools/validate-decision-packet.py"],
    ["python3", "tools/validate-engine-data.py"],
    ["python3", "tools/validate-apply-mechanism.py"],
    ["python3", "tools/validate-integration-live.py", "--identifier-mode", "bota-fullname", "--default-dota-acronyms"],
    ["bash", "tools/check-bota-export.sh"],
]
STATUS_VALIDATORS = [
    ["python3", "tools/refresh-export-hashes.py"],
    ["python3", "tools/bota-export-watch.py"],
    ["python3", "tools/validate-export-status.py"],
]


def sha(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def peer_hashes() -> dict[str, dict]:
    out = {}
    for p in PEER_PATHS:
        out[str(p)] = {"status": "ready" if p.is_file() else "UNAVAILABLE", "sha256": sha(p)}
    for d in PEER_DIRS:
        files = sorted(d.glob("*")) if d.is_dir() else []
        h = hashlib.sha256()
        for p in files:
            h.update(str(p).encode()); h.update((sha(p) or "").encode())
        out[str(d / "*")] = {"status": "ready" if files else "UNAVAILABLE", "count": len(files), "sha256": h.hexdigest()}
    return out


def load(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def counts() -> dict:
    demand = load(E / "rule-demand.json") or {}
    coord = load(E / "coordination-status.json") or {}
    queue = load(E / "content-request-queue.json") or {}
    gaps = load(E / "spawn-extraction-gaps.json") or {}
    return {
        "ruleDemand": demand.get("counts", {}),
        "coordination": coord.get("counts", {}),
        "contentQueueRows": len(queue.get("rows", [])),
        "spawnGapRows": len(gaps.get("rows", [])),
        "extraGapRows": sum(r.get("peer") == "extra" for r in gaps.get("rows", [])),
    }


def run(cmd: list[str], label: str, results: list[dict]) -> int:
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    results.append({"command": " ".join(cmd), "label": label, "exit": p.returncode, "stdoutTail": (p.stdout + p.stderr).strip().splitlines()[-3:]})
    print(f"AUTO_REFRESH {label} EXIT={p.returncode}")
    return p.returncode


def pass_once() -> tuple[dict, int]:
    before_hashes = peer_hashes()
    prev = load(RECORD) or {}
    prev_hashes = prev.get("peerManifestHashes", {})
    before = counts()
    validators_run: list[dict] = []
    errors: list[str] = []
    # Always run the live watcher first.
    if run(["python3", "tools/watch-coordinated-queues.py", "--once"], "watch", validators_run):
        errors.append("watch-coordinated-queues --once failed")
    changed = before_hashes != prev_hashes
    if changed or not prev:
        # Rebuild from live peer evidence. v2 builder publishes demand + both queues.
        if run(["python3", "tools/build-rule-demand-v2.py"], "build-rule-demand-v2", validators_run):
            errors.append("build-rule-demand-v2 failed")
        if run(["python3", "tools/watch-coordinated-queues.py", "--once"], "watch-after-build", validators_run):
            errors.append("post-build watch failed")
        if run(["python3", "tools/refresh-export-hashes.py"], "refresh-export-hashes", validators_run):
            errors.append("hash refresh failed")
        if run(["python3", "tools/build-engine-data.py"], "build-engine-data", validators_run):
            errors.append("build-engine-data failed")
        if run(["python3", "tools/refresh-export-hashes.py"], "refresh-export-hashes-final", validators_run):
            errors.append("final hash refresh failed")
        for cmd in VALIDATORS:
            if run(cmd, cmd[1].split("/")[-1], validators_run):
                errors.append(f"validator failed: {' '.join(cmd)}")
        if run(["python3", "tools/bota-export-watch.py"], "bota-export-watch", validators_run):
            errors.append("status watch failed")
        if run(["python3", "tools/validate-export-status.py"], "validate-export-status", validators_run):
            errors.append("status validator failed")
    else:
        # No peer change: still prove the frozen coordination state is valid.
        for cmd in VALIDATORS[:1] + VALIDATORS[1:3]:
            if run(cmd, cmd[1].split("/")[-1], validators_run):
                errors.append(f"validator failed: {' '.join(cmd)}")
    after = counts()
    # Strict gates.
    coord = load(E / "coordination-status.json") or {}
    demand = load(E / "rule-demand.json") or {}
    gated = [r for r in demand.get("rows", []) if r.get("status") in {"owner-decision", "intentionally-open"}]
    if not all(r.get("validation", {}).get("do_not_promote") is True for r in gated):
        errors.append("gated row lost do_not_promote")
    if (E / "engine-resolved").exists():
        errors.append("export/engine-resolved exists")
    if coord.get("counts", {}).get("unexplainedUnavailable") != 0:
        errors.append("unexplained UNAVAILABLE remains")
    record = {
        "schema": "bota.coordination-auto-refresh/v1",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "readOnlyPeers": ["/workspace/hy3d", "/workspace/wscheppity", "/workspace/extra", "/workspace/oscraft", "/workspace/gmweb", "/workspace/bitvoice"],
        "bounded": {"defaultMinutes": ARGS.minutes, "pollSeconds": ARGS.poll_seconds, "once": ARGS.once},
        "peerManifestHashes": before_hashes,
        "peerChanged": changed,
        "rebuilt": bool(changed or not prev),
        "before": before,
        "after": after,
        "validatorsRun": validators_run,
        "gatedRows": len(gated),
        "doNotPromote": True,
        "engineResolvedExists": (E / "engine-resolved").exists(),
        "errors": errors,
        "ok": not errors,
    }
    # Write the record with an explicit zero self-hash, then keep that byte-stable
    # while refreshing export hashes, engine provenance and status.
    record["validatorsRun"] = validators_run
    record["ok"] = not errors
    record["recordSha256"] = "0" * 64
    RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if run(["python3", "tools/build-engine-data.py"], "build-engine-data-record", validators_run):
        errors.append("record engine rebuild failed")
    if run(["python3", "tools/refresh-export-hashes.py"], "refresh-export-hashes-record", validators_run):
        errors.append("record hash refresh failed")
    record["validatorsRun"] = validators_run
    record["ok"] = not errors
    record["recordSha256"] = hashlib.sha256(RECORD.read_bytes()).hexdigest()
    print(f"AUTO_REFRESH once={str(ARGS.once).lower()} changed={changed} rebuilt={record['rebuilt']} ok={record['ok']} validators={len(validators_run)}")
    print(f"BEFORE coordination={before['coordination'].get('rows')} gaps={before['spawnGapRows']} extra={before['extraGapRows']}")
    print(f"AFTER coordination={after['coordination'].get('rows')} gaps={after['spawnGapRows']} extra={after['extraGapRows']}")
    return record, 0 if record["ok"] else 1


parser = argparse.ArgumentParser(description="Bounded BOTA coordination auto-refresh")
parser.add_argument("--once", action="store_true")
parser.add_argument("--minutes", type=float, default=10)
parser.add_argument("--poll-seconds", type=float, default=10)
ARGS = parser.parse_args()


def main() -> int:
    deadline = time.monotonic() + max(0.0, ARGS.minutes) * 60
    code = 0
    while True:
        _, code = pass_once()
        if ARGS.once:
            return code
        if time.monotonic() >= deadline:
            return code
        time.sleep(max(0.1, ARGS.poll_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
