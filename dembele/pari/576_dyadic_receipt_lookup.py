"""D139 receipt discovery without a directory scan for each phase.

The exact lookup covers the old glob's entire 00..99 range. The inventory
is a snapshot for read-only checks, or for one coordinator that owns its
output prefix under its exclusive lock. Rebuild it on resume. Register
completed attempts and reconcile it before publishing a completion record.
Receipt contents and hashes are deliberately not cached.
"""
import json
import os
from pathlib import Path
import re


def valid_stem(stem):
    assert re.fullmatch(r'[A-Za-z0-9_]+', stem) and '_attempt' not in stem


def exact_receipts(directory, stem):
    valid_stem(stem)
    directory = Path(directory)
    # lexists also retains broken links: reading one must fail, as with glob.
    return [p for n in range(100)
            if os.path.lexists(p := directory / f'{stem}_attempt{n:02d}.job.json')]


class ReceiptInventory:
    def __init__(self, directory, prefix):
        valid_stem(prefix)
        self.directory, self.prefix = Path(directory), prefix
        self.names = set()
        self.entries_scanned = 0
        with os.scandir(self.directory) as entries:
            for entry in entries:
                self.entries_scanned += 1
                if entry.name.startswith(prefix + '_') and '_attempt' in entry.name:
                    self.names.add(entry.name)
        self._index()

    def _index(self):
        self.receipts, self.logs = {}, {}
        for name in sorted(self.names):
            stem, _, suffix = name.partition('_attempt')
            if re.fullmatch(r'[0-9]{2}\.job\.json', suffix):
                self.receipts.setdefault(stem, []).append(self.directory / name)
            if suffix.endswith('.log'):
                self.logs.setdefault(stem, []).append(self.directory / name)

    def lookup(self, stem):
        valid_stem(stem)
        assert stem.startswith(self.prefix + '_')
        return self.receipts.get(stem, []).copy(), self.logs.get(stem, []).copy()

    def preflight(self, stem):
        receipts, logs = self.lookup(stem)
        for path in receipts:
            assert json.loads(path.read_text())['status'] == 'pass', (
                'inspect failed production attempt before resuming', path.name)
        assert len(receipts) <= 1, ('multiple passing receipts', stem)
        if not receipts:
            assert not (self.directory / (stem + '.json')).exists() and not logs, (
                'inspect partial job', stem)
        return receipts

    def register(self, stem, attempt):
        self.lookup(stem)
        assert 0 <= attempt < 100
        for suffix in ('.job.json', '.log'):
            name = f'{stem}_attempt{attempt:02d}{suffix}'
            assert (self.directory / name).exists()
            self.names.add(name)
        # Update only this stem, rather than rebuilding the entire inventory.
        self.receipts[stem] = exact_receipts(self.directory, stem)
        log = self.directory / f'{stem}_attempt{attempt:02d}.log'
        self.logs[stem] = sorted(set(self.logs.get(stem, []) + [log]))

    def reconcile(self):
        current = ReceiptInventory(self.directory, self.prefix)
        assert current.names == self.names, 'unexpected output-prefix attempts; inspect before publication'
        return current.entries_scanned
