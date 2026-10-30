"""Offline structural checks. Passing does not prove model behavior or Cofa compatibility."""
from pathlib import Path
import hashlib
import json
import re
import sys


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    skill = root / 'skills/data-mission-partner'
    required = ['README.md', 'START_HERE.md', 'NOTICE.md', 'LICENSE',
                'docs/REVIEW.md', 'docs/VALIDATION.md', 'checks/scenarios.json',
                'skills/data-mission-partner/SKILL.md',
                'skills/data-mission-partner/agents/openai.yaml']
    for rel in required:
        if not (root / rel).is_file(): errors.append('missing: ' + rel)
    if errors: return errors
    core = (skill / 'SKILL.md').read_text(encoding='utf-8')
    if not core.startswith('---\n') or '\n---\n' not in core[4:]:
        errors.append('missing frontmatter')
    if 'name: data-mission-partner\n' not in core:
        errors.append('wrong skill name')
    if not re.search(r'^description: ".+"$', core, flags=re.M):
        errors.append('missing description')
    if len(core.splitlines()) > 110:
        errors.append('core exceeds the authored 110-line limit')
    if len(list((root/'skills').rglob('SKILL.md'))) != 1:
        errors.append('more than one entry skill')
    yaml = (skill/'agents/openai.yaml').read_text(encoding='utf-8')
    if not re.search(r'^policy:\n  allow_implicit_invocation: true\s*$',yaml,re.M):
        errors.append('implicit invocation not explicitly enabled')
    if '$data-mission-partner' not in yaml:
        errors.append('default prompt does not name skill')
    desc=re.search(r'  short_description: "(.+)"', yaml)
    if not desc or not 25 <= len(desc.group(1)) <= 64:
        errors.append('short_description not 25..64 chars')
    paths = sorted(p for p in root.rglob('*') if p.is_file() and not ({'.git', '__pycache__'} & set(p.relative_to(root).parts)))
    for file in paths:
        rel = file.relative_to(root)
        if file.is_symlink(): errors.append('symlink: '+str(rel))
        if file.suffix not in {'.md','.txt','.json','.yaml','.py'} and file.name not in {'.gitignore','LICENSE'}:
            errors.append('unexpected file: '+str(rel)); continue
        data = file.read_text(encoding='utf-8')
        if file.suffix=='.md':
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',data):
                if '://' in target or target.startswith('#'): continue
                check = (file.parent / target.split('#')[0]).resolve()
                if not check.is_relative_to(root) or not check.exists():
                    errors.append('broken local link: '+str(rel)+' -> '+target)
        # Known private identifiers must not be distributed. This is not a complete secret scanner.
        if re.search(r'cand_[A-Za-z0-9]{6,}|sk-proj-[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{15,}',data):
            errors.append('possible private identifier: '+str(rel))
    refs=list((skill/'references').glob('*.md'))
    if len(refs)!=5: errors.append('expected five focused reference files')
    for p in refs:
        if 'references/'+p.name not in core: errors.append('unrouted reference: '+p.name)
    for license_file in ['ColdTbrew-MIT.txt','JINwonLEE-MIT.txt','JINwonLEE-UPSTREAM-NOTICE.txt','pstack-NOTICE.txt','PROJECT-MIT.txt']:
        p=skill/'licenses'/license_file
        if not p.is_file(): errors.append('missing attribution: '+license_file)
    if (skill/'licenses/PROJECT-MIT.txt').is_file() and (root/'LICENSE').read_bytes()!=(skill/'licenses/PROJECT-MIT.txt').read_bytes():
        errors.append('project license copy differs')
    scenarios=json.loads((root/'checks/scenarios.json').read_text(encoding='utf-8'))
    if scenarios.get('kind')!='DESIGNED_NOT_EXECUTED_WITH_MODEL':
        errors.append('scenario execution boundary missing')
    cases=scenarios.get('cases',[])
    if len(cases)!=22 or len({c['id'] for c in cases})!=22:
        errors.append('expected 22 unique designed cases')
    return errors


if __name__=='__main__':
    base=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
    issues=validate(base)
    print(json.dumps({'structural_validation':'FAIL' if issues else 'PASS',
                      'model_behavior_evaluated':False, 'cofa_runtime_evaluated':False,
                      'errors':issues},ensure_ascii=False,indent=2))
    raise SystemExit(1 if issues else 0)
