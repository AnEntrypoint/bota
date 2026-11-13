# BOTA apply guide

**No value becomes canon until the owner explicitly chooses it.** `export/engine/` stays null-gated. `tools/apply-decision.py` never overwrites canonical engine files; confirmed applies write only to `export/engine-resolved/`.

The option must be either an exact supported option string from `export/decision-packet.json` or a valid JSON literal. Arbitrary unquoted strings are refused.

## 1. Dry-run (default; writes nothing)

```bash
python3 tools/apply-decision.py \
  --decision-id sigma_value_tiers \
  --option '"Use the plan tier table as implementation defaults, still labelled UNVERIFIED pending playable build"' \
  --dry-run
```

Expected: `APPLY_PLAN: DRY-RUN`, `CANONICAL_ENGINE_UNCHANGED=true`, exit `0`.

## 2. One confirmed owner-decision apply

Only after the owner chooses a supported option:

```bash
python3 tools/apply-decision.py \
  --decision-id sigma_value_tiers \
  --option '"Use the plan tier table as implementation defaults, still labelled UNVERIFIED pending playable build"' \
  --apply --confirm-owner-decision
```

Output lands in:

```text
export/engine-resolved/sigma_value_tiers.json
export/engine-resolved/sigma_value_tiers.audit.json
```

## 3. One intentionally-open apply

This needs both confirmations:

```bash
python3 tools/apply-decision.py \
  --decision-id cross_hero_hook_guesses \
  --option '"Keep hooks as GUESS flavor/spec notes outside first-playable mechanics"' \
  --apply --confirm-owner-decision --confirm-intentionally-open
```

## 4. Inspect an overlay and its audit

```bash
cat export/engine-resolved/<decision-id>.json
cat export/engine-resolved/<decision-id>.audit.json
python3 tools/validate-apply-mechanism.py
python3 tools/validate-decision-packet.py
python3 tools/validate-engine-data.py
```

The audit record contains decision id, selected option, UTC timestamp, `decision_packet_sha256`, `decisions_json_sha256`, `engine_manifest_sha256`, affected field paths, `canonical_engine_overwritten: false`, and `do_not_promote_canonical: true`.

## 5. Revert

Deleting the overlay fully reverts the decision because canonical engine data was never touched:

```bash
rm -f export/engine-resolved/<decision-id>.json export/engine-resolved/<decision-id>.audit.json
# or remove all opt-in overlays:
rm -rf export/engine-resolved/
```

Then rerun:

```bash
python3 tools/validate-decision-packet.py
python3 tools/validate-engine-data.py
```

`engine-resolved/` is an overlay, not a merge. A later owner-approved step would be required to promote any resolved value into canon; this guide intentionally does not provide that step.
