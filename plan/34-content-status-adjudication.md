# 34. Content-status adjudication and chain escalation

Status: rules-owned. This is the second iteration after `plan/33`, triggered by hy3d publishing `output/content-for-bota.json` with 67 `ready` rows: 26 BOTA hero models (24 active plus two retired), 14 structures, 26 studio substitutes and one relay extra. The rows carry a category, slug, source, optimized path, destination, SHA-256, generation method and status. They are content evidence, not permission to change a rule.

## Status adjudication

| hy3d row | BOTA rule use | Demand status | Notes |
| --- | --- | --- | --- |
| `bota-hero`, 26 rows | Model evidence for the 24 active heroes plus the two retired heroes | `available` | Only when the SHA-256 matches a local optimized/source/destination file or a hash-verified destination record. The active hero key remains the canonical acronym in BOTA's export. |
| `structure`, 14 rows | Candidate geometry for rule-implied buildings and map furniture | `requested` for the exact BOTA prop | A `tree_of_life` GLB is evidence that hy3d can deliver a structure; it is not automatically a Tier 1 tower. A BOTA prop needs its own row before the rule can name a model. |
| `studio-substitute`, 26 rows | Relay fallback coverage while pooled-email content was unavailable | `available` as content, `requested` as BOTA rule mapping | A substitute may be presented as a fallback candidate; it cannot become a hero, kit, talent, voice row or active acronym. |
| `relay-extra`, 1 row (`doomer`) | Evidence of relay completion outside the 24-hero set | `available` as content, not a roster demand | The 24 active heroes and `003` image-only reserve remain the roster truth. |
| Spawn CDN candidate | Comparison evidence for `reusable-data` | `blocked` unless content-addressed and policy-satisfied | `/cdn/value.<sha256>.<ext>` names are not local BOTA assets. A generated-placeholder probe is not an upload. |

`available` is a proof word; `requested` is a demand word; `blocked` is an external-condition word. No rule may use `available` to mean "plausible", "close enough" or "hy3d once made something similar".

## Receipt/Repost/Camera adjudication

The three chains from `plan/16` and `plan/33` read as follows after the content pass:

1. **Receipt Chain.** The first beat is an in-game bill: Neckbeard's crumb invoice after a last hit, Boomer's grass-stain bill beside the silver can after a tower hit, Howard's incident report after a Markdown. The misfile beat puts the wrong date on the recap but never changes gold, XP, Clout or death state. The appeal beat dates every document. If a document prop or recap clip is not a `ready` hy3d row, the prop stays `requested`; the joke still works as text.
2. **Repost Chain.** The first beat adds a `via` tag and Grey's final final v3 memo on a Resell. The misfile beat queues the memo under a replay, so Snapshot and Rebrand argue about whether the ledger closed. The third beat is Gothgirl's pre-vibe rewind and Forever's clip: the clip repeats because that is the mechanic, not because the chain gets a fourth joke. No `vibe` is spoken in the shipped line.
3. **Camera Chain.** The first beat has Bot Bernard dodging the portrait while `003` stands as monochrome stillness and says nothing. The misfile beat has Noscope's goggle reviewing a no-scope with orbit-grade seriousness. The wipe beat is Shoop erasing the cameraman. A camera prop, transition clip or orbit graphic must be a `ready` row before presentation; otherwise the rule stays in scoreboard text and does not invent a model.

## Grounded substance from hy3d rows

- The hero rows let every active hero have a model demand without guessing a path. Each demand links to `content/bota-hero/<hy3d_slug>`. The BOTA registry keeps `nec`, `woj`, `blo` and the other acronyms; the downstream oscraft artifact may use `neckbeard`, `wojak`, `bloomer` and the other full slugs.
- The 14 structure rows are enough to prove hy3d's pooled-email pipeline produced geometry. They are not enough to rename a BOTA Tier 1 tower, Content Mill, Stockpile or Spawn Lounge. Rule-implied buildings therefore remain `requested` with a section citation.
- The 26 studio substitutes include creeps, ranged creeps, siege creeps and super creeps. Those are useful evidence for lane pressure, but the lane rules in `plan/03` still decide wave timing, siege frequency and upgrade caps. A content row cannot change `5 + 3.8 × level`, `every 30 s`, `every fifth wave` or `four upgrades at most`; all numeric values remain `UNVERIFIED`/`GUESS` under their existing decisions.
- The one `doomer` relay extra is not a twenty-seventh hero, not a Trend boss, not a voice line and not a `003` replacement. It stays in the content ledger.
- Spawn CDN probes are all generated placeholders in hy3d's contract. Under `export/spawn-compatibility.json`, those remain `blocked` for BOTA asset use. The `reusable-data` verdict is unchanged.

