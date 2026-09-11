"""Bounded, immutable continuation after matrix evaluation. Importing makes no calls."""
from __future__ import annotations

import argparse
from copy import deepcopy
import fcntl
import hashlib
from itertools import combinations_with_replacement
import json
import math
from pathlib import Path
import random
import subprocess
import time

from prediction import pipeline
from prediction.games import generate_games, make_game
from prediction.io_utils import now, read_json, write_json

METHODS = ('raw_logistic', 'combined_logistic_both', 'combined_mlp_both')
TARGETS = ('action0', 'cooperation', 'coordination')
MIN_IMPROVEMENT = .005
MIN_COVERAGE = .90
TERMINAL = ('complete_through_gate7', 'informative_negative')


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def gate_signal(scores, splits, require_interval=True):
    """Prespecified screening rule, not a multiplicity-adjusted discovery claim."""
    contrasts, qualifying = [], []
    for row in scores.get('comparisons_to_pair', []):
        if (row.get('baseline') != 'pair' or row.get('method') not in METHODS or
                row.get('target') not in TARGETS or row.get('split') not in splits):
            continue
        contrasts.append(row)
        point = row.get('improvement', {}).get('event_brier')
        lower = row.get('intervals', {}).get('event_brier', {}).get('lower')
        if (isinstance(point, (float, int)) and math.isfinite(point) and point >= MIN_IMPROVEMENT
                and (not require_interval or isinstance(lower, (float, int)) and math.isfinite(lower) and lower > 0)):
            qualifying.append(row)
    return dict(passed=bool(qualifying), qualifying=qualifying, contrasts=contrasts,
                criterion=dict(methods=list(METHODS), targets=list(TARGETS), splits=list(splits),
                               baseline='ordered focal/opponent context', event_brier_improvement_min=MIN_IMPROVEMENT,
                               require_paired_interval_lower_above_zero=require_interval),
                interpretation='Predeclared expansion screen across multiple contrasts; unadjusted intervals are descriptive.')


def expansion_decision(scores, splits):
    """Stop only when universal-target coverage and every upper bound exclude .005."""
    signal = gate_signal(scores, splits)
    observed = {(r['split'], r['method']) for r in signal['contrasts'] if r['target'] == 'action0'}
    required = {(split, method) for split in splits for method in METHODS}
    adequate = required <= observed
    def excludes_relevant_gain(row):
        upper = row.get('intervals', {}).get('event_brier', {}).get('upper')
        return isinstance(upper, (float, int)) and math.isfinite(upper) and upper < MIN_IMPROVEMENT
    decisive_negative = adequate and bool(signal['contrasts']) and all(
        excludes_relevant_gain(row) for row in signal['contrasts'])
    signal.update(proceed=not decisive_negative, decisive_negative=decisive_negative,
                  adequate_universal_comparisons=adequate,
                  missing_universal_comparisons=[list(key) for key in sorted(required-observed)],
                  decision='decisive_negative' if decisive_negative else
                           'positive_screen' if signal['passed'] else 'uncertainty_replication',
                  negative_criterion='All three methods have action0 comparisons in each declared split, and every available prespecified contrast has finite Brier upper interval < .005.')
    return signal


def new_prospective_games(training_groups):
    games = generate_games(seed=20260912, n=21)
    for game in games:
        game['id'] = 'prospective-'+game['id']
    overlap = set(training_groups) & {game['group_id'] for game in games}
    if overlap:
        raise ValueError('Prospective canonical game groups overlap training: '+str(sorted(overlap)))
    return games


def control_games(pilot_games):
    bases = pilot_games[:7]
    if len(bases) != 7 or len({game['family'] for game in bases}) != 7:
        raise ValueError('First seven pilot games must cover seven distinct families')
    games = []
    for base in bases:
        values = [base['payoffs'][key] for key in ('R', 'S', 'T', 'P')]
        for variant in ('scale3', 'offset10', 'abstract_text'):
            changed = ([round(v*3, 2) for v in values] if variant == 'scale3' else
                       [round(v+10, 2) for v in values] if variant == 'offset10' else values)
            game = make_game(f"controls-{variant}-{base['id']}", *changed,
                             source_game_id=base['id'], source_group_id=base['group_id'],
                             control_variant=variant)
            if game['group_id'] != base['group_id'] or game['family'] != base['family']:
                raise ValueError('Affine control changed the source game structure')
            games.append(game)
    return games


