"""Bookkeeping controls for the unattended D133/D134 continuation.

Temporary fixtures exercise real file locks, receipt preservation,
authentication and mutable-document updates. No mathematical driver runs.
"""
from contextlib import redirect_stdout
import fcntl
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / 'dembele/pari/run_d133_completion.py'
spec = importlib.util.spec_from_file_location('continuation', TARGET)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class Controls(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='d133-completion-controls-')
        self.root = Path(self.scratch.name)
        self.data = self.root / 'dembele/data/computed'
        self.data.mkdir(parents=True)
        self.patches = [patch.object(c, 'ROOT', self.root), patch.object(c, 'DATA', self.data)]
        for change in self.patches:
            change.start()

    def tearDown(self):
        for change in reversed(self.patches):
            change.stop()
        self.scratch.cleanup()

    def test_live_production_lock_waits_then_remains_exclusive(self):
        path = self.data / (c.BASE + '.lock')
        owner = path.open('a+b')
        fcntl.flock(owner, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sleeping = threading.Event()
        release_wait = threading.Event()
        result, errors = [], []
        def sleep(_):
            sleeping.set()
            assert release_wait.wait(2)
        def follower():
            try:
                result.append(c.wait_for_production())
            except BaseException as error:
                errors.append(error)
        with patch.object(c, 'time', SimpleNamespace(sleep=sleep)), redirect_stdout(io.StringIO()):
            thread = threading.Thread(target=follower)
            thread.start()
            try:
                self.assertTrue(sleeping.wait(2))
                self.assertEqual(result, [])
                self.assertEqual(errors, [])
                (self.data / (c.BASE + '_completed.json')).write_text(json.dumps(
                    {'status': 'pass', 'all_phases_complete': True, 'maximum_workers': 3}))
                sealed = self.data / 'dyadic_rowjournal_P6400_col00_d132/SEALED.json'
                sealed.parent.mkdir()
                sealed.write_text('{}')
                owner.close()
            finally:
                release_wait.set()
                thread.join(3)
                owner.close()
            self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(len(result), 1)
            with path.open('a+b') as other:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result[0].close()

    def test_incomplete_production_stops_without_a_job(self):
        with patch.object(c.subprocess, 'run', side_effect=AssertionError('must not launch')) as launch:
            with self.assertRaises(FileNotFoundError):
                c.main()
            launch.assert_not_called()

    def test_failed_receipt_is_preserved_without_retry(self):
        path = self.data / 'example_attempt01.job.json'
        original = '{"status":"fail","exit_code":1}\n'
        path.write_text(original)
        with patch.object(c.subprocess, 'run', side_effect=AssertionError('must not retry')) as launch:
            with self.assertRaises(AssertionError):
                c.capped('driver.py', 'example_attempt01', 'PASS')
            launch.assert_not_called()
        self.assertEqual(path.read_text(), original)

    def test_passing_receipt_reused_and_altered_log_rejected(self):
        driver = self.root / 'driver.py'
        driver.write_text('# fixture; never executed\n')
        log = self.data / 'example_attempt01.log'
        log.write_text('PASS\n')
        packet = {'status': 'pass', 'exit_code': 0, 'timeout_seconds': 180,
                  'timeout_terminates_process_group': True,
                  'command': ['python3', str(driver)],
                  'driver': c.source(driver), 'log': c.source(log)}
        (self.data / 'example_attempt01.job.json').write_text(json.dumps(packet))
        with patch.object(c.subprocess, 'run', side_effect=AssertionError('must not rerun')) as launch:
            with redirect_stdout(io.StringIO()):
                self.assertEqual(c.capped('driver.py', 'example_attempt01', 'PASS'), packet)
            log.write_text('changed\n')
            with self.assertRaises(AssertionError):
                c.capped('driver.py', 'example_attempt01', 'PASS')
            launch.assert_not_called()

    def test_document_updates_are_idempotent_and_links_resolve(self):
        for name in c.DOCS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# Fixture\n\nHistorical content.\n\n*Maintenance note: keep history.*\n')
        for name in ('dyadic-precision6400-d133.md', 'arithmetic-twist-classification-d134.md'):
            path = self.root / 'dembele/certificates' / name
            path.parent.mkdir(exist_ok=True)
            path.write_text('fixture\n')
        for name in ('dyadic_precision6400_completion_d133', 'arithmetic_cover_criterion_completion_d134'):
            (self.data / (name + '.json')).write_text('{}')
        import re
        for milestone in (133, 134):
            packet = {'passing_input_jobs': 24577 if milestone == 133 else 1, 'sources': [None] * 3}
            c.checkpoint_docs(milestone, packet)
            saved = {name: (self.root / name).read_text() for name in c.DOCS}
            c.checkpoint_docs(milestone, packet)
            for name, content in saved.items():
                path = self.root / name
                self.assertEqual(content, path.read_text())
                self.assertIn('Historical content.', content)
                self.assertEqual(content.count(f'<!-- D{milestone} reviewed continuation checkpoint -->'), 1)
                for link in re.findall(r'\]\(([^)]+)\)', content):
                    self.assertTrue((path.parent / link).resolve().is_file(), (name, link))

    def test_completed_artifacts_cannot_be_changed(self):
        path = self.data / 'fixed.json'
        c.put(path, 'original\n')
        c.put(path, 'original\n')
        with self.assertRaises(AssertionError):
            c.put(path, 'changed\n')
        self.assertEqual(path.read_text(), 'original\n')


if __name__ == '__main__':
    output = ROOT / 'dembele/data/computed/dyadic_continuation_controls_d133.json'
    assert not output.exists(), 'completed controls are not rerun'
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    assert result.wasSuccessful() and result.testsRun == 6
    packet = {'status': 'pass', 'milestone': 'D133', 'kind': 'nonmathematical_completion_controls',
              'passing_fixture_controls': result.testsRun, 'mathematical_driver_jobs_launched': 0,
              'scope': 'Real lock ordering, stop on incomplete/failed inputs, receipt authentication, idempotent documentation, immutable artifacts.',
              'sources': [c.source(Path(__file__)), c.source(TARGET)]}
    with output.open('x') as stream:
        stream.write(json.dumps(packet, indent=2) + '\n')
    print('PASS|D133_CONTINUATION_CONTROLS', flush=True)
