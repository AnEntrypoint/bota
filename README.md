# Brainrot of the AI - BotA

Design docs for the 112-hero roster: characters, kits, mechanics, art, tone and spec.

Use the navigation. Every number and cross-hero hook marked GUESS is unverified.

Key files: [ROSTER.md](ROSTER.md), [plan/22-art-direction.md](plan/22-art-direction.md), [plan/17-presentation-and-readability.md](plan/17-presentation-and-readability.md), [characters/INDEX.tsv](characters/INDEX.tsv).

Character prompts: characters/STYLE.md holds the shared lead and tail. Each characters/NNN-*.md holds its subject and hook. Run `node tools/sync-roster.mjs` after editing them; it regenerates roster.yaml, characters/INDEX.tsv, each file's Card section, and the signature gags in plan/15. Run `node tools/sync-roster.mjs --check` before committing.
