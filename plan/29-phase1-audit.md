# 29. Phase 1 audit: gm skills, spawn usage, spawn and savi gaps

Read-only. Source checks: gm verb list from `gm.verbs()` (44 verbs, run through run_code), gm skill files, `/workspace/gm/tools/spawn.mjs`, `/tmp/spawn-docs.json`, `/workspace/savi/.spawn/agent-interface.md`. No write verb of spawn.mjs was run, and no live read was sent (see the note under section 2).

## 1. Skill verb references

Status key: exists = in `gm.verbs()`; helper = a runtime wrapper, not a verb row; family = a name pattern whose members exist. No missing, renamed or unreadable entries.

| skill | line | named verb | status |
|---|---|---|---|
| gm/SKILL.md | 14, 39, 40, 43, 44, 57, 93, 108 | gm.read_file | exists |
| gm/SKILL.md | 39, 59 | gm.write_file | exists |
| gm/SKILL.md | 39, 60, 79, 129 | gm.run_shell | exists |
| gm/SKILL.md | 39 | gm.verbs() | exists (lists the verbs; not itself a row) |
| gm/SKILL.md | 41, 75, 79 | gm.try | helper (wrapper, absent from verbs list) |
| gm/SKILL.md | 42, 67, 70 | gm.job_start, gm.job_status | exists |
| gm/SKILL.md | 42 | gm.job_stop | exists |
| gm/SKILL.md | 22 | gm.playwriter_execute, gm.playwriter_browsers | exists |
| gm/SKILL.md | 32, 38, 43, 107 | gm.query_log | exists |
| gm/SKILL.md | 43 | gm.search | exists |
| gm/SKILL.md | 43 | gm.prd_delete | exists |
| gm/SKILL.md | 43, 112 | gm.unknown_add | exists |
| gm/SKILL.md | 43 | gm.unknown_resolve | exists |
| gm/SKILL.md | 112 | gm.prd_add | exists |
| gm/SKILL.md | 37-44 | next_context, finish, run_code (served MCP tools) | exists (host tool list) |
| dev/SKILL.md | 10 | gm.job_start | exists |
| dev/SKILL.md | 24 | gm.fetch | exists |
| gm-continue/SKILL.md | 8, 21 | gm.stat_file | exists |
| gm-continue/SKILL.md | 8, 21 | gm.prd_list | exists |
| gm-continue/SKILL.md | 8, 21 | gm.unknown_list | exists |
| gm-continue/SKILL.md | 11, 21 | gm.prd_add | exists |
| gm-continue/SKILL.md | 13, 21 | gm.prd_delete | exists |
| gm-continue/SKILL.md | 21 | gm.prd_resolve | exists |
| gm-continue/SKILL.md | 21 | gm.unknown_* (prefix, not a verb) | family: add, list, resolve all exist |

Named files, all present: gm/skills/gm/WORKFLOWS.md (gm L14), gm/defaults/mcp.json (gm L22), gm/research/deep-research.md (gm L138), gm/tools/gm-continue-setup.mjs (gm-continue L8), gm/tools/ship.sh (dev L40), gm/src/skills.mjs (dev L44), gm/src/cli.mjs, gm/docs/index.html, gm/README.md, gm/DESIGN.md, gm/AGENTS.md (dev L4, L48).

Skill files: gm/skills/gm/SKILL.md, gm/skills/dev/SKILL.md and gm/skills/gm-continue/SKILL.md all exist. None is missing.

## 2. spawn.mjs usage text against the code

| check | usage text says | code does | result |
|---|---|---|---|
| read verb list | me, worlds, inbox, feed, invites, notifications, social, resolve, docs, rooms, logs, health, skill | READS has all 13 names | match |
| write verb list | publish, crew-ask, chat-room, dm, exec, asset-put, mod, push | WRITES plus push branch has all 8 | match |
| mod sub-verbs | install, update, list, status | MOD_VERBS identical | match |
| social sub-verbs | me, relation, who, met, personas, places, hidden | SOCIAL_READS identical | match |
| argument shapes | e.g. chat-room, exec, asset-put, docs, rooms, skill | arguments and defaults agree | match |
| token path | /config/.spawn/token, never printed | TOKEN_FILE default is the same path | match |
| no argument | usage printed, exit code not stated | prints usage to stderr, exit 0 (`process.exit(verb ? 2 : 0)`) | MISMATCH with the expected exit 2; usage text itself is right |
| unknown verb (`nosuchverb`) | usage | usage, exit 2 | match |
| bad args (`social bogus`, `skill`, `resolve`) | usage with a message | message, usage, exit 2 | match |

