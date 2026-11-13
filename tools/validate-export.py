#!/usr/bin/env python3
"""Validate the implementation-ready BOTA export."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
EXPECTED = ["nec", "cha", "woj", "blo", "tra", "boo", "coo", "gon", "spu", "kar", "how", "san", "lan", "fin", "wil", "nos", "din", "ecc", "bot", "sho", "npc", "for", "col", "gre", "ghi", "got"]
DECISIONS_MODE = "--decisions" in sys.argv[1:]
INTEGRATION_MODE = "--integration" in sys.argv[1:]
MARKER_RE = re.compile(r"GUESS|UNVERIFIED|AMBIGUOUS")
FORBIDDEN_KEY_NAMES = {
    "gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer",
    "boxxy", "chungus", "starwarskid", "disaster", "pepe", "doge",
}
OLD_SLUGS = [
    "001-neckbeard", "002-chad", "003-gigachad", "004-wojak",
    "005-bloomer", "006-tradwife", "007-boomer", "008-coomer",
    "009-gondola", "010-spurdo", "011-karen", "012-howard",
    "013-sanic", "014-lankdad", "015-finger-dan", "016-willie",
    "017-noscope", "018-dino", "019-ecce", "020-bot-bernard",
    "021-shoop", "022-npc", "023-forever", "024-cole", "025-grey",
    "026-ghillie", "027-gothgirl", "028-wanderer", "029-raker",
    "030-seeder", "031-wartrucker", "032-bouncer",
]
KEY_RE = re.compile(r"^[a-z]{3}$")
errors: list[str] = []
warnings: list[str] = []
checks: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        checks.append(message)
    else:
        errors.append(message)


def load_json(name: str):
    path = EXPORT / name
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        errors.append(f"{name}: JSON parse failed: {exc}")
        return None


registry = load_json("hero-registry.json")
kits = load_json("hero-kits.json")
voice = load_json("hero-voice.json")
images = load_json("image-references.json")
sums = load_json("SHA256SUMS.json")
manifest_path = ROOT / "manifest.json"
try:
    manifest = json.loads(manifest_path.read_text())
except Exception as exc:
    errors.append(f"manifest.json: JSON parse failed: {exc}")
    manifest = []

# Exact registry and acronym format.
registry_heroes = registry.get("heroes", {}) if registry else {}
keys = sorted(registry_heroes)
check(keys == sorted(EXPECTED), f"registry has exactly 26 expected keys: {','.join(keys)}")
check(all(KEY_RE.match(k) for k in keys), "all registry keys match ^[a-z]{3}$")
check(len(keys) == len(set(keys)), "registry keys are unique")
check(not any(any(bad in k for bad in FORBIDDEN_KEY_NAMES) for k in keys), "no retired/reserve name is a registry key")
for obj_name, obj, section in [("hero-kits.json", kits, "heroes"), ("hero-voice.json", voice, "heroes"), ("image-references.json", images, "heroes")]:
    if obj:
        check(sorted(obj.get(section, {})) == sorted(EXPECTED), f"{obj_name} heroes cover exactly the 26 active acronyms")
        check(all(KEY_RE.match(k) for k in obj.get(section, {})), f"{obj_name} keys are lowercase three-letter acronyms")

# Required fields and discrepancy documentation.
required_registry = ["slot", "acronym", "display_name", "archetype", "role", "attribute", "range", "launch", "first_playable", "portrait_path", "sources"]
for key, hero in registry_heroes.items():
    for field in required_registry:
        value = hero.get(field)
        if value is None or value == "" or value == {}:
            errors.append(f"registry[{key}].{field} is empty")
    if hero.get("acronym") != key:
        errors.append(f"registry[{key}].acronym does not match key")
if registry:
    auth = registry.get("authority", {})
    check(auth.get("active_count") == 26 and auth.get("gallery_image_count") == 25, "registry documents 26 historical hero keys and the 25-image public gallery")
    discrepancy = auth.get("discrepancy", {})
    check(discrepancy.get("slot") == "003" and discrepancy.get("display_name") == "Gigachad" and discrepancy.get("status") == "image-only retired/reserve", "003 gallery-only discrepancy is documented")
    check(auth.get("retired_slots") == ["028", "029", "030", "031", "032"], "028-032 retired slots are documented")

# Kit, voice and image completeness.
if kits:
    for key in EXPECTED:
        block = kits.get("heroes", {}).get(key, {})
        abilities = block.get("abilities", [])
        check(len(abilities) == 4, f"kits[{key}] has four abilities")
        check(sum(bool(a.get("is_ultimate")) for a in abilities) == 1, f"kits[{key}] has one ultimate")
        for ability in abilities:
            for field in ["ability_id", "name", "type", "mechanic", "source"]:
                if not ability.get(field):
                    errors.append(f"kits[{key}].{ability.get('slot')}.{field} is empty")
        # Talents may be empty for the first-playable slice, but present rows must be non-empty.
        for talent in block.get("talents", []):
            if not talent.get("choice"):
                errors.append(f"kits[{key}] has an empty talent choice")
if voice:
    for key in EXPECTED:
        block = voice.get("heroes", {}).get(key, {})
        lines = [block.get("kill"), block.get("death"), block.get("idle")]
        check(any(bool(x) for x in lines), f"voice[{key}] has at least one hero line")
        seen = set()
        for line in lines:
            if not line:
                continue
            if line in seen:
                warnings.append(f"voice[{key}] repeats the exact line: {line}")
            seen.add(line)
    exchange_pairs = []
    for exchange in voice.get("cross_hero_exchanges", []):
        a = exchange.get("a", {}).get("acronym")
        b = exchange.get("b", {}).get("acronym")
        check(a in EXPECTED and b in EXPECTED, f"exchange {exchange.get('id')} uses active acronyms")
        exchange_pairs.append(tuple(sorted((a, b))))
    check(len(exchange_pairs) == len(set(exchange_pairs)), "cross-hero exchanges are deduplicated by acronym pair")
if images:
    for key in EXPECTED:
        block = images.get("heroes", {}).get(key, {})
        details = block.get("visually_grounded_details", [])
        check(bool(block.get("gallery_path")) and len(details) >= 4, f"images[{key}] has a path and visible details")

# Every source reference and path exists; source line numbers are in range.
def validate_sourcemaps(node, where: str) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, int) and ("/" in k or k.endswith(".md")):
                p = ROOT / k
                if not p.exists():
                    errors.append(f"{where}: source file missing: {k}")
                else:
                    count = len(p.read_text().splitlines())
                    if not 1 <= v <= count:
                        errors.append(f"{where}: line {v} out of range in {k}")
            else:
                validate_sourcemaps(v, f"{where}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            validate_sourcemaps(v, f"{where}[{i}]")

for name, data in [("hero-registry.json", registry), ("hero-kits.json", kits), ("hero-voice.json", voice), ("image-references.json", images)]:
    if data:
        validate_sourcemaps(data.get("sources", data), name)
for key, hero in registry_heroes.items():
    portrait = ROOT / hero.get("portrait_path", "")
    check(portrait.is_file(), f"registry[{key}] portrait exists: {hero.get('portrait_path')}")
if images:
    for key, block in images.get("heroes", {}).items():
        check((ROOT / block.get("gallery_path", "")).is_file(), f"images[{key}] gallery JPG exists")
    retired = images.get("retired_image", {})
    check(retired.get("not_a_hero_key") is True and (ROOT / retired.get("path", "")).is_file(), "003 retired image exists and is not a hero key")

# TSV and YAML parse cleanly and key on acronyms only.
for name in ["heroes.tsv", "abilities.tsv", "voice.tsv", "images.tsv"]:
    path = EXPORT / name
    try:
        with path.open(newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        check(bool(rows), f"{name} parses and has rows")
        ids = sorted({r.get("hero_id", "") for r in rows})
        check(all(KEY_RE.match(x) for x in ids), f"{name} hero_id values are lowercase acronyms")
        check(all(x in EXPECTED for x in ids), f"{name} contains no retired/reserve hero_id")
        if name in {"heroes.tsv", "images.tsv"}:
            check(ids == sorted(EXPECTED), f"{name} covers exactly 26 heroes")
    except Exception as exc:
        errors.append(f"{name}: TSV parse failed: {exc}")
try:
    yaml_text = (EXPORT / "export.yaml").read_text()
    # Lightweight parser: validate scalar/list shape and required keys without a third-party dependency.
    check("schema: \"bota.export-manifest/v1\"" in yaml_text, "export.yaml has the expected schema")
    check("active_hero_count: 26" in yaml_text and "gallery_image_count: 25" in yaml_text, "export.yaml documents the 26-key historical export and 25-image gallery")
    yaml_acronyms = re.findall(r"^  - \"([a-z]{3})\"$", yaml_text, re.M)
    check(yaml_acronyms == EXPECTED, "export.yaml acronym list matches the oscraft order")
except Exception as exc:
    errors.append(f"export.yaml: parse failed: {exc}")

# SHA256 integrity.
if sums:
    for name, expected_hash in sums.items():
        path = EXPORT / name
        if not path.is_file():
            errors.append(f"SHA256SUMS references missing file {name}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        check(actual == expected_hash, f"sha256 {name} matches")

# Stale-name / old-slug identifier scan: identifiers and keys only, not creative prose.
key_blob = json.dumps({
    "registry": keys,
    "kit_keys": sorted(kits.get("heroes", {})) if kits else [],
    "voice_keys": sorted(voice.get("heroes", {})) if voice else [],
    "image_keys": sorted(images.get("heroes", {})) if images else [],
    "ability_ids": [a.get("ability_id") for h in (kits or {}).get("heroes", {}).values() for a in h.get("abilities", [])],
    "exchange_ids": [x.get("id") for x in (voice or {}).get("cross_hero_exchanges", [])],
}).lower()
for bad in FORBIDDEN_KEY_NAMES:
    check(bad not in key_blob, f"identifier scan excludes retired/legacy name {bad}")
for slug in OLD_SLUGS:
    check(slug not in key_blob, f"identifier scan excludes old slug {slug}")

# Manifest discovery.
export_section = next((s for s in manifest if s.get("title") == "Export"), None)
if export_section:
    listed = export_section.get("files", [])
    for name in ["hero-registry.json", "hero-kits.json", "hero-voice.json", "image-references.json", "heroes.tsv", "abilities.tsv", "voice.tsv", "images.tsv", "export.yaml"]:
        check(f"export/{name}" in listed, f"manifest.json discovers export/{name}")
else:
    errors.append("manifest.json has no Export section")

# Decision-resolution coverage mode.
if DECISIONS_MODE:
    decisions_path = EXPORT / "decisions.json"
    decision_errors: list[str] = []
    decision_checks = 0
    try:
        decisions_doc = json.loads(decisions_path.read_text())
    except Exception as exc:
        errors.append(f"decisions.json: JSON parse failed: {exc}")
        decisions_doc = None
    if decisions_doc:
        decisions = decisions_doc.get("decisions", [])
        ids = [d.get("id") for d in decisions]
        if len(ids) != len(set(ids)):
            decision_errors.append("duplicate decision ids")
        else:
            decision_checks += 1
        for d in decisions:
            for required in ["id", "category", "sources", "options", "recommended_default", "reason", "confidence", "field_paths", "affected_heroes"]:
                if d.get(required) in (None, "", []):
                    decision_errors.append(f"decision {d.get('id')} has empty {required}")
            if not d.get("covers") and d.get("coverage_role") != "recommendation-only":
                decision_errors.append(f"decision {d.get('id')} has empty covers without coverage_role=recommendation-only")
            if d.get("confidence") not in {"resolved-from-plan", "owner-decision", "intentionally-open"}:
                decision_errors.append(f"decision {d.get('id')} has invalid confidence")
            for hero in d.get("affected_heroes", []):
                if hero not in EXPECTED:
                    decision_errors.append(f"decision {d.get('id')} affects non-active hero {hero}")
            for source in d.get("sources", []):
                path = ROOT / source.get("file", "")
                line = source.get("line")
                if not path.is_file():
                    decision_errors.append(f"decision {d.get('id')} cites missing {source.get('file')}")
                elif not isinstance(line, int) or not 1 <= line <= len(path.read_text().splitlines()):
                    decision_errors.append(f"decision {d.get('id')} cites invalid line {source.get('file')}:{line}")
                else:
                    decision_checks += 1
            for fp in d.get("field_paths", []):
                if "#" not in fp:
                    decision_errors.append(f"decision {d.get('id')} field path lacks file separator: {fp}")
                    continue
                fname, dotted = fp.split("#", 1)
                obj = load_json(fname) if fname.endswith(".json") else None
                cur = obj
                for part in dotted.split("."):
                    if isinstance(cur, dict) and part in cur:
                        cur = cur[part]
                    elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
                        cur = cur[int(part)]
                    else:
                        cur = None
                        break
                if cur is None:
                    decision_errors.append(f"decision {d.get('id')} field path does not resolve: {fp}")
                else:
                    decision_checks += 1
        # Enumerate every marker in the four export JSONs and require exact coverage.
        marker_ids = []
        def collect_markers(node, path_parts, filename):
            if isinstance(node, dict):
                for key, value in node.items():
                    collect_markers(value, path_parts + [key], filename)
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    collect_markers(value, path_parts + [str(index)], filename)
            elif isinstance(node, str) and MARKER_RE.search(node):
                marker_ids.append(f"{filename}#{'.'.join(path_parts)}")
        for name, data in [("hero-registry.json", registry), ("hero-kits.json", kits), ("hero-voice.json", voice), ("image-references.json", images)]:
            if data is not None:
                collect_markers(data, [], f"export/{name}")
        covered = [mid for d in decisions for mid in d.get("covers", [])]
        covered_set = set(covered)
        marker_set = set(marker_ids)
        orphans = sorted(marker_set - covered_set)
        unknown_covers = sorted(covered_set - marker_set)
        duplicate_covers = sorted(m for m, count in __import__("collections").Counter(covered).items() if count > 1)
        if orphans:
            decision_errors.append(f"orphan markers: {orphans[:5]}" + (" …" if len(orphans) > 5 else ""))
        if unknown_covers:
            decision_errors.append(f"unknown covered markers: {unknown_covers[:5]}")
        if duplicate_covers:
            decision_errors.append(f"markers covered more than once: {duplicate_covers[:5]}")
        decision_checks += 1 if not orphans else 0
        print(f"DECISION_COVERAGE: {len(marker_ids)} / {len(marker_set & covered_set)} markers covered; {len(decisions)} decisions; {len(orphans)} orphans")
        for error in decision_errors:
            errors.append(f"decisions: {error}")
        print(f"DECISION_CHECKS: {decision_checks} source/path checks passed")

# Engine integration contract and conformance fixture mode.
if INTEGRATION_MODE:
    integration_errors: list[str] = []
    integration_checks = 0
    try:
        contract = json.loads((EXPORT / "integration-contract.json").read_text())
        fixture = json.loads((EXPORT / "conformance.json").read_text())
        integration_text = (EXPORT / "INTEGRATION.md").read_text()
    except Exception as exc:
        errors.append(f"integration files: parse/read failed: {exc}")
        contract = fixture = None
        integration_text = ""
    if contract and fixture:
        # Basic prose/spec checks.
        for phrase in ["Do not silently promote", "003", "acronym", "decisions.json"]:
            if phrase in integration_text:
                integration_checks += 1
            else:
                integration_errors.append(f"INTEGRATION.md missing phrase: {phrase}")
        # Live counts from parsed exports and TSVs.
        try:
            with (EXPORT / "voice.tsv").open(newline="") as handle:
                live_voice_rows = len(list(csv.DictReader(handle, delimiter="\t")))
            live_counts = {
                "active_heroes": len(EXPECTED),
                "gallery_images": len(list((ROOT / "gallery").glob("*.jpg"))),
                "active_gallery_images": len(images.get("heroes", {})) if images else 0,
                "ability_rows": sum(len((kits or {}).get("heroes", {}).get(a, {}).get("abilities", [])) for a in EXPECTED),
                "voice_rows": live_voice_rows,
                "decisions": len((json.loads((EXPORT / "decisions.json").read_text())).get("decisions", [])),
                "covered_markers": (json.loads((EXPORT / "decisions.json").read_text())).get("marker_scan", {}).get("covered"),
                "raw_markers": (json.loads((EXPORT / "decisions.json").read_text())).get("marker_scan", {}).get("markers"),
                "export_hash_files": len(sums or {}),
                "engine_files": len(list((EXPORT / "engine").glob("*.json"))),
                "decision_packet_fields": (json.loads((EXPORT / "field-index.json").read_text())).get("count"),
                "decision_packet_decisions": len((json.loads((EXPORT / "decision-packet.json").read_text())).get("decisions", [])),
            }
            for key, expected in fixture.get("expected_counts", {}).items():
                if live_counts.get(key) != expected:
                    integration_errors.append(f"count {key}: live {live_counts.get(key)} != contract {expected}")
                else:
                    integration_checks += 1
            if contract.get("counts") != fixture.get("expected_counts"):
                integration_errors.append("contract counts differ from conformance fixture")
            else:
                integration_checks += 1
        except Exception as exc:
            integration_errors.append(f"live count calculation failed: {exc}")
        # Acronym-to-slot mapping and presence paths.
        live_mapping = {a: registry_heroes.get(a, {}).get("slot") for a in EXPECTED}
        if fixture.get("acronym_to_slot") != live_mapping:
            integration_errors.append("conformance acronym_to_slot differs from registry")
        else:
            integration_checks += 1
        for a in EXPECTED:
            for surface, obj in [("registry", registry_heroes), ("kit", (kits or {}).get("heroes", {})), ("voice", (voice or {}).get("heroes", {})), ("image", (images or {}).get("heroes", {}))]:
                if a not in obj:
                    integration_errors.append(f"{surface} missing active hero {a}")
                else:
                    integration_checks += 1
        # Hash parity with SHA256SUMS.json and actual files.
        expected_hashes = fixture.get("expected_hashes") or {}
        expected_sums = {k: v for k, v in (sums or {}).items() if k != "conformance.json"}
        if expected_hashes != expected_sums:
            integration_errors.append("conformance expected_hashes differ from SHA256SUMS.json (excluding conformance self-hash)")
        else:
            integration_checks += 1
        for name, expected_hash in (fixture.get("expected_hashes") or {}).items():
            path = EXPORT / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
                integration_errors.append(f"conformance hash mismatch: {name}")
            else:
                integration_checks += 1
        # Identifier and reserve rules.
        active_keys = set(fixture.get("active_acronyms", []))
        if active_keys != set(EXPECTED):
            integration_errors.append("fixture active_acronyms differs from expected 26")
        else:
            integration_checks += 1
        forbidden = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
        if any(k.lower() in forbidden or re.match(r"^\d{3}-", str(k)) for k in active_keys):
            integration_errors.append("retired/reserve/old-slug identifier in fixture active keys")
        else:
            integration_checks += 1
        # Every owner-decision and intentionally-open id has a do_not_promote rule.
        decisions_doc = json.loads((EXPORT / "decisions.json").read_text())
        gated = set(decisions_doc.get("unresolvable_owner_decisions", [])) | set(decisions_doc.get("intentionally_open", []))
        rules = contract.get("integration_rules", [])
        for did in sorted(gated):
            matched = [r for r in rules if r.get("id", "").endswith(did) or did in r.get("rule", "")]
            if not matched or not all(r.get("do_not_promote") is True for r in matched):
                integration_errors.append(f"missing do_not_promote rule for {did}")
            else:
                integration_checks += 1
        if set(fixture.get("do_not_promote_ids", [])) != gated:
            integration_errors.append("fixture do_not_promote_ids differs from gated decisions")
        else:
            integration_checks += 1
        # Contract field paths resolve in export JSON, expanding {hero}.
        def resolve_field_path(fp: str) -> bool:
            if "#" not in fp:
                return False
            fname, dotted = fp.split("#", 1)
            obj = load_json(fname)
            for part in dotted.split("."):
                if "{hero}" in part:
                    return all(part.replace("{hero}", a) in obj for a in EXPECTED) if isinstance(obj, dict) else False
                if isinstance(obj, dict) and part in obj:
                    obj = obj[part]
                elif isinstance(obj, list) and part.isdigit() and int(part) < len(obj):
                    obj = obj[int(part)]
                else:
                    return False
            return True
        for fp in contract.get("field_semantics", {}).get("canonical", {}):
            if resolve_field_path(fp):
                integration_checks += 1
            else:
                integration_errors.append(f"contract field path does not resolve: {fp}")
        # Required files and manifest discovery.
        for rel in contract.get("authority", {}).get("required_files", []):
            if (ROOT / rel).is_file():
                integration_checks += 1
            else:
                integration_errors.append(f"required integration file missing: {rel}")
        print(f"INTEGRATION_COUNTS: heroes={live_counts.get('active_heroes')} abilities={live_counts.get('ability_rows')} voice={live_counts.get('voice_rows')} gallery={live_counts.get('gallery_images')} decisions={live_counts.get('decisions')} markers={live_counts.get('covered_markers')}/{live_counts.get('raw_markers')} hashes={live_counts.get('export_hash_files')}")
        for error in integration_errors:
            errors.append(f"integration: {error}")
        print(f"INTEGRATION_CHECKS: {integration_checks} checks passed")

for warning in warnings:
    print(f"warning: {warning}")
if errors:
    for error in errors:
        print(f"error: {error}")
    sys.exit(1)
print(f"EXPORT VALIDATION: PASS ({len(checks)} checks, {len(warnings)} warnings)")
print("ACTIVE_ACRONYMS=" + ",".join(EXPECTED))
