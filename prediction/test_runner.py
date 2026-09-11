"""Offline contract tests. Run with python -B -m unittest prediction.test_runner.

No constructor loads credentials, no test accesses the network, and temporary
artifacts are restricted to the user-approved durable temporary directory.
"""
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import threading
import types
import unittest
from unittest.mock import patch

from prediction import runner
from prediction.client import Client, ModelConfig, Ledger, BudgetExceeded
from prediction.io_utils import read_json, write_json


TEMP_ROOT = Path('/shared/allie/home/.codex/tmp')


def fixture_payoff(game, first, second):
    p = game['payoffs']
    return ((p['R'], p['R']), (p['S'], p['T']),
            (p['T'], p['S']), (p['P'], p['P']))[2 * first + second]


def fixture_render(game, representation='matrix', swap=False):
    labels = ['B', 'A'] if swap else ['A', 'B']
    return '\n'.join(f'you {labels[a]}, other {labels[b]}: '
                     f'your points {fixture_payoff(game, a, b)[0]:g}, '
                     f'other points {fixture_payoff(game, a, b)[1]:g}'
                     for a in range(2) for b in range(2))


def config(name='fake', provider='openrouter'):
    return ModelConfig(name, provider, 'offline/' + name, 'https://invalid.example',
                       'UNUSED_OFFLINE_KEY', .7, None, 'low')


def response(content='A', finish='stop', cost=.01, choices=True):
    raw = dict(model='offline/fake', choices=[dict(message=dict(content=content),
               finish_reason=finish)] if choices else [], usage={} if cost is None else dict(cost=cost))
    return types.SimpleNamespace(
        choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=content, refusal=None),
                 finish_reason=finish)] if choices else [],
        model='offline/fake', model_dump=lambda **kwargs: deepcopy(raw))


class Transport:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.requests = []
        self.api_key = 'offline-secret-for-redaction-test'
        self.chat = types.SimpleNamespace(completions=types.SimpleNamespace(create=self.create))

    def create(self, **kwargs):
        self.requests.append(deepcopy(kwargs))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class RecordingClient:
    def __init__(self, cfg, out, replies, barrier=None):
        self.config, self.out, self.replies = cfg, out, iter(replies)
        self.messages, self.barrier = [], barrier

    def generate(self, messages):
        self.messages.append(deepcopy(messages))
        if self.barrier:
            self.barrier.wait(timeout=5)
        reply = next(self.replies)
        ident = f'{self.config.model_id}-{len(self.messages)}'
        raw = dict(model=self.config.provider_model,
                   choices=[dict(message=dict(content=reply, refusal=None), finish_reason='stop')],
                   usage=dict(cost=0))
        write_json(self.out / 'calls' / self.config.model_id / (ident + '.json'),
                   dict(call_id=ident, status='ok', config=asdict(self.config),
                        request=dict(messages=deepcopy(messages), model=self.config.provider_model,
                                     temperature=.7, max_tokens=128,
                                     extra_body={'reasoning': {'effort': 'low'},
                                                 'provider': {'max_price': {'prompt': 20, 'completion': 120, 'request': 0}}}), response=raw))
        return reply, dict(call_id=ident, status='ok', finish_reason='stop', actual_model=self.config.provider_model)


class OfflineCase(unittest.TestCase):
    def setUp(self):
        TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix='prediction-audit-', dir=TEMP_ROOT)
        self.addCleanup(self.temporary.cleanup)
        self.out = Path(self.temporary.name)


