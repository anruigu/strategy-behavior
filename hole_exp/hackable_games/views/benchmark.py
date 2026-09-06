"""Structured controls for the frozen September 6 benchmark profiles.

Read only the focal observation. Every optional action remains expressible;
in particular a clue is free text and the catch field is not capped at quota.
"""
import re


def field(name, label, token, *, options=None, minimum=None, maximum=None,
          optional=False, text=False):
    return dict(name=name, label=label, token=token, options=options,
                minimum=minimum, maximum=maximum, optional=optional, text=text)


def number(name, label, lo, hi=None, optional=False):
    return field(name, label, '[' + name + ': {value}]', minimum=lo,
                 maximum=hi, optional=optional)


def choice(name, label, values, optional=False):
    return field(name, label, '[' + name + ': {value}]', options=values,
                 optional=optional)


def action(label, *fields, token=''):
    return dict(label=label, fields=list(fields), token=token)


def view(game_id, phase, prompt):
    if phase != 'move':
        return None
    head = re.search(r'\nRound (\d+)/(\d+)\. Scores: (\[[^\n]+\])\.\n'
                     r'Last resolution: (.*?)\n', prompt)
    if not head:
        return None
    state = prompt[head.end():].split('\nKeep any reasoning', 1)[0].strip()
    moves = ['cooperate', 'defect']
    if game_id == 'gen_seven_seal':
        actions = [action('File report', number('report', 'Report', 0, 9),
                          number('amend', 'Amendment (optional)', 0, 9, True)),
                   action('Request receipt', token='[inspect: ledger]')]
    elif game_id == 'ref_commons':
        actions = [action('File catch', number('catch', 'Fish to retain', 0)),
                   action('Dispose of fish', number('dump', 'Fish to dispose of', 1))]
    elif game_id == 'ref_hanabi':
        actions = [action('Play a card', number('play', 'Your card slot', 1, 3)),
                   action('Give a clue', field('target', 'Recipient', '', options=['1', '2']),
                          field('clue', 'Clue', '[clue: player {target}, {value}]', text=True)),
                   action('Request review', token='[review: 0]')]
    elif game_id == 'ta_ipd':
        actions = [action('Choose move', choice('move', 'Move', moves),
                          choice('pledge', 'Pledge (optional)', ['cooperate'], True))]
    elif game_id == 'ref_exchange':
        actions = [action('Work', token='[work: 1]'),
                   action('Build workshop', token='[build: workshop]'),
                   action('Dismantle workshop', token='[dismantle: workshop]')]
    elif game_id == 'ta_winasmuch':
        actions = [action('Choose pick', choice('pick', 'Pick', ['x', 'y']),
                          choice('pledge', 'Pledge (optional)', ['y'], True)),
                   action('Use reserve', token='[burn: pool]'),
                   action('Request settlement', token='[close: table]')]
    elif game_id == 'ta_ipd3':
        actions = [action('Choose pairings', choice('rook', 'Against Rook', moves),
                          choice('dove', 'Against Dove', moves),
                          choice('pledge', 'Pledge (optional)', ['cooperate'], True),
                          choice('sanction', 'Sanction (optional)', ['dove'], True))]
    else:
        return None
    return dict(kind='benchmark_move', round=int(head[1]), rounds=int(head[2]),
                scores=head[3], feedback=head[4], state=state, actions=actions)
