# Bota ambiguous row resolution (survey 2026-11-06, owner decisions 2026-11-07)

Input: /tmp/bota-needed-props.json, 40 rows, 16 with unambiguous:false. The survey records the local evidence an owner decision would use and proposes slugs only where a local source names the thing verbatim. All 16 rows are owner-decided (2026-11-07): trend-costumes and trend-death-husks by the one-mesh decisions in the Owner decisions section, the other 14 by the fast-path decisions A3, B2, C3, C2 and D1 recorded there. Every decision yields 0 new GLBs. No generation is performed.

Scope and constraints: all evidence comes from /workspace/bota files read with gm.grep and gm.read_file. The 2026-11-06 survey was read-only: no network, no .env read, no repo edits, commits or pushes. /tmp/bota-needed-props.json is not rewritten. No numeric count is expanded into slugs. Every proposed slug is transcribed from a name that appears in the cited line. Where a category has only a count, the row says no slugs and states the decision that is needed.

## Global blockers (apply to all 16 rows)

- plan/18-asset-manifest-and-audio.md:3 — Counts and sizes in this chapter are UNVERIFIED until the asset list is built. No asset list exists in /workspace/bota; the only other mention is plan/18:119, Counts are estimates until the asset list is locked.
- plan/20-open-questions-sources-and-decisions.md:16 — decision 11: A new number with a source is UNVERIFIED until a playable build exists. A new number with no source is GUESS with its reason (decision 42).
- plan/20-open-questions-sources-and-decisions.md:26 — decision 21: No classic number is checked against 6.88g until the archive is available. Each stays UNVERIFIED.
- plan/25-engine-data-plan.md:20 — No Clout, Trend, boost, Markdown, Resell, Stan, draft-mode or archetype data exists in the engine or the packs. The engine cannot arbitrate these counts.
- plan/25-engine-data-plan.md:16 and :17 name engine-repo tables (doodads-688g.tsv, doodad-types-688g.tsv, slot-models.tsv). They are outside /workspace/bota and hold original-game doodad types, not Brainrot prop names. Using them needs an owner decision and a read of another repo, out of scope here.
- plan/29-phase1-audit.md:172-173 — GUESS: 73 tags. UNVERIFIED: 110 tags. Source URLs: 0. These are plan status tags, not prop counts, but they show the plan's unknowns are held by the orchestrator.

Resolution order, cheapest first: (1) build the asset list named in plan/18:3, the single source that resolves the count-only rows; (2) decide model-vs-instance accounting for towers, Content Mills, Stockpile and Safe Spots; (3) decide scope, since rigged unit/NPC models, interface dioramas, cosmetic plinths and overlays are not static props; (4) the costume and husk mesh decisions are recorded above, and mega creeps are decided as runtime scale variants below; (5) classic-number checks stay blocked on the 6.88g archive (plan/20:26).

## Owner decisions (2026-11-07)

| row | decision | new GLBs |
| --- | --- | --- |
| trend-costumes | one base mesh with eight material swaps | 0 |
| trend-death-husks | one desaturated mesh with modifier materials | 0 |

The two decisions replace the guessed visual forms and their tags under plan/20 decision 11 and decision 42. No GLB, model, material or prop file is generated. The neededCount 8 rows stay as survey input; each decision yields one mesh with eight material variants. The remaining 14 rows are decided below; the per-row evidence sections keep their survey text.

### Fast-path decisions for the other 14 rows (owner, 2026-11-07)

Source: [fast-path dry run](/tmp/hy3d-bota-held-fast-path-dry-run.md) (6438 bytes, sha256 9723ef7bb047587a6d16502a87ae208a83145c725ac9d81d5d2262cf0a399bec) and /tmp/hy3d-bota-held-decision-memo.md (sha256 39a8acd72be260c4bf583181f9095c2d3d4784b1180bb27bfa41051317a029e9). All 14 rows are decided with 0 new GLBs, 0 relay jobs and 0 bytes. No GLB, response.json, manifest, roster or script is created, deleted or changed; the two prop manifests and the 63 generated GLBs (2,000,948,996 bytes) are unchanged.

