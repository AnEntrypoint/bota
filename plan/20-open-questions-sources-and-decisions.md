# 20. Open questions, sources and decisions
### Decisions made

| # | Decision | Reason |
| --- | --- | --- |
| 1 | Anonymous Blade item renamed Anon Mask. The Helios ability Anonymous Dagger is renamed Marble Dagger. The Helios invisibility ability is renamed Mirror Shade Mode. | Anon Mask names an invisibility item. Marble Dagger names a marble dagger. Mirror Shade Mode names the invisibility. |
| 2 | Pro Plan is the one ultimate upgrade per hero. | Clear name for an upgrade item |
| 3 | Orbs do not stack. | Keeps attack modifiers simple |
| 4 | Clout is the only audience resource. | Keeps one readable currency |
| 5 | Seven boosts, Algorithm Boost included. | Readable boost pool |
| 6 | Roster is 112, Scalper included. | Matches the roster target |
| 7 | Meme vocabulary in voice lines, item flavor and marketing copy is generic usage only: no brand names, named creators, franchise characters or owned catchphrases. The six roster labels Zyzz, Uber, Crossfit, Starwarskid, Rickroll and Frogger are listed for the record. Hero and ability labels are outside this scope. | Lets phrases rotate each patch while the roster stays stable |
| 8 | Every ability in sections 9 and 10 has a Brainrot name. Original hero, ability and item names live only in internal/parity-map.md and in this decision record; they never appear in shipped text or elsewhere in the plan. | Original names stay out of shipped text |
| 9 | Clout drives Reach, reveal and mood only, never a stat. Late-game Clout carry mood, Breaking News, stage camps and signature mechanics keep to that rule. | Keeps the one-currency rule from section 6 |
| 10 | Generic classic-MOBA terms are renamed to Brainrot names (mapping in internal/parity-map.md). | Uniqueness |
| 11 | Every new number is UNVERIFIED until a playable build exists. | Matches the balance rule in /workspace/oscraft/AGENTS.md |
| 12 | Algorithm Boost changes from cooldown and mana cuts to Reach +100. | Keeps it on the Clout identity |
| 13 | Spectators can react but never vote on play. | Ranked integrity |
| 14 | Starting gold is 600. The engine docs say 625 and need changing to match. | The plan is the design source; the engine number is recalled, not confirmed |
| 15 | Ultimates unlock at 6, 11 and 16. The engine format doc's 6, 12 and 18 change to match. | The plan is the design source |
| 16 | The LIVE dot is #6A1FD1 with a white ring. | Keeps it apart from Clout's #A35CFF |
| 17 | Cost bands in section 11 are set to the costs the roster uses. Costs are unchanged. | The roster costs are the fixed point |
| 18 | Drain Blade: 1,600 gold, 12% attack lifesteal for 6 s after a hit. UNVERIFIED. | Its tier 3 entry had no row |
| 19 | The formerly tag reads "formerly Guest" and shows only on the death recap or victory screen. No client storage. | Removes an invented name pool and new client state |
| 20 | Power tier letters are withdrawn until a playable build exists. The flag list and the test-first list stay. | Tier A held 64 of 112 heroes, so the letters measure nothing |
| 21 | No classic number is checked against 6.88g until the archive is available. Each stays UNVERIFIED. | Matches the rule in /workspace/oscraft/AGENTS.md |
| 22 | The parity map stays internal: tracked in git, never copied into plan/, the site or a pack. | Keeps original names out of shipped text |
| 23 | The engine build is not started in this round. The first-playable slice (plan/26) is the next task, and it starts once the repo is synced (the local checkout and origin/main matched on 2026-10-27). | A build needs the repo state fixed first |
| 24 | Plan distances are game units: 1 game unit is 125/8 milli-units. | Removes the last unit ambiguity for the data generator |
| 25 | Props marked (worn), (no held prop) or otherwise thin are taken from a worn item or a pose as drawn. | No owner confirmation is pending; the default is recorded here so plan/22 has no open item. |
| 26 | Stat Boost and Decoy Posts are cut. Leftover ability points after the four skills are maxed stay unspent. | Stat Boost has no rival use for leftover points, and Decoy Posts have no classic job (plan/02 rules 2 and 3). |
| 27 | Counter coverage means at least one hard counter per archetype, read from its Hard counter cell. Soft counters are not a separate rule. | The archetype table has no soft-counter column, and four archetype rows have no weak entry beyond their hard counter. |

### Open questions

No design question in sections 1 to 24 and 26 is open: each is closed by a decision above or by a value in the body. Section 25 records engine and data questions; only archive access remains open.

### Sources

Classic-rule reference pages and the original-name parity map are kept outside the plan, in internal/parity-map.md. Numbers are set in the balance pass.
