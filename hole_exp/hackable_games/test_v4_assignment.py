"""V4 assignments are server-owned; the model is revealed after the run."""
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
from test_v4 import Client, choice
from eval_opponents import EvalOpponent, LABELS, PROTOCOL
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
                for i, (condition, model) in enumerate((c,m) for c in ('ordinary','nerfed','defensive') for m in PROTOCOL['models']):
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
                    self.assertEqual(rows[-1]['study']['assignment']['models'], list(PROTOCOL['models']))
                    self.assertEqual(random.return_value.choice.call_args_list[-1].args[0], list(PROTOCOL['models']))
                self.assertEqual(len(rows), 21)

    def test_model_revealed_only_after_both_plays_for_every_opponent(self):
        def factory(game_id, condition, model):
            bot = EvalOpponent(game_id, condition, model, Client())
            bot.fresh = lambda: factory(game_id, condition, model)
            return bot

        handler = server.Handler.__new__(server.Handler)
        for model, config in PROTOCOL['models'].items():
            with self.subTest(model=model), tempfile.TemporaryDirectory() as tmp, patch('eval_opponents.EvalOpponent', side_effect=factory):
                run = server.Run('reveal-test', 'v4_signal_notes', 'hole', 2,
                                 'ai', 0, PlayCollector(tmp), [], opponent=model)
                try:
                    for play in range(2):
                        session = run.start_next()
                        deadline = time.monotonic() + 5
                        while not session.done.is_set() and time.monotonic() < deadline:
                            self.assertNotIn('opponent', handler._play_payload(run)['run'])
                            self.assertNotIn('opponent', run.summary())
                            if session.pending:
                                turn = session.turn
                                session.submit(choice(0, 'move', session.pending['prompt']))
                                while session.pending and session.turn == turn and time.monotonic() < deadline:
                                    time.sleep(.002)
                            else:
                                time.sleep(.002)
                        self.assertTrue(session.done.is_set())
                        self.assertIsNone(session.error)
                        self.assertTrue(all(call['model'] == config['provider_model'] for call in run.ai.client.calls))
                        payload = handler._settle(run)
                        if play == 0:
                            self.assertNotIn('opponent', json.dumps(payload))
                        else:
                            self.assertEqual(payload['run']['summary']['opponent'],
                                             {'model_id': model, 'label': LABELS[model]})
                            for private in ('condition', 'systems', 'base_url', 'requested_model'):
                                self.assertNotIn(private, json.dumps(payload))
                            self.assertEqual(handler._settle(run)['run']['summary'], payload['run']['summary'])
                    self.assertEqual(len(run.scores), 2)
                finally:
                    run.kill()

    def test_unplayed_run_does_not_reveal_model_when_marked_finished(self):
        with tempfile.TemporaryDirectory() as tmp, patch('eval_opponents.EvalOpponent'):
            run = server.Run('abandoned-test', 'v4_signal_notes', 'hole', 2,
                             'ai', 0, PlayCollector(tmp), [])
            run.finished = True
            self.assertNotIn('opponent', run.summary())

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
