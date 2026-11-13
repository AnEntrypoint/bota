#!/usr/bin/env python3
"""Build export/owner-decision-brief.md from gated rule-demand rows only."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "export"


def quote(citation: str) -> str:
    rel, _, line = citation.partition(":")
    p = ROOT / rel
    try:
        return p.read_text().splitlines()[max(0, int(line) - 1)].strip()
    except Exception:
        return ""


def main() -> int:
    demand = json.loads((E / "rule-demand.json").read_text())
    rows = [r for r in demand["rows"] if r.get("status") in {"owner-decision", "intentionally-open"}]
    lines = [
        "# BOTA owner-decision brief",
        "",
        f"Generated: `{dt.datetime.now(dt.timezone.utc).isoformat()}`",
        "",
        "Scope: only `owner-decision` and `intentionally-open` rows from `export/rule-demand.json`. No value is recommended, applied, or promoted. `do_not_promote: true` remains in force; `export/engine-resolved/` is absent.",
        "",
        f"Rows: `{len(rows)}`. Canonical engine data and the 425 decision-gated null fields are unchanged.",
        "",
    ]
    for r in rows:
        citation = r.get("ruleCitation", "")
        lines += [
            f"## `{r['slug']}` — `{r['status']}`",
            "",
            f"- Current actor: `{r.get('nextActor')}`. Stable ID: `{r.get('stableId')}`.",
            f"- Rule citation: `{citation}` — `{quote(citation)}`",
            f"- Evidence: `{r.get('hy3dEvidence')}`",
            f"- Current destination/reference: `{r.get('destination')}`",
            f"- Gate: `do_not_promote: {str(r.get('validation', {}).get('do_not_promote', True)).lower()}`.",
            "",
            "Neutral options:",
            "",
        ]
        if r["status"] == "owner-decision":
            lines += [
                "1. **Keep gated.** Leave the exact clip duration/content as an owner decision. Nothing changes in engine data, kit behavior, voice rules, or the decision packet.",
                "2. **Owner supplies an exact choice.** Record the chosen value and its confidence in the owner decision flow. Only an explicit confirmed apply could write an opt-in `export/engine-resolved/` overlay; canonical `export/engine/` remains null-gated.",
                "3. **Defer to a playable build.** Keep the current text rule and wait for measured build evidence. The row remains `owner-decision`; no `UNVERIFIED`/`GUESS` value is promoted.",
                "",
                "If accepted: only the named decision field may gain an owner-chosen value through the existing apply mechanism. The Receipt/Repost/Camera chains, 27 gallery images, 26 active heroes, `003` image-only Reserve, and all other null gates stay unchanged.",
            ]
        else:
            lines += [
                "1. **Keep intentionally open.** The presentation cue remains a text rule with no exact visual asset. Nothing changes.",
                "2. **Owner asks for a concrete cue.** BOTA may add a rule demand for a specific hash-verified hy3d content row; the cue is not invented and no numeric value is promoted.",
                "3. **Owner retires the cue.** Remove or simplify the presentation line in a future rule pass, while preserving the three-beat chain structure and all decision gates.",
                "",
                "If accepted: only presentation wording or a future demand row changes. No canonical engine field, ability value, active hero key, or `003` reserve status changes.",
            ]
        lines += ["", "Acceptance criteria:", ""]
        for c in r.get("acceptanceCriteria", []): lines.append(f"- {c}")
        lines += ["", "Non-promotion invariant:", "", "- `do_not_promote: true`", "- canonical `export/engine/` unchanged", "- `export/engine-resolved/` absent", "- no new `GUESS`/`UNVERIFIED` value promoted", ""]
    (E / "owner-decision-brief.md").write_text("\n".join(lines))
    print(f"OWNER_BRIEF rows={len(rows)} do_not_promote=true engine_resolved_absent={not (E/'engine-resolved').exists()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
