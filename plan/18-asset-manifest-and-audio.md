# 18. Asset manifest and audio

Counts and sizes in this chapter are UNVERIFIED until the asset list is built.
Launch counts assume 24 heroes and four abilities each. Full-roster counts (59 heroes) are in brackets.

### Heroes

| Asset | Per hero | Launch \[Full\] | Format |
| --- | --- | --- | --- |
| Model with LOD1 and LOD2 | 3 | 36 \[129\] | FBX or glTF. LOD0 12 to 18k tris, LOD1 50%, LOD2 25%. 2048² diffuse and mask. |
| Animations | About 15: idle ×2, idle gag, run, haste run, attack ×2, cast ×4, channel, death, spawn, victory | 180 \[645\] | FBX, 30 fps |
| HUD portrait | 1 | 12 \[43\] | 256 × 256 PNG |
| Loading and promo art | 1 | 12 \[43\] | 1920 × 1080 and 1080 × 1920 |
| Minimap icon | 1 | 12 \[43\] | 32 × 32 PNG |
| Pick-screen pose | 1 | 12 \[43\] | Engine scene |
| Voice lines | About 60 | 720 \[2,580\] | 48 kHz WAV, −16 LUFS, subtitled |

### Abilities and status

| Asset | Launch \[Full\] | Format |
| --- | --- | --- |
| Ability icons | 96 \[448\] | 128 × 128 PNG |
| Cast VFX | 96 \[448\] | Particle, 512² flipbook |
| Impact VFX | 96 \[448\] | Particle, peak 0.4 s or less |
| Ground telegraphs (about 40% of abilities) | About 38 \[about 180\] | Team-colored decal |
| Mechanic status icons | 9 | 64 × 64 |
| Kill streak readout | 1 | Number on the Clout bar, not an icon |
| Generic status icons | 12 | 64 × 64 |
| Trend modifier icons | 8 | 64 × 64, plus 256 × 256 banner |

Mechanic status icons: Reach (concentric arcs), Stan (raised sign), Hype Spike (spike with ring timer), Markdown (split circle), LIVE (filled dot with ring), Resell stacks 1 to 5 (curved double arrow with pips), Snapshot (corner brackets), Go Private (padlock with timer ring), Rebrand (circular arrow around a blank tag).

### Items

| Asset | Count | Format |
| --- | --- | --- |
| Item icons | 50 | 88 × 64 PNG, 176 × 128 master |
| World models, shop and drop | 15 | 500 to 2,000 tris, 512² texture |
| Active and consumable VFX | 30 | Particle. On-use pop 0.3 s or less. |
| Shop NPC, The Plug | 1, with 6 animations | Hero-grade |

Item icon style: one object, ¾ top-down view, three value groups, warm key light top left, cool rim light, 2 px dark outline, no text. Consumables sit on a circular plinth. Actives carry a grey edge glow. Passives do not.

### Neutrals, objectives, map

| Asset | Count | Notes |
| --- | --- | --- |
| The Trend base model | 1 | Blank boss built from stacked banners |
| The Trend costumes | 8 | Swappable modifier meshes. Silhouette stays constant. |
| The Trend animations | 7 | Idle, three attacks, enrage, death, respawn |
| Trend death husks | 8 | One per modifier. Desaturated, no health bar. |
| Trend announcement banners | 8 | 1920 × 200 |
| Snapshot pickup and revive | 2 | One model, one VFX |
| Breaking News zone | 1 | Ground ring with a capture meter above it |
| Front Page icon | 1 | Reach buff from a held zone, 64 × 64 |
| The Trend pit | 1 | Recessed amphitheater with marginal props |
| Bases | 2 | Morning Market and Late Night Market |
| Terrain kits and props | 3 kits, 120 props | Lanes, jungle, river |
| Towers | 8 | Four tiers across two teams. Tier read by size and stacked stamps. |
| Content Mills | 4 | Melee and ranged, two teams |
| Stockpile | 2 | Pinned shop-card monolith. Ends as a grey, half-height monolith; the \[deleted\] placeholder is an end-screen gag only. |
| Boosts | 7 | Each a unique shape |
| Front Runner icon | 1 | White pennant on a grey disc (UNVERIFIED). |
| Wards | 4 | Lurker Cam: closed-eye icon. Spoiler Tag: open-eye icon with a tag. Two teams. Placed and revealed states. |
| Delivery Drones | 2 | Envelope on legs, plus flying upgrade |
| Out-of-bounds marginalia | 10 | Static vignettes |

### Creeps

| Asset | Count | Notes |
| --- | --- | --- |
| Melee, ranged, siege, two teams | 6 | Allies rounded hood. Enemies angular hood. |
| Stan-buffed overlays | 6 | Raised sign and orange trim |
| Mega creeps | 6 | +25% scale, gold trim, original seal emblem |
| Jungle camp creatures | 12 | NPCs, Spam, Scoffer, Troll-Bridge, Old Forum Ticker, and others |
| Creep animations | 180 | Six per model: idle, walk, attack, death, Stan cheer, spawn |

### Interface

| Screen or element | Count | Copy |
| --- | --- | --- |
| HUD frame | 1, plus 3 colorblind skins | None |
| Clout bar | 1 | Clout |
| LIVE dot | 1 | LIVE. Slow pulse, 1 Hz or below. |
| Scoreboard | 1 | K, D, A, Clout, Net Worth |
| Pick and ban screen | 1 | Title in plan/14 |
| Loading screen | 1 template, 24 dioramas | Caption from gag 01 (plan/16) |
| Victory and defeat | 2 | Victory. Stall sold. / Defeat. Stall closed. |
| Shop | 1 | The Plug |
| Settings | 1 | Reduced motion, flash limiter, colorblind presets, subtitle size and background |
| Tooltips | About 600 | Order and size in plan/17. |
| Announcer strings | About 30 | Section 16 |

### Effects

| Effect | Specification |
| --- | --- |
| Hype Spike glow, 20 s | Steady violet rim light. Slow upward particles. Shadow counter. |
| Markdown record-scratch | Clout bar halves. Violet arc from corpse to killers. 0.3 s desaturation on the victim's screen. |
| Resell arcs | Ally-blue dotted arc with grey core. Via tags show on hover only. At most 5 drawn. |
| Trend banner | Slides from top, 2 s |
| Go Private | Padlock decal, 5 s ring timer, blinds |
| Snapshot revive | 3 s rewind clip. Corner brackets snap in. Soft white fade. |
| Rebrand record | Formerly tag, static; behaviour in plan/23 |

### Audio

| Category | Count | Direction |
| --- | --- | --- |
| Announcer stingers | 40 | Fad-forward, reactive, expressive |
| Clout SFX | 8 | Gain tick, Hype Spike start and end, Markdown scratch, LIVE on and off, Resell link, Rebrand |
| Trend SFX | 10 | Spawn, modifier reveal, attacks, death, Snapshot pickup and revive |
| UI SFX | 40 | Click, hover, purchase, error, pick, ban, ready |
| Ambient beds | 5 | Two bases, river, jungle, pit. Sound only, no music. |
| Hero voice | About 60 per hero | Expressive and reactive; see plan/16 rule 3. |

### Totals (launch)

Heroes 528. Hero voice 1,440. Abilities 326. Status icons 29. Items about 100. Neutrals and objectives 35. Map about 160. Creeps 210. Interface 34 screen and element units, including 24 loading dioramas, and about 700 strings. Audio, non-voice 103. Total about 3,000 assets and about 700 strings. Counts are estimates until the asset list is locked.
