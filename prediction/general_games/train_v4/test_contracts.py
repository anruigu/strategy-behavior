import copy
from prediction.io_utils import read_json
from . import DATA, STUDY
from .catalog import TRAIN, HOLDOUT, VALIDATION
from .dataset import observable, render_input, source_hashes
from .labels import episode_row
from .runtime import messages


def test_frozen_disjoint_balanced_design():
    train = read_json(STUDY / 'training/plan.json')['episodes']; test = read_json(STUDY / 'test/plan.json')['episodes']
    assert len(train) == 3456 and len(test) == 544 and sum(e['small'] for e in train) == 864
    assert not set(TRAIN) & set(HOLDOUT) and set(VALIDATION) <= set(TRAIN)
    for fid in TRAIN:
        rows = [e for e in train if e['game']['family_id'] == fid]
        assert len(rows) == 192 and sum(e['small'] for e in rows) == 48
        assert len({e['seed'] for e in rows}) in (24, 48)
    trained_configs = {e['game']['configuration_id'] for e in train}
    assert not trained_configs & {e['game']['configuration_id'] for e in test if e['suite'] == 'configuration'}
    assert not {e['seed'] for e in train} & {e['seed'] for e in test}
    assert read_json(DATA / 'manifest.json')['source_hashes'] == source_hashes()


def test_actor_format_cue_in_every_prediction_input():
    for q in read_json(DATA / 'test-queries.json'):
        assert 'Action-format reminder:' in q['inputs']['opening_messages'][0]['content']
        assert 'Draws are not strict wins.' in q['input_text']
        assert 'opening_state' not in q and 'targets' not in q and 'seed' not in q['inputs']
        assert q['inputs']['opening_messages'][0]['content'] in q['input_text'].replace('\\n', '\n') or 'Action-format reminder:' in q['input_text']


def test_native_draw_and_solution_labels_keep_v4_prompt():
    fixtures = read_json(DATA / 'fixtures.evaluator.json'); games = {g['configuration_id']: g for g in read_json(DATA / 'catalog.json')['configurations']}
    for fid in ('stag_hunt', 'sokoban', 'ultimatum', 'blackjack'):
        fixture = next(f for f in fixtures if games[f['configuration_id']]['family_id'] == fid); trace = copy.deepcopy(fixture['trace']); g = games[fixture['configuration_id']]
        trace['item'] = dict(game=g, seed=fixture['seed'], seat=0, model='glm', condition='normal', replicate=0, small=True,
            episode_id='scripted-test-only', opening_group='scripted-test-only', suite='test')
        for step in trace['steps']:
            step['is_focal'] = step['actor'] == 0
            if step['is_focal']: step['messages'] = messages(g, trace['opening_observations']['0'])
        row, _ = episode_row(trace)
        assert row['inputs']['opening_messages'] == messages(g, trace['opening_observations']['0'])
        assert all(0 <= v <= 1 for v in row['targets'].values())
        if fid == 'stag_hunt': assert row['targets']['win'] == 0 and row['targets']['native_score'] == .5
        if fid == 'sokoban': assert row['targets']['win'] == 1 and row['targets']['native_score'] == 1
