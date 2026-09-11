"""Resume the fixed study after its existing Fleet job; never submits GPU jobs.

Default is a read-only dry run. Paid forecasting/player calls require --execute.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from prediction.improve.data import TARGETS
from prediction.improve.baselines import METHODS as BASELINES
from prediction.improve.integrate import immutable, prompted, read, stamp
from prediction.improve.prospective_design import forecast_coverage, freeze_forecast_evidence, verify_prepared

NUMERICAL = tuple(BASELINES)+('qwen3_frozen_head', 'qwen3_lora_head')
METHODS = NUMERICAL+('llm_few_shot',)
STEPS = ('audit_training', 'score_development', 'development_gate', 'prompted_scopes',
         'normalize_and_freeze', 'players', 'collect', 'score_fresh', 'render')


def now(): return datetime.now(timezone.utc).isoformat()


def local(path):
    value = str(path)
    return Path('/shared/'+value[len('/mnt/sfs/'):] if value.startswith('/mnt/sfs/') else value).resolve()


def sha(path):
    result = hashlib.sha256()
    with local(path).open('rb') as handle:
        while block := handle.read(4*1024*1024): result.update(block)
    return result.hexdigest()


def hashes(paths): return {str(local(p)): sha(p) for p in paths}


def verify(table):
    for path, expected in table.items():
        if sha(path) != expected: raise ValueError('Bound artifact changed: '+path)


def save(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n'); temporary.replace(path)


def alive(pid):
    try: return Path(f'/proc/{int(pid)}/stat').read_text().split(') ')[1].split()[0] != 'Z'
    except (OSError, ValueError, IndexError): return False


def competitors(root):
    result = []
    tokens = ('prediction.improve.post_training', 'post_training.py', 'prediction.improve.inference',
              '/inference.py', 'prediction.runner', 'prediction.llm_forecast')
    for path in Path('/proc').glob('[0-9]*/cmdline'):
        try:
            pid = int(path.parent.name); args = path.read_bytes().decode().split('\0')
            if pid == os.getpid() or not alive(pid) or not args or 'python' not in Path(args[0]).name: continue
            command = ' '.join(args)
            if str(root) in command and any(token in command for token in tokens): result.append(pid)
        except (OSError, UnicodeError, ValueError): continue
    return result


@contextmanager
def execution_lock(root):
    root = Path(root); root.mkdir(parents=True, exist_ok=True)
    with (root/'execution.lock').open('a+') as handle:
        try: fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc: raise RuntimeError('Another execution owner holds the run lock') from exc
        other = competitors(root)
        if other: raise RuntimeError('Live competing executor processes: '+str(other))
        yield handle.fileno()  # Children inherit this descriptor, retaining ownership if this parent exits.


def evidence_table(record, field, marker, forecast=None):
    value = record.get(field, {}) if isinstance(record, dict) else {}
    if isinstance(value, dict): return value
    if not isinstance(value, str): raise ValueError('Invalid hash evidence field: '+field)
    target = record.get('source') if field == 'source_sha256' else None
    if field == 'output_sha256':
        target = forecast or record.get('output')
        if target is None and str(marker).endswith('.manifest.json'):
            target = str(marker)[:-len('.manifest.json')]+'.jsonl'
    if target is None: raise ValueError('Scalar hash lacks its artifact path: '+field)
    return {str(local(target)): value}


def record_evidence(path, forecast=None):
    record = read(path); evidence = {str(local(path)): sha(path)}
    for field in ('input_sha256', 'source_sha256', 'source_code_sha256', 'output_sha256', 'artifact_sha256', 'trace_sha256', 'decision_sha256', 'call_sha256'):
        table = evidence_table(record, field, path, forecast)
        verify(table); evidence.update({str(local(p)): value for p, value in table.items()})
    if forecast is not None:
        expected = record.get('forecast_sha256', record.get('output_sha256'))
        if not isinstance(expected, str) or sha(forecast) != expected: raise ValueError('Saved forecast changed')
        evidence[str(local(forecast))] = sha(forecast)
    return evidence


def verify_record_inputs(path, required):
    record_evidence(path)
    record = read(path)
    declared = {str(local(p)): h for field in ('input_sha256', 'source_sha256')
                for p,h in evidence_table(record, field, path).items()}
    for name, expected in hashes(required).items():
        if declared.get(name) != expected: raise ValueError('Existing result omitted or changed a required input: '+name)


def selected_path(root, value, default):
    path = Path(value) if value is not None else Path(default)
    path = local(path if path.is_absolute() else root/path)
    if not path.is_relative_to(root): raise ValueError('Selected execution evidence must be inside this run')
    return path


def selection_contract(root, submission, config, monitor):
    submitted, configured = read(submission), read(config)
    response = submitted['response']; job = response['name']
    if not isinstance(response.get('run_dir'), str) or not local(response['run_dir']).is_relative_to(root):
        raise ValueError('Selected Fleet run directory is outside this study')
    if response.get('run_dir') != configured.get('run_dir'):
        raise ValueError('Selected submission/config run directory differs')
    if not (job == configured['name'] or job.startswith(configured['name']+'-')):
        raise ValueError('Selected submission/config name differs')
    return dict(existing_fleet_run_id=job, submission_path=str(submission), config_path=str(config),
                monitor_dir=str(monitor), input_sha256=hashes([submission, config]))


def normalize_scope(scope, queries, rows):
    sid = scope['scope_id']; split = 'fresh_full' if sid == 'full' else 'fresh_family_excluded'
    index = {q['row_id']: q for q in queries}; output, seen = [], set()
    for row in rows:
        identity = row['method'], row['row_id'], row['target']
        if identity in seen or row['method'] not in METHODS or row['row_id'] not in scope['query_row_ids'] or row['target'] not in TARGETS:
            raise ValueError('Duplicate or unplanned fresh forecast')
        if row['split'] != split or row['fold_id'] != sid: raise ValueError('Fresh forecast scope mismatch')
        query = index[row['row_id']]
        for field in ('game_id', 'group_id', 'model', 'opponent'):
            if row[field] != query[field]: raise ValueError('Fresh forecast metadata mismatch')
        if any(row.get(k) is not None for k in ('value', 'successes', 'opportunities', 'targets')):
            raise ValueError('Fresh forecast contains observed outcomes')
        seen.add(identity)
        output.append(dict(row, family=query['family'], scope_id=sid))
    for qid in scope['query_row_ids']:
        for target in TARGETS:
            for method in METHODS:
                if (method, qid, target) not in seen:
                    if method != 'llm_few_shot': raise ValueError('Missing numerical forecast row')
                    q = index[qid]
                    output.append(dict(**{k:q[k] for k in ('row_id','game_id','group_id','model','opponent','family')},
                        scope_id=sid, fold_id=sid, split=split, target=target, method=method,
                        prediction=None, status='explicit_missing_prompted_forecast'))
    return output


class Work:
    def __init__(self, root, lock_fd, python=sys.executable):
        self.root, self.folder, self.lock_fd, self.python = Path(root), Path(root)/'post-training', lock_fd, python
        self.plan = None
        self.report_out = self.root.parents[1]/'IMPROVEMENT-REPORT.md'
        self.submission_path = self.root/'fleet-runtime/main-submit.json'
        self.config_path = self.root/'fleet-runtime/main-config-allie.json'
        self.monitor_dir = self.root/'fleet-runtime/main-monitor'

    def prepare(self):
        verify_prepared(self.root)
        fixed = ['training-freeze.json', 'gate-protocol.json', 'baseline-protocol.json', 'transformer-protocol.json',
                 'budget-policy.json',
                 'inference-source-manifest.json', 'development-few-shot/forecasts.jsonl', 'development-few-shot/forecasts.manifest.json']
        paths = [self.root/p for p in fixed]+[self.submission_path, self.config_path]
        prior_submission = self.root/'fleet-runtime/main-submit.json'
        if prior_submission != self.submission_path and prior_submission.exists(): paths.append(prior_submission)
        selected = selection_contract(self.root, self.submission_path, self.config_path, self.monitor_dir)
        paths += [Path(__file__).with_name(name+'.py') for name in
                  ('post_training','inference','integrate','evaluate','gate','report','prospective_design','data','baselines')]
        training = read(self.root/'training-freeze.json')
        expected = {str(self.root/p): h for p,h in training['relative_sha256'].items()}
        expected.update({str(self.root/'inference-source'/p): h for p,h in read(self.root/'inference-source-manifest.json')['files'].items()})
        verify(expected)
        for scope in read(self.root/'prospective-design/scopes.json'):
            folder = self.root/'fresh-forecasts/few_shot'/scope['scope_id']
            paths += [folder/n for n in ('inputs.json','query-index.json','inference-wrapper.json')]
            paths += sorted((folder/'queries').glob('*.json'))
        wrapper = self.folder/'inference.py'
        wrapper.parent.mkdir(parents=True, exist_ok=True)
        content = Path(__file__).with_name('inference.py').read_bytes()
        if wrapper.exists() and wrapper.read_bytes() != content: raise ValueError('Archived wrapper changed')
        if not wrapper.exists():
            with wrapper.open('xb') as handle: handle.write(content)
        paths.append(wrapper)
        plan = dict(version='improve-post-training-v2', **{k:v for k,v in selected.items() if k != 'input_sha256'}, input_sha256={**expected, **hashes(paths)},
                    methods=list(METHODS), scopes=[s['scope_id'] for s in read(self.root/'prospective-design/scopes.json')],
                    steps=list(STEPS), kimi_concurrency='one scope process at a time, frozen workers=8',
                    player_workers=32, paid_calls_require_execute=True, fleet_submission_or_cancellation=False)
        immutable(self.folder/'plan.json', plan); self.plan = plan
        if (self.root/'fresh-prospective/status.json').exists() and not (self.root/'fresh-prospective/forecast-freeze.json').exists():
            raise ValueError('Player startup exists without a forecast freeze')

    def step(self, name, fn, inputs=(), outputs=()):
        verify(self.plan['input_sha256'])
        path = self.folder/'steps'/(name+'.json')
        contract = dict(plan_sha256=sha(self.folder/'plan.json'), input_sha256=hashes(inputs))
        previous = read(path) if path.exists() else None
        if previous:
            if previous['contract'] != contract: raise ValueError('Step inputs changed: '+name)
            if previous['status'] == 'complete':
                verify(previous['output_sha256'])
                for output in previous['output_sha256']:
                    if Path(output).suffix == '.json': record_evidence(output)
                return previous.get('result')
            if previous.get('child_pid') and alive(previous['child_pid']): raise RuntimeError('Prior owned child is still alive')
        save(path, dict(status='running', started_utc=now(), pid=os.getpid(), contract=contract))
        save(self.folder/'status.json', dict(status='running', step=name, updated_utc=now(), pid=os.getpid()))
        try:
            result = fn()
            verify(contract['input_sha256']); verify(self.plan['input_sha256'])
            save(path, dict(status='complete', finished_utc=now(), contract=contract, output_sha256=hashes(outputs), result=result))
            return result
        except BaseException as exc:
            state = read(path); state.update(status='error', error_type=type(exc).__name__, message=str(exc), updated_utc=now())
            save(path, state); raise

    def command(self, name, arguments):
        other = competitors(self.root)
        if other: raise RuntimeError('Competing executor appeared: '+str(other))
        log = self.folder/'logs'/(name+'.log'); log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('a') as stream:
            child = subprocess.Popen([self.python, '-B', *arguments], stdout=stream, stderr=subprocess.STDOUT,
                                     cwd=Path(__file__).resolve().parents[2], pass_fds=(self.lock_fd,))
            marker = self.folder/'steps'/(name+'.json')
            state = read(marker); state.update(child_pid=child.pid, command=arguments); save(marker, state)
            code = child.wait()
        if code: raise RuntimeError(f'{name} exited with code {code}; outputs preserved for checkpoint audit')

    def audit_training(self):
        state = read(self.root/'fleet-runtime/training-status.json')
        if state['status'] != 'complete' or state['fleet_run_id'] != self.plan['existing_fleet_run_id']:
            raise ValueError('Wrong or incomplete existing Fleet job')
        evidence = hashes([self.root/'fleet-runtime/training-status.json'])
        baseline = self.root/'baselines/completion.json'
        if read(baseline)['run_id'] != state['fleet_run_id']: raise ValueError('Baseline Fleet lineage differs')
        evidence.update(record_evidence(baseline))
        folds = read(self.root/'data/folds.json')
        if len(folds) != 10: raise ValueError('Expected ten fixed folds')
        for method in ('frozen','lora'):
            for fold in folds:
                folder = self.root/'transformer'/method/fold['fold_id']
                evidence.update(record_evidence(folder/'complete.json'))
                artifact = read(folder/'artifact.json')
                if artifact['training_row_ids'] != fold['train_row_ids'] or artifact['diagnostics']['fleet']['fleet_run_id'] != state['fleet_run_id']:
                    raise ValueError('Fit scope or Fleet lineage differs')
                if method == 'lora' and artifact['diagnostics']['optimization_success'] is not True:
                    raise ValueError('Fixed LoRA optimization did not finish')
                evidence.update(record_evidence(folder/'forecast-manifest.json', folder/'forecasts.jsonl'))
        for sid in self.plan['scopes']:
            for method in ('baselines','frozen','lora'):
                folder = self.root/'fresh-forecasts'/method/sid
                manifest = folder/('forecasts.manifest.json' if method=='baselines' else 'forecast-manifest.json')
                evidence.update(record_evidence(manifest, folder/'forecasts.jsonl'))
        immutable(self.folder/'training-audit.json', dict(status='verified', fleet_run_id=state['fleet_run_id'],
            transformer_fits=20, artifact_sha256=evidence, no_local_training=True))

    def score_development(self):
        from prediction.improve.evaluate import score_files
        forecasts = [self.root/'baselines/forecasts.jsonl', self.root/'development-few-shot/forecasts.jsonl']
        forecasts += [self.root/'transformer'/method/fold['fold_id']/'forecasts.jsonl'
                      for method in ('frozen','lora') for fold in read(self.root/'data/folds.json')]
        if len(forecasts) != 22: raise ValueError('Expected all twenty transformer forecast files')
        declarations = {(r['method'], r['fold_id']) for path in forecasts for line in path.read_text().splitlines()
                        if line.strip() for r in [json.loads(line)]}
        expected = {(method, fold['fold_id']) for method in NUMERICAL for fold in read(self.root/'data/folds.json')}
        if declarations != expected | {('llm_few_shot', 'full')}:
            raise ValueError('Development candidate/scope inventory differs from the fixed comparison')
        output = self.root/'development-evaluation'; audit = output/'audit.json'
        def score():
            if audit.exists(): verify_record_inputs(audit, [self.root/'data/data.json', self.root/'data/folds.json', *forecasts])
            else: score_files(self.root/'data/data.json', self.root/'data/folds.json', forecasts, output)
        self.step('score_development', score, [self.root/'data/data.json', self.root/'data/folds.json', *forecasts], [audit])

    def apply_gate(self):
        from prediction.improve.gate import decide
        path = self.root/'development-gate.json'
        def gate():
            if path.exists(): verify_record_inputs(path, [self.root/'gate-protocol.json', self.root/'development-evaluation/scores.json', self.root/'development-evaluation/paired-comparisons.json'])
            else: decide(self.root, self.root/'development-evaluation')
            return read(path)['proceed']
        return self.step('development_gate', gate,
            [self.root/'development-evaluation/audit.json', self.root/'development-evaluation/scores.json',
             self.root/'development-evaluation/paired-comparisons.json', self.folder/'training-audit.json'], [path])

    def prompts(self):
        for sid in self.plan['scopes']:
            folder = self.root/'fresh-forecasts/few_shot'/sid; status = folder/'status.json'; name = 'kimi_'+sid
            def execute():
                if status.exists() and read(status).get('status') in ('complete','finished_with_errors'):
                    if sha(folder/'forecasts.jsonl') != read(status)['forecast_sha256']: raise ValueError('Prompted terminal forecast changed')
                else: self.command(name, [str(self.folder/'inference.py'), 'few_shot', '--run-root', str(self.root),
                    '--source-root', str(self.root/'inference-source'), '--scope', sid, '--workers', '8'])
            self.step(name, execute, [folder/'inputs.json', folder/'query-index.json', self.root/'development-gate.json'],
                      [status, folder/'forecasts.jsonl'])

    def freeze(self):
        scopes, queries = read(self.root/'prospective-design/scopes.json'), read(self.root/'prospective-design/queries.json')
        normalized, exclusions = [], []
        for scope in scopes:
            sid = scope['scope_id']; split = 'fresh_full' if sid=='full' else 'fresh_family_excluded'; rows = []
            for method in ('baselines','frozen','lora'):
                rows.extend(json.loads(line) for line in (self.root/'fresh-forecasts'/method/sid/'forecasts.jsonl').read_text().splitlines() if line)
            folder = self.root/'fresh-forecasts/few_shot'/sid; status = read(folder/'status.json')
            if status['status'] not in ('complete','finished_with_errors'): raise ValueError('Prompted source is not terminal')
            if sha(folder/'forecasts.jsonl') != status['forecast_sha256']: raise ValueError('Prompted forecast changed')
            selected = [q for q in queries if q['row_id'] in scope['query_row_ids']]
            rows += prompted(folder/'forecasts.jsonl', selected, self.folder/'prompted-joined'/sid/'forecasts.jsonl', split, sid)
            normalized += normalize_scope(scope, queries, rows)
            if status['status'] == 'finished_with_errors':
                exclusions.append(dict(scope_id=sid, method='llm_few_shot', created_utc=status['finished_utc'],
                    reason='Original bounded prompted runner ended with technical failures; retain available predictions and missing all-method support.',
                    evidence_path=str(folder/'status.json'), evidence_sha256=sha(folder/'status.json')))
        coverage = forecast_coverage(scopes, queries, normalized, METHODS, NUMERICAL, exclusions)
        if not coverage['ready']: raise ValueError('Required fresh numerical/prompted coverage failed')
        path = self.folder/'normalized-forecasts.jsonl'
        immutable(path, normalized, jsonl=True); immutable(self.folder/'coverage.json', coverage)
        evidence = set(self.plan['input_sha256']) | set(read(self.folder/'training-audit.json')['artifact_sha256'])
        evidence.update(str(p) for p in (self.root/'fresh-forecasts').rglob('*') if p.is_file() and not p.is_symlink()
                        and p.suffix in ('.json','.jsonl'))
        evidence.update(str(p) for p in (self.folder/'prompted-joined').rglob('*') if p.is_file())
        evidence.update(str(p) for p in [self.folder/'plan.json', self.folder/'training-audit.json', self.folder/'coverage.json',
                                       self.root/'development-gate.json'])
        freeze_forecast_evidence(self.root, sorted(evidence), coverage, path)

    def players(self):
        folder = self.root/'fresh-prospective'; status = folder/'status.json'
        def execute():
            if not status.exists() or read(status).get('status') not in ('complete','finished_with_errors'):
                self.command('players', [str(self.folder/'inference.py'), 'players', '--run-root', str(self.root),
                    '--source-root', str(self.root/'inference-source'), '--workers', '32'])
        self.step('players', execute, [folder/'forecast-freeze.json', self.root/'development-gate.json'], [status])

    def collect(self):
        from prediction.improve.integrate import collect
        self.step('collect', lambda: collect(self.root),
            [self.root/'fresh-prospective/status.json', self.root/'fresh-prospective/forecast-freeze.json'], [self.root/'fresh-collected/audit.json'])

    def score_fresh(self):
        from prediction.improve.evaluate import score_files
        folder, output = self.root/'fresh-collected', self.root/'fresh-evaluation'
        forecasts = self.folder/'normalized-forecasts.jsonl'
        def score():
            if (output/'audit.json').exists(): verify_record_inputs(output/'audit.json', [folder/'data.json', folder/'folds.json', forecasts])
            else: score_files(folder/'data.json', folder/'folds.json', [forecasts], output)
        self.step('score_fresh', score, [folder/'data.json', folder/'folds.json', forecasts], [output/'audit.json'])

    def render(self):
        from prediction.improve.report import render
        render(self.root, self.report_out, figures=self.root/'report-figures')


def run(root, execute=False, deadline=None, poll=30, work_factory=Work, clock=time.time, sleep=time.sleep, report_out=None,
        submission=None, config=None, monitor_dir=None):
    root = Path(root).resolve()
    if not root.is_relative_to(Path('/shared/allie')): raise ValueError('Shared storage required')
    submission_path = selected_path(root, submission, 'fleet-runtime/main-submit.json')
    config_path = selected_path(root, config, 'fleet-runtime/main-config-allie.json')
    monitor_path = selected_path(root, monitor_dir, 'fleet-runtime/main-monitor')
    if not execute: return dict(submission=str(submission_path), config=str(config_path), monitor_dir=str(monitor_path), status='dry_run', steps=list(STEPS), paid_calls=False, fleet_calls=False,
                                 kimi_concurrency='one prepared scope at a time, workers=8', player_workers=32)
    if not 1 <= poll <= 60: raise ValueError('Polling interval must be between one and sixty seconds')
    with execution_lock(root) as lock_fd:
        status_path = root/'post-training/status.json'
        try:
            work = work_factory(root, lock_fd)
            work.submission_path, work.config_path, work.monitor_dir = submission_path, config_path, monitor_path
            if report_out is not None:
                work.report_out = Path(report_out).resolve()
                if not work.report_out.is_relative_to(Path('/shared/allie')): raise ValueError('Report must use shared storage')
            work.prepare()
            limit = stamp(deadline or read(root/'training-freeze.json')['absolute_conservative_deadline']).timestamp()
            job = read(submission_path)['response']['name']
            prior_path = root/'fleet-runtime/main-submit.json'
            prior_job = read(prior_path)['response']['name'] if prior_path.exists() and prior_path != submission_path else None
            while True:
                path = root/'fleet-runtime/training-status.json'; state = read(path) if path.exists() else {}
                if state and state.get('fleet_run_id') != job:
                    if state.get('fleet_run_id') == prior_job and state.get('status') in ('error','failed','stopped'):
                        state = {}  # Wait for the explicitly selected retry; preserve the original terminal evidence.
                    else: raise ValueError('Different Fleet job wrote the training status')
                if state.get('status') == 'complete': break
                completion_path = monitor_path/'completion.json'
                monitor = read(completion_path) if completion_path.exists() else {}
                if monitor and monitor.get('name') != job: raise ValueError('Different Fleet job in local monitor completion')
                terminal_monitor = bool(monitor) and str(monitor.get('status','')).lower() in ('succeeded','complete','completed','failed','stopped','cancelled','canceled','deleted')
                if state.get('status') in ('error','failed','stopped') or terminal_monitor or clock() >= limit:
                    reason = state.get('message') or ('Fleet monitor is terminal without verified worker completion' if terminal_monitor else 'Training did not finish before the wait deadline')
                    result = dict(status='training_blocked', reason=reason,
                                  existing_fleet_run_id=job, updated_utc=now(), no_job_submitted_or_cancelled=True,
                                  behavioral_conclusion='Not evaluated: technical training block; this is not a negative behavioral result.')
                    save(status_path, result)
                    try: work.render()
                    except Exception as exc:
                        result['report_error'] = type(exc).__name__+': '+str(exc); save(status_path, result)
                    return result
                save(status_path, dict(status='waiting_for_existing_training', existing_fleet_run_id=job, updated_utc=now()))
                sleep(min(poll, max(0, limit-clock())))
            work.step('audit_training', work.audit_training, [root/'fleet-runtime/training-status.json'], [root/'post-training/training-audit.json'])
            work.score_development()
            if not work.apply_gate():
                work.render(); result = dict(status='stopped_at_development_gate', fresh_calls=False, updated_utc=now())
            else:
                work.prompts()
                work.step('normalize_and_freeze', work.freeze, [root/'post-training/training-audit.json', root/'development-gate.json'],
                    [root/'fresh-prospective/forecast-freeze.json', root/'post-training/normalized-forecasts.jsonl', root/'post-training/coverage.json'])
                work.players(); work.collect(); work.score_fresh(); work.render()
                result = dict(status='fresh_results_complete_interpretation_pending',
                              interpretation='Fresh results complete; scientific interpretation pending.', updated_utc=now())
            save(status_path, result); return result
        except BaseException as exc:
            save(status_path, dict(status='error', error_type=type(exc).__name__, message=str(exc), updated_utc=now()))
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', required=True); parser.add_argument('--execute', action='store_true')
    parser.add_argument('--deadline'); parser.add_argument('--interval', type=float, default=30)
    parser.add_argument('--report-out')
    parser.add_argument('--submission'); parser.add_argument('--config'); parser.add_argument('--monitor-dir')
    args = parser.parse_args()
    print(json.dumps(run(args.run_root, args.execute, args.deadline, args.interval, report_out=args.report_out,
                         submission=args.submission, config=args.config, monitor_dir=args.monitor_dir)))


if __name__ == '__main__': main()
