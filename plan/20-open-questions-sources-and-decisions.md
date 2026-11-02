# 20. Open questions, sources and decisions
### Decisions made

| # | Decision | Reason |
| --- | --- | --- |
| 1 | Renames of items and abilities are listed in internal/parity-map.md. Anon Mask, Marble Dagger and Mirror Shade Mode are the Brainrot names. | Anon Mask names an invisibility item. Marble Dagger names a marble dagger. Mirror Shade Mode names the invisibility. |
| 2 | Pro Plan is the one ultimate upgrade per hero. | Clear name for an upgrade item |
| 3 | Orbs do not stack. | Keeps attack modifiers simple |
| 4 | Clout is the only audience resource. | Keeps one readable currency |
| 5 | Seven boosts, Demand Boost included. | Readable boost pool |
| 6 | Roster is 112, Scalper included. | Matches the roster target |
| 7 | Fad vocabulary in voice lines, item flavor and marketing copy is generic usage only: no brand names, named creators, franchise characters or owned catchphrases. The six roster labels Zyzz, Uber, Crossfit, Starwarskid, Rickroll and Frogger are listed for the record, and two platform formats are kept as gags: Nobody: / Me: (gag 18) and [deleted] (gag 11). Hero and ability labels are outside this scope. | Lets phrases rotate each patch while the roster stays stable |
| 8 | Every ability in sections 9 and 10 has a Brainrot name. Original hero, ability and item names live only in internal/parity-map.md; decision 22 keeps them out of shipped text. | Original names stay out of shipped text |
| 9 | Clout drives Reach, reveal and mood only, never a stat. Late-game Clout carry mood, Breaking News, stage camps and signature mechanics keep to that rule. | Keeps the one-currency rule from section 6 |
| 10 | Generic classic-MOBA terms are renamed to Brainrot names (mapping in internal/parity-map.md). Creep, lane, jungle and tower stay generic usage. | Uniqueness |
| 11 | A new number with a source is UNVERIFIED until a playable build exists. A new number with no source is GUESS with its reason (decision 42). | Keeps new numbers from passing as checked values |
| 12 | Demand Boost changes from cooldown and sigma cuts to Reach +100 (UNVERIFIED). | Keeps it on the Clout identity |
| 13 | Spectators never vote on play. | Ranked integrity |
| 14 | Starting gold is 600 (UNVERIFIED). | The plan is the design source. The engine repo holds 875 (scenarios/moba/economy.osd); the plan keeps 600 until the balance pass sets it. |
| 15 | Ultimates unlock at 6, 11 and 16. The engine format doc already gives 6, 11 and 16. | The plan is the design source |
| 16 | The LIVE dot is #6A1FD1 with a white ring. | Keeps it apart from Clout's #A35CFF |
| 17 | Item costs in section 11 are the cost bands the roster uses, and only the balance pass changes them. | One place to change item costs |
| 18 | Drain Blade: 1,600 gold, 12% attack lifesteal for 6 s after a hit. UNVERIFIED. | Its tier 3 entry had no row |
| 19 | The formerly tag reads "formerly Guest" and shows only on the death recap or victory screen. No client storage. | Removes an invented name pool and new client state |
| 20 | Power tier letters are withdrawn until a playable build exists. The flag list and the test-first list stay. | Tier A held 64 of 112 heroes, so the letters measure nothing |
| 21 | No classic number is checked against 6.88g until the archive is available. Each stays UNVERIFIED. | Keeps classic numbers from passing as checked values |
| 22 | The parity map stays internal: tracked in git, never copied into plan/, the site or a pack. | Keeps original names out of shipped text |
| 23 | The engine build starts after the first-playable slice (plan/26), which is the next build task. | A build needs the slice scope fixed first |
| 24 | Plan distances are game units: 1 game unit is 125/8 milli-units. | Removes the last unit ambiguity for the data generator |
| 25 | Props marked (worn), (no held prop) or otherwise thin are taken from a worn item or a pose as drawn. | No owner confirmation is pending; the default is recorded here so plan/22 has no open item. |
| 26 | Stat Boost and Decoy Lots are cut. Leftover ability points after the four skills are maxed stay unspent. | Stat Boost has no rival use for leftover points, and Decoy Lots have no classic job (plan/02 rules 2 and 3). |
| 27 | Counter coverage means at least one hard counter per archetype, read from its Hard counter cell. Soft counters are not a separate rule. | The archetype table has no soft-counter column, and four archetype rows have no weak entry beyond their hard counter. |
| 28 | Spectator reactions are cut. Decision 13 keeps only its no-vote clause. Talents, backpack, neutral items, disable duration and sustain gain plan/02 rows; Chat Check and Demand Boost use the vision and map-pressure rows. | Spectator reactions have no classic job (plan/02 rules 2 and 3), as with Decoy Lots in decision 26. |
| 29 | Breaking News maps to the Capture objective row in plan/02. | Breaking News is a capture objective with its own cost, the contest, as plan/02 rule 3 requires. |
| 30 | The surrender vote has a plan/02 Surrender row: a vote that ends the match. | Decisions 26 and 28 cut systems with no classic job; this one has a classic forfeit, so it stays with a cost. |
| 31 | Showboat's level-15 talent raises Reach by 25 (UNVERIFIED), after the Clout-term cap. | plan/06 Clout rules cap the Clout term of Reach at 600; the talent adds Reach after that cap. |
| 32 | Item classic jobs stay in internal/parity-map.md; the balance pass checks each item's Mapped job there. | A 50-row Job column would copy the internal mapping into the plan, against decision 22. |
| 33 | Draft maps to a plan/02 Draft row, named in the draft chapter. | Drafting holds a classic job (plan/02 rule 3), and the pick order has a cost on each side (rule 2). |
| 34 | The premise is a commodity market, not posting. Go Viral becomes Hype Spike, Repost becomes Resell, Original Post becomes Exchange, Screenshot becomes Snapshot, Feed becomes Market, Algorithm becomes Demand, Thread becomes Ticker, Ratio becomes Markdown, Meme becomes Fad. Clout stays the audience resource. Coffee and intelligence are the funniest goods. | The commodity-market premise is funnier than posting, and Clout stays the audience resource. Decisions 4 and 9 are unchanged. |
| 35 | Front Runner's icon is a choice: its heroes may hide it for 20 s by giving up Reach +50 for that window (UNVERIFIED). | The leader had no choice, only an icon it could not avoid. |
| 36 | Tier 4 finished items are sold at the Back Alley Shop, with the Tier 2 and Tier 3 items. | Tier 4 items had prices but no sale point. |
| 37 | A hard disable is a stun, hold, sleep, fear, charm, polymorph, cyclone or petrify; silence, root, slow, blind, disarm and taunt are soft. | C6 and the resell trigger need one definition. |
| 38 | Passives that reflect damage to an attacker (Rolling Back, Receipt Reflect, Sad Clapback, Chunky Shell, Lamp Reflect, Reply All, Zip Tie Network, and the level-20 Handlebar Appeal (Frogger) and Bulwark Reflect 10% talents in plan/21) share one per-hit reflect cap of one quarter of the hit, value UNVERIFIED. | Nine reflects need the same rule. |
| 39 | The launch set is the 24 heroes with kits in plan/09, Frogger and Chudjak included. Mallcop and Rageguy are remaining heroes with kits in plan/10. The plan/23 voice, the plan/25 heroes.tsv row and the plan/26 slice follow this set. | plan/09 holds the kits and plan/21 the talents the engine data is built on. |
| 40 | The resource is named sigma in every design doc: prose, table column names and character text. Original names stay in internal/parity-map.md. Engine identifiers live in the engine repo and change only when its data format does. | Owner request for a full rename. Sigma is the Brainrot resource word; the rename removes the original resource name from shipped text. |
| 41 | The energy-drink item is named Coffee. Brand names stay out of shipped text under decision 7; the parity map keeps the original name. | Owner flagged the brand as a trademark risk and chose Coffee as the replacement. |
| 42 | GUESS marks a value, name or slot choice with no source in 6.88g, the repo or the web, and its row gives the reason. UNVERIFIED marks a value that has a source not yet checked. | Keeps a design guess apart from a source-backed value that is not checked yet. |
| 43 | The spike is named Hype Spike and the state is named Hyped. Crypto terms stay out of shipped text. | Owner: crypto is lame; the spike and the state keep their mechanics. |
| 44 | Open Market is the casual mode with no bans. Players pick in seat order, one at a time, and a later seat picks from the heroes the earlier seats left (UNVERIFIED). | Gives the free pick a cost on each side (plan/02 rule 2), as decision 33 requires of every draft. |

### Open questions

No design question in sections 1 to 24 and 26 is open: each is closed by a decision above or by a value in the body. Section 25 records engine and data questions; archive access is tracked as decision 21, not as an open question.
