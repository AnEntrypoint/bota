# 20. Open questions, sources and decisions
### Decisions made

| # | Decision | Reason |
| --- | --- | --- |
| 1 | Anonymous Blade item renamed Anon Mask. The Helios ability Anonymous Dagger is renamed Marble Dagger. The Helios invisibility ability is renamed Mirror Shade Mode. | Anon Mask names an invisibility item. Marble Dagger names a marble dagger. Mirror Shade Mode names the invisibility. |
| 2 | Pro Plan is the one ultimate upgrade per hero. | Clear name for an upgrade item |
| 3 | Orbs do not stack. | Keeps attack modifiers simple |
| 4 | Clout is the only audience resource. | Keeps one readable currency |
| 5 | Seven boosts, Demand Boost included. | Readable boost pool |
| 6 | Roster is 112, Scalper included. | Matches the roster target |
| 7 | Fad vocabulary in voice lines, item flavor and marketing copy is generic usage only: no brand names, named creators, franchise characters or owned catchphrases. The six roster labels Zyzz, Uber, Crossfit, Starwarskid, Rickroll and Frogger are listed for the record. Hero and ability labels are outside this scope. | Lets phrases rotate each patch while the roster stays stable |
| 8 | Every ability in sections 9 and 10 has a Brainrot name. Original hero, ability and item names live only in internal/parity-map.md and in this decision record; decision 22 keeps them out of shipped text. | Original names stay out of shipped text |
| 9 | Clout drives Reach, reveal and mood only, never a stat. Late-game Clout carry mood, Breaking News, stage camps and signature mechanics keep to that rule. | Keeps the one-currency rule from section 6 |
| 10 | Generic classic-MOBA terms are renamed to Brainrot names (mapping in internal/parity-map.md). Creep, lane, jungle and tower stay generic usage. | Uniqueness |
| 11 | Every new number is UNVERIFIED until a playable build exists. | Matches the balance rule in the engine repo AGENTS.md |
| 12 | Demand Boost changes from cooldown and mana cuts to Reach +100. | Keeps it on the Clout identity |
| 13 | Spectators never vote on play. Reactions are cut (decision 28). | Ranked integrity |
| 14 | Starting gold is 600 (UNVERIFIED). | The plan is the design source; the engine number is recalled, not confirmed, and tracked in plan/25 section 4 |
| 15 | Ultimates unlock at 6, 11 and 16. The engine format doc's 6, 12 and 18 change to match. | The plan is the design source |
| 16 | The LIVE dot is #6A1FD1 with a white ring. | Keeps it apart from Clout's #A35CFF |
| 17 | Item costs in section 11 are the cost bands the roster uses, and only the balance pass changes them. | One place to change item costs |
| 18 | Drain Blade: 1,600 gold, 12% attack lifesteal for 6 s after a hit. UNVERIFIED. | Its tier 3 entry had no row |
| 19 | The formerly tag reads "formerly Guest" and shows only on the death recap or victory screen. No client storage. | Removes an invented name pool and new client state |
| 20 | Power tier letters are withdrawn until a playable build exists. The flag list and the test-first list stay. | Tier A held 64 of 112 heroes, so the letters measure nothing |
| 21 | No classic number is checked against 6.88g until the archive is available. Each stays UNVERIFIED. | Matches the rule in the engine repo AGENTS.md |
| 22 | The parity map stays internal: tracked in git, never copied into plan/, the site or a pack. | Keeps original names out of shipped text |
| 23 | The engine build is not started in this round. The first-playable slice (plan/26) is the next task, and it starts once the repo is synced (the local checkout and origin/main matched on 2026-10-27). | A build needs the repo state fixed first |
| 24 | Plan distances are game units: 1 game unit is 125/8 milli-units. | Removes the last unit ambiguity for the data generator |
| 25 | Props marked (worn), (no held prop) or otherwise thin are taken from a worn item or a pose as drawn. | No owner confirmation is pending; the default is recorded here so plan/22 has no open item. |
| 26 | Stat Boost and Decoy Lots are cut. Leftover ability points after the four skills are maxed stay unspent. | Stat Boost has no rival use for leftover points, and Decoy Lots have no classic job (plan/02 rules 2 and 3). |
| 27 | Counter coverage means at least one hard counter per archetype, read from its Hard counter cell. Soft counters are not a separate rule. | The archetype table has no soft-counter column, and four archetype rows have no weak entry beyond their hard counter. |
| 28 | Spectator reactions are cut. Decision 13 keeps only its no-vote clause. Talents, backpack, neutral items, disable duration and sustain gain plan/02 rows; Chat Check and Demand Boost use the vision and map-pressure rows. | Spectator reactions have no classic job (plan/02 rules 2 and 3), as with Decoy Lots in decision 26. |
| 29 | Breaking News maps to the Capture objective row in plan/02. | Breaking News is a capture objective with its own cost, the contest, as plan/02 rule 3 requires. |
| 30 | The surrender vote has a plan/02 Surrender row: a vote that ends the match. | Decisions 26 and 28 cut systems with no classic job; this one has a classic forfeit, so it stays with a cost. |
| 31 | Showboat's level-15 talent raises Reach by 25 in place of the undefined Clout cap. | Reach is defined in plan/06 Clout rules; Clout cap is not defined anywhere. |
| 32 | Item classic jobs stay in internal/parity-map.md; the balance pass checks each item's Mapped job there. | A 50-row Job column would copy the internal mapping into the plan, against decision 22. |
| 33 | Draft maps to a plan/02 Draft row, named in the draft chapter. | Drafting holds a classic job (plan/02 rule 3), and the pick order has a cost on each side (rule 2). |
| 34 | The premise is a commodity market, not posting. Go Viral becomes Bull Run, Repost becomes Resell, Original Post becomes Exchange, Screenshot becomes Snapshot, Feed becomes Market, Algorithm becomes Demand, Thread becomes Ticker, Ratio becomes Markdown, Meme becomes Fad. Clout stays the audience resource. Coffee and intelligence are the funniest goods. | The user asked for less lame humour and kept Clout. Decisions 4 and 9 are unchanged. |
| 35 | Front Runner's icon is a choice: its heroes may hide it for 20 s by giving up Reach +50 for that window (UNVERIFIED). | The leader had no choice, only an icon it could not avoid. |
| 36 | Tier 4 finished items are sold at the Back Alley Shop, with the Tier 2 and Tier 3 items. | Tier 4 items had prices but no sale point. |
| 37 | A hard disable is a stun, hold, sleep, fear, charm, polymorph, cyclone or petrify; silence, root, slow, blind, disarm and taunt are soft. | C6 and the resell trigger need one definition. |
| 38 | Passives that reflect damage to an attacker (Rolling Back, Receipt Reflect, Sad Clapback, Chunky Shell, Lamp Reflect, Reply All, and the Handlebar Appeal and Bulwark Reflect 10% talents) share one per-hit reflect cap, value UNVERIFIED. | Eight reflects need the same rule. |

### Open questions

No design question in sections 1 to 24 and 26 is open: each is closed by a decision above or by a value in the body. Section 25 records engine and data questions; archive access is tracked as decision 21, not as an open question.

### Sources

The original-name parity map is decision 22. Numbers are set in the balance pass.
