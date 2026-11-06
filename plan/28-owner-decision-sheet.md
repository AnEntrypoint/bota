# 28. Owner decision sheet

Every item below is owner-blocked. Nothing here has been acted on. Each item gives the decision, the options, and a recommended choice with its reason. Recommendations are for the owner to accept or change.

Item numbers follow the remaining-work list the orchestrator relayed. Items 1, 2, 4, 7 and 8 are matched by content, as plan/27 describes them. Where the match is inferred, the item says so.

## 1. Delete `../bota-notdone`

- **Decision:** delete the archive folder beside this repo.
- **Options:** (a) delete now; (b) inspect first, then delete; (c) keep.
- **Recommended:** (b). Check that every file in the archive is either in bota's git history or is no longer needed, then delete. The archive was not inspected for this sheet, so its contents are unknown here.

## 2. Delete retired originals, `research/` and `sources/`

- **Decision:** remove the cut characters' source files and the two working folders.
- **Options:** (a) delete the retired originals in `/workspace/chars` (Chonky Hop 002, Soyjak 006, Trevor 015, and the other non-kept originals) and keep `research/` and `sources/`; (b) delete all three; (c) keep all.
- **Recommended:** (a). The retired originals are cut, and no kept character depends on them. Keep `research/` and `sources/` until someone checks whether they hold the only record of asset provenance, since plan/20 lists sources as open. The retired files were not inspected for this sheet.

## 3. Cole art (inferred match: item 3 is the art decision)

- **Decision:** whether Cole's render stays as it is or is regenerated to match the new card.
- **Options:** (a) keep the restored original render; (b) regenerate from a prompt that matches the card's Ash look (goofy cartoon trainer, spiky black hair under a red-and-white cap); (c) keep the render and reword the card to match it.
- **Recommended:** (a). The owner already said "coles art was already right as it was". The card wording (`characters/024-cole.md`) is the part that can change, so (c) follows if the owner wants the card to match the render. Regeneration (b) costs an image run and is not needed to satisfy that statement.

## 4. Another session's gm changes (routed to gm)

- **Decision:** what happens to uncommitted gm changes in `native/components/host`, `.github/workflows`, `scripts/install.*`, `tools/release-manifest.mjs` and `skills/gm-continue/SKILL.md`.
- **Options:** (a) the gm session commits or discards them; (b) bota stashes them; (c) leave them as they are.
- **Recommended:** (a). These are gm's files and the gm session owns them. Bota does not touch them (plan/27).

## 5. Six-hero launch set (plan/09) versus first-playable slice (plan/26)

The two plans name different six heroes. They share three (Grey, Boomer, Ghillie), so three of six differ.

- **Plan/09 launch set:** Grey, Boomer, Noscope, Wojak, Ghillie, Forever. Covers four of twelve role families.
- **Plan/26 slice set:** Grey, Gothgirl, Ecce, Coomer, Boomer, Ghillie. Covers six role families.
- **Decision:** which six heroes launch, and whether the slice set and launch set are the same.
- **Options:** (a) use the plan/26 slice set for both; (b) use the plan/09 set for both; (c) keep them separate on purpose.
- **Recommended:** (a). The slice exists to test the mechanics across role families, and plan/26 covers six families where plan/09 covers four. Make plan/09 follow it. Note: this changes plan/09's Noscope, Wojak and Forever rows, which then move to the second wave.

## 6. Gigachad as reserve

- **Decision:** where Gigachad sits.
- **Options:** (a) reserve, as now; (b) promote to active (26 active becomes 27); (c) remove.
- **Recommended:** (a). It is already reserve in the card (`- Status: reserve.`) and in roster.yaml, and the owner asked to combine Gigachad with Chad as Chad's ultimate while keeping both in the gallery. Promoting it would also change the 26 active count the plans use.

## 7. Spawn scope, account doors and the first live send (plan/27 open questions)

Three linked decisions.

- **7a. Spawn scope.** Options: (a) reads plus gated writes, dry run unless `--yes` (the current DESIGN.md decision); (b) reads only. **Recommended:** (a). Writes stay dry until a first send is approved.
- **7b. Account doors** (token revoke, signup, login link). Options: (a) leave unwired; (b) wire them. **Recommended:** (a). They change credentials, which a peer or a script should not do.
- **7c. First live Spawn send** (plan/27 question 2). Options: (a) approve `chat-room` to a named test room; (b) hold until a room is named. **Recommended:** (b) until the owner names a room. The room is the one fact needed before any send, and no send has run so far.

## 8. Phase 2 decision list and the Savi audit scope (plan/27 questions 1 and 3)

- **8a. Approve the Phase 2 decision list before any Phase 3 edits.** Options: (a) approve as written; (b) approve with changes; (c) hold. **Recommended:** (a). Phase 3 only fixes skill mismatches and adds read verbs, and it needs no live writes.
- **8b. Audit scope.** Options: (a) spawn only; (b) spawn and `../savi`. **Recommended:** (b), read-only. The spawn docs point at the Savi endpoint doc (`../savi/.spawn/agent-interface.md`), so the audit misses endpoints without it. The skill check has already confirmed the `spawn-engine` read path.

## Reply format

For each item, the owner answers with the letter chosen (for example, "5a, 7b, 8b"). Any other answer is recorded as written.
