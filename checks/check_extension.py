"""Check the portable extension only. Does not evaluate agent behavior or public deployment."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

def validate(root):
    root=Path(root).resolve()
    errors=[]
    spec=importlib.util.spec_from_file_location('extension_installer',root/'scripts/install.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    try:source,files=module.validate_source(root/'skills/data-mission-partner')
    except module.SourceError as exc:return [str(exc)]
    core=(source/'SKILL.md').read_text(encoding='utf-8')
    if len(core.splitlines())>110:errors.append('Core too long')
    if len(list((root/'skills').rglob('SKILL.md')))!=1:errors.append('Expected one entry skill')
    if not core.startswith('---\nname: data-mission-partner\n'):errors.append('Incorrect metadata')
    config=(source/'agents/openai.yaml').read_text(encoding='utf-8')
    if 'allow_implicit_invocation: true' not in config:errors.append('Implicit invocation policy changed')
    domains=list((source/'references/domains').glob('*.md'))
    if len(domains)!=8:errors.append('Expected eight optional domain references')
    for p in domains:
        t=p.read_text(encoding='utf-8')
        for term in ['## 먼저 이해할 말','## 작은 첫 결과와 분업','## 놓치기 쉬운 검사','## 한 사례로 설명','## 설명 준비','공개 배경:']:
            if term not in t:errors.append(p.name+': missing '+term)
    cases=json.loads((root/'checks/coverage_scenarios.json').read_text(encoding='utf-8'))
    if cases.get('kind')!='DESIGNED_NOT_EXECUTED_WITH_MODEL':errors.append('Unclear eval status')
    if len(cases.get('cases',[]))!=36 or len({v['id'] for v in cases['cases']})!=36:errors.append('Expected 36 designed cases')
    expected={p.stem for p in domains}
    observed={v['domain'] for v in cases['cases'] if v.get('domain')}
    if expected!=observed:errors.append('Case coverage incomplete')
    for p in files:
        if p.suffix in {'.md','.yaml','.json','.txt'}:
            text=p.read_text(encoding='utf-8')
            if re.search(r'cand_[a-zA-Z0-9]{6,}|sk-proj-[a-zA-Z0-9]{10,}|ghp_[a-zA-Z0-9]{15,}',text):errors.append('Possible secret: '+p.name)
            if '-persona' in text:errors.append('Assessment identifier in portable skill: '+p.name)
    if (source/'licenses/PROJECT-MIT.txt').read_bytes()!=(root/'LICENSE').read_bytes():errors.append('License copy differs')
    return errors

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
    issues=validate(root)
    print(json.dumps({'portable_extension':'FAIL' if issues else 'PASS',
                     'model_behavior_evaluated':False,'cofa_runtime_evaluated':False,
                     'public_update_verified':False,'errors':issues},ensure_ascii=False,indent=2))
    raise SystemExit(1 if issues else 0)
