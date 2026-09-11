from pathlib import Path
import tempfile
import unittest
from backup import snapshot


class SnapshotTests(unittest.TestCase):
    def test_complete_lines_and_nested_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); src = root/'source'; src.mkdir()
            (src/'assignments.jsonl').write_bytes(b'{"run":1}\n{"run":')
            (src/'players').mkdir()
            (src/'players'/'plays.jsonl').write_bytes(b'{"move":2}\n')
            rows = snapshot(src, root/'copy')
            self.assertEqual((root/'copy'/'assignments.jsonl').read_bytes(), b'{"run":1}\n')
            self.assertEqual(len(rows), 2)
            self.assertEqual((src/'assignments.jsonl').read_bytes(), b'{"run":1}\n{"run":')
            self.assertGreater(rows[0]['source_bytes'], rows[0]['bytes'])

    def test_rejects_corrupt_complete_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'source'; src.mkdir()
            (src/'plays.jsonl').write_bytes(b'not json\n')
            with self.assertRaises(ValueError): snapshot(src, Path(tmp)/'copy')

    def test_rejects_symlinks_and_empty_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'source'; src.mkdir()
            with self.assertRaises(ValueError): snapshot(src, Path(tmp)/'copy')
            (src/'outside').symlink_to('/etc/passwd')
            with self.assertRaises(ValueError): snapshot(src, Path(tmp)/'copy')


if __name__ == '__main__': unittest.main()
