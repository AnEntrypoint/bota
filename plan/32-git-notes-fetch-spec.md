# 32. Git notes fetch: read-only spec

Status: spec, with the fetch verified live (see Live result). Nothing is pushed or committed to gm. The gm change waits for the folio commit (plan/29, debt item 2). Framing is unverified, as with SSE (plan/30) and spawn events (plan/31).

## Source

- Savi endpoint doc, `/workspace/savi/.spawn/agent-interface.md`: "git log --notes=spawn carries the world's reading of each commit."
- Remote: `https://git.spawn.co/@lanmower/the-savi-gallery.git` (game-6.git also resolves). Auth: the global git credential helper reads `/config/.spawn/token`. The token is never printed.
- Local clone: `/workspace/game-6`. This is the only clone the spec reads; it is not a scratch copy.

## Read-only shape

- Fetch the notes ref, then read it with `git log --notes=spawn`. Both steps read the world; they write only the local notes ref in the clone.
- Fetch: `git fetch origin 'refs/notes/*:refs/notes/*'`. This writes the local `refs/notes/*` and nothing on the remote.
- Read: `git log --notes=spawn --format=%H%x09%s` (one commit per line, the note printed under each commit). Do not use `--notes=spawn` with a push.
- Excluded: any `git push`, any `git notes add` or edit, `exec --persist`, and any command that writes to the remote.

## Node witness plan (not run; no token printed)

1. Run `git -C /workspace/game-6 fetch origin 'refs/notes/*:refs/notes/*'` with a 60 s timeout, using `spawnSync`. Print the exit code only.
2. Run `git -C /workspace/game-6 log --notes=spawn --format=%H --max-count=20` and count the lines. Print the count only, not the hashes.
3. For the first commit, check that the notes output is non-empty. Print the byte count only, never the note text.
4. Mark the notes framing verified only if step 3 finds a non-empty note. An empty note set is a valid result and leaves the framing open.
5. Exit 0 on a clean fetch, whether or not notes are found. Exit 1 on a non-zero git exit or a timeout.

## Live result (fetch only, into local refs/notes)

- `git fetch origin refs/notes/*:refs/notes/*` in /workspace/game-6: exit 0. It wrote `refs/notes/spawn` locally. No push, no remote write.
- `git log --notes=spawn`: 20 commits in the last 20 read.
- The first commit (b5be09a) has a non-empty spawn note, 16 bytes. Verified: notes are returned by the fetch. The note text was not read, and its format stays unverified.

## Unverified

- The note format (plain text or structured) is not stated in the savi doc. The witness above records only sizes, so the format stays open until a note is read by the owner or by a later, separate witness.
- Whether `refs/notes/spawn` is the only notes namespace. The spec fetches all of `refs/notes/*`, which covers it.

## Blocked

- Nothing live is blocked: the fetch is a read. Live writes are not part of this spec.
- No deletions, no account doors, no publish.
