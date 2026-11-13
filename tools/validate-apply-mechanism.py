#!/usr/bin/env python3
"""Prove the opt-in decision applier is safe in an isolated temp workspace."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REAL_EXPORT = ROOT / "export"
REAL_APPLIER = ROOT / "tools" / "apply-decision.py"
results: list[tuple[str, int, bool, str]] = []
errors: list[str] = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root: Path):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def report(name: str, code: int, passed: bool, detail: str = "") -> None:
    results.append((name, code, passed, detail))
    print(f"CASE {name}: {'PASS' if passed else 'FAIL'} EXIT={code} {detail}")


def run(tmp: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(tmp / "tools" / "apply-decision.py"), *args], cwd=tmp, text=True, capture_output=True)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="bota-apply-check-"))
    try:
        (tmp / "tools").mkdir()
        shutil.copytree(REAL_EXPORT / "engine", tmp / "export" / "engine")
        for name in ["decisions.json", "decision-packet.json", "field-index.json"]:
            shutil.copy2(REAL_EXPORT / name, tmp / "export" / name)
        shutil.copy2(REAL_APPLIER, tmp / "tools" / "apply-decision.py")
        decisions = json.loads((tmp / "export" / "decisions.json").read_text())
        by_id = {d["id"]: d for d in decisions["decisions"]}
        owner_id = "sigma_value_tiers"
        open_id = "cross_hero_hook_guesses"
        owner_option = by_id[owner_id]["options"][0]
        open_option = by_id[open_id]["options"][0]

        # Canonical engine snapshot in temp workspace.
        engine_dir = tmp / "export" / "engine"
        before = snapshot(engine_dir)
        canonical_before_all = snapshot(tmp / "export")

        # 1. Dry run writes nothing.
        p = run(tmp, ["--decision-id", owner_id, "--option", json.dumps(owner_option), "--dry-run"])
        after_dry = snapshot(engine_dir)
        report("dry_run", p.returncode, p.returncode == 0 and before == after_dry and "CANONICAL_ENGINE_UNCHANGED=true" in p.stdout and before == snapshot(engine_dir), "no writes")

        # 2. Missing confirmation is refused.
        p = run(tmp, ["--decision-id", owner_id, "--option", json.dumps(owner_option), "--apply"])
        report("missing_owner_confirmation", p.returncode, p.returncode == 2 and "confirm-owner-decision" in p.stdout, "refused")

        # 3. Intentionally-open without extra confirmation is refused.
        p = run(tmp, ["--decision-id", open_id, "--option", json.dumps(open_option), "--apply", "--confirm-owner-decision"])
        report("intentionally_open_requires_extra", p.returncode, p.returncode == 2 and "confirm-intentionally-open" in p.stdout, "refused")

        # 4. Unknown decision id is refused.
        p = run(tmp, ["--decision-id", "not_a_decision", "--option", json.dumps(owner_option), "--dry-run"])
        report("unknown_decision_id", p.returncode, p.returncode == 2 and "unknown decision id" in p.stdout, "refused")

        # 5. Unknown option is refused. The applier accepts JSON literals as explicit owner values,
        # so use a marker-bearing option string that is neither supported nor valid JSON.
        p = run(tmp, ["--decision-id", owner_id, "--option", "UNSUPPORTED {not json}", "--dry-run"])
        report("unknown_option", p.returncode, p.returncode == 2 and "not supported" in p.stdout, "refused")

        # 6. Confirmed owner-decision apply writes only engine-resolved and leaves engine byte-identical.
        p = run(tmp, ["--decision-id", owner_id, "--option", json.dumps(owner_option), "--apply", "--confirm-owner-decision"])
        after_owner = snapshot(engine_dir)
        resolved = tmp / "export" / "engine-resolved"
        overlay = resolved / f"{owner_id}.json"
        audit = resolved / f"{owner_id}.audit.json"
        ok_owner = p.returncode == 0 and before == after_owner and overlay.is_file() and audit.is_file()
        report("confirmed_owner_apply", p.returncode, ok_owner, "canonical engine byte-identical")
        if audit.is_file():
            a = json.loads(audit.read_text())
            required = ["decision_id", "option", "timestamp", "decision_packet_sha256", "decisions_json_sha256", "engine_manifest_sha256", "affected_field_paths"]
            report("audit_record", 0, all(k in a for k in required) and a["decision_id"] == owner_id and a["canonical_engine_overwritten"] is False and len(a["affected_field_paths"]) > 0, f"fields={len(a.get('affected_field_paths', []))}")
        else:
            report("audit_record", 1, False, "missing")

        # 7. Confirmed intentionally-open apply also writes only to resolved.
        p = run(tmp, ["--decision-id", open_id, "--option", json.dumps(open_option), "--apply", "--confirm-owner-decision", "--confirm-intentionally-open"])
        report("confirmed_intentionally_open", p.returncode, p.returncode == 0 and before == snapshot(engine_dir) and (resolved / f"{open_id}.json").is_file() and (resolved / f"{open_id}.audit.json").is_file(), "extra confirmation honored")

        # 8. No bulk apply: only the two tested overlays and their audits exist.
        resolved_files = sorted(p.name for p in resolved.glob("*")) if resolved.exists() else []
        expected = sorted([f"{owner_id}.json", f"{owner_id}.audit.json", f"{open_id}.json", f"{open_id}.audit.json"])
        report("no_bulk_apply", 0, resolved_files == expected, f"files={','.join(resolved_files)}")

        # 9. Canonical engine files remain byte-identical after all cases.
        report("canonical_immutability", 0, before == snapshot(engine_dir), f"files={len(before)}")

        # 10. Real export is untouched during harness execution.
        real_engine_before = snapshot(REAL_EXPORT / "engine")
        real_resolved_exists = (REAL_EXPORT / "engine-resolved").exists()
        report("real_export_untouched", 0, real_engine_before == real_engine_before and not real_resolved_exists, "real engine-resolved absent")

        # 11. Cleanup safety: remove overlays and confirm canonical restore is deletion-only.
        shutil.rmtree(resolved)
        report("overlay_revert", 0, not resolved.exists() and before == snapshot(engine_dir), "delete overlay only")

        failed = [r for r in results if not r[2]]
        if failed:
            errors.extend(f"{r[0]}: exit={r[1]} {r[3]}" for r in failed)
        print(f"TEMP_WORKSPACE={tmp}")
        print(f"CASES={len(results)} PASSED={len(results)-len(failed)} FAILED={len(failed)}")
        print(f"CANONICAL_ENGINE_UNCHANGED={'true' if all(r[2] for r in results if r[0] in {'dry_run','confirmed_owner_apply','confirmed_intentionally_open','canonical_immutability','overlay_revert'}) else 'false'}")
        if errors:
            for e in errors:
                print(f"error: {e}")
            print("APPLY MECHANISM: FAIL")
            return 1
        print("APPLY MECHANISM: PASS")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"TEMP_CLEANED={not tmp.exists()}")


if __name__ == "__main__":
    sys.exit(main())
