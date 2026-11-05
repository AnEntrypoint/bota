---
name: lame-list
description: "Lists what is lame in this repo: an evidence-ranked audit of contradictions, unearned numbers, grey pillar failures, duplicate identities, stale references, bloat and spec gaps. Writes .gm/lame/ledger.json, then hands off to lame-fix, which fixes and calls this skill back. Use when asked to list what's lame, critique the design, find weaknesses, or run the lame loop. Does not edit product files."
---

# lame-list

You are the prosecution. Find what is lame, rank it, cite it, and hand it to lame-fix. You do not edit product files. lame-fix fixes and calls you back with the next round.

## Finish invariant

Every successful run ends in exactly one of these states. There is no fifth state and no prose-only stop while a handoff is due.

- HANDOFF: at least one row is open and round <= rounds -> invoke the lame-fix skill with round=<round> rounds=<rounds>. This is the default finish.
- CLEAN: no row is open -> print LAME: CLEAN round=N and stop.
- BLOCKED: only blocked or wontfix rows remain -> print LAME: BLOCKED round=N with each question and stop.
- CAP: round > rounds -> print LAME: CAP and stop.

A run that finds open rows and stops without HANDOFF has failed.

## Shared contract: the lame loop

State: .gm/lame/ledger.json. Both skills read and rewrite this one file.

    {
      "round": 1,
      "rounds": 3,
      "findings": [
        {
          "id": "L001",
          "round": 1,
          "severity": "P0",
          "kind": "contradiction",
          "file": "plan/06-clout.md",
          "anchor": "line 42, or the exact quoted sentence",
          "finding": "one sentence",
          "why": "the rule or decision it violates",
          "fix": "the smallest change that removes it",
          "status": "open",
          "witness": null
        }
      ]
    }

- **Severity.** P0: the docs lie or break their own rule; a reader or implementer would build the wrong thing. P1: a plan/02 pillar fails, a number is unearned, or a shipped reference is stale. P2: weak identity, bloat, polish.
- **Kinds.** contradiction | unearned | grey-pillar | identity | stale-ref | bloat | spec-gap | comment.
- **Evidence.** Every row cites a file and a line or an exact quote. A taste call without a named comparison and a cited rule is not a finding.
- **No deletion.** Keep ids. Update status. Never drop a row.
- **Status.** open | fixed | blocked | wontfix | stale.
- **Round bound.** rounds defaults to 3, clamped to 1..5. One user invocation runs at most that many list/fix pairs. list calls fix at round N; fix calls list at round N+1.
- **Terminal.** Stop when a pass adds no new open row, when only blocked/wontfix rows remain, or when round reaches rounds.
- **Degradation.** The ledger is plain JSON and works with only Read/Write. If the harness has no skill tool, read ../lame-fix/SKILL.md and follow it inline. When gm is available, use gm.search, gm.read_file, gm.write_file and the gm.git_* verbs, not shell grep/find.
- **Publish.** This skill never publishes. lame-fix publishes after verification.
- **Tracking.** When gm is available, mirror every row to a PRD row with prd_add (id lame-L001, subject, description, acceptance_criteria, witness_plan) and use prd_list to read status. The JSON ledger stays the portable source for skill-only agents.

## What counts as lame

