#!/usr/bin/env python3
from __future__ import annotations
import collections, json, pathlib, sys
R=pathlib.Path(__file__).resolve().parents[1]; E=R/'export'; errors=[]; checks=0
def ck(c,m):
 global checks; checks+=1
 if not c: errors.append(m)
def load(p): return json.loads((E/p).read_text())
reg=load('active-roster.json'); q=load('content-request-queue.json'); cs=load('coordination-status.json'); rd=load('rule-demand.json'); fr=load('final-reconciliation.json')
ck(reg['activeHeroCount']==24,'active hero count'); ck(len(reg['activeHeroKeys'])==24 and len(set(reg['activeHeroKeys']))==24,'active keys')
bad={'cha','kar','chad','karen','002-chad','011-karen'}; ck(not (set(reg['activeHeroKeys']) & bad),'retired active keys')
ck(all(x['acronym'] in bad for x in reg['retired']),'retired provenance marked')
s=json.loads(pathlib.Path('/workspace/hy3d/output/bota-final-asset-status.json').read_text())
ck(s['generatedCount']==24 and s['blockedCount']==30,'upstream counts'); ck(s['counts']=={'blocked':30,'ready':24,'owner-decision':1,'intentionally-open':1},'upstream classification')
ck(len(s['rows'])==56 and len({r['slug'] for r in s['rows']})==56,'final evidence rows unique')
ck(len(fr['rows'])==56 and len({r['stableId'] for r in fr['rows']})==56,'reconciliation stable IDs unique')
ck(all(r.get('finalEvidenceClassification') in {'ready','blocked','owner-decision','intentionally-open'} for r in fr['rows']),'reconciliation classification exactly once')
c=collections.Counter(r['finalEvidenceClassification'] for r in fr['rows']); ck(c=={'ready':24,'blocked':30,'owner-decision':1,'intentionally-open':1},f'final disposition {dict(c)}')
ck(all(r.get('exactEvidencePaths') for r in fr['rows']),'exact evidence paths')
ck(not any(r.get('finalEvidenceClassification')=='ready' and r.get('kind') in {'clip','hero-voice'} for r in fr['rows']),'no blocked audio promoted')
ck(sum(1 for r in fr['rows'] if r.get('retiredRosterExclusion'))>=2,'retired reconciliation rows marked')
ck(reg['downstreamDrift']['oscraftDefaultDotaAcronyms']==127 and reg['downstreamDrift']['legacyBotaModelGuarantee']==26,'downstream drift recorded')
for p in ['/workspace/hy3d/output/bota-final-asset-status.json','/workspace/hy3d/output/bota-final-asset-evidence.json']: ck(pathlib.Path(p).is_file(),f'evidence {p}')
print('ACTIVE_ROSTER_COUNTS active=24 ready=24 blocked=30 owner-decision=1 intentionally-open=1 reconciled=56')
if errors:
 print(f'ACTIVE ROSTER: FAIL ({checks} checks, {len(errors)} errors)'); print('\n'.join(errors)); sys.exit(1)
print(f'ACTIVE ROSTER: PASS ({checks} checks, 0 errors)')
