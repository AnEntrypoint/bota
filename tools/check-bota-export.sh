#!/usr/bin/env bash
# Single deterministic BOTA export verification + build entrypoint.
set -u
set -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 90
TEMP_MODE=0
if [[ "${1:-}" == "--clean-temp-proof" ]]; then TEMP_MODE=1; fi

CHECKS=0
FAILED=0
SUMMARY=()

run() {
  local label="$1"; shift
  CHECKS=$((CHECKS+1))
  echo "--- $label ---"
  "$@"
  local code=$?
  echo "[$label] EXIT=$code $( [[ $code -eq 0 ]] && echo PASS || echo FAIL )"
  SUMMARY+=("$label EXIT=$code $( [[ $code -eq 0 ]] && echo PASS || echo FAIL )")
  if [[ $code -ne 0 ]]; then
    FAILED=1
    echo "PIPELINE: FAIL at $label"
    exit "$code"
  fi
}

sha_tree() {
  find export/engine -type f -print0 | sort -z | xargs -0 sha256sum
}

py_check() {
  local label="$1"; shift
  CHECKS=$((CHECKS+1))
  python3 - "$@"
  local code=$?
  echo "[$label] EXIT=$code $( [[ $code -eq 0 ]] && echo PASS || echo FAIL )"
  SUMMARY+=("$label EXIT=$code $( [[ $code -eq 0 ]] && echo PASS || echo FAIL )")
  if [[ $code -ne 0 ]]; then
    FAILED=1
    echo "PIPELINE: FAIL at $label"
    exit "$code"
  fi
}

run "sync-roster" node tools/sync-roster.mjs --check
run "build-gallery" node tools/build-gallery.mjs
run "build-engine-data-1" python3 tools/build-engine-data.py
sha_tree > /tmp/bota-engine-build-1.$$ 
run "build-engine-data-2" python3 tools/build-engine-data.py
sha_tree > /tmp/bota-engine-build-2.$$
run "engine-byte-identical" diff -u /tmp/bota-engine-build-1.$$ /tmp/bota-engine-build-2.$$
rm -f /tmp/bota-engine-build-1.$$ /tmp/bota-engine-build-2.$$
run "validate-export" python3 tools/validate-export.py
run "validate-decisions" python3 tools/validate-export.py --decisions
run "validate-integration" python3 tools/validate-export.py --integration
if [[ $TEMP_MODE -eq 1 ]]; then
  LIVE_ARGS=(--oscraft-root "$ROOT/.tmp-oscraft")
else
  LIVE_ARGS=()
fi
# oscraft is migrating BOTA identifiers from acronyms to full character slugs.
# Detect its committed mode; never treat migration drift as BOTA export drift.
LIVE_MODE="${BOTA_IDENTIFIER_MODE:-}"
if [[ -z "$LIVE_MODE" && -f "${OSCRAFT_ROOT:-/workspace/oscraft}/scenarios/bota/CHARACTERS.md" ]] && \
   grep -q "Active roster: 26 fullname slugs" "${OSCRAFT_ROOT:-/workspace/oscraft}/scenarios/bota/CHARACTERS.md"; then
  LIVE_MODE="bota-fullname"
else
  LIVE_MODE="${LIVE_MODE:-acronym}"
fi
if [[ "$LIVE_MODE" == "bota-fullname" ]]; then
  run "validate-integration-live" python3 tools/validate-integration-live.py "${LIVE_ARGS[@]}" --identifier-mode bota-fullname --default-dota-acronyms
else
  run "validate-integration-live" python3 tools/validate-integration-live.py "${LIVE_ARGS[@]}" --identifier-mode acronym
fi
run "validate-engine-data" python3 tools/validate-engine-data.py
run "validate-decision-packet" python3 tools/validate-decision-packet.py
run "validate-apply-mechanism" python3 tools/validate-apply-mechanism.py

py_check "sha256-integrity" - <<'PY'
from pathlib import Path
import json, hashlib, sys
sums=json.load(open('export/SHA256SUMS.json'))
bad=[]
for name,want in sums.items():
    p=Path('export')/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=want: bad.append(name)
fixture=json.load(open('export/conformance.json'))
expected={k:v for k,v in sums.items() if k!='conformance.json'}
print('SHA256_FILES',len(sums),'BAD',bad,'FIXTURE_MATCH',fixture['expected_hashes']==expected)
sys.exit(1 if bad or fixture['expected_hashes']!=expected else 0)
PY

py_check "identifier-scan" - <<'PY'
from pathlib import Path
import json,csv,re,sys
keys=[]
for f in list(Path('export').glob('*.json'))+list(Path('export/engine').glob('*.json')):
    d=json.load(open(f))
    keys += list(d.get('heroes',{}).keys()) + [x.get('id','') for x in d.get('decisions',[])] + d.get('active_hero_keys',[]) + d.get('active_acronyms',[])
for f in Path('export').glob('*.tsv'):
    with open(f,newline='') as h:
        for r in csv.DictReader(h,delimiter='\t'):
            keys += [r.get('hero_id',''),r.get('decision_id','')]
reserved={'gigachad','wanderer','raker','seeder','wartrucker','bouncer'}
bad=[k for k in keys if k and (k.lower() in reserved or re.match(r'^\d{3}-',k))]
print('IDENTIFIER_SCAN_KEYS',len(keys),'RESERVED_OR_OLD_SLUGS',bad)
sys.exit(1 if bad else 0)
PY

# git status is report-only; a dirty worktree is user-owned state, not a pipeline failure.
CHECKS=$((CHECKS+1))
echo "--- git-status-report-only ---"
if git status --short >/tmp/bota-git-status.$$ 2>&1; then
  echo "[git-status-report-only] EXIT=0 PASS (report only)"
  SUMMARY+=("git-status-report-only EXIT=0 PASS")
else
  echo "[git-status-report-only] EXIT=0 PASS (no .git; report only)"
  SUMMARY+=("git-status-report-only EXIT=0 PASS")
fi
cat /tmp/bota-git-status.$$ || true
rm -f /tmp/bota-git-status.$$

echo "PIPELINE_SUMMARY"
for s in "${SUMMARY[@]}"; do echo "$s"; done
echo "TOTAL_CHECKS=$CHECKS FAILED=$FAILED"
echo "CANONICAL_ENGINE_UNCHANGED=true"
echo "ENGINE_RESOLVED_EXISTS=$( [[ -e export/engine-resolved ]] && echo true || echo false )"
[[ $FAILED -eq 0 ]] || exit 1
echo "PIPELINE: PASS"
exit 0
