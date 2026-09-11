"""CPU-only integration audits. The already-tested frozen trace verifier is mocked."""
from copy import deepcopy
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from prediction.games import make_game, payoff
from prediction.prospective import build_rows
from prediction.improve.data import metadata_examples, file_hash
from prediction.improve.integrate import collect, prompted, read
from prediction.improve.prospective_design import make_manifest
from prediction.improve.test_prospective_design import primary_fixture, write

TMP = '/shared/allie/home/.codex/tmp'
FREEZE = '2026-09-10T12:00:00+00:00'


def fixture(root):
    primary = primary_fixture()
    project = Path(__file__).resolve().parents[2]
    primary['sources'] = {p: file_hash(project/p) for p in
        ('prediction/runner.py', 'prediction/games.py', 'prediction/measurements.py')}
    games = [make_game('synthetic-pd', 3, 0, 5, 1), make_game('synthetic-stag', 4, 0, 3, 2)]
    manifest = make_manifest(primary, games, '2026-09-10T11:00:00+00:00')
    metadata = build_rows(manifest)
    queries = metadata_examples(metadata, manifest['protocol'])
    scope = dict(scope_id='full', train_example_indices=[], train_row_ids=[], train_group_ids=[],
                 query_example_indices=list(range(len(queries))), query_row_ids=[q['row_id'] for q in queries],
                 query_group_ids=sorted({q['group_id'] for q in queries}))
    planned = {root/'fresh-prospective/manifest.json': manifest,
               root/'fresh-prospective/metadata.json': metadata,
               root/'prospective-design/queries.json': queries,
               root/'prospective-design/scopes.json': [scope],
               root/'prospective-design/expansion.json': []}
    for path, value in planned.items(): write(path, value)
    write(root/'data/data.json', dict(train_examples=[], development_examples=[]))
    source = root/'synthetic-source.json'; write(source, {})
    audit = dict(artifact_sha256={str(p): file_hash(p) for p in planned},
                 contract=dict(implementation_sha256={}, primary_manifest_path=str(source),
                               primary_manifest_sha256=file_hash(source), observed_sources=[]))
    write(root/'prospective-design/audit.json', audit)
    write(root/'fresh-prospective/forecast-freeze.json', dict(status='forecasts_frozen_before_fresh_rollouts',
        created_utc=FREEZE, coverage={'ready': True}, artifact_sha256={},
        design_audit_sha256=file_hash(root/'prospective-design/audit.json')))
    write(root/'fresh-prospective/status.json', dict(status='finished_with_errors', completed=4,
                                                   errors=[{'error': 'synthetic incomplete episodes'}]))
    selected = [s for s in manifest['episodes'] if s['game_id'] == games[0]['id'] and s['models'] in (['a','a'], ['a','b'])]
    for spec in selected:
        path = root/'fresh-prospective/episodes'/spec['id']
        rounds = []
        for number in range(1, 9):
            actions = [0, 1] if number % 2 else [1, 0]
            decisions = []
            for role in (0, 1):
                call_id = f"{spec['id']}-r{number}-p{role}"
                name = f'round-{number:02}-player-{role}.json'
                decisions.append(name)
                write(path/name, dict(attempts=[dict(meta={'call_id': call_id})]))
                write(root/'fresh-prospective/calls'/spec['models'][role]/(call_id+'.json'),
                      dict(call_id=call_id, timestamp='2026-09-10T12:01:00+00:00'))
            rounds.append(dict(round=number, actions=actions, payoffs=list(payoff(games[0], *actions)), decisions=decisions))
        trace = dict(id=spec['id'], game=games[0], models=spec['models'], trial_id=spec['trial_id'],
                     representation=spec['representation'], swap=spec['swap'], status='complete', rounds=rounds,
                     started='2026-09-10T12:00:30+00:00', finished='2026-09-10T12:02:00+00:00')
        write(path/'trace.json', trace)
    return manifest, queries, selected


def mocked_collect(root):
    # Importing integrate never reads outcome files. Only this explicit call does.
    with patch('prediction.runner.verify_trace', side_effect=lambda path, manifest: read(path)):
        collect(root)


