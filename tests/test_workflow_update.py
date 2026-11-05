"""Structural and package regression tests, NOT model behavior or domain-solver tests."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest import mock
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'data-mission-partner'
spec = importlib.util.spec_from_file_location('update_installer', ROOT/'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
PATTERNS = ('comparison', 'change-review', 'allocation', 'schedule-preference',
            'spatial-review', 'measurement-quality', 'relationship-impact', 'learning-content')


def snapshot(root):
    return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}


def links(path):
    for t in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        u=urlsplit(t)
        if u.scheme or not u.path: continue
        yield (path.parent/u.path).resolve()


class WorkflowUpdateTests(unittest.TestCase):
    def test_single_entry_and_bounded_core(self):
        self.assertEqual(len(list((ROOT/'skills').rglob('SKILL.md'))), 1)
        self.assertLessEqual(len((SKILL/'SKILL.md').read_text(encoding='utf-8').splitlines()),110)
        core_refs = {'collaboration.md', 'data-checks.md', 'debugging.md',
                     'tools-and-models.md', 'delivery-checks.md'}
        self.assertTrue(core_refs.issubset({p.name for p in (SKILL/'references').glob('*.md')}))

    def test_all_eight_patterns_are_linked(self):
        linked=set(links(SKILL/'references/patterns/index.md'))
        for name in PATTERNS:
            self.assertIn((SKILL/f'references/patterns/{name}.md').resolve(),linked)
        self.assertIn((SKILL/'references/patterns/other-work.md').resolve(),linked)

    def test_all_reference_documents_reachable(self):
        pending=[(SKILL/'SKILL.md').resolve()];seen=set()
        while pending:
            p=pending.pop()
            if p in seen or p.suffix!='.md':continue
            seen.add(p);pending.extend(links(p))
        for p in (SKILL/'references').rglob('*.md'):
            self.assertIn(p.resolve(),seen)

    def test_source_validates_without_registration(self):
        source,files=installer.validate_source(SKILL)
        self.assertEqual(source,SKILL.resolve())
        self.assertIn(SKILL/'references/workflows/parallel.md',files)
        self.assertIn(SKILL/'references/workflows/submission-understanding.md',files)

    def test_metadata_allows_but_does_not_claim_implicit_success(self):
        t=(SKILL/'agents/openai.yaml').read_text(encoding='utf-8')
        self.assertIn('allow_implicit_invocation: true',t)
        desc=re.search('short_description: "(.+)"',t).group(1)
        self.assertTrue(25 <= len(desc) <= 64)
        self.assertIn('$data-mission-partner',t)

    def test_designed_scenarios_not_claimed_as_model_runs(self):
        c=json.loads((ROOT/'checks/expanded_scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(c['kind'],'DESIGNED_NOT_EXECUTED_WITH_MODEL')
        self.assertEqual(len(c['cases']),28)
        self.assertEqual(len({x['id'] for x in c['cases']}),28)
        for case in c['cases']:
            p=(ROOT/case['expected_reference']).resolve()
            self.assertTrue(p.is_file(),case['id'])
            self.assertTrue(p.is_relative_to(SKILL))
            self.assertTrue(case['criteria']);self.assertTrue(case['must_not'])

    def test_pattern_sections_are_consistent(self):
        for name in PATTERNS:
            t=(SKILL/f'references/patterns/{name}.md').read_text(encoding='utf-8')
            for section in ('뜻과 적용','먼저 확인','작은 첫 결과와 구조','검증할 위험','실무자 질문과 설명'):
                self.assertIn(section,t,name)

    def test_no_scripts_or_hooks_added_inside_portable_skill(self):
        self.assertFalse(list(SKILL.rglob('*.py')))
        self.assertFalse(list(SKILL.rglob('*.sh')))
        self.assertFalse(list(SKILL.rglob('*.js')))
        self.assertFalse((SKILL/'hooks').exists())

    def test_every_new_nested_document_is_required_transitively(self):
        nested=list((SKILL/'references/patterns').glob('*.md'))+list((SKILL/'references/workflows').glob('*.md'))
        with tempfile.TemporaryDirectory(dir=os.environ.get('SKILL_TEST_TMPDIR')) as temp:
            source=Path(temp)/'source';shutil.copytree(SKILL,source)
            project=Path(temp)/'project';project.mkdir()
            (project/'README.md').write_text('existing project')
            before=snapshot(project)
            for original in nested:
                p=source/original.relative_to(SKILL);data=p.read_bytes();p.unlink()
                try:
                    for mode in ([],['--apply'],['--check']):
                        with self.subTest(file=original.name,mode=mode),mock.patch.object(installer,'SOURCE',source),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                            self.assertEqual(installer.run(['--target',str(project)]+mode),2)
                            self.assertEqual(snapshot(project),before)
                            self.assertFalse((project/'.agents').exists())
                finally:p.write_bytes(data)

    def test_nested_source_symlink_is_rejected_without_writes(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('SKILL_TEST_TMPDIR')) as temp:
            source=Path(temp)/'source';shutil.copytree(SKILL,source)
            external=Path(temp)/'outside.md';external.write_text('not a reference')
            p=source/'references/patterns/comparison.md';p.unlink()
            try:p.symlink_to(external)
            except (OSError,NotImplementedError):self.skipTest('Host disallows symlinks')
            with self.assertRaises(installer.SourceError):installer.validate_source(source)

    def test_portable_copy_is_self_contained(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('SKILL_TEST_TMPDIR')) as temp:
            project=Path(temp)/'project';project.mkdir()
            with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(installer.run(['--target',str(project),'--apply']),0)
            installed=project/'.agents/skills/data-mission-partner'
            self.assertEqual(snapshot(installed),snapshot(SKILL))
            installer.validate_source(installed)

    def test_text_encoding_and_no_exam_identifiers(self):
        # Targeted publication screen; not a full security or privacy audit.
        for p in SKILL.rglob('*'):
            if not p.is_file():continue
            text=p.read_text(encoding='utf-8')
            self.assertNotRegex(text,r'cand_[A-Za-z0-9]{6,}|skhynix-[a-z-]+-persona')
            self.assertNotIn('目標',text)

if __name__=='__main__':
    unittest.main()
