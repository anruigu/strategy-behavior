"""Offline fault injection for V4 opponent transport recovery."""
import unittest
from urllib.error import HTTPError
from unittest.mock import patch

from test_v4 import Client
from engines_v4 import GAMES
from eval_opponents import EvalOpponent


class RetryTests(unittest.TestCase):
    def setUp(self):
        game = GAMES['v4_trust_pledge']
        self.prompt = game.observe(game.initial(0), 1, 'communicate', 'hole')
        self.client = Client(['[statement: pledge]'])
        self.bot = EvalOpponent(game.ORIGINAL, client=self.client)

    def error(self, status, headers=None):
        return HTTPError('https://example.test', status, 'failure', headers or {}, None)

    @patch('eval_opponents.time.sleep')
    def test_recovers_after_three_failures_with_same_request(self, sleep):
        create = self.client.create
        calls = []
        def flaky(**payload):
            calls.append(payload)
            if len(calls) < 4:
                raise self.error(503, {'x-request-id': 'test-request'})
            return create(**payload)
        with patch.object(self.client, 'create', side_effect=flaky):
            self.assertEqual(self.bot(1, 'move', self.prompt), '[statement: pledge]')
        self.assertEqual(len(calls), 4)
        self.assertTrue(all(c == calls[0] for c in calls))
        self.assertEqual(len(self.bot.memory[1]), 2)
        self.assertEqual(sleep.call_count, 3)
        self.assertEqual(self.bot.records[0]['http_status'], 503)
        self.assertEqual(self.bot.records[0]['request_id'], 'test-request')

    @patch('eval_opponents.time.sleep')
    def test_permanent_http_errors_fail_once(self, sleep):
        for status in (400, 401, 403, 404):
            with self.subTest(status=status), patch.object(self.client, 'create', side_effect=self.error(status)) as create:
                with self.assertRaises(RuntimeError):
                    self.bot(1, 'move', self.prompt)
                self.assertEqual(create.call_count, 1)
        sleep.assert_not_called()
        self.assertEqual(self.bot.memory[1], [])

    @patch('eval_opponents.time.sleep')
    def test_transport_exhaustion_does_not_spend_output_allowance(self, sleep):
        with patch.object(self.client, 'create', side_effect=TimeoutError()) as create:
            with self.assertRaises(RuntimeError):
                self.bot(1, 'move', self.prompt)
        self.assertEqual(create.call_count, 4)
        self.assertEqual(sleep.call_count, 3)
        self.assertEqual(self.bot.memory[1], [])

    @patch('eval_opponents.time.sleep')
    def test_retry_after_respected(self, sleep):
        response = self.client.create(model='test', messages=[])
        with patch.object(self.client, 'create', side_effect=[self.error(429, {'Retry-After': '12'}), response]):
            self.bot(1, 'move', self.prompt)
        sleep.assert_called_once_with(12)

    @patch('eval_opponents.time.sleep')
    def test_long_retry_after_is_not_retried_early(self, sleep):
        with patch.object(self.client, 'create', side_effect=self.error(429, {'Retry-After': '120'})) as create:
            with self.assertRaises(RuntimeError):
                self.bot(1, 'move', self.prompt)
        self.assertEqual(create.call_count, 1)
        sleep.assert_not_called()


if __name__ == '__main__':
    unittest.main()
