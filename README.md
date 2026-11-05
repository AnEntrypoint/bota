# Brainrot of the AI - BotA

[Open the character gallery](GALLERY.md) — every generated character in one grid.

Design docs for the 59-hero roster: characters, kits, mechanics, art, tone and spec.

Use the navigation. Numbers and cross-hero hooks marked UNVERIFIED or GUESS are unverified.

Character prompts: characters/STYLE.md holds the shared lead and tail. Each characters/NNN-*.md holds its subject and hook. Run `node tools/sync-roster.mjs` after editing them; it regenerates roster.yaml, characters/INDEX.tsv, each file's Card section, and the signature gags in plan/15. Run `node tools/sync-roster.mjs --check` before committing.
