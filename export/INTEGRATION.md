# BOTA engine integration contract

This is the handoff contract for downstream `oscraft` / `wscheppity` work. It is grounded only in the finished export and decision layer. It does not change creative text, invent canon, or promote uncertain values.

## Authority

Required input files:

- `export/hero-registry.json`
- `export/hero-kits.json`
- `export/hero-voice.json`
- `export/image-references.json`
- `export/decisions.json`

Canonical validation commands:

- `python3 tools/validate-export.py`
- `python3 tools/validate-export.py --decisions`
- `python3 tools/validate-export.py --integration`

## Identifiers

The engine `hero_id` **must** be a lowercase three-letter acronym matching `^[a-z]{3}$`. The exact active set is:

`nec, cha, woj, blo, tra, boo, coo, gon, spu, kar, how, san, lan, fin, wil, nos, din, ecc, bot, sho, npc, for, col, gre, ghi, got`

Full names, filename slugs, numeric slots, retired/reserve names, and `001..032` numeric IDs are never active keys. `display_name` is non-key provenance only. An old slug such as `001-neckbeard` may appear only inside a portrait/source path.

## 003 discrepancy

`gallery/003-gigachad.jpg` exists, but `003` is **image-only retired/reserve**. It has no active acronym, registry row, kit, voice entry, spawn list, draft option, or talent. Its only allowed use is as a visual reference for `cha`'s ultimate. The active roster is 26 heroes; the gallery has 27 images.

## Canonical versus decision-gated fields

Canonical fields are listed in `integration-contract.json#field_semantics.canonical`. They include `hero-registry.json#acronym_order`, active slots, portrait paths, four-ability kit rows, voice entries, image references, and the decision marker scan.

Decision-gated fields are **not canon** until their decision record says so. `GUESS`, `UNVERIFIED`, and `AMBIGUOUS` values must not be silently promoted. Do not silently promote GUESS, UNVERIFIED, or AMBIGUOUS values.. Downstream must read `decisions.json` and obey the confidence label:

- `resolved-from-plan`: use only the stated implementation default.
- `owner-decision`: `do_not_promote: true`; neutral options remain open.
- `intentionally-open`: `do_not_promote: true`; the plan deliberately lacks a discriminator or engine support.

Owner decisions: `default_damage_types, forever_eternal_loop_clip, sigma_value_tiers, voice_cooldown_8s, wojak_sorrowful_cancel_threshold`.

Intentionally open: `ability_3_passive_vs_aura_cost, cross_hero_hook_guesses`.

## Counts

| Item | Expected |
|---|---:|
| Active heroes | 26 |
| Gallery images | 27 |
| Active gallery images | 26 |
| Ability rows | 104 |
| Voice rows | 50 |
| Decisions | 12 |
| Covered markers | 169 / 169 |
| Hashed export files | 25 |

## Conformance fixture

`export/conformance.json` contains the exact acronym-to-slot mapping, required presence paths, expected counts, SHA-256 hashes copied from `export/SHA256SUMS.json`, allowed optional/ignored paths, and `do_not_promote` IDs. `python3 tools/validate-export.py --integration` checks live export state against this fixture.
## Live cross-project conformance

`python3 tools/validate-integration-live.py` is a **read-only** check against `/workspace/oscraft/scenarios/bota/`. It reads current files as they are, never writes to oscraft, and does not require oscraft to be idle. `--identifier-mode acronym` is the historical contract; `--identifier-mode bota-fullname --default-dota-acronyms` is the owner's identifier inversion target. The validator compares UI keys, generated Lua keys, mapping provenance, model files and `bota-skinned.json` slot/hash rows against `export/conformance.json` and `hero-registry.json`.

Expected live result for the committed oscraft target: `IDENTIFIER_MODE=bota-fullname`, `CROSS_PROJECT_KEY_DIFF=[]`, `MODEL_PARSE_COUNT=26`, and `LIVE INTEGRATION: PASS`. Against a migrated checkout, historical acronym mode truthfully reports `UNAVAILABLE`/`DRIFT` with exact paths. If oscraft is mid-write and a file is missing or unreadable, the validator prints `UNAVAILABLE`; if keys, slots, hashes or model skin data differ, it prints `DRIFT`. Neither condition crashes or reports success.
## Generated engine-data view

`python3 tools/build-engine-data.py` deterministically derives `export/engine/heroes.json`, `abilities.json`, `voice.json`, `portraits.json`, and `manifest.json` from the seven export/contract inputs only. This view is safe for engine consumption: `resolved-from-plan` data may be emitted as values, while `owner-decision`, `intentionally-open`, and any `GUESS`/`UNVERIFIED`/`AMBIGUOUS` field is emitted as `null` with `decisionId`, `status`, `options`, `source`, and `do_not_promote: true`. Recommendations are never silently promoted.

`python3 tools/validate-engine-data.py` checks the generated files, counts, hashes, acronym keys, 003 retired visual note, decision gates, and JSON parsing. The build is deterministic: two consecutive runs must be byte-identical.
## Owner decision packet and opt-in overlays

`export/DECISION-PACKET.md` and `export/decision-packet.json` compress the 425 null-gated engine fields into 12 decisions. `export/field-index.json` and `export/field-index.tsv` hold every exact field path. Recommendations are recorded but **not applied by default**; canonical `export/engine/` stays null-gated.

`python3 tools/apply-decision.py --decision-id ID --option VALUE --dry-run` prints the exact change plan and writes nothing. A non-dry apply requires `--apply --confirm-owner-decision`; intentionally-open decisions additionally require `--confirm-intentionally-open`. Any non-dry apply writes only to `export/engine-resolved/`, with an audit record, and leaves canonical engine data untouched. `python3 tools/validate-decision-packet.py` proves packet coverage, no leaks, and dry-run safety.
## Reversible apply audit

