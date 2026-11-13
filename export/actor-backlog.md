# BOTA bounded actor backlog

Generated: `2026-11-13T12:29:41.595220+00:00`. Read-only toward peers. All rows keep `do_not_promote: true`.

Rows: `12`; blocked rows: `5`.

## By actor

- `hy3d`: `2`
- `wscheppity`: `1`
- `extra`: `2`
- `oscraft`: `1`
- `gmweb`: `1`
- `bitvoice`: `1`
- `owner`: `1`
- `bota`: `3`

## Actions

### `actor:4d8cf0def2c5e8b0` — `owner` / P5

- Choose whether to keep, specify, or defer `forever_eternal_loop_clip`
- Evidence: `/workspace/bota/export/owner-decision-brief.md`
- Acceptance: `["Owner records an explicit choice", "No canonical engine value is written without opt-in apply", "do_not_promote remains true"]`
- Blocked by: `["owner decision required"]`
- Note: Neutral options: keep gated; supply an exact choice; defer to a playable build. No option is recommended.

### `actor:94c9394a5d057634` — `bitvoice` / P10

- Keep service contract 1.0.0 stable; continue full-duplex benchmark
- Evidence: `/workspace/bitvoice/service-contract.json`
- Acceptance: `["service-contract.json schemaVersion 1.0.0", "interfaceStability stable", "benchmark evidence records clean shutdown/errors without overclaiming"]`
- Blocked by: `["persistent service not running"]`

### `actor:19b6d891bd3beae6` — `bota` / P10

- Keep live coordination watcher and auto-refresh bounded/read-only
- Evidence: `/workspace/bota/export/coordination-auto-refresh.json`
- Acceptance: `["--once PASS", "validate-auto-refresh PASS", "SHA256SUMS covers new files", "export-status STALE=false"]`
- Blocked by: `[]`

### `actor:cbaa4203c966523a` — `extra` / P10

- Finish upstream ledger rebuild after temporary red gate
- Evidence: `/workspace/extra/.local/extraction-manifest.json`
- Acceptance: `["On-disk extraction manifest reports 44 tracked files, 102 commits, 51 notes", "extraction-contract.json exists if used by the ledger", "red gate resolved"]`
- Blocked by: `["temporary red gate", "extraction-contract.json UNAVAILABLE"]`
- Note: 44/102/51 is owner context; on-disk count is reported separately and not invented.

### `actor:e66d633379e3ef2e` — `gmweb` / P10

- Preserve auto-GM/GitHub AgentGUI rollout gates
- Evidence: `/workspace/gmweb/docs/ROLLOUT_REPORT.json`
- Acceptance: `["ROLLOUT_REPORT ok=true", "11 gates exit 0", "failures=[]", "post-restart live UNAVAILABLE remains allowed"]`
- Blocked by: `[]`

### `actor:73affc38e6ffeb33` — `hy3d` / P10

- Keep 50 audio/voice rows endpoint-blocked until a stable persistent BitTTS service exists
- Evidence: `/workspace/hy3d/output/content-for-bota.json`
- Acceptance: `["Pinned service contract remains 1.0.0", "Health returns required ok/service/schemaVersion/interfaceStability", "Probe audio validates", "Only then publish ready hash-verified rows"]`
- Blocked by: `["no persistent service", "recovery=false"]`
- Note: Contract is stable; service is not running. No quota burned.

### `actor:99413e02a0c62955` — `oscraft` / P10

- Maintain fullname BOTA IDs and default Dota acronym inversion
- Evidence: `/workspace/oscraft/scenarios/bota/cross-contract-snapshot.json`
- Acceptance: `["26 BOTA fullname IDs", "127 default acronym IDs", "cross-contract optionalMissing=0", "npm run check:cross-contracts stays green"]`
- Blocked by: `[]`

### `actor:7d5528947f2bc8ac` — `wscheppity` / P10

- Keep 23/23 extraction classes complete and local runner verified
- Evidence: `/workspace/wscheppity/.local/extraction-manifest.json`
- Acceptance: `["classes equals complete", "partial=0", "blocked=0", "cdnBad=0", "local runner verification recorded"]`
- Blocked by: `[]`

### `actor:7c5f5b2e42910e1f` — `bota` / P20

- Preserve canonical null gates and identifier contract
- Evidence: `/workspace/bota/export/export-status.json`
- Acceptance: `["425 gated fields", "engine-resolved absent", "26 active acronyms in BOTA export", "do_not_promote true"]`
- Blocked by: `[]`

### `actor:463679334c35b811` — `extra` / P20

- Capture exact bytes for extra generated-on-demand CDN names
- Evidence: `/workspace/extra/.local/cdn/manifest-all.json`
- Acceptance: `["Exact HTTP status/content-type/body-size", "SHA-256 and local extraction path", "manifest row ok=true"]`
- Blocked by: `["generated-on-demand names"]`

### `actor:420268710fefa092` — `hy3d` / P20

- Maintain asset gates and prepared-only inventory without claiming delivery
- Evidence: `/workspace/hy3d/output/asset-delivery-report.json`
- Acceptance: `["asset-delivery-report ok=true", "hash sweep remains green", "no false ready rows"]`
- Blocked by: `[]`
- Note: Owner reports asset gates green.

### `actor:4dd721b2c01ce2f9` — `bota` / P30

- Keep transition-wipe presentation intentionally open
- Evidence: `/workspace/bota/export/owner-decision-brief.md`
- Acceptance: `["Presentation cue remains text-only", "No asset hash invented", "Three-beat Camera Chain preserved"]`
- Blocked by: `[]`
- Note: It stays open because the exact visual asset is a presentation choice, not a rule value.