1. **Contradiction (P0).** Two sources disagree on a number, name, count or rule; or a shipped claim contradicts plan/20 or a repo invariant.
2. **Unearned certainty (P1).** A number or claim is stated as fact with no UNVERIFIED or GUESS label and no source, where plan/20 decisions 11 and 21 require one; or a GUESS has no stated reason. One section-level UNVERIFIED banner covers that section's numbers; an unlabeled number outside it is a finding.
3. **Grey pillar (P1).** A system fails one of the four rules in plan/02: Readable, Decisive, Mapped, Off the read path. A choice with no cost on one side, a system with no classic job, a joke on the read path, or a signal that needs text all qualify.
4. **Identity (P2; P1 if two heroes are indistinguishable).** A hero, item, ability or voice shares its role, silhouette and hook, or three stat/behaviour lines, with another and adds no decision. A name that is a costume rather than a mechanic, or a joke that explains itself, qualifies.
5. **Stale reference (P1).** A broken link or path, a missing file, generated drift, a count mismatch, a section or banner that no longer applies, or an open question left in shipped text.
6. **Bloat (P2).** A paragraph restates a rule, explains the joke, or duplicates another section; a table row with no decision.
7. **Spec gap (P1).** A rule cannot be read at a glance, measured, or implemented; a playtest has no observable pass condition; a check has no threshold where one is required; a term is used before it is defined.
8. **Comment (P1).** Any comment in source. This repo keeps facts in AGENTS.md and intent in names. Cite the comment; the fix moves the durable fact and deletes the comment.

## Authoritative sources

| What | Edit here | Never here |
| --- | --- | --- |
| Plan chapter | plan/NN-*.md | any generated copy of the plan |
| Character subject and hook | characters/NNN-*.md | roster.yaml, characters/INDEX.tsv, a file's ## Card section, plan/15 signature gags (all generated by tools/sync-roster.mjs) |
| Original MOBA names | internal/parity-map.md | plan/, characters/, README.md, ROSTER.md, the site, a pack (plan/20 decisions 8 and 22) |
| Numbers | the chapter that owns the number | any copy of the number elsewhere |

Baseline facts: 28 active heroes plus 6 reserve heroes (34 files); INDEX.tsv is generated; node tools/sync-roster.mjs --check exits 1 on drift; manifest.json lists every shipped doc.

## Procedure

1. Parse args: round, rounds (default 3, clamp 1..5), scope (default all; or plan, characters, or a comma-separated path list).
2. Load .gm/lame/ledger.json. Create it if absent. If round is absent, use ledger.round + 1 when the ledger already has findings, else 1. If round > rounds, print LAME: CAP and stop.
3. Revalidate every open row against its file and anchor. No anchor: status stale. Anchor present and defect gone: status fixed with witness "re-check". Anchor present and defect still there: keep open.
4. Read the baseline: README.md, plan/00-index.md, plan/02-vision-and-pillars.md, plan/20-open-questions-sources-and-decisions.md, manifest.json, characters/INDEX.tsv, roster.yaml, tools/sync-roster.mjs. If node is available, run node tools/sync-roster.mjs --check and record the exact pass or fail.
5. Audit these dimensions. Fan out one subagent per dimension when the harness allows; otherwise run them in order. Each subagent uses gm.search, returns only file:line citations, an exact quote, the rule id and a one-sentence fix, and edits nothing.
   - A. Contradiction and references: documents against documents, links, manifest paths, section references, counts, generated drift.
   - B. Pillars and decisions: every system against plan/02's four rules and plan/20's decision table.
   - C. Identity and tone: hero, item, ability and voice distinctness; decision 7 (no brand names, named creators, franchise characters or owned catchphrases); decisions 8 and 22 (no original MOBA name outside internal/parity-map.md); jokes off the read path.
   - D. Completeness and executability: undefined terms, circular rules, playtests without a pass condition, checks without thresholds, open questions in shipped text.
   - E. Bloat and hygiene: restated rules, explained jokes, duplicate sections, comments in source.
6. Dedupe new rows against existing rows by kind, file and normalized anchor. Assign ids L001, L002, ... in one sequence. Set round on new rows.
7. Rewrite the whole ledger atomically. Never commit it. When gm is available, mirror new and changed rows with prd_add.
8. Print a compact table: id, severity, file:line, finding.
9. Handoff. Apply the finish invariant: HANDOFF when any row is open and round <= rounds; otherwise CLEAN, BLOCKED or CAP.

## Never

- Never edit a product file, mark a finding fixed, or invent evidence.
- Never add a finding from memory without re-reading the cited line.
- Never call lame-fix twice in one pass.