`export/APPLY-GUIDE.md` gives the exact opt-in commands. Confirmed applies write only `export/engine-resolved/` overlays and `<decision-id>.audit.json` records. Canonical `export/engine/` is never overwritten, and deleting the overlay directory reverts the apply. `python3 tools/validate-apply-mechanism.py` proves this in an isolated temp workspace, including dry-run safety, confirmation refusals, audit contents, no bulk apply, canonical byte identity, and cleanup.
## Single verification entrypoint

Run `bash tools/check-bota-export.sh` for the full deterministic pipeline: roster/gallery generators, two engine builds with byte-identical comparison, all validators, the temp-workspace apply mechanism test, SHA-256 integrity, identifier scan, and report-only `git status`. `python3 tools/check-bota-export-clean.py` proves the same pipeline from a clean temp workspace without `.git`, recreates `export/engine/`, and compares its five files byte-for-byte with the real generated data. Live oscraft validation is included in temp mode through `validate-integration-live.py --oscraft-root`, using a read-only symlink, so no check is skipped.
## Status watch

`python3 tools/bota-export-watch.py` is the lightweight drift watch. It runs `bash tools/check-bota-export.sh` once, parses all 15 labeled check results, reads the key manifests, confirms `export/engine-resolved/` is absent and canonical engine data is unchanged, and writes `export/export-status.json`. It does not apply decisions, write to oscraft, or create overlays. `python3 tools/validate-export-status.py` validates the report, hashes, counts, identifiers, and staleness; `export/STATUS.md` is the human snapshot.
## Spawn world compatibility (read-only report)

`export/SPAWN-COMPATIBILITY.md` and `export/spawn-compatibility.json` record a conservative cross-project verdict for `/workspace/wscheppity`: **reusable-data**, not the same game. The Spawn world is a three.js frog sitcom with scene rows, behavior modules and `/cdn/` asset names; BOTA is a 26-acronym MOBA export. Only descriptive metadata or humor/voice flavor could be reused through a future owner-approved adapter. `python3 tools/validate-spawn-compatibility.py` re-checks both trees read-only and proves wscheppity `git status --short` is unchanged.

## Coordinated rule demand

`plan/33-coordinated-content-rule-iteration.md` defines the content/rules boundary. hy3d owns content and publishes `/workspace/hy3d/output/content-for-bota.json` first with pooled emails and then with the relay. BOTA owns rules and rebuilds `export/rule-demand.json` / `.tsv` before every pass. `python3 tools/validate-rule-demand.py` checks all 26 active heroes, kits, voice, images, the `003` image-only reserve, rule-implied props/structures/clips, Spawn CDN evidence, identifier inversion, and real SHA-256 provenance. `available` never means guessed; `requested`/`blocked` degrade honestly. Canonical engine null gates and `do_not_promote: true` are unchanged.

## Six-state request queues

`python3 tools/build-rule-demand-v2.py` reads hy3d content/generation/blocker manifests and wscheppity extraction/CDN manifests read-only, then publishes `export/rule-demand.json` / `.tsv` (`bota.rule-demand/v2`), `export/content-request-queue.json` / `.tsv` for hy3d, and `export/spawn-extraction-gaps.json` for wscheppity. `python3 tools/validate-request-queues.py` checks that every prior requested/blocked row is represented exactly once in an actionable queue or is `available`, that queue rows carry stable IDs, nextActor, plan citations, evidence and acceptance criteria, and that no asset hash is invented. `owner-decision` and `intentionally-open` rows preserve `do_not_promote: true`; canonical engine null gates are unchanged.

## Live coordination status

`python3 tools/watch-coordinated-queues.py --once` reads hy3d content/demand/generation/recovery/probe evidence, wscheppity extraction/CDN/HTTP evidence, `/workspace/extra` evidence when present, and oscraft identifier snapshots. It writes `export/coordination-status.json` / `.md` with per-peer counts, per-row recomputed status, exact evidence paths and nextActor queue counts. The default mode is bounded at 10 minutes with a 10 s poll and never writes to peers. `python3 tools/validate-coordination-status.py` checks counts, no orphan queue rows, real available hashes, exact HTTP evidence for `spawn-generated`, decision IDs for gated rows, identifier inversion and the absent `export/engine-resolved/`. `export/owner-decision-brief.md` is generated from the two gated rows only and applies nothing.

## Coordination auto-refresh

`export/AUTO-REFRESH.md` documents `python3 tools/auto-refresh-coordination.py --once`, the bounded default loop, peer-change triggers, the strict no-promotion rule, and `python3 tools/validate-auto-refresh.py`. `export/coordination-auto-refresh.json` records before/after counts, exact peer manifest hashes, all validator commands and `ok`. `extra` is a first-class extraction peer via `/workspace/extra/.local/extraction-manifest.json` and CDN manifests; its `extraction-contract.json` is reported as `UNAVAILABLE` when absent. No peer project is written.

## Owner dashboard and actor backlog

`export/PROGRESS-DASHBOARD.md` and `export/progress-dashboard.json` summarize per-agent status, exact source paths, verified commands/exit codes, unresolved rows by nextActor, top blocked reasons and separately highlighted owner-decision / intentionally-open rows. `export/actor-backlog.json` / `actor-backlog.md` give bounded prioritized actions for hy3d, wscheppity, extra, oscraft, gmweb, bitvoice, owner and bota, with stable IDs, evidence paths, acceptance criteria and blockedBy. `python3 tools/validate-progress-dashboard.py` checks cited paths, source counts, no orphan rows, identifier hygiene, null gates, SHA-256 integrity and `STALE=false`. `extra` mid-rebuild is reported as `UNAVAILABLE` with exact paths; no recommendation is applied.
