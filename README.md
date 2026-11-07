# Brainrot of the AI - BotA

[Open the character gallery](GALLERY.md) — every generated character in one grid.

Design docs for the 59-hero roster: characters, kits, mechanics, art, tone and spec.

Use the navigation. Numbers and cross-hero hooks marked UNVERIFIED or GUESS are unverified.

Character prompts: characters/STYLE.md holds the shared lead and tail. Each characters/NNN-*.md holds its subject and hook. Run `node tools/sync-roster.mjs` after editing them; it regenerates roster.yaml, characters/INDEX.tsv, each file's Card section, and the signature gags in plan/15. Run `node tools/sync-roster.mjs --check` before committing.

Gallery: `node tools/build-gallery.mjs` rebuilds GALLERY.md and the gallery images from the character source images, adds the gallery to manifest.json and the README link when missing. The repo root comes from the script's own path, so any working directory works. The image inputs live outside this repo and are set with BOTA_CHARS_DIR (default ../chars), BOTA_GENERATED_DIR (default ../characters/memes/generated) and BOTA_PYTHON (default python3, which must provide PIL for tools/resize.py). Without any source images the script exits 2 instead of writing an empty gallery.

Prop manifests: `node tools/verify-props.mjs` checks both `docs/bota-props-*.json` offline against the GLBs (magic, version, declared length, bytes, sha256, jobId, responseJson); `node tools/verify-props.mjs --self-test` witnesses forced failures using file:// fixtures. No network, no `.env`, no regeneration.
