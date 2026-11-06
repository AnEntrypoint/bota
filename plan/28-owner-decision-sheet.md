# 28. Owner decision sheet

Status: items 3a, 3b, 3c, 3d, 4, 6a and 6b were approved by the orchestrator as reversible and are recorded in plan/20 decisions 48 to 54. Item 3a moved the launch kits in plan/09 and plan/10. Items 1, 2 and 7 are held for the owner (irreversible). Item 8 is for the gm session to commit its own changes; nothing is discarded.

Every item below is owner-blocked unless marked approved above. Each item gives the decision, the options, and a recommended choice with its reason. Recommendations are for the owner to accept or change.

Item numbers follow the orchestrator's remaining-work list. Item 5 (the stale gm run) is done and is left out.

## 1. Delete `../bota-notdone`

- **Decision:** delete the archive folder beside this repo.
- **Options:** (a) delete now; (b) inspect first, then delete; (c) keep.
- **Recommended:** (b). Check that every file in the archive is either in bota's git history or is no longer needed, then delete. The archive was not inspected for this sheet, so its contents are unknown here.

## 2. Delete retired originals, `research/` and `sources/`

- **Decision:** remove the cut characters' source files and the two working folders.
- **Options:** (a) delete the retired originals in `/workspace/chars` (Chonky Hop 002, Soyjak 006, Trevor 015, and the other non-kept originals) and keep `research/` and `sources/`; (b) delete all three; (c) keep all.
- **Recommended:** (a). The retired originals are cut, and no kept character depends on them. Keep `research/` and `sources/` until someone checks whether they hold the only record of asset provenance, since plan/20 lists sources as open. The retired files were not inspected for this sheet.

## 3. Owner confirmations

Four separate decisions.

- **3a. Six-hero launch set and slice picks.** Plan/09 and plan/26 name different six heroes. They share three (Grey, Boomer, Ghillie), so three of six differ.
  - Plan/09 launch set: Grey, Boomer, Noscope, Wojak, Ghillie, Forever. Covers four of twelve role families.
  - Plan/26 slice set: Grey, Gothgirl, Ecce, Coomer, Boomer, Ghillie. Covers six role families.
  - Options: (a) use the plan/26 slice set for both; (b) use the plan/09 set for both; (c) keep them separate on purpose.
  - **Recommended:** (a). The slice exists to test the mechanics across role families, and plan/26 covers six where plan/09 covers four. Plan/09's Noscope, Wojak and Forever rows would then move to the second wave.
- **3b. Gigachad as reserve.** Options: (a) reserve, as now; (b) promote to active (26 active becomes 27); (c) remove. **Recommended:** (a). The card already says `- Status: reserve.`, and the owner asked to keep Gigachad in the gallery as Chad's ultimate. Promoting it would change the 26 active count the plans use.
- **3c. Spawn scope.** Options: (a) reads plus gated writes, dry run unless `--yes` (the current DESIGN.md decision); (b) reads only. **Recommended:** (a). Writes stay dry until a first send is approved (see item 7).
- **3d. Account doors** (token revoke, signup, login link). Options: (a) leave unwired; (b) wire them. **Recommended:** (a). They change credentials, which a peer or a script should not do.

## 4. Cole's Ash-style card and prompt

- **Decision:** whether Cole's card and prompt are reworded to the Ash look, and whether the render changes to match.
- **Options:** (a) keep the restored original render and leave the card as it is; (b) keep the render and reword the card to match it; (c) regenerate the render from a prompt that matches the card's Ash look (goofy cartoon trainer, spiky black hair under a red-and-white cap).
- **Recommended:** (a). The owner already said "coles art was already right as it was". If the owner wants the card to match the render instead, take (b). Regeneration (c) costs an image run and is not needed to satisfy that statement.

## 6. Open questions from the plan/27 scoped plan

- **6a. Approve the Phase 2 decision list before any Phase 3 edits.** Options: (a) approve as written; (b) approve with changes; (c) hold. **Recommended:** (a). Phase 3 only fixes skill mismatches and adds read verbs, and it needs no live writes.
- **6b. Audit scope.** Options: (a) spawn only; (b) spawn and `../savi`. **Recommended:** (b), read-only. The spawn docs point at the Savi endpoint doc (`../savi/.spawn/agent-interface.md`), so a spawn-only audit misses endpoints. The skill check has already confirmed the `spawn-engine` read path.

## 7. Live Spawn sends (publish, chat, exec)

- **Decision:** whether any live write runs, and to where.
- **Options:** (a) approve one first send, `chat-room` to a named test room; (b) hold until the owner names a room; (c) approve publish or exec as well.
- **Recommended:** (b). No live send has run, and the room is the one fact needed before the first send. Publish and exec are not recommended for a first send.

## 8. Uncommitted gm changes owned by another session

- **Decision:** what happens to uncommitted gm changes in `native/components/host`, `.github/workflows`, `scripts/install.*`, `tools/release-manifest.mjs` and `skills/gm-continue/SKILL.md`.
- **Options:** (a) the gm session commits or discards them; (b) bota stashes them; (c) leave them as they are.
- **Recommended:** (a). These are gm's files and the gm session owns them. Bota does not touch them (plan/27).

## 9. Talent choices for the slice heroes without named sets

Decided by the orchestrator: write the smallest option that matches the hero pattern. Each hero's named row in plan/21 uses its role family's values with its own ability names.

- **9a. Gothgirl: decided.** Named row added in plan/21 (role family Recluse values). Reversible.
- **9b. Ecce: decided.** Named row added in plan/21 (role family Archivist values). Reversible.
- **9c. Coomer: decided.** Named row added in plan/21 (role family Firebrand values, GUESS where marked). Reversible.
- **9d. GUESS entries: decided.** Keep as written: Gothgirl's Cardigan Flicker root and Velvet Double heal, Gothgirl's Clout and regen rows, and Coomer's four GUESS cells (plan/21, named rows for Gothgirl and Coomer). Reversible.

## Reply format

For each item, the owner answers with the letter chosen (for example, "3a, 4a, 6b"). Any other answer is recorded as written.
