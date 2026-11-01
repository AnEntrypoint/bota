# 26. First playable, cut list and checks

The first playable tests what is unique before it tests the classic MOBA basics. Every number here is UNVERIFIED until a build runs the checks below.

## First playable slice

**Goal:** show that Clout, the Late-game Clout carry mood and the Trend modifiers make matches different, and that the rest of the game can be built on top.

| Area | In the slice |
| --- | --- |
| Map | Short Form layout (section 14): two lanes per side, the river, both bases, one stage camp per side. |
| Heroes | Six: Grey (Drifter, Ranged nuker), Tinfoil (Drifter, Ranged nuker), Chudjak (Bulwark, Reach tank, initiator), Disaster (Firebrand, Hot-take initiator), Waffle (Bulwark, Reach tank, initiator), Ghillie (Stalker, Assassin, vision denial). |
| Clout | Earn, decay, Reach, Bull Run, Markdown on death with the 200 cap. |
| Mood | Front Runner, Underdog and Even (section 6). |
| Events | Breaking News, two events per match (section 12); the slice runs the 18:00 one. |
| Modifiers | Two from the pool: Cast Rush and Learn to Code. |
| Items | Lurker Cam, Spoiler Tag, Anon Mask, Confident Answer, Sticky Note, Ring Light and Drafted Note. |
| Presentation | LIVE dot, Clout bar, Stan, Bull Run and Resell signals, the Front Runner minimap icon, death recap (Markdown), Rebrand record, announcer lines for kills and Markdown. |

**Not in the slice:** Showrunner Draft (draft is a fixed pick order for the slice), the full talent trees, neutral items, Safe Spots, Chat Check, Go Private, Scalper, Seasons, spectator reactions, the other 18 of the 24 launch heroes.

**Exit criteria:** the runnable checks below pass across at least 200 matches (UNVERIFIED), and the eight playtest scenarios each meet their Pass clause.

## Cut list

| Item | v1 | Later | Why |
| --- | --- | --- | --- |
| Heroes | 6 | 24 launch, then 112 | Test the mechanics before the roster. |
| Boosts | Demand Boost, Bounty, Dank Goods (Haste) | Dank Goods (Illusion, Invisibility, Regeneration), Sweat Mode | Fewer boosts make the Clout effects easier to read. |
| Trend modifiers | 2 | 8 | Compare two before adding more. |
| Talents | None | Full sets from section 21 | Power growth comes after the base kits are tested. |
| Neutral items | None | Section 21 | Tested after camps are proven. |
| Safe Spots | None | Section 21 | Not needed to test Clout. |
| Chat Check | None | Section 21 | Vision is covered by wards. |
| Go Private | None | Section 3 | Building defence is tested later. |
| Resell chain | Yes, cap 5 stacks | Full rules | It is a core system, so it is included at full cap. |
| Gags | Death recap, Rebrand record, announcer | All others | Gags are presentation, not balance. |
| Seasons | None | Section 21 | Not part of a test. |

## Playtest scenarios

Run each scenario in the build. Record the result, the time taken and any sign that a rule was unreadable.

1. **Clout comeback.** One team gets 300 Clout ahead for 30 s, then the gap drops below 150 for 30 s. Does the Front Runner mood show on the minimap? Pass: each mood holds for 30 s, C4 records zero flips in any 30 s window, and the Front Runner icon shows on the minimap for 20 s.
2. **Lurk ambush.** Tinfoil waits unseen for 8 s, then uses Foil Mention. Can a player see from the screen alone that it was unseen? Pass: no LIVE dot, and at least 4 of 5 testers answer yes when asked whether they could tell it was unseen from the screen alone (UNVERIFIED count).
3. **Markdown cap.** A hero dies with 400 or more Clout. Pass: at most 200 Clout moves, so the 200 cap binds exactly at 400 Clout, and the split goes 50% to the killer and 50% equally among assists (UNVERIFIED; plan/06 Markdown row).
4. **Trend modifier fight.** Cast Rush and Learn to Code both on offer. Pass: C1 and C2 hold (see Runnable checks).
5. **Breaking News contest.** Both teams have heroes in the zone. Pass: C3 records zero capture progress.
6. **Stage camp.** The same pull is made watched and unwatched. Pass: only the watched pull gives Clout.
7. **Rebrand while Bullish.** A Bullish hero dies. Pass: the Bullish-ended marker shows, and Rebrand swaps it for Rebranded.
8. **Read check.** Grayscale and each colorblind preset show LIVE, Stan, Bull Run, Markdown and Resell. Pass: at least 4 of 5 observers (UNVERIFIED) name each signal without its color under deuteranopia, protanopia and tritanopia.

## Runnable checks

Each check has an ID, an input, an output and a threshold. Thresholds come from section 19, plan/12 (C3, Breaking News) and plan/06 (C4, 30 s window).

| ID | Check | Input | Output | Pass |
| --- | --- | --- | --- | --- |
| C1 | Modifier win rate | Matches grouped by picked modifier | Win rate per modifier | 45 to 55% for each, with at least 200 matches per modifier (UNVERIFIED) |
| C2 | Modifier pick rate | Offers and picks | Share of offers picked | At most 65% |
| C3 | Breaking News contest | Matches with both teams in the zone | Capture progress made | Zero |
| C4 | Mood flicker | Mood flips with timestamps | Flips within 30 s of the last flip | Zero |
| C5 | Markdown cap | Markdown events | Clout moved per death | At most 200 |
| C6 | Disable cap | Hard disables per team | Fourth disable in any 10 s window | Shortened to 0.5 s every time |
| C7 | Comeback | Matches where a team is 10,000 gold behind at 15:00 | Share of those matches the behind team wins | At least 10% (UNVERIFIED) |
| C8 | Rename regression | Win rate before and after a rename | Difference in percentage points | Within 1 percentage point, with at least 200 matches in each arm (UNVERIFIED) |
| C9 | Chat mute | Mutes in the first 10 minutes | Share of players | At most 25% of players mute; above 25%, rotate the phrase pool |
| C10 | Breaking News capture rate | Captures per event | Capture rate | At least one per event; no team above 70% (UNVERIFIED) |
| C11 | Clout-only rule (reading check) | Effect text of every Clout effect | Clout effects that change damage or armour directly; the Stan buff is Reach and out of scope | Zero |

C11 checks the Clout-only rule (decision 9 in section 20) by reading the effect text of every Clout effect; it is a reading check, not a runtime check.
