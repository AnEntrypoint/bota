# 13. Vision and fog

Numbers in this chapter are UNVERIFIED.
Vision decides what the enemy can see, and therefore what they can take. Under Brainrot, enemy vision is also the source of your Clout. Vision is the most-used system in the game.

### Wards

- Job: vision and wards (plan/02, Vision and wards row). The cost is the ward's gold and its 6 min life.

| Ward | Brainrot name | Cost | Duration | Stock | Function |
| --- | --- | --- | --- | --- | --- |
| Vision ward | Lurker Cam | 65 gold | 6 min | Start 2, max 4, restock 150 s | Vision. Enemies see the reveal and earn no Clout. |
| True sight ward | Spoiler Tag | 75 gold | 6 min | Start 1, max 2, restock 150 s (GUESS: no source gives its stock; it takes the Lurker Cam restock so the pair reads alike) | True sight. Reveals invisible units and wards. |

- Enemy wards reveal the area but earn their owner no Clout.
- Towers give true sight at 700 range.

### Reveal tools

- Job: reveal (plan/02, Vision and wards row). The cost is the item at risk: the Gem drops on death, and Smoke restocks in 11 min.

| Tool | Brainrot name | Effect |
| --- | --- | --- |
| Gem | Gem of Subtext | True sight carried by one hero. Drops on death. |
| Dust | Dust of Receipts | Reveals invisible units in the radius plan/11 gives |
| Smoke | Smoke of Deniability | Group invisibility, hidden on the minimap until an enemy hero is within 300 range or an enemy tower within 700 range (UNVERIFIED). Restock 11 min. |

### Vision states

- **LIVE:** an enemy hero sees you. Clout is earned. The LIVE dot shows on your portrait.
- **Hidden:** no enemy hero sees you. No Clout is earned. This is the vision side of plan/06's Quiet state: Quiet is Hidden with Clout below the Hype Spike threshold, and a hero at that threshold is Hyped instead (plan/06 overlap order).
- **Revealed** (a visibility flag, not a Clout state): an enemy ward, a reveal tool, or a reveal modifier or ability (Cast Rush, Tendril Flare) shows your position. No Clout is earned.

The LIVE dot uses the colour and ring in decision 16. It is never red (red means damage).

### Day and night

- Job: vision (plan/02, Vision and wards row). The cost is the vision radius lost at night.
- The day and night cycle runs 4 min day, 4 min night.
- At night, vision radius drops for every hero: push while vision is short, or ward for cover (both cost tempo, UNVERIFIED). Some heroes have night abilities (Barista).
- The clock is shown on the minimap as a sun or moon.

### Fog rules

- Clout uses enemy hero vision only. Enemy creeps, towers and wards do not count.
- A stealthed hero is revealed by true sight, reveal tools and any enemy hero within 300 range.
- Invisibility from items and abilities is broken when the hero attacks, casts or takes damage.
