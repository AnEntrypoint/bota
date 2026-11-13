# BOTA ↔ Spawn compatibility

Verdict: **reusable-data**. These are **not** the same game.

BOTA's canonical export is a 26-hero, acronym-keyed MOBA design/export. Downstream oscraft BOTA artifacts are being inverted to full BOTA character names/slugs, while default-Dota legacy hero IDs become three-letter acronyms. `/workspace/wscheppity` is `WONSCHWEPPIDYTIME`, a live three.js multi-camera frog sitcom where objects are scene rows, behaviors are `update(ctx, dt)` modules, and art is referenced by `/cdn/` names. No BOTA live integration into Spawn has been built by this report.

## Counts

| Side | Counts |
|---|---|
| BOTA | 26 heroes, 104 abilities, 50 voice rows, 25 gallery images, 12 decisions, 169 covered markers, 425 gated fields, 25 hashes |
| wscheppity | 189 tracked files, 4 refs, 79 scripts, 14 places, 6 scene cells, 67 world.assets entries, 2 templates |

## Identifier inversion

`tools/validate-integration-live.py` supports two read-only modes:

- `--identifier-mode acronym`: historical contract. Against a migrated oscraft checkout, missing acronym files are `UNAVAILABLE` and present full-name keys are `DRIFT`, each with an exact path.
- `--identifier-mode bota-fullname --default-dota-acronyms`: owner's target contract. BOTA artifact keys use full slugs; `character-mapping.tsv` `legacy_acronym` values for default-Dota heroes must be acronyms.

The inversion does not rewrite BOTA's export and does not make `003 Gigachad` active. It also does not turn WONSCHWEPPIDYTIME scene IDs into hero IDs. If oscraft is mid-migration, either `UNAVAILABLE` or `DRIFT` is a truthful result, not a crash or a pass.

## Coordinated content

hy3d owns all content, first with pooled emails then with the relay. BOTA owns rules and reads `/workspace/hy3d/output/content-for-bota.json` before each pass. `export/rule-demand.json` / `.tsv` lists implied heroes, kits, voice, images, props, structures, clips and Spawn CDN evidence with `available`, `requested` and `blocked` status. Only a real hy3d SHA-256 may make a demand `available`; no BOTA rule invents an asset path.

## Evidence

- `/workspace/wscheppity/AGENTS.md:6` says an object is a row with three.js geometry/material fields.
- `/workspace/wscheppity/world.config.yaml:2` names the world `WONSCHWEPPIDYTIME`.
- `/workspace/wscheppity/design.md:2` calls it a 3D multi-camera frog sitcom.
- `/workspace/wscheppity/places/main/sim.js:18` uses `frog-him` / `frog-her` cast IDs, not BOTA acronyms.
- `/workspace/bota/ROSTER.md:7` begins BOTA's active roster; `export/hero-registry.json` requires lowercase three-letter acronym keys in the canonical export.
- `export/field-index.json` records 425 decision-gated fields. `do_not_promote: true` remains in force.

## Conservative reuse

Could reuse only as metadata or creative reference: the acronym registry as provenance, humor/voice flavor as reference, and verification discipline for a separate checker.

Must not be copied blindly: engine ability values, decision-gated nulls, three.js scene rows, behavior modules, local BOTA GLB/JPG paths as `/cdn/` names, or retired/reserve identifiers.

No owner decision was applied; `export/engine-resolved/` is not created by this report.