| row | decision | meaning | new GLBs |
| --- | --- | --- | --- |
| terrain-kits-and-props | A3 | defer the 120 unnamed props until plan/18's asset list exists; 3 kits already generated | 0 |
| world-models-shop-and-drop | A3 | defer the 15 unnamed world models until plan/18's asset list exists; 14 named candidates already generated | 0 |
| out-of-bounds-marginalia | A3 | defer the 9 unnamed vignettes until plan/18's asset list exists; marginalia-no-signal-tree already generated | 0 |
| towers | B2 | reuse tower-tier1..4 (4 GLBs) for all 22 placements; 8 vs 22 is model vs instance | 0 |
| content-mills | B2 | reuse content-mill-melee/ranged (2 GLBs) for all 12 placements | 0 |
| loading-dioramas | C3 | 2D/interface scope, not a prop mesh; conflicting 24 vs 6 counts stay UNVERIFIED | 0 |
| stockpile | B2 | per-team vs intact/destroyed is placement/state, not a generation | 0 |
| lane-creeps | C2 | rigged unit scope; creep-melee/ranged/siege already generated | 0 |
| mega-creeps | C2 | runtime scale variants; 0 new GLBs | 0 |
| stan-buffed-overlays | C3 | decal/VFX scope; stan-sign is a world model, not an overlay | 0 |
| jungle-camp-creatures | C2 | NPC unit scope; all 12 named models already generated | 0 |
| shop-npc-the-plug | D1 | duplicate held row, generated exactly once as an explicit prop; no second generation | 0 |
| safe-spot | D1 | plan/26 cut list defers Safe Spots; 4 is 2 per team, no shape | 0 |
| cosmetic-plinth | D1 | no count, shape or asset row; 2D icon style rule only | 0 |

Rows 3 and 4 (trend-costumes, trend-death-husks) carry A3 in the dry run. The owner's earlier one-mesh decisions in commit 5a9b7ff resolve more, so by the rule of deciding by most progress they stand in the two-row table above; both also yield 0 new GLBs. All 16 held rows are therefore decided.

## Per-row evidence (16)

### 1. terrain-kits-and-props — neededCount 3 kits / 120 props

Unresolved: the 3 kits are named but the 120 individual props are not; both counts are UNVERIFIED. Primary citation plan/18-asset-manifest-and-audio.md:58; secondary plan/04-map.md:3.

Local evidence:
- plan/18:58 — Terrain kits and props | 3 kits, 120 props | Lanes, jungle, river |. The Notes column spells out Lanes, jungle, river as the three kit names.
- plan/18:3 — counts are UNVERIFIED until the asset list is built.
- plan/04:15 — Three lanes per team: top, mid and bottom. Lane Stalls sit at the lane mouths and sell basic components.
- plan/04:19 — The river splits the map. It holds the two boost spots, which spawn every 2 min (section 12), and the Trend pit.
- plan/04:20 — Shallow crossings let heroes cross the river at fixed points only.
- plan/04:26-28 — jungle camp table: Primary 2 hard, 2 medium, 1 small; Secondary 1 hard, 1 elder; Near Back Alley Shop 1 hard.
- plan/04:34 — Out-of-bounds marginalia (ten static vignettes) sit on the map edge.
- plan/16:24 — A creep sits on grass with eyes shut. A lone tree carries a no signal glyph. This is the only individually described map prop in local source.
- plan/04:3 — Numbers in this chapter are UNVERIFIED.
- plan/25:16-17 — names engine-repo doodad tables, no Brainrot prop names.

What would resolve it: the plan/18 asset list, or an owner decision to treat the three kit names as the generation units and defer the 120 props.

Proposed slugs (explicit names only): terrain-kit-lanes, terrain-kit-jungle, terrain-kit-river, from Lanes, jungle, river in plan/18:58. No slugs for the 120 props: no source names any of them, so none are invented.

Status: decided — owner, 2026-11-07; A3, 0 new GLBs.

### 2. world-models-shop-and-drop — neededCount 15

Unresolved: 15 unnamed world models. The plan names many items but never maps any of them to these 15. Primary citation plan/18-asset-manifest-and-audio.md:38.

