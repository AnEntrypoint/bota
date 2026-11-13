# Export decisions and resolutions

This is an additive decision layer. It does **not** overwrite `hero-registry.json`, `hero-kits.json`, `hero-voice.json` or `image-references.json`.
- Marker scan: **169 / 169** markers covered; **0** orphans.
- Distinct decisions: **12**.
- Owner decisions still open: default_damage_types, forever_eternal_loop_clip, sigma_value_tiers, voice_cooldown_8s, wojak_sorrowful_cancel_threshold.
- Intentionally open: ability_3_passive_vs_aura_cost, cross_hero_hook_guesses.

## Decisions

### `ability_3_passive_vs_aura_cost`

Coverage role: **recommendation-only**

Category: **balance value** · Confidence: **intentionally-open** · Covered markers: **0**

Recommendation: Emit both branches and require per-ability classification before runtime generation.

Reason: The plan explicitly gives both costs and says each kit names which, but the current rows do not label passive versus aura; guessing one for all 26 would invent data.

Sources:
- `plan/09-launch-hero-kits.md:18`
- `plan/26-first-playable-cut-list-and-checks.md:32`

Options:
- Emit both branches: 0 Sigma when passive, 50 Sigma when aura
- Classify every Ability 3 as passive
- Classify every Ability 3 as aura

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-kits.json#value_tiers.ability_3_aura_or_passive.sigma_cost, hero-kits.json#heroes.nec.abilities.2.tier_values.sigma_cost, hero-kits.json#heroes.cha.abilities.2.tier_values.sigma_cost, hero-kits.json#heroes.woj.abilities.2.tier_values.sigma_cost, hero-kits.json#heroes.blo.abilities.2.tier_values.sigma_cost, hero-kits.json#heroes.tra.abilities.2.tier_values.sigma_cost` …

### `ability_slot_mapping`

Category: **slot mapping** · Confidence: **resolved-from-plan** · Covered markers: **104**

Recommendation: Keep the four-slot map and Brainrot names as theme-only GUESS values for the export; do not change numbers or effects.

Reason: Plan/09 says ability IDs, slot order, four-ability count, effect kinds and tier numbers are kept; plan/19 says a rename never changes a number; plan/26 needs 24 ability rows for the six-hero slice.

Sources:
- `plan/09-launch-hero-kits.md:4`
- `plan/19-balance-and-qa.md:87`
- `plan/26-first-playable-cut-list-and-checks.md:32`

Options:
- Keep the four-slot map and Brainrot names as theme-only GUESS values
- Re-map slots using section 24 numbering
- Re-map slots after a playable build and C8 rename regression

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-kits.json#heroes.nec.abilities.0.status, hero-kits.json#heroes.nec.abilities.1.status, hero-kits.json#heroes.nec.abilities.2.status, hero-kits.json#heroes.nec.abilities.3.status, hero-kits.json#heroes.cha.abilities.0.status, hero-kits.json#heroes.cha.abilities.1.status` …

### `ambiguity_record_status_markers`

Category: **other** · Confidence: **resolved-from-plan** · Covered markers: **34**

Recommendation: Keep ambiguity records as provenance and cover them with this decision layer.

Reason: Plan/20 decision 11 defines GUESS and UNVERIFIED provenance; its open-questions section says sections 1-24 and 26 are closed by decisions or body values, while section 25 retains engine/data questions.

Sources:
- `plan/20-open-questions-sources-and-decisions.md:16`
- `plan/20-open-questions-sources-and-decisions.md:63`

Options:
- Keep ambiguity records as provenance and cover them with this decision layer
- Delete ambiguity records
- Promote all ambiguity records to final values

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-registry.json#ambiguities.0.statement, hero-registry.json#ambiguities.1.statement, hero-registry.json#ambiguities.3.statement, hero-registry.json#ambiguities.4.statement, hero-registry.json#ambiguities.5.statement, hero-registry.json#ambiguities.6.statement` …

### `cross_hero_hook_guesses`

