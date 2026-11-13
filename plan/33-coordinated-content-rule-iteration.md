# 33. Coordinated content-gated rule iteration

Status: rules-owned, read-only toward `/workspace/hy3d`. This chapter does not create content, copy an asset, or claim a hash. hy3d owns all content and publishes `output/content-for-bota.json` / `.tsv` first with pooled-email generation, then with the relay. BOTA owns the rules and publishes `export/rule-demand.json` / `.tsv` before and after every rule pass.

## Ownership and evidence

| Question | Owner | Authority |
| --- | --- | --- |
| What a rule means | BOTA | `plan/`, `ROSTER.md`, `GALLERY.md`, `export/hero-registry.json` |
| Whether a model, structure, clip, prop, voice asset, destination or hash exists | hy3d | `/workspace/hy3d/output/content-for-bota.json` and its cited source manifests |
| Whether a content row may be called `available` | BOTA validator | `tools/validate-rule-demand.py`: a real published SHA-256 and an existing evidence path |
| Whether an identifier is historical or downstream | BOTA live validator | `tools/validate-integration-live.py --identifier-mode` |

A rule may name a required thing before the thing exists. It must not name a file that hy3d did not publish. `status: requested` means the rule implies the demand and hy3d has not supplied a hash-verified row. `status: blocked` means a known external condition prevents the asset. `status: available` means the row is `ready` in hy3d's contract and hash-verified. No rule pass may turn `requested` into `available` by optimism.

## Pass 1: the three chains are content gates, not a shopping list

The Receipt, Repost and Camera chains from `plan/16` are the comedy's audit trail. Each chain has exactly three beats, and each beat must be legible from a game state, a visible detail from the 25 gallery JPGs, and one punchline:

| Chain | Introduce | Misfile | Appeal / wipe |
| --- | --- | --- | --- |
| Receipt | A last hit or tower hit becomes a crumb invoice, grass-stain bill or shoulder-bag complaint. | The document appears on the wrong recap; the game state still earns gold and XP, but no Clout is invented for an unseen action. | Howard dates every prior document. The punchline is the filing date, not a new hero. |
| Repost | A Resell adds a `via` tag and a final final v3 memo. | The memo is misfiled under the next replay; Forever's loop keeps the same clip. | Gothgirl rewinds before the word vibe, so the appeal never claims the argument ended. |
| Camera | Bot Bernard dodges the portrait while `003` stands as monochrome stillness, a visual only. | Noscope brings orbit-grade optics to a no-scope. | Shoop wipes between takes; the wipe erases the cameraman, not the scoreboard. |

Rule: when a chain beat needs a clip, prop or model, the beat is a `rule-demand` row. The chain still reads as text with no asset. If hy3d supplies the asset, the text may gain a presentation cue; the rule, kit, Clout state and outcome do not change. This keeps `plan/16` funnier than a prop checklist and keeps the `003` image-only retired/reserve discrepancy intact.

## Pass 2: ambiguity resolution without promotion

The following ambiguities are resolved as rules. None changes a canonical engine value, a decision packet field, a null gate or an owner-decision:

| Ambiguity | Resolution | Still intentionally open |
| --- | --- | --- |
| Does a `ready` row become a rule? | No. It becomes evidence that a demanded asset can be presented. | Whether to change any numeric balance value remains owner-decision and `do_not_promote: true`. |
| Can an absent clip be faked with a gallery JPG? | No. A gallery JPG grounds visible detail; it is not a clip, model or audio hash. | Exact clip durations remain `UNVERIFIED` until a playable build. |
| Can a studio substitute become a BOTA hero? | No. It is a fallback content candidate. Active hero keys remain the 24 acronyms in `ROSTER.md`. | Which substitute maps to which cosmetic remains hy3d content, not BOTA rules. |
| Can a Spawn CDN name be copied into BOTA? | No. It is compatibility evidence for `reusable-data`. | Any future Spawn adapter needs owner approval. |
| Does the identifier inversion rewrite this export? | No. BOTA's canonical export keeps acronyms; oscraft BOTA artifacts move to full names/slugs while default-Dota heroes use acronyms. | The timing of oscraft's migration is owned by its agent. |

All `GUESS`, `UNVERIFIED`, `AMBIGUOUS`, `owner-decision` and `intentionally-open` markers keep their existing status. `export/engine-resolved` stays absent. `do_not_promote: true` remains on owner-decision and intentionally-open fields. Decisions in this chapter resolve interpretation only; they never promote a number.

## Pass 3: grounded nuance and humor

