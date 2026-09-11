"""Offline tests for prompted forecasts; fake transports only."""
from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import tempfile
import threading
import time
import types
import unittest
from unittest.mock import patch

from prediction import llm_forecast as forecast
from prediction.games import make_game, payoff
from prediction.io_utils import read_json, write_json
from prediction.measurements import measure_episode


class FakeForecastClient:
    def __init__(self, out, reply, statuses=None):
        self.config = replace(forecast.MODELS['kimi-k3'], temperature=0., seed=None, reasoning_effort='low')
        self.log_dir = out/'calls'
        self.reply, self.statuses = reply, iter(statuses or [])
        self.requests, self.active, self.peak = [], 0, 0
        self.lock = threading.Lock()
        self.ledger = self.stage_ledger = types.SimpleNamespace(summary=lambda: dict(committed_usd=0.))

    def generate(self, messages, purpose):
        with self.lock:
            self.active += 1
            self.peak = max(self.peak, self.active)
            self.requests.append(deepcopy(messages))
            ident = str(len(self.requests))
            status = next(self.statuses, 'ok')
        time.sleep(.005)
        reply = self.reply() if callable(self.reply) else self.reply
        record = dict(call_id=ident, status=status, config=asdict(self.config),
                      request=dict(messages=deepcopy(messages), model=self.config.provider_model,
                                   max_tokens=4096, temperature=0., extra_body={'reasoning': {'effort': 'low'}}),
                      response=dict(model=self.config.provider_model,
                                    choices=[dict(message=dict(content=reply, refusal=None), finish_reason='stop')]))
        write_json(self.log_dir/(ident+'.json'), record)
        with self.lock:
            self.active -= 1
        return reply, dict(call_id=ident, status=status, actual_model=self.config.provider_model,
                           finish_reason='stop')