Category: **other** · Confidence: **intentionally-open** · Covered markers: **21**

Recommendation: Keep hooks as GUESS flavor/spec notes outside first-playable mechanics until shared-counter support is chosen.

Reason: Plan/09 says every cross-hero hook is GUESS and requests a cross-hero unit-counter read; the first-playable slice focuses on six base kits and four ability slots each.

Sources:
- `plan/09-launch-hero-kits.md:6`
- `plan/09-launch-hero-kits.md:27`
- `plan/09-launch-hero-kits.md:46`
- `plan/10-remaining-hero-kits.md:37`

Options:
- Keep hooks as GUESS flavor/spec notes outside first-playable mechanics
- Implement every hook now with shared counters
- Cut all hooks

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-kits.json#emergent_hooks.0.status, hero-kits.json#emergent_hooks.1.status, hero-kits.json#emergent_hooks.2.status, hero-kits.json#emergent_hooks.3.status, hero-kits.json#emergent_hooks.4.status, hero-kits.json#emergent_hooks.5.status` …

### `default_damage_types`

Coverage role: **recommendation-only**

Category: **damage type** · Confidence: **owner-decision** · Covered markers: **0**

Recommendation: Use the plan defaults and allow row overrides; keep UNVERIFIED status.

Reason: The plan supplies defaults and explicitly allows a kit row to name another type; decision 11 keeps sourced numbers UNVERIFIED until a playable build exists.

Sources:
- `plan/09-launch-hero-kits.md:26`
- `plan/20-open-questions-sources-and-decisions.md:16`

Options:
- Use defaults: Ability 1 physical, Ability 2 magical, Ability 3 pure, while allowing row overrides
- Leave damage type unset
- Set every ability to one type

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-kits.json#value_tiers.defaults.damage_types, hero-kits.json#value_tiers.defaults.status`

### `engine_hero_id_language`

Coverage role: **recommendation-only**

Category: **engine id** · Confidence: **resolved-from-plan** · Covered markers: **0**

Recommendation: Use lowercase three-letter acronyms as engine IDs, with slot as separate data.

Reason: Plan/00 authority excludes 003 and 028-032; plan/25’s 001..032 language is historical source evidence; plan/20 decision 40 says engine identifiers live in the engine repo and use short acronyms.

Sources:
- `plan/00-index.md:42`
- `plan/25-engine-data-plan.md:54`
- `plan/20-open-questions-sources-and-decisions.md:40`

Options:
- Use lowercase three-letter acronyms as engine IDs, with slot as separate data
- Use contiguous 001..032 IDs
- Use slots with gaps as IDs

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-registry.json#engine_convention.hero_id, hero-registry.json#engine_convention.pattern`

### `forever_eternal_loop_clip`

Coverage role: **recommendation-only**

Category: **threshold** · Confidence: **owner-decision** · Covered markers: **0**

Recommendation: Keep the three-stun clip as a provisional bound and enforce plan/24’s longest-stun <=3 s test.

Reason: The kit explicitly says three stuns and marks it UNVERIFIED; plan/24 test-first asks the longest stun to stay at or below 3 s; plan/26 C6 shortens a fourth disable in a 10 s window.

Sources:
- `plan/10-remaining-hero-kits.md:27`
- `plan/24-power-tier-draft.md:70`
- `plan/26-first-playable-cut-list-and-checks.md:86`

Options:
- Keep three-stun clip as provisional, capped by plan/24 test at <=3 s
- Leave clip unbounded until owner decision
- Owner picks a different clip length

Affected heroes: `for`

Export field paths: `hero-kits.json#heroes.for.abilities.3.mechanic, hero-kits.json#heroes.for.abilities.3.numeric_values`

### `sigma_value_tiers`

Category: **balance value** · Confidence: **owner-decision** · Covered markers: **2**

Recommendation: Use the plan tier table as implementation defaults, still labelled UNVERIFIED pending playable build.

