# Brainrot of the AI - BotA: Complete Game Bible

Nov 2, 2026 · @Admin

## Contents

- [1. Scope](01-scope.md)
- [2. Vision and pillars](02-vision-and-pillars.md)
- [3. Core loop and win condition](03-core-loop-and-win-condition.md)
- [4. Map](04-map.md)
- [5. Economy](05-economy.md)
- [6. Clout](06-clout.md)
- [7. Heroes and attributes](07-heroes-and-attributes.md)
- [8. Combat rules](08-combat-rules.md)
- [9. Launch hero kits](09-launch-hero-kits.md)
- [10. Remaining hero kits](10-remaining-hero-kits.md)
- [11. Items](11-items.md)
- [12. Neutrals, boosts, The Trend and Snapshot](12-neutrals-boosts-the-trend-and-snapshot.md)
- [13. Vision and fog](13-vision-and-fog.md)
- [14. Draft and modes](14-draft-and-modes.md)
- [15. Roster and role families](15-roster-and-archetypes.md)
- [16. Humor and tone](16-humor-and-tone.md)
- [17. Presentation and readability](17-presentation-and-readability.md)
- [18. Asset manifest and audio](18-asset-manifest-and-audio.md)
- [19. Balance and QA](19-balance-and-qa.md)
- [20. Open questions, sources and decisions](20-open-questions-sources-and-decisions.md)
- [21. Systems added back](21-systems-added-back.md)
- [22. Art direction](22-art-direction.md)
- [23. Voice and banter](23-voice-and-banter.md)
- [24. Power tier draft](24-power-tier-draft.md)
- [25. Engine data plan](25-engine-data-plan.md)
- [26. First playable, cut list and checks](26-first-playable-cut-list-and-checks.md)
- [27. GM skills and spawn plan](27-gm-skills-and-spawn-plan.md)
- [28. Owner decision sheet](28-owner-decision-sheet.md)
- [29. Phase 1 audit](29-phase1-audit.md)
- [30. SSE notifications reader spec](30-sse-notifications-reader-spec.md)
- [31. Spawn events reader spec](31-spawn-events-reader-spec.md)
- [32. Git notes fetch spec](32-git-notes-fetch-spec.md)
- [33. Coordinated content-gated rule iteration](33-coordinated-content-rule-iteration.md)
- [34. Content-status adjudication and chain escalation](34-content-status-adjudication.md)
- [35. Continuous iteration ledger](35-continuous-iteration-ledger.md)

## Canonical character authority

`GALLERY.md` has 25 generated images: the 24 active heroes plus `003`, and is the authority for visual grounding. `ROSTER.md` has 24 active heroes, `001`, `004` through `010`, and `012` through `027`, and is the authority for the playable roster. Slots `002 Chad` and `011 Karen` were retired by the owner and are excluded from shipped prose, kits, talents, voice lines, spawn entries and draft options. `003 Gigachad` has a generated gallery image but is retired/reserve and is not a playable hero. Slots `028` through `032` have no gallery images and are not part of the game plan.

Every hero named anywhere in `plan/00` through `plan/35` must be one of those 24 active heroes. Reserve, retired, original-game parity, and legacy meme names are excluded from shipped prose; `003` is a documented visual-reference status, never an active character. The gallery is therefore 25 images for looking; the roster is 24 heroes for playing.

`plan/33`, `plan/34` and `plan/35` are the live coordination contracts for rule iteration: hy3d owns content with pooled emails then the relay, BOTA owns rules, and `export/rule-demand.json` / `.tsv` is rebuilt before each pass. It preserves the Receipt/Repost/Camera chains, the `003` image-only reserve, canonical null gates and identifier-mode-aware downstream conformance.
