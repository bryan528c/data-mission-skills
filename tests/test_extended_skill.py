"""Structural installer regressions, not model-response or Cofa runtime tests."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('extended_installer', ROOT/'scripts/install.py')
i = importlib.util.module_from_spec(spec)
spec.loader.exec_module(i)

def snapshot(root):
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}

class ExtendedInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=os.environ.get('SKILL_TEST_TMPDIR'))
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.source=self.base/'source'
        shutil.copytree(i.SOURCE,self.source)
        self.target=self.base/'project'
        self.target.mkdir()

    def run_install(self,*args):
        with mock.patch.object(i,'SOURCE',self.source), contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            return i.run(['--target',str(self.target),*args])

    def rejected(self):
        before=snapshot(self.target)
        paths={p.relative_to(self.target) for p in self.target.rglob('*')}
        for mode in [(),('--apply',),('--check',)]:
            self.assertEqual(self.run_install(*mode),2)
            self.assertEqual(snapshot(self.target),before)
            self.assertEqual({p.relative_to(self.target) for p in self.target.rglob('*')},paths)

    def test_all_eight_domains_installed(self):
        self.assertEqual(self.run_install('--apply'),0)
        dest=self.target/'.agents/skills'/i.SKILL_NAME
        self.assertEqual(snapshot(dest),snapshot(self.source))
        self.assertEqual(len(list((dest/'references/domains').glob('*.md'))),8)
        self.assertEqual(self.run_install('--check'),0)

    def test_each_domain_missing_rejected(self):
        for p in list((self.source/'references/domains').glob('*.md')):
            with self.subTest(p=p.name):
                b=p.read_bytes();p.unlink()
                try:self.rejected()
                finally:p.write_bytes(b)

    def test_new_core_reference_missing_rejected(self):
        for name in ['parallel-work','implementation-proof','scenario-router']:
            with self.subTest(name=name):
                p=self.source/'references'/(name+'.md');b=p.read_bytes();p.unlink()
                try:self.rejected()
                finally:p.write_bytes(b)

    def test_empty_domain_rejected(self):
        (self.source/'references/domains/meal-planning.md').write_text('  ',encoding='utf-8')
        self.rejected()

    def test_unrouted_domain_rejected(self):
        p=self.source/'references/scenario-router.md'
        p.write_text(p.read_text(encoding='utf-8').replace('(domains/market-comparison.md)','(domains/supplier-change.md)'),encoding='utf-8')
        self.rejected()

    def test_unlinked_additional_reference_rejected(self):
        (self.source/'references/unlinked.md').write_text('# Lost document',encoding='utf-8')
        self.rejected()

    def test_local_anchor_and_link_cycle_do_not_hang(self):
        p=self.source/'references/domains/market-comparison.md'
        p.write_text(p.read_text(encoding='utf-8')+'\n[back](../scenario-router.md)\n[self](#example)\n',encoding='utf-8')
        self.assertEqual(self.run_install('--apply'),0)

    def test_conflict_with_form_keeps_both(self):
        (self.target/'official-form.json').write_text('{"fixed": "keep"}')
        self.assertEqual(self.run_install('--apply'),0)
        dest=self.target/'.agents/skills'/i.SKILL_NAME/'references/domains/market-comparison.md'
        dest.write_text('user edits')
        self.rejected()
        self.assertEqual((self.target/'official-form.json').read_text(encoding='utf-8'),'{"fixed": "keep"}')

    def test_transitive_escaped_domain_link_rejected(self):
        outside=self.base/'outside.md';outside.write_text('keep')
        p=self.source/'references/domains/overlay-quality.md'
        p.write_text(p.read_text(encoding='utf-8')+'\n[out](../../../outside.md)\n',encoding='utf-8')
        self.rejected()

    def test_source_symbolic_link_rejected(self):
        outside=self.base/'outside.md';outside.write_text('not copied')
        p=self.source/'references/domains/market-comparison.md';p.unlink()
        try:p.symlink_to(outside)
        except (OSError,NotImplementedError):self.skipTest('symlink unavailable')
        self.rejected()

    def test_unicode_project_and_reinstall_unchanged(self):
        self.target=self.base/'연습 폴더';self.target.mkdir()
        self.assertEqual(self.run_install('--apply'),0)
        before={p:(p.read_bytes(),p.stat().st_mtime_ns) for p in self.target.rglob('*') if p.is_file()}
        self.assertEqual(self.run_install('--apply'),0)
        self.assertEqual(before,{p:(p.read_bytes(),p.stat().st_mtime_ns) for p in before})

    def test_new_refs_cannot_be_installed_into_source(self):
        self.target=self.source/'references/domains'
        self.rejected()

if __name__=='__main__':unittest.main()