## Humor constraints tightened by the pass

1. **No prop by association.** A `tree_of_life` structure row does not make Ghillie's grass beard a tree. A `goblin_merchant` row does not turn the Back Alley Shop into a goblin. A `fountain_of_health` row does not turn Coffee into a fountain. The gallery JPG remains the visible-detail authority.
2. **No substitute biography.** Studio substitutes may appear as fallback geometry; they receive no hero name, no lore, no banter and no Receipt/Repost/Camera beat. Giving one a personality would be content ownership leaking into rules.
3. **No hash joke without a hash.** A caption may say `Receipt pending` or `Fact check pending`. It may not claim `verified`, `delivered`, `relayed` or `hash matched` unless the contract row is `ready` and hash-verified.
4. **No final word.** The Stockpile destruction line `Stall shut.` is the outcome. Repost and Camera gags may imply the recap continues, but no gag overrides the win condition.
5. **No stealth promotion.** `GUESS`, `UNVERIFIED`, `AMBIGUOUS`, `owner-decision` and `intentionally-open` values remain gated. This pass resolves presentation semantics only; `do_not_promote: true` and the absent `export/engine-resolved/` are preserved.

## Ambiguities resolved here

| Ambiguity | Resolution | Non-promotion |
| --- | --- | --- |
| Are hy3d's 14 structures BOTA towers? | No. They are ready structure content; exact BOTA buildings remain demands. | No structure count, HP, armor aura, gold or respawn value changed. |
| Are studio substitutes active heroes? | No. They are fallback content candidates. | No acronym, slot, kit, voice, talent, spawn or draft entry changed. |
| Is `doomer` a hero? | No. It is a relay-extra content row. | 24 active heroes and 25 gallery images remain. |
| Can a CDN candidate be an asset? | Only when content-addressed, policy-satisfied and hash-verified; current probes are blocked. | No `/cdn/` name copied into a BOTA rule or path. |
| Does `ready` content resolve a numeric rule? | No. Content status and balance confidence are separate axes. | All existing gates remain null/owner-decision/intentionally-open. |

## Pass result

After this pass, `export/rule-demand.json` / `.tsv` must be rebuilt from hy3d's latest contract and `python3 tools/validate-rule-demand.py` must prove that every `available` row has a real SHA-256. Then `bash tools/check-bota-export.sh`, both identifier modes where meaningful, the status watcher, and hash/document coherence checks run again. A failure in a downstream identifier mode is reported with its exact path; it is not hidden by calling the content pass successful.

## Live evidence pass

wscheppity's `.local/cdn/manifest.json` and `.local/cdn/manifest-all.json` are now read alongside hy3d's contract. The active CDN manifest can make a previously blocked Spawn name `available` when its local file exists, byte length matches, and SHA-256 matches. The all-name manifest is the 100% extraction scope: names with zero-byte/generated placeholders become `spawn-generated` gaps, with acceptance criteria requiring HTTP 200, content-type, exact body size and a published SHA-256. This does not convert a CDN name into a BOTA asset path; it only satisfies the owner's extraction requirement.

hy3d's `generation-status.json` and `studio-blocked-diagnosis.json` supply the relay-fallback evidence: pooled quota, service-side HTTP 500/no-worksId classification, `retryRecommended: false`, `quotaPreserved: 30`, and the exact future retry condition. A `requested-relay` row therefore means "after a recorded pooled attempt, use the quota-free relay path", not "pretend the service recovered". No studio substitute receives a hero biography, and no structure row is renamed into a BOTA tower by association.

## Watcher evidence pass

wscheppity's all-name CDN manifest now includes HEAD/GET request records and `.local/cdn/http/*` per-name HTTP evidence. A 200 GET with a positive body size and matching SHA-256 makes a row `available`; a generated-on-demand or zero-body probe with exact HTTP evidence stays `spawn-generated`, not `UNAVAILABLE`. hy3d's `content-demand-v2.json` supplies exact `endpointBlocked`, `ownerDecision` and `intentionallyOpen` rows; oscraft's `cross-contract-snapshot.json` proves 26 BOTA fullname IDs and 127 default-Dota acronym IDs. `/workspace/extra` has no extraction manifest yet, so the watcher records that exact path as `UNAVAILABLE` rather than inventing a world.