Local evidence:
- plan/18:38 — World models, shop and drop | 15 | 500 to 2,000 tris, 512² texture |.
- plan/18:37 — Item icons | 50 | 88 × 64 PNG, 176 × 128 master |. These are 2D and excluded.
- plan/11:9 — Drop-on-death items: Hot Take, Unironic and Gem of Subtext. Their holder drops them on death, visible to all.
- plan/11:8 — The Trend's Snapshot (section 12) and Coffee (section 21) cannot be sold.
- plan/12:57 — The Trend drops Coffee on its second kill and every kill after (UNVERIFIED).
- plan/21:111 — Coffee cannot be sold. Chug it to restore 700 HP and 300 sigma over 4 s. One can per drop.
- plan/21:57 — Neutral items drop from jungle camps. A hero gets one choice of three. A new neutral replaces the old one.
- plan/21:62-65 — the 12 named neutral items: Ticker Pin, Crumb Pouch, NPC Badge; Echo Ring, Stan Sign, Hot Mic; Ding Bell, Thick Cloak, Cancel Mask; Eternal Ticker, Vintage Lot, Long Tail.
- plan/26:53 — Neutral items | None | Section 21 | Tested after camps are proven. The cut list defers them from the first playable.
- plan/18:3 — UNVERIFIED until the asset list is built.

What would resolve it: an owner decision mapping the 15 to named items. The named items below are candidates, not a mapping and not derived from the number 15.

Proposed slugs (explicit names only; kebab-cased plan names): hot-take-unironic, gem-of-subtext (plan/11:9); ticker-pin, crumb-pouch, npc-badge, echo-ring, stan-sign, hot-mic, ding-bell, thick-cloak, cancel-mask, eternal-ticker, vintage-lot, long-tail (plan/21:62-65). Coffee is named in plan/12:57 and plan/21:111 but already has the coffee-drop row in the JSON; do not duplicate it. stan-sign is a neutral item name (plan/21:63, plan/23:97), not the Stan overlay in row 12.

Status: decided — owner, 2026-11-07; A3, 0 new GLBs.

### 3. trend-costumes — neededCount 8

Decided (owner, 2026-11-07): one base mesh with eight material swaps, 0 new GLBs. The 8 costumes still have no costume names. Primary citation plan/18-asset-manifest-and-audio.md:49; secondary plan/12-neutrals-boosts-the-trend-and-snapshot.md:66.

Local evidence:
- plan/18:49 — The Trend costumes | 8 | Swappable modifier meshes. Silhouette stays constant. |
- plan/18:48 — The Trend base model | 1 | Blank boss built from stacked banners |.
- plan/12:50 — A blank boss built from stacked ticker banners. Every number in this block is UNVERIFIED.
- plan/12:66 — Eight modifiers rotate each patch. Two are offered per kill.
- plan/12:70-77 — the eight modifier names: Cast Rush, Cooldown Sale, Study Tax, Sprint Bonus, Channel Haste, Lounge Discount, Demand Tide, Solo Hustle.
- plan/21:132 — The Trend modifier pool (section 12).
- plan/21:134 — The cosmetic skin theme: costumes, plinths and the Trend banner.
- plan/26:51 — Trend modifiers | 2 | 8 | Compare two before adding more.
- plan/18:51 explicitly says only the husks, not the costumes, are one per modifier.

Decision (owner, 2026-11-07): one base mesh with eight material swaps; silhouette stays constant, 0 new GLBs. The guess and UNVERIFIED tags on the costume form are closed under plan/20 decision 11 and decision 42.

Proposed slugs: none. No local source names a costume. The eight names above are gameplay modifiers; using them as costume slugs would be an invented mapping. No slugs are invented from the count 8.

Status: decided — owner, 2026-11-07; one base mesh with eight material swaps, 0 new GLBs.

### 4. trend-death-husks — neededCount 8

Decided (owner, 2026-11-07): one desaturated mesh with modifier materials, 0 new GLBs. The 8 husks, one per modifier, still have no husk names. Primary citation plan/18-asset-manifest-and-audio.md:51; secondary plan/16-humor-and-tone.md:23.