def stage_manifest(primary, stage, games, created):
    """Copy the exact frozen player protocol/source; each game has two label swaps."""
    budget = {'prospective': 250., 'controls': 200.}[stage]
    if len(primary['models']) != 4:
        raise ValueError('The continuation requires the fixed four-player roster')
    episodes = []
    for game in games:
        representation = 'text' if game.get('control_variant') == 'abstract_text' else 'matrix'
        for pair in combinations_with_replacement(sorted(primary['models']), 2):
            for trial in range(2):
                episodes.append(dict(id=f"{game['id']}--{pair[0]}--{pair[1]}--{representation}--t{trial}",
                                     game_id=game['id'], models=list(pair), trial_id=trial,
                                     representation=representation, swap=bool(trial % 2)))
    random.Random(20260912).shuffle(episodes)
    value = {key: deepcopy(primary[key]) for key in ('models', 'protocol', 'sources', 'source_root', 'ledger')}
    value.update(stage=stage, created=created, games=deepcopy(games), episodes=episodes, stage_budget_usd=budget)
    return value


def immutable_json(path, value):
    """Idempotent logical snapshot, never replace an existing artifact."""
    path = Path(path)
    if path.exists():
        if read_json(path) != value:
            raise ValueError('Existing immutable artifact differs: '+str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def step_contract(arguments):
    contract = pipeline.command_contract(arguments)
    for source in ('after_matrix.py', 'pipeline.py', 'controls_analysis.py'):
        path = pipeline.ROOT/'prediction'/source
        if path.exists():
            contract['source_hashes'][str(path)] = file_hash(path)
    for index, argument in enumerate(arguments[:-1]):
        if argument in ('--pilot-records', '--controls-records', '--controls-manifest'):
            path = Path(arguments[index+1]).resolve()
            contract['input_hashes'][str(path)] = file_hash(path)
    return contract


def checked_step(root, name, arguments, outputs):
    """Never retry a partial step or trust an output without its completed hash."""
    marker = root/'steps'/('after-'+name+'.json')
    outputs = [Path(path) for path in outputs]
    contract = step_contract(arguments)
    if marker.exists():
        saved = read_json(marker)
        if saved.get('status') != 'complete':
            raise RuntimeError('Interrupted/failed step requires explicit checkpoint audit: '+name)
        if saved['command'] != arguments:
            raise ValueError('Completed step command changed: '+name)
        if saved.get('contract') != contract:
            raise ValueError('Completed step inputs or computational sources changed: '+name)
        if not {str(path) for path in outputs} <= set(saved['output_sha256']):
            raise ValueError('Completed step declared outputs changed: '+name)
        actual = {path: file_hash(path) for path in saved['output_sha256']}
        if actual != saved['output_sha256']:
            raise ValueError('Completed step outputs changed: '+name)
        return
    if any(path.exists() for path in outputs):
        raise FileExistsError('Unmarked output already exists for step '+name)
    log_path = root/'logs'/('after-'+name+'.log')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = now()
    write_json(marker, dict(status='running', started=started, command=arguments, contract=contract))
    try:
        with log_path.open('a') as log:
            result = subprocess.run([pipeline.PYTHON, '-B', *arguments], cwd=pipeline.ROOT,
                                    env=pipeline.ENV, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'{name} returned {result.returncode}; see {log_path}')
        hashes = {str(path): file_hash(path) for path in outputs}
        hashes.update(pipeline.command_outputs(arguments))
    except Exception as exc:
        write_json(marker, dict(status='error', started=started, finished=now(), command=arguments,
                                contract=contract, error=type(exc).__name__+': '+str(exc)))
        raise
    write_json(marker, dict(status='complete', started=started, finished=now(), command=arguments,
                            contract=contract, output_sha256=hashes))


def safe_reporting(root):
    """Make rendering best effort, including calls inside pipeline.wait_stages."""
    from prediction import report
    original = report.render
    def guarded(*args, **kwargs):
        try:
            return original(*args, **kwargs)
        except Exception as exc:
            path = root/'logs'/'after-report-warnings.jsonl'
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('a') as handle:
                handle.write(json.dumps(dict(time=now(), error=type(exc).__name__+': '+str(exc)))+'\n')
    report.render = guarded
    return guarded


def update_state(root, phase, **extra):
    item = dict(status='running', phase=phase, updated=now(), driver='after_matrix', **extra)
    write_json(root/'after-matrix-status.json', item)
    write_json(root/'pipeline-status.json', item)


def record_gate(root, key, number, decision, reason, **extra):
    value = read_json(root/'gates.json')
    comparable = dict(continuation_key=key, gate=number, decision=decision, reason=reason, **extra)
    previous = [item for item in value['decisions'] if item.get('continuation_key') == key]
    if previous:
        if len(previous) != 1 or {k: v for k, v in previous[0].items() if k != 'time'} != comparable:
            raise ValueError('Continuation gate decision changed: '+key)
        return
    value['decisions'].append(dict(time=now(), **comparable))
    value['updated'] = now()
    write_json(root/'gates.json', value)


def finish(root, status, reason, **extra):
    item = dict(status=status, phase=status, updated=now(), driver='after_matrix', reason=reason,
                gate8_run=False, further_paid_expansion=False, **extra)
    write_json(root/'after-matrix-status.json', item)
    write_json(root/'pipeline-status.json', item)


def await_matrix(root, poll_seconds=30):
    while True:
        item = read_json(root/'pipeline-status.json') if (root/'pipeline-status.json').exists() else {}
        status, phase = item.get('status', ''), item.get('phase', '')
        if status == 'error' or status.startswith('stopped') or status in TERMINAL:
            return False
        if phase == 'awaiting_prospective_stage':
            return True
        if item.get('driver') == 'after_matrix' and status == 'running':
            return True  # Subsequent immutable steps verify a resumable continuation.
        time.sleep(poll_seconds)


def validate_training(root, primary):
    for relative, error_key in (('primary-pilot/final-collection/summary.json', 'integrity_errors'),
                                ('development/collected/summary.json', 'errors')):
        summary = read_json(root/relative)
        if summary[error_key] or summary['complete_episodes']/summary['planned_episodes'] < MIN_COVERAGE:
            raise ValueError('Training collection lacks required integrity/.90 coverage: '+relative)
    development = read_json(root/'development'/'manifest.json')
    for key in ('models', 'protocol', 'sources', 'source_root', 'ledger'):
        if primary[key] != development[key]:
            raise ValueError('Training stages differ in frozen '+key)
    if Path(primary['source_root']).resolve() != (root/'source').resolve():
        raise ValueError('Unexpected frozen source root')
    if Path(primary['ledger']).resolve() != (root/'budget.sqlite').resolve() or not (root/'budget.sqlite').is_file():
        raise ValueError('Continuation must use the existing root $3,000 ledger')
    for relative, expected in primary['sources'].items():
        if file_hash(root/'source'/relative) != expected:
            raise ValueError('Frozen player source changed: '+relative)
    # Generator/features must agree with the game definitions the player will see.
    for relative in ('prediction/games.py', 'prediction/measurements.py'):
        if file_hash(pipeline.ROOT/relative) != primary['sources'][relative]:
            raise ValueError('Current '+relative+' differs from frozen collection source')
    roster = list(primary['models'])
    def one(part):
        matches = [name for name in roster if part.lower() in name.lower()]
        if len(matches) != 1:
            raise ValueError('Expected exactly one primary player matching '+part)
        return matches[0]
    kimi, unknown = one('kimi'), one('gpt-oss')
    one('haiku'); one('qwen')
    rows = read_json(root/'training-records.json')
    if not rows or any(r['model'] not in roster or r['opponent'] not in roster for r in rows):
        raise ValueError('Training snapshot does not match the fixed player roster')
    keys = [(r['episode_id'], r['player_index']) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate focal rows in training snapshot')
    return rows, kimi, unknown


def save_stage(root, primary, name, games):
    path = root/name/'manifest.json'
    created = read_json(path)['created'] if path.exists() else now()
    immutable_json(path, stage_manifest(primary, name, games, created))
    return path


def prepare_metadata(root, stage):
    folder = root/stage
    path = folder/'metadata.json'
    checked_step(root, stage+'-metadata', ['-m', 'prediction.prospective', 'build-rows', '--manifest',
                 str(folder/'manifest.json'), '--output', str(path)], [path, path.with_suffix('.manifest.json')])
    return path


def fit_and_freeze(root, name, training, metadata):
    folder = root/'prospective'/'numerical'/name
    artifact, forecasts = folder/'fit.pkl', folder/'forecasts.jsonl'
    checked_step(root, 'fit-'+name, ['-m', 'prediction.modeling', 'fit', '--input', str(training),
                 '--artifact', str(artifact)], [artifact, artifact.with_suffix('.pkl.json')])
    checked_step(root, 'forecast-'+name, ['-m', 'prediction.modeling', 'forecast', '--artifact', str(artifact),
                 '--input', str(metadata), '--output', str(forecasts)],
                 [forecasts, forecasts.with_suffix('.manifest.json')])
    return artifact, forecasts


def freeze_before_launch(root, stage, files):
    """Freeze completed outputs while no episode has begun; verify on resume."""
    folder = root/stage
    path = folder/'forecast-freeze.json'
    hashes = {str(Path(p).resolve()): file_hash(p) for p in files}
    if path.exists():
        if read_json(path)['sha256'] != hashes:
            raise ValueError('Pre-rollout frozen artifacts changed for '+stage)
        return
    if (folder/'process.json').exists() or (folder/'episodes').exists() or (folder/'status.json').exists():
        raise ValueError('Cannot first freeze forecasts after player stage has begun')
    immutable_json(path, dict(created_utc=now(), stage=stage, sha256=hashes,
                              ordering='All listed forecasts completed before launch; actual trace timestamps audited at scoring.'))


def collect_stage(root, stage):
    folder = root/stage
    if (folder/'process.json').exists() and not (folder/'status.json').exists():
        # Launch may have returned just before the runner wrote its first status.
        process = read_json(folder/'process.json')
        if not pipeline.alive(process['pid']):
            raise RuntimeError('Stage process exited without status: '+stage)
    else:
        pipeline.launch(root, stage)
    pipeline.wait_stages(root, (stage,))
    records = folder/'collected'/'records.json'
    checked_step(root, stage+'-collect', [str(root/'source/prediction/study.py'), 'collect', '--stage-root', str(folder)],
                 [records, folder/'collected'/'summary.json', folder/'collected'/'provenance.json'])
    summary = read_json(folder/'collected'/'summary.json')
    if summary['errors']:
        raise ValueError('Integrity errors in '+stage+' collected traces; no additional paid expansion')
    return records, summary


def score_stage(root, stage, name, forecasts, records, llm=None, focus_pair=None, focus_model=None):
    folder = root/stage
    output = folder/name
    split = ('prospective_pair' if focus_pair else 'prospective_model' if focus_model else
             'prospective_controls' if stage == 'controls' else 'prospective')
    args = ['-m', 'prediction.prospective', 'score', '--forecasts', str(forecasts), '--records', str(records),
            '--out', str(output), '--stage-root', str(folder), '--split', split, '--bootstrap', '500']
    if llm:
        args += ['--llm-forecasts', str(llm)]
    if focus_pair:
        args += ['--focus-pair', focus_pair]
    if focus_model:
        args += ['--focus-model', focus_model]
    checked_step(root, stage+'-'+name.replace('/', '-'), args,
                 [output/file for file in ('scores.json', 'coverage.json', 'audit.json', 'joined-predictions.jsonl')])
    audit, coverage, scores = [read_json(output/file) for file in ('audit.json', 'coverage.json', 'scores.json')]
    if not audit['prospective_verified']:
        raise ValueError('Prospective timing/hash audit failed: '+str(audit['issues']))
    return dict(audit=audit, coverage=coverage, comparisons_to_pair=scores['comparisons_to_pair'],
                scores_sha256=file_hash(output/'scores.json'))


def continuation(root):
    primary = read_json(root/'primary-pilot-manifest.json')
    training, kimi, unknown = validate_training(root, primary)
    pair = '|'.join(sorted((kimi, unknown)))
    plan = dict(version='after-matrix-v1', training_sha256=file_hash(root/'training-records.json'),
                primary_manifest_sha256=file_hash(root/'primary-pilot-manifest.json'),
                retrospective_scores_sha256=file_hash(root/'development/evaluation/scores.json'),
                source_sha256={name: file_hash(pipeline.ROOT/'prediction'/name) for name in
                               ('after_matrix.py', 'pipeline.py', 'modeling.py', 'analysis.py', 'prospective.py',
                                'llm_forecast.py', 'controls_analysis.py', 'diagnostics.py', 'io_utils.py')},
                retrospective_screen=gate_signal({}, ('family', 'random_group'))['criterion'],
                retrospective_stopping_rule=expansion_decision({}, ('family', 'random_group'))['negative_criterion'],
                prospective_screen=gate_signal({}, ('prospective',), False)['criterion'],
                minimum_completed_episode_coverage=MIN_COVERAGE,
                prospective_seed=20260912, prospective_games=21, trials=2, pair_holdout=pair,
                model_holdout=unknown, player_protocol=primary['protocol'], global_budget_usd=3000.,
                stage_budgets_usd=dict(prospective=250., controls=200., llm_forecasts=150.),
                controls=dict(source='first seven primary pilot games', variants=['scale3', 'offset10', 'abstract_text']),
                gate8=False)
    immutable_json(root/'after-matrix-plan.json', plan)
    label_output = root/'primary-pilot'/'label-analysis'
    checked_step(root, 'label-sensitivity', ['-m', 'prediction.controls_analysis', '--pilot-records',
                 str(root/'primary-pilot/final-records.json'), '--out', str(label_output), '--bootstrap', '500'],
                 [label_output/'controls-analysis.json', label_output/'derivation.json'])
    signal = expansion_decision(read_json(root/'development/evaluation/scores.json'), ('family', 'random_group'))
    immutable_json(root/'after-matrix-screen.json', signal)
    if not signal['proceed']:
        record_gate(root, 'expansion-screen', 5, 'informative negative',
                    'Every available prespecified contrast excludes a .005 Brier gain at its upper interval, with all universal-target method/split comparisons present; halt additional paid work.', screen=signal)
        finish(root, 'informative_negative', 'Declared interval screen excludes the prespecified useful gain across adequately represented retrospective comparisons.')
        return
    record_gate(root, 'expansion-screen', 5, 'proceed',
                'Run the single fixed prospective cohort after positive screening or inconclusive retrospective evidence. No result-driven enlargement of this cohort is permitted.', screen=signal)
    update_state(root, 'after_matrix_freezing_prospective')
    groups = {r['group_id'] for r in training}
    manifest = save_stage(root, primary, 'prospective', new_prospective_games(groups))
    prospective = root/'prospective'
    if not (prospective/'forecast-freeze.json').exists() and any(
            (prospective/name).exists() for name in ('episodes', 'process.json', 'status.json')):
        raise ValueError('An existing prospective player stage lacks a prior forecast freeze')
    metadata = prepare_metadata(root, 'prospective')
    snapshots = {}
    predicates = dict(full=lambda r: True,
                      excluded_pair=lambda r: '|'.join(sorted((r['model'], r['opponent']))) != pair,
                      excluded_model=lambda r: unknown not in (r['model'], r['opponent']))
    for name, predicate in predicates.items():
        selected = [r for r in training if predicate(r)]
        if not selected:
            raise ValueError('Empty training snapshot for '+name)
        path = root/'prospective'/'training'/(name+'.json')
        immutable_json(path, selected)
        episodes = {r['episode_id'] for r in selected}
        if any(sum(r['episode_id'] == episode for r in selected) != 2 for episode in episodes):
            raise ValueError('Training filter split an episode')
        immutable_json(path.with_suffix('.audit.json'), dict(source_sha256=plan['training_sha256'],
                       filtered_sha256=file_hash(path), filter=name, held_pair=pair if name == 'excluded_pair' else None,
                       held_model=unknown if name == 'excluded_model' else None, rows=len(selected), episodes=len(episodes),
                       excluded_rows=len(training)-len(selected), game_groups=len({r['group_id'] for r in selected})))
        snapshots[name] = path
    fitted = {name: fit_and_freeze(root, name, path, metadata) for name, path in snapshots.items()}
    update_state(root, 'after_matrix_llm_forecasts')
    llm_root = root/'prospective'/'llm-forecasts'
    llm = llm_root/'forecasts.jsonl'
    if llm_root.exists() and not (root/'steps'/'after-llm-forecasts.json').exists():
        raise ValueError('Unmarked existing LLM run requires explicit checkpoint audit before any calls')
    checked_step(root, 'llm-forecasts', ['-m', 'prediction.llm_forecast', '--games', str(manifest),
                 '--players', str(manifest), '--training-records', str(snapshots['full']), '--modes',
                 'zero_shot', 'few_shot', 'game_theory', '--forecaster', kimi,
                 '--ledger', str(root/'budget.sqlite'), '--out', str(llm_root), '--stage-budget', '150', '--workers', '8'],
                 [llm, llm_root/'inputs.json', llm_root/'status.json'])
    llm_status = read_json(llm_root/'status.json')
    if llm_status.get('status') not in ('complete', 'finished_with_errors') or llm_status.get('forecast_sha256') != file_hash(llm):
        raise ValueError('LLM forecasts did not reach an intact terminal export')
    freeze_files = [manifest, metadata, llm, llm_root/'inputs.json', llm_root/'status.json']
    for artifact, forecasts in fitted.values():
        freeze_files += [artifact, artifact.with_suffix('.pkl.json'), forecasts, forecasts.with_suffix('.manifest.json')]
    freeze_before_launch(root, 'prospective', freeze_files)
    update_state(root, 'after_matrix_prospective_rollout')
    records, collection = collect_stage(root, 'prospective')
    update_state(root, 'after_matrix_prospective_scoring')
    numerical = score_stage(root, 'prospective', 'evaluation-numerical', fitted['full'][1], records)
    full = score_stage(root, 'prospective', 'evaluation', fitted['full'][1], records, llm=llm)
    held_pair = score_stage(root, 'prospective', 'evaluation-pair', fitted['excluded_pair'][1], records, focus_pair=pair)
    held_model = score_stage(root, 'prospective', 'evaluation-model', fitted['excluded_model'][1], records, focus_model=unknown)
    coverage = collection['complete_episodes']/collection['planned_episodes']
    if coverage < MIN_COVERAGE:
        record_gate(root, 'prospective-coverage', 6, 'technical stop',
                    'Prospective scoring retained partial outcomes, but completion coverage is below .90; no scientific/control expansion decision.',
                    coverage=coverage, collection=collection)
        raise RuntimeError('Prospective completion coverage below .90; partial scores retained')
    record_gate(root, 'prospective-games', 6, 'prospective evaluation complete',
                'All numerical and prompted forecasts were frozen before new-game player episodes. Missing outcomes and LLM failures remain explicit.',
                collection=collection, full=full, numerical=numerical, freeze=read_json(root/'prospective/forecast-freeze.json'))
    record_gate(root, 'prospective-identities', 7, 'prospective evaluation complete',
                'Additional frozen fits excluded the unordered test pair or every test-model interaction; both roles were purged. Unknown identities use declared fallbacks.',
                pair=held_pair, model=held_model)
    positive = gate_signal(numerical, ('prospective',), require_interval=False)
    immutable_json(root/'prospective'/'controls-screen.json', positive)
    if not positive['passed']:
        evidence = expansion_decision(numerical, ('prospective',))
        decisive = evidence['decisive_negative']
        record_gate(root, 'controls-screen', 6, 'informative negative' if decisive else 'inconclusive / controls unsupported',
                    'No prespecified numerical predictor met the .005 point-gain control trigger. Upper intervals determine whether useful gains are excluded; failure to trigger alone is not evidence of absence.',
                    screen=positive, evidence=evidence)
        finish(root, 'informative_negative' if decisive else 'complete_through_gate7',
               'Prospective game/pair/model and LLM comparisons completed; bounded controls skipped.',
               evidence='useful gain excluded by declared interval screen' if decisive else 'inconclusive / controls unsupported')
        return
    record_gate(root, 'controls-screen', 6, 'proceed',
                'A prespecified numerical predictor improved ordered context by at least .005 Brier prospectively. Paired intervals are reported without requiring their lower bound above zero for this bounded control screen.', screen=positive)
    update_state(root, 'after_matrix_freezing_controls')
    control_manifest = save_stage(root, primary, 'controls', control_games(primary['games']))
    control_metadata = prepare_metadata(root, 'controls')
    artifact = fitted['full'][0]
    control_forecasts = root/'controls'/'forecasts.jsonl'
    checked_step(root, 'controls-forecast', ['-m', 'prediction.modeling', 'forecast', '--artifact', str(artifact),
                 '--input', str(control_metadata), '--output', str(control_forecasts)],
                 [control_forecasts, control_forecasts.with_suffix('.manifest.json')])
    freeze_before_launch(root, 'controls', [control_manifest, control_metadata, artifact,
                         control_forecasts, control_forecasts.with_suffix('.manifest.json')])
    update_state(root, 'after_matrix_controls_rollout')
    control_records, control_collection = collect_stage(root, 'controls')
    controls = score_stage(root, 'controls', 'evaluation', control_forecasts, control_records)
    sensitivity = root/'controls'/'sensitivity'
    checked_step(root, 'control-sensitivity', ['-m', 'prediction.controls_analysis', '--pilot-records',
                 str(root/'primary-pilot/final-records.json'), '--controls-records', str(control_records),
                 '--controls-manifest', str(control_manifest), '--out', str(sensitivity), '--bootstrap', '500'],
                 [sensitivity/'controls-analysis.json', sensitivity/'derivation.json'])
    control_coverage = control_collection['complete_episodes']/control_collection['planned_episodes']
    if control_coverage < MIN_COVERAGE:
        record_gate(root, 'controls-coverage', 6, 'technical stop',
                    'Control scoring retained partial outcomes, but completion coverage is below .90.',
                    coverage=control_coverage, collection=control_collection)
        raise RuntimeError('Control completion coverage below .90; partial scores retained')
    record_gate(root, 'affine-presentation-controls', 6, 'control evaluation complete',
                'Seven source games each received scale x3, offset +10 and abstract-text controls, preserving canonical shapes. Original training fit remained frozen; no Gate8 adaptation or narratives.',
                collection=control_collection, evaluation=controls, freeze=read_json(root/'controls/forecast-freeze.json'))
    finish(root, 'complete_through_gate7', 'Bounded prospective games, joint identity holdouts, prompted baselines and affine/presentation controls completed; Gate8 not run.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, required=True)
    args = parser.parse_args(argv)
    root = args.run_root.resolve()
    if not root.is_relative_to(Path('/shared/allie')) or not root.is_dir():
        parser.error('run-root must be an existing directory under /shared/allie')
    with (root/'after-matrix.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        render = safe_reporting(root)
        try:
            if await_matrix(root):
                continuation(root)
        except Exception as exc:
            item = dict(status='error', phase='after_matrix_error', driver='after_matrix', updated=now(),
                        error=type(exc).__name__+': '+str(exc), additional_paid_expansion=False,
                        resume='Explicit checkpoint audit required; completed artifacts must remain unchanged.')
            write_json(root/'after-matrix-status.json', item)
            write_json(root/'pipeline-status.json', item)
            raise
        finally:
            render(root, pipeline.ROOT/'prediction/REPORT.md')


if __name__ == '__main__':
    main()