class ForecastTests(unittest.TestCase):
    def setUp(self):
        root = Path('/shared/allie/home/.codex/tmp')
        root.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix='forecast-test-', dir=root)
        self.addCleanup(temporary.cleanup)
        self.out = Path(temporary.name)
        self.game = make_game('test', 3, 0, 5, 1)
        self.players = forecast.configurations(['kimi-k3', 'gemma-4-31b'])
        self.schema = forecast.target_schema(self.game)
        self.vector = {key: .5 if applicable else None for key, applicable in self.schema.items()}

    def prepare(self, modes=('zero_shot',), training=None):
        return forecast.prepare_run([self.game], self.players, training or [], modes,
                                    'kimi-k3', self.out, self.out/'global.sqlite')

    @staticmethod
    def training_row(game, own='kimi-k3', other='gemma-4-31b', suffix=''):
        actions = [(0, 1), (1, 0), (0, 0), (1, 0)]
        trace = dict(id=game['id']+suffix, game=game, models=[own, other], trial_id=0,
                     representation='matrix', swap=False, status='complete',
                     rounds=[dict(round=t, actions=list(pair), payoffs=list(payoff(game, *pair)))
                             for t, pair in enumerate(actions, 1)])
        return measure_episode(trace)[0]

    def test_probability_parser_rejects_nonfinite_bool_extra_duplicate_and_wrong_null(self):
        self.assertEqual(forecast.parse_forecast(json.dumps(self.vector), self.schema), self.vector)
        for value in [float('nan'), float('inf'), -.1, 1.1, True, '0.5', None]:
            bad = dict(self.vector, action0=value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                forecast.parse_forecast(json.dumps(bad), self.schema)
        for text in ['```json\n'+json.dumps(self.vector)+'\n```', json.dumps(dict(self.vector, explanation='x')),
                     json.dumps(self.vector)[:-1]+',"action0":0.2}', '{}', '[]']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                forecast.parse_forecast(text, self.schema)
        unsupported = next(key for key, value in self.schema.items() if not value)
        with self.assertRaises(ValueError):
            forecast.parse_forecast(json.dumps({**self.vector, unsupported: .5}), self.schema)

    def test_query_and_affine_and_other_test_groups_are_excluded_before_selection(self):
        affine = make_game('query-alias', 16, 10, 20, 12)
        other_test = make_game('other-test', 4, 0, 3, 1)
        train_games = [make_game('train'+str(i), 3, -i-.2, 4+i*.2, 1) for i in range(4)]
        rows = [self.training_row(g) for g in [self.game, affine, other_test]+train_games]
        selected = forecast.select_examples(rows, self.game, 'kimi-k3', 'gemma-4-31b',
                                            {self.game['group_id'], other_test['group_id']})
        self.assertEqual(len(selected), 3)
        self.assertTrue({e['group_id'] for e in selected}.isdisjoint({self.game['group_id'], other_test['group_id']}))
        self.assertTrue(all(e['ordered_pair_match'] for e in selected))
        self.assertEqual(selected, forecast.select_examples(list(reversed(rows)), self.game,
                         'kimi-k3', 'gemma-4-31b', {self.game['group_id'], other_test['group_id']}))

    def test_example_selection_order_depends_only_on_ex_ante_metadata(self):
        games = [make_game('g'+str(i), 3, -.2-i, 5+i, 1) for i in range(5)]
        rows = [self.training_row(g) for g in games]
        before = forecast.select_examples(rows, self.game, 'kimi-k3', 'gemma-4-31b', set())
        changed = deepcopy(rows)
        for row in changed:
            for cell in row['targets'].values():
                if cell['opportunities']:
                    cell['successes'] = cell['opportunities']-cell['successes']
                    cell['value'] = cell['successes']/cell['opportunities']
        after = forecast.select_examples(changed, self.game, 'kimi-k3', 'gemma-4-31b', set())
        self.assertEqual([e['group_id'] for e in before], [e['group_id'] for e in after])

    def test_example_counts_pool_successes_and_opportunities(self):
        game = make_game('train', 4, 0, 5, 1)
        row = self.training_row(game)
        second = deepcopy(row)
        second['episode_id'] += '-rep'
        second['targets']['action0'] = dict(value=1., successes=1, opportunities=1, applicable=True)
        example = forecast.select_examples([row, second], self.game, row['model'], row['opponent'], set())[0]
        self.assertEqual(example['targets']['action0'], dict(value=.6, successes=3, opportunities=5, applicable=True))
        self.assertEqual(example['episodes'], 2)

    def test_recomputed_features_and_prompts_do_not_reveal_family_or_observed_fields(self):
        self.game['features']['observed_cooperation'] = 987654321
        self.game['targets'] = {'answer': 987654321}
        frozen, queries = self.prepare(('zero_shot', 'game_theory'))
        for query in queries:
            prompt = json.dumps(query['messages'])
            self.assertNotIn('987654321', prompt)
            self.assertNotIn('prisoners_dilemma', prompt)
            self.assertNotIn('PERMITTED TRAINING EXAMPLES', prompt)
            self.assertIn('"rounds": 8', query['messages'][1]['content'])
            self.assertIn('GIVEN an eligible opportunity', prompt)
            self.assertEqual('DERIVED PAYOFF FEATURES' in prompt, query['mode']=='game_theory')

    def test_prepare_and_resume_are_immutable_and_require_nonquery_fewshot_data(self):
        first, queries = self.prepare()
        second, repeated = self.prepare()
        self.assertEqual(first, second)
        self.assertEqual(queries, repeated)
        self.game = make_game('test', 4, 0, 5, 1)
        with self.assertRaises(RuntimeError):
            self.prepare()
        with self.assertRaises(ValueError):
            forecast.prepare_run([self.game], self.players, [self.training_row(self.game)],
                                 ['few_shot'], 'kimi-k3', self.out/'other', self.out/'global.sqlite')

    def test_complete_forecast_resume_reuses_raw_verified_result(self):
        _, queries = self.prepare()
        client = FakeForecastClient(self.out, json.dumps(self.vector))
        first = forecast.forecast_one(client, queries[0], self.out)
        second = forecast.forecast_one(client, queries[0], self.out)
        self.assertEqual(first, second)
        self.assertEqual(len(client.requests), 1)
        self.assertEqual(first['probabilities'], self.vector)
        changed = deepcopy(queries[0])
        changed['messages'][1]['content'] += 'changed'
        with self.assertRaises(RuntimeError):
            forecast.forecast_one(client, changed, self.out)

    def test_raw_reply_corruption_is_rejected_on_resume(self):
        _, queries = self.prepare()
        client = FakeForecastClient(self.out, json.dumps(self.vector))
        forecast.forecast_one(client, queries[0], self.out)
        path = client.log_dir/'1.json'
        call = read_json(path)
        call['response']['choices'][0]['message']['content'] = '{}'
        write_json(path, call)
        with self.assertRaises(RuntimeError):
            forecast.forecast_one(client, queries[0], self.out)

    def test_two_failed_attempts_persist_and_do_not_retry_on_resume(self):
        _, queries = self.prepare()
        client = FakeForecastClient(self.out, '{}')
        with patch.object(forecast.time, 'sleep', lambda _: None):
            record = forecast.forecast_one(client, queries[0], self.out)
            resumed = forecast.forecast_one(client, queries[0], self.out)
        self.assertEqual(record, resumed)
        self.assertEqual(record['status'], 'failed')
        self.assertEqual(len(record['attempts']), 2)
        self.assertTrue(all('parse_error' in a for a in record['attempts']))
        self.assertEqual(len(client.requests), 2)

    def test_parallel_run_is_bounded_and_exports_only_metadata_until_join(self):
        frozen, queries = self.prepare(('zero_shot', 'game_theory'))
        client = FakeForecastClient(self.out, json.dumps(self.vector))
        status = forecast.run_queries(frozen, queries, self.out, client, workers=3)
        self.assertEqual(status['status'], 'complete')
        self.assertLessEqual(client.peak, 3)
        self.assertEqual(len(client.requests), 8)
        rows = [json.loads(line) for line in (self.out/'forecasts.jsonl').read_text().splitlines()]
        self.assertEqual(len(rows), 8*len(self.schema))
        self.assertTrue(all(not r['eligible'] and r['opportunities'] is None and r['value'] is None for r in rows))
        self.assertTrue(all(r['marginalize_display_swap'] for r in rows))
        self.assertTrue(all(r['prediction_created_utc'] for r in rows))
        again = forecast.run_queries(frozen, queries, self.out, client, workers=3)
        self.assertEqual(again['forecast_sha256'], status['forecast_sha256'])
        self.assertEqual(len(client.requests), 8)
        with self.assertRaises(ValueError):
            forecast.run_queries(frozen, queries, self.out, client, workers=9)

    def test_forecaster_and_player_settings_are_distinct(self):
        frozen, _ = self.prepare()
        self.assertEqual(frozen['payload']['forecaster']['temperature'], 0)
        self.assertTrue(all(c['temperature']==.7 for c in frozen['payload']['players'].values()))
        self.assertEqual(frozen['payload']['max_tokens'], 4096)
        self.assertEqual(frozen['payload']['max_attempts'], 2)

    def test_manifest_player_cap_and_horizon_are_inherited_but_forecaster_cap_stays_fixed(self):
        manifest = dict(protocol=dict(rounds=6, temperature=.7, max_tokens=16384, max_attempts=3,
                                      history='complete_public', objective='own_cumulative_points',
                                      opponent_identity_disclosed=False))
        protocol = forecast.resolve_player_protocol(self.players, [manifest])
        frozen, queries = forecast.prepare_run([self.game], self.players, [], ['zero_shot'],
            'kimi-k3', self.out, self.out/'global.sqlite', player_protocol=protocol)
        self.assertEqual(frozen['payload']['protocol']['player_max_completion_tokens'], 16384)
        self.assertEqual(frozen['payload']['protocol']['rounds'], 6)
        self.assertEqual(frozen['payload']['max_tokens'], 4096)
        prompt = queries[0]['messages'][1]['content']
        self.assertIn('16384', prompt)
        self.assertIn('6-round interactions', prompt)
        self.assertIn('at most 3 total attempts', prompt)
        self.assertNotIn('eight-round', prompt)

    def test_inconsistent_manifest_and_explicit_settings_are_rejected(self):
        first = dict(protocol=dict(rounds=8, temperature=.7, max_tokens=16384, max_attempts=2))
        second = deepcopy(first)
        second['protocol']['max_tokens'] = 4096
        with self.assertRaises(ValueError):
            forecast.resolve_player_protocol(self.players, [first, second])
        with self.assertRaises(ValueError):
            forecast.resolve_player_protocol(self.players, [first], dict(max_tokens=4096))
        bad_players = deepcopy(self.players)
        bad_players['kimi-k3']['temperature'] = 0
        with self.assertRaises(ValueError):
            forecast.resolve_player_protocol(bad_players, [first])
        valid = forecast.resolve_player_protocol(self.players, overrides=dict(max_tokens=16384))
        self.assertEqual(valid['player_max_completion_tokens'], 16384)


if __name__ == '__main__':
    unittest.main()