class IntegrationTests(unittest.TestCase):
    def test_collection_retains_roles_missing_contexts_counts_and_game_weights(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root = Path(folder); manifest, queries, selected = fixture(root)
            mocked_collect(root)
            audit = read(root/'fresh-collected/audit.json')
            rows = read(root/'fresh-collected/records.json')
            examples = read(root/'fresh-collected/data.json')['development_examples']
            self.assertEqual(len(rows), 8)
            self.assertEqual(audit['distinct_episode_roles'], 8)
            self.assertEqual(audit['complete_episodes'], 4)
            self.assertEqual(audit['selected_successful_calls'], 64)
            self.assertEqual(audit['all_recorded_calls'], 64)
            self.assertEqual(len(examples), len(queries))
            self.assertEqual([e['row_id'] for e in examples], [q['row_id'] for q in queries])
            self.assertEqual(audit['observed_label_episodes'], {'False': 2, 'True': 2})
            self.assertEqual(audit['complete_canonical_groups'], 0)
            self.assertEqual(audit['collection_status'], 'complete_with_missing_episodes')
            observed = [e for e in examples if e['mask'][0]]
            self.assertEqual(len(observed), 3)
            own = next(e for e in observed if e['model'] == e['opponent'])
            self.assertEqual(own['opportunities'][0], 32)
            self.assertEqual(len(own['source_row_indices']), 4)
            self.assertEqual(len(own['episode_ids']), 2)
            self.assertEqual(own['y'][0], .5)
            self.assertAlmostEqual(sum(e['weights'][0] for e in observed), 1.)
            for row in examples:
                if not row['mask'][0]:
                    self.assertEqual(row['successes'], [None]*3)
                    self.assertEqual(row['opportunities'], [0]*3)
                    self.assertEqual(row['y'], [None]*3)
            before = file_hash(root/'fresh-collected/audit.json')
            mocked_collect(root)
            self.assertEqual(before, file_hash(root/'fresh-collected/audit.json'))

    def test_rejects_trace_copied_into_different_planned_episode(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root = Path(folder); _, _, selected = fixture(root)
            first = root/'fresh-prospective/episodes'/selected[0]['id']/'trace.json'
            other = root/'fresh-prospective/episodes'/selected[1]['id']/'trace.json'
            write(other, read(first))
            with self.assertRaisesRegex(ValueError, 'identity'):
                mocked_collect(root)
            self.assertFalse((root/'fresh-collected').exists())

    def test_rejects_wrong_swap_and_reused_successful_call(self):
        for mode in ('swap', 'call'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(dir=TMP) as folder:
                root = Path(folder); _, _, selected = fixture(root)
                path = root/'fresh-prospective/episodes'/selected[0]['id']
                trace = read(path/'trace.json')
                if mode == 'swap':
                    trace['swap'] = not trace['swap']; write(path/'trace.json', trace)
                else:
                    # Self-play roles use the same model folder, enabling a real duplicate call reference.
                    selected_self = next(s for s in selected if s['models'] == ['a','a'])
                    path = root/'fresh-prospective/episodes'/selected_self['id']
                    write(path/'round-01-player-1.json', read(path/'round-01-player-0.json'))
                with self.assertRaisesRegex(ValueError, 'metadata|reused'):
                    mocked_collect(root)

    def test_all_calls_including_unused_failures_must_follow_freeze(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root = Path(folder); fixture(root)
            write(root/'fresh-prospective/calls/a/unused-failed.json', dict(call_id='unused-failed',
                  timestamp='2026-09-10T11:59:00+00:00', status='error'))
            with self.assertRaisesRegex(ValueError, 'predates'):
                mocked_collect(root)

    def test_rejects_trace_before_freeze_and_call_after_trace_finish(self):
        for mode in ('trace', 'call'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(dir=TMP) as folder:
                root = Path(folder); _, _, selected = fixture(root)
                path = root/'fresh-prospective/episodes'/selected[0]['id']/'trace.json'
                if mode == 'trace':
                    trace = read(path); trace['started'] = '2026-09-10T11:00:00+00:00'; write(path, trace)
                else:
                    spec = selected[0]; call_id = f"{spec['id']}-r1-p0"
                    write(root/'fresh-prospective/calls'/spec['models'][0]/(call_id+'.json'),
                          dict(call_id=call_id, timestamp='2026-09-10T12:03:00+00:00'))
                with self.assertRaisesRegex(ValueError, 'chronology|postdates'):
                    mocked_collect(root)

    def test_requires_terminal_runner_valid_freeze_and_immutable_design(self):
        for mode in ('running', 'freeze', 'design'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(dir=TMP) as folder:
                root = Path(folder); fixture(root)
                if mode == 'running':
                    write(root/'fresh-prospective/status.json', {'status': 'running'})
                elif mode == 'freeze':
                    path = root/'fresh-prospective/forecast-freeze.json'
                    freeze = read(path); freeze['design_audit_sha256'] = 'changed'; write(path, freeze)
                else:
                    path = root/'fresh-prospective/metadata.json'
                    rows = read(path); rows[0]['model'] = 'altered'; write(path, rows)
                with self.assertRaises(ValueError):
                    mocked_collect(root)
                self.assertFalse((root/'fresh-collected').exists())

    def prompt_fixture(self, root):
        _, queries, _ = fixture(root)
        examples = queries[:2]
        rows = []
        for example in examples:
            for target in ('action0', 'cooperation', 'coordination'):
                applicable = target == 'action0' or example['applicability'][target]
                rows.append(dict(game_id=example['game_id'], group_id=example['group_id'], model=example['model'],
                    opponent=example['opponent'], family=example['family'], representation=example['representation'],
                    method='llm_few_shot', target=target, prediction=.4 if applicable else None,
                    structurally_applicable=applicable, prediction_created_utc=FREEZE, value=None,
                    successes=None, opportunities=None))
        return examples, rows

    def write_prompts(self, path, rows):
        path.write_text(''.join(json.dumps(r)+'\n' for r in rows))

    def test_prompted_join_preserves_probabilities_timing_and_explicit_missing(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root = Path(folder); examples, rows = self.prompt_fixture(root)
            source, out = root/'forecasts.jsonl', root/'joined.jsonl'
            rows[0]['prediction'] = None; rows[0]['prediction_created_utc'] = None
            rows.pop(); self.write_prompts(source, rows)
            joined = prompted(source, examples, out, 'fresh_full', 'full')
            self.assertIsNone(joined[0]['prediction'])
            self.assertEqual(joined[1]['source_prediction_created_utc'], FREEZE)
            audit = read(out.with_suffix('.manifest.json'))
            self.assertEqual(len(audit['missing_row_targets']), 1)
            self.assertEqual(joined, prompted(source, examples, out, 'fresh_full', 'full'))
            rows[1]['prediction'] = .6; self.write_prompts(source, rows)
            with self.assertRaisesRegex(ValueError, 'Immutable'):
                prompted(source, examples, out, 'fresh_full', 'full')

    def test_prompted_join_rejects_duplicate_examples_and_metadata_errors(self):
        for mode in ('example', 'row', 'group', 'representation', 'probability', 'outcome', 'timestamp'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(dir=TMP) as folder:
                root = Path(folder); examples, rows = self.prompt_fixture(root)
                if mode == 'example': examples.append(dict(examples[0], representation='text', row_id='new-id'))
                elif mode == 'row': rows.append(deepcopy(rows[0]))
                elif mode == 'group': rows[0]['group_id'] = 'incorrect'
                elif mode == 'representation': rows[0]['representation'] = 'text'
                elif mode == 'probability': rows[0]['prediction'] = True
                elif mode == 'outcome': rows[0]['successes'] = 1
                else: rows[0]['prediction_created_utc'] = '2026-09-10T12:00:00'
                source = root/'forecasts.jsonl'; self.write_prompts(source, rows)
                with self.assertRaises(ValueError): prompted(source, examples, root/'out.jsonl', 'fresh_full', 'full')
                self.assertFalse((root/'out.jsonl').exists())


if __name__ == '__main__': unittest.main()
