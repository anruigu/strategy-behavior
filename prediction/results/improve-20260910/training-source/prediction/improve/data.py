"""Portable, label-independent split design and count-preserving data export.

This module prepares data; it does not fit any model or calibration parameter.
Only the standard library and the original pure-Python game definitions are used.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

from prediction.games import make_game

TARGETS = ('action0', 'cooperation', 'coordination')
FAMILIES = ('anti_coordination', 'chicken', 'coordination', 'harmony',
            'prisoners_dilemma', 'stag_hunt', 'weak_dominance')
SCHEMA = 'improve-counts-v1'


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')


def game_of(row):
    game = make_game(row.get('game_id', row.get('id', 'metadata')), **row['payoffs'])
    for field in ('group_id', 'family'):
        if field in row and row[field] != game[field]:
            raise ValueError('Payoff-derived '+field+' differs from metadata')
    return game


def split_coordinate(row):
    """Fixed family-specific coordinate, invariant to positive affine payoffs/action relabeling."""
    game = game_of(row)
    family, values = game['family'], game['payoffs']
    if family in ('coordination', 'anti_coordination'):
        span = max(values.values())-min(values.values())
        name, value = 'offdiagonal_imbalance', abs(values['S']-values['T'])/span
    elif family == 'weak_dominance':
        name, value = 'canonical_s', game['split_metadata']['canonical_s']
    elif family in FAMILIES:
        name, value = 'canonical_t', game['split_metadata']['canonical_t']
    else:
        raise ValueError('Unsupported declared family: '+family)
    if value is None or not math.isfinite(value):
        raise ValueError('Undefined fixed split coordinate for '+family)
    return dict(name=name, value=round(float(value), 12))


def input_text(row, protocol):
    """The only predictor text: no outcomes, game ID, split, taxonomy, or trial/swap."""
    if protocol.get('rounds') != 8:
        raise ValueError('This fixed improvement protocol requires eight rounds')
    p = row['payoffs']
    return (f"Predict behavior before an eight-round simultaneous symmetric two-action game. "
            f"The focal model is {row['model']}; the opponent model is {row['opponent']}. "
            "Each player maximizes its own cumulative points. Both receive the complete public "
            "history of actions and realized payoffs before each later round; current choices are hidden "
            "until both players act. Opponent model identity is hidden from the players. "
            "Each round is a fresh request with full public history; private reasoning is not carried forward. "
            f"Temperature is {protocol.get('temperature')}, completion cap {protocol.get('max_tokens')}, "
            f"and at most {protocol.get('max_attempts')} attempts per decision. "
            "Player-visible labels A/B are balanced across opposite label orientations; forecast the "
            "canonical action coordinates below, averaging over those orientations. "
            f"Canonical payoff matrix (row player's points, column player's points): "
            f"(0,0)=({p['R']},{p['R']}); (0,1)=({p['S']},{p['T']}); "
            f"(1,0)=({p['T']},{p['S']}); (1,1)=({p['P']},{p['P']}). "
            "Predict canonical action0 frequency; mutual cooperation frequency when a unique "
            "welfare-maximizing symmetric action exists; and frequency of strict pure equilibrium "
            "profiles when at least two such profiles exist. Structurally undefined targets are masked.")


def metadata_examples(records, protocol):
    buckets = {}
    for index, row in enumerate(records):
        game = game_of(row)
        for field in ('model', 'opponent'):
            if not isinstance(row.get(field), str) or not row[field]:
                raise ValueError('Missing ordered player identity')
        representation = row.get('representation', 'matrix')
        identity = dict(game_id=game['id'], group_id=game['group_id'], payoffs=game['payoffs'],
                        model=row['model'], opponent=row['opponent'], representation=representation,
                        protocol=protocol)
        key = canonical_hash(identity)
        if key not in buckets:
            buckets[key] = dict(row_id=key, example_id=key, **identity, family=game['family'],
                features=game['features'], applicability=game['applicability'],
                split_coordinate=split_coordinate(game), source_row_indices=[], episode_ids=[])
        bucket = buckets[key]
        bucket['source_row_indices'].append(index)
        if row.get('episode_id') is not None:
            bucket['episode_ids'].append(row['episode_id'])
    result = sorted(buckets.values(), key=lambda r:(r['game_id'],r['model'],r['opponent'],r['representation']))
    for row in result:
        row['episode_ids'] = sorted(set(row['episode_ids']))
        row['input_text'] = input_text(row, protocol)
    return result


def validated_counts(row, target):
    cell = row.get('targets', {}).get(target)
    if cell is None:
        raise ValueError('Training record lacks declared target '+target)
    n, k = cell.get('opportunities'), cell.get('successes')
    if cell.get('applicable') is not True:
        if n not in (0, None) or k not in (0, None) or cell.get('value') is not None:
            raise ValueError('Inapplicable target has observations')
        return 0, 0
    if type(n) is not int or type(k) is not int or not 0 <= k <= n:
        raise ValueError('Invalid integer target counts')
    if n == 0:
        if cell.get('value') is not None:
            raise ValueError('Zero opportunity target has nonmissing value')
        return 0, 0
    if cell.get('value') is None or abs(cell['value']-k/n) > 1e-8:
        raise ValueError('Target rate differs from successes/opportunities')
    return k, n


def target_weights(examples):
    totals = defaultdict(lambda:[0]*len(TARGETS))
    for row in examples:
        for t, target in enumerate(TARGETS):
            totals[row['group_id']][t] += row['targets'][target]['opportunities'] or 0
    return [[(row['targets'][target]['opportunities'] or 0)/totals[row['group_id']][t]
             if totals[row['group_id']][t] else 0.0 for t,target in enumerate(TARGETS)]
            for row in examples]


def aggregate_records(records, protocol):
    result = metadata_examples(records, protocol)
    for row in result:
        row['targets'] = {}
        for target in TARGETS:
            counts = [validated_counts(records[i], target) for i in row['source_row_indices']]
            k, n = sum(c[0] for c in counts), sum(c[1] for c in counts)
            applicable = target == 'action0' or row['applicability'][target]
            if not applicable and n:
                raise ValueError('Outcomes supplied for structurally undefined target')
            row['targets'][target] = dict(successes=k if n else None, opportunities=n,
                                          value=k/n if n else None, applicable=applicable)
        row['y'] = [row['targets'][t]['value'] for t in TARGETS]
        row['successes'] = [row['targets'][t]['successes'] for t in TARGETS]
        row['opportunities'] = [row['targets'][t]['opportunities'] for t in TARGETS]
        row['mask'] = [n > 0 for n in row['opportunities']]
    for row, weights in zip(result, target_weights(result)):
        row['weights'] = weights
    return result


def build_folds(examples, development_examples=None, require_all_families=True):
    """Only payoff/group metadata are inspected; neither labels nor masks choose folds."""
    groups = {}
    for row in examples:
        info = dict(family=row['family'], coordinate=split_coordinate(row))
        if row['group_id'] in groups and groups[row['group_id']] != info:
            raise ValueError('Equivalent group has inconsistent split metadata')
        groups[row['group_id']] = info
    families = sorted({g['family'] for g in groups.values()})
    if require_all_families and set(families) != set(FAMILIES):
        raise ValueError('All seven declared families are required')
    result = []

    def add(fold_id, split, train_groups, test_groups, tests=None, details=None):
        tests = examples if tests is None else tests
        if train_groups & test_groups:
            raise ValueError('Game group crosses train/test')
        train = [i for i,r in enumerate(examples) if r['group_id'] in train_groups]
        test = [i for i,r in enumerate(tests) if r['group_id'] in test_groups]
        if not train or not test:
            raise ValueError('Empty fold')
        result.append(dict(fold_id=fold_id, split=split, train=train, test=test,
            test_dataset='train' if tests is examples else 'development',
            train_row_ids=[examples[i]['row_id'] for i in train], test_row_ids=[tests[i]['row_id'] for i in test],
            train_groups=sorted(train_groups), test_groups=sorted(test_groups),
            train_family_groups=dict(Counter(groups[g]['family'] for g in train_groups)),
            test_family_groups=dict(Counter(r['family'] for r in {x['group_id']:x for x in tests if x['group_id'] in test_groups}.values())),
            details=details or {}))

    for family in families:
        held = {g for g,info in groups.items() if info['family'] == family}
        add('family_'+family, 'family', set(groups)-held, held, details=dict(held_out_family=family))
    regions, table = defaultdict(set), {}
    for family in families:
        family_groups = {g:info['coordinate']['value'] for g,info in groups.items() if info['family'] == family}
        distinct = sorted(set(family_groups.values()))
        if len(distinct) < 3:
            raise ValueError('Need three distinct invariant coordinates within '+family)
        width = len(distinct)//3
        lower, middle, upper = distinct[:width], distinct[width:2*width], distinct[2*width:]
        cuts = {'lower': lower, 'middle': middle, 'upper': upper}
        table[family] = dict(coordinate=next(info['coordinate']['name'] for info in groups.values() if info['family']==family),
            distinct_values=distinct, regions={name:dict(min=min(values), max=max(values),
                groups=sorted(g for g,v in family_groups.items() if v in values)) for name,values in cuts.items()})
        for name, values in cuts.items():
            regions[name].update(g for g,v in family_groups.items() if v in values)
        assert max(lower) < min(middle) <= max(middle) < min(upper)
    add('within_family_interpolation', 'interpolation', regions['lower']|regions['upper'], regions['middle'], details=table)
    add('within_family_extrapolation', 'extrapolation', regions['lower']|regions['middle'], regions['upper'], details=table)
    if development_examples is not None:
        add('full', 'development', set(groups), {r['group_id'] for r in development_examples}, development_examples,
            details=dict(classification='Previously inspected 21-shape development cohort; not prospective'))
    return result


def support(examples):
    return dict(examples=len(examples), canonical_groups=len({r['group_id'] for r in examples}),
        source_rows=sum(len(r['source_row_indices']) for r in examples),
        episodes=len({e for r in examples for e in r['episode_ids']}),
        targets={t:dict(opportunities=sum(r['targets'][t]['opportunities'] for r in examples),
             eligible_examples=sum(r['targets'][t]['opportunities'] > 0 for r in examples),
             eligible_groups=len({r['group_id'] for r in examples if r['targets'][t]['opportunities'] > 0})) for t in TARGETS})


def export(training, development, manifest, output):
    inputs = {str(Path(p).resolve()): file_hash(p) for p in (training, development, manifest)}
    train_records = json.loads(Path(training).read_text())
    dev_records = json.loads(Path(development).read_text())
    original = json.loads(Path(manifest).read_text())
    protocol = original['protocol']
    train, dev = aggregate_records(train_records, protocol), aggregate_records(dev_records, protocol)
    folds = build_folds(train, dev)
    output = Path(output)
    if any((output/name).exists() for name in ('data.json','folds.json','provenance.json')):
        raise FileExistsError('Preserve existing export; choose a new directory')
    for path, expected in inputs.items():
        if file_hash(path) != expected:
            raise ValueError('Source changed during export: '+path)
    data = dict(schema_version=SCHEMA, targets=list(TARGETS), protocol=protocol, models=original['models'],
        train_examples=train, development_examples=dev,
        classification='Follow-up development data; all empirical fitting restricted to Fleet Training API jobs',
        weighting='Per target, n divided by total target opportunities in the canonical game; recompute after selecting each train fold.',
        aggregation='Exact payoff/game/ordered-context inputs; opposite display labels and repetitions marginalized; both focal roles retained in source mapping.')
    write_new(output/'data.json', data)
    write_new(output/'folds.json', folds)
    provenance = dict(created_utc=datetime.now(timezone.utc).isoformat(), source_sha256=inputs,
        source_code_sha256={str(Path(__file__).resolve()):file_hash(__file__),
                            str(Path(__file__).resolve().parents[1]/'games.py'):file_hash(Path(__file__).resolve().parents[1]/'games.py')},
        output_sha256={str((output/name).resolve()):file_hash(output/name) for name in ('data.json','folds.json')},
        training=support(train), development=support(dev), folds=len(folds), fitting_performed=False,
        coordinate_contract='canonical_t for PD/stag/chicken/harmony; canonical_s for weak dominance; |S-T|/(max-min) for equal-diagonal coordination/anti-coordination; rounded12, tied blocks never split; thirds by distinct metadata values within family.',
        source_records=dict(training=str(Path(training).resolve()),development=str(Path(development).resolve())))
    write_new(output/'provenance.json', provenance)
    return provenance


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--training', required=True)
    p.add_argument('--development', required=True)
    p.add_argument('--manifest', required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    result = export(a.training,a.development,a.manifest,a.out)
    print(json.dumps({k:result[k] for k in ('training','development','folds','fitting_performed')}))


if __name__ == '__main__':
    main()
