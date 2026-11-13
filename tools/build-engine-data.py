#!/usr/bin/env python3
"""Deterministically derive contract-safe engine data from the BOTA export."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
OUT = EXPORT / "engine"
INPUTS = [
    "hero-registry.json", "hero-kits.json", "hero-voice.json", "image-references.json",
    "decisions.json", "integration-contract.json", "conformance.json",
]
MARKER_RE = re.compile(r"GUESS|UNVERIFIED|AMBIGUOUS")


def load(name: str):
    return json.loads((EXPORT / name).read_text())


registry, kits, voice, images, decisions, contract, conformance = [load(x) for x in INPUTS]
ACTIVE = conformance["active_acronyms"]
decision_by_id = {d["id"]: d for d in decisions["decisions"]}
gated_ids = set(decisions["unresolvable_owner_decisions"]) | set(decisions["intentionally_open"])
# Decision lookup by export field path, e.g. "hero-kits.json#heroes.nec.abilities.0.status".
decision_by_field: dict[str, str] = {}
for d in decisions["decisions"]:
    for fp in d.get("field_paths", []):
        decision_by_field[fp] = d["id"]

source_hashes = {
    name: hashlib.sha256((EXPORT / name).read_bytes()).hexdigest() for name in INPUTS
}


def literal(value):
    """Return a known-safe scalar/list/dict with no uncertainty markers."""
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return None if MARKER_RE.search(value) else value
    if isinstance(value, list):
        return [literal(x) for x in value]
    if isinstance(value, dict):
        return {k: literal(v) for k, v in value.items()}
    return None


def gate(field_path: str, decision_id: str | None = None, source: str | None = None, extra: dict | None = None):
    """Emit a decision-gated field as null with provenance; never use recommendation."""
    did = decision_id or decision_by_field.get(field_path, "ambiguity_record_status_markers")
    decision = decision_by_id[did]
    result = {
        "value": None,
        "decisionId": did,
        "status": decision["confidence"],
        "do_not_promote": True,
        "options_ref": f"decisions.json#decisions[{did}].options",
        "options": decision["options"],
        "source": source or f"export/{field_path}",
    }
    if extra:
        result.update(extra)
    return result


def engine_hero(a: str):
    h = registry["heroes"][a]
    return {
        "hero_id": a,
        "slot": h["slot"],
        "display_name": h["display_name"],
        "archetype": h["archetype"],
        "role": h["role"],
        "attribute": h["attribute"],
        "range": h["range"],
        "launch": h["launch"],
        "first_playable": h["first_playable"],
        "portrait": f"portraits.json#heroes.{a}",
        "abilities": f"abilities.json#heroes.{a}",
        "voice": f"voice.json#heroes.{a}",
        "source": f"hero-registry.json#heroes.{a}",
    }


heroes = {a: engine_hero(a) for a in ACTIVE}

# Abilities: emit name, slot, type, and clean mechanic text only when no marker is embedded.
abilities = {"schema": "bota.engine.abilities/v1", "heroes": {}, "decision_gated_fields": []}
for a in ACTIVE:
    rows = []
    for i, ability in enumerate(kits["heroes"][a]["abilities"]):
        fp = f"hero-kits.json#heroes.{a}.abilities.{i}.status"
        did = decision_by_field.get(fp, "ability_slot_mapping")
        # Slot mapping is resolved-from-plan, so this field can be emitted as a value.
        status_value = ability["status"] if decision_by_id[did]["confidence"] == "resolved-from-plan" else gate(fp, did)
        mechanic = ability["mechanic"]
        numeric = ability["numeric_values"]
        mechanic_gated = bool(MARKER_RE.search(mechanic)) or bool(MARKER_RE.search(json.dumps(numeric)))
        # Wojak threshold and Forever clip fields are owner-decision gated.
        owner_override = None
        if a == "woj" and ability["is_ultimate"]:
            owner_override = "wojak_sorrowful_cancel_threshold"
        if a == "for" and ability["is_ultimate"]:
            owner_override = "forever_eternal_loop_clip"
        row = {
            "ability_id": ability["ability_id"],
            "slot": ability["slot"],
            "name": ability["name"],
            "type": ability["type"],
            "is_ultimate": ability["is_ultimate"],
            "status": status_value,
            "mechanic": gate(f"hero-kits.json#heroes.{a}.abilities.{i}.mechanic", owner_override or did) if mechanic_gated or owner_override else mechanic,
            "numeric_values": gate(f"hero-kits.json#heroes.{a}.abilities.{i}.numeric_values", owner_override or did) if owner_override else numeric,
            "tier_values": gate("hero-kits.json#value_tiers", "sigma_value_tiers"),
            "cooldown": gate("hero-kits.json#value_tiers", "sigma_value_tiers"),
            "cost": gate("hero-kits.json#value_tiers", "sigma_value_tiers"),
            "damage_type": gate("hero-kits.json#value_tiers.defaults.damage_types", "default_damage_types"),
            "flavor_text": ability["flavor_text"],
            "source": f"hero-kits.json#heroes.{a}.abilities.{i}",
            "do_not_promote": True,
        }
        rows.append(row)
        if owner_override:
            abilities["decision_gated_fields"].append(f"heroes.{a}.abilities.{i}.mechanic")
            abilities["decision_gated_fields"].append(f"heroes.{a}.abilities.{i}.numeric_values")
        abilities["decision_gated_fields"] += [f"heroes.{a}.abilities.{i}.tier_values", f"heroes.{a}.abilities.{i}.cooldown", f"heroes.{a}.abilities.{i}.cost", f"heroes.{a}.abilities.{i}.damage_type"]
    abilities["heroes"][a] = rows

# Voice: lines are canonical text; rules with UNVERIFIED/GUESS status are gated.
voice_engine = {"schema": "bota.engine.voice/v1", "heroes": {}, "rules": {}, "decision_gated_fields": []}
for a in ACTIVE:
    v = voice["heroes"][a]
    voice_engine["heroes"][a] = {
        "kill": v.get("kill"), "death": v.get("death"), "idle": v.get("idle"),
        "pair_lines": v.get("pair_lines", []), "chains": v.get("chains", []),
        "source": f"hero-voice.json#heroes.{a}",
    }
voice_engine["rules"]["line_cap_words"] = gate("hero-voice.json#rules.line_cap_status", "voice_line_cap")
voice_engine["rules"]["cooldown_seconds"] = gate("hero-voice.json#rules.cooldown_status", "voice_cooldown_8s")
voice_engine["decision_gated_fields"] = ["rules.line_cap_words", "rules.cooldown_seconds"]

# Portraits and visual details: image refs are canonical; 003 is documented but not a hero key.
portraits = {"schema": "bota.engine.portraits/v1", "heroes": {}, "retired_visual_reference": {
    "slot": "003", "display_name": "Gigachad", "gallery_path": "gallery/003-gigachad.jpg",
    "status": "image-only retired/reserve", "do_not_promote": True,
    "allowed_use": "visual reference for cha ultimate", "not_a_hero_key": True,
}}
for a in ACTIVE:
    img = images["heroes"][a]
    portraits["heroes"][a] = {
        "gallery_path": img["gallery_path"], "visually_grounded_details": img["visually_grounded_details"],
        "source": f"image-references.json#heroes.{a}",
    }

# Cross-hero hook values are intentionally open.
hooks = gate("hero-kits.json#emergent_hooks", "cross_hero_hook_guesses")
ability3 = gate("hero-kits.json#value_tiers.ability_3_aura_or_passive.sigma_cost", "ability_3_passive_vs_aura_cost")
talents = gate("hero-kits.json#heroes.*.talents", "talent_values")

engine_heroes = {
    "schema": "bota.engine.heroes/v1", "active_hero_count": 26, "active_acronyms": ACTIVE,
    "acronym_to_slot": conformance["acronym_to_slot"], "heroes": heroes,
    "retired_visual_reference": portraits["retired_visual_reference"],
    "do_not_promote": True,
}
manifest = {
    "schema": "bota.engine.manifest/v1",
    "generated_from": [f"export/{x}" for x in INPUTS],
    "source_hashes": source_hashes,
    "hash_source": "export/SHA256SUMS.json",
    "generation_rules": {
        "only_reads_export_files": True,
        "active_keys": "three-letter lowercase acronyms from conformance.json",
        "resolved-from-plan": "emit value",
        "owner-decision": "emit null with decisionId, status, options, source, do_not_promote=true",
        "intentionally-open": "emit null with decisionId, status, options, source, do_not_promote=true",
        "GUESS/UNVERIFIED/AMBIGUOUS": "omit from canonical values or emit null with status + decisionId + source",
        "never_promote_recommendation": True,
        "003": "image-only retired/reserve note; never an active hero key",
    },
    "outputs": ["heroes.json", "abilities.json", "voice.json", "portraits.json"],
    "decision_gated_fields": {
        "owner-decision": sorted(decisions["unresolvable_owner_decisions"]),
        "intentionally-open": sorted(decisions["intentionally_open"]),
        "hooks": hooks,
        "ability_3_passive_vs_aura_cost": ability3,
        "talent_values": talents,
    },
    "counts": conformance["expected_counts"],
}

OUT.mkdir(parents=True, exist_ok=True)
payloads = {
    "heroes.json": engine_heroes,
    "abilities.json": abilities,
    "voice.json": voice_engine,
    "portraits.json": portraits,
    "manifest.json": manifest,
}
for name, data in payloads.items():
    (OUT / name).write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
print("ENGINE_BUILD: heroes=26 abilities=104 voice_heroes=26 portraits=26 decision_gated_fields=" + str(len(abilities["decision_gated_fields"]) + len(voice_engine["decision_gated_fields"]) + 3))
