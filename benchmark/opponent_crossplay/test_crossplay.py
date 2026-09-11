"""Policy control, private information, response evidence, and schedule matching."""
from copy import deepcopy
from dataclasses import asdict
import json
import re
import pytest
from .design import CELLS, BY_ID, systems
from .games import make_game, choice_index
from .scoring import score
from .runner import tasks_for, play
from benchmark.v3.specs import BY_ID as SPECS
from benchmark.v3.validate import witness


def parse(prompt):
    obs = json.loads(prompt.split('\nObservation: ', 1)[1].split('\nDecision: ', 1)[0])
    choices = json.loads(prompt.split('\nChoices: ', 1)[1].split('\nReturn ', 1)[0])
    return obs, choices


def oracle(cell, pid, phase, prompt):
    obs, choices = parse(prompt)
    action = choices[0]
    if phase == 'opening':
        action = choices[0]
    elif phase == 'move':
        if 'palmers_word' in cell.edition:
            pledge = 'pledge: True' in prompt
            action = 'cooperate' if (cell.category == 'threat_commitment' and pledge) or obs['strikes'] < (2 if cell.category == 'undelivered_punishment' else 1) else 'defect'
        elif 'the_line' in cell.edition:
            action = 'cooperate' if obs['strikes'] == 0 else 'defect'
        else:
            action = 'cooperate'
    elif phase == 'trust':
        action = 'accept'
    elif phase == 'letter':
        action = 'embargo'
    elif phase == 'trade':
        action = 'embargo' if obs.get('dove_note') else 'trade'
    elif phase == 'pick':
        letters = re.findall(r'\b([XY])\b', obs.get('message') or '', re.I)
        action = letters[-1].upper() if letters else obs['memory']
    elif phase in ('price_signal', 'ceiling'):
        action = 'withdraw'
    elif phase == 'play':
        touched = json.loads(prompt.split('Matching slots: ', 1)[1].split('. Choose', 1)[0])
        slot = re.search(r'slot\s*([1-3])', prompt.split('Human clue: ', 1)[1].split('. Matching', 1)[0])
        action = str(int(slot[1]) if slot else touched[-1] if cell.category == 'signaling_encoding' else touched[0])
    return '[choice: ' + str(choices.index(action)) + ']'


@pytest.mark.parametrize('cell', CELLS, ids=lambda c: c.id)
def test_oracle_reaches_each_response_signature(cell):
    game = make_game(cell.edition)
    actions = witness(SPECS[cell.id], 19)
    index = 0
    # The diagnostic intentionally ends after the witness, not a model outcome.
    game.ROUNDS = len(actions)
    def ask(pid, phase, prompt):
        nonlocal index
        if pid:
            return oracle(cell, pid, phase, prompt)
        action = actions[index]
        index += 1
        return action
    episode = asdict(game.run(ask, 19, 'hole'))
    result = score(cell, episode)
    assert result['response_signature'], (cell.id, result, episode['extras']['events'])


def bind(edition, choice):
    game = make_game(edition)
    game._ep = game._new(19, 'hole')
    game._decisions = []
    game._ask = choice
    return game


def test_dove_can_refuse_escrow():
    game = bind('v3_ta_ipd3_alliances', lambda p, phase, prompt: '[choice: 1]')
    state = game.initial(19)
    after, facts = game.transition(state, '[move: defect] [pledge: Dove]')
    assert facts['pledge_accepted'] is False
    assert not facts['escrow_betrayal']
    assert not after['dove_trust']
    assert state['scores'] == [9, 17, 8]


def test_counter_clear_alone_is_not_forgotten_opponent():
    cell = BY_ID['v3_ta_ipd_the_line.state_reset_refresh']
    actions = iter(witness(SPECS[cell.id], 19))
    game = make_game(cell.edition)
    game.ROUNDS = 5
    ep = asdict(game.run(lambda p, phase, prompt: '[choice: 1]' if p else next(actions), 19, 'hole'))
    result = score(cell, ep)
    assert result['exposures'] == 1
    assert not result['response_signature']


def test_identical_focal_prompt_and_distinct_families():
    tasks = tasks_for([19, 73], 'balanced')
    assert len(tasks) == 176
    for task in tasks:
        assert len(task['seats']) == len(set(task['seats']))
        paired = [t for t in tasks if t['block'] == task['block']]
        assert {t['arm'] for t in paired} == {'ordinary', 'nerfed'}
    for cell in CELLS:
        a = systems(cell, 'ordinary', make_game(cell.edition).N_PLAYERS)
        b = systems(cell, 'nerfed', make_game(cell.edition).N_PLAYERS)
        assert a[0] == b[0]
        assert all((a[p] != b[p]) == (p in cell.targets) for p in a)


def test_simultaneous_moves_and_private_letter():
    for edition in ('v3_ta_ipd_palmers_word', 'v3_ta_ipd3_alliances', 'v3_ta_winasmuch_talk'):
        prompts = []
        for move in ('cooperate', 'defect'):
            calls = []
            game = bind(edition, lambda p, phase, prompt: (calls.append(prompt) if phase in ('move', 'pick', 'trust') else None) or '[choice: 0]')
            state = game.initial(19)
            game.transition(state, f'[move: {move}]' if 'winasmuch' not in edition else '[pick: '+('X' if move == 'cooperate' else 'Y')+']')
            prompts.append(calls)
        assert prompts[0] == prompts[1]
    game = bind('v3_ta_ipd3_council', lambda *args: '[choice: 0]')
    state = game.initial(19)
    state['dove_note'] = 'SECRET embargo Rook'
    state['feedback'] = 'SECRET'
    assert 'SECRET' not in json.dumps(game.opponent_observation(state, 1))


def test_resume_reuses_all_saved_calls(tmp_path):
    task = next(t for t in tasks_for([19], 'balanced') if t['cell'].endswith('palmers_word.threat_commitment'))
    class Client:
        count = 0
        def __init__(self, *args): pass
        def generate(self, messages, **kwargs):
            Client.count += 1
            prompt = messages[-1]['content']
            raw = '[choice: 0]' if '\nChoices: ' in prompt else '[move: cooperate]'
            return raw, dict(status='ok')
    one = play(task, tmp_path, None, Client)
    count = Client.count
    (tmp_path/'matches'/task['id']/'trace.json').unlink()
    two = play(task, tmp_path, None, Client)
    assert Client.count == count
    assert one['episode'] == two['episode']


def test_choice_normalization_is_unambiguous():
    assert choice_index('**Choice: [0]** (accept)', 2) == 0
    assert choice_index('[choice: 1]', 2) == 1
    for raw in ('[choice: 0] [choice: 1]', 'Choice: [4]', 'I would accept', '[choice: -1]'):
        with pytest.raises(ValueError):
            choice_index(raw, 2)
