# BOTA owner progress dashboard

Generated: `2026-11-13T12:19:35.499791+00:00`

Dashboard status: `PASS`. Read-only peer evidence only; no peer writes.

## Coordination

- Rows: `536`; resolved/available: `439`; unresolved: `97`; unexplained UNAVAILABLE: `0`.
- Statuses: `available=439`, `requested-pooled-email=54`, `requested-relay=0`, `spawn-generated=41`, `owner-decision=1`, `intentionally-open=1`.
- Next actors: `bota=0`, `extra=8`, `hy3d=54`, `owner=1`, `wscheppity=33`.

## Agents

### `bota` — `DRIFT`

- Counts: `{"coordinationRows": 536, "gatedFields": 425, "hashes": 50, "ruleDemandRows": 382}`
- Evidence: `/workspace/bota/export/coordination-status.json`, `/workspace/bota/export/coordination-auto-refresh.json`, `/workspace/bota/export/export-status.json`, `/workspace/bota/export/SHA256SUMS.json`
- Verified commands: `python3 tools/validate-request-queues.py` exit `0`, `python3 tools/validate-decision-packet.py` exit `0`, `python3 tools/validate-engine-data.py` exit `0`, `python3 tools/validate-apply-mechanism.py` exit `0`, `python3 tools/validate-integration-live.py --identifier-mode bota-fullname --default-dota-acronyms` exit `0`

### `hy3d` — `asset-gates-green / persistent-service-UNAVAILABLE`

- Counts: `{"assetGatesOk": true, "contractRows": 159, "endpointBlocked": 50, "preparedOnly": 52, "quota": 30, "ready": 107, "recovery": true, "requested": 54}`
- Evidence: `/workspace/hy3d/output/content-for-bota.json`, `/workspace/hy3d/output/content-demand-v2.json`, `/workspace/hy3d/output/generation-status.json`, `/workspace/hy3d/output/studio-recovery-watch.json`, `/workspace/hy3d/output/asset-delivery-report.json`
- Verified commands: `npm run check:assets` exit `0`, `npm run watch:bittts -- --once` exit `0`

### `wscheppity` — `complete`

- Counts: `{"blocked": 0, "cdnBad": 0, "cdnNames": 402, "classes": 23, "complete": 23, "manifestAllBad": 0, "manifestAllOk": 369, "partial": 0}`
- Evidence: `/workspace/wscheppity/.local/extraction-manifest.json`, `/workspace/wscheppity/.local/cdn/manifest.json`, `/workspace/wscheppity/.local/cdn/manifest-all.json`
- Verified commands: `local runner restarted and verified (owner turn context)` exit `0`

### `extra` — `REBUILDING`

- Counts: `{"cdnBad": 0, "cdnNames": 78, "cdnOk": 70, "onDisk": {"activeAssets": 35, "activeAssetsValid": 35, "apiCaptures": 37, "apiDoorGroups": 42, "blocked": 0, "cdnBad": 0, "cdnNames": 78, "classes": 22, "complete": 22, "docsSections": 68, "engineFiles": 27, "gitCommits": 84, "gitNotes": 42, "gitRefs": 3, "partial": 0, "trackedFiles": 42}, "ownerExpectedAfterRebuild": {"gitCommits": 102, "gitNotes": 51, "trackedFiles": 44}}`
- Evidence: `/workspace/extra/.local/extraction-manifest.json`, `/workspace/extra/.local/extraction-contract.json`, `/workspace/extra/.local/cdn/manifest.json`, `/workspace/extra/.local/cdn/manifest-all.json`
- UNAVAILABLE: `["extra.contract"]`
- Verified commands: `extra upstream pull / ledger rebuild in progress (owner context)` exit `None`

### `oscraft` — `fullname-ready`

- Counts: `{"botaFullnameIds": 24, "defaultAcronymIds": 127, "extraMissing": 0, "extraPresent": 2, "optionalMissing": 0, "optionalPresent": 10, "required": 8, "skinnedModels": 24}`
- Evidence: `/workspace/oscraft/scenarios/bota/IDENTIFIERS.md`, `/workspace/oscraft/scenarios/bota/cross-contract-snapshot.json`, `/workspace/oscraft/scenarios/bota/bota_ui.json`
- Verified commands: `npm run check:cross-contracts (owner context)` exit `0`

### `gmweb` — `gates-green`

- Counts: `{"failures": 0, "gatePasses": 317, "gateTotals": 317, "gates": 11, "rolloutOk": true}`
- Evidence: `/workspace/gmweb/docs/ROLLOUT_REPORT.json`, `/workspace/gmweb/docs/POST-RESTART.md`
- Verified commands: `/data/cache/node/node-v24.22.0-linux-x64/bin/node startup/check-startup-sources.mjs` exit `0`, `/data/cache/node/node-v24.22.0-linux-x64/bin/node startup/check-runtime-install.mjs` exit `0`, `/data/cache/node/node-v24.22.0-linux-x64/bin/node startup/check-container-startup-path.mjs` exit `0`, `/data/cache/node/node-v24.22.0-linux-x64/bin/node scripts/check-rollout-docs.mjs` exit `0`, `/data/cache/node/node-v24.22.0-linux-x64/bin/node startup/check-post-restart.mjs --offline` exit `0`