Local evidence:
- plan/18:51 — Trend death husks | 8 | One per modifier. Desaturated, no health bar. |
- plan/16:23 — The expired modifier's costume lies in the pit as a glyph-splintered husk until the Trend respawns. The husk is one desaturated mesh with modifier materials.
- plan/18:49 — costumes are swappable modifier meshes whose silhouette stays constant.
- plan/12:66 — eight modifiers rotate each patch.
- plan/18:3 — counts are UNVERIFIED until the asset list is built.

Decision (owner, 2026-11-07): one desaturated mesh with modifier materials, 0 new GLBs. The guess tag under plan/20 decision 42 is removed.

Proposed slugs: none. No source names a husk; modifier names are not husk names. No slugs are invented from the count 8.

Status: decided — owner, 2026-11-07; one desaturated mesh with modifier materials, 0 new GLBs.

### 5. out-of-bounds-marginalia — neededCount 10

Unresolved: 10 static vignettes, only one described, none named. Primary citation plan/18-asset-manifest-and-audio.md:66; secondary plan/04-map.md:34.

Local evidence:
- plan/18:66 — Out-of-bounds marginalia | 10 | Static vignettes |.
- plan/04:34 — Out-of-bounds marginalia (ten static vignettes) sit on the map edge. They never block movement and never hide a unit. Count in section 18.
- plan/16:24 — A creep sits on grass with eyes shut. A lone tree carries a no signal glyph. [GUESS] | Map edge | Camera at edge | Static and silent.
- plan/02-vision-and-pillars.md:13 — rule 4 (Off the read path) — Jokes live in tooltips, announcers, idle animations and marginalia. They never hide a gameplay signal.
- plan/04:3 — Numbers in this chapter are UNVERIFIED.

What would resolve it: owner-supplied names or descriptions for the other nine, or a decision to reuse one vignette mesh. The single described vignette already has the JSON row marginalia-no-signal-tree; that slug is a descriptive label coined for the row, not a source name.

Proposed slugs: none. No source names any vignette, so no slugs are invented from the count 10.

Status: decided — owner, 2026-11-07; A3, 0 new GLBs.

### 6. towers — conflicting neededCount 8 vs 22

Unresolved: plan/18 counts 8 unique tower models (four tiers across two teams); plan/03 places 11 towers per side, 22 instances. Both UNVERIFIED. Primary citation plan/18-asset-manifest-and-audio.md:59; secondary plan/03-core-loop-and-win-condition.md:13.

Local evidence:
- plan/18:59 — Towers | 8 | Four tiers across two teams. Tier read by size and stacked stamps. |
- plan/03:10 — Tier 1 tower | 3 (one per lane) | Armor aura for allied heroes: +1.
- plan/03:11 — Tier 2 tower | 3 | Armor aura: +3. Invulnerable until its T1 falls.
- plan/03:12 — Tier 3 tower | 3 | Armor aura: +3. Damage equal to T2.
- plan/03:13 — Tier 4 towers | 2 (at the Stockpile) | Invulnerable until a T3 falls in any lane.
- plan/03:20 — Tower HP: T1 1,300, T2 1,600, T3 1,600, T4 2,200.
- plan/05:16 — Tower | Team gold per tier (about 160, 200, 240, 280).
- plan/17:37-38 — Ally team, Morning Market | #2E8BFF | Light-value structures. Teams also differ in value. / Enemy team, Late Night Market | #FF8A1F | Dark-value structures.
- plan/17:48 — Every color signal on a unit or ability carries a shape. Ally creeps have rounded hoods. Enemy creeps have angular hoods. Team colour on structures carries value instead.

What would resolve it: an owner decision on model-vs-instance accounting. plan/17:48 is evidence that team difference may be a value or material treatment rather than a second mesh, which would make 4 tier models the likely unit. A team-qualified slug would be a derived combination, not an explicit name, so none is proposed.

Proposed slugs (explicit tier names only): tower-tier1, tower-tier2, tower-tier3, tower-tier4, from Tier 1 tower through Tier 4 towers in plan/03:10-13. No per-instance or per-team slugs.