1. **Visible prosecution.** A joke may use a detail only if `GALLERY.md` or `export/image-references.json` records it. Neckbeard's crumb invoice belongs in a cargo pocket; Boomer's bill points at the silver can; Howard's appeal points at the plaid-shirt smile. If the JPG does not show it, the rule calls it a demand, not a prop.
2. **Three-beat escalation.** Running gags introduce, misfile and appeal exactly three times. A fourth repetition is a bug except in Forever's clip, where repetition is the named mechanic and the clip stays `requested` until hy3d publishes its hash.
3. **Game-state first.** Every announcer line, recap glyph and chain cue names the state it reacts to: last hit, deny, kill, tower damage, stage camp, Hype Spike, Markdown, Rebrand, Snapshot revive, Go Private or Stockpile destroyed. The joke never invents a state.
4. **Clout is an audience resource.** Reach, reveal and mood follow `plan/06`. A content row cannot add Clout, change a threshold or create a stat. A Lurker Cam prop can reveal; it cannot quietly become a Clout battery.
5. **Receipts are funny because they lose.** A denied creep gives no gold or XP to the enemy team and takes Clout from the nearest seeing enemy hero under `plan/06`. The recap may bill the crumb, but the economy row wins.
6. **Reposts are funny because they do not end.** Resell `via` tags, final final v3 memos and Snapshot revives are the same promise: the ledger is still open. The Stockpile win condition is the only final entry.
7. **Cameras are funny because they ask the wrong question.** Bot Bernard dodges the portrait, Noscope over-instruments a no-scope, Shoop wipes. The Camera Chain never answers whether the play was good; the scoreboard does.
8. **The 003 statue says nothing.** `gallery/003-gigachad.jpg` is monochrome stillness, impossible jaw gravity and one unbroken stride. It has no hero ID, kit, talent, voice line, spawn entry, draft option or banter pair. It is a retired visual reference, not a twenty-fifth playable hero.
9. **Owner-only shame.** Steam puffs, tiny house icons, Hyped-ended markers and Markdown name plates are cosmetic, self-only where `plan/16` says so, and never hide a stat. A content upgrade may change the puff's texture, not who sees it.
10. **Deadpan escalation.** The announcer may say `F.` for a Delivery Drone and `L + markdown.` for a team wipe, but the words aim at the play. No shipped joke names a retired hero, an original-game character or a real person.

## Pass 4: identifier inversion and live conformance

The owner's cross-project update inverts downstream identifiers: oscraft BOTA artifacts are expected to use full BOTA character names/slugs, while default-Dota hero IDs become acronyms. This export's established contract remains acronym-keyed. Therefore:

- `tools/validate-integration-live.py --identifier-mode acronym` is the historical contract for the current oscraft checkout.
- `tools/validate-integration-live.py --identifier-mode bota-fullname` is the new oscraft target. It compares full-name/slug keys and expects default-Dota hero IDs to be acronyms under `--default-dota-acronyms`.
- While oscraft is migrating, `UNAVAILABLE` and `DRIFT` are reported with exact paths and never converted into a success claim. A missing downstream file is unavailable; a present downstream file with the wrong identifier family is drift.
- `spawn-compatibility.json` keeps the `reusable-data` verdict. The inversion changes identifier expectations, not the fact that WONSCHWEPPIDYTIME uses scene rows, behavior modules and CDN names instead of a BOTA hero registry.

## Pass 5: iteration loop

For every rule pass:

1. Read hy3d's `content-for-bota.json` if present. If absent, read the fallback manifests and label the contract `UNAVAILABLE`.
2. Rebuild `export/rule-demand.json` / `.tsv` with `python3 tools/build-rule-demand.py`.
3. Run `python3 tools/validate-rule-demand.py`; every `available` row must have a real hy3d SHA-256 or an exact local rule/gallery hash.
4. Re-run `bash tools/check-bota-export.sh`, the focused decision/engine/apply validators, and both live identifier modes when oscraft is ready.
5. Refresh `export-status.json` with `python3 tools/bota-export-watch.py`, then refresh `SHA256SUMS.json`, `conformance.json`, docs and `manifest.json` so hashes and counts stay coherent.

The loop is continuous in the sense that no pass assumes the content contract is final. hy3d may publish pooled-email rows, then relay rows; BOTA reads the latest contract before each pass. The rules are stable enough to test, and the demand contract is live enough to follow hy3d.

## Pass 6: six-state resolution without promotion

The canonical demand contract is now `bota.rule-demand/v2`. Every row that was `requested` or `blocked` gets exactly one of six states: `available`, `requested-pooled-email`, `requested-relay`, `spawn-generated`, `owner-decision` or `intentionally-open`. Each state has a `nextActor` (`hy3d`, `wscheppity`, `owner` or `bota`), exact evidence and acceptance criteria. `available` still requires real hash-verified bytes; the other five states are honest work states, not guesses.

`export/content-request-queue.json` / `.tsv` is the prioritized, deduplicated queue for hy3d. It follows the owner sequence: pooled-email attempt first, relay fallback second, owner decision or intentionally-open rule third. `export/spawn-extraction-gaps.json` is the 100% upstream extraction ledger for wscheppity: verified local bytes are evidence, zero-byte/generated names are `spawn-generated` until exact HTTP status, content-type, body size and SHA-256 are captured. A CDN name is not content in BOTA; it is cross-project extraction evidence under `reusable-data`.

The Receipt/Repost/Camera chains remain text-first. A hash-verified CDN clip may prove that wscheppity extracted a generated-on-demand asset; it does not create a BOTA hero, change Clout, supply a voice line, or make `003` playable. `owner-decision` and `intentionally-open` rows keep `do_not_promote: true`, and `export/engine-resolved/` stays absent.

## Pass 7: live coordination watcher

`tools/watch-coordinated-queues.py` now recomputes every row in `export/content-request-queue.json` and `export/spawn-extraction-gaps.json` from live peer evidence. Its default is bounded at 10 minutes with a 10 s poll; `--once` is a single read-only pass. It reads hy3d `content-for-bota.json`, `content-demand-v2.json`, generation status, recovery watch and CDN probes; wscheppity extraction/CDN/HTTP evidence; `/workspace/extra` evidence when present; and oscraft `IDENTIFIERS.md`, `cross-contract-snapshot.json` and `bota_ui.json`. It writes only `export/coordination-status.json` / `.md`.

A row is `available` only with real hash-verified bytes. `spawn-generated` requires an exact HTTP/status/content-type/body-size/SHA-256 evidence record, including zero-body generated-on-demand probes; a missing peer path is `UNAVAILABLE`. `owner-decision` and `intentionally-open` rows keep `do_not_promote: true`. `export/owner-decision-brief.md` presents neutral options for those two rows only and applies nothing.