class RunnerTests(OfflineCase):
    def setUp(self):
        super().setUp()
        module = types.ModuleType('prediction.games')
        module.payoff, module.render_game = fixture_payoff, fixture_render
        self.module_patch = patch.dict('sys.modules', {'prediction.games': module})
        self.module_patch.start()
        self.addCleanup(self.module_patch.stop)
        self.sleep_patch = patch.object(runner.time, 'sleep', lambda _: None)
        self.sleep_patch.start()
        self.addCleanup(self.sleep_patch.stop)
        self.game = dict(id='g', group_id='shape', family='pd', payoffs=dict(R=3, S=-2, T=7, P=1))
        self.spec = dict(id='episode', game_id='g', models=['left', 'right'], trial_id=2,
                         representation='matrix', swap=False)
        self.manifest = dict(protocol=dict(rounds=2, max_attempts=2, max_tokens=128),
                             models={n: asdict(config(n)) for n in ['left', 'right']}, sources={},
                             games=[self.game], episodes=[self.spec])

    def run_episode(self, left=('A', 'B'), right=('B', 'A'), simultaneous=False):
        barrier = threading.Barrier(2) if simultaneous else None
        self.clients = {n: RecordingClient(config(n), self.out, values, barrier)
                        for n, values in [('left', left), ('right', right)]}
        with ThreadPoolExecutor(max_workers=2) as pool:
            return runner.episode(self.spec, self.game, self.manifest, self.out, self.clients, pool)

    @property
    def trace_path(self):
        return self.out / 'episodes' / 'episode' / 'trace.json'

    def test_parser_exact_labels_only(self):
        for value, action in [('A', 0), ('B', 1), (' \nA\t', 0)]:
            self.assertEqual(runner.parse_action(value), action)
        for value in ['a', 'AB', 'A.', '"A"', '{"action":"A"}', 'Choose A', '```A```', '', 'Ａ']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                runner.parse_action(value)

    def test_simultaneous_history_and_player_payoff_orientation(self):
        trace = self.run_episode(simultaneous=True)
        self.assertEqual(trace['rounds'][0]['actions'], [0, 1])
        self.assertEqual(trace['rounds'][0]['payoffs'], [-2, 7])
        left = self.clients['left'].messages
        right = self.clients['right'].messages
        self.assertEqual(left[0], right[0])
        self.assertIn('No rounds have been played.', left[0][1]['content'])
        self.assertIn('you A, other B; your points -2, other points 7.', left[1][1]['content'])
        self.assertIn('you B, other A; your points 7, other points -2.', right[1][1]['content'])
        for messages in [left[1], right[1]]:
            self.assertNotIn('Round 2:', messages[1]['content'])
            self.assertNotIn('left', messages[1]['content'])
            self.assertNotIn('right', messages[1]['content'])
        self.assertEqual(runner.verify_trace(self.trace_path, self.manifest), trace)

    def test_swap_maps_display_to_canonical_actions_and_history(self):
        self.spec['swap'] = True
        trace = self.run_episode()
        self.assertEqual(trace['rounds'][0]['actions'], [1, 0])
        self.assertEqual(trace['rounds'][0]['payoffs'], [7, -2])
        self.assertIn('you A, other B; your points 7, other points -2.',
                      self.clients['left'].messages[1][1]['content'])
        runner.verify_trace(self.trace_path, self.manifest)

    def test_complete_decision_context_change_is_rejected_without_calls(self):
        client = RecordingClient(config('left'), self.out, ['A'])
        path = self.out / 'decision.json'
        messages = [dict(role='user', content='original')]
        runner.decision(client, messages, path, 'identity')
        for changed, identity in [([dict(role='user', content='changed')], 'identity'), (messages, 'changed')]:
            with self.subTest(identity=identity), self.assertRaises(RuntimeError):
                runner.decision(client, changed, path, identity)
        self.assertEqual(len(client.messages), 1)

    def test_partial_run_reconstructs_history_without_repeating_completed_calls(self):
        expected = self.run_episode()
        self.trace_path.unlink()
        with ThreadPoolExecutor(max_workers=2) as pool:
            actual = runner.episode(self.spec, self.game, self.manifest, self.out, self.clients, pool)
        self.assertEqual(actual['rounds'], expected['rounds'])
        self.assertEqual([len(c.messages) for c in self.clients.values()], [2, 2])
        runner.verify_trace(self.trace_path, self.manifest)

    def test_invalid_reply_is_not_default_action_and_retries_are_bounded(self):
        client = RecordingClient(config('left'), self.out, ['A because', 'B'])
        item = runner.decision(client, [], self.out / 'ok.json', 'identity', max_attempts=2)
        self.assertEqual(item['displayed_action'], 1)
        self.assertTrue(item['attempts'][0]['parse_error'])
        client = RecordingClient(config('right'), self.out, ['bad', 'still bad'])
        path = self.out / 'bad.json'
        with self.assertRaises(RuntimeError):
            runner.decision(client, [], path, 'identity', max_attempts=2)
        with self.assertRaises(RuntimeError):
            runner.decision(client, [], path, 'identity', max_attempts=2)
        self.assertEqual(len(client.messages), 2)
        self.assertEqual(len(read_json(path)['attempts']), 2)

    def test_refusal_truncation_and_hard_http_error_are_not_actions(self):
        for status, http_status, expected_calls in [('refusal', None, 2), ('truncated', None, 2),
                                                    ('transport_error', 401, 1)]:
            with self.subTest(status=status):
                mock = types.SimpleNamespace(calls=0)
                def generate(messages):
                    mock.calls += 1
                    return 'A', dict(status=status, http_status=http_status, call_id='fake')
                mock.generate = generate
                with self.assertRaises(RuntimeError):
                    runner.decision(mock, [], self.out / (status + '.json'), 'identity')
                self.assertEqual(mock.calls, expected_calls)

    def test_resume_rejects_mutated_saved_decision_messages(self):
        self.run_episode()
        self.trace_path.unlink()
        path = self.trace_path.parent / 'round-01-player-0.json'
        item = read_json(path)
        item['messages'][1]['content'] += '\nUnrecorded context mutation'
        write_json(path, item)
        with ThreadPoolExecutor(max_workers=2) as pool, self.assertRaises((RuntimeError, AssertionError)):
            runner.episode(self.spec, self.game, self.manifest, self.out, self.clients, pool)

    def test_completed_trace_is_verified_on_resume(self):
        trace = self.run_episode()
        trace['rounds'][0]['payoffs'] = [999, 999]
        write_json(self.trace_path, trace)
        with ThreadPoolExecutor(max_workers=2) as pool, self.assertRaises((RuntimeError, AssertionError)):
            runner.episode(self.spec, self.game, self.manifest, self.out, self.clients, pool)

    def test_trace_metadata_must_match_spec(self):
        trace = self.run_episode()
        for key, value in [('trial_id', 999), ('representation', 'narrative'), ('swap', True)]:
            with self.subTest(key=key):
                corrupt = deepcopy(trace)
                corrupt[key] = value
                write_json(self.trace_path, corrupt)
                with self.assertRaises((RuntimeError, AssertionError)):
                    runner.verify_trace(self.trace_path, self.manifest)

    def test_raw_call_response_and_status_bind_saved_action(self):
        self.run_episode()
        path = self.out / 'calls' / 'left' / 'left-1.json'
        original = read_json(path)
        for kind in ['reply', 'status', 'finish_reason']:
            with self.subTest(kind=kind):
                corrupt = deepcopy(original)
                if kind == 'reply':
                    corrupt['response']['choices'][0]['message']['content'] = 'B'
                elif kind == 'status':
                    corrupt['status'] = 'truncated'
                else:
                    corrupt['response']['choices'][0]['finish_reason'] = 'length'
                write_json(path, corrupt)
                with self.assertRaises((RuntimeError, AssertionError)):
                    runner.verify_trace(self.trace_path, self.manifest)

    def test_raw_sampling_settings_match_frozen_configuration(self):
        self.run_episode()
        path = self.out / 'calls' / 'left' / 'left-1.json'
        original = read_json(path)
        for key in ['temperature', 'reasoning']:
            with self.subTest(key=key):
                corrupt = deepcopy(original)
                if key == 'temperature':
                    corrupt['request']['temperature'] = 0
                else:
                    corrupt['request']['extra_body']['reasoning']['effort'] = 'high'
                write_json(path, corrupt)
                with self.assertRaises((RuntimeError, AssertionError)):
                    runner.verify_trace(self.trace_path, self.manifest)


