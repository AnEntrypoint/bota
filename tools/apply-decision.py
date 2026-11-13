#!/usr/bin/env python3
"""Strictly opt-in decision application to a separate engine-resolved overlay."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
ENGINE = EXPORT / "engine"
RESOLVED = EXPORT / "engine-resolved"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply one explicit owner decision to a separate overlay")
    ap.add_argument("--decision-id", required=True)
    ap.add_argument("--option", required=True, help="Explicit chosen option value; must match a supported option string or JSON literal")
    ap.add_argument("--confirm-owner-decision", action="store_true", help="Required for any non-dry apply")
    ap.add_argument("--confirm-intentionally-open", action="store_true", help="Additionally required for intentionally-open decisions")
    ap.add_argument("--dry-run", action="store_true", help="Print the exact plan and write nothing; default when --apply is absent")
    ap.add_argument("--apply", action="store_true", help="Actually write export/engine-resolved/")
    args = ap.parse_args()

    decisions = json.loads((EXPORT / "decisions.json").read_text())
    index = json.loads((EXPORT / "field-index.json").read_text())
    packet = json.loads((EXPORT / "decision-packet.json").read_text())
    by_id = {d["id"]: d for d in decisions["decisions"]}
    if args.decision_id not in by_id:
        print(f"ERROR: unknown decision id {args.decision_id}")
        return 2
    d = by_id[args.decision_id]
    packet_d = next(x for x in packet["decisions"] if x["id"] == args.decision_id)

    # Parse option: accept an exact supported option string or a JSON literal.
    try:
        value = json.loads(args.option)
        json_literal = True
    except json.JSONDecodeError:
        value = args.option
        json_literal = False
    # Explicit owner values must be either an exact supported option or valid JSON.
    # Arbitrary unquoted strings are not options and are refused.
    supported = args.option in d["options"] or json_literal
    if not supported:
        print(f"ERROR: option is not supported by decision {args.decision_id}: {args.option}")
        return 2

    fields = [f for f in index["fields"] if f["decision_id"] == args.decision_id]
    if len(fields) != packet_d["engine_gated_fields"]:
        print(f"ERROR: field index count {len(fields)} differs from packet {packet_d['engine_gated_fields']}")
        return 2
    if not fields:
        print(f"ERROR: decision {args.decision_id} has no engine-gated fields to apply")
        return 2

    # Dry-run is the default and always safe.
    if args.dry_run or not args.apply:
        print("APPLY_PLAN: DRY-RUN (no files written)")
        print(f"DECISION_ID={args.decision_id}")
        print(f"CONFIDENCE={d['confidence']}")
        print(f"OPTION={json.dumps(value,ensure_ascii=False,sort_keys=True)}")
        print(f"AFFECTED_FIELDS={len(fields)}")
        print(f"RESOLVES_TO=export/engine-resolved/{args.decision_id}.json")
        for f in fields[:5]:
            print(f"FIELD={f['engine_file']}#{f['field_path']}: null -> {json.dumps(value,ensure_ascii=False,sort_keys=True)}")
        if len(fields) > 5:
            print(f"FIELD_INDEX=export/field-index.json ({len(fields)} exact paths)")
        print("CANONICAL_ENGINE_UNCHANGED=true")
        return 0

    # Non-dry apply requires explicit confirmations and never touches export/engine/.
    if not args.confirm_owner_decision:
        print("ERROR: non-dry apply requires --confirm-owner-decision")
        return 2
    if d["confidence"] == "intentionally-open" and not args.confirm_intentionally_open:
        print("ERROR: intentionally-open decision requires --confirm-intentionally-open")
        return 2
    if d["confidence"] == "resolved-from-plan":
        print("ERROR: resolved-from-plan decisions must stay in canonical engine data; no overlay needed")
        return 2

    source_hash = sha(EXPORT / "decision-packet.json")
    audit = {
        "schema": "bota.decision-apply-audit/v1",
        "decision_id": args.decision_id,
        "category": d["category"],
        "confidence": d["confidence"],
        "option": value,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "decision_packet_sha256": source_hash,
        "decisions_json_sha256": sha(EXPORT / "decisions.json"),
        "engine_manifest_sha256": sha(ENGINE / "manifest.json"),
        "affected_field_paths": [f"{f['engine_file']}#{f['field_path']}" for f in fields],
        "canonical_engine_overwritten": False,
        "do_not_promote_canonical": True,
    }
    RESOLVED.mkdir(parents=True, exist_ok=True)
    (RESOLVED / f"{args.decision_id}.json").write_text(json.dumps({
        "schema": "bota.engine-resolved-overlay/v1",
        "decision_id": args.decision_id,
        "option": value,
        "fields": audit["affected_field_paths"],
        "canonical_value": None,
        "resolved_value": value,
        "warning": "Owner-supplied overlay; not canonical until explicitly merged by a later owner-approved step",
    }, indent=2, sort_keys=True) + "\n")
    (RESOLVED / f"{args.decision_id}.audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(f"APPLIED_OVERLAY=export/engine-resolved/{args.decision_id}.json")
    print(f"AUDIT=export/engine-resolved/{args.decision_id}.audit.json")
    print(f"AFFECTED_FIELDS={len(fields)}")
    print("CANONICAL_ENGINE_UNCHANGED=true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
