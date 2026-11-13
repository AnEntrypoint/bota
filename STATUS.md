# BOTA STATUS — full-green-integration-2026-11-13

Generated 2026-11-13. Local verified state.

## Integration is green
- All 18 export checks exit `0`: sync-roster, active-roster, export, decisions, integration, engine-data, decision-packet, apply-mechanism, request-queues, rule-demand, coordination-status, spawn-compatibility, export-status, auto-refresh, export-clean, integration-live and progress-dashboard.
- `validate-integration-live --identifier-mode bota-fullname --default-dota-acronyms` reports `PASS (198 checks, 0 unavailable, 0 drift)` against `/workspace/oscraft`, which now carries the 24 active fullname slugs. The former 2-item drift is gone.
- `validate-export-status` reports `PASS (40 checks, 0 errors)` and `check-bota-export-clean` proves the clean-state rebuild byte-identical across all five engine files.
- Two validators carried a hardcoded 26: `validate-coordination-status.py` now compares oscraft's fullname count with `export/active-roster.json` `activeHeroCount` (24), and `validate-integration-live.py` derives its downstream expectation from `activeHeroKeys` while the export fixture keeps its 26 historical keys. `check-bota-export.sh` detects fullname mode from the live roster line instead of a fixed 26 phrase.
- The 241 legacy `lame-*` PRD rows are closed against the lame ledger's fixed or wontfix witnesses; `gm.prd_list` is empty.
- `export/` is now tracked so a fresh clone can run every documented validator.

Pass history and evidence live in `plan/35-continuous-iteration-ledger.md`; `export/STATUS.md` holds the generated snapshot.
