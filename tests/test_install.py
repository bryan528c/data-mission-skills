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
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts' / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}


class InstallTests(unittest.TestCase):
    def setUp(self):
        temp_root = Path(os.environ.get('SKILL_TEST_TMPDIR', tempfile.gettempdir())).resolve()
        temp_root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=temp_root)
        self.assertEqual(Path(self.temp.name).resolve().parent, temp_root)
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'project'
        self.project.mkdir()
        self.dest = self.project / '.agents' / 'skills' / installer.SKILL_NAME

    def run_install(self, *extra, source=None, target=None):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()), mock.patch.object(installer, 'SOURCE', source or installer.SOURCE):
            return installer.run(['--target', str(target or self.project), *extra])

    def copy_source(self, path=None):
        path = path or Path(self.temp.name) / 'source'
        shutil.copytree(installer.SOURCE, path)
        return path

    def assert_rejected_without_changes(self, source, target=None):
        target = target or self.project
        before = snapshot(target)
        paths = {p.relative_to(target) for p in target.rglob('*')}
        for mode in [(), ('--apply',), ('--check',)]:
            with self.subTest(mode=mode):
                self.assertEqual(self.run_install(*mode, source=source, target=target), 2)
                self.assertEqual(snapshot(target), before)
                self.assertEqual({p.relative_to(target) for p in target.rglob('*')}, paths)

    def test_preview_does_not_create_files(self):
        before = snapshot(self.project)
        self.assertEqual(self.run_install(), 0)
        self.assertEqual(snapshot(self.project), before)
        self.assertFalse((self.project / '.agents').exists())

    def test_apply_includes_all_references_and_notices(self):
        self.assertEqual(self.run_install('--apply'), 0)
        self.assertEqual(snapshot(self.dest), snapshot(installer.SOURCE))
        self.assertTrue((self.dest / 'references' / 'collaboration.md').is_file())
        self.assertTrue((self.dest / 'NOTICE.md').is_file())
        self.assertEqual(self.run_install('--check'), 0)

    def test_repeated_install_keeps_content_and_timestamps(self):
        self.assertEqual(self.run_install('--apply'), 0)
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.dest.rglob('*') if p.is_file()}
        self.assertEqual(self.run_install('--apply'), 0)
        self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in before})

    def test_conflict_stops_before_other_files_are_copied(self):
        self.dest.mkdir(parents=True)
        (self.dest / 'SKILL.md').write_text('my existing skill', encoding='utf-8')
        before = snapshot(self.project)
        self.assertEqual(self.run_install('--apply'), 2)
        self.assertEqual(snapshot(self.project), before)

    def test_existing_project_instructions_data_and_settings_are_preserved(self):
        existing = {'AGENTS.md': 'existing rules', 'input.csv': 'id,value\n001,5\n', '.codex/config.toml': 'existing = true', '.env': 'DEMO=not-a-secret'}
        for rel, value in existing.items():
            path = self.project / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding='utf-8')
        before = snapshot(self.project)
        self.assertEqual(self.run_install('--apply'), 0)
        after = snapshot(self.project)
        self.assertEqual(before, {rel: after[rel] for rel in before})

    def test_missing_project_is_rejected(self):
        with self.assertRaises(installer.InstallError):
            installer.make_plan(self.project / 'missing')

    def test_file_instead_of_destination_directory_is_rejected(self):
        (self.project / '.agents').write_text('keep', encoding='utf-8')
        self.assertEqual(self.run_install('--apply'), 2)
        self.assertEqual((self.project / '.agents').read_text(encoding='utf-8'), 'keep')

    def test_check_fails_when_not_installed(self):
        self.assertEqual(self.run_install('--check'), 2)
        self.assertFalse((self.project / '.agents').exists())

    def test_symbolic_link_destination_is_rejected(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        try:
            (self.project / '.agents').symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Host does not allow creating a symbolic link.')
        self.assertEqual(self.run_install('--apply'), 2)
        self.assertEqual(snapshot(outside), {})

    def test_incomplete_source_cannot_install_or_pass_check(self):
        source = self.copy_source()
        # Even an already installed destination must not make an incomplete
        # source pass --check. Keep the complete installed copy untouched.
        self.assertEqual(self.run_install('--apply', source=source), 0)
        for rel in ['references/collaboration.md', 'SKILL.md', 'agents/openai.yaml', 'NOTICE.md',
                    'licenses/ColdTbrew-MIT.txt', 'licenses/JINwonLEE-MIT.txt',
                    'licenses/JINwonLEE-UPSTREAM-NOTICE.txt', 'licenses/pstack-NOTICE.txt',
                    'licenses/PROJECT-MIT.txt']:
            with self.subTest(missing=rel):
                path = source / rel
                content = path.read_bytes()
                path.unlink()
                try:
                    self.assert_rejected_without_changes(source)
                finally:
                    path.write_bytes(content)

    def test_incomplete_source_does_not_create_destination(self):
        source = self.copy_source()
        (source / 'references/data-checks.md').unlink()
        self.assert_rejected_without_changes(source)
        self.assertFalse((self.project / '.agents').exists())

    def test_missing_transitive_reference_is_rejected(self):
        source = self.copy_source()
        with (source / 'references/collaboration.md').open('a', encoding='utf-8') as stream:
            stream.write('\n[Related guide](missing-guide.md)\n')
        self.assert_rejected_without_changes(source)

    def test_local_reference_cannot_escape_skill(self):
        source = self.copy_source()
        (Path(self.temp.name) / 'outside.md').write_text('outside', encoding='utf-8')
        with (source / 'references/collaboration.md').open('a', encoding='utf-8') as stream:
            stream.write('\n[Outside](../../outside.md)\n')
        self.assert_rejected_without_changes(source)

    def test_install_into_source_or_its_child_is_rejected(self):
        source = self.copy_source()
        for target in [source, source / 'references']:
            with self.subTest(target=target.name):
                self.assert_rejected_without_changes(source, target)
        self.assertFalse((source / '.agents').exists())

    def test_destination_containing_source_is_rejected(self):
        source = self.copy_source(self.dest / 'source-copy')
        self.assert_rejected_without_changes(source)

    def test_direct_read_source_is_complete_without_installation(self):
        source = self.copy_source()
        checked_source, files = installer.validate_source(source)
        self.assertEqual(checked_source, source.resolve())
        self.assertIn(source / 'references/collaboration.md', files)
        self.assertFalse((self.project / '.agents').exists())
        self.assertFalse((source / '.agents').exists())


if __name__ == '__main__':
    unittest.main()
