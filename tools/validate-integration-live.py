#!/usr/bin/env python3
"""Read-only live cross-project conformance check for BOTA export and oscraft.

Two identifier contracts are supported:

* ``acronym``: historical BOTA export and oscraft keys are three-letter acronyms.
* ``bota-fullname``: oscraft BOTA artifacts use full BOTA character slugs while
  default-Dota hero IDs are represented by acronym-shaped legacy IDs.

The validator never writes to oscraft. Missing downstream files are UNAVAILABLE;
present files with the wrong identifier family or content are DRIFT.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path

BOTA = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description="Read-only live BOTA/oscraft conformance check")
parser.add_argument("--oscraft-root", default="/workspace/oscraft", help="Override downstream oscraft root for isolated test workspaces")
parser.add_argument("--identifier-mode", choices=["acronym", "bota-fullname"], default="acronym",
                    help="Downstream identifier contract: historical acronym or new full BOTA slug")
parser.add_argument("--default-dota-acronyms", action="store_true",
                    help="Expect default-Dota legacy hero IDs to be three-letter acronyms (required for bota-fullname)")
ARGS, _ = parser.parse_known_args()
OSCRAFT = Path(ARGS.oscraft_root)
OS = OSCRAFT / "scenarios" / "bota"
EXPORT = BOTA / "export"
MODE = ARGS.identifier_mode
FORBIDDEN = {"gigachad", "wanderer", "raker", "seeder", "wartrucker", "bouncer"}
OLD_SLUG_RE = re.compile(r"^\d{3}-")
ACRONYM_RE = re.compile(r"^[a-z]{3}$")
FULLNAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
errors: list[str] = []
drift: list[str] = []
unavailable: list[str] = []
checks = 0


def ok(_message: str = "") -> None:
    global checks
    checks += 1


def fail(kind: str, message: str) -> None:
    (unavailable if kind == "UNAVAILABLE" else drift).append(message)


def read_json(path: Path, label: str):
    try:
        data = json.loads(path.read_text())
        ok(f"{label} parsed")
        return data
    except FileNotFoundError:
        fail("UNAVAILABLE", f"{label}: missing {path}")
    except PermissionError:
        fail("UNAVAILABLE", f"{label}: permission denied {path}")
    except json.JSONDecodeError as exc:
        fail("DRIFT", f"{label}: invalid JSON {path}:{exc.lineno}:{exc.colno} ({exc.msg})")
    except OSError as exc:
        fail("UNAVAILABLE", f"{label}: unreadable {path}: {exc}")
    return None


def read_text(path: Path, label: str):
    try:
        text = path.read_text()
        ok(f"{label} read")
        return text
    except FileNotFoundError:
        fail("UNAVAILABLE", f"{label}: missing {path}")
    except PermissionError:
        fail("UNAVAILABLE", f"{label}: permission denied {path}")
    except OSError as exc:
        fail("UNAVAILABLE", f"{label}: unreadable {path}: {exc}")
    except UnicodeDecodeError as exc:
        fail("DRIFT", f"{label}: non-UTF8 {path}: {exc}")
    return None


# BOTA side: canonical export conformance fixture.
fixture = read_json(EXPORT / "conformance.json", "bota conformance.json")
registry = read_json(EXPORT / "hero-registry.json", "bota hero-registry.json")
kits = read_json(EXPORT / "hero-kits.json", "bota hero-kits.json")
voice = read_json(EXPORT / "hero-voice.json", "bota hero-voice.json")
images = read_json(EXPORT / "image-references.json", "bota image-references.json")
acronyms = list((fixture or {}).get("active_acronyms", []))
slot_map = dict((fixture or {}).get("acronym_to_slot", {}))
hero_entries = (registry or {}).get("heroes", {})
fullnames = [str(hero_entries.get(a, {}).get("display_name", a)).lower().replace(" ", "-").replace("-", "_") for a in acronyms]
# hy3d/oscraft use full slugs with underscores for multiword names.
fullnames = [x.replace("finger-dan", "finger_dan").replace("bot-bernard", "bot_bernard") for x in fullnames]
fullname_by_acronym = dict(zip(acronyms, fullnames))
acronym_by_fullname = {v: k for k, v in fullname_by_acronym.items()}
expected = acronyms if MODE == "acronym" else fullnames
key_re = ACRONYM_RE if MODE == "acronym" else FULLNAME_RE

if len(acronyms) != 26 or any(not ACRONYM_RE.match(x) for x in acronyms):
    fail("DRIFT", f"bota fixture does not contain 26 lowercase acronym keys: {acronyms}")
else:
    ok("bota fixture has 26 acronym keys")
if len(set(fullnames)) != 26 or any(not FULLNAME_RE.match(x) for x in fullnames):
    fail("DRIFT", f"bota fullname derivation is not 26 clean slugs: {fullnames}")
else:
    ok("bota fullname derivation has 26 clean slugs")
if registry and list((registry or {}).get("acronym_order", [])) != acronyms:
    fail("DRIFT", "bota registry order differs from conformance fixture")
else:
    ok("bota registry order matches fixture")
for label, obj in [("registry", registry), ("kit", kits), ("voice", voice), ("image", images)]:
    if obj:
        missing = sorted(set(acronyms) - set(obj.get("heroes", {})))
        extra = sorted(set(obj.get("heroes", {})) - set(acronyms))
        if missing or extra:
            fail("DRIFT", f"bota {label} hero drift missing={missing} extra={extra}")
        else:
            ok(f"bota {label} has exactly 26 canonical acronym entries")

# ROSTER.md slot order and the 003 image-only discrepancy.
roster_text = read_text(BOTA / "ROSTER.md", "bota ROSTER.md")
if roster_text:
    slots = re.findall(r"^\| (\d{3}) \|", roster_text, re.M)
    expected_slots = [slot_map[a] for a in acronyms]
    if slots != expected_slots:
        fail("DRIFT", f"bota ROSTER.md slot order differs: live={slots} expected={expected_slots}")
    else:
        ok("bota ROSTER.md slot order matches fixture")
    if registry:
        discrepancy = (registry or {}).get("authority", {}).get("discrepancy", {})
        if discrepancy.get("slot") == "003" and discrepancy.get("display_name") == "Gigachad" and discrepancy.get("status") == "image-only retired/reserve":
            ok("bota registry documents 003 image-only reserve")
        else:
            fail("DRIFT", "bota registry does not document 003 image-only retired/reserve discrepancy")
gallery_files = sorted((BOTA / "gallery").glob("*.jpg"))
if len(gallery_files) != 27:
    fail("DRIFT", f"bota gallery image count is {len(gallery_files)}, expected 27")
else:
    ok("bota gallery has 27 JPGs")

# oscraft UI: active hero keys must match the selected downstream identifier family.
ui = read_json(OS / "bota_ui.json", "oscraft bota_ui.json")
ui_keys: set[str] = set()
ui_acronyms: set[str] = set()
if ui:
    heroes = ui.get("heroes")
    acronyms_obj = ui.get("heroAcronyms")
    if isinstance(heroes, dict):
        ui_keys = set(heroes)
    else:
        fail("DRIFT", f"oscraft bota_ui.json heroes is {type(heroes).__name__}, expected object at {OS / 'bota_ui.json'}")
    if isinstance(acronyms_obj, dict):
        ui_acronyms = set(acronyms_obj)
    else:
        fail("DRIFT", f"oscraft bota_ui.json heroAcronyms is {type(acronyms_obj).__name__}, expected object at {OS / 'bota_ui.json'}")
    for side_name, side in [("heroes", ui_keys), ("heroAcronyms", ui_acronyms)]:
        if side != set(expected):
            fail("DRIFT", f"oscraft {OS / 'bota_ui.json'} {side_name} in {MODE} mode diff missing={sorted(set(expected)-side)} extra={sorted(side-set(expected))}")
        else:
            ok(f"oscraft bota_ui.json {side_name} matches 26 {MODE} keys")
    print(f"UI_KEY_DIFF={sorted(set(expected)^ui_keys)}")
else:
    print("UI_KEY_DIFF=UNAVAILABLE")

# oscraft generated Lua roster keys, if present. Both quoted and bare keys are accepted.
roster_lua = read_text(OS / "bota_roster.lua", "oscraft bota_roster.lua")
if roster_lua:
    lua_keys = re.findall(r'^\s*\[\s*"([A-Za-z0-9_]+)"\s*\]\s*=\s*\{', roster_lua, re.M)
    if not lua_keys:
        lua_keys = re.findall(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{", roster_lua, re.M)
    if sorted(lua_keys) != sorted(expected):
        fail("DRIFT", f"oscraft {OS / 'bota_roster.lua'} keys in {MODE} mode diff missing={sorted(set(expected)-set(lua_keys))} extra={sorted(set(lua_keys)-set(expected))}")
    else:
        ok(f"oscraft bota_roster.lua has 26 {MODE} keys")

# Source mapping provenance: CHARACTERS.md and character-mapping.tsv.
chars = read_text(OS / "CHARACTERS.md", "oscraft CHARACTERS.md")
if chars:
    wanted_phrase = "Active roster: 26 acronyms" if MODE == "acronym" else "Active roster: 26 fullname slugs"
    if wanted_phrase not in chars:
        fail("DRIFT", f"oscraft {OS / 'CHARACTERS.md'} does not state '{wanted_phrase}' for {MODE} mode")
    else:
        ok(f"oscraft CHARACTERS.md states {wanted_phrase}")
mapping_path = OS / "character-mapping.tsv"
mapping_rows: list[dict] = []
try:
    with mapping_path.open(newline="") as handle:
        lines = handle.read().splitlines()
    header = [x.strip() for x in lines[0].split(",")]
    for line in lines[1:]:
        if line.strip():
            mapping_rows.append(dict(zip(header, line.split("\t"))))
    ok("oscraft character-mapping.tsv parsed")
except FileNotFoundError:
    fail("UNAVAILABLE", f"oscraft mapping missing {mapping_path}")
except PermissionError:
    fail("UNAVAILABLE", f"oscraft mapping permission denied {mapping_path}")
except OSError as exc:
    fail("UNAVAILABLE", f"oscraft mapping unreadable {mapping_path}: {exc}")
if mapping_rows:
    key_field = "acronym" if MODE == "acronym" else "active_id"
    map_by_key = {r.get(key_field): r for r in mapping_rows if r.get(key_field) in set(expected)}
    missing_map = sorted(set(expected) - set(map_by_key))
    if missing_map:
        fail("DRIFT", f"oscraft {mapping_path} missing active rows in {MODE} mode: {missing_map}")
    else:
        ok(f"oscraft character-mapping.tsv has all 26 active {MODE} rows")
    for active_key in expected:
        row = map_by_key.get(active_key, {})
        acro = active_key if MODE == "acronym" else acronym_by_fullname[active_key]
        if row.get("slot") != slot_map.get(acro):
            fail("DRIFT", f"oscraft {mapping_path} slot for {active_key}: {row.get('slot')} != {slot_map.get(acro)}")
        else:
            ok(f"oscraft mapping slot {active_key}")
        wanted_model = f"assets/models/{active_key}-skinned.glb"
        if row.get("optimized_3d_model") != wanted_model:
            fail("DRIFT", f"oscraft {mapping_path} model path for {active_key}: {row.get('optimized_3d_model')} != {wanted_model}")
        else:
            ok(f"oscraft mapping model path {active_key}")
    if ARGS.default_dota_acronyms and MODE == "bota-fullname":
        legacy_values = sorted({r.get("legacy_acronym", "") for r in mapping_rows})
        bad = [x for x in legacy_values if not ACRONYM_RE.match(x)]
        if bad:
            fail("DRIFT", f"oscraft {mapping_path} default-Dota legacy IDs are not acronyms: {bad}")
        else:
            ok("oscraft default-Dota legacy IDs are acronyms")
    elif MODE == "bota-fullname":
        ok("default-Dota acronym expectation not requested")
    elif ARGS.default_dota_acronyms:
        fail("DRIFT", f"--default-dota-acronyms is only meaningful with --identifier-mode bota-fullname at {mapping_path}")

# bota-skinned.json: exactly 26 rows, both source-static and skinned hashes.
skinned = read_json(OS / "bota-skinned.json", "oscraft bota-skinned.json")
if skinned:
    rows_obj = skinned.get("heroes")
    if not isinstance(rows_obj, dict):
        fail("DRIFT", f"oscraft {OS / 'bota-skinned.json'} heroes is {type(rows_obj).__name__}, expected object")
        rows_obj = {}
    if sorted(rows_obj) != sorted(expected):
        fail("DRIFT", f"oscraft {OS / 'bota-skinned.json'} hero diff in {MODE} mode missing={sorted(set(expected)-set(rows_obj))} extra={sorted(set(rows_obj)-set(expected))}")
    else:
        ok(f"oscraft bota-skinned.json has exactly 26 {MODE} rows")
    for active_key in expected:
        row = rows_obj.get(active_key, {})
        acro = active_key if MODE == "acronym" else acronym_by_fullname[active_key]
        for field in ["slot", "sourceStaticSha256", "skinnedSha256"]:
            value = row.get(field)
            if not value or not isinstance(value, str):
                fail("DRIFT", f"oscraft {OS / 'bota-skinned.json'} {active_key}.{field} is empty")
            else:
                ok(f"oscraft bota-skinned.json {active_key}.{field}")
        if row.get("slot") != slot_map.get(acro):
            fail("DRIFT", f"oscraft {OS / 'bota-skinned.json'} slot for {active_key}: {row.get('slot')} != {slot_map.get(acro)}")
        else:
            ok(f"oscraft bota-skinned.json slot {active_key}")

# GLB parser: glTF 2, JSON chunk, skin count, JOINTS_0/WEIGHTS_0, joint count <=64.
def inspect_glb(path: Path):
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return "UNAVAILABLE", f"missing {path}"
    except PermissionError:
        return "UNAVAILABLE", f"permission denied {path}"
    except OSError as exc:
        return "UNAVAILABLE", f"unreadable {path}: {exc}"
    try:
        if len(data) < 20:
            return "DRIFT", f"too short ({len(data)} bytes)"
        magic, version, declared = struct.unpack_from("<4sII", data, 0)
        if magic != b"glTF" or version != 2 or declared != len(data):
            return "DRIFT", f"bad header magic={magic!r} version={version} declared={declared} bytes={len(data)}"
        chunk_len, chunk_type = struct.unpack_from("<I4s", data, 12)
        if chunk_type != b"JSON" or 20 + chunk_len > len(data):
            return "DRIFT", f"bad JSON chunk type={chunk_type!r} len={chunk_len}"
        gltf = json.loads(data[20:20 + chunk_len].decode("utf-8").rstrip("\0 "))
        skins = gltf.get("skins", [])
        attrs = set()
        for mesh in gltf.get("meshes", []):
            for primitive in mesh.get("primitives", []):
                attrs.update(primitive.get("attributes", {}))
        max_joints = max((len(skin.get("joints", [])) for skin in skins), default=0)
        if len(skins) < 1:
            return "DRIFT", "skins<1"
        if "JOINTS_0" not in attrs or "WEIGHTS_0" not in attrs:
            return "DRIFT", f"missing skin attributes attrs={sorted(attrs)}"
        if max_joints > 64:
            return "DRIFT", f"joint_count={max_joints}>64"
        return "OK", {"skins": len(skins), "joint_count": max_joints, "attributes": sorted(attrs)}
    except (struct.error, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return "DRIFT", f"parse failed: {exc}"

model_ok = 0
for active_key in expected:
    path = OS / "assets" / "models" / f"{active_key}-skinned.glb"
    status, detail = inspect_glb(path)
    if status == "OK":
        model_ok += 1
        checks += 1
    elif status == "UNAVAILABLE":
        fail("UNAVAILABLE", f"oscraft model {active_key}: {detail} {path}")
    else:
        fail("DRIFT", f"oscraft model {active_key}: {detail} {path}")

# Identifier hygiene: active keys must match the selected family; reserves never become active.
all_keys = set(expected) | ui_keys | ui_acronyms | set((skinned or {}).get("heroes", {}))
bad_keys = []
for key in all_keys:
    if key.lower() in FORBIDDEN or OLD_SLUG_RE.match(key) or not key_re.match(key):
        bad_keys.append(key)
if bad_keys:
    fail("DRIFT", f"forbidden/mismatched active identifiers in {MODE} mode at {OS}: {sorted(bad_keys)}")
else:
    ok(f"no retired/reserve/old-slug active keys in {MODE} mode")

# Compact, honest reporting.
bota_count = len((registry or {}).get("heroes", {}))
os_ui_count = len(ui_keys)
os_skinned_count = len((skinned or {}).get("heroes", {}))
key_diff = sorted(set(expected) ^ ui_keys)
print(f"IDENTIFIER_MODE={MODE} DEFAULT_DOTA_ACRONYMS={'true' if ARGS.default_dota_acronyms else 'false'}")
print(f"LIVE_COUNTS: bota={bota_count} os_ui={os_ui_count} os_models={model_ok}/26 os_skinned={os_skinned_count} gallery={len(gallery_files)}")
print(f"CROSS_PROJECT_KEY_DIFF={key_diff}")
print(f"MODEL_PARSE_COUNT={model_ok}")
for item in unavailable:
    print(f"UNAVAILABLE: {item}")
for item in drift:
    print(f"DRIFT: {item}")
if unavailable or drift or errors:
    print(f"LIVE INTEGRATION: FAIL ({checks} checks, {len(unavailable)} unavailable, {len(drift)} drift)")
    sys.exit(1)
print(f"LIVE INTEGRATION: PASS ({checks} checks, 0 unavailable, 0 drift)")
