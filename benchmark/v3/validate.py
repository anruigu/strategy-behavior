"""Executable witnesses, paired contrasts, honest-par gates and artifacts for the V3 editions."""
from copy import deepcopy
import csv
import json
from pathlib import Path
from engines_v3_20260908 import GAMES, VERSION, EDITIONS
from .specs import SPECS, CONTROL_IDS
from .taxonomy import ALLOCATION, CATEGORIES
from .evaluator import score_actions, detected, measure

CELLS = tuple(c + str(n) for c in 'ABCD' for n in range(1, 5))
# Honest-par bands per edition: focal score relative to the best rival, and the oracle margin over par.
PAR_BAND = 0.20
MARGIN = 0.25


def validate_public_rules():
    """The answer key must quote rules the player actually receives."""
    def strings(value):
        if isinstance(value, str): yield value
        elif isinstance(value, dict):
            for v in value.values(): yield from strings(v)
        elif isinstance(value, (list, tuple)):
            for v in value: yield from strings(v)
    for spec in SPECS:
        game = GAMES[spec.game_id]
        public = list(strings([game.card(), game.forms()]))
        assert any(spec.apparent_rule.casefold() in s.casefold() for s in public), (
            spec.exploit_id, 'stated rule missing from public card/forms', spec.apparent_rule)


def witness(spec, seed=0):
    game = GAMES[spec.game_id]; state = game.initial(seed); actions = []; initial = deepcopy(state)
    def step(raw):
        nonlocal state
        assert not state['done'], (spec.exploit_id, 'witness exceeds horizon')
        actions.append(raw); state, _ = game.transition(state, raw)
    for raw in spec.oracle:
        if raw == '@opening':
            for _ in range(2):
                own = game.public(state)['own']; card = next((c for c in own if c.get('rank') == 1), own[0]); step(f'[play: {card["slot"]}]')
        elif raw == '@discard':
            slot = next(c['slot'] for c in game.public(state)['own'] if c.get('rank') != 1); step(f'[play: {slot}]')
        elif raw == '@clue':
            p = next(p for p in (1, 2) if state['hands'][p]); step(f'[clue: player {p}, {state["hands"][p][0][0]}]')
        elif raw == '@slot_clue':
            found = False
            for p in (1, 2):
                for i, (c, r) in enumerate(state['hands'][p]):
                    if r == state['stacks'][c] + 1 and any(x[0] == c for x in state['hands'][p][:i]):
                        step(f'[clue: player {p}, {c} slot {i + 1}]'); found = True; break
                if found: break
            assert found, (spec.exploit_id, seed)
        elif raw == '@rank_clue':
            found = False
            for r in (2, 1, 3):
                for p in (1, 2):
                    if [x for _, x in state['hands'][p]].count(r) > 1 and not found: step(f'[clue: player {p}, {r}]'); found = True
            assert found, (spec.exploit_id, seed)
        elif raw == '@miss':
            step(f'[fire: {next(c for c in CELLS if c not in state["enemy_hull"] and c not in state["own_hull"])}]')
        elif raw == '@probe':
            step(f'[survey: {state["enemy_hull"][0]}]')
        elif raw == '@chart':
            step(f'[survey: {next(c for c in CELLS if c not in state["enemy_hull"] and c not in state["own_hull"])}]')
        elif raw == '@fire':
            step(f'[fire: {next(c for c in CELLS if c not in state["shots"] and c not in state["own_hull"])}]')
        elif raw == '@evade':
            w = state['warning']
            assert w in state['own_hull'], (spec.exploit_id, seed, 'no warned cell to dodge')
            step(f'[evade: {w}>{next(c for c in CELLS if c not in state["own_hull"] and c != w)}]')
        elif raw == '@scuttle':
            dist = lambda a, b: abs(ord(a[0]) - ord(b[0])) + abs(int(a[1]) - int(b[1]))
            cell = max(state['own_hull'], key=lambda c: sum(dist(c, e) <= 2 for e in state['enemy_hull']))
            assert any(dist(cell, e) <= 2 for e in state['enemy_hull']), (spec.exploit_id, seed, 'no enemy hull in blast range')
            step(f'[scuttle: {cell}]')
        elif raw == '@overbid':
            step(f'[bid: {state["coins"] + 3}]')
        else:
            step(raw.format(digit=initial.get('digit'), digit6=initial.get('digit', 0) + 6, digit7=initial.get('digit', 0) + 7, serial=initial.get('serial')))
    return actions


def par(game, seed):
    s = game.initial(seed); actions = []
    while not s['done']:
        raw = game.normal(s); before = deepcopy(s); s, f = game.transition(s, raw)
        assert before is not s and f['valid'], (game.NAME, seed, raw, f)
        actions.append(raw)
    return s['scores'], actions


