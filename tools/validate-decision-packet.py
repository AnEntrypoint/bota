#!/usr/bin/env python3
"""Validate the owner-facing decision packet and canonical engine null gates."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
ENGINE = EXPORT / "engine"
errors: list[str] = []
checks = 0
leaks = 0


def ok() -> None:
    global checks
    checks += 1


def err(message: str) -> None:
    errors.append(message)


def load(path: Path, label: str):
    try:
        data = json.loads(path.read_text())
        ok()
        return data
    except Exception as exc:
        err(f"{label}: parse/read failed: {exc}")
        return None


packet = load(EXPORT / "decision-packet.json", "decision-packet.json")
index = load(EXPORT / "field-index.json", "field-index.json")
decisions = load(EXPORT / "decisions.json", "decisions.json")
md_text = (EXPORT / "DECISION-PACKET.md").read_text()
engine = {p.name: load(p, f"engine/{p.name}") for p in sorted(ENGINE.glob("*.json"))}
decision_ids = {d["id"] for d in (decisions or {}).get("decisions", [])}
packet_ids = [d["id"] for d in (packet or {}).get("decisions", [])]

# Packet covers all 12 decisions.
if len(packet_ids) == 12 and set(packet_ids) == decision_ids:
    ok()
else:
    err(f"packet decision ids differ: packet={packet_ids} decisions={sorted(decision_ids)}")

# Exact field coverage: every engine gate appears once in the field index and in packet totals.
engine_gates = []
def collect(node, path, filename):
    global leaks
    if isinstance(node, dict):
        if "value" in node and "decisionId" in node:
            gate = f"{filename}#{'.'.join(path)}"
            engine_gates.append((gate, node))
            if node.get("value") is not None or node.get("do_not_promote") is not True:
                leaks += 1
        for k, v in node.items():
            collect(v, path + [k], filename)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            collect(v, path + [str(i)], filename)
for name, data in engine.items():
    if data:
        collect(data, [], f"export/engine/{name}")
index_ids = [f"{f['engine_file']}#{f['field_path']}" for f in (index or {}).get("fields", [])]
engine_ids = [x[0] for x in engine_gates]
if sorted(index_ids) == sorted(engine_ids) and len(index_ids) == len(set(index_ids)) == 425:
    ok()
else:
    err(f"field index coverage mismatch: index={len(index_ids)} unique={len(set(index_ids))} engine={len(engine_ids)}")
if sum(d["engine_gated_fields"] for d in (packet or {}).get("decisions", [])) == 425:
    ok()
else:
    err("packet decision gated-field totals do not sum to 425")

# Every field path resolves in engine JSON and points to a null gate.
def resolve(fp: str):
    if "#" not in fp:
        return None
    rel, dotted = fp.split("#", 1)
    name = Path(rel).name
    obj = engine.get(name)
    for part in dotted.split("."):
        if isinstance(obj, dict) and part in obj:
            obj = obj[part]
        elif isinstance(obj, list) and part.isdigit() and int(part) < len(obj):
            obj = obj[int(part)]
        else:
            return None
    return obj
for f in (index or {}).get("fields", []):
    obj = resolve(f"{f['engine_file']}#{f['field_path']}")
    if not isinstance(obj, dict) or obj.get("value") is not None or obj.get("do_not_promote") is not True or obj.get("decisionId") != f["decision_id"]:
        err(f"field does not resolve to a null gate: {f['engine_file']}#{f['field_path']}")
    else:
        ok()

# Every decision id exists; do_not_promote is true in packet.
for d in (packet or {}).get("decisions", []):
    if d["id"] in decision_ids and d["do_not_promote"] is True and d["current_state"] == "null" and d["recommendation_applied_by_default"] is False:
        ok()
    else:
        err(f"packet decision invalid: {d.get('id')}")

# Markdown count matches machine packet.
m = re.search(r"Coverage: \*\*(\d+) / (\d+)\*\* engine-gated fields across \*\*(\d+)\*\* decisions. Leaks: \*\*(\d+)\*\*", md_text)
expected_md = (425, 425, 12, 0)
if m and tuple(int(x) for x in m.groups()) == expected_md:
    ok()
else:
    err("DECISION-PACKET.md coverage/count text does not match packet")

# Dry-run apply on one decision must produce a valid plan and write nothing.
before = {p.name: p.read_bytes() for p in EXPORT.rglob("*") if p.is_file()}
proc = subprocess.run(
    [sys.executable, "tools/apply-decision.py", "--decision-id", "sigma_value_tiers", "--option", '"Use the plan tier table as implementation defaults, still labelled UNVERIFIED pending playable build"', "--dry-run"],
    cwd=ROOT, text=True, capture_output=True,
)
if proc.returncode == 0 and "APPLY_PLAN: DRY-RUN" in proc.stdout and "CANONICAL_ENGINE_UNCHANGED=true" in proc.stdout:
    ok()
else:
    err(f"apply --dry-run failed code={proc.returncode} stdout={proc.stdout[:200]} stderr={proc.stderr[:200]}")
after = {p.name: p.read_bytes() for p in EXPORT.rglob("*") if p.is_file()}
if before == after:
    ok()
else:
    err("apply --dry-run changed files")
dry_run_output = proc.stdout.strip().splitlines()

# No resolved value leaked into canonical engine files.
if leaks == 0 and not (EXPORT / "engine-resolved").exists():
    ok()
else:
    err(f"canonical leaks={leaks}; engine-resolved exists={(EXPORT / 'engine-resolved').exists()}")

# Identifier hygiene.
for d in (packet or {}).get("decisions", []):
    for a in d.get("affected_hero_acronyms", []):
        if not re.match(r"^[a-z]{3}$", a):
            err(f"bad affected hero acronym {a}")
ok()

print("DRY_RUN_EXAMPLE:")
for line in dry_run_output[:8]:
    print(line)
print(f"coverage={len(engine_ids)}/{len(index_ids)} leaks={leaks}")
if errors:
    for e in errors:
        print(f"error: {e}")
    print(f"DECISION PACKET: FAIL ({checks} checks, {len(errors)} errors)")
    sys.exit(1)
print(f"DECISION PACKET: PASS ({checks} checks, 0 errors)")
