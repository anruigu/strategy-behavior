"""Join frozen ex-ante forecasts to later outcomes without refitting or rewriting them."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from collections import defaultdict

from prediction.modeling import (load_records, output_path, require_new_paths,
                                 write_new_json, supported_target, pair_id, SEED)
from prediction.analysis import summarize_predictions


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical_hash(data):
    # Exact serialization used by modeling.forecast_bundle's input_sha256.
    return sha(json.dumps(data, sort_keys=True, allow_nan=False).encode())


def _frozen_identity(data):
    return sha(json.dumps(data, sort_keys=True, ensure_ascii=False).encode())


def _time(value):
    if not isinstance(value, str):
        raise ValueError('Missing timestamp')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timestamp needs a timezone')
    return result.astimezone(timezone.utc)


def focal_key(row):
    episode, player = row.get('episode_id'), row.get('player_index')
    if not isinstance(episode, str) or not episode or type(player) is not int or player not in (0, 1):
        raise ValueError('Every episode-level row requires episode_id and integer player_index 0/1')
    return episode, player


def unique_index(rows, key, description):
    result = {}
    for row in rows:
        identity = key(row)
        if identity in result:
            raise ValueError(f'Duplicate/conflicting {description} key: {identity}')
        result[identity] = row
    return result


def build_rows(manifest):
    """Exactly two metadata-only focal rows per manifest episode, in manifest order."""
    games = unique_index(manifest['games'], lambda game: game['id'], 'game')
    specs = unique_index(manifest['episodes'], lambda spec: spec['id'], 'planned episode')
    rows = []
    for spec in specs.values():
        game = games[spec['game_id']]
        if len(spec['models']) != 2 or any(model not in manifest['models'] for model in spec['models']):
            raise ValueError('Planned episode has an unknown model or wrong player count')
        if type(spec['swap']) is not bool:
            raise ValueError('Planned swap must be boolean')
        if any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in game['payoffs'].values()):
            raise ValueError('Nonfinite planned payoffs')
        for player in (0, 1):
            row = dict(episode_id=spec['id'], player_index=player, game_id=game['id'],
                       group_id=game['group_id'], family=game['family'], model=spec['models'][player],
                       opponent=spec['models'][1-player], trial_id=spec['trial_id'],
                       representation=spec['representation'], swap=spec['swap'],
                       payoffs=copy.deepcopy(game['payoffs']), features=copy.deepcopy(game['features']),
                       split_metadata=copy.deepcopy(game.get('split_metadata', {})),
                       planned_manifest_sha256=canonical_hash(manifest))
            row['pair'] = pair_id(row)
            rows.append(row)
    return rows


def build_rows_file(manifest_path, output):
    raw = Path(manifest_path).read_bytes()
    manifest = json.loads(raw)
    rows = build_rows(manifest)
    output, companion = require_new_paths(output, Path(output).with_suffix('.manifest.json'))
    if output.suffix == '.jsonl':
        with output.open('x') as handle:
            for row in rows:
                handle.write(json.dumps(row, allow_nan=False)+'\n')
    else:
        write_new_json(output, rows)
    write_new_json(companion, dict(created_utc=datetime.now(timezone.utc).isoformat(),
        stage_manifest_path=str(Path(manifest_path).resolve()), stage_manifest_sha256=sha(raw),
        metadata_file_sha256=sha(output.read_bytes()), metadata_rows_sha256=canonical_hash(rows),
        planned_episodes=len(manifest['episodes']), focal_rows=len(rows), contains_targets=False))
    return rows


IDENTITY_FIELDS = ('game_id', 'group_id', 'family', 'model', 'opponent', 'trial_id', 'representation', 'swap')


def validate_compatible(row, planned, description, require_features=False):
    for field in IDENTITY_FIELDS:
        if field in row and row[field] != planned.get(field):
            raise ValueError(f'{description} conflicts with planned {field}: {focal_key(planned)}')
    if row.get('pair', pair_id(row)) != pair_id(planned):
        raise ValueError(f'{description} has inconsistent unordered pair')
    for field in ('payoffs', 'features'):
        if require_features and field not in row:
            raise ValueError(f'{description} is missing {field}')
        if field in row and field in planned and row[field] != planned[field]:
            raise ValueError(f'{description} conflicts with planned {field}')


def _check_forecast(row):
    if any(row.get(field) is not None for field in ('value', 'successes', 'opportunities')):
        raise ValueError('Source forecasts already contain outcome labels/counts')
    probability = row.get('prediction')
    if probability is not None and (type(probability) not in (int, float) or not math.isfinite(probability) or not 0 <= probability <= 1):
        raise ValueError('Invalid frozen probability')
    if not isinstance(row.get('target'), str) or not isinstance(row.get('method'), str):
        raise ValueError('Forecast requires target and method identifiers')


def _read_snapshot(path, snapshots):
    path = Path(path).resolve()
    raw = path.read_bytes()
    snapshots[str(path)] = raw
    return raw


def _read_json_snapshot(path, snapshots):
    return json.loads(_read_snapshot(path, snapshots))


def _read_forecasts(path, snapshots):
    raw = _read_snapshot(path, snapshots)
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def _records_snapshot(path, snapshots):
    raw = _read_snapshot(path, snapshots)
    if Path(path).suffix == '.jsonl':
        return [json.loads(line) for line in raw.splitlines() if line.strip()]
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get('records', data.get('measurements'))
    if not isinstance(data, list):
        raise ValueError('Expected a list of records')
    return data


def _audit_numerical(path, rows, planned, snapshots):
    result = {'kind': 'numerical', 'path': str(Path(path).resolve()), 'issues': []}
    companion = Path(path).with_suffix('.manifest.json')
    if not companion.exists():
        result['issues'].append('missing numerical forecast manifest')
        return result
    manifest = _read_json_snapshot(companion, snapshots)
    if manifest.get('forecast_sha256') != sha(snapshots[str(Path(path).resolve())]):
        raise ValueError('Numerical forecast bytes disagree with their frozen manifest hash')
    result['hash_verified'] = True
    if planned is None:
        result['issues'].append('planned feature rows unavailable: payoff/input identity unverified')
    elif manifest.get('input_sha256') != canonical_hash(planned):
        raise ValueError('Numerical input hash does not match planned game/model/episode metadata')
    else:
        result['input_identity_verified'] = True
    try:
        result['created_utc'] = _time(manifest.get('created_utc')).isoformat()
    except (ValueError, TypeError):
        result['issues'].append('missing or invalid numerical forecast creation timestamp')
    if manifest.get('rows') != len(rows):
        raise ValueError('Numerical forecast row count disagrees with manifest')
    return result


def _audit_llm(path, rows, manifest, planned, snapshots):
    path = Path(path)
    result = {'kind': 'llm', 'path': str(path.resolve()), 'issues': []}
    status_path, input_path = path.parent/'status.json', path.parent/'inputs.json'
    if not status_path.exists() or not input_path.exists():
        result['issues'].append('missing LLM forecast status or frozen input file')
        return result
    status, frozen = _read_json_snapshot(status_path, snapshots), _read_json_snapshot(input_path, snapshots)
    if status.get('forecast_sha256') != sha(snapshots[str(path.resolve())]):
        raise ValueError('LLM forecast bytes disagree with status hash')
    payload = frozen['payload']
    if frozen.get('identity_sha256') != _frozen_identity(payload):
        raise ValueError('LLM frozen input identity hash is invalid')
    if any(r.get('input_identity_sha256') != frozen['identity_sha256'] for r in rows):
        raise ValueError('LLM forecast input identity does not match frozen inputs')
    result['hash_verified'] = True
    frozen_games = unique_index(payload['games'], lambda r: r['id'], 'LLM game')
    for row in rows:
        if row['game_id'] not in frozen_games or row['model'] not in payload['players'] or row['opponent'] not in payload['players']:
            raise ValueError('LLM forecast context is absent from its frozen inputs')
    if planned is None:
        result['issues'].append('planned feature rows unavailable: LLM payoff identity unverified')
    else:
        for row in planned:
            game = frozen_games.get(row['game_id'])
            if game is None:
                continue  # Explicitly report partial forecast coverage later.
            if game['group_id'] != row['group_id'] or game['payoffs'] != row['payoffs']:
                raise ValueError('LLM frozen game payoffs/group disagree with planned game')
        result['input_identity_verified'] = True
    if manifest is not None:
        if payload['players'] != manifest['models']:
            raise ValueError('LLM player configurations differ from the target stage')
        mapping = {'rounds': 'rounds', 'temperature': 'player_temperature',
                   'max_tokens': 'player_max_completion_tokens', 'max_attempts': 'player_max_attempts'}
        if any(manifest['protocol'][a] != payload['protocol'][b] for a, b in mapping.items()):
            raise ValueError('LLM forecast gameplay protocol differs from target stage')
    else:
        result['issues'].append('stage manifest unavailable: LLM gameplay protocol unverified')
    timestamps = []
    for row in rows:
        if row.get('prediction') is not None:
            if row.get('status') != 'complete':
                raise ValueError('Noncomplete LLM forecast carries a probability')
            try:
                timestamps.append(_time(row.get('prediction_created_utc')))
            except (ValueError, TypeError):
                result['issues'].append('numeric LLM prediction lacks a valid completion timestamp')
    try:
        timestamps.append(_time(status.get('finished_utc')))
    except (ValueError, TypeError):
        result['issues'].append('LLM export lacks a valid completion timestamp')
    if timestamps:
        result['created_utc'] = max(timestamps).isoformat()
    return result


def _temporal_audit(stage_root, expected, snapshots):
    if stage_root is None:
        return {'issues': ['stage-root not supplied: no verified rollout start time'], 'earliest_started_utc': None}
    starts, observed_episodes = [], set()
    episodes = Path(stage_root)/'episodes'
    for filename in ('trace.json', 'progress.json', 'incomplete.json'):
        for path in sorted(episodes.glob('*/'+filename)):
            trace = _read_json_snapshot(path, snapshots)
            if trace.get('id') not in {key[0] for key in expected}:
                raise ValueError('Stage contains an unexpected episode trace')
            starts.append(_time(trace.get('started')))
            observed_episodes.add(trace['id'])
    if not starts:
        return {'issues': ['no actual trace start timestamps found'], 'earliest_started_utc': None}
    return {'issues': [], 'earliest_started_utc': min(starts).isoformat(),
            'episodes_with_timestamps': sorted(observed_episodes)}


def join_forecasts(numerical, llm, records, planned=None):
    actual = unique_index(records, focal_key, 'actual focal row')
    numeric_index = unique_index(numerical, lambda r: (*focal_key(r), r['target'], r['method']), 'numerical forecast')
    llm_index = unique_index(llm, lambda r: (r['game_id'], r['model'], r['opponent'], r['target'], r['method']), 'LLM forecast')
    for row in numerical + llm:
        _check_forecast(row)
    if planned is None:
        # With no immutable metadata input, identity checks remain possible but
        # payoff and temporal verification cannot support a prospective claim.
        planned_index = {}
        for row in numerical:
            key = focal_key(row)
            if key in planned_index:
                validate_compatible(row, planned_index[key], 'numerical forecast')
            else:
                planned_index[key] = {k: copy.deepcopy(v) for k, v in row.items()
                                      if k not in ('target', 'method', 'prediction', 'value', 'successes', 'opportunities')}
        planned = list(planned_index.values())
    expected = unique_index(planned, focal_key, 'planned focal row')
    for key, row in actual.items():
        if key not in expected:
            raise ValueError(f'Unexpected actual focal row: {key}')
        validate_compatible(row, expected[key], 'actual outcome', require_features=True)
    row_indices = {focal_key(row): i for i, row in enumerate(planned)}
    seen_row_indices = {}
    for row in numerical:
        key = focal_key(row)
        if key not in expected:
            raise ValueError('Numerical forecast refers to an unplanned episode/player')
        validate_compatible(row, expected[key], 'numerical forecast')
        index = row.get('row_index')
        if index is not None and index in seen_row_indices and seen_row_indices[index] != key:
            raise ValueError('One numerical row_index refers to different focal observations')
        seen_row_indices[index] = key
    contexts = {(r['game_id'], r['model'], r['opponent']) for r in planned}
    for row in llm:
        context = row['game_id'], row['model'], row['opponent']
        if context not in contexts:
            raise ValueError('LLM forecast refers to an unplanned game/model/opponent context')
        reference = next(r for r in planned if (r['game_id'], r['model'], r['opponent']) == context)
        for field in ('group_id', 'family', 'representation'):
            if row.get(field) != reference.get(field):
                raise ValueError('LLM forecast has conflicting '+field)
    joined, missing_outcomes = [], sorted(set(expected)-set(actual))
    def attach(source, plan):
        key = focal_key(plan)
        observation = actual.get(key)
        cell = supported_target(observation, source['target']) if observation is not None else None
        original_cell = observation.get('targets', {}).get(source['target'], {}) if observation is not None else {}
        result = {**source, **{field: plan.get(field) for field in IDENTITY_FIELDS},
                  'episode_id': key[0], 'player_index': key[1], 'row_index': row_indices[key],
                  'pair': pair_id(plan), 'fold': 'frozen',
                  'value': cell['value'] if cell else None,
                  'successes': original_cell.get('successes'), 'opportunities': original_cell.get('opportunities'),
                  'eligible': cell is not None, 'outcome_observed': observation is not None}
        joined.append(result)
    for row in numeric_index.values():
        attach(row, expected[focal_key(row)])
    for row in llm_index.values():
        for plan in planned:
            if (plan['game_id'], plan['model'], plan['opponent']) == (row['game_id'], row['model'], row['opponent']):
                attach(row, plan)
    unique_index(joined, lambda r: (*focal_key(r), r['target'], r['method']), 'joined method forecast')
    covered = {focal_key(row) for row in joined}
    coverage = dict(planned_focal_rows=len(planned), observed_focal_rows=len(actual),
                    planned_episodes=len({k[0] for k in expected}), observed_episodes=len({k[0] for k in actual}),
                    missing_planned_outcomes=[dict(episode_id=e, player_index=p) for e, p in missing_outcomes],
                    unforecast_planned_rows=[dict(episode_id=e, player_index=p) for e, p in sorted(set(expected)-covered)],
                    numerical_source_rows=len(numerical), llm_source_rows=len(llm), joined_rows=len(joined),
                    supported_joined_rows=sum(r['eligible'] for r in joined))
    by_method_target = defaultdict(list)
    for row in joined:
        by_method_target[row['method'], row['target']].append(row)
    coverage['method_target_coverage'] = [dict(method=method, target=target,
        forecast_rows=len(rows), observed_rows=sum(r['outcome_observed'] for r in rows),
        supported_rows=sum(r['eligible'] for r in rows),
        unavailable_probabilities=sum(r['prediction'] is None for r in rows))
        for (method, target), rows in sorted(by_method_target.items())]
    return joined, coverage, expected


def plot_scores(summary, outdir, prospective_verified):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    valid = [row for row in summary['scores'] if row['event_brier'] is not None]
    if not valid:
        return
    targets = sorted({r['target'] for r in valid})
    fig, axes = plt.subplots(len(targets), 1, figsize=(12, max(3.5, 2.8*len(targets))), squeeze=False)
    for target, ax in zip(targets, axes[:, 0]):
        rows = sorted([r for r in valid if r['target'] == target], key=lambda r: r['event_brier'])
        ax.plot(range(len(rows)), [r['event_brier'] for r in rows], 'o', color='#126B87')
        for i, row in enumerate(rows):
            interval = row['intervals'].get('event_brier')
            if interval:
                ax.vlines(i, interval['lower'], interval['upper'], color='#126B87')
        ax.set_xticks(range(len(rows)), [r['method'] for r in rows], rotation=30, ha='right', fontsize=8)
        ax.set_title(target, loc='left'); ax.set_ylabel('Brier score'); ax.grid(axis='y', alpha=.2)
    title = 'Verified prospective forecasts' if prospective_verified else 'Forecast scores: prospective timing unverified'
    fig.suptitle(title+'\nEqual game weights; lower Brier score is better')
    fig.tight_layout(); fig.savefig(outdir/'comparison.png', dpi=160); plt.close(fig)
    selected = [t for t in ('action0', 'cooperation') if t in targets] or targets[:2]
    fig, axes = plt.subplots(1, len(selected), figsize=(6*len(selected), 5), squeeze=False)
    for target, ax in zip(selected, axes[0]):
        target_rows = [r for r in valid if r['target'] == target]
        preferred = [r for r in target_rows if r['method'] in ('marginal', 'pair', 'combined_logistic_both', 'combined_mlp_both', 'llm_zero_shot', 'llm_game_theory')]
        for row in preferred or target_rows[:6]:
            points = row['calibration']
            ax.plot([p['prediction'] for p in points], [p['observed'] for p in points], 'o-', label=row['method'])
        ax.plot([0, 1], [0, 1], '--', color='gray'); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_title(target); ax.set_xlabel('Predicted probability'); ax.set_ylabel('Observed event rate')
        ax.legend(fontsize=8); ax.grid(alpha=.2)
    fig.tight_layout(); fig.savefig(outdir/'calibration.png', dpi=160); plt.close(fig)


def score(forecasts, records_path, outdir, llm_forecasts=None, split='prospective', stage_root=None,
          planned_rows=None, bootstrap=300, focus_pair=None, focus_model=None):
    if focus_pair and focus_model:
        raise ValueError('Select only one focus pair/model')
    snapshots = {}
    numerical = _read_forecasts(forecasts, snapshots)
    llm = _read_forecasts(llm_forecasts, snapshots) if llm_forecasts else []
    records = _records_snapshot(records_path, snapshots)
    records_sha256 = sha(snapshots[str(Path(records_path).resolve())])
    manifest = _read_json_snapshot(Path(stage_root)/'manifest.json', snapshots) if stage_root else None
    planned = build_rows(manifest) if manifest else (_records_snapshot(planned_rows, snapshots) if planned_rows else None)
    audits = [_audit_numerical(forecasts, numerical, planned, snapshots)]
    if llm_forecasts:
        audits.append(_audit_llm(llm_forecasts, llm, manifest, planned, snapshots))
    joined, coverage, expected = join_forecasts(numerical, llm, records, planned)
    temporal = _temporal_audit(stage_root, expected, snapshots)
    issues = list(temporal['issues'])
    for audit in audits:
        issues.extend(audit['issues'])
        if temporal['earliest_started_utc'] and audit.get('created_utc'):
            audit['precedes_rollouts'] = _time(audit['created_utc']) < _time(temporal['earliest_started_utc'])
            if not audit['precedes_rollouts']:
                issues.append(audit['kind']+' forecasts were not completed before target rollouts started')
        else:
            audit['precedes_rollouts'] = False
    timestamped = set(temporal.get('episodes_with_timestamps', []))
    if stage_root and {r['episode_id'] for r in records} - timestamped:
        issues.append('some observed outcome episodes lack actual trace start timestamps')
    verified = not issues and all(a.get('hash_verified') and a.get('input_identity_verified') and a.get('precedes_rollouts') for a in audits)
    effective_split = split if verified else 'unverified_'+split
    if focus_pair:
        pieces = focus_pair.split('|')
        if len(pieces) != 2 or not all(pieces):
            raise ValueError('focus-pair must contain two model IDs separated by |')
        focus_pair = '|'.join(sorted(pieces))
    def focused(row):
        return ((not focus_pair or pair_id(row) == focus_pair) and
                (not focus_model or focus_model in (row['model'], row['opponent'])))
    focused_expected = {key: row for key, row in expected.items() if focused(row)}
    if (focus_pair or focus_model) and not focused_expected:
        raise ValueError('Focus selection contains no planned episodes')
    joined = [row for row in joined if focused(row)]
    coverage['focus'] = {'pair': focus_pair, 'model': focus_model}
    coverage['scoring_planned_focal_rows'] = len(focused_expected)
    coverage['scoring_joined_rows'] = len(joined)
    coverage['scoring_missing_planned_outcomes'] = [row for row in coverage['missing_planned_outcomes']
                                                   if focal_key(row) in focused_expected]
    for row in joined:
        row['split'] = effective_split
    summary = summarize_predictions(joined, bootstrap=bootstrap, seed=SEED)
    audit = dict(created_utc=datetime.now(timezone.utc).isoformat(), prospective_verified=verified,
                 requested_split=split, effective_split=effective_split, issues=issues,
                 sources=audits, rollout_timing=temporal, records_sha256=records_sha256,
                 source_sha256={path: sha(raw) for path, raw in snapshots.items()},
                 limitations=['Temporal audit relies on saved timestamps and hashes, not an external notarization.'])
    # Detect edits during scoring; never modify any input or source forecast bytes.
    for path, raw in snapshots.items():
        if Path(path).read_bytes() != raw:
            raise ValueError('A frozen source changed while scoring: '+path)
    output = output_path(outdir)
    output.mkdir(parents=True, exist_ok=False)
    with (output/'joined-predictions.jsonl').open('x') as handle:
        for row in joined:
            handle.write(json.dumps(row, allow_nan=False)+'\n')
    write_new_json(output/'scores.json', summary)
    write_new_json(output/'coverage.json', coverage)
    plot_scores(summary, output, verified)
    write_new_json(output/'audit.json', audit)
    return {'audit': audit, 'coverage': coverage, 'scores': summary}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build-rows')
    build.add_argument('--manifest', required=True); build.add_argument('--output', required=True)
    scoring = sub.add_parser('score')
    scoring.add_argument('--forecasts', required=True); scoring.add_argument('--llm-forecasts')
    scoring.add_argument('--records', required=True); scoring.add_argument('--out', required=True)
    scoring.add_argument('--split', default='prospective'); scoring.add_argument('--stage-root')
    scoring.add_argument('--planned-rows', help='immutable metadata rows when stage-root is unavailable; timing remains unverified')
    scoring.add_argument('--bootstrap', type=int, default=300)
    focus = scoring.add_mutually_exclusive_group()
    focus.add_argument('--focus-pair', help='unordered IDs joined by |; validation still covers the entire stage')
    focus.add_argument('--focus-model', help='include both focal rows whenever this model appears in either role')
    args = parser.parse_args(argv)
    if args.command == 'build-rows':
        build_rows_file(args.manifest, args.output)
    else:
        score(args.forecasts, args.records, args.out, args.llm_forecasts, args.split,
              args.stage_root, args.planned_rows, args.bootstrap, args.focus_pair, args.focus_model)


if __name__ == '__main__':
    main()
