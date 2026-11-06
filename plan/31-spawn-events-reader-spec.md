# 31. spawn events reader: read-only spec

Status: spec only. Nothing is run or committed to gm. The gm change waits for the folio commit (plan/29, debt item 2). Framing is unverified, as with SSE (plan/30).

## Source

- `spawn events [--kind a,b] [--world] [--from] [--since] [--exec cmd] [--once]`: "live inbox as JSON lines" (savi doc, Client CLI section, `/workspace/savi/.spawn/agent-interface.md`).
- The CLI is at `/config/.bun/bin/spawn` (package `@spawnco/client` 0.2.0). It is not on PATH; the spawn.mjs `SPAWN_CLI` default is the same path.
- The HTTP door behind it is not named in the savi doc. The spec therefore uses the CLI, not a guessed URL.

## Read-only shape

- Read only: `spawn events --once --kind <kinds>` (or `--since`/`--from` for a window). `--once` prints the queued events and exits, so the call ends.
- Excluded: `--exec <cmd>`, because it runs a command for each event, which is not a read.
- Expected output: one JSON object per line on stdout. Field names unverified until a live run.

## Node witness plan (not run; no token printed)

1. Run `spawn events --once --kind chat_mention` with a 20 s timeout, using `child_process.spawnSync`, capturing stdout and stderr.
2. Print the exit code and the byte count of stdout only.
3. Split stdout on newlines. For each non-empty line, try `JSON.parse`. Print the count of lines that parse, and the sorted key names of the first parsed object. Never print values.
4. If stdout is empty, print `no events` and the exit code. Mark framing verified only if at least one line parses as JSON.
5. Exit 0 on a clean run, whether or not events arrived. Exit 1 on a non-zero CLI exit or a timeout.

## Blocked

- A `chat_mention` event needs a mention in chat, which is a live write held until the owner names a test room (plan/28, item 7). An empty queue is a valid result and leaves the JSON-line framing open.
- No live send, no deletions, no account doors.

## Open questions

- Whether `--since` or `--from` windows are wanted for the reader, given that the reader is read-only.
