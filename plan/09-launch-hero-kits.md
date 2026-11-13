# 9. Launch hero kits
Six launch characters across six of the twelve role families (Bulwark, Engine, Herald, Leash and Phantom have no launch hero). The launch set is the first-playable slice set in plan/26 (decision 48). Each has four abilities: three basic and one ultimate. Ultimates unlock at 6, 11 and 16.

Slot in brackets = character number. Slot mapping follows the section 24 number, so it is GUESS. Every renamed ability and hero name is GUESS (theme only). Archetypes kept from the former kit (GUESS: each former archetype maps to a role family in plan/15).

Emergent rewrite (GUESS): each effect carries its character's gag (a visible trait from the character prompt). Ability IDs, slot order, the four-ability count, effect kinds and the tier numbers below are kept. Any number that moved is GUESS inline (decision 42). Every cross-hero hook is GUESS and lives only in Emergent hooks, at most one per row (a hero may be named as the partner in several rows). No new engine kinds or ability slots; ideas that need one are in Requests.

### Ability value tiers

Every ability uses one of these tiers. Each hero's abilities are sized to them, with the role-family talent sets in section 21 added on top.

Sigma is the ability resource: base pool 50, +12 max per Intelligence point and +0.05 regen per second per Intelligence point (plan/07). A cast spends its Sigma figure from the table below (UNVERIFIED).

| Ability type | Level 1 | Level 2 | Level 3 | Level 4 | Cooldown (L1 to L4) | Sigma (L1 to L4) |
| --- | --- | --- | --- | --- | --- | --- |
| Ability 1, damage | 80 | 160 | 240 | 320 | 10, 9, 8, 7 s | 60, 70, 80, 90 |
| Ability 2, control or utility | 2.0 s | 2.5 s | 3.0 s | 3.5 s | 12, 11, 10, 9 s | 70, 80, 90, 100 |
| Ability 3, aura or passive | 300 radius | 350 radius | 400 radius | 450 radius | 14, 12, 10, 8 s | 0 when the kit's Ability 3 is a passive, 50 when it is an aura (each hero's kit names which) |
| Ultimate (unlocks at 6, 11, 16) | 250 damage | 400 damage | 550 damage | n/a (max 3) | 100, 85, 70 s | 150, 200, 250 |

Notes:

- Stun and root durations in ability 2 (the control or utility slot) scale with its Level 1 to Level 4 durations in the table above. Status resistance (section 21) reduces them.
- Damage numbers are base values. Attribute scaling and item bonuses are added on top.
- Nearby means within 300 units when a row names no radius (UNVERIFIED).
- Default damage type: Ability 1 physical, Ability 2 magical, Ability 3 pure (UNVERIFIED); a kit row can name another type.
- Hooks name the other hero and the ability they touch. A hook that needs a counter read across heroes uses an existing unit counter from Lua (GUESS).

| Hero | Archetype | Ability 1 | Ability 2 | Ability 3 | Ultimate |
| --- | --- | --- | --- | --- | --- |
| Grey [025] | Drifter | Beam Quote: three-hit tractor-beam burst from a patched orange-and-teal jumpsuit; each line is another follow-up nobody remembers opening (GUESS) | Abduction Count: collects a specimen stack when a nearby enemy dies, cap 5; the alien frowns as if the department lost the first four forms (GUESS) | Orb Vibes Aura: the patched orange-and-teal jumpsuit hums through metal wrist cuffs, cutting nearby enemy armor; the utility belt calls it a compliance check (GUESS) | Probe Ticker: lines of damage that probe the target; each kill adds a specimen and a memo marked final final v3 (GUESS) |
| Boomer [007] | Heckler | Pull Cord Hurl: yanks an imaginary mower cord and tosses a ranged slow; the silver energy drink stays raised like a receipt for damages (GUESS) | Ok Boomer Strike: next attack, with a dismissive wave over black shades, deals bonus damage and blames the youth (GUESS) | Cobalt Fade: black shades and stained white tee make him invisible for 2 s while moving; attacking smears the fade (GUESS) | Tracked Lawn: reveals an enemy; every hit leaves a grass stain billed to the nearest minor (GUESS) |
| Ghillie [026] | Stalker | Burlap Warning: straw ghillie strips scatter as area traps with damage; the haystack posts a warning and then denies being the haystack (GUESS) | Twine Lock: camouflage twine holds and reveals enemies; the grass beard cites the exact shrub (GUESS) | Corn Stalk Jump: leaping strike with damage; goggles pop open at the worst possible moment (GUESS) | Scoped Temp Ban: remote detonation through the wrapped scope disables; the round goggles file an appeal from inside the bush (GUESS) |
| Coomer [008] | Firebrand | Lone Arm Clap: stuns and damages; both perfectly ordinary sleeves clap around the hoodie pocket (GUESS) | Bloodshot Brew: fire area; the huge black-ringed eyes ignite a brew he calls herbal (GUESS) | Tank Top Splash: pushes enemies back; the grey hoodie pocket flings the splash and the grin denies everything (GUESS) | Right Arm Clones: summons clones of self; every clone claims to be a different browser tab (GUESS) |
| Ecce [019] | Archivist | Halo Beam: stuns and damages; the crown of thorns catches a light nobody can find in the level (GUESS) | Burlap Reshare: bounces between enemies; the burgundy robe reshares the bounce without attribution (GUESS) | Fresco Aura: damages nearby enemies; watery eyes smudge the damage across them (GUESS) | Halo Shutter: repeated light rays over a window; every frame is captioned Behold, then Behold again (GUESS) |
| Gothgirl [027] | Recluse | Fan Swarm: summons bugs; the black dress produces them from a sigh so quiet it has subtitles (GUESS) | Cardigan Flicker: blinks; one sleeve goes, then the other, because leaving is a process (GUESS) | Velvet Double: double attack; the choker doubles it and refuses to be impressed (GUESS) | Rewind Smoke: rewinds a target's position to before anyone said vibe; platform boots land on the word and erase it (GUESS) |

Notes:

- Talent trees are in section 21.

### Emergent hooks

No hook is led by Gothgirl [027]; she may still be the partner named in another hero's hook. Heroes without an entry carry no hook.

- Boomer [007] with Wojak [004]: Pull Cord Hurl slowed targets draw Hollow Stare (GUESS).
- Coomer [008] with Bot Bernard [020]: Tank Top Splash pushes into Stage Rain zones (GUESS).

### Requests

- A cross-hero unit-counter read that does not need Lua per hook (GUESS): several hooks above read another hero's stack; a shared stack channel would make them plain data.

### Launch-slice callbacks

Grey's final final v3 memo, Boomer's grass-stain bill and Ghillie's haystack appeal seed the Receipt Chain for section 10. Ecce's Behold caption and Gothgirl's pre-vibe rewind seed the Repost Chain. Coomer's browser-tab clones give Npc a line to repeat later; every launch joke has a payoff in the full roster and every payoff still describes a real effect. By the third reread, final final v3 is simultaneously Grey's damage line, Howard's filing date and Forever's loop; the joke has grown without adding a mechanic.