Live reads were not run. They are network calls that send the token, and the code-to-usage check does not need them. The offline error paths above were run. Writes were not run, not even as dry runs.

## 3. Endpoints and features not covered by spawn.mjs

Class: read (a GET or local read that spawn.mjs could wrap), gated write (needs a dry run and `--yes`), or out of scope (account doors). Size: S, M or L. Method marked "unverified" where the docs do not state it.

| endpoint or feature | source | class | size | reason |
|---|---|---|---|---|
| POST /api/agent/v1/token (signup) | savi | out of scope | - | account door |
| POST /api/agent/v1/token/revoke | savi | out of scope | - | account door, revokes the token |
| POST /api/agent/v1/signup | savi | out of scope | - | account door |
| POST /api/agent/v1/link-request | savi | out of scope | - | account door |
| POST /api/agent/v1/login-link | savi, docs | out of scope | - | account door, one-use browser sign-in |
| spawn login --invite / --reconnect | savi | out of scope | - | mints or relinks the token |
| PATCH /api/agent/v1/me {name, face} | savi | gated write | S | changes public identity |
| POST /api/agent/v1/games (create world) | savi, docs | gated write | M | creates a world billed to lanmower |
| DELETE /api/games/{appId} | savi | gated write | M | destructive; owner decision |
| GET /api/games/{appId}/comments | savi | read (method unverified) | S | list comments for review |
| GET /api/games/{appId}/folio, /folio/zip | savi | read | M | launch kit, zip download |
| GET /api/agent/v1/access | savi | read (method unverified) | S | access check |
| GET /api/agent/v1/pfp/{seed} | savi | read | S | image bytes, low value |
| GET /api/agent/v1/api | savi | read | S | API door index |
| GET /api/sdk/v1/{w}/db | savi | read (method unverified) | S | world database read, useful for debugging |
| POST /api/sdk/v1/{w}/report | savi | gated write (method unverified) | M | sends a report |
| POST /api/sdk/v1/{w}/assets/upload-target, then PUT with tempPath | savi, docs | gated write | M | assets above the 4.5 MB cap; asset-put covers small files only |
| GET /api/notifications/stream (SSE) | savi | read | M | long-lived stream; needs a streaming reader |
| POST /api/notifications/read | savi | gated write | S | marks notifications read |
| POST /api/notifications/{id}/decide | savi | gated write | S | answers a notification |
| POST /api/invites/{id}/accept | savi | gated write | S | joins a world |
| POST /api/social/report | savi | gated write | S | sends a report |
| POST /api/player/heartbeat | savi | gated write | S | presence ping, not needed by an agent |
| POST /api/session/grant/agent | savi | gated write | M | play grant, changes a session |
| /api/character/* (generate, picture, convert, equip, equip-model, reset) | savi | gated write | L | several paid generation doors |
| GET /api/character/jobs/{id} | savi | read | S | polls a character job |
| GET /llms.txt | savi, docs | read | S | public agent guide |
| spawn client where, players, logs, status, hear | savi | read | S | live-room state from the CLI |
| spawn client join, leave, exec, say | savi | gated write | L | stands bodies in the live room (budget 60 bodies); exec can persist |
| spawn client install-browser | savi | out of scope | S | local one-time install |
| spawn events (live inbox JSON lines) | savi | read | M | streaming output |
| spawn api <Type> [kind] | savi | read | S | spec shape at the engine version |
| spawn numbers | savi | read | S | numbers on each game |
| spawn preview | savi | gated write | M | runs the tree in a private room; no push, but changes live state |
| spawn bring <folder> | savi | gated write | M | writes files into a clone |
| git fetch of refs/notes/* (git log --notes=spawn) | savi, docs | read | S | the world's reading of each commit |
| Tome docs and skill doors | savi, docs | covered | - | docs and skill verbs |
| social who, met, places, hidden, relation, personas | savi | covered | - | social verb |

## Decision inputs for plan/27 Phase 2

1. spawn.mjs with no arguments exits 0, not 2; the usage text is correct. Size S. Fix the exit code, or change the plan's expectation.
2. No usage-text mismatch besides item 1. The 13 read and 8 write verbs match the code. Size S (none to fix).
3. gm skills reference no missing or renamed verb. gm.try and gm.verbs() are helpers outside the verb list; document them in the skill if the audit check reads that list. Size S.
4. Read gap: GET /api/notifications/stream (SSE). Size M.
5. Read gap: folio launch kit (GET folio and folio/zip). Size M.
6. Read gap: comments, access, db, pfp, api, llms.txt, character job status. Size S each; add as read verbs with no owner approval.
7. Read gap: spawn events, git notes fetch. Size M and S.
8. Gated write gap: PATCH /me identity. Size S. Needs a dry run and `--yes`.
9. Gated write gap: POST games (create world). Size M. Needs owner approval.
10. Gated write gap: DELETE game. Size M. Owner decision.
11. Gated write gap: large asset upload via upload-target. Size M. Needs a dry run and `--yes`.
12. Gated write gap: character generation doors. Size L. Paid; owner approval.
13. Gated write gap: spawn client join, leave, exec, say. Size L. Live writes stay blocked until the owner approves a first send.
14. Out of scope: the five account doors (token, token revoke, signup, link-request, login-link) and spawn login. No size needed.

## Phase 3 close-out

Accepted by the orchestrator: gm `88e50d3` (step 2) and bota `bd55bae` (step 3).

**Added**

- gm `tools/spawn.mjs`: read verbs `comments [appId]`, `api`, `llms` and `job <id>`. Each returned HTTP 200 live, except `job`, which was checked with a bad id (HTTP 404) to confirm its path. Bare `job` exits 2 with usage.
- Usage text updated to list them.

**Not added, and why**

- `access`: plain GET returns HTTP 400 `world_required`. With `?world=<worldId>` it returns 200, so it was added in gm `b964424` (local; push pending, see below) as a read verb that passes the world id.
- `pfp`: the live door returns SVG text, not binary. It stays excluded as low value for an agent, not because of its format.
- `db`: removed earlier, because GET returns 405.
- SSE notifications stream (audit item 4): needs a streaming reader, not a one-shot GET. Held.
- folio JSON and zip (item 5): zip is binary, and the JSON form is unverified. Held.
- `spawn events` and git notes fetch (item 7): `events` is a CLI streaming command, and notes fetch is a git operation. Held.

**Decisions**

- Item 1 (no-argument exit code): bare `spawn.mjs` exits 0 on purpose and prints usage as help. The exit-2 expectation in the audit was wrong, so no code change was made.
- Step 1 (skill mismatches): none found, so no gm skill changed.

**Not run**

- No live writes, deletions or account doors.
- The four held items above were not started.

## Phase 4 close-out

All four read-only gates pass. The first live send is held for the owner's test room.

1. Usage matches the verb table. Passes at gm `b4ef35a`, with the `access` line present.
2. Every skill reference resolves to a gm verb. Passes (section 1 above).
3. gm git status shows only intended files. Passes: the tree is clean, and local main matches origin `b4ef35a`.
4. Live read verbs re-run. `comments`, `api`, `llms` and `access` exit 0. `job` exits 2 with no id and 1 for a bad id (HTTP 404), as designed.

Not run: no live writes, deletions or account doors. The first live Spawn send (`chat-room`, `publish` or `exec`) is held until the owner names a test room.

## Files in this change set

Committed as bota `07ea551` (owner-approved push), with the Phase 3 step 3 update in the next bota commit:

- `plan/09-launch-hero-kits.md`: launch set is the plan/26 slice set (decision 48).
- `plan/10-remaining-hero-kits.md`: Noscope, Wojak and Forever added; Gothgirl, Ecce and Coomer removed.
- `plan/20-open-questions-sources-and-decisions.md`: decisions 48 to 54.
- `plan/27-gm-skills-and-spawn-plan.md`: Phase 2 approved; open questions answered.
- `plan/28-owner-decision-sheet.md`: status line for the approved items.
- `plan/29-phase1-audit.md`: audit and Phase 3 status.
