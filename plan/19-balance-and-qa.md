# 19. Balance and QA
Every hero plays against the others in fights. Each archetype has a fixed power budget, at least one hard counter and at least one soft counter. Hero numbers are set from these budgets.

### Archetype budgets

| Archetype | Role | Early power | Late power | Disable budget | Strong against | Weak against | Hard counter |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Clout carry | Clout carry | Low | High | Low | Tethered support, dueler, Jungler, sustain | Tank, initiator, Healer, buffer | Tank, initiator, Assassin, vision denial |
| Assassin, vision denial | Assassin, vision denial | High | Medium | Low | Clout carry | Utility, zone control, Healer, buffer | Utility, zone control |
| Harasser, zoner | Harasser, zoner | Medium | Medium | Medium | Healer, buffer | Tank, initiator | Tank, initiator |
| Late-game carry | Late-game carry | Low | High | Low | Ranged nuker | Burst initiator, Assassin, vision denial | Burst initiator |
| Ranged nuker | Ranged nuker | High | Medium | Low | Late-game carry | Assassin, vision denial, Tank, initiator | Assassin, vision denial |
| Healer, buffer | Healer, buffer | Medium | Medium | Medium | Harasser, zoner | Burst initiator, Ranged nuker | Burst initiator |
| Tank, initiator | Tank, initiator | Medium | Medium | High | Clout carry, Late-game carry, Tethered support, dueler | Illusionist, summoner, Utility, zone control | Illusionist, summoner |
| Illusionist, summoner | Illusionist, summoner | Medium | High | Low | Tank, initiator | Utility, zone control, Burst initiator | Utility, zone control |
| Burst initiator | Burst initiator | High | Low | High | Healer, buffer, Jungler, sustain | Tank, initiator | Tank, initiator |
| Utility, zone control | Utility, zone control | Medium | High | Medium | Assassin, vision denial, Illusionist, summoner | Ranged nuker | Ranged nuker |
| Tethered support, dueler | Tethered support, dueler | Medium | Medium | Medium | Clout carry | Burst initiator | Burst initiator |
| Jungler, sustain | Jungler, sustain | Low | High | Low | Burst initiator | Assassin, vision denial, Utility, zone control | Assassin, vision denial |

### Fight rules

| Rule | Value |
| --- | --- |
| Power budget | Total stats and ability points fixed by archetype tier, then shifted within ±10% by attribute and range |
| Hard disable cap | 3 per team in any 10 s window. A fourth is shortened to 0.5 s. |
| Counter coverage | Every hero has one hard counter and one soft counter, drawn from the table above |
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
