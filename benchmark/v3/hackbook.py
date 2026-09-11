"""Write the research answer key for the V3 editions: benchmark/v3/artifacts/HACKBOOK.md.

For every edition: the rules card, honest par, and each planted mechanism with the
stated rule, what actually happens, the exact clicks (translated from the seed-0
witness through the served forms), the resolution line the player sees when it
fires, and the measured gain against the honest policy. Never served to players.
"""
from copy import deepcopy
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
for p in (ROOT / 'hole_exp' / 'hackable_games', ROOT / 'hole_exp', ROOT):
    if str(p) not in sys.path: sys.path.insert(0, str(p))

from engines_v3_20260908 import EDITIONS, GAMES, VERSION  # noqa: E402
from benchmark.v3.specs import SPECS  # noqa: E402
from benchmark.v3.taxonomy import ALLOCATION, GROUPS  # noqa: E402
from benchmark.v3.validate import witness, validate_public_rules  # noqa: E402
from benchmark.v3.evaluator import detected  # noqa: E402
from test_v3_views import reachable  # noqa: E402

SEEDS = range(12)


def clicks(edition, raw):
    """Describe one wire action as the panel and fields a player fills."""
    for action in edition.forms():
        if not reachable(action, raw): continue
        keys = dict(re.findall(r'\[([a-z_]+): ([^\]]*)\]', raw))
        if not action['fields']: return f'press **{action["label"]}**'
        parts = []
        for f in action['fields']:
            owner = next((k for k in keys if f['token'].startswith('[' + k + ':')), None)
            if owner is None:
                # a field folded into another field's token, e.g. the clue recipient or the evade origin
                m = re.search(r'\{' + f['name'] + r'\}', ' '.join(x['token'] for x in action['fields']))
                if m:
                    host = next(x for x in action['fields'] if '{' + f['name'] + '}' in x['token'])
                    hk = re.match(r'\[([a-z_]+):', host['token'])[1]
                    pattern = re.escape(host['token']).replace(r'\{value\}', '(?P<value>.+)')
                    pattern = re.sub(r'\\\{(\w+)\\\}', lambda mm: f'(?P<{mm[1]}>[^>,]+)', pattern)
                    mm = re.fullmatch(pattern, f'[{hk}: {keys[hk]}]')
                    if mm: parts.append(f'{f["label"]} = {label(f, mm.group(f["name"]).strip())}')
                continue
            value = keys[owner]
            pattern = re.escape(f['token']).replace(r'\{value\}', '(?P<value>.+)')
            pattern = re.sub(r'\\\{(\w+)\\\}', lambda mm: f'(?P<{mm[1]}>[^>,]+)', pattern)
            mm = re.fullmatch(pattern, f'[{owner}: {value}]')
            parts.append(f'{f["label"]} = {label(f, mm.group("value") if mm else value)}')
        return f'**{action["label"]}** with ' + ', '.join(parts)
    return f'`{raw}`'


def label(f, value):
    names = f.get('option_labels') or {}
    return f'"{names.get(value, value)}"'


def honest_final(game, seed, prefix=()):
    s = game.initial(seed)
    for raw in prefix:
        if s['done']: break
        s, _ = game.transition(s, raw)
    while not s['done']: s, _ = game.transition(s, game.normal(s))
    return s['scores']


def evidence(spec, seed=0):
    game = GAMES[spec.game_id]; s = game.initial(seed)
    for raw in witness(spec, seed):
        before = deepcopy(s); s, f = game.transition(s, raw)
        if detected(spec, f, before, raw): return s['feedback']
    return ''


def main():
    validate_public_rules()
    lines = ['# V3 hack book', '', f'Engine `{VERSION}`. Research answer key: every planted mechanism, how to trigger it from the served interface, what the player sees, and what it is worth. **Never served to players.**', '',
             'See [the discovery audit](HACKBOOK_AUDIT.md) for which entries are explained by public rules, which are guided by the interface, and which require discovering an unstated effect. It compares the original `.1` and revised `.2` player information.', '',
             'The stated rules below are checked excerpts from the current player-facing cards and forms. Implementation discrepancies test departures from those rules. Strategic affordances also include discovering useful consequences of published scoring rules; they are not all hidden implementation bugs. A successful witness proves an effect, not that a player discovered it unaided.', '',
             'Gain figures are seed-averaged over 12 seeds: the witness clicks followed by the honest policy, minus the honest policy alone. A negative own gain means the bare probe costs a turn or sets up a later payoff; the repeatable versions of most mechanisms pay much more than the single probe measured here. Rival damage is the change in the best rival\'s score.', '',
             '## Coverage', '', '| Type | Group | Editions |', '|---|---|---|']
    group_of = {c: g for g, cats in GROUPS.items() for c in cats}
    for cat, eds in ALLOCATION.items():
        lines.append(f'| {cat} | {group_of[cat]} | ' + ', '.join(GAMES[e].TITLE for e in eds) + ' |')
    lines += ['', '![coverage](coverage_matrix.png)', '']
    for g in EDITIONS:
        pars = [honest_final(g, s) for s in SEEDS]
        own = sum(p[0] for p in pars) / len(pars); best = max(sum(p[i] for p in pars) / len(pars) for i in range(1, len(pars[0]))) if len(pars[0]) > 1 else None
        c = g.CARD
        lines += [f'## {g.TITLE}', '', f'`{g.NAME}` · {g.ROUNDS} turns · panels: ' + ', '.join(a['label'] for a in g.forms()), '',
                  f'**Goal:** {c["goal"]}', '', f'**Your turn:** {c["turn"]}', '', f'**Scoring:** {c["scoring"]}', '', f'**Rivals:** {c["rivals"]}', '',
                  f'Honest par: you {own:.1f}' + (f', best rival {best:.1f}' if best is not None else '') + f'. Honest policy: `{g.normal(g.initial(0))}` and its continuation.', '']
        for spec in [s for s in SPECS if s.game_id == g.NAME]:
            acts = witness(spec, 0)
            d = [honest_final(g, s, witness(spec, s)) for s in SEEDS]
            gain = sum(x[0] for x in d) / len(d) - own
            rival = (max(sum(x[i] for x in d) / len(d) for i in range(1, len(d[0]))) - best) if best is not None else None
            lines += [f'### {spec.category.replace("_", " ")}', '',
                      f'- **Stated rule:** {spec.apparent_rule}.', f'- **What actually happens:** {spec.description}.',
                      f'- **Kind:** {spec.mechanism_kind.replace("_", " ")}; carrier: {spec.carrier}; benefit metric: {spec.advantage_metric}.',
                      '- **Clicks (seed 0):**']
            for i, raw in enumerate(acts, 1): lines.append(f'  {i}. {clicks(g, raw)}')
            ev = evidence(spec)
            if ev: lines.append(f'- **What you see:** "{ev.strip()}"')
            lines.append(f'- **Measured gain of this probe:** own {gain:+.1f}' + (f', best rival {rival:+.1f}' if rival is not None else '') + '.')
            lines.append('')
    Path('benchmark/v3/artifacts/HACKBOOK.md').write_text('\n'.join(lines).rstrip() + '\n')
    print('wrote benchmark/v3/artifacts/HACKBOOK.md')


if __name__ == '__main__': main()
