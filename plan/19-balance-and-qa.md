# 19. Balance and QA
Every hero plays against the others in fights. Each archetype has a fixed power budget and at least one hard counter. Hero numbers are set from these budgets.

### Archetype budgets

| Archetype | Early power | Late power | Disable budget | Strong against | Weak against | Hard counter |
| --- | --- | --- | --- | --- | --- | --- |
| Clout carry | Low | High | Low | Offline sustain | Reach tank, initiator, Resell healer, buffer | Reach tank, initiator |
| Assassin, vision denial | High | Medium | Low | Clout carry | Utility, zone control, Resell healer, buffer | Utility, zone control |
| Harasser, zoner | Medium | Medium | Medium | Resell healer, buffer | Reach tank, initiator | Reach tank, initiator |
| Late-game Clout carry | Low | High | Low | None | Hot-take initiator, Assassin, vision denial | Hot-take initiator |
| Ranged nuker | High | Medium | Low | Late-game Clout carry | Assassin, vision denial, Reach tank, initiator | Assassin, vision denial |
| Resell healer, buffer | Medium | Medium | Medium | None | Hot-take initiator, Ranged nuker | Hot-take initiator |
| Reach tank, initiator | Medium | Medium | High | Clout carry, Late-game Clout carry, Tethered support, dueler | Ghost-account summoner, Utility, zone control | Ghost-account summoner |
| Ghost-account summoner | Medium | High | Low | Reach tank, initiator | Utility, zone control, Hot-take initiator | Utility, zone control |
| Hot-take initiator | High | Low | High | Resell healer, buffer | Reach tank, initiator | Reach tank, initiator |
| Utility, zone control | Medium | High | Medium | Assassin, vision denial, Ghost-account summoner | Ranged nuker | Ranged nuker |
| Tethered support, dueler | Medium | Medium | Medium | Clout carry | Hot-take initiator | Hot-take initiator |
| Offline sustain | Low | High | Low | Hot-take initiator | Assassin, vision denial, Utility, zone control | Assassin, vision denial |

Disable budget counts the hard disables (decision 37) that one hero of the archetype lands in any 10 s window: Low 1, Medium 2, High 3 (UNVERIFIED). The fourth disable in a team's 10 s window is shortened to 0.5 s (C6).

Strong against and Weak against are separate claims and need not mirror. The Matchup test (below) checks every named pair.

### Archetype tiers (UNVERIFIED)

The tier sets the total stat points and the ability power budget before the ±10% shift. Ability power is spent in ranks: a hero spends at most 15 ranks (plan/07), and each tier value is the ranks it may spend (UNVERIFIED).

| Tier | Stat points | Ability power | Archetypes |
| --- | --- | --- | --- |
| 1 | 100 | 15 | Clout carry; Assassin, vision denial; Harasser, zoner; Hot-take initiator |
| 2 | 90 | 12 | Late-game Clout carry; Ranged nuker; Resell healer, buffer; Reach tank, initiator; Ghost-account summoner; Utility, zone control; Tethered support, dueler |
| 3 | 80 | 9 | Offline sustain |

Allocation: start at the tier total, then shift up to ±10% by attribute and range. A shift up on one attribute is paid for by an equal shift down on others, so the shifted total equals the tier total. All values are UNVERIFIED.

### Fight rules

Numbers in this section are UNVERIFIED.

| Rule | Value |
| --- | --- |
| Power budget | Total stats and ability points fixed by archetype tier, then shifted within ±10% by attribute and range |
| Counter coverage | Every archetype row names at least one hard counter in its Hard counter cell |
| Markdown ceiling | Rule in plan/06 (Markdown on death and its cap) |
| Hype Spike limit | None. Each Hyped hero runs its own 20 s Hype Spike and pays its own global reveal. |
| Resell cap | Rule in plan/08 (Resell chain, max stacks and stacking) |

### Stat sheet

- HP, damage, armor and sigma per tier, as totals at level 1 (UNVERIFIED): tier 1 has 700 HP, 55 damage, 4 armor and 300 sigma; tier 2 has 630, 50, 3 and 270; tier 3 has 560, 45, 2 and 240.
- Attack time (BAT) and turn rate are set per hero, and are the main tool for a hero's feel.
- Movement speed is capped at 522 (UNVERIFIED; not checked against 6.88g).

### Balance process

Numbers in this section are UNVERIFIED.

| Stage | Measure | Action |
| --- | --- | --- |
| Stat sheet | Power budget per hero | Set HP, damage, armor and sigma to the archetype tier |
| Bracket test | Win rate by archetype, by bracket (a bracket is one of three equal groups of matches, sorted by average Clout at 10:00; UNVERIFIED) | Retune any archetype outside 47 to 53% (UNVERIFIED, with at least 200 matches per archetype per bracket) |
| Matchup test | Win rate for each hard counter pair (counter side) and each strong or weak pair | Retune a hard counter pair below 55% or above 65%, and any strong or weak pair outside 45 to 55% (UNVERIFIED) |
| Pick and ban test | Pick rate and ban rate per hero, over Showrunner Draft matches only (at least 200 matches; UNVERIFIED) | Retune any hero above 3× the average pick or ban rate |
| Body and luminance test | Body percentages from plan/22 and the head-to-body luminance delta from plan/17, read from the grayscale capture | Fail any hero outside the plan/22 percentages or under a 30% luminance delta (UNVERIFIED) |
| Comeback check | Comeback rate after a 10,000 gold deficit | Adjust Markdown and decay if comebacks fall below 10% |

### QA gates

Testers are ten players who have not played the build; observers are five of them, chosen at random and shown the grayscale capture. A build passes QA when:

1. Every hero renders at gameplay zoom, and passes the blind silhouette test in plan/17 (90% or better).
2. Every ability has a cast point and an impact effect.
3. Every item's tooltip shows its stat and effect lines with the flavor line hidden, and at least 9 of 10 testers (UNVERIFIED) name the effect.
4. Every signal (LIVE, Stan, Hype Spike, Markdown, Resell) is named by at least 4 of 5 observers (UNVERIFIED) in grayscale, at minimap size, and under each colorblind preset.
5. Every gag in section 16 fires on its trigger, and none of them hides a signal, which 4 of 5 observers confirm (UNVERIFIED).
6. The 10,000 gold Comeback check and the bracket test are inside their targets on the build under test (named by version or commit at each run).

### New-system checks

Targets for the first simulated and played matches. These are thresholds to test, not results. Every number in this section is UNVERIFIED. Runnable versions of the C-checks, with IDs and inputs, are in plan/26 (C1 to C11). The Sweat Mode check is tracked by hand until a build exists; C8 is runnable.

| System | Check | Pass |
| --- | --- | --- |
| Trend modifiers (8, 2 offered per kill) | Win rate of the team that picks each modifier | 45 to 55% for every modifier, with at least 200 matches each (plan/26 C1) |
| Every modifier in the plan/12 table (eight) | Pick rate when offered against another modifier | No modifier picked above 65% of offers |
| Sweat Mode boost (Later: deferred by plan/26, not measured in the first playable) | Share of teamfights opened within 10 s of pickup, where a teamfight opens at the first hero-on-hero damage | Under 40% |
| Loaded gags | Players who mute chat in the first 10 minutes | At most 25% of players mute; above 25%, rotate the phrase pool. Tracked per patch. |
| Renamed abilities | Hero win rate before and after the rename pass | Check C8 in plan/26. A rename never changes a number. |
| Breaking News capture rate | Captures per event | Check C10 in plan/26. |