class ClientBudgetTests(OfflineCase):
    def make_client(self, outcomes, global_ceiling=10, stage_ceiling=10, provider='openrouter'):
        instance = Client.__new__(Client)
        instance.config = config(provider=provider)
        instance.log_dir = self.out / 'calls'
        instance.log_dir.mkdir(exist_ok=True)
        instance.ledger = Ledger(self.out / 'global.sqlite', global_ceiling)
        instance.stage_ledger = Ledger(self.out / 'stage.sqlite', stage_ceiling)
        instance.max_tokens = 128
        instance.semaphore = threading.BoundedSemaphore(1)
        instance.client = Transport(outcomes)
        return instance

    def test_stage_rejection_prevents_request(self):
        client = self.make_client([], stage_ceiling=0)
        with self.assertRaises(BudgetExceeded):
            client.generate([])
        self.assertEqual(client.client.requests, [])
        self.assertEqual(client.ledger.summary()['committed_usd'], 0)

    def test_global_rejection_releases_stage_reservation(self):
        client = self.make_client([], global_ceiling=0)
        with self.assertRaises(BudgetExceeded):
            client.generate([])
        self.assertEqual(client.client.requests, [])
        self.assertEqual(client.stage_ledger.summary()['committed_usd'], 0)

    def test_transport_error_preserves_both_reservations_and_redacts_key(self):
        client = self.make_client([RuntimeError('bad offline-secret-for-redaction-test')])
        content, meta = client.generate([])
        self.assertEqual(content, '')
        self.assertEqual(meta['status'], 'transport_error')
        for ledger in [client.ledger, client.stage_ledger]:
            self.assertGreater(ledger.summary()['committed_usd'], 0)
            self.assertEqual(ledger.summary()['states']['unknown']['calls'], 1)
        record = read_json(client.log_dir / (meta['call_id'] + '.json'))
        self.assertNotIn(client.client.api_key, json.dumps(record))
        self.assertIn('[REDACTED]', record['error_message'])

    def test_success_settles_actual_cost_and_missing_cost_stays_reserved(self):
        client = self.make_client([response(cost=.01), response(cost=None)])
        content, first = client.generate([])
        self.assertEqual((content, first['status']), ('A', 'ok'))
        self.assertAlmostEqual(client.ledger.summary()['committed_usd'], .01)
        _, second = client.generate([])
        self.assertIsNone(second['budget_cost_usd'])
        summary = client.ledger.summary()
        self.assertGreater(summary['committed_usd'], .01)
        self.assertEqual(summary['states']['unknown']['calls'], 1)
        self.assertEqual(summary, client.stage_ledger.summary())

    def test_failed_request_retry_is_individually_recorded_and_reserved(self):
        client = self.make_client([RuntimeError('offline failure'), response()])
        with patch.object(runner.time, 'sleep', lambda _: None):
            item = runner.decision(client, [], self.out / 'decision.json', 'identity')
        self.assertEqual(item['status'], 'complete')
        self.assertEqual(len(list(client.log_dir.glob('*.json'))), 2)
        self.assertEqual(len(item['attempts']), 2)
        summary = client.ledger.summary()
        self.assertEqual(summary['states']['unknown']['calls'], 1)
        self.assertEqual(summary['states']['settled']['calls'], 1)
        self.assertGreater(summary['committed_usd'], summary['reported_usd'])

    def test_malformed_response_is_preserved_as_failed_call(self):
        client = self.make_client([response(choices=False)])
        try:
            content, meta = client.generate([])
        except Exception as exc:
            self.fail(f'Malformed provider response escaped without normalized failure: {type(exc).__name__}')
        self.assertNotEqual(meta['status'], 'ok')
        record = read_json(client.log_dir / (meta['call_id'] + '.json'))
        self.assertIn('response', record)
        self.assertEqual(record['response']['choices'], [])
        self.assertNotEqual(record['status'], 'reserved')

    def test_context_limit_rejects_before_reserving(self):
        client = self.make_client([])
        with self.assertRaises(ValueError):
            client.generate([dict(role='user', content='x' * 40001)])
        self.assertEqual(client.client.requests, [])
        self.assertEqual(client.ledger.summary()['states'], {})

    def test_parallel_reservations_do_not_exceed_ceiling(self):
        ledger = Ledger(self.out / 'parallel.sqlite', 1)
        def reserve(_):
            try:
                return ledger.reserve('fake', .2)
            except BudgetExceeded:
                return None
        with ThreadPoolExecutor(max_workers=10) as pool:
            result = list(pool.map(reserve, range(20)))
        self.assertEqual(sum(value is not None for value in result), 5)
        self.assertLessEqual(ledger.summary()['committed_usd'], 1)