Status: decided — owner, 2026-11-07; B2, 0 new GLBs.

### 7. content-mills — conflicting neededCount 4 vs 12

Unresolved: plan/18 counts 4 (melee and ranged, two teams); plan/03 says 6 per side (two per lane, melee and ranged), 12 instances. Primary citation plan/18-asset-manifest-and-audio.md:60; secondary plan/03-core-loop-and-win-condition.md:14.

Local evidence:
- plan/18:60 — Content Mills | 4 | Melee and ranged, two teams |.
- plan/03:14 — Content Mills | 6 (two per lane, melee and ranged) | A lane with both its Content Mills down spawns Mega creeps; a destroyed mill respawns after 5 min (UNVERIFIED) |.
- plan/03:15 — All six Content Mills down | n/a | Mega creeps spawn in all three lanes until a mill respawns.
- plan/04:15 — Three lanes per team: top, mid and bottom. This explains 2 per lane × 3 lanes = 6 per side.
- plan/17:48 — team colour on structures carries value instead.
- plan/03:3 — Numbers in this chapter are UNVERIFIED.

What would resolve it: an owner decision on model-vs-instance accounting, and whether team value needs a second mesh.

Proposed slugs (explicit kinds only): content-mill-melee, content-mill-ranged, from melee and ranged in plan/18:60 and plan/03:14. No per-lane slugs: top, mid and bottom name lanes, not mills.

Status: decided — owner, 2026-11-07; B2, 0 new GLBs.

### 8. loading-dioramas — conflicting neededCount 24 vs 6

Unresolved: two contradictory counts inside plan/18, both UNVERIFIED, and dioramas are interface scene compositions rather than individual props. Primary citation plan/18-asset-manifest-and-audio.md:87; secondary plan/18-asset-manifest-and-audio.md:119.

Local evidence:
- plan/18:87 — Loading screen | 1 template, 24 dioramas | Caption from gag 01 (plan/16) |.
- plan/18:119 — Interface 16 screen and element units, including 6 loading dioramas, and about 700 strings. ... Counts are estimates until the asset list is locked.
- plan/16:17 — Two outer panels slide together like Willie's ship bell swinging, revealing the caption. [GUESS] | The Trend | Every load | Skippable. This describes a UI panel animation, not a 3D prop.
- plan/26:58 — Gags | Death recap, Rebrand record, Hyped-ended marker, announcer | All others | Gags are presentation, not balance.
- plan/18:89 — Shop | 1 | The Plug |. The dioramas sit in the Interface section, not Neutrals, objectives, map.

What would resolve it: an owner decision to pick one count or drop the row from the prop list.

Proposed slugs: none. No local source names a diorama, so no slugs are invented from either count.

Status: decided — owner, 2026-11-07; C3, 0 new GLBs.

### 9. stockpile — neededCount 2, two readings

Unresolved: 2 can be one per team (plan/03:4, :16 and plan/02:36) or intact plus destroyed state (the plan/18:61 note). Primary citation plan/18-asset-manifest-and-audio.md:61; secondary plan/03-core-loop-and-win-condition.md:16.

Local evidence:
- plan/18:61 — Stockpile | 2 | Pinned shop-card monolith. Ends as a grey, half-height monolith; the [deleted] placeholder is an end-screen gag only. |
- plan/03:4 — Two teams of five. Each team defends a base, a set of lanes, and a Stockpile. Destroying the enemy Stockpile wins the match.
- plan/03:16 — Stockpile | 1 | Invulnerable until both T4s fall. Destroying it wins (plan/02, Win objective row). |
- plan/02:36 — Win objective | The Stockpile: invulnerable until both T4s fall, destroying it wins |.
- plan/16:27 — Click and hold reveals the losing Stockpile as [deleted] ... | End screen | Requires a click.
- plan/18:57 — Bases | 2 | Morning Market and Late Night Market |. plan/04:8-9 names the two bases.
- plan/18:61 explicitly excludes the [deleted] end-screen gag as an asset.

What would resolve it: an owner decision on what the 2 counts. Pinned shop-card monolith and grey, half-height monolith are descriptions, not names.

