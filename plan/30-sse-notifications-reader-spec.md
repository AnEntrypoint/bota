# 30. SSE notifications reader: read-only spec

Status: spec, with the stream type verified live (see Event framing). Reader code is not built. No code is written and nothing is committed to gm. The gm change waits for the folio commit (plan/29, debt item 2). Sources: `/workspace/savi/.spawn/agent-interface.md` (the endpoint line and the chat section) and the spawn CLI `spawn events --kind chat_mention`, named in the same doc.

## Endpoint

- `GET https://www.spawn.co/api/notifications/stream?kind=chat_mention` (SSE). Auth: `Authorization: Bearer <token>`, token read from `/config/.spawn/token`, never printed.
- The `kind` query narrows the stream. `chat_mention` is the kind the savi doc names. Other kinds are not verified.
- Non-stream list: `GET /api/notifications` (with `?unread=1` for unread only), already a spawn.mjs read verb (`notifications`).

## Event framing (live check, 15 s read)

Verified on one live GET (node, read only, 15 s timeout): HTTP 200, `Content-Type: text/event-stream; charset=utf-8`, 68 bytes read, one frame, and that frame held only a comment line (a keep-alive). No `data:` frame arrived in 15 s, so the `id`, `event` and `data` framing and the chat_mention JSON shape remain unverified until a live event arrives.

Second read, unfiltered (`/api/notifications/stream`, 15 s, read only): the same result, HTTP 200 `text/event-stream`, 68 bytes, one keep-alive comment, no data frame. A chat_mention frame needs a mention in chat, and sending one is a live write held until the owner names a test room, so data framing stays blocked on that room.

The savi doc names the endpoint as SSE but does not give the frame format. The spec assumes the standard `text/event-stream` framing, and the witness below must confirm it before the reader is built:

- Response `Content-Type` starts with `text/event-stream`.
- Frames are separated by a blank line. Each frame has optional `id:`, `event:` and `data:` lines. Multiple `data:` lines join with a newline.
- Comment lines start with `:` and carry no event; a keep-alive may be a comment.
- Each event's `data` is expected to be JSON with a `kind` field and an `actionData` read door (the savi doc says each chat_mention event's `actionData` is the read door). Unverified until a live event arrives.

## Reader behaviour (planned, not built)

1. Open the stream with a timeout, read bytes until a blank line or the timeout, and split into frames.
2. Yield one object per frame: `{ id, event, data }`, with `data` parsed as JSON when it parses and kept as text otherwise.
3. Stop on timeout, on HTTP error (print status only), or on a caller limit (a frame count).
4. Reconnect is out of scope for the first version. A dropped stream is reported, not retried.

## Witness plan (node, no token printed)

Run only after the spec is accepted, and only as a read:

1. Call the stream endpoint with a 15 s timeout and a bearer header from the token file.
2. Check the HTTP status is 200 and the content type starts with `text/event-stream`. Print the status and the content type only.
3. Read raw bytes for up to 15 s. Count frames separated by a blank line, and count how many carry a `data:` line. Print the counts and the first frame's field names (`id`, `event`, `data`), never the values.
4. If no frame arrives in 15 s, print `no frames in 15 s` and the status. That is a valid result: the stream may be quiet. Mark the framing as verified only if at least one frame was seen.
5. Exit 0 on a 200 with a `text/event-stream` type, whether or not a frame arrived. Exit 1 on any other status.

## Open questions for the owner

- Whether `kind` filters other than `chat_mention` are wanted.
- Whether a reconnect is wanted in the first version. The spec says no.

## Held

- The reader code and the gm commit wait for the folio commit.
- No live send, no deletions, no account doors.
