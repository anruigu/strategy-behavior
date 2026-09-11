"""Prepare and audit the improvement study's fresh, outcome-free cohort.

This module never trains, calls a model, or launches the frozen player runner.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from itertools import combinations_with_replacement
import json
import math
from pathlib import Path
import random

from prediction.games import generate_games, make_game
from prediction.prospective import build_rows


VERSION = 'improve-fresh-design-v1'
DEFAULT_SEED = 20260913
FAMILIES = ('prisoners_dilemma', 'stag_hunt', 'chicken', 'harmony',
            'coordination', 'anti_coordination', 'weak_dominance')
TARGETS = ('action0', 'cooperation', 'coordination')
PLAYER_MARKERS = ('process.json', 'status.json', 'episodes', 'calls')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def _read(path):
    return json.loads(Path(path).read_text())


def _time(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamps require an explicit timezone')
    return parsed.astimezone(timezone.utc)


def no_players_started(stage_root):
    present = [str(Path(stage_root)/name) for name in PLAYER_MARKERS
               if (Path(stage_root)/name).exists()]
    if present:
        raise ValueError('Fresh player stage has begun or has startup markers: '+', '.join(present))


def _immutable(path, value):
    path = Path(path).resolve()
    if not path.is_relative_to(Path('/shared/allie')):
        raise ValueError('Outputs must remain under /shared/allie')
    if path.exists():
        if _read(path) != value:
            raise ValueError('Refusing to replace different immutable design artifact: '+str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write('\n')


def observed_groups(record_sources):
    """Validate recorded payoff/group identities and return their unique union."""
    result, sources = set(), []
    for source in record_sources:
        records = _read(source)
        if not isinstance(records, list) or not records:
            raise ValueError('Observed records must be a nonempty list')
        source_groups, seen = set(), set()
        for row in records:
            signature = (row['group_id'], tuple(row['payoffs'][k] for k in ('R', 'S', 'T', 'P')))
            if signature not in seen:
                actual = make_game('identity-audit', **row['payoffs'])
                if actual['group_id'] != row['group_id'] or actual['family'] != row['family']:
                    raise ValueError('Observed game identity does not match its payoffs')
                seen.add(signature)
            source_groups.add(row['group_id'])
        result.update(source_groups)
        sources.append(dict(path=str(Path(source).resolve()), sha256=sha(source),
                            rows=len(records), groups=sorted(source_groups)))
    return result, sources


def fresh_games(forbidden_groups, seed=DEFAULT_SEED, per_family=4):
    if type(per_family) is not int or per_family <= 0:
        raise ValueError('per_family must be a positive integer')
    forbidden = set(forbidden_groups)
    selected, counts, scanned = [], Counter(), 0
    # Re-generating a larger deterministic prefix never redraws an accepted game.
    for length in range(7*per_family, 10001, 7*per_family):
        candidates = generate_games(seed=seed, n=length)
        for game in candidates[scanned:]:
            scanned += 1
            family = game['family']
            if family not in FAMILIES:
                raise ValueError('Generator produced an undeclared strategic family')
            if game['group_id'] in forbidden or counts[family] >= per_family:
                continue
            copied = deepcopy(game)
            copied['id'] = f'improve-fresh-g{len(selected):04d}'
            copied['design_version'] = VERSION
            selected.append(copied)
            forbidden.add(game['group_id'])
            counts[family] += 1
            if len(selected) == 7*per_family:
                return selected
    raise ValueError('Unable to fill the fixed family quotas without observed-shape overlap')


def make_manifest(primary, games, created_utc, seed=DEFAULT_SEED, stage_budget_usd=150., ledger=None):
    if len(primary['models']) != 4:
        raise ValueError('Exactly the original four players are required')
    protocol = primary['protocol']
    required = dict(rounds=8, temperature=.7, max_tokens=4096, max_attempts=2,
                    history='complete_public', objective='own_cumulative_points',
                    opponent_identity_disclosed=False)
    if any(protocol.get(key) != value for key, value in required.items()):
        raise ValueError('Player protocol differs from the fixed original study')
    if not 0 < stage_budget_usd <= 150:
        raise ValueError('Shared evaluation cap must be in (0,150], within the original Kimi CLI limit')
    _time(created_utc)
    episodes = []
    for game in games:
        for pair in combinations_with_replacement(sorted(primary['models']), 2):
            for trial in (0, 1):
                episodes.append(dict(id=f"{game['id']}--{pair[0]}--{pair[1]}--matrix--t{trial}",
                                     game_id=game['id'], models=list(pair), trial_id=trial,
                                     representation='matrix', swap=bool(trial)))
    random.Random(seed+1).shuffle(episodes)
    value = {key: deepcopy(primary[key]) for key in ('models', 'protocol', 'sources', 'source_root', 'ledger')}
    if ledger is not None:
        value['ledger'] = str(Path(ledger).resolve())
    value.update(stage='improve-fresh-prospective', created=created_utc,
                 games=deepcopy(games), episodes=episodes, stage_budget_usd=float(stage_budget_usd))
    return value


def audit_manifest(manifest, primary, forbidden_groups, per_family=4, ledger=None):
    games = manifest['games']
    if Counter(g['family'] for g in games) != Counter({f: per_family for f in FAMILIES}):
        raise ValueError('Fresh cohort must contain exactly four new shapes per family')
    groups = {g['group_id'] for g in games}
    if len(groups) != len(games) or groups & set(forbidden_groups):
        raise ValueError('Fresh cohort has duplicate or previously observed canonical groups')
    if any(manifest[k] != primary[k] for k in ('models', 'protocol', 'sources', 'source_root')):
        raise ValueError('Fresh manifest changed an original player/protocol/source field')
    if manifest['ledger'] != (str(Path(ledger).resolve()) if ledger is not None else primary['ledger']):
        raise ValueError('Fresh manifest has an unexpected authorization ledger')
    if not 0 < manifest.get('stage_budget_usd', 0) <= 150:
        raise ValueError('Fresh stage exceeds the shared150 USD evaluation cap')
    ids = {g['id'] for g in games}
    if len(ids) != len(games):
        raise ValueError('Duplicate fresh game IDs')
    for game in games:
        actual = make_game(game['id'], **game['payoffs'])
        for key in ('group_id', 'family', 'features', 'applicability', 'pure_nash'):
            if actual[key] != game[key]:
                raise ValueError('Fresh game metadata disagrees with its actual payoffs: '+key)
    seen = set()
    expected_pairs = set(combinations_with_replacement(sorted(primary['models']), 2))
    bygame = defaultdict(set)
    for e in manifest['episodes']:
        key = (tuple(e['models']), e['trial_id'])
        if e['id'] in seen or e['game_id'] not in ids or key in bygame[e['game_id']]:
            raise ValueError('Duplicate or unplanned player episode')
        if tuple(e['models']) not in expected_pairs or type(e['trial_id']) is not int or e['trial_id'] not in (0, 1):
            raise ValueError('Invalid pair or trial')
        if type(e['swap']) is not bool or e['swap'] != bool(e['trial_id']) or e['representation'] != 'matrix':
            raise ValueError('Display schedule or representation is not the balanced fixed matrix protocol')
        seen.add(e['id'])
        bygame[e['game_id']].add(key)
    expected = {(pair, trial) for pair in expected_pairs for trial in (0, 1)}
    if set(bygame) != ids or any(keys != expected for keys in bygame.values()):
        raise ValueError('Incomplete fresh pair/trial design')
    return dict(groups=len(groups), families=dict(Counter(g['family'] for g in games)),
                episodes=len(seen), focal_rows=2*len(seen),
                label_episodes=dict(Counter(str(e['swap']) for e in manifest['episodes'])),
                self_play_episodes=sum(e['models'][0] == e['models'][1] for e in manifest['episodes']))


def build_scopes(training, metadata, protocol, example_builder=None):
    if example_builder is None:
        from prediction.improve.data import metadata_examples
        example_builder = metadata_examples
    train_examples = example_builder(training, protocol)
    queries = example_builder(metadata, protocol)
    id_of = lambda row: row.get('row_id', row.get('example_id'))
    if any(not isinstance(id_of(row), str) for row in train_examples+queries):
        raise ValueError('Prepared examples require stable row_id/example_id strings')
    if len({id_of(r) for r in train_examples}) != len(train_examples) or len({id_of(r) for r in queries}) != len(queries):
        raise ValueError('Duplicate aggregated example identity')
    scopes = []
    for family in (None, *FAMILIES):
        ti = [i for i, row in enumerate(training) if family is None or row['family'] != family]
        qi = [i for i, row in enumerate(metadata) if family is None or row['family'] == family]
        te = [i for i, row in enumerate(train_examples) if family is None or row['family'] != family]
        qe = [i for i, row in enumerate(queries) if family is None or row['family'] == family]
        if not te or not qe:
            raise ValueError('Empty training or fresh-query scope')
        scopes.append(dict(scope_id='full' if family is None else 'family_'+family,
                           setting='full' if family is None else 'family_excluded', excluded_family=family,
                           train_original_row_indices=ti, query_original_row_indices=qi,
                           train_example_indices=te, query_example_indices=qe,
                           train_row_ids=[id_of(train_examples[i]) for i in te],
                           query_row_ids=[id_of(queries[i]) for i in qe],
                           train_group_ids=sorted({training[i]['group_id'] for i in ti}),
                           query_group_ids=sorted({metadata[i]['group_id'] for i in qi})))
    for scope in scopes:
        if set(scope['train_group_ids']) & set(scope['query_group_ids']):
            raise ValueError('Fresh forecast scope leaks a query shape into training')
        selected = set(scope['train_original_row_indices'])
        episode_indices = defaultdict(set)
        for i, row in enumerate(training):
            episode_indices[row['episode_id']].add(i)
        if any(indices & selected and not indices <= selected for indices in episode_indices.values()):
            raise ValueError('Training scope split focal roles or repeated episode copies')
    family_queries = [i for s in scopes[1:] for i in s['query_original_row_indices']]
    if sorted(family_queries) != list(range(len(metadata))):
        raise ValueError('LOFO query scopes must partition exactly the same full fresh outcomes')
    expansion = []
    for query in queries:
        indices = query['source_row_indices']
        if not indices:
            raise ValueError('Every aggregated query needs an expansion to player outcomes')
        expansion.append(dict(row_id=id_of(query), game_id=query['game_id'], group_id=query['group_id'],
                              outcomes=[dict(original_row_index=i, episode_id=metadata[i]['episode_id'],
                                             player_index=metadata[i]['player_index'], trial_id=metadata[i]['trial_id'],
                                             swap=metadata[i]['swap']) for i in indices]))
    if sorted(x['original_row_index'] for q in expansion for x in q['outcomes']) != list(range(len(metadata))):
        raise ValueError('Query expansion must retain every focal outcome exactly once')
    return scopes, queries, train_examples, expansion


def prepare(previous_root, run_root, seed=DEFAULT_SEED, stage_budget_usd=150.):
    previous_root, run_root = Path(previous_root).resolve(), Path(run_root).resolve()
    if not run_root.is_relative_to(Path('/shared/allie')) or run_root.is_relative_to(previous_root):
        raise ValueError('New artifacts must be under /shared/allie and outside the old run')
    out, stage = run_root/'prospective-design', run_root/'fresh-prospective'
    no_players_started(stage)
    sources = [previous_root/'training-records.json', previous_root/'prospective/collected/records.json',
               previous_root/'controls/collected/records.json']
    forbidden, provenance = observed_groups(sources)
    if [len(s['groups']) for s in provenance] != [72, 21, 7] or len(forbidden) != 93:
        raise ValueError('The declared observed history must contain 72/21/7 source groups, with exactly93 unique shapes')
    primary_path = previous_root/'primary-pilot-manifest.json'
    primary, training = _read(primary_path), _read(sources[0])
    frozen_sources = {}
    for name in ('prediction/games.py', 'prediction/measurements.py', 'prediction/runner.py', 'prediction/study.py',
                 'prediction/client.py', 'prediction/io_utils.py', 'benchmark/clients.py', 'benchmark/fullscale/budget.py'):
        frozen_path = Path(primary['source_root'])/name
        if sha(frozen_path) != primary['sources'][name]:
            raise ValueError('Original frozen scientific source changed: '+name)
        frozen_sources[str(frozen_path)] = primary['sources'][name]
    implementation = Path(__file__).resolve().parents[1]
    source_paths = [Path(__file__).resolve(), implementation/'improve/data.py', implementation/'games.py',
                    implementation/'prospective.py']
    ledger = run_root/'authorization-budget.sqlite'
    contract = dict(version=VERSION, seed=seed, observed_sources=provenance,
                    primary_manifest_path=str(primary_path), primary_manifest_sha256=sha(primary_path),
                    implementation_sha256={str(path): sha(path) for path in source_paths},
                    frozen_player_source_sha256=frozen_sources,
                    authorization_ledger=str(ledger), shared_eval_ledger=str(run_root/'eval-budget.sqlite'),
                    stage_budget_usd=float(stage_budget_usd))
    old_audit = _read(out/'audit.json') if (out/'audit.json').exists() else None
    if old_audit and old_audit['contract'] != contract:
        raise ValueError('Design inputs or implementation changed since preparation')
    created = old_audit['created_utc'] if old_audit else datetime.now(timezone.utc).isoformat()
    manifest = make_manifest(primary, fresh_games(forbidden, seed), created, seed, stage_budget_usd, ledger)
    summary = audit_manifest(manifest, primary, forbidden, ledger=ledger)
    metadata = build_rows(manifest)
    scopes, queries, train_examples, expansion = build_scopes(training, metadata, primary['protocol'])
    if len(queries) != 448 or len(metadata) != 1120:
        raise ValueError('Fresh cohort requires448 ordered-context queries and1120 focal outcomes')
    files = {stage/'manifest.json': manifest, stage/'metadata.json': metadata,
             out/'queries.json': queries, out/'training-example-metadata.json': train_examples,
             out/'scopes.json': scopes, out/'expansion.json': expansion,
             out/'players.json': dict(models=primary['models'], protocol=primary['protocol'])}
    for scope in scopes:
        folder = out/'scopes'/scope['scope_id']
        files[folder/'training-records.json'] = [training[i] for i in scope['train_original_row_indices']]
        selected_games = [g for g in manifest['games'] if g['group_id'] in set(scope['query_group_ids'])]
        files[folder/'games.json'] = dict(games=selected_games, protocol=primary['protocol'])
        files[folder/'queries.json'] = [queries[i] for i in scope['query_example_indices']]
    for path, value in files.items():
        _immutable(path, value)
    for source in provenance:
        if sha(source['path']) != source['sha256']:
            raise ValueError('Observed source changed during design preparation')
    no_players_started(stage)
    audit = dict(created_utc=created, status='prepared_not_authorized_to_launch', contract=contract,
                 observed_unique_groups=len(forbidden), fresh_summary=summary,
                 ordered_context_queries=len(queries), total_few_shot_queries=2*len(queries),
                 required_forecast_scopes=[s['scope_id'] for s in scopes],
                 artifact_sha256={str(path): sha(path) for path in files},
                 chronology='Root driver must freeze every full and family-excluded forecast or explicit technical exclusion before any fresh player startup marker. Preparation itself never authorizes launch.',
                 budget='Root owns the new authorization ledger with imported prior commitments. The inference wrapper routes every forecast/player stage Ledger connection to canonical eval-budget.sqlite capped at150 USD, below the authorized200 USD stage cap; aliases are display conveniences only.')
    _immutable(out/'audit.json', audit)
    return audit


def verify_prepared(run_root, require_unstarted=False):
    """Read-only verification also works when resuming after players have begun."""
    root = Path(run_root).resolve()
    audit = _read(root/'prospective-design/audit.json')
    if require_unstarted:
        no_players_started(root/'fresh-prospective')
    contract = audit['contract']
    expected = dict(audit['artifact_sha256'])
    expected.update(contract['implementation_sha256'])
    expected.update(contract.get('frozen_player_source_sha256', {}))
    expected[contract['primary_manifest_path']] = contract['primary_manifest_sha256']
    expected.update({s['path']: s['sha256'] for s in contract['observed_sources']})
    for path, value in expected.items():
        if sha(path) != value:
            raise ValueError('Prepared design/input/source changed: '+path)
    return audit


def forecast_coverage(scopes, queries, predictions, required_methods, numerical_methods,
                      technical_exclusions=()):
    """Audit normalized context forecasts; never impute a missing prediction.

    Rows: scope_id, method, row_id, target, prediction. An explicit technical
    exclusion may permit incomplete scope/method coverage, but never removes it
    silently from the declared all-method intersection. Target inapplicability
    comes from payoff metadata, not observed fresh opportunities.
    """
    methods = set(required_methods)
    if not methods or len(methods) != len(required_methods) or not set(numerical_methods) <= methods:
        raise ValueError('Required methods must be distinct and include all numerical methods')
    scope_index = {s['scope_id']: s for s in scopes}
    query_index = {q.get('row_id', q.get('example_id')): q for q in queries}
    exclusions = {}
    for exclusion in technical_exclusions:
        key = exclusion['scope_id'], exclusion['method']
        if key[0] not in scope_index or key[1] not in methods or not exclusion.get('reason', '').strip():
            raise ValueError('Technical exclusions require a declared scope/method and explicit reason')
        if key in exclusions:
            raise ValueError('Duplicate technical exclusion')
        _time(exclusion['created_utc'])
        exclusions[key] = exclusion
    index = {}
    for row in predictions:
        scope, method, query, target = (row[k] for k in ('scope_id', 'method', 'row_id', 'target'))
        if scope not in scope_index or method not in methods or query not in scope_index[scope]['query_row_ids'] or target not in TARGETS:
            raise ValueError('Forecast row refers to an undeclared method/scope/query/target')
        if any(row.get(field) is not None for field in ('value', 'successes', 'opportunities', 'targets')):
            raise ValueError('Pre-rollout forecast rows must not contain fresh outcome supervision')
        key = scope, method, query, target
        if key in index:
            raise ValueError('Duplicate normalized forecast key')
        p = row.get('prediction')
        if p is not None and (type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1):
            raise ValueError('Forecast probability must be finite and in [0,1], or explicitly missing')
        index[key] = p
    support, missing = [], []
    for scope in scopes:
        sid = scope['scope_id']
        for target in TARGETS:
            def applicable(qid):
                app = query_index[qid]['applicability']
                return target == 'action0' or (app['cooperative_action'] is not None if target == 'cooperation' else app['coordination'])
            expected = {qid for qid in scope['query_row_ids'] if applicable(qid)}
            valid = {}
            for method in sorted(methods):
                valid[method] = {qid for qid in expected if index.get((sid, method, qid, target)) is not None}
                absent = sorted(expected-valid[method])
                if absent:
                    missing.append(dict(scope_id=sid, method=method, target=target, row_ids=absent,
                                        technical_exclusion_recorded=(sid, method) in exclusions))
                for qid in set(scope['query_row_ids'])-expected:
                    if index.get((sid, method, qid, target)) is not None:
                        raise ValueError('Structurally unsupported forecast must be null or absent')
            common = set.intersection(*(valid[m] for m in sorted(methods)))
            numeric = set.intersection(*(valid[m] for m in numerical_methods)) if numerical_methods else set()
            support.append(dict(scope_id=sid, setting=scope['setting'], target=target,
                                expected_row_ids=sorted(expected),
                                valid_row_ids_by_method={m: sorted(ids) for m, ids in valid.items()},
                                all_method_common_row_ids=sorted(common), numerical_common_row_ids=sorted(numeric)))
    undeclared = [cell for cell in missing if not cell['technical_exclusion_recorded']]
    return dict(ready=not undeclared, required_methods=sorted(methods), numerical_methods=list(numerical_methods),
                scope_ids=[s['scope_id'] for s in scopes],
                query_identity_sha256=digest(queries), scope_identity_sha256=digest(scopes),
                normalized_prediction_sha256=digest(predictions),
                technical_exclusions=list(technical_exclusions), missing=missing, support=support,
                limitation='Coverage is structural pre-outcome support. Final scoring must additionally use actual valid episodes and opportunity counts, retaining both focal roles and whole game clusters. Technical failures remain visible in all-declared-method support.')


def freeze_forecast_evidence(run_root, files, coverage, normalized_predictions_path, created_utc=None):
    """Bind reviewable forecast evidence before root may launch any fresh player.

    Root supplies every forecast, checkpoint/provenance/source/protocol artifact
    and any technical-exclusion evidence in files. This helper cannot assert
    remote fitting happened; Fleet submissions/artifact lineage must be audited
    separately by the root driver and included among those bound files.
    """
    root = Path(run_root).resolve()
    design = verify_prepared(root)
    scopes = _read(root/'prospective-design/scopes.json')
    queries = _read(root/'prospective-design/queries.json')
    normalized_path = Path(normalized_predictions_path).resolve()
    raw = normalized_path.read_bytes()
    predictions = ([json.loads(line) for line in raw.decode().splitlines() if line]
                   if normalized_path.suffix == '.jsonl' else json.loads(raw))
    recomputed = forecast_coverage(scopes, queries, predictions, coverage['required_methods'],
                                   coverage['numerical_methods'], coverage['technical_exclusions'])
    if coverage != recomputed or coverage.get('ready') is not True:
        raise ValueError('Forecast coverage must pass on the exact frozen query and scope design')
    evidence = {str(Path(p).resolve()): sha(p) for p in files}
    if not evidence:
        raise ValueError('Concrete forecast/provenance files are required')
    evidence[str(normalized_path)] = hashlib.sha256(raw).hexdigest()
    path = root/'fresh-prospective/forecast-freeze.json'
    if path.exists():
        previous = _read(path)
        if previous['artifact_sha256'] != evidence or previous['coverage'] != coverage or previous['design_audit_sha256'] != sha(root/'prospective-design/audit.json'):
            raise ValueError('Frozen forecast evidence changed')
        return previous
    no_players_started(root/'fresh-prospective')
    timestamp = created_utc or datetime.now(timezone.utc).isoformat()
    freeze_time = _time(timestamp)
    if freeze_time < _time(design['created_utc']):
        raise ValueError('Forecast freeze cannot predate cohort preparation')
    if any(_time(x['created_utc']) > freeze_time for x in coverage['technical_exclusions']):
        raise ValueError('Technical exclusions must be recorded before the forecast freeze')
    value = dict(created_utc=timestamp, status='forecasts_frozen_before_fresh_rollouts',
                 design_audit_sha256=sha(root/'prospective-design/audit.json'),
                 artifact_sha256=evidence, coverage=coverage,
                 interpretation='Same fresh outcomes support distinct full72 and family-excluded settings. Root still owns optimization/gate/budget checks and runner launch; post-collection actual trace timing must independently verify this ordering.')
    for name, expected in evidence.items():
        if sha(name) != expected:
            raise ValueError('Forecast evidence changed during freezing')
    _immutable(path, value)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous-root', type=Path, required=True)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=DEFAULT_SEED)
    parser.add_argument('--stage-budget', type=float, default=150.)
    args = parser.parse_args(argv)
    print(json.dumps(prepare(args.previous_root, args.run_root, args.seed, args.stage_budget), indent=2))


if __name__ == '__main__':
    main()
