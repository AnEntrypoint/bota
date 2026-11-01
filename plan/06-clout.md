# 6. Clout
Clout is the signature resource. A hero earns Clout only while an enemy hero can see them. It is the reason to stay in the open, and the reason to be marked down when you are.

### Earning Clout

- Job: last hitting, denying and vision (plan/02 rows). The cost is the Clout earned only while seen.

Numbers in this section are UNVERIFIED.

| Action | Clout | Condition |
| --- | --- | --- |
| Last hit | +1 | Inside enemy hero vision |
| Deny | +0.5 | Taken from the nearest enemy hero, while that hero sees the creep |
| Hero kill | +10 | Inside enemy hero vision |
| Assist | +4 | Inside enemy hero vision |
| Tower damage | +1 per 100 damage | While an enemy hero sees the tower |
| Stage camp creature | +1 | While an enemy hero sees the camp |
| Enemy ward | 0 | Reveals the warded area, earns nothing |
| Any action unseen | 0 | Gold and XP still earned |

### Clout rules

Numbers in this table are UNVERIFIED.

| Rule | Value |
| --- | --- |
| Reach radius | 300 + 3 × Clout, capped at 600 for the Clout term; Hype Spike and talent Reach add after the cap, each source as its chapter lists it (UNVERIFIED) |
| Stan | Allied creeps inside Reach: +20% damage, +2 armor |
| Hype Spike threshold | 100 Clout, unless a talent sets its own (plan/21) |
| Hype Spike duration | 20 s |
| Hype Spike effects | Reach +200; caster revealed on the global minimap |
| Clout after Hype Spike | 25 |
| Markdown on death | Victim loses 50% of Clout: the killer takes half of it and assists split the other half equally |
| Clout decay | Above 50 Clout: −1 every 10 s while unseen for those 10 s |
| Cap on Markdown | At most 200 Clout moves in one death |

- Job: vision and wards (plan/02, Vision and wards row). The cost is the Clout lost while unseen.

### Clout states

Numbers in this section are UNVERIFIED.

Each hero is in one of four states at any time. The state sets what the rest of the map can see.

1. **Quiet.** Below 100 Clout and no enemy vision. Earns gold and XP only.
2. **LIVE.** An enemy hero has the hero in vision. The violet LIVE dot shows on the portrait. Clout is earned.
3. **Hyped.** At 100 Clout. Hype Spike is active for 20 s. The hero is revealed on the global minimap.
4. **Marked down.** Death. The victim loses 50% of Clout. The killer takes half of that and assists split the rest (Clout rules). The hero returns to Quiet at spawn. When states overlap, Marked down wins, then Hyped, then LIVE, then Quiet.

- Job: map pressure and rotation (plan/02, Map pressure, rotation row). The cost is the global reveal that a Hyped hero gives up for 20 s.

Rebrand resets a hero to Quiet at 0 Clout.

### Design rules

- Clout is never a stat. It never adds damage or armor directly. Its only effects are Reach (which carries the Stan buff), Hype Spike and the Late-game Clout carry mood.
- Clout moves between teams only through the rules that name it: Deny takes it from the nearest enemy hero, and Markdown moves it on death. The ally tether (section 2) gives 20% of a tethered ally's Clout gains while within 600 range; the ally keeps its own Clout (UNVERIFIED).
- Clout is shown as one number on the top bar, abbreviated (1.2K) and exact on hover.

### Late-game Clout carry mood

- Job: comeback pressure (plan/02, Comeback gold row). The cost is the Front Runner icon on the minimap, or the Reach +50 given up to hide it.

Each team has one mood, set by the gap between the two teams' total Clout. Mood changes Reach and minimap reveal only. Numbers are UNVERIFIED.

| Mood | Entered when | Effect |
| --- | --- | --- |
| Front Runner | Team total ahead by 300 Clout or more for 30 s | Its heroes get Reach +50. Its highest-Clout hero shows on the minimap as a Front Runner icon for 20 s every 60 s, unless its heroes give up Reach +50 for those 20 s to hide it (UNVERIFIED). |
| Underdog | Team total behind by 300 Clout or more for 30 s | Its heroes get Reach +50 and show on the minimap for 10 s after each kill (UNVERIFIED). |
| Even | Neither of the above | No effect. |

A mood ends when the gap falls below 150 Clout for 30 s, so moods do not flicker.
