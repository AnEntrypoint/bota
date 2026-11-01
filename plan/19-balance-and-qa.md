# 19. Balance and QA
Every hero plays against the others in fights. Each archetype has a fixed power budget, at least one hard counter and at least one soft counter. Hero numbers are set from these budgets.

### Archetype budgets

| Archetype | Role | Early power | Late power | Disable budget | Strong against | Weak against | Hard counter |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Clout carry | Clout carry | Low | High | Low | Offline sustain | Reach tank, initiator, Repost healer, buffer | Reach tank, initiator |
| Assassin, vision denial | Assassin, vision denial | High | Medium | Low | Clout carry | Utility, zone control, Repost healer, buffer | Utility, zone control |
| Harasser, zoner | Harasser, zoner | Medium | Medium | Medium | Repost healer, buffer | Reach tank, initiator | Reach tank, initiator |
| Late-game Clout carry | Late-game Clout carry | Low | High | Low | None | Hot-take initiator, Assassin, vision denial | Hot-take initiator |
| Ranged nuker | Ranged nuker | High | Medium | Low | Late-game Clout carry | Assassin, vision denial, Reach tank, initiator | Assassin, vision denial |
| Repost healer, buffer | Repost healer, buffer | Medium | Medium | Medium | None | Hot-take initiator, Ranged nuker | Hot-take initiator |
| Reach tank, initiator | Reach tank, initiator | Medium | Medium | High | Clout carry, Late-game Clout carry, Tethered support, dueler | Ghost-account summoner, Utility, zone control | Ghost-account summoner |
| Ghost-account summoner | Ghost-account summoner | Medium | High | Low | Reach tank, initiator | Utility, zone control, Hot-take initiator | Utility, zone control |
| Hot-take initiator | Hot-take initiator | High | Low | High | Repost healer, buffer | Reach tank, initiator | Reach tank, initiator |
| Utility, zone control | Utility, zone control | Medium | High | Medium | Assassin, vision denial, Ghost-account summoner | Ranged nuker | Ranged nuker |
| Tethered support, dueler | Tethered support, dueler | Medium | Medium | Medium | Clout carry | Hot-take initiator | Hot-take initiator |
| Offline sustain | Offline sustain | Low | High | Low | Hot-take initiator | Assassin, vision denial, Utility, zone control | Assassin, vision denial |

### Archetype tiers (UNVERIFIED)

The tier sets the total stat and ability points before the ±10% shift.

| Tier | Stat points | Ability points | Archetypes |
| --- | --- | --- | --- |
| 1 | 100 | 24 | Clout carry; Assassin, vision denial; Harasser, zoner; Hot-take initiator |
| 2 | 90 | 20 | Late-game Clout carry; Ranged nuker; Repost healer, buffer; Reach tank, initiator; Ghost-account summoner; Utility, zone control; Tethered support, dueler |
| 3 | 80 | 16 | Offline sustain |

Allocation: start at the tier total, then shift up to ±10% by attribute and range. The shifted total stays within the tier total. All values are UNVERIFIED.

### Fight rules

| Rule | Value |
| --- | --- |
| Power budget | Total stats and ability points fixed by archetype tier, then shifted within ±10% by attribute and range |
| Hard disable cap | 3 per team in any 10 s window. A fourth is shortened to 0.5 s. |
| Counter coverage | Every hero has at least one hard counter and at least one soft counter, drawn from the table above |
| Ratio ceiling | At most 50% of Clout moves, and at most 200 Clout in total per death |
| Go Viral limit | One Go Viral active per team at a time |
| Repost cap | Five stacks per target. Stacks from one source do not stack twice. |

### Stat sheet

- HP, damage, armor and mana are set to the archetype tier.
- Attack time (BAT) and turn rate are set per hero, and are the main tool for a hero's feel.
- Movement speed is capped at 522.

### Balance process

| Stage | Measure | Action |
| --- | --- | --- |
| Stat sheet | Power budget per hero | Set HP, damage, armor and mana to the archetype tier |
| Bracket test | Win rate by archetype, by bracket | Retune any archetype outside 47 to 53% |
| Matchup test | Win rate for each hard counter pair | Retune any pair outside 45 to 55% |
| Pick and ban test | Pick rate and ban rate per hero | Retune any hero above 3× the average pick or ban rate |
| Snowball check | Comeback rate after a 10,000 gold deficit | Adjust Ratio and decay if comebacks fall below 10% |

### QA gates

A build passes QA when:

1. Every hero renders at gameplay zoom, and passes the blind silhouette test.
2. Every ability has a cast point, an impact effect and a telegraph (where the table calls for one).
3. Every item's tooltip reads without its flavor line.
4. Every signal (LIVE, Stan, Go Viral, Ratio, Repost) reads in grayscale and under each colorblind preset.
5. Every gag in section 16 fires on its trigger, and none of them hides a signal.
6. The 10,000 gold snowball check and the bracket test are inside their targets on the current patch.

### New-system checks

Targets for the first simulated and played matches. These are thresholds to test, not results. Runnable versions of the C-checks, with IDs and inputs, are in plan/26 (C1 to C10). The Sweat Mode and rename checks are tracked by hand until a build exists.

| System | Check | Pass |
| --- | --- | --- |
| Trend modifiers (8, 2 offered per kill) | Win rate of the team that picks each modifier | 45 to 55% for every modifier |
| Learn to Code, Speedrun, Storytime, Get Ready With Me | Pick rate when offered against another modifier | No modifier picked above 65% of offers |
| Sweat Mode boost | Share of teamfights opened within 10 s of pickup | Under 40% |
| Loaded gags | Players who mute chat in the first 10 minutes | Tracked per patch. Phrase pool rotates when above 25%. |
| Renamed abilities | Hero win rate before and after the rename pass | Within 1 point. A rename never changes a number. |
| Breaking News capture rate | Captures per event | At least one per event; no team above 70% of events (UNVERIFIED). |
