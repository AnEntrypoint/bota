# 24. Power tier draft (UNVERIFIED)

**Status: tier letters withdrawn** (decision 20). The flag list and the test-first list stay: they are what the first playtest should check. UNVERIFIED throughout.

No simulation exists. Flags are read from the kit text (sections 9, 10, 21). This is not a power budget or a balance result.

Names: the characters are the ROSTER.md set, slot = number. Renamed kits are GUESS (theme only); kit mechanics are unchanged, so the flags carry over.

## Method

- Timed disables scale with the ability 2 table, so only disables with no timer or an until-condition count as long.
- Stacks with a stated cap count as stacking but are not flagged. Talent choices count only when they add a global, uncapped-stacking or no-timer disable effect.
- FLAG: global effect, permanent disable (no timer or until-condition), or stacking with no stated cap. Flagged heroes are tested first.
- The role family average is the mean of the same measure over every other hero in the same role family (section 15), taken from the same test (UNVERIFIED until the first playtest).

## 1. Table (26 active heroes)

| # | Hero | Role family | Flag | Reason |
| --- | --- | --- | --- | --- |
| 001 | Neckbeard | Heckler | - | Ult makes an ally untargetable; otherwise shield, heal, slow. |
| 002 | Chad | Showboat | - | Ult replays the next death after a delay; frost slow, stun mark. |
| 004 | Wojak | Recluse | - | Taunt, slow, reflect, threshold kill; no global, stacking or escape. |
| 005 | Bloomer | Herald | - | Stun and slow; hawk and boar summons; ult rallies allies. |
| 006 | Tradwife | Herald | - | Movement-scaled bleed, attack speed, area damage; reveal and drain. |
| 007 | Boomer | Heckler | - | Brief invisibility while moving; reveal and gold on hit; slow toss. |
| 008 | Coomer | Firebrand | - | Stun and damage, fire area, knockback; ult summons self-clones. |
| 009 | Gondola | Recluse | FLAG | Potato Spit stacks, no cap stated; ult adds damage per hit taken. |
| 010 | Spurdo | Firebrand | FLAG | Summons spiderlings, no cap stated; web slow, poison, heal on kills. |
| 011 | Karen | Heckler | - | Nearby stun; charge; reflect when hit; line charge ult. |
| 012 | Howard | Archivist | - | Ult is a temporary sanctuary; creep conversion and healing. |
| 013 | Sanic | Stalker | - | Stealth while moving is its escape; fire arrows; skeleton ult. |
| 014 | Lankdad | Phantom | - | Reveal and damage nearby; pull; push; ult stuns all in radius. |
| 015 | Finger Dan | Heckler | - | Fire cone, stun and knockback, armor and regen; ult stronger attacks. |
| 016 | Willie | Engine | - | Rolling rock projectiles, line roll, pull; ult zone stun. |
| 017 | Noscope | Stalker | - | Nearby spin damage, radius heals, crit chance; ult jumps between enemies. |
| 018 | Dino | Bulwark | - | Beam, area blind, sigma restore; ult fast flight, heals on pass. |
| 019 | Ecce | Archivist | - | Stun, bounce blade, nearby aura; ult repeated light rays. |
| 020 | Bot Bernard | Herald | - | Line stun, leap with attack speed, ally shadow; ult damages all nearby. |
| 021 | Shoop | Drifter | - | Dash strike, stat-scaled damage, stat swap; ult copies enemy ability. |
| 022 | Npc | Phantom | FLAG | Ult creates more illusions, no cap stated; blink; slow lance. |
| 023 | Forever | Recluse | FLAG | Ult stuns until the clip ends, no timer; brief evasion while moving. |
| 024 | Cole | Phantom | - | Hold that copies an enemy's image; bonus damage, poison; ult stun, slow. |
| 025 | Grey | Drifter | - | Abduction Count stacks on kills, capped (talent raises cap); burst; ult lines. |
| 026 | Ghillie | Stalker | - | Area traps, hold and reveal, leaping strike; ult remote disable. |
| 027 | Gothgirl | Recluse | - | Cardigan Flicker is its escape; bug summons, double attack, ult rewinds target. |

## 2. Summary

- Coverage: 6 launch kits (section 9), 20 remaining kits (section 10). All 26 active heroes matched by slot.
- Flags: 4. Permanent disable 1 (Forever 023). Uncapped stacking 3 (Gondola 009, Spurdo 010, Npc 022).

## 3. Test first

Timer passes stay at or below 3 s and stack passes at or below 10 (UNVERIFIED), unless a line gives its own bound.

1. Spurdo (010): spiderlings with no cap stated. Measure spiderlings alive over a match and heal from spider kills. Pass: spiderlings alive at once stay at or below 6 over a match (GUESS: a count a player can track on screen; the balance pass sets it).
2. Npc (022): more illusions with no cap stated, plus a blink. Measure illusions alive over time and their total damage. Pass: illusions alive at once stay at or below 4 (UNVERIFIED).
3. Forever (023): ult stun has no timer. Measure the longest stun and whether target death or clip end ends it. Pass: the longest stun stays at or below 3 s (GUESS: a stun past three seconds stops reading as a tempo break; the balance pass sets it).
4. Gondola (009): Potato Spit stacks with no cap stated. Measure stacks at fight end and damage per hit taken under the ult. Pass: the stack bound above holds.