Reason: Plan/09 gives exact Sigma and tier values; plan/20 decision 11 says a new number with a source is UNVERIFIED until a playable build exists; plan/19 states new-system numbers are thresholds to test, not results.

Sources:
- `plan/09-launch-hero-kits.md:12`
- `plan/09-launch-hero-kits.md:16`
- `plan/09-launch-hero-kits.md:17`
- `plan/09-launch-hero-kits.md:18`
- `plan/09-launch-hero-kits.md:19`
- `plan/20-open-questions-sources-and-decisions.md:16`
- `plan/19-balance-and-qa.md:79`

Options:
- Use the plan tier table as implementation defaults, still labelled UNVERIFIED pending playable build
- Wait for balance pass before emitting numeric defaults
- Use engine values from another repo

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-kits.json#value_tiers.sigma.status, hero-kits.json#value_tiers.defaults.status`

### `talent_values`

Category: **talent** · Confidence: **resolved-from-plan** · Covered markers: **6**

Recommendation: Keep named talent choices, cut talent values from first-playable data, and add full sets only after base kits are tested.

Reason: Plan/26 explicitly cuts talents from v1; plan/21 says all talent numbers are UNVERIFIED and named choices are GUESS where marked; plan/20 decision 11 prevents GUESS numbers passing as checked.

Sources:
- `plan/21-systems-added-back.md:5`
- `plan/21-systems-added-back.md:9`
- `plan/26-first-playable-cut-list-and-checks.md:52`
- `plan/20-open-questions-sources-and-decisions.md:16`

Options:
- Keep named talent choices but cut talent values from first-playable data
- Owner approves full talent numbers now
- Generate family-template talent numbers

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-kits.json#heroes.coo.talents.0.choice, hero-kits.json#heroes.coo.talents.1.choice, hero-kits.json#heroes.coo.talents.2.choice, hero-kits.json#heroes.coo.talents.3.choice, hero-kits.json#heroes.got.talents.2.choice, hero-kits.json#heroes.got.talents.3.choice`

### `voice_cooldown_8s`

Category: **voice cap** · Confidence: **owner-decision** · Covered markers: **1**

Recommendation: Use 8 s as a provisional runtime cooldown and keep the balance-pass note.

Reason: Plan/23 gives 8 s, explains the reason and marks it GUESS; plan/20 decision 11 keeps sourced GUESS values from passing as checked values.

Sources:
- `plan/23-voice-and-banter.md:10`
- `plan/20-open-questions-sources-and-decisions.md:16`

Options:
- Use 8 s as provisional cooldown
- Owner chooses another cooldown
- Disable per-line cooldown

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-voice.json#rules.cooldown_status`

### `voice_line_cap`

Category: **voice cap** · Confidence: **resolved-from-plan** · Covered markers: **1**

Recommendation: Enforce under twelve words as a validation rule.

Reason: Plan/23 directly states hero and pair lines stay under twelve words; only the cap is UNVERIFIED, not the design intent.

Sources:
- `plan/23-voice-and-banter.md:8`

Options:
- Enforce under twelve words
- Owner chooses a different cap
- Leave uncapped

Affected heroes: `nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Export field paths: `hero-voice.json#rules.line_cap_status`

### `wojak_sorrowful_cancel_threshold`

Coverage role: **recommendation-only**

Category: **threshold** · Confidence: **owner-decision** · Covered markers: **0**

Recommendation: Keep below 25% health as a provisional implementation threshold, labelled UNVERIFIED.

Reason: The kit row gives below 25% and marks the threshold UNVERIFIED; plan/24 keeps Wojak unflagged and test-first list focuses on longer balance risks.

Sources:
- `plan/10-remaining-hero-kits.md:26`
- `plan/24-power-tier-draft.md:69`

Options:
- Keep below 25% health as provisional threshold
- Set threshold after playtest
- Use a different threshold chosen by owner

Affected heroes: `woj`

Export field paths: `hero-kits.json#heroes.woj.abilities.3.mechanic, hero-kits.json#heroes.woj.abilities.3.numeric_values`
