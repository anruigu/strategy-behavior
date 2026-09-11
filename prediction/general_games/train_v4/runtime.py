"""Versioned format cue; unchanged native engines and observed-information bots."""
from prediction.general_games.native import messages as native_messages
from prediction.general_games.scaleup_v2 import runtime as v2
from prediction.general_games.breadth_v3 import runtime as v3
from prediction.general_games.scaleup_v2.catalog import FAMILIES as V2
from prediction.io_utils import read_json

Session = v3.Session


def view(session, actor, history):
    return (v2 if session.game['family_id'] in V2 else v3).view(session, actor, history)


def action(visible, seed, step):
    return (v2 if visible['family_id'] in V2 else v3).action(visible, seed, step)


def messages(game, history, condition='normal'):
    result = native_messages(game, history, condition)
    result[0]['content'] += (' Action-format reminder: during an action phase, use the native syntax, including square brackets where shown. '
        'Illustrative syntax: ' + game['structured']['action_format'] + '. Substitute legal values and all fields required by the current game. '
        'During a conversation phase, a short plain-language message is allowed.')
    return result


def replay(item, record, raw_dir=None):
    s = Session(item['game'], item['seed'])
    assert s.snapshot() == record['opening_state'] and s.opening == {int(k): v for k, v in record['opening_observations'].items()}
    for i, step in enumerate(record['steps']):
        actor, incoming, h = s.observe()
        assert [actor, incoming, view(s, actor, h), s.snapshot()] == [step['actor'], step['incoming'], step['visible_state'], step['before']]
        if step['is_focal']:
            expected = messages(item['game'], h, item['condition']); assert expected == step['messages']
            if raw_dir:
                call = read_json(raw_dir / (step['call']['call_id'] + '.json'))
                assert call['status'] == 'ok' and call['request']['messages'] == expected
                assert call['response']['choices'][0]['message']['content'] == step['raw_action']
        else:
            assert action(step['visible_state'], item['seed'], i) == step['raw_action']
        assert s.step(step['raw_action']) == step['result'] and s.snapshot() == step['after']
    if record['status'] == 'complete': assert s.env.state.done and s.snapshot() == record['final_state']
    return s