### `bitvoice` — `contract-stable / benchmark-in-progress`

- Counts: `{"cleanShutdown": false, "contractName": "bitvoice-full-duplex", "errors": 0, "fullDuplexConcurrentSessions": 2, "interfaceStability": "stable", "schemaVersion": "1.0.0"}`
- Evidence: `/workspace/bitvoice/service-contract.json`, `/workspace/bitvoice/docs/full-duplex-metrics.json`, `/workspace/bitvoice/docs/VERIFICATION.md`
- Verified commands: `python3 scripts/validate-service-contract.py` exit `0`, `python3 scripts/service-contract-smoke.py` exit `0`

## Top blocked reasons

- `54` rows — `requested-pooled-email`
- `41` rows — `spawn-generated`
- `1` rows — `intentionally-open`
- `1` rows — `owner-decision`

## Owner-gated rows

- `owner-decision`: `1`. Neutral options only; no value chosen. `do_not_promote: true`.
- `intentionally-open`: `1`. Presentation cue remains open; no value chosen. `do_not_promote: true`.

## Exact source paths

- `bota.coordinationStatus`: `/workspace/bota/export/coordination-status.json` — `ready`
- `bota.autoRefresh`: `/workspace/bota/export/coordination-auto-refresh.json` — `ready`
- `bota.ruleDemand`: `/workspace/bota/export/rule-demand.json` — `ready`
- `bota.contentQueue`: `/workspace/bota/export/content-request-queue.json` — `ready`
- `bota.spawnGaps`: `/workspace/bota/export/spawn-extraction-gaps.json` — `ready`
- `bota.ownerBrief`: `/workspace/bota/export/owner-decision-brief.md` — `ready`
- `bota.exportStatus`: `/workspace/bota/export/export-status.json` — `ready`
- `bota.sha256Sums`: `/workspace/bota/export/SHA256SUMS.json` — `ready`
- `hy3d.content`: `/workspace/hy3d/output/content-for-bota.json` — `ready`
- `hy3d.demandV2`: `/workspace/hy3d/output/content-demand-v2.json` — `ready`
- `hy3d.generation`: `/workspace/hy3d/output/generation-status.json` — `ready`
- `hy3d.recovery`: `/workspace/hy3d/output/studio-recovery-watch.json` — `ready`
- `hy3d.delivery`: `/workspace/hy3d/output/asset-delivery-report.json` — `ready`
- `wscheppity.extraction`: `/workspace/wscheppity/.local/extraction-manifest.json` — `ready`
- `wscheppity.cdn`: `/workspace/wscheppity/.local/cdn/manifest.json` — `ready`
- `wscheppity.cdnAll`: `/workspace/wscheppity/.local/cdn/manifest-all.json` — `ready`
- `extra.extraction`: `/workspace/extra/.local/extraction-manifest.json` — `ready`
- `extra.contract`: `/workspace/extra/.local/extraction-contract.json` — `UNAVAILABLE`
- `extra.cdn`: `/workspace/extra/.local/cdn/manifest.json` — `ready`
- `extra.cdnAll`: `/workspace/extra/.local/cdn/manifest-all.json` — `ready`
- `oscraft.identifiers`: `/workspace/oscraft/scenarios/bota/IDENTIFIERS.md` — `ready`
- `oscraft.snapshot`: `/workspace/oscraft/scenarios/bota/cross-contract-snapshot.json` — `ready`
- `oscraft.ui`: `/workspace/oscraft/scenarios/bota/bota_ui.json` — `ready`
- `gmweb.rolloutReport`: `/workspace/gmweb/docs/ROLLOUT_REPORT.json` — `ready`
- `gmweb.postRestart`: `/workspace/gmweb/docs/POST-RESTART.md` — `ready`
- `bitvoice.serviceContract`: `/workspace/bitvoice/service-contract.json` — `ready`
- `bitvoice.metrics`: `/workspace/bitvoice/docs/full-duplex-metrics.json` — `ready`
- `bitvoice.verification`: `/workspace/bitvoice/docs/VERIFICATION.md` — `ready`
- `bota.progressDashboardJson`: `/workspace/bota/export/progress-dashboard.json` — `generated`
- `bota.progressDashboardMd`: `/workspace/bota/export/PROGRESS-DASHBOARD.md` — `generated`
- `bota.actorBacklogJson`: `/workspace/bota/export/actor-backlog.json` — `generated`
- `bota.actorBacklogMd`: `/workspace/bota/export/actor-backlog.md` — `generated`

## UNAVAILABLE

- `extra.contract`: `/workspace/extra/.local/extraction-contract.json`

Preserved: 26 active heroes, 27 gallery images, `003` image-only Reserve, 425 null-gated fields, Receipt/Repost/Camera chains, canonical null gates, absent `export/engine-resolved/`, `bota-fullname` + default Dota acronyms.
