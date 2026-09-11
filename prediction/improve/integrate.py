"""Pure joins and explicit post-rollout collection; never fits or calls a model."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

from prediction.improve.data import TARGETS, aggregate_records, file_hash, target_weights


def read(path):
    return json.loads(Path(path).read_text())


def stamp(value):
    if not isinstance(value, str):
        raise ValueError('A timestamp string is required')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('An explicit timezone is required')
    return result.astimezone(timezone.utc)


def immutable(path, value, jsonl=False):
    path = Path(path).resolve()
    if not path.is_relative_to(Path('/shared/allie')):
        raise ValueError('Outputs must use shared storage')
    payload = (''.join(json.dumps(row, allow_nan=False)+'\n' for row in value) if jsonl else
               json.dumps(value, indent=2, allow_nan=False)+'\n')
    if path.exists():
        if path.read_text() != payload:
            raise ValueError('Immutable output differs: '+str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        handle.write(payload)


def prompted(source, examples, out, split, fold_id):
    """Join saved forecast metadata exactly, preserving missing probabilities."""
    source, out = Path(source).resolve(), Path(out).resolve()
    index, ids = {}, set()
    for example in examples:
        key = example['game_id'], example['model'], example['opponent']
        if key in index or example['row_id'] in ids:
            raise ValueError('Duplicate or ambiguous input example key')
        index[key] = example
        ids.add(example['row_id'])
    source_bytes = source.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    rows, seen = [], set()
    for line in source_bytes.decode().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row['method'] != 'llm_few_shot' or row['target'] not in TARGETS:
            continue
        key = row['game_id'], row['model'], row['opponent']
        if key not in index:
            raise ValueError('Unplanned prompted query')
        example = index[key]
        identity = example['row_id'], row['target']
        if identity in seen:
            raise ValueError('Duplicate prompted query/target')
        seen.add(identity)
        for field in ('group_id', 'family', 'representation', 'payoffs'):
            if field in row and row[field] != example[field]:
                raise ValueError('Prompted metadata mismatch: '+field)
        if any(row.get(field) is not None for field in ('value', 'successes', 'opportunities', 'targets')):
            raise ValueError('Prompted forecast source contains observed outcomes')
        probability = row['prediction']
        applicable = row['target'] == 'action0' or example['applicability'][row['target']]
        if 'structurally_applicable' in row and row['structurally_applicable'] != applicable:
            raise ValueError('Prompted target applicability mismatch')
        if probability is not None:
            if type(probability) not in (int, float) or not math.isfinite(probability) or not 0 <= probability <= 1:
                raise ValueError('A finite probability in [0,1] is required')
            if not applicable:
                raise ValueError('Unsupported target has a probability')
            if row.get('prediction_created_utc') is None:
                raise ValueError('A completed prediction needs a creation timestamp')
        if row.get('prediction_created_utc') is not None:
            stamp(row['prediction_created_utc'])
        clean = {k: example[k] for k in ('row_id', 'game_id', 'group_id', 'model', 'opponent', 'family')}
        clean.update(method='llm_few_shot', split=split, fold_id=fold_id, target=row['target'],
                     prediction=probability, source_prediction_created_utc=row.get('prediction_created_utc'))
        rows.append(clean)
    expected = {(e['row_id'], t) for e in examples for t in TARGETS}
    manifest_path = out.with_suffix('.manifest.json')
    created = read(manifest_path)['created_utc'] if manifest_path.exists() else datetime.now(timezone.utc).isoformat()
    if file_hash(source) != source_hash:
        raise ValueError('Prompted source changed during joining')
    immutable(out, rows, jsonl=True)
    immutable(manifest_path, dict(created_utc=created, source=str(source), source_sha256=source_hash,
        output_sha256=file_hash(out), forecasts=len(rows), expected_rows=len(expected),
        missing_row_targets=[list(k) for k in sorted(expected-seen)],
        valid_predictions_by_target={t: sum(r['target'] == t and r['prediction'] is not None for r in rows) for t in TARGETS},
        fitting_performed=False,
        interpretation='Exact primary-target metadata join of saved prompted forecasts. Missing probabilities remain null; no new model calls.'))
    return rows


def collect(root):
    """Collect only a terminal stage; all fresh outcome reads are inside this call."""
    from prediction.runner import verify_trace
    from prediction.measurements import measure_episode
    from prediction.improve.prospective_design import verify_prepared
    root = Path(root).resolve()
    if not root.is_relative_to(Path('/shared/allie')):
        raise ValueError('Run root must use shared storage')
    stage, out = root/'fresh-prospective', root/'fresh-collected'
    verify_prepared(root)
    paths = [stage/'manifest.json', stage/'forecast-freeze.json', stage/'status.json',
             root/'data/data.json', root/'prospective-design/queries.json',
             root/'prospective-design/scopes.json', root/'prospective-design/expansion.json',
             stage/'metadata.json', root/'prospective-design/audit.json']
    input_hashes = {str(p): file_hash(p) for p in paths}
    manifest, freeze, status = (read(stage/name) for name in ('manifest.json', 'forecast-freeze.json', 'status.json'))
    if status.get('status') not in ('complete', 'finished_with_errors'):
        raise ValueError('Fresh player stage is not terminal')
    if freeze.get('status') != 'forecasts_frozen_before_fresh_rollouts' or freeze.get('coverage', {}).get('ready') is not True:
        raise ValueError('A completed forecast freeze is required')
    if freeze['design_audit_sha256'] != file_hash(root/'prospective-design/audit.json'):
        raise ValueError('Forecast freeze design audit differs')
    frozen_time = stamp(freeze['created_utc'])
    for path, expected in freeze['artifact_sha256'].items():
        if file_hash(path) != expected:
            raise ValueError('Frozen forecast evidence changed')
        input_hashes[path] = expected
    source_root = Path(__file__).resolve().parents[2]
    source_hashes = {}
    for relative in ('prediction/runner.py', 'prediction/measurements.py', 'prediction/games.py'):
        path = source_root/relative
        if file_hash(path) != manifest['sources'][relative]:
            raise ValueError('Measurement/trace source changed')
        source_hashes[str(path)] = manifest['sources'][relative]
    metadata = read(stage/'metadata.json')
    expected_roles = {(r['episode_id'], r['player_index']): r for r in metadata}
    if len(expected_roles) != len(metadata) or len(metadata) != 2*len(manifest['episodes']):
        raise ValueError('Invalid planned episode/role mapping')
    specs = {s['id']: s for s in manifest['episodes']}
    if len(specs) != len(manifest['episodes']):
        raise ValueError('Duplicate planned episode ID')
    existing = {p.parent.name for p in (stage/'episodes').glob('*/trace.json')}
    if existing-set(specs):
        raise ValueError('Unplanned complete episode directory')
    # Capture inputs before the verifier reads them; recheck every byte before export.
    call_snapshot = {str(p): file_hash(p) for p in (stage/'calls').rglob('*.json')}
    decision_snapshot = {str(p): file_hash(p) for p in (stage/'episodes').glob('*/round-*-player-*.json')}
    records, missing, seen_roles, seen_episodes = [], [], set(), set()
    trace_hashes, decision_hashes, selected_calls, trace_finished = {}, {}, set(), {}
    for spec in manifest['episodes']:
        path = stage/'episodes'/spec['id']/'trace.json'
        if not path.exists():
            missing.append(spec['id'])
            continue
        before = file_hash(path)
        if read(path)['id'] != spec['id']:
            raise ValueError('Trace identity differs from scheduled episode path')
        trace = verify_trace(path, manifest)
        if trace['id'] != spec['id'] or trace['id'] in seen_episodes:
            raise ValueError('Duplicate or mismatched verified episode')
        seen_episodes.add(trace['id'])
        started, finished = stamp(trace['started']), stamp(trace['finished'])
        if started < frozen_time or finished < started:
            raise ValueError('Invalid player trace chronology relative to forecast freeze')
        trace_finished[trace['id']] = finished
        for turn in trace['rounds']:
            for role in (0, 1):
                filename = f"round-{turn['round']:02}-player-{role}.json"
                if turn['decisions'][role] != filename:
                    raise ValueError('Decision filename differs from scheduled round/role')
                decision_path = path.parent/filename
                decision_hashes[str(decision_path)] = decision_snapshot[str(decision_path)]
                if file_hash(decision_path) != decision_hashes[str(decision_path)]:
                    raise ValueError('Decision changed during verification')
                decision = read(decision_path)
                call_path = stage/'calls'/spec['models'][role]/(decision['attempts'][-1]['meta']['call_id']+'.json')
                if str(call_path) in selected_calls:
                    raise ValueError('A successful player call was reused across decisions')
                selected_calls.add(str(call_path))
                if stamp(read(call_path)['timestamp']) > finished:
                    raise ValueError('A selected call postdates its completed trace')
        rows = measure_episode(trace)
        if len(rows) != 2:
            raise ValueError('A complete episode requires two focal rows')
        for row in rows:
            key = row['episode_id'], row['player_index']
            if row['episode_id'] != trace['id'] or type(row['player_index']) is not int or key not in expected_roles or key in seen_roles:
                raise ValueError('Duplicate or unplanned focal role')
            expected = expected_roles[key]
            for field in ('game_id', 'group_id', 'family', 'model', 'opponent', 'trial_id', 'swap', 'representation', 'payoffs'):
                if row[field] != expected[field]:
                    raise ValueError('Measured role differs from planned metadata: '+field)
            seen_roles.add(key)
        records.extend(rows)
        if file_hash(path) != before:
            raise ValueError('Trace changed during verification')
        trace_hashes[str(path)] = before
    if not records:
        raise ValueError('No verified complete fresh episodes')
    call_hashes, call_times = {}, []
    for path in sorted((stage/'calls').rglob('*.json')):
        before = file_hash(path)
        if call_snapshot.get(str(path)) != before:
            raise ValueError('Call files changed during verification')
        call = read(path)
        call_time = stamp(call['timestamp'])
        if call_time < frozen_time:
            raise ValueError('A player call predates the forecast freeze')
        if call.get('call_id') != path.stem:
            raise ValueError('Call identity differs from its file')
        call_hashes[str(path)] = before
        call_times.append(call_time)
    if set(call_hashes) != set(call_snapshot):
        raise ValueError('Call inventory changed during verification')
    if not selected_calls <= set(call_hashes):
        raise ValueError('Missing selected player call provenance')
    original = read(root/'data/data.json')
    queries = read(root/'prospective-design/queries.json')
    if len({q['row_id'] for q in queries}) != len(queries):
        raise ValueError('Duplicate planned context')
    observed = {r['row_id']: r for r in aggregate_records(records, manifest['protocol'])}
    if set(observed)-{q['row_id'] for q in queries}:
        raise ValueError('Unexpected observed context')
    examples = []
    for query in queries:
        if query['row_id'] in observed:
            row = observed[query['row_id']]
        else:
            row = deepcopy(query)
            row.update(source_row_indices=[], episode_ids=[], targets={})
            for target in TARGETS:
                row['targets'][target] = dict(successes=None, opportunities=0, value=None,
                    applicable=target == 'action0' or row['applicability'][target])
            row.update(y=[None]*3, successes=[None]*3, opportunities=[0]*3, mask=[False]*3)
        examples.append(row)
    for row, weights in zip(examples, target_weights(examples)):
        row['weights'] = weights
    scopes, folds = read(root/'prospective-design/scopes.json'), []
    for scope in scopes:
        train, test, sid = scope['train_example_indices'], scope['query_example_indices'], scope['scope_id']
        if [original['train_examples'][i]['row_id'] for i in train] != scope['train_row_ids']:
            raise ValueError('Training scope no longer matches prepared IDs')
        if [examples[i]['row_id'] for i in test] != scope['query_row_ids']:
            raise ValueError('Query scope no longer matches prepared IDs')
        folds.append(dict(fold_id=sid, split='fresh_full' if sid == 'full' else 'fresh_family_excluded',
            train=train, test=test, test_dataset='development', train_row_ids=scope['train_row_ids'],
            test_row_ids=scope['query_row_ids'], train_groups=scope['train_group_ids'], test_groups=scope['query_group_ids']))
    data = dict(original, development_examples=examples,
                classification='Fresh prospective outcomes, measured after all forecasts were frozen')
    group_id = {g['id']: g['group_id'] for g in manifest['games']}
    group_coverage = defaultdict(lambda: dict(planned_episodes=0, complete_episodes=0))
    for spec in manifest['episodes']:
        cell = group_coverage[group_id[spec['game_id']]]
        cell['planned_episodes'] += 1
        cell['complete_episodes'] += spec['id'] in seen_episodes
    for cell in group_coverage.values():
        cell['complete'] = cell['planned_episodes'] == cell['complete_episodes']
    audit_path = out/'audit.json'
    created = read(audit_path)['created_utc'] if audit_path.exists() else datetime.now(timezone.utc).isoformat()
    for path, expected in {**input_hashes, **source_hashes, **trace_hashes, **decision_hashes, **call_hashes}.items():
        if file_hash(path) != expected:
            raise ValueError('Verified collection input changed: '+path)
    immutable(out/'records.json', records)
    immutable(out/'data.json', data)
    immutable(out/'folds.json', folds)
    immutable(audit_path, dict(status='verified', collection_status='complete' if not missing else 'complete_with_missing_episodes',
        runner_status=status['status'], runner_reported_completed=status.get('completed'), runner_errors=status.get('errors', []),
        runner_coverage_matches_verified=status.get('completed') == len(seen_episodes),
        created_utc=created, planned_episodes=len(specs), complete_episodes=len(seen_episodes), missing_episodes=missing,
        focal_rows=len(records), distinct_episode_roles=len(seen_roles), contexts=len(examples),
        observed_contexts=len(observed), missing_contexts=len(examples)-len(observed),
        complete_canonical_groups=sum(c['complete'] for c in group_coverage.values()),
        canonical_group_coverage=dict(group_coverage),
        observed_label_episodes=dict(Counter(str(specs[e]['swap']) for e in seen_episodes)),
        forecast_freeze_utc=freeze['created_utc'], first_player_call_utc=min(call_times).isoformat() if call_times else None,
        last_player_call_utc=max(call_times).isoformat() if call_times else None,
        selected_successful_calls=len(selected_calls), all_recorded_calls=len(call_hashes),
        trace_sha256=trace_hashes, decision_sha256=decision_hashes, call_sha256=call_hashes,
        input_sha256=input_hashes, source_sha256=source_hashes,
        output_sha256={str(out/n): file_hash(out/n) for n in ('records.json', 'data.json', 'folds.json')},
        interpretation='All planned contexts retained. Missing observations are null with zero opportunities. Group weights use actual observed counts; partial games and label imbalance are reported, not imputed. Call timing includes failed calls and retries; resumed traces can begin after cached calls, all of which must follow the forecast freeze.'))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    command = sub.add_parser('development-prompts')
    command.add_argument('--run-root', required=True)
    command.add_argument('--source', required=True)
    command = sub.add_parser('collect')
    command.add_argument('--run-root', required=True)
    args = parser.parse_args()
    root = Path(args.run_root)
    if args.command == 'collect':
        collect(root)
    else:
        prompted(args.source, read(root/'data/data.json')['development_examples'],
                 root/'development-few-shot/forecasts.jsonl', 'development', 'full')


if __name__ == '__main__':
    main()