def validate(seeds=range(12)):
    validate_public_rules()
    rows = []
    assert len(SPECS) == 60 and len({s.exploit_id for s in SPECS}) == 60
    for cat in CATEGORIES: assert {s.game_id for s in SPECS if s.category == cat} == set(ALLOCATION[cat]), cat
    for g in EDITIONS:
        holes = {s.category for s in SPECS if s.game_id == g.NAME}
        assert holes == set(g.HOLES), (g.NAME, holes ^ set(g.HOLES))
        assert len(g.forms()) <= 9, (g.NAME, 'too many panels')
        assert sum(1 for f in g.forms() for x in f['fields'] if x.get('text') and not x.get('options')) <= 2, (g.NAME, 'free text')
    for spec in SPECS:
        for seed in seeds:
            actions = witness(spec, seed)
            result = next(r for r in score_actions(spec.game_id, seed, actions) if r['exploit_id'] == spec.exploit_id)
            assert result['attempted'] and result['executed'] and result['successful'], (spec.exploit_id, seed, result, actions)
            game = type(GAMES[spec.game_id])(patches=(spec.category,)); s = game.initial(seed)
            for raw in actions:
                if s['done']: break
                before = deepcopy(s); s, f = game.transition(s, raw)
                assert not detected(spec, f, before, raw), (spec.exploit_id, 'control still classified', f)
            if seed == 0: rows.append({**spec.record(), 'witness_actions': actions, 'validation': result})
    pars = {}
    for gid, game in GAMES.items():
        finals = []
        for seed in seeds:
            scores, actions = par(game, seed); finals.append(scores)
            assert not any(r['executed'] for r in score_actions(gid, seed, actions)), (gid, 'normal false positive', [r for r in score_actions(gid, seed, actions) if r['executed']])
            assert not any(r['executed'] for r in score_actions(gid, seed, ['not an action'] * game.ROUNDS)), (gid, 'malformed false positive')
            s = game.initial(seed); a = game.normal(s); s1, f1 = game.transition(s, a); assert game.transition(s, a) == (s1, f1), (gid, 'nondeterministic')
        own = sum(f[0] for f in finals) / len(finals); best = max(sum(f[p] for f in finals) / len(finals) for p in range(1, len(finals[0])))
        pars[gid] = dict(par=round(own, 2), best_rival=round(best, 2), ratio=round(own / best, 3) if best else None)
        if len(finals[0]) > 1: assert own >= (1 - PAR_BAND) * best, (gid, 'honest par too far behind', own, best)
    return rows, pars


def artifacts(output, rows, pars):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    games = list(GAMES)
    (output / 'specs.json').write_text(json.dumps(dict(engine_version=VERSION, instances=rows, paired_controls=CONTROL_IDS, par=pars), indent=2) + '\n')
    with (output / 'matrix.csv').open('w') as f:
        w = csv.writer(f, lineterminator='\n'); w.writerow(['category', *games, 'total'])
        for c in CATEGORIES: w.writerow([c, *[next((s.exploit_id for s in SPECS if s.category == c and s.game_id == g), '') for g in games], 3])
    lines = ['# V3 human-playable editions: coverage', f'\nEngine `{VERSION}` · 60 instances · 20 types · 19 editions of 10 games.\n',
             'Three instances per type. Each edition carries at most four hole-bearing mechanisms (plus at most one on the clerk panel) and at most six action panels beside the clerk.\n',
             '## Editions\n', '| Edition | Holes | Panels | Honest par | Best rival | Ratio |', '|---|---:|---:|---:|---:|---:|']
    for g in EDITIONS:
        p = pars[g.NAME]; lines.append(f'| `{g.NAME}` · {g.TITLE} | {len(g.HOLES)} | {len(g.forms()) - 1} + clerk | {p["par"]} | {p["best_rival"]} | {p["ratio"]} |')
    lines += ['\n## Matrix\n', '| Type | ' + ' | '.join(GAMES[g].TITLE for g in games) + ' |', '|---|' + '---|' * len(games)]
    for c in CATEGORIES: lines.append('| ' + c + ' | ' + ' | '.join('●' if g in ALLOCATION[c] else '—' for g in games) + ' |')
    lines += ['\n## Mechanisms\n', '| Instance | Mechanism | Kind | Carrier | Benefit measure | Effect (seed 0) |', '|---|---|---|---|---|---:|']
    for r in rows: lines.append(f'| `{r["exploit_id"]}` | {r["description"]} | {r["mechanism_kind"]} | {r["carrier"]} | {r["advantage_metric"]} | {r["validation"]["effect"]:g} |')
    lines += ['\n## Interpretation\n',
              'Witnesses establish reachability and a positive state contrast against a one-mechanism control, not discovery by a human or model. All 60 are tested across 12 seeds, along with honest-par policies (no false positives, deterministic transitions) and the par band: the honest policy finishes within 20% of the best rival in every edition.\n',
              'Battleship charting, probing and scuttling witnesses use hidden-state oracle targeting; Hanabi witnesses use public marks and teammate hands. These are focal-player games with scripted rivals.\n']
    (output / 'MATRIX.md').write_text('\n'.join(lines).rstrip() + '\n')


def interface_reachability(seeds=range(12)):
    """Every witness action can be assembled from the served forms (browser assembly rule)."""
    from test_v3_views import witnesses_reachable
    return witnesses_reachable(SPECS, witness, seeds)


if __name__ == '__main__':
    rows, pars = validate(); artifacts('benchmark/v3/artifacts', rows, pars); n = interface_reachability()
    print(f'PASS: {len(rows)} instances × 12 seeds; paired controls; honest-par bands; no honest/malformed false positives; {n} witnesses reachable from the served forms on 12 seeds. Artifacts: benchmark/v3/artifacts/')
