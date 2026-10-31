---
name: lame-fix
description: "Fixes the top open findings in .gm/lame/ledger.json at their authoritative sources, verifies with the repo's checks, publishes the changed product files, then calls lame-list back for the next round. Use only from lame-list or when asked to fix the lame list; if the ledger is empty it seeds the loop by calling lame-list. Does not hunt new findings."
---

# lame-fix

You are the surgeon. Fix what the list proves, at the source that owns it, verify it, publish it, and call lame-list back. Do not expand scope silently and do not hunt new findings; that is lame-list's job.

If this skill is invoked first and the ledger is missing or has no findings, call Skill with skill "lame-list" and args "round=1 rounds=<rounds>" and stop. The loop starts there.

## Shared contract: the lame loop

State: .gm/lame/ledger.json. The full contract is in ../lame-list/SKILL.md; the load-bearing rules are repeated here.

- Severity: P0 lies and broken rules, P1 pillar or evidence failures, P2 identity, bloat and polish.
- Kinds: contradiction | unearned | grey-pillar | identity | stale-ref | bloat | spec-gap | comment.
- Status: open | fixed | blocked | wontfix | stale. Keep every row and every id.
- Round bound: rounds defaults to 3, clamped to 1..5. Fix at round N, then call list at round N+1. Never call list twice in one pass.
- Terminal: after fixing round N, if N >= rounds, report and stop. If only blocked or wontfix rows remain, report and stop. A pass that fixes nothing and leaves no open row ends the chain.
- Degradation: plain JSON and only Read/Write are enough. If Skill is unavailable, read ../lame-list/SKILL.md and follow it inline. When gm is available, use fs_read, fs_write, codesearch and the git verbs.

## Fix at the source

| Finding is about | Edit | Regenerate |
| --- | --- | --- |
| A plan rule or number | plan/NN-*.md | spec.prd only through its generator, never by hand |
| A character's subject, hook or Card | characters/NNN-*.md subject or hook | node tools/sync-roster.mjs (then --check) |
| A generated roster table or gag | the character or plan source | node tools/sync-roster.mjs |
| An original MOBA name in shipped text | remove it from the shipped text; keep the mapping in internal/parity-map.md | none |
| A broken manifest or index path | the source that emits it | its generator |
| A comment in source | make the code self-explanatory; move any durable fact to AGENTS.md | none |

Repo rules the edit must keep:
- 6.88g wins over every other source. If 6.88g is silent, use our data, map and script, then the web, then a GUESS with its reason. Label every value.
- A generated file is never hand-edited. Edit the generator or the source it reads.
- No brand names, named creators, franchise characters or owned catchphrases (plan/20 decision 7). Original names only in internal/parity-map.md and the decision record (decisions 8 and 22).
- Clout is the only audience resource and never a stat (decisions 4 and 9). Do not add a new resource.
- Keep the voice, table shape and anchors. The smallest edit that removes the defect wins.
- If a real design decision is needed: choose the most defensible default consistent with plan/02 and plan/20, add a decision row to plan/20 when the choice changes the design, and label any new number UNVERIFIED. If that default would contradict an explicit decision, set the row blocked with the exact question and skip it. Do not ask the user mid-loop.

## Procedure

1. Parse args: round, rounds (default 3, clamp 1..5), batch (default 12), retry_blocked (default false), publish (default true).
2. Load .gm/lame/ledger.json. If it is missing or has no findings, call Skill "lame-list" with round=1 and stop. If round is absent, use ledger.round. If round > rounds, print LAME: CAP and stop.
3. Select rows: all open P0, then P1, then P2, up to batch. Skip blocked unless retry_blocked is true. Never select fixed, stale or wontfix rows.
4. If no row is selected: print LAME: BLOCKED or LAME: CLEAN with the remaining rows and stop.
5. For each selected row, in order:
   - Re-read the anchor. If it is gone, set status stale and continue. If the defect is already gone, set status fixed with witness "re-check" and continue.
   - Apply the smallest source edit that removes the cause, following the table and repo rules above.
   - Re-read the changed line and confirm the defect is gone. A fix that only softens the wording without removing the contradiction or gap is not a fix.
6. Verify the batch:
   - After any character or roster edit: run node tools/sync-roster.mjs --check. On failure, run node tools/sync-roster.mjs, then re-run --check. Record the exact command and exit result.
   - Confirm touched links and paths exist. Confirm 112 active plus 5 reserve heroes and that INDEX.tsv matches the files.
   - If the edit touched internal/parity-map.md, confirm the map still has no original name in plan/, characters/, README.md or ROSTER.md.
   - If a check cannot run, record witness "unavailable: <reason>"; never mark a row fixed without a witness of some kind.
7. Update the ledger: fixed with its witness, blocked with its exact question, wontfix with its reason. Rewrite the whole file atomically. Never commit the ledger.
8. Publish, when publish is true and git is available: add only the product files changed, by explicit path; commit with the author lanmower and no Co-Authored-By, Signed-off-by or generated-with trailer; push main. On a rejected push, fetch, reapply on the new tip, push. If a CI run exists for the pushed sha, read it; a red run becomes a new P0 open row in the ledger, not a success. If git or the remote is unavailable, record publish unavailable in the response and leave the working tree.
9. Handoff. If round < rounds, call Skill with skill "lame-list" and args "round=<round+1> rounds=<rounds>". If round >= rounds, print LAME: CAP round=N and stop with the counts fixed, blocked, wontfix and publish.

## Never

- Never hand-edit spec.prd, roster.yaml, characters/INDEX.tsv, a Card section or plan/15 gags.
- Never invent a 6.88g fact, a brand name, a new hero, or a new resource.
- Never mark fixed without re-reading the anchor and recording a witness.
- Never publish the ledger, .gm state or an unrelated file.
- Never end a pass with an open row and round < rounds without calling lame-list.
