# BOTA owner-decision brief

Generated: `2026-11-11T08:23:05.210328+00:00`

Scope: only `owner-decision` and `intentionally-open` rows from `export/rule-demand.json`. No value is recommended, applied, or promoted. `do_not_promote: true` remains in force; `export/engine-resolved/` is absent.

Rows: `2`. Canonical engine data and the 425 decision-gated null fields are unchanged.

## `rule-demand/eternal-loop` — `owner-decision`

- Current actor: `owner`. Stable ID: `resolve:78018b1b730b1b83`.
- Rule citation: `plan/18-asset-manifest-and-audio.md:1` — `# 18. Asset manifest and audio`
- Evidence: `export/decision-packet.json; export/DECISION-PACKET.md`
- Current destination/reference: `export/decision-packet.json#forever_eternal_loop_clip`
- Gate: `do_not_promote: true`.

Neutral options:

1. **Keep gated.** Leave the exact clip duration/content as an owner decision. Nothing changes in engine data, kit behavior, voice rules, or the decision packet.
2. **Owner supplies an exact choice.** Record the chosen value and its confidence in the owner decision flow. Only an explicit confirmed apply could write an opt-in `export/engine-resolved/` overlay; canonical `export/engine/` remains null-gated.
3. **Defer to a playable build.** Keep the current text rule and wait for measured build evidence. The row remains `owner-decision`; no `UNVERIFIED`/`GUESS` value is promoted.

If accepted: only the named decision field may gain an owner-chosen value through the existing apply mechanism. The Receipt/Repost/Camera chains, 27 gallery images, 26 active heroes, `003` image-only Reserve, and all other null gates stay unchanged.

Acceptance criteria:

- Owner records an explicit choice
- No canonical engine value is written
- do_not_promote remains true

Non-promotion invariant:

- `do_not_promote: true`
- canonical `export/engine/` unchanged
- `export/engine-resolved/` absent
- no new `GUESS`/`UNVERIFIED` value promoted

## `rule-demand/transition-wipe` — `intentionally-open`

- Current actor: `bota`. Stable ID: `resolve:42b153c501fe22c4`.
- Rule citation: `plan/16-humor-and-tone.md:4` — `### Rules`
- Evidence: `plan/16-humor-and-tone.md; plan/34-content-status-adjudication.md`
- Current destination/reference: `plan/16-humor-and-tone.md:8`
- Gate: `do_not_promote: true`.

Neutral options:

1. **Keep intentionally open.** The presentation cue remains a text rule with no exact visual asset. Nothing changes.
2. **Owner asks for a concrete cue.** BOTA may add a rule demand for a specific hash-verified hy3d content row; the cue is not invented and no numeric value is promoted.
3. **Owner retires the cue.** Remove or simplify the presentation line in a future rule pass, while preserving the three-beat chain structure and all decision gates.

If accepted: only presentation wording or a future demand row changes. No canonical engine field, ability value, active hero key, or `003` reserve status changes.

Acceptance criteria:

- Design remains intentionally open
- No canonical engine value is written
- do_not_promote remains true

Non-promotion invariant:

- `do_not_promote: true`
- canonical `export/engine/` unchanged
- `export/engine-resolved/` absent
- no new `GUESS`/`UNVERIFIED` value promoted
