# 9. Launch hero kits
Eight launch characters across six of the twelve role families (Archivist, Bulwark, Engine, Firebrand, Phantom and Showboat have no launch hero). Each has four abilities: three basic and one ultimate. Ultimates unlock at 6, 11 and 16.

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
| Grey [077] | Drifter | Beam Quote: three-hit tractor-beam burst; each hit spends an Abduction Count stack for +10% damage (GUESS) | Abduction Count: collects a specimen stack when a nearby enemy dies, cap 5 (GUESS); an allied kill adds one too (GUESS) | Orb Vibes Aura: the levitating orb hums, cutting nearby enemy armor (GUESS) | Probe Ticker: lines of damage that probe the target; each line that kills adds an Abduction Count stack (GUESS) |
| Boomer [010] | Heckler | Pull Cord Hurl: yanks the weedwhacker cord and tosses it for a ranged slow (GUESS) | Ok Boomer Strike: next attack, with a dismissive wave, deals bonus damage (GUESS) | Cobalt Fade: a blue paint fade makes him invisible for 2 s while moving; attacking smears the fade and breaks the invisibility (GUESS) | Tracked Lawn: reveals an enemy; every hit leaves a grass stain that pays gold (GUESS) |
| Noscope [039] | Stalker | Hitmarker Spin: spins and damages nearby enemies; each hit flashes the green crosshair hitmarker over the target (GUESS) | Sponsor Patch Heal: heals allies in radius; a healed ally also gets Noscope's Lucky Scope crit chance (GUESS) | Lucky Scope: the lens flare gives a chance to critically strike; a crit pays a sponsor bonus (GUESS) | Bolt Action Chain: rapid bolt-action strikes that jump between enemies (GUESS) |
| Viking [019] | Herald | Mead Clink: area damage and slow; the slow lasts while enemies stand in Hydrate or Diedrate's aura (GUESS) | Hammer Hold: the silver hammer pendant roots and damages over time (GUESS) | Hydrate or Diedrate: sigma regen for allies, sipped from a half-full bottle (GUESS) | Ragnarok March: area nuke around the hero; each rhythmic march step stomps the ground (GUESS) |
| Smudge [021] | Leash | Eyeliner Bleed: damage over time as the eyeliner runs; bleeding targets take the Emo Vibes armor cut (same hero, GUESS) | Sweater Slip: the oversized sweater slips off one shoulder to protect an ally from death for 2 s (GUESS) | Open Palm Bounce: animated open-palm gestures bounce to nearby units (GUESS) | Emo Vibes: reduces enemy armor; the cut doubles on targets already bleeding from Eyeliner Bleed (GUESS) |
| Wojak [005] | Recluse | Sigh at Clouds: a wistful sigh taunts enemies in range (GUESS) | Hollow Stare: downcast hollow eyes slow and damage over time (GUESS) | Sad Clapback: a wounded sigh returns damage when attacked (GUESS) | Sorrowful Cancel: instant kill below 25% health (GUESS, threshold UNVERIFIED) |
| Ghillie [089] | Stalker | Burlap Warning: burlap strips scatter as area traps with damage (GUESS) | Twine Lock: camouflage twine holds and reveals enemies (GUESS) | Corn Stalk Jump: leaping strike with damage; a jump over a trap triggers it early (GUESS) | Scoped Temp Ban: remote detonation through the scope disables (GUESS) |
| Forever [068] | Recluse | Tear Clip: a single tear projectile; a slowed target keeps the tear stuck (GUESS) | Lumpy Wail: a weeping wail damages around the hero (GUESS) | Crawl Ghost: brief evasion while crawling low (GUESS) | Eternal Loop: the weeping stun repeats until its clip of three stuns ends, then refills, forever (GUESS; the three-stun clip is UNVERIFIED) |

Notes:

- Talent trees are in section 21.

### Emergent hooks

No hook is led by Forever [068]; it may still be the partner named in another hero's hook.

- Grey [077] with Smugjak [029]: Orb Vibes and Smug Citation armor cuts do not stack; the larger applies (GUESS: decision 3 keeps orb effects from stacking, and this extends it to armor cuts).
- Boomer [010] with Wojak [005]: Pull Cord Hurl slowed targets draw Hollow Stare (GUESS).

### Requests

- A cross-hero unit-counter read that does not need Lua per hook (GUESS): several hooks above read another hero's stack; a shared stack channel would make them plain data.
- An armor-cut stack rule that caps combined armor cuts (GUESS): Orb Vibes and Smug Citation would stack to a combined armor cut of 4 instead of the larger applying (GUESS, no 6.88g source).
