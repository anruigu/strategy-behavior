"""Offline V4 integration checks; never call a hosted provider."""
import json
import tempfile
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import catalog
import play_server
import server
import views
from collector import PlayCollector
from hosted_opponents import HostedConfig, HostedOpponent, HTTPClient
from test_views import _from_view


class FakeClient:
    def __init__(self, answer=lambda messages: '[act: check]'):
        self.requests = []
        self.answer = answer
        self.chat = SimpleNamespace(completions=self)

    def create(self, **request):
        self.requests.append(request)
        return SimpleNamespace(model='test-model', usage=None, choices=[
            SimpleNamespace(message=SimpleNamespace(content=self.answer(request['messages'])), finish_reason='stop')])


class HostedTests(unittest.TestCase):
    def test_native_http_transport_retries_and_sends_chat_request(self):
        import threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_POST(self):
                requests.append((self.path, self.headers.get('Authorization'),
                    json.loads(self.rfile.read(int(self.headers['Content-Length'])))))
                if len(requests) == 1:
                    self.send_response(429)
                    self.end_headers()
                    return
                body = json.dumps({'model': 'test-model', 'usage': {'total_tokens': 12},
                    'choices': [{'finish_reason': 'stop', 'message': {'content': '[act: call]'}}]}).encode()
                self.send_response(200)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            client = HTTPClient(f'http://127.0.0.1:{server.server_port}/v1', 'test-key')
            bot = HostedOpponent(HostedConfig('test-model', 'unused', 'TEST_KEY'), client)
            self.assertEqual(bot(1, 'bet', 'Your card is KING'), '[act: call]')
            self.assertEqual(len(requests), 2)
            self.assertEqual(requests[1][0], '/v1/chat/completions')
            self.assertEqual(requests[1][1], 'Bearer test-key')
            self.assertEqual(requests[1][2]['model'], 'test-model')
            self.assertEqual(bot.records[0]['usage']['total_tokens'], 12)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_private_memory_and_incomplete_reply(self):
        client = FakeClient()
        bot = HostedOpponent(HostedConfig('test', 'https://example.test', 'TEST_KEY'), client)
        bot(1, 'bet', 'private card KING')
        bot(2, 'bet', 'private card JACK')
        bot(1, 'show', 'declare your card')
        self.assertNotIn('KING', json.dumps(client.requests[1]))
        self.assertNotIn('JACK', json.dumps(client.requests[2]))
        self.assertIn('KING', json.dumps(client.requests[2]))
        client.answer = lambda messages: ''
        with self.assertRaises(RuntimeError): bot(1, 'bet', 'next')

    def test_truncated_reasoning_retries_same_model_with_larger_budget(self):
        class TruncatedFirst(FakeClient):
            def create(self, **request):
                result = super().create(**request)
                if len(self.requests) == 1:
                    result.choices[0].finish_reason = 'length'
                    result.choices[0].message.content = ''
                return result
        client = TruncatedFirst(lambda _: '[choice: 1]')
        bot = HostedOpponent(HostedConfig('qwen3.8-27b', 'https://inference.flt.build/v1', 'TEST_KEY'), client)
        self.assertEqual(bot(1, 'move', 'Choose'), '[choice: 1]')
        self.assertEqual([r['max_tokens'] for r in client.requests], [4096, 8192])
        self.assertTrue(all(r['model'] == 'qwen3.8-27b' for r in client.requests))
        self.assertEqual(client.requests[0]['reasoning'], {'effort': 'low'})
        self.assertEqual(len(bot.memory[1]), 2)
        self.assertEqual(bot.records[0]['error'], 'truncated_response')

    def test_every_v4_game_routes_opponents_and_has_boards(self):
        for gid in catalog.V4_IDS:
            c = catalog.GAMES[gid]

            seen = set()
            def ask(pid, phase, prompt):
                if pid:
                    seen.add(pid)
                view = views.build(c['board_id'], phase, prompt)
                self.assertIsNotNone(view, (gid, phase))
                return _from_view(view, phase, prompt)
            ep = c['game'].run(ask, 0, 'hole')
            self.assertEqual(seen, set(range(1, c['n_players'])), gid)
            self.assertIn(0, ep.scores)

    def test_complete_play_persistence_and_repeated_settlement(self):
        gid = 'v4_ta_ipd_palmers_word'
        def answer(messages): return '[move: cooperate]'
        client = FakeClient(answer)
        with tempfile.TemporaryDirectory() as tmp, patch.object(HostedConfig, 'client', return_value=client):
            collector = PlayCollector(tmp)
            run = play_server.Run('test', gid, 'hole', 1, 'ai', 0, collector, [])
            session = run.start_next()
            deadline = time.monotonic() + 10
            turn = 0
            while not session.done.is_set() and time.monotonic() < deadline:
                state = session.state()
                if state['pending'] and state['turn'] != turn:
                    turn = state['turn']
                    p = state['pending']
                    session.submit(_from_view(views.build('v3_ta_ipd_palmers_word', p['phase'], p['prompt']), p['phase'], p['prompt']))
                time.sleep(.001)
            self.assertTrue(session.done.is_set())
            self.assertIsNone(session.error)
            handler = object.__new__(play_server.Handler)
            first = handler._settle(run)
            second = handler._settle(run)
            self.assertEqual(first['play_result'], second['play_result'])
            self.assertEqual(len(run.scores), 1)
            rows = collector.player_plays('test')
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['bots'], 'ai')
            self.assertTrue(rows[0]['opponent']['decisions'])
            self.assertEqual(rows[0]['engine_version'], 'v4-symmetric-1')
            self.assertTrue(rows[0]['engine_trace']['events'])
            self.assertEqual(set(e['player'] for e in rows[0]['engine_trace']['events']), {0, 1})
            self.assertNotIn('engine_trace', session.public_state())
            self.assertNotIn('opponent', session.public_state())

    def test_parallel_metadata_cannot_overwrite_newer_transcript(self):
        with tempfile.TemporaryDirectory() as tmp:
            collector = PlayCollector(tmp)
            pid = collector.start(player='parallel-log', game='v4_ta_winasmuch_talk', seat=0,
                arm='hole', seed=0, bots='ai', run_id='test', play_index=0)
            newest = dict(model='test-model', decisions=[{'pid': n} for n in (1, 2, 3)])
            collector.record_opponent(pid, newest)
            collector.record_opponent(pid, dict(model='test-model', decisions=[{'pid': 1}]))
            collector.finish(pid, None, abandoned=True)
            self.assertEqual(collector.player_plays('parallel-log')[0]['opponent'], newest)

    def test_move_returns_while_hosted_opponent_is_thinking(self):
        import threading
        release = threading.Event()
        class SlowClient(FakeClient):
            def create(self, **request):
                release.wait(5)
                return super().create(**request)
        client = SlowClient(lambda _: '[move: cooperate]')
        with tempfile.TemporaryDirectory() as tmp, patch.object(HostedConfig, 'client', return_value=client):
            run = play_server.Run('slow-test', 'v4_ta_ipd_palmers_word', 'hole', 1, 'ai', 0, PlayCollector(tmp), [])
            session = run.start_next()
            deadline = time.monotonic() + 2
            while not session.pending and time.monotonic() < deadline: time.sleep(.001)
            handler = object.__new__(play_server.Handler)
            handler._json = lambda data, *args: data
            try:
                with patch.dict(play_server.RUNS, {run.id: run}):
                    start = time.monotonic()
                    state = handler._move({'run': run.id, 'text': '[move: cooperate]'})
                    self.assertLess(time.monotonic() - start, 2)
                    self.assertNotIn('pending', state)
                    self.assertFalse(state['done'])
            finally:
                release.set()
                run.kill()
                session.done.wait(timeout=2)

    def test_provider_failure_stops_without_scripted_fallback(self):
        def broken(*args): raise RuntimeError('provider unavailable')
        session = server.Session('v4_ta_ipd_palmers_word', 0, 'hole', 0, 'ai', bot=broken)
        deadline = time.monotonic() + 5
        while not session.done.is_set() and time.monotonic() < deadline:
            if session.pending: session.submit('[move: cooperate]')
            time.sleep(.005)
        self.assertTrue(session.done.is_set())
        self.assertIn('provider unavailable', session.error)
        self.assertIsNone(session.episode)


if __name__ == '__main__':
    unittest.main()