Proposed slugs: none. Morning Market and Late Night Market are explicit base names but no source names a Stockpile variant, so no team-qualified or state-qualified slugs are invented.

Status: decided — owner, 2026-11-07; B2, 0 new GLBs.

### 10. lane-creeps — neededCount 6

Unresolved: scope (rigged unit models, not static props) and whether the ally/enemy hood difference needs 6 meshes or 3 meshes plus hood variants. Primary citation plan/18-asset-manifest-and-audio.md:72.

Local evidence:
- plan/18:72 — Melee, ranged, siege, two teams | 6 | Allies rounded hood. Enemies angular hood. |
- plan/03:29 — A wave spawns every 30 s: three melee and one ranged per lane.
- plan/03:30 — A siege creep joins every fifth wave.
- plan/17:48 — Every color signal on a unit or ability carries a shape. Ally creeps have rounded hoods. Enemy creeps have angular hoods. Team colour on structures carries value instead.
- plan/02:20 — Creep wave pressure | Stan: allied creeps inside Reach gain damage and armor.
- plan/06:29 — Stan | Allied creeps inside the Reach of any allied hero: +20% damage, +2 armor.
- plan/18:76 — Creep animations | 180 | Six per model: idle, walk, attack, death, Stan cheer, spawn. Animations are excluded from the prop list.

What would resolve it: an owner decision on scope and hood handling. The hood is a shape signal, not a separate name.

Proposed slugs (explicit creep types only): creep-melee, creep-ranged, creep-siege, from melee, ranged, siege in plan/18:72 and plan/03:29-30. No ally or enemy slugs: those words are not names.

Status: decided — owner, 2026-11-07; C2, 0 new GLBs.

### 11. mega-creeps — neededCount 6

Unresolved: 6 scaled variants with no mega-specific names; original seal emblem is an internal parity reference. Primary citation plan/18-asset-manifest-and-audio.md:74.

Local evidence:
- plan/18:74 — Mega creeps | 6 | +25% scale, gold trim, original seal emblem |.
- plan/03:14 — A lane with both its Content Mills down spawns Mega creeps; a destroyed mill respawns after 5 min (UNVERIFIED).
- plan/03:15 — All six Content Mills down | n/a | Mega creeps spawn in all three lanes until a mill respawns.
- plan/20:27 — decision 22: The parity map stays internal: tracked in git, never copied into plan/, the site or a pack. Original emblems and names stay out of shipped text.
- plan/18:3 — counts are UNVERIFIED until the asset list is built.

What would resolve it: an owner decision whether mega creeps are six meshes or scale and material variants of the three named creep types.

Proposed slugs: none. +25% scale, gold trim and original seal emblem describe variants, not names. No slugs are invented from the count 6.

Status: decided — owner, 2026-11-07; C2, 0 new GLBs.

### 12. stan-buffed-overlays — neededCount 6

Unresolved: whether the Stan buff is a 3D mesh, a decal, a material or VFX; the 6 and the sign form are UNVERIFIED and GUESS-tagged. Primary citation plan/18-asset-manifest-and-audio.md:73; secondary plan/16-humor-and-tone.md:18.

Local evidence:
- plan/18:73 — Stan-buffed overlays | 6 | Raised sign and orange trim |.
- plan/16:18 — Hand-lettered Stan signs held by buffed creeps, with a different misspelling each match. [GUESS] | Stan and Reach | Zoom or spectator camera | Signs stay. Misspelling rotates.
- plan/18:31 — Mechanic status icons: Reach (concentric arcs), Stan (raised sign), ... . This is a 2D icon, excluded.
- plan/06:29 — Stan | Allied creeps inside the Reach of any allied hero: +20% damage, +2 armor.
- plan/21:63 — Stan Sign: allied creeps in Reach gain +5% damage. A named tier-2 neutral item.
- plan/23:97 — Stan Sign | Hand-lettered, slightly misspelled, deeply sincere.

What would resolve it: an owner decision on mesh versus decal or VFX, and whether the 6 are per-creep-type variants. Stan Sign is an explicitly named neutral item and is already a candidate slug in row 2; it is not the overlay and must not be reused for it.