class NumericalContractAudit(unittest.TestCase):
    """Independent synthetic checks of scientific identities, not rollout labels."""
    def test_game_properties_against_exhaustive_best_response_definition(self):
        import itertools
        from prediction.games import make_game, payoff
        for values in itertools.product(range(3), repeat=4):
            game = make_game('grid', *values)
            expected = []
            for a, b in itertools.product((0, 1), repeat=2):
                own, other = payoff(game, a, b)
                if own >= payoff(game, 1-a, b)[0] and other >= payoff(game, a, 1-b)[1]:
                    expected.append([a, b])
            self.assertEqual(game['pure_nash'], expected, values)
            shifted = make_game('affine', *(17 + 2.5*v for v in values))
            swapped = make_game('swap', *values[::-1])
            self.assertEqual(game['group_id'], shifted['group_id'], values)
            self.assertEqual(game['group_id'], swapped['group_id'], values)
            self.assertEqual(game['family'], swapped['family'], values)
            features = game['features']
            if features['has_interior_mixed_equilibrium']:
                q = features['mixed_equilibrium_action0_probability']
                R, S, T, P = values
                self.assertAlmostEqual(q*R+(1-q)*S, q*T+(1-q)*P)

    @staticmethod
    def synthetic_records():
        from prediction.games import generate_games, payoff
        from prediction.measurements import measure_episode
        records = []
        for g, game in enumerate(generate_games(n=14)):
            for p, models in enumerate([['m0', 'm1'], ['m0', 'm2'], ['m1', 'm2']]):
                actions = [((t+g) % 2, (t+p) % 2) for t in range(4)]
                trace = dict(id=f'{g}-{p}', game=game, models=models, trial_id=0,
                             representation='matrix', swap=False, status='complete',
                             rounds=[dict(round=t, actions=list(a), payoffs=list(payoff(game, *a)))
                                     for t, a in enumerate(actions, 1)])
                records.extend(measure_episode(trace))
        return records

    def test_game_family_parameter_splits_purge_shapes_and_all_splits_keep_episodes(self):
        from prediction.modeling import build_folds
        records = self.synthetic_records()
        kinds = ['random_group', 'family', 'interpolation', 'extrapolation', 'pair', 'model']
        for kind in kinds:
            folds = build_folds(records, kind)
            self.assertTrue(folds, kind)
            for fold in folds:
                train = [records[i] for i in fold['train']]
                test = [records[i] for i in fold['test']]
                self.assertFalse({r['episode_id'] for r in train} & {r['episode_id'] for r in test})
                if kind in ['random_group', 'family', 'interpolation', 'extrapolation']:
                    self.assertFalse({r['group_id'] for r in train} & {r['group_id'] for r in test})
                if kind == 'pair':
                    self.assertFalse({r['pair'] for r in train} & {r['pair'] for r in test})
                if kind == 'model':
                    held_out = fold['detail']['held_out_model']
                    self.assertTrue(all(held_out not in [r['model'], r['opponent']] for r in train))

    def test_split_membership_does_not_depend_on_outcomes(self):
        from prediction.modeling import build_folds
        records = self.synthetic_records()
        altered = deepcopy(records)
        for row in altered:
            row['targets'] = {'deliberately': 'not a target'}
        for kind in ['random_group', 'family', 'interpolation', 'extrapolation', 'pair', 'model']:
            self.assertEqual(build_folds(records, kind), build_folds(altered, kind))

    def test_bernoulli_brier_includes_within_episode_variation(self):
        from prediction.analysis import score_rows
        rows = [dict(group_id='g', episode_id='e', prediction=.5, value=.5,
                     successes=5, opportunities=10)]
        metrics = score_rows(rows)
        self.assertEqual(metrics['rate_rmse'], 0)
        self.assertAlmostEqual(metrics['event_brier'], .25)
        self.assertAlmostEqual(metrics['event_log_loss'], -__import__('math').log(.5))
        self.assertEqual(metrics['calibration_ece'], 0)

    def test_equal_game_weighting_survives_unbalanced_episode_counts(self):
        from prediction.analysis import score_rows
        a = dict(group_id='a', episode_id='a', prediction=0, value=1, successes=1, opportunities=1)
        b = dict(group_id='b', episode_id='b', prediction=0, value=0, successes=0, opportunities=100)
        one_each = score_rows([a, b])
        unbalanced = score_rows([a] + [{**b, 'episode_id': f'b{n}'} for n in range(20)])
        self.assertAlmostEqual(one_each['event_brier'], .5)
        for key in ['rate_mae', 'rate_rmse', 'event_brier', 'event_log_loss', 'calibration_ece']:
            self.assertAlmostEqual(one_each[key], unbalanced[key])

    def test_encoder_and_fitted_forecasts_do_not_read_test_labels(self):
        from prediction.modeling import FittedPredictor, ModelSpec
        records = self.synthetic_records()
        model = FittedPredictor(ModelSpec('audit', 'ridge', 'combined', 'both'), 'first_action0').fit(records[:48], tune=False)
        self.assertIsNotNone(model.estimator)
        training_means = model.encoder.mean.copy()
        held_out = deepcopy(records[48:])
        before = model.predict(held_out)
        for row in held_out:
            row.pop('targets')
            row['model'] = 'unseen-model'
        unknown_before = model.predict(held_out)
        for row in held_out:
            row['targets'] = {'not': 'valid'}
        self.assertEqual(unknown_before, model.predict(held_out))
        self.assertTrue((training_means == model.encoder.mean).all())
        self.assertEqual(len(before), len(held_out))
        self.assertTrue(all(0 <= p <= 1 for p in unknown_before))

    def test_derived_feature_ablation_excludes_literal_payoffs(self):
        from prediction.modeling import FeatureEncoder, row_weights
        records = self.synthetic_records()
        encoder = FeatureEncoder('structural').fit(records, row_weights(records))
        keys = set(encoder.feature_keys)
        self.assertFalse(keys & {('features', prefix + key) for prefix in ['raw_', 'normalized_'] for key in 'RSTP'})
        self.assertTrue(keys)

    def test_nash_unsupported_targets_do_not_erase_learned_common_support(self):
        from prediction.modeling import FittedPredictor, ModelSpec, prediction_rows
        from prediction.analysis import summarize_predictions
        records = self.synthetic_records()
        forecasts = []
        for spec in [ModelSpec('marginal', 'marginal'), ModelSpec('nash', 'nash')]:
            predictor = FittedPredictor(spec, 'retaliation').fit(records)
            forecasts.extend(prediction_rows(predictor, records, split='audit'))
        summary = summarize_predictions(forecasts, bootstrap=0)
        self.assertTrue(summary['scores'])
        self.assertEqual(summary['scores'][0]['method'], 'marginal')
        self.assertGreater(summary['scores'][0]['rows'], 0)

    def test_bootstrap_keeps_opposite_focal_rows_together_and_pairs_methods(self):
        from prediction.analysis import bootstrap_intervals, paired_improvement_intervals
        rows = [dict(group_id=f'g{g}', episode_id=f'e{g}', fold='f', row_index=2*g+y,
                     prediction=0., value=float(y), successes=y, opportunities=1)
                for g in range(2) for y in range(2)]
        intervals = bootstrap_intervals(rows, repetitions=50)
        for key in ['rate_mae', 'event_brier']:
            self.assertAlmostEqual(intervals[key]['lower'], .5)
            self.assertAlmostEqual(intervals[key]['upper'], .5)
        comparisons = paired_improvement_intervals(rows, list(reversed(rows)), repetitions=50)
        for interval in comparisons.values():
            self.assertEqual(interval, dict(lower=0., upper=0.))


if __name__ == '__main__':
    unittest.main()
