"""CPU-only supervisor for audited secondary analyses, independent of paid jobs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from prediction.io_utils import now, read_json, write_json

ROOT = Path(__file__).resolve().parents[1]
PYTHON = '/shared/allie/venvs/hole/bin/python'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR='/shared/allie/home/.codex/tmp',
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
           MPLCONFIGDIR='/shared/allie/home/.codex/tmp/matplotlib-prediction',
           JOBLIB_TEMP_FOLDER='/shared/allie/home/.codex/tmp/joblib-prediction')
SOURCE_NAMES = ('secondary_analysis.py', 'secondary_baselines.py', 'prospective.py', 'modeling.py',
                'analysis.py', 'games.py', 'io_utils.py')
TERMINAL = ('complete_through_gate7', 'informative_negative')
REQUIRED = ('scores.json', 'audit.json', 'joined-predictions.jsonl')


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            digest.update(block)
    return digest.hexdigest()


def snapshot(paths):
    return {str(Path(path).resolve()): file_hash(path) for path in sorted(set(map(Path, paths)))}


def unchanged(saved):
    for path, expected in saved.items():
        if not Path(path).is_file() or file_hash(path) != expected:
            raise ValueError('Audited input/source/artifact changed: '+path)


def _time(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Prospective evidence needs timezone-aware timestamps')
    return parsed.astimezone(timezone.utc)


def verified_evaluation(folder):
    """Independently recompute timestamp order, beyond trusting a saved true flag."""
    folder = Path(folder)
    audit = read_json(folder/'audit.json')
    if audit.get('prospective_verified') is not True or audit.get('issues') != []:
        raise ValueError('Evaluation is not supported by a clean prospective audit: '+str(folder))
    source_hashes = audit.get('source_sha256', {})
    if not source_hashes:
        raise ValueError('Evaluation audit lacks its source hashes')
    unchanged(source_hashes)
    starts = []
    for path in source_hashes:
        path = Path(path)
        if path.name in ('trace.json', 'progress.json', 'incomplete.json') and 'episodes' in path.parts:
            starts.append(_time(read_json(path)['started']))
    if not starts:
        raise ValueError('No actual trace timestamps in evaluation evidence')
    earliest = min(starts)
    if _time(audit['rollout_timing']['earliest_started_utc']) != earliest:
        raise ValueError('Saved rollout timing differs from audited trace bytes')
    if audit.get('effective_split', '').startswith('unverified_') or audit.get('requested_split') != audit.get('effective_split'):
        raise ValueError('Evaluation does not retain a verified requested split')
    evidence = []
    for source in audit.get('sources', []):
        if source.get('issues') != [] or any(source.get(field) is not True for field in
                                             ('hash_verified', 'input_identity_verified', 'precedes_rollouts')):
            raise ValueError('Source audit flags do not establish a prior intact forecast')
        path = Path(source['path']).resolve()
        if str(path) not in source_hashes:
            raise ValueError('Forecast source is absent from the audited source hash table')
        if source['kind'] == 'numerical':
            sidecar = path.with_suffix('.manifest.json')
            if str(sidecar) not in source_hashes:
                raise ValueError('Forecast creation manifest was not audited')
            manifest = read_json(sidecar)
            if manifest['forecast_sha256'] != file_hash(path):
                raise ValueError('Numerical forecast differs from its creation manifest')
            created = _time(manifest['created_utc'])
        elif source['kind'] == 'llm':
            status_path = path.parent/'status.json'
            if str(status_path) not in source_hashes:
                raise ValueError('LLM completion status was not audited')
            status = read_json(status_path)
            if status['forecast_sha256'] != file_hash(path):
                raise ValueError('LLM forecast differs from its terminal export hash')
            times = [_time(status['finished_utc'])]
            with path.open() as handle:
                for line in handle:
                    if line.strip():
                        row = json.loads(line)
                        if row.get('prediction') is not None:
                            times.append(_time(row['prediction_created_utc']))
            created = max(times)
        else:
            raise ValueError('Unknown audited forecast source kind')
        if created != _time(source['created_utc']) or created >= earliest:
            raise ValueError('Forecast completion does not precede actual target trace start')
        evidence.append(dict(path=str(path), created_utc=created.isoformat(), earliest_started_utc=earliest.isoformat()))
    if not evidence:
        raise ValueError('No verified forecast sources')
    return dict(prospective_verified=True, independently_checked_sources=evidence)


def files_in(folder):
    folder = Path(folder)
    return sorted(path for path in folder.rglob('*') if path.is_file()) if folder.exists() else []


def source_paths():
    return [ROOT/'prediction'/name for name in SOURCE_NAMES]


def completed_marker(path):
    path = Path(path)
    if not path.exists():
        return False
    item = read_json(path)
    if item.get('status') == 'complete':
        return True
    if item.get('status') in ('error', 'failed'):
        raise RuntimeError('Required upstream step failed: '+str(path))
    return False


def validate_upstream_markers(paths):
    for path in paths:
        item = read_json(path)
        if item.get('status') != 'complete':
            raise ValueError('Required upstream marker is not complete: '+str(path))
        hashes = item.get('output_hashes', item.get('output_sha256'))
        if not hashes:
            raise ValueError('Required upstream marker lacks completed output hashes: '+str(path))
        unchanged(hashes)


def ready_decision(ready, upstream, needs_freeze=False, freezer=None, skip_authorized=False):
    """Available CPU analyses remain runnable after the paid pipeline terminates."""
    if ready:
        return 'ready'
    if upstream == 'error' or upstream.startswith('stopped'):
        return 'upstream_error'
    if needs_freeze and freezer == 'error':
        return 'freezer_error'
    if upstream in TERMINAL:
        return 'skip_unavailable_terminal_stage' if skip_authorized else 'missing_required_terminal_output'
    return 'wait'


def can_skip_unrun_job(root, job):
    """Only a recorded no-expansion decision can excuse a truly unrun stage."""
    if job['kind'] == 'retrospective' or job.get('stage') not in ('prospective', 'controls'):
        return False
    stage = job['stage']
    if any((root/stage/name).exists() for name in ('process.json', 'status.json', 'episodes')):
        return False
    if any((root/'steps').glob('after-'+stage+'-evaluation*.json')):
        return False
    gates_path = root/'gates.json'
    if not gates_path.is_file():
        return False
    gates = {item.get('continuation_key'): item for item in read_json(gates_path).get('decisions', [])}
    expansion = gates.get('expansion-screen', {})
    no_cohort = (expansion.get('gate') == 5 and expansion.get('decision') == 'informative negative' and
                 expansion.get('screen', {}).get('decisive_negative') is True)
    if stage == 'prospective':
        return no_cohort
    controls = gates.get('controls-screen')
    if controls is not None:
        return (controls.get('gate') == 6 and controls.get('decision') in
                ('informative negative', 'inconclusive / controls unsupported') and
                controls.get('screen', {}).get('passed') is False)
    return no_cohort


def job_specs(root, bootstrap=500):
    secondary = root/'secondary-baselines'
    plan = read_json(secondary/'plan.json') if (secondary/'plan.json').exists() else {}
    jobs = []
    for name, records, evaluation in (
            ('pilot', root/'primary-pilot/final-records.json', root/'pilot/evaluation'),
            ('development', root/'training-records.json', root/'development/evaluation')):
        output = root/'independent-analysis'/(name+'-secondary')
        marker = root/'steps'/(name+'-numerical.json')
        inputs = [records]+[evaluation/file for file in ('run_config.json', 'folds.json', 'predictions.jsonl')]
        jobs.append(dict(name=name+'-retrospective', kind='retrospective', output=output, evaluation=evaluation,
                         readiness=inputs+[marker], markers=[marker], base_inputs=inputs,
                         arguments=['-m', 'prediction.secondary_baselines', 'retrospective', '--records', str(records),
                                    '--evaluation', str(evaluation), '--out', str(output), '--bootstrap', str(bootstrap)],
                         classification='secondary_post_pilot_retrospective_sensitivity'))
    for fit, stage, primary_name, split, focus in (
            ('full', 'prospective', 'evaluation', 'prospective', None),
            ('excluded_pair', 'prospective', 'evaluation-pair', 'prospective_pair', 'pair'),
            ('excluded_model', 'prospective', 'evaluation-model', 'prospective_model', 'model'),
            ('full', 'controls', 'evaluation', 'prospective_controls', None)):
        folder = secondary/fit
        primary = root/stage/primary_name
        primary_marker = root/'steps'/('after-'+stage+'-'+primary_name+'.json')
        forecast = folder/(stage+'.jsonl')
        records = root/stage/'collected/records.json'
        output = folder/(stage+'-evaluation')
        args = ['-m', 'prediction.prospective', 'score', '--forecasts', str(forecast), '--records', str(records),
                '--stage-root', str(root/stage), '--split', split, '--out', str(output), '--bootstrap', str(bootstrap)]
        if focus:
            value = plan.get('pair_exclusion' if focus == 'pair' else 'model_exclusion')
            args += ['--focus-'+focus, value or '<awaiting-frozen-exclusion-plan>']
        base = [forecast, forecast.with_suffix('.manifest.json'), folder/'fit.json', folder/'training.json',
                folder/'training-audit.json', secondary/'plan.json', secondary/'forecast-freeze.json', records,
                root/stage/'manifest.json', root/stage/'metadata.json']
        name = fit+'-'+stage
        jobs.append(dict(name=name+'-score', kind='score', output=output, stage=stage, primary=primary,
                         readiness=base+[primary/'audit.json', primary_marker], markers=[primary_marker],
                         base_inputs=base, arguments=args, needs_freeze=True,
                         classification='secondary_post_pilot_prospective_evaluation'))
        comparison = folder/(stage+'-comparison')
        own_marker = root/'steps'/('secondary-analysis-'+name+'-score.json')
        jobs.append(dict(name=name+'-compare', kind='compare', output=comparison, stage=stage,
                         depends_on=name+'-score',
                         primary=primary, secondary=output, readiness=[primary/'audit.json', output/'supervisor-audit.json', own_marker, primary_marker],
                         markers=[primary_marker, own_marker], base_inputs=[secondary/'plan.json', secondary/'forecast-freeze.json'],
                         arguments=['-m', 'prediction.secondary_baselines', 'compare', '--primary-evaluation', str(primary),
                                    '--secondary-evaluation', str(output), '--out', str(comparison), '--bootstrap', str(bootstrap)],
                         needs_freeze=True, classification='secondary_post_pilot_prospective_comparison'))
    return jobs


def input_paths(root, job):
    paths = list(job['base_inputs'])+job['markers']+source_paths()
    if job['kind'] == 'retrospective':
        paths += files_in(job['evaluation'])
    else:
        freeze_path = root/'secondary-baselines/forecast-freeze.json'
        evidence = read_json(freeze_path)
        paths += [Path(path) for path in evidence['forecasts_sha256']]
        plan_path = root/'secondary-baselines/plan.json'
        if file_hash(plan_path) != evidence['plan_sha256']:
            raise ValueError('Frozen secondary plan changed')
        unchanged(evidence['forecasts_sha256'])
        if job['kind'] == 'score':
            paths += files_in(root/job['stage']/'collected')
            paths += [path for path in files_in(root/job['stage']/'episodes')
                      if path.name in ('trace.json', 'progress.json', 'incomplete.json')]
        folders = [job['primary']]+([job['secondary']] if job['kind'] == 'compare' else [])
        for folder in folders:
            paths += files_in(folder)
            audit = read_json(folder/'audit.json')
            paths += [Path(path) for path in audit.get('source_sha256', {})]
    return sorted(set(paths))


def validate_outputs(job):
    output = job['output']
    for name in REQUIRED:
        if not (output/name).is_file():
            raise ValueError('Missing completed analysis output: '+str(output/name))
    audit = read_json(output/'audit.json')
    if job['kind'] == 'score':
        return verified_evaluation(output)
    if audit.get('classification') != job['classification']:
        raise ValueError('Analysis classification differs from the declared job')
    if job['kind'] == 'compare' and audit.get('prospective_verified') is not True:
        raise ValueError('Secondary comparison did not preserve verified prospectivity')
    if not (output/'secondary-comparisons.json').is_file():
        raise ValueError('Missing secondary baseline contrasts')
    return dict(classification=audit['classification'], prospective_verified=audit.get('prospective_verified', False))


def run_step(root, job):
    """Before/after byte guards make read-before-hash helper outputs unreportable."""
    arguments = job['arguments']
    if arguments[:3] not in (['-m', 'prediction.secondary_baselines', 'retrospective'],
                             ['-m', 'prediction.secondary_baselines', 'compare'],
                             ['-m', 'prediction.prospective', 'score']):
        raise ValueError('Supervisor only permits the three CPU analysis commands')
    marker = root/'steps'/('secondary-analysis-'+job['name']+'.json')
    paths = input_paths(root, job)
    initial = snapshot(paths)
    contract = dict(command=arguments, classification=job['classification'], initial_sha256=initial)
    if marker.exists():
        saved = read_json(marker)
        if saved.get('status') != 'complete':
            raise RuntimeError('Interrupted/error secondary step needs explicit checkpoint audit: '+job['name'])
        if saved.get('contract') != contract:
            raise ValueError('Completed secondary command/input/source snapshot changed')
        unchanged(saved['output_sha256'])
        if read_json(job['output']/'supervisor-audit.json').get('status') != 'verified':
            raise ValueError('Completed secondary output lacks its valid supervisor audit')
        return
    if job['output'].exists():
        raise FileExistsError('Unmarked secondary output already exists: '+str(job['output']))
    validate_upstream_markers(job['markers'])
    prior_evidence = []
    if job['kind'] != 'retrospective':
        prior_evidence = [verified_evaluation(job['primary'])]
        if job['kind'] == 'compare':
            prior_evidence.append(verified_evaluation(job['secondary']))
    # Recheck after validation, before launching a helper that reads its inputs.
    unchanged(initial)
    started = now()
    write_json(marker, dict(status='running', started=started, api_calls=False, contract=contract))
    log = root/'logs'/('secondary-analysis-'+job['name']+'.log')
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        with log.open('a') as handle:
            result = subprocess.run([PYTHON, '-B', *arguments], cwd=ROOT, env=ENV,
                                    stdout=handle, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'Secondary command returned {result.returncode}; see {log}')
        if {str(path.resolve()) for path in input_paths(root, job)} != set(initial):
            raise ValueError('Analysis input/source directory membership changed during execution')
        unchanged(initial)
        evidence = validate_outputs(job)
        unchanged(initial)
        scientific_outputs = snapshot(files_in(job['output']))
        wrapper = job['output']/'supervisor-audit.json'
        with wrapper.open('x') as handle:
            json.dump(dict(status='verified', classification=job['classification'], started_utc=started,
                finished_utc=now(), api_calls=False, original_methods_and_gate_criteria_unchanged=True,
                initial_sha256=initial, final_recheck='Every input/source/artifact hash and input path membership matched after computation.',
                prospective_checks=prior_evidence, output_validation=evidence, output_sha256=scientific_outputs),
                handle, indent=2, allow_nan=False)
            handle.write('\n')
        output_hashes = dict(scientific_outputs, **{str(wrapper.resolve()): file_hash(wrapper)})
        write_json(marker, dict(status='complete', started=started, finished=now(), api_calls=False,
                                contract=contract, output_sha256=output_hashes))
    except Exception as exc:
        write_json(marker, dict(status='error', started=started, finished=now(), api_calls=False, contract=contract,
                                error=type(exc).__name__+': '+str(exc), report_eligible=False))
        raise


def render_safely(root):
    try:
        from prediction.report import render
        render(root, ROOT/'prediction/REPORT.md')
    except Exception as exc:
        path = root/'logs/secondary-analysis-report-warnings.jsonl'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a') as handle:
            handle.write(json.dumps(dict(time=now(), error=type(exc).__name__+': '+str(exc)))+'\n')


def supervise(root, bootstrap=500, poll_seconds=20):
    status_path = root/'independent-analysis/secondary-status.json'
    saved = read_json(status_path) if status_path.exists() else {}
    states = saved.get('jobs', {})
    # Completed jobs are checked again on every process resume, not silently trusted.
    resumed = set()
    while True:
        upstream = read_json(root/'pipeline-status.json').get('status', '') if (root/'pipeline-status.json').exists() else ''
        freezer = read_json(root/'secondary-baselines/status.json').get('status', '') if (root/'secondary-baselines/status.json').exists() else ''
        progress, waiting = False, []
        for job in job_specs(root, bootstrap):
            name = job['name']
            previous = states.get(name, {})
            if previous.get('status') == 'error':
                continue
            if previous.get('status') in ('complete', 'skipped') and name in resumed:
                continue
            try:
                dependency = states.get(job.get('depends_on'), {})
                if dependency.get('status') == 'error':
                    raise RuntimeError('Required secondary scoring job failed: '+job['depends_on'])
                ready = all(Path(path).is_file() for path in job['readiness']) and all(completed_marker(path) for path in job['markers'])
                skip_authorized = can_skip_unrun_job(root, job) if upstream in TERMINAL and not ready else False
                choice = ready_decision(ready, upstream, job.get('needs_freeze', False), freezer, skip_authorized)
                if previous.get('status') == 'complete' and choice != 'ready':
                    raise ValueError('Completed analysis prerequisites are now missing')
                if choice == 'ready':
                    states[name] = dict(status='running', started=now(), output=str(job['output']))
                    write_json(status_path, dict(status='running', updated=now(), api_calls=False, jobs=states))
                    render_safely(root)
                    run_step(root, job)
                    states[name] = dict(status='complete', finished=now(), output=str(job['output']), report_eligible=True)
                    resumed.add(name); progress = True
                elif choice == 'wait':
                    waiting.append(name)
                    states[name] = dict(status='waiting', output=str(job['output']))
                elif choice == 'skip_unavailable_terminal_stage':
                    states[name] = dict(status='skipped', reason='Recorded gate decision declined this conditional stage, and no player or primary scoring artifacts exist.',
                                        upstream_status=upstream, output=str(job['output']), report_eligible=False)
                    resumed.add(name)
                    progress = True
                else:
                    raise RuntimeError('Required unavailable result after '+choice+': '+upstream+' / '+freezer)
            except Exception as exc:
                states[name] = dict(status='error', finished=now(), output=str(job['output']), report_eligible=False,
                                    error=type(exc).__name__+': '+str(exc))
                progress = True
            write_json(status_path, dict(status='running', updated=now(), api_calls=False, jobs=states))
        if not waiting:
            terminal = 'error' if any(item['status'] == 'error' for item in states.values()) else (
                       'complete_with_skips' if any(item['status'] == 'skipped' for item in states.values()) else 'complete')
            write_json(status_path, dict(status=terminal, updated=now(), api_calls=False, jobs=states,
                                        paid_pipeline_unchanged=True, primary_terminal_status=upstream))
            render_safely(root)
            return
        write_json(status_path, dict(status='waiting', updated=now(), api_calls=False, jobs=states, waiting_for=waiting))
        render_safely(root)
        if not progress:
            time.sleep(poll_seconds)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--bootstrap', type=int, default=500)
    args = parser.parse_args(argv)
    root = args.run_root.resolve()
    if not root.is_relative_to(Path('/shared/allie')) or not root.is_dir():
        parser.error('run-root must be an existing directory under /shared/allie')
    if args.bootstrap < 0:
        parser.error('bootstrap must be nonnegative')
    with (root/'secondary-analysis.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            supervise(root, args.bootstrap)
        except Exception as exc:
            status_path = root/'independent-analysis/secondary-status.json'
            status = read_json(status_path) if status_path.exists() else {}
            write_json(status_path, dict(status, status='error', updated=now(), api_calls=False,
                error=type(exc).__name__+': '+str(exc), paid_pipeline_unchanged=True))
            render_safely(root)
            raise


if __name__ == '__main__':
    main()
