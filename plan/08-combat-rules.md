# 8. Combat rules

Numbers in this chapter are UNVERIFIED.
### Damage types

| Type | Reduced by | Blocked by |
| --- | --- | --- |
| Physical | Armor | Evasion, miss chance |
| Magical | Magic resistance | Spell immunity |
| Pure | Nothing | Nothing |
| HP removal | Nothing | Nothing; HP removal ignores spell immunity |

### Armor and magic resistance

- Physical damage multiplier, where A is armor: for A ≥ 0, 1 − (0.06 × A) / (1 + 0.06 × A); for A < 0, 2 − 0.94^(−A), capped at 120 armor (engine armour scale).
- Magic resistance: heroes start at 25%. Each source multiplies. Two sources at 25% each give 1 − 0.75 × 0.75 = 43.75%.

### Attack speed

- Attacks per second = (100 + bonus attack speed) / (BAT × 100).
- Bonus attack speed (the term in the formula above) is capped at 600 (UNVERIFIED).
- Attack animation: attack point 0.3 s, then backswing 0.2 s at base attack speed (GUESS: a short wind-up and recovery read as one swing; the balance pass sets them). Animation canceling is allowed; a cancel leaves the cooldown spent.

### Evasion and miss

- Evasion uses pseudo-random distribution, checked on impact. The base chance is 0%; each source adds a flat percent, 25% for Evasion (GUESS: a quarter reads at a glance; the balance pass sets it).
- Miss chance is separate from evasion.
- True strike ignores evasion. Source: the Hot-take initiator role (Firebrand family, plan/15).

### Lifesteal and amplification

- Attack lifesteal: items, and the hero abilities whose kit row in plan/09 or plan/10 says attack lifesteal (Stare Glaze, plan/10).
- Spell lifesteal: none in v1.
- Spell amplification: Intelligence (section 7) plus one item.
- Cooldown reduction: Refresh Page (cooldown reset), the Unboxing modifier, and Eternal Ticker (10% faster cooldowns). Ability-specific cooldown cuts are not global CDR.

### Disables

| Disable | Class | Effect | Break rule |
| --- | --- | --- | --- |
| Stun | Hard | No actions or movement | Stun cannot be broken |
| Polymorph | Hard | Transforms the target | Dispelled by strong dispel |
| Silence | Soft | No abilities, items still work | Strong dispel removes it |
| Root | Soft | No movement, abilities work | Dispelled by basic dispel |
| Sleep | Hard | Stun that breaks on damage | Breaks on any damage |
| Taunt | Soft | Forced to attack the source | Lasts its duration |
| Disarm | Soft | No attacks, abilities work | Dispelled by basic dispel |
| Fear | Hard | Forced to move away | Lasts its duration |
| Cyclone | Hard | Airborne, no actions | Stun-equivalent, dispelled by strong dispel |
| Hold | Hard | No actions or movement; held in place | Lasts its duration (GUESS: no break rule in our data yet) |
| Charm | Hard | Forced to move toward the source | Lasts its duration (GUESS: no break rule in our data yet) |
| Petrify | Hard | No actions or movement; stone form | Breaks on damage (GUESS: keeps petrify readable as a hold that breaks) |
| Slow | Soft | Movement and attack speed reduced | Lasts its duration (GUESS: no break rule in our data yet) |
| Blind | Soft | Attacks can miss at the blind miss percent | Lasts its duration (GUESS: no break rule in our data yet) |

Rules:

- Hard disable cap: 3 hard disables per team in any 10 s window (a hard disable is defined in decision 37). A fourth is shortened to 0.5 s.
- Purge: basic dispel removes the Stan, Front Page and boost buffs (Sweat Mode, Dank Goods), plus root and disarm. It does not remove Hype Spike, Resell or Clout states. Strong dispel removes polymorph, silence and cyclone.
- Spell immunity blocks magical damage and disables, not pure damage or HP removal.

### Resell chain (Brainrot original)

- Job: teamfight chain (plan/02, Teamfight chain row). The cost is the grouping it needs, or the spread against area damage.

| Property | Value |
| --- | --- |
| Trigger | Hard disable or ultimate lands on an enemy |
| Radius | 600 |
| Stack effect | +8% attack speed or spell amp per stack, chosen by the caster when the chain starts and fixed for every stack of that chain |
| Spread | Any ally who damages the target passes a stack to allies within 600 of the target; the donor keeps its stack (UNVERIFIED) |
| Max stacks | 5 |
| Stack decay | 4 s per stack, from that stack's own spread (UNVERIFIED) |

Stacks show as dotted arcs between heroes. Resell arcs are capped at five on screen.
