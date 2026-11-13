#!/usr/bin/env python3
"""Clean-state proof for the consolidated BOTA export pipeline."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REAL = ROOT / "export" / "engine"


def sha_tree(root: Path):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root / "export" / "engine").glob("*.json"))}


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="bota-clean-state-"))
    try:
        # Copy repo inputs without .git; keep only paths needed by the pipeline.
        for rel in ["tools", "export", "characters", "gallery", "plan", "internal"]:
            shutil.copytree(ROOT / rel, tmp / rel, ignore=shutil.ignore_patterns("__pycache__"))
        for rel in ["ROSTER.md", "roster.yaml", "manifest.json", "README.md", "GALLERY.md", "index.html"]:
            src = ROOT / rel
            if src.exists():
                shutil.copy2(src, tmp / rel)
        # Read-only symlink for the absolute oscraft dependency.
        oscraft_link = tmp / ".tmp-oscraft"
        oscraft_link.symlink_to(Path("/workspace/oscraft"), target_is_directory=True)
        # Remove generated engine outputs to prove the pipeline recreates them.
        shutil.rmtree(tmp / "export" / "engine", ignore_errors=True)
        before_real = sha_tree(ROOT)
        # build-gallery.mjs resolves external source dirs relative to its parent.
        # Point it at the real read-only sources when present; otherwise use the copied gallery itself.
        import os
        env = os.environ.copy()
        chars = Path("/workspace/chars")
        generated = Path("/workspace/characters/memes/generated")
        env["BOTA_CHARS_DIR"] = str(chars if chars.exists() else tmp / "gallery")
        env["BOTA_GENERATED_DIR"] = str(generated if generated.exists() else tmp / "gallery")
        env["BOTA_PYTHON"] = env.get("BOTA_PYTHON", "python3")
        cmd = ["bash", "tools/check-bota-export.sh", "--clean-temp-proof"]
        print("--- clean-temp-proof consolidated pipeline ---")
        proc = subprocess.run(cmd, cwd=tmp, text=True, capture_output=True, env=env)
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        code = proc.returncode
        after_temp = sha_tree(tmp)
        identical = before_real == after_temp
        print(f"[clean-temp-proof] EXIT={code} {'PASS' if code == 0 else 'FAIL'}")
        print(f"TEMP_ENGINE_FILES={len(after_temp)} REAL_ENGINE_FILES={len(before_real)} BYTE_IDENTICAL={'true' if identical else 'false'}")
        print(f"CANONICAL_ENGINE_UNCHANGED={'true' if before_real == sha_tree(ROOT) else 'false'}")
        ok = code == 0 and identical
        print(f"CLEAN STATE PROOF: {'PASS' if ok else 'FAIL'}")
        return 0 if ok else code or 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"TEMP_CLEANED={not tmp.exists()}")


if __name__ == "__main__":
    sys.exit(main())
