# 27. Scoped plan: gm skills review and savi/spawn follow-up

Status: Phase 2 decision list approved as written (plan/20 decision 53). The Phase 1 audit is in plan/29. Phase 3 has not started, and no gm edits were made in this plan. Items 1, 2 and 7 from the remaining-work list are held for the owner. Item 8 is another session's work.

## Why

The original goal asked for three things: confirm the gm skills are current, study ../savi and ../spawn for features worth adding, and finish the remaining work. The skills check was never done in the bota session, and the spawn tool has only partial coverage. This plan scopes the next pass so it can run without guessing.

## Facts already established

- `gm/tools/spawn.mjs` exposes reads (me, worlds, inbox, docs, rooms, logs, health) and gated writes (publish, crew-ask, chat-room, dm, exec, asset-put, mod, push). Writes are dry runs unless `--yes` is given.
- `gm/DESIGN.md`, "Decided" item (4): scope is reads plus gated writes. Account doors (token revoke, signup, login link) are not wired because they change credentials.
- Live sends have never run.
- Another session has uncommitted gm changes in `native/components/host`, `.github/workflows`, `scripts/install.*`, `tools/release-manifest.mjs` and `skills/gm-continue/SKILL.md`. This plan does not touch them.

## Phase 1: audit (read-only)

1. Read `skills/gm/SKILL.md`, `skills/dev/SKILL.md` and `skills/gm-continue/SKILL.md` in gm. For each verb or tool they name, confirm it exists in the current gm verb list (`gm.verbs()`). Record mismatches in a table: skill, line, named verb, status.
2. Run `node tools/spawn.mjs` with no arguments and each read verb to confirm the usage text matches the code. Do not run writes.
3. Read the spawn Tome reference through the live `docs` read verb (`node tools/spawn.mjs docs`). `../spawn` holds no docs; it has only `.claude/`, `.playwriter/`, `runs/` and `sources/`. Read the savi endpoint doc at `../savi/.spawn/agent-interface.md`. List every endpoint or feature they expose that spawn.mjs does not cover. Mark each as read, gated write, or out of scope (account doors).

Exit: one audit table and one feature list, each row with a size (S/M/L) and a reason.

## Phase 2: decide (no edits)

1. Keep the Decided item (4) scope unless the audit shows a read-only gap that is clearly useful. A new read verb needs no owner approval. A new write verb does, and it needs a dry-run default and `--yes`.
2. Any skill mismatch becomes a PRD row in gm, not an in-place edit here.
3. Live sends stay blocked until the owner approves a first send.

Exit: a short decision list for the owner, with the default choice marked.

## Phase 3: implement (after owner sign-off on Phase 2)

1. Fix skill mismatches in gm, one skill per change, each pushed to main with the gm invariants (no trailers, lanmower attribution).
2. Add any approved read verbs to spawn.mjs, with a usage line and no token output.
3. Verify each change by running the verb against the live read endpoints and quoting the output. No live writes.

## Phase 4: validate

- `node tools/spawn.mjs` usage matches the verb table.
- Every skill reference resolves to a verb in `gm.verbs()`.
- `git status` in gm shows only the intended files, with the other session's changes still untouched.

## Out of scope

- Account doors (token revoke, signup, login link).
- Live writes (publish, chat, exec, asset-put) until the owner approves.
- Other session's uncommitted gm changes.
- The three retired-character originals and the `../bota-notdone` archive (owner decision, item 1 and 2).

## Open questions, with answers

1. Approve the Phase 2 decision list before any Phase 3 edits? Approved as written (plan/20 decision 53). Phase 3 still needs the audit in plan/29.
2. Is a first live Spawn write approved, and if so, which room? Held. Not approved yet; the owner has to name a test room (plan/28 item 7, irreversible).
3. Should the audit cover `../savi` as well as `../spawn`? Yes, read only (plan/20 decision 54).
