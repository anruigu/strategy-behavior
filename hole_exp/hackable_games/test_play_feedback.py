import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor

from collector import PlayCollector
from play_feedback import save_feedback
import play_server


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.run = SimpleNamespace(id='run-1', player='Pilot Tester', slug='pilot-tester',
            gid='v3_ref_auction_room', index=0, collector=PlayCollector(self.path),
            session=SimpleNamespace(play_id='play-1', turn=3, seed=19))
        self.handler = SimpleNamespace(_json=lambda data, code=200: (code, data))

    def submit(self, body):
        with patch.dict(play_server.RUNS, {'run-1': self.run}, clear=True):
            return play_server.Handler._feedback(self.handler, body)

    def test_multiple_submissions_use_server_identity_and_preserve_game(self):
        for text in ['First note', 'Second note\nwith unicode: café', 'First note']:
            code, data = self.submit(dict(run='run-1', text=text, player='forged', game='wrong'))
            self.assertEqual(code, 200)
            self.assertTrue(data['ok'])
        rows = [json.loads(s) for s in (self.path/'feedback.jsonl').read_text().splitlines()]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({r['feedback_id'] for r in rows}), 3)
        for r in rows:
            self.assertEqual((r['player'], r['game'], r['run_id'], r['play_id'], r['turn']),
                             ('Pilot Tester', 'v3_ref_auction_room', 'run-1', 'play-1', 3))
        self.assertEqual(self.run.session.turn, 3)

    def test_invalid_or_expired_submissions_and_disk_failure(self):
        for text in ['', '   ', None, 123, 'x'*10001]:
            self.assertEqual(self.submit(dict(run='run-1', text=text))[0], 400)
        self.assertEqual(self.submit(dict(run='expired', text='note'))[0], 404)
        self.assertFalse((self.path/'feedback.jsonl').exists())
        with patch('play_server.save_feedback', side_effect=OSError('disk error')):
            self.assertEqual(self.submit(dict(run='run-1', text='note'))[0], 503)

    def test_concurrent_appends_remain_complete_records(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda n: save_feedback(self.path, f'note {n}', player=str(n), game='game'), range(40)))
        rows = [json.loads(s) for s in (self.path/'feedback.jsonl').read_text().splitlines()]
        self.assertEqual({r['text'] for r in rows}, {f'note {n}' for n in range(40)})


if __name__ == '__main__':
    unittest.main()
