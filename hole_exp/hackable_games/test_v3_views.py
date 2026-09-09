"""V3 editions: public-only honest policies, hidden-state invariance, rules-card surface, form reachability."""
from copy import deepcopy
import json
import re
from pathlib import Path
import catalog
import views


def normal_from_public(v):
    """A legal honest move chosen from the served view alone (no engine state)."""
    s = v['public_state']; card = v['card']['edition']; rnd = v['round']
    if 'digit' in s: return f'[redeem: {s["serial"]}]' if not s['redeemed'] else f'[report: {s["digit"]}]'
    if 'stock' in s: return '[catch: 3]'
    if 'piles' in s:
        own = [c for c in s['own'] if c.get('rank') == 1]
        if own: return f'[play: {own[0]["slot"]}]'
        if s['tokens']:
            for p in s['others']:
                if p['cards']: return f'[clue: player {p["player"]}, {p["cards"][0]["colour"]}]'
        return '[play: 1]' if s['own'] else '[clerk: review]' if card == 'clues' else '[clerk: appeal]'
    if 'strikes' in s:
        if not s['connected']: return '[reconnect: 1]'
        if v.get('notice') and 'proposes' in v['notice']: return '[vote: approve]'
        return '[move: cooperate]'
    if 'workshop' in s:
        if card == 'workshops':
            if s['boards'] and s['offer_open']: return '[accept: 1]'
            if not s['workshop'] and s['coins'] >= 3: return '[build: 1]'
            return '[work: 1]'
        if rnd >= 7 and s['boards'] and not s['shipment']: return '[reserve: 1]'
        if s['boards'] and rnd < 7: return '[sell: 1]'
        return '[work: 1]'
    if 'memory' in s:
        if not s['present']: return '[join: 1]'
        if s.get('slot_open'): return '[reserve: 1]'
        return '[pick: Y]'
    if 'dove_trust' in s: return '[move: cooperate] [pledge: Dove]' if card == 'alliances' else ('[move: cooperate] [proxy: 1]' if rnd == 1 else '[move: cooperate]')
    if 'lots' in s:
        if s['lot'] == 1 and s['coins'] >= 7: return '[bid: 7]'
        if s['lot'] == 2 and s['coins'] >= 8: return f'[bid: {min(s["coins"], 10)}]'
        return '[bid: 0]' if s['lot'] < 3 else '[wait: 1]'
    if 'titles' in s: return '[pay_rent: 1]' if s['rent_due'] else ('[lease: 1]' if card == 'neighbours' and '1' in s['titles'] and s['rent_pending'] is None else '[build: 1]' if card == 'development' and '1' in s['titles'] and s['height'] < 2 and s['coins'] >= 1 else '[wait: 1]')
    if 'own_hull' in s: return '[fire: ' + next(c + str(n) for c in 'ABCD' for n in range(1, 5) if c + str(n) not in s['shots'] and c + str(n) not in s['own_hull'] and c + str(n) not in s['charts']) + ']'
    raise AssertionError('Unknown public board')


def submit(action, values):
    """Assemble the wire text exactly as the browser does: action token plus each filled field token."""
    tokens = [action['token']] if action['token'] else []
    for f in action['fields']:
        if values.get(f['name']) and f['token']:
            tokens.append(f['token'].format(**{**values, 'value': values[f['name']]}))
    return ' '.join(tokens)


def research_specs():
    """The research package is not part of the public deployment's sparse checkout; use it when present."""
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    if (root / 'benchmark' / 'v3' / 'specs.py').exists() and str(root) not in sys.path: sys.path.insert(0, str(root))
    try:
        from benchmark.v3.specs import SPECS
        from benchmark.v3.validate import witness
        return SPECS, witness
    except ImportError:
        return None, None


def discovery_surface():
    """Hidden effects emerge from action results, not advance help or examples."""
    cases = (
        ('v3_ref_commons_neighbours', r'three seasons|closes rival landings|each rival (?:loses|lost)',
         '[dump: 1]', 'closure_set', 'closed for three seasons'),
        ('v3_ref_commons_neighbours', r'each rival (?:loses|lost)',
         '[tow: 1]', 'rival_tow_loss', 'each rival lost 6 fish'),
        ('v3_ta_winasmuch_reserve', r'removes up to|each rival (?:loses|lost)',
         '[burn: 1]', 'rival_reserve_removed', 'each rival lost'),
        ('v3_ref_battleship_blockade', r'blast|within two steps',
         '[scuttle: A1]', 'scuttle_cost', 'blast'),
        ('v3_ta_ipd_the_line', r're-record.{0,25}defect',
         None, None, None),
    )
    for gid, spoilers, raw, fact, feedback in cases:
        game = catalog.GAMES[gid]['game']; state = game.initial(0)
        initial = views.build(gid, 'move', game.observe(state))
        assert not re.search(spoilers, json.dumps(initial), re.I), (gid, 'advance spoiler')
        if raw:
            assert any(reachable(a, raw) for a in initial['actions']), (gid, 'action hidden')
            after, facts = game.transition(state, raw)
            assert facts['valid'] and facts[fact] > 0, (gid, facts)
            observed = views.build(gid, 'move', game.observe(after))
            assert feedback in observed['feedback'], (gid, 'result hidden')
    game = catalog.GAMES['v3_ta_winasmuch_talk']['game']
    example = next(a['example'] for a in game.forms() if a['label'] == 'Post message')
    _, facts = game.transition(game.initial(0), '[say: ' + example + ']')
    assert not facts['extra_signal_followed'], 'The message example triggers the hidden behavior'

    # Check both checked-in guides: a stale generated page can reintroduce spoilers.
    from build_v3_guide import render
    page, markdown = render(); here = Path(__file__).resolve().parent
    assert (here / 'play/guide-v3.html').read_text() == page, 'Rebuild the public V3 guide'
    md = here.parents[1] / 'docs/v3-player-guide.md'
    if md.exists(): assert md.read_text() == markdown, 'Rebuild the Markdown V3 guide'


