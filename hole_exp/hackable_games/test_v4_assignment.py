"""Public V4 assignments are server-owned, durable and hidden."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from test_v4 import Client
from eval_opponents import EvalOpponent
from collector import PlayCollector
import play_server as server


class AssignmentTests(unittest.TestCase):
    def test_assignments_ignore_client_and_are_recorded(self):
        def factory(game_id, condition, model):
            return EvalOpponent(game_id, condition, model, Client())
        with tempfile.TemporaryDirectory() as tmp:
            collector = PlayCollector(tmp)
            handler = server.Handler.__new__(server.Handler)
            handler._json = lambda body, status=200: (status, body)
            with patch.object(server, 'COLLECTOR', collector), patch.object(server, 'RUNS', {}), patch.object(server, 'BY_PLAYER', {}), patch.object(server, 'reap_runs'), patch.object(server, 'make_room'), patch('eval_opponents.EvalOpponent', side_effect=factory), patch.object(server.Run, 'start_next', return_value=True), patch.object(server.random, 'SystemRandom') as random:
                for i, (condition, model) in enumerate((c,m) for c in ('ordinary','nerfed','defensive') for m in ('qwen-3.8-27b','glm','claude-haiku-4.5','gpt-5-mini')):
                    random.return_value.choice.side_effect = [condition, model]
                    random.return_value.randrange.return_value = 1000 + i
                    status, payload = handler._start(dict(player='assignment-test', game='v4_trust_pledge', condition='forged', opponent='forged', seed='forged'))
                    self.assertEqual(status, 200)
                    run = server.RUNS[payload['run']['run_id']]
                    self.assertEqual(run.study['condition'], condition)
                    self.assertEqual(run.study['opponent'], model)
                    self.assertEqual(run.study['seeds'], [1000+i, 1001+i])
                    self.assertEqual(payload['run']['eval'], {'focal_seat': 0})
                    for private in ('condition', 'opponent', 'seed'):
                        self.assertNotIn(private, json.dumps(payload))
                    rows = [json.loads(line) for line in (Path(tmp)/'assignments.jsonl').read_text().splitlines()]
                    self.assertEqual(rows[-1]['study'], run.study)
                    self.assertEqual(rows[-1]['run_id'], run.id)
                    self.assertEqual(rows[-1]['study']['assignment']['method'], 'server-uniform-independent-v1')
                self.assertEqual(len(rows), 12)

    def test_failed_save_does_not_start_opponents(self):
        with tempfile.TemporaryDirectory() as tmp, patch('eval_opponents.EvalOpponent'), patch.object(server.Run, 'start_next') as start:
            collector = PlayCollector(tmp)
            handler = server.Handler.__new__(server.Handler)
            handler._json = lambda body, status=200: (status, body)
            with patch.object(server, 'COLLECTOR', collector), patch.object(collector, 'record_assignment', side_effect=OSError('disk full')):
                status, body = handler._start(dict(player='test', game='v4_trust_pledge'))
            self.assertEqual(status, 503)
            start.assert_not_called()
            self.assertNotIn('disk full', str(body))


if __name__ == '__main__':
    unittest.main()
