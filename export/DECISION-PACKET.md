# BOTA decision packet

This is an owner-facing view of the generated engine data. It does **not** apply recommendations. `export/engine/` remains canonical and decision-gated; every affected field is currently `null` with `do_not_promote: true`.

Coverage: **425 / 425** engine-gated fields across **12** decisions. Leaks: **0**.

Applying a choice requires `tools/apply-decision.py --decision-id ID --option VALUE --confirm-owner-decision` (plus `--confirm-intentionally-open` where applicable). `--dry-run` is the default and writes nothing. Non-dry applies write only to `export/engine-resolved/`.

| Decision | Category | Confidence | Gated fields | Affected | Source |
|---|---|---:|---:|---|---|
| `ability_3_passive_vs_aura_cost` | balance value | intentionally-open | 1 | 26 heroes | plan/09-launch-hero-kits.md:18, plan/26-first-playable-cut-list-and-checks.md:32 |
| `ability_slot_mapping` | slot mapping | resolved-from-plan | 0 | 26 heroes | plan/09-launch-hero-kits.md:4, plan/19-balance-and-qa.md:87 … |
| `ambiguity_record_status_markers` | other | resolved-from-plan | 0 | 26 heroes | plan/20-open-questions-sources-and-decisions.md:16, plan/20-open-questions-sources-and-decisions.md:63 |
| `cross_hero_hook_guesses` | other | intentionally-open | 1 | 26 heroes | plan/09-launch-hero-kits.md:6, plan/09-launch-hero-kits.md:27 … |
| `default_damage_types` | damage type | owner-decision | 104 | 26 heroes | plan/09-launch-hero-kits.md:26, plan/20-open-questions-sources-and-decisions.md:16 |
| `engine_hero_id_language` | engine id | resolved-from-plan | 0 | 26 heroes | plan/00-index.md:42, plan/25-engine-data-plan.md:54 … |
| `forever_eternal_loop_clip` | threshold | owner-decision | 2 | 1 heroes | plan/10-remaining-hero-kits.md:27, plan/24-power-tier-draft.md:36 … |
| `sigma_value_tiers` | balance value | owner-decision | 312 | 26 heroes | plan/09-launch-hero-kits.md:12, plan/09-launch-hero-kits.md:16 … |
| `talent_values` | talent | resolved-from-plan | 1 | 26 heroes | plan/21-systems-added-back.md:5, plan/21-systems-added-back.md:9 … |
| `voice_cooldown_8s` | voice cap | owner-decision | 1 | 26 heroes | plan/23-voice-and-banter.md:10, plan/20-open-questions-sources-and-decisions.md:16 |
| `voice_line_cap` | voice cap | resolved-from-plan | 1 | 26 heroes | plan/23-voice-and-banter.md:8 |
| `wojak_sorrowful_cancel_threshold` | threshold | owner-decision | 2 | 1 heroes | plan/10-remaining-hero-kits.md:26, plan/24-power-tier-draft.md:35 |

## Options (not applied)

Full field paths are in `export/field-index.json` and `export/field-index.tsv`; the packet intentionally avoids a 425-row dump.

### `ability_3_passive_vs_aura_cost`

Confidence: **intentionally-open** · Gated fields: **1** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Emit both branches: 0 Sigma when passive, 50 Sigma when aura
- Classify every Ability 3 as passive
- Classify every Ability 3 as aura

Recorded recommendation (not applied): Emit both branches and require per-ability classification before runtime generation.

### `ability_slot_mapping`

Confidence: **resolved-from-plan** · Gated fields: **0** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Keep the four-slot map and Brainrot names as theme-only GUESS values
- Re-map slots using section 24 numbering
- Re-map slots after a playable build and C8 rename regression

Recorded recommendation (not applied): Keep the four-slot map and Brainrot names as theme-only GUESS values for the export; do not change numbers or effects.

### `ambiguity_record_status_markers`

Confidence: **resolved-from-plan** · Gated fields: **0** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Keep ambiguity records as provenance and cover them with this decision layer
- Delete ambiguity records
- Promote all ambiguity records to final values

Recorded recommendation (not applied): Keep ambiguity records as provenance and cover them with this decision layer.

### `cross_hero_hook_guesses`

Confidence: **intentionally-open** · Gated fields: **1** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Keep hooks as GUESS flavor/spec notes outside first-playable mechanics
- Implement every hook now with shared counters
- Cut all hooks

Recorded recommendation (not applied): Keep hooks as GUESS flavor/spec notes outside first-playable mechanics until shared-counter support is chosen.

### `default_damage_types`

Confidence: **owner-decision** · Gated fields: **104** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Use defaults: Ability 1 physical, Ability 2 magical, Ability 3 pure, while allowing row overrides
- Leave damage type unset
- Set every ability to one type

Recorded recommendation (not applied): Use the plan defaults and allow row overrides; keep UNVERIFIED status.

### `engine_hero_id_language`

Confidence: **resolved-from-plan** · Gated fields: **0** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Use lowercase three-letter acronyms as engine IDs, with slot as separate data
- Use contiguous 001..032 IDs
- Use slots with gaps as IDs

Recorded recommendation (not applied): Use lowercase three-letter acronyms as engine IDs, with slot as separate data.

### `forever_eternal_loop_clip`

Confidence: **owner-decision** · Gated fields: **2** · Current: **null** · `do_not_promote: true`

Affected heroes: `for`

Supported options:
- Keep three-stun clip as provisional, capped by plan/24 test at <=3 s
- Leave clip unbounded until owner decision
- Owner picks a different clip length

Recorded recommendation (not applied): Keep the three-stun clip as a provisional bound and enforce plan/24’s longest-stun <=3 s test.

### `sigma_value_tiers`

Confidence: **owner-decision** · Gated fields: **312** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Use the plan tier table as implementation defaults, still labelled UNVERIFIED pending playable build
- Wait for balance pass before emitting numeric defaults
- Use engine values from another repo

Recorded recommendation (not applied): Use the plan tier table as implementation defaults, still labelled UNVERIFIED pending playable build.

### `talent_values`

Confidence: **resolved-from-plan** · Gated fields: **1** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Keep named talent choices but cut talent values from first-playable data
- Owner approves full talent numbers now
- Generate family-template talent numbers

Recorded recommendation (not applied): Keep named talent choices, cut talent values from first-playable data, and add full sets only after base kits are tested.

### `voice_cooldown_8s`

Confidence: **owner-decision** · Gated fields: **1** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Use 8 s as provisional cooldown
- Owner chooses another cooldown
- Disable per-line cooldown

Recorded recommendation (not applied): Use 8 s as a provisional runtime cooldown and keep the balance-pass note.

### `voice_line_cap`

Confidence: **resolved-from-plan** · Gated fields: **1** · Current: **null** · `do_not_promote: true`

Affected heroes: `blo, boo, bot, cha, col, coo, din, ecc, fin, for, ghi, gon, got, gre, how, kar, lan, nec, nos, npc, san, sho, spu, tra, wil, woj`

Supported options:
- Enforce under twelve words
- Owner chooses a different cap
- Leave uncapped

Recorded recommendation (not applied): Enforce under twelve words as a validation rule.

### `wojak_sorrowful_cancel_threshold`

Confidence: **owner-decision** · Gated fields: **2** · Current: **null** · `do_not_promote: true`

Affected heroes: `woj`

Supported options:
- Keep below 25% health as provisional threshold
- Set threshold after playtest
- Use a different threshold chosen by owner

Recorded recommendation (not applied): Keep below 25% health as a provisional implementation threshold, labelled UNVERIFIED.