def gate():
    discovery_surface()
    SPECS, witness = research_specs()
    tells = re.compile(r'\b(hole|exploit|loophole|cheat|hack|bug|flaw|vulnerab)', re.I)
    for gid in catalog.V3_IDS.values():
        g = catalog.GAMES[gid]['game']; s = g.initial(0); kinds = set()
        while not s['done']:
            v = views.build(gid, 'move', g.observe(s)); assert v and v['kind'] == 'v3_move', gid
            assert v['public_state'] == {k: x for k, x in g.public(s).items() if k != 'notice'}, gid
            assert v['card']['goal'] and v['card']['seats'] and len(g.rules.split()) <= 160, (gid, len(g.rules.split()))
            assert not tells.search(json.dumps(v)), (gid, 'tell in served view')
            assert v['actions'] and all(a['token'] or a['fields'] for a in v['actions']) and v['actions'][-1]['label'] == 'Ask the clerk', gid
            assert len(v['actions']) <= 9, (gid, 'panel count')
            raw = normal_from_public(v); s, f = g.transition(s, raw); assert f['valid'], (gid, raw, f, s['feedback'])
        # Hidden state must not change the served view.
        s = g.initial(0); hidden = deepcopy(s)
        for key, alt in (('enemy_hull', ['D4', 'D3', 'C4', 'B4', 'A4']), ('rival_bids', [[9, 9]] * 3), ('enemy_orders', None), ('tie_break', 'X')):
            if key in hidden and alt is not None: hidden[key] = alt
        if 'hands' in hidden: hidden['hands'][0] = [['R', 3]] * len(hidden['hands'][0])
        assert views.build(gid, 'move', g.observe(s)) == views.build(gid, 'move', g.observe(hidden)), gid
    # Every witness action is producible from the served forms with the browser's assembly rule.
    if SPECS is None:
        print(f'  ok   V3: {len(catalog.V3_IDS)} editions, public-only honest episodes, hidden-state invariance, no tells (research witnesses not in this checkout)')
        return 0
    from benchmark.v3.validate import validate_public_rules
    validate_public_rules()
    n = witnesses_reachable(SPECS, witness)
    print(f'  ok   V3: {len(catalog.V3_IDS)} editions, public-only honest episodes, hidden-state invariance, no advance spoilers, current guides/rule excerpts, {n} witnesses reachable from forms')
    return 0


def witnesses_reachable(SPECS, witness, seeds=(0,)):
    for spec in SPECS:
        for seed in seeds:
            g = catalog.GAMES[spec.game_id]['game']; s = g.initial(seed)
            for raw in witness(spec, seed):
                v = views.build(spec.game_id, 'move', g.observe(s)); assert v, spec.exploit_id
                assert any(reachable(a, raw) for a in v['actions']), (spec.exploit_id, seed, raw, [a['label'] for a in v['actions']])
                s, _ = g.transition(s, raw)
    return len(SPECS)


def reachable(action, raw):
    """Can some filling of this form produce `raw`? Fields are matched by their token shape and options."""
    keys = re.findall(r'\[([a-z_]+): ([^\]]*)\]', raw)
    if action['token'] and not action['fields']: return raw == action['token']
    if action['token'] and action['fields']: return False
    named = {f['name']: f for f in action['fields']}
    wanted = {}
    for key, value in keys:
        owners = [x for x in action['fields'] if x['token'].startswith('[' + key + ':')]
        if not owners: return False
        f = owners[0]
        pattern = re.escape(f['token']).replace(r'\{value\}', '(?P<value>.+)')
        pattern = re.sub(r'\\\{(\w+)\\\}', lambda m: f'(?P<{m[1]}>[^>,]+)', pattern)
        m = re.fullmatch(pattern, f'[{key}: {value}]')
        if not m: return False
        wanted[f['name']] = m.group('value')
        for k2, v2 in m.groupdict().items():
            if k2 != 'value': wanted[k2] = v2.strip()
    for name, f in named.items():
        if name not in wanted:
            if not f['optional']: return False
            continue
        if f['options'] is not None and wanted[name] not in f['options']: return False
        if f['options'] is None and not f['text'] and not re.fullmatch(r'-?\d+', wanted[name]): return False
    return True


if __name__ == '__main__': gate()
