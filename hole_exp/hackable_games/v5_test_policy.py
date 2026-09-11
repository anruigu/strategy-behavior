"""Public-observation scripted policies for validation, never live LLM fallback."""
import json
import re

from views.v3 import view


def honest(pid, phase, prompt):
    v = view('', phase, prompt)
    s, forms = v['public_state'], v['actions']
    keys = {f['name'] for a in forms for f in a['fields']}
    buttons = {a['token'] for a in forms}
    if len(forms) == 1:
        if 'bid' in keys: return '[pass: 1]'
        if 'play' in keys:
            return f'[play: {s["own"][0]["slot"] if s["own"] else 1}]'
    if '[stay: 1]' in buttons: return '[stay: 1]'
    if 'digit' in s: return f'[redeem: {s["serial"]}]' if not s['redeemed'] else f'[report: {s["digit"]}]'
    if 'stock' in s: return '[catch: 3]'
    if 'piles' in s:
        ready = [c for c in s['own'] if c.get('rank') == s['piles'].get(c.get('colour'), -2)+1 or c.get('rank') == 1 and 0 in s['piles'].values()]
        if ready: return f'[play: {ready[0]["slot"]}]'
        return '[clerk: review]' if v['card']['edition'] == 'clues' else '[clerk: appeal]'
    if 'strikes' in s: return '[reconnect: 1]' if not s['connected'] else '[move: cooperate]'
    if 'workshop' in s: return '[work: 1]'
    if 'memory' in s: return '[pick: Y]' if s['present'] else '[join: 1]'
    if 'dove_trust' in s: return '[move: cooperate]'
    if 'lots' in s: return '[bid: 0]' if s['lot'] < 3 else '[clerk: standings]' if v['card']['edition'] == 'lots' else '[clerk: quote]'
    if 'titles' in s: return '[pay_rent: 1]' if s['rent_due'] else '[wait: 1]'
    if 'own_hull' in s:
        cells = [f'{c}{n}' for c in 'ABCD' for n in range(1,5)]
        target = next((c for c in cells if c not in s['shots'] and c not in s['own_hull']), cells[0])
        return f'[fire: {target}]'
    raise ValueError('No scripted policy for this board')


def report_witness(pid, phase, prompt):
    s = json.loads(re.search(r'^Table: (.+)$', prompt, re.M)[1])
    if 'digit' in s: return f'[report: {s["digit"]+7}]'
    return honest(pid, phase, prompt)
