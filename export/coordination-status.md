# BOTA live coordination status

Generated: `2026-11-13T12:32:15.466272+00:00`
Mode: `bota-fullname`; default Dota acronyms: `true`; engine-resolved absent: `true`.

## Counts

- Rows: `536`; resolved/available: `439`; unresolved evidence-backed: `97`; unexplained UNAVAILABLE: `0`.
- Statuses: `spawn-generated=41`, `requested-pooled-email=54`, `UNAVAILABLE=0`, `intentionally-open=1`, `requested-relay=0`, `owner-decision=1`, `available=439`.
- Next actors: `hy3d=54`, `wscheppity=33`, `extra=8`, `owner=1`, `bota=0`.

## Peer evidence

- hy3d: contract rows `159`, demand-v2 rows `382`, requested `54`, quota `30`, recovery `True`.
- wscheppity: CDN names `402`, ok `369`, bad `0`, HTTP files `578`.
- extra: extraction `ready`, contract `UNAVAILABLE`, CDN names `78`, ok `70`, bad `0`, HTTP files `126`, first-class peer `true`.
- extra root: `/workspace/extra`; nested git repo (read-only) may be `/workspace/extra/game-16`.
- oscraft: BOTA fullname IDs `24`, default acronym IDs `127`.

## Exact evidence paths

- `hy3d.content`: `/workspace/hy3d/output/content-for-bota.json` — `ready`
- `hy3d.demandV2`: `/workspace/hy3d/output/content-demand-v2.json` — `ready`
- `hy3d.generation`: `/workspace/hy3d/output/generation-status.json` — `ready`
- `hy3d.recovery`: `/workspace/hy3d/output/studio-recovery-watch.json` — `ready`
- `hy3d.probes`: `/workspace/hy3d/output/spawn-cdn-probes.json` — `ready`
- `hy3d.contentGaps`: `/workspace/hy3d/output/content-gaps*.json` — `UNAVAILABLE`, count `0`
- `wscheppity.extraction`: `/workspace/wscheppity/.local/extraction-manifest.json` — `ready`
- `wscheppity.cdnAll`: `/workspace/wscheppity/.local/cdn/manifest-all.json` — `ready`
- `wscheppity.cdnActive`: `/workspace/wscheppity/.local/cdn/manifest.json` — `ready`
- `wscheppity.httpDir`: `/workspace/wscheppity/.local/cdn/http/*` — `ready`, count `578`
- `extra.extraction`: `/workspace/extra/.local/extraction-manifest.json` — `ready`
- `extra.contract`: `/workspace/extra/.local/extraction-contract.json` — `UNAVAILABLE`
- `extra.cdnAll`: `/workspace/extra/.local/cdn/manifest-all.json` — `ready`
- `extra.cdnActive`: `/workspace/extra/.local/cdn/manifest.json` — `ready`
- `extra.httpDir`: `/workspace/extra/.local/cdn/http/*` — `ready`, count `126`
- `oscraft.identifiers`: `/workspace/oscraft/scenarios/bota/IDENTIFIERS.md` — `ready`
- `oscraft.crossContract`: `/workspace/oscraft/scenarios/bota/cross-contract-snapshot.json` — `ready`
- `oscraft.ui`: `/workspace/oscraft/scenarios/bota/bota_ui.json` — `ready`

## Unresolved rows

- `hero-voice/blo` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/boo` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/bot` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/cha` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/col` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/coo` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/din` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/ecc` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/fin` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/for` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/ghi` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/gon` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/got` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/gre` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/how` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/kar` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/lan` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/nec` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/nos` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/npc` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/san` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/sho` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/spu` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/tra` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/wil` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `hero-voice/woj` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `rule-demand/coffee-can` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `rule-demand/content-mill-melee` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `rule-demand/content-mill-ranged` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- `rule-demand/delivery-drone` → `requested-pooled-email` / `hy3d`; evidence `{"classification": "endpoint-blocked", "paths": ["/workspace/hy3d/output/content-demand-v2.json", "/workspace/hy3d/output/generation-status.json", "/workspace/hy3d/output/studio-recovery-watch.json"], "quota": 30}`
- … and `67` more; see `coordination-status.json`.