Proposed slugs: none for the overlay. Raised sign and orange trim are descriptions, not names.

Status: decided — owner, 2026-11-07; C3, 0 new GLBs.

### 13. jungle-camp-creatures — neededCount 12

Unresolved: scope (12 NPC unit models, not static props) and whether all 12 need distinct meshes. Primary citation plan/18-asset-manifest-and-audio.md:75; secondary plan/12-neutrals-boosts-the-trend-and-snapshot.md:10.

Local evidence:
- plan/18:75 — Jungle camp creatures | 12 | NPCs, Spam, Scoffer, Troll-Bridge, Old Forum Ticker, and others |.
- plan/12:10-17 — the full named camp creature table: Background NPCs, Spam, Scoffer, Troll-Bridge, Old Forum Ticker, Static Imp, Ticker Sprite, Bio Bot, Reverb Wraith, Cancel Mob, Clang Golem, Markdown Hound, with camp types small, medium, hard and elder.
- plan/04:30 — Jungle creature names are in section 12.
- plan/04:26-28 — jungle camp counts per side.
- plan/12:23 — Camp stat budgets: Small 300 HP, Medium 550, Hard 950, Elder 1,600 (UNVERIFIED under decision 21).
- plan/16:30 — NPC camp creatures repeat one grey speech bubble when pulled ... Fades in 2 s (UNVERIFIED).

What would resolve it: an owner decision on whether rigged NPC unit models are in the static-prop remit. The 12 names are explicit, so slugs can be proposed without expanding the count.

Proposed slugs (12, names verbatim from plan/12:10-17): neutral-creature-background-npcs, neutral-creature-spam, neutral-creature-scoffer, neutral-creature-troll-bridge, neutral-creature-old-forum-ticker, neutral-creature-static-imp, neutral-creature-ticker-sprite, neutral-creature-bio-bot, neutral-creature-reverb-wraith, neutral-creature-cancel-mob, neutral-creature-clang-golem, neutral-creature-markdown-hound. These come from names, not from the number 12.

Status: decided — owner, 2026-11-07; C2, 0 new GLBs.

### 14. shop-npc-the-plug — neededCount 1

Unresolved: The Plug is a hero-grade rigged NPC with 6 animations, not a static prop; it needs the character pipeline. Primary citation plan/18-asset-manifest-and-audio.md:40; secondary plan/11-items.md:15.

Local evidence:
- plan/18:40 — Shop NPC, The Plug | 1, with 6 animations | Hero-grade |.
- plan/11:15 — The Spawn Lounge shop is run by The Plug, the shop NPC (section 18). It sells every component, every Tier 1 finished item and the consumable wards.
- plan/04:10 — Each base holds the Spawn Lounge, a main shop at the Spawn Lounge, one Back Alley Shop, two Lane Stalls.
- plan/18:10 — Model with LOD1 and LOD2 | 3 | 18 [78] | FBX or glTF. Hero-grade model spec.
- plan/18:89 — Shop | 1 | The Plug |. Interface section.

What would resolve it: an owner decision to include a rigged NPC in the static-prop remit, or route it to the character pipeline used for the 27 generated characters.

Proposed slugs: shop-npc-the-plug. The Plug is an explicit name and this is already the row slug. No additional slugs.

Status: decided — owner, 2026-11-07; D1, 0 new GLBs.

### 15. safe-spot — neededCount 4

Unresolved: no shape, no plan/18 asset row, deferred by the cut list; 4 is placed instances (2 per team), not 4 distinct models. Primary citation plan/21-systems-added-back.md:71; secondary plan/26-first-playable-cut-list-and-checks.md:54.

Local evidence:
- plan/21:71 — Two Safe Spots per team, one at each river crossing next to the team's safe lane. Available from 0:00.
- plan/21:73 — Active: heals all allies within 500 radius for 14% of max HP per second, for 5 s.
- plan/21:74 — Cooldown 45 s, shared per Safe Spot.
- plan/21:69 — Numbers in this section are UNVERIFIED.
- plan/04:20 — Shallow crossings let heroes cross the river at fixed points only. Crossings are described, not named.
- plan/26:54 — Safe Spots | None | Section 21 | Not needed to test Clout.
- plan/18 has no Safe Spot asset row.

