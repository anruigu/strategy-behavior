"""Parse only the public hand/mark projection printed in the observation."""
import json
import re
from . import benchmark


def view(phase, prompt):
    v = benchmark.view('ref_hanabi', phase, prompt)
    match = re.search(r'^Table: (.+)$', prompt, re.M)
    if not v or not match:
        return None
    table = json.loads(match[1])
    v.update(kind='hanabi_human', table=table, title='Mini Hanabi', state='')
    actions = []
    if table['own']:
        play = benchmark.action('Play a card', benchmark.choice(
            'play', 'Your card slot', [str(c['slot']) for c in table['own']]))
        play['help'] = 'Choose a slot in your hand. Use the clue marks to decide what to play.'
        actions.append(play)
    targets = [str(p['player']) for p in table['others'] if p['cards']]
    if targets and table['tokens']:
        clue = benchmark.action('Give a clue',
            benchmark.field('target', 'Recipient', '', options=targets),
            benchmark.field('clue', 'Colour or rank clue', '[clue: player {target}, {value}]', text=True))
        clue['help'] = 'Give one colour or one rank, not a full card like R2. The teammate plays their leftmost matching card immediately.'
        clue['fields'][1]['quick_options'] = ['R', 'B', '1', '2', '3']
        actions.append(clue)
    review = benchmark.action('Review clue marks', token='[review: 0]')
    review['help'] = 'Uses this turn to request a record of your clue marks.'
    actions.append(review)
    v['actions'] = actions
    return v