What would resolve it: an owner decision to add a Safe Spot mesh with a shape and an asset row, or drop the row.

Proposed slugs: none beyond the row's own safe-spot name. No per-crossing slugs are invented from the count 4.

Status: decided — owner, 2026-11-07; D1, 0 new GLBs.

### 16. cosmetic-plinth — neededCount null

Unresolved: no count, no shape, no asset row. The word plinth appears only in a season theme and a 2D icon style rule. Primary citation plan/21-systems-added-back.md:134; secondary plan/18-asset-manifest-and-audio.md:42.

Local evidence:
- plan/21:134 — The cosmetic skin theme: costumes, plinths and the Trend banner.
- plan/21:130 — A season is one patch. Each season rotates three things and changes no numbers.
- plan/18:42 — Item icon style: one object, ¾ top-down view, three value groups, warm key light top left, cool rim light, 2 px dark outline, no text. Consumables sit on a circular plinth. This is a 2D icon style, not a 3D asset.
- plan/18 has no plinth asset row.
- plan/18:3 — counts and sizes are UNVERIFIED until the asset list is built.

What would resolve it: an owner decision to drop the row, or add a plinth mesh with a count, shape and asset row.

Proposed slugs: none. cosmetic-plinth is a descriptive label coined for the row, not a source name. No slug is invented.

Status: decided — owner, 2026-11-07; D1, 0 new GLBs.

## Summary

| # | row | neededCount | unresolved | explicit slugs proposed |
| --- | --- | --- | --- | --- |
| 1 | terrain-kits-and-props | 3 kits / 120 props | 120 props unnamed, UNVERIFIED | 3 |
| 2 | world-models-shop-and-drop | 15 | no item-to-15 mapping | 14 named candidates |
| 3 | trend-costumes | 8 | decided: one base mesh, eight material swaps | 0 |
| 4 | trend-death-husks | 8 | decided: one desaturated mesh, modifier materials | 0 |
| 5 | out-of-bounds-marginalia | 10 | 9 vignettes unnamed | 0 |
| 6 | towers | 8 vs 22 | model vs instance | 4 |
| 7 | content-mills | 4 vs 12 | model vs instance | 2 |
| 8 | loading-dioramas | 24 vs 6 | two counts, interface scope | 0 |
| 9 | stockpile | 2 / 2 | team vs state reading | 0 |
| 10 | lane-creeps | 6 | unit scope, hood variants | 3 |
| 11 | mega-creeps | 6 | variant vs mesh | 0 |
| 12 | stan-buffed-overlays | 6 | mesh vs decal/VFX | 0 |
| 13 | jungle-camp-creatures | 12 | unit scope | 12 |
| 14 | shop-npc-the-plug | 1 | rigged NPC scope | 1 (existing row slug) |
| 15 | safe-spot | 4 | no shape or asset row | 0 |
| 16 | cosmetic-plinth | none | no count, shape or asset row | 0 |

Totals: 16 rows reviewed, 16 decided by the owner and 0 open. 7 rows propose explicit-name slugs (39 slugs, all transcribed from names in the cited lines). 9 rows propose none. No slug is derived from a numeric count. Instantiated counts that are not model counts (22 tower placements, 12 Content Mill placements, 4 Safe Spot placements, 24 or 6 loading dioramas) stay as neededCount values only.

Explicitly unnamed categories: individual terrain props, Trend costumes, Trend death husks, loading dioramas, marginalia vignettes, mega creep variants, Stan overlays, Stockpile variants, Safe Spot variants and cosmetic plinths. No source names them, so no slugs are invented for them.

The 2026-11-06 survey changed no product file; the 2026-11-07 decisions change docs only, from the [fast-path dry run](/tmp/hy3d-bota-held-fast-path-dry-run.md). /tmp/bota-needed-props.json remains final at 44,007 bytes with sha256 ef431bb9a5a587c6a507a105325beb03fd59f2bec88dbafce2be455cd8449175; the 24 unambiguous:true rows are hy3d's generation set.
