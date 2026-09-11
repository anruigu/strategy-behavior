"""Read-only final artifact audit. Writes only a new audit JSON under this run.

Run from /shared/allie/strategy-behavior with Python -B. No clients, model fitting,
score recomputation, signals, billing mutations, or report rendering are used.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time

PROJECT = Path('/shared/allie/strategy-behavior')
ROOT = PROJECT/'prediction/results/overnight-20260910'
sys.path.insert(0, str(PROJECT))
from prediction import pipeline, after_matrix, secondary_analysis


def utc():
    return datetime.now(timezone.utc).isoformat()


def dt(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    assert result.tzinfo is not None, 'Timezone missing'
    return result


def plain(path):
    return json.loads(Path(path).read_text())


def readiness():
    main = plain(ROOT/'pipeline-status.json')
    secondary = plain(ROOT/'independent-analysis/secondary-status.json')
    jobs = secondary.get('jobs', {})
    return dict(ready=main.get('status') == 'complete_through_gate7'
                and secondary.get('status') == 'complete' and len(jobs) == 10
                and all(j.get('status') == 'complete' for j in jobs.values()),
                main=main.get('status'), secondary=secondary.get('status'),
                complete_secondary_jobs=sum(j.get('status') == 'complete' for j in jobs.values()))


class Audit:
    def __init__(self):
        self.hashes = {}
        self.stats = {}
        self.checks = []
        self.issues = []

    def raw(self, path):
        path = str(Path(path).resolve())
        data = Path(path).read_bytes()
        hashed = hashlib.sha256(data).hexdigest()
        if path in self.hashes:
            assert self.hashes[path] == hashed, 'Changed during audit: '+path
        self.hashes[path] = hashed
        self.stats[path] = (Path(path).stat().st_size, Path(path).stat().st_mtime_ns)
        return data

    def read(self, path):
        return json.loads(self.raw(path))

    def hash(self, path):
        path = str(Path(path).resolve())
        if path not in self.hashes:
            self.raw(path)
        return self.hashes[path]

    def semantic_hash(self, path):
        # io_utils.digest convention used by collection provenance; read() also
        # preserves the separate file-byte digest in the final audit closure.
        return hashlib.sha256(json.dumps(self.read(path), sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def check_hashes(self, mapping):
        assert mapping, 'Empty hash contract'
        for path, expected in mapping.items():
            assert self.hash(path) == expected, 'Hash mismatch: '+str(path)
        return len(mapping)

    def section(self, name, function):
        try:
            result = function()
            self.checks.append(dict(name=name, status='verified', result=result))
            print(json.dumps(dict(section=name, status='verified')), flush=True)
        except Exception as exc:
            issue = dict(name=name, status='failed', error=type(exc).__name__+': '+str(exc))
            self.checks.append(issue)
            self.issues.append(issue)
            print(json.dumps(issue), flush=True)

    def unchanged(self):
        for path, expected in self.hashes.items():
            assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, 'Changed during audit: '+path
        return len(self.hashes)


def steps(a):
    required = {
        'primary-pilot-collect', 'primary-pilot-diagnostics', 'pilot-numerical',
        'development-collect', 'development-numerical', 'after-label-sensitivity',
        'after-prospective-metadata', 'after-llm-forecasts', 'after-prospective-collect',
        'after-prospective-evaluation-numerical', 'after-prospective-evaluation',
        'after-prospective-evaluation-pair', 'after-prospective-evaluation-model',
        'after-controls-metadata', 'after-controls-forecast', 'after-controls-collect',
        'after-controls-evaluation', 'after-control-sensitivity',
    }
    for name in ('full', 'excluded_pair', 'excluded_model'):
        required.update(('after-fit-'+name, 'after-forecast-'+name,
                         'after-secondary-fit-'+name,
                         'after-secondary-forecast-'+name+'-prospective'))
    required.add('after-secondary-forecast-full-controls')
    jobs = {j['name']: j for j in secondary_analysis.job_specs(ROOT, bootstrap=500)}
    assert len(jobs) == 10
    required.update('secondary-analysis-'+name for name in jobs)
    markers = {p.stem: p for p in (ROOT/'steps').glob('*.json')}
    assert required <= set(markers), 'Missing required markers: '+str(sorted(required-set(markers)))
    result = []
    for name, path in sorted(markers.items()):
        saved = a.read(path)
        assert saved['status'] == 'complete', 'Unfinished step: '+name
        contract = saved['contract']
        args = saved.get('command', contract['command'])
        assert args == contract['command'], 'Command copies disagree: '+name
        if name.startswith('secondary-analysis-'):
            job = jobs[name.removeprefix('secondary-analysis-')]
            assert args == job['arguments'] and contract['classification'] == job['classification']
            membership = {str(p.resolve()) for p in secondary_analysis.input_paths(ROOT, job)}
            assert membership == set(contract['initial_sha256']), 'Input closure membership changed: '+name
            inputs = a.check_hashes(contract['initial_sha256'])
            supervisor = a.read(job['output']/'supervisor-audit.json')
            assert supervisor['status'] == 'verified'
            assert supervisor['initial_sha256'] == contract['initial_sha256']
            a.check_hashes(supervisor['output_sha256'])
        else:
            actual = after_matrix.step_contract(args) if name.startswith('after-') else pipeline.command_contract(args)
            assert actual == contract, 'Command/input/source contract changed: '+name
            inputs = a.check_hashes(contract['source_hashes'])
            if contract['input_hashes']:
                inputs += a.check_hashes(contract['input_hashes'])
        outputs = saved.get('output_hashes', saved.get('output_sha256'))
        count = a.check_hashes(outputs)
        assert saved.get('returncode', 0) == 0
        result.append(dict(name=name, command=args, input_source_hashes=inputs,
                           output_hashes=count, finished=saved.get('finished')))
    return dict(required_count=len(required), completed_count=len(result), steps=result)


def archives(a):
    specs = [('source-manifest.json', 'source'),
             ('analysis-source-v1-manifest.json', 'analysis-source-v1'),
             ('execution-source-v1-manifest.json', 'execution-source-v1'),
             ('secondary-source-v1/manifest.json', 'secondary-source-v1'),
             ('secondary-analysis-source-v1/manifest.json', 'secondary-analysis-source-v1')]
    result = []
    for manifest, folder in specs:
        record = a.read(ROOT/manifest)
        files = record.get('files', record)
        count = a.check_hashes({str(ROOT/folder/name): expected for name, expected in files.items()})
        result.append(dict(manifest=manifest, archived_files=count))
    return result


def cohorts(a):
    primary = a.read(ROOT/'primary-pilot-manifest.json')
    result = {}
    all_rows = {}
    expected = {'primary-pilot': (960, 958, 24), 'development': (960, 960, 48),
                'prospective': (420, 420, 21), 'controls': (420, 420, 21)}
    for stage, (planned, completed, shapes) in expected.items():
        manifest = primary if stage == 'primary-pilot' else a.read(ROOT/stage/'manifest.json')
        for key in ('models', 'protocol', 'sources', 'source_root', 'ledger'):
            assert manifest[key] == primary[key], stage+' protocol/source/config inheritance: '+key
        folder = ROOT/'primary-pilot/final-collection' if stage == 'primary-pilot' else ROOT/stage/'collected'
        summary, rows = a.read(folder/'summary.json'), a.read(folder/'records.json')
        assert summary.get('integrity_errors', 0) == 0 and not summary.get('errors', [])
        assert summary['planned_episodes'] == planned and summary['complete_episodes'] == completed
        assert len(manifest['games']) == summary['games'] == shapes
        specs = {r['id']: r for r in manifest['episodes']}
        assert len(specs) == len(manifest['episodes']) == planned
        by_episode = defaultdict(list)
        for row in rows:
            by_episode[row['episode_id']].append(row)
        assert len(rows) == completed*2 and len(by_episode) == completed
        assert set(by_episode) <= set(specs)
        missing = sorted(set(specs)-set(by_episode))
        if stage == 'primary-pilot':
            assert missing == sorted(summary['missing_episodes'])
            assert rows == a.read(ROOT/'primary-pilot/final-records.json')
        else:
            status = a.read(ROOT/stage/'status.json')
            assert status['status'] == 'complete' and status['completed'] == completed and not status.get('errors', [])
        for episode, focal in by_episode.items():
            spec = specs[episode]
            assert len(focal) == 2 and {r['player_index'] for r in focal} == {0, 1}
            for row in focal:
                assert row['model'] == spec['models'][row['player_index']]
                assert row['opponent'] == spec['models'][1-row['player_index']]
                assert row['game_id'] == spec['game_id']
                for key in ('trial_id', 'representation', 'swap'):
                    assert row[key] == spec[key]
            source_stage = focal[0]['source_stage'] if stage == 'primary-pilot' else stage
            trace = a.read(ROOT/source_stage/'episodes'/episode/'trace.json')
            assert trace['id'] == episode and trace['status'] == 'complete' and len(trace['rounds']) == 8
            assert trace['models'] == spec['models']
            assert trace['game']['id'] == spec['game_id']
            for key in ('trial_id', 'representation', 'swap'):
                assert trace[key] == spec[key]
        provenance = a.read(folder/'provenance.json')
        if stage == 'primary-pilot':
            for source in provenance:
                p = ROOT/source['source_stage']/'manifest.json'
                # combine_pilot stores io_utils.digest(parsed_manifest), not a
                # digest of the file's whitespace. Retain both hash conventions.
                assert a.semantic_hash(p) == source['manifest_sha256'], 'Combined source manifest semantic digest: '+str(p)
                trace_provenance = a.read(source['trace_provenance'])
                for item in trace_provenance:
                    assert a.semantic_hash(item['path']) == item['sha256'], 'Trace semantic digest: '+item['path']
        else:
            assert len(provenance) == completed
            for item in provenance:
                assert a.semantic_hash(item['path']) == item['sha256'], 'Trace semantic digest: '+item['path']
        support = {}
        for target in sorted({t for r in rows for t in r['targets']}):
            eligible = [(r, r['targets'][target]) for r in rows if target in r['targets'] and r['targets'][target].get('opportunities', 0) > 0]
            support[target] = dict(focal_rows=len(eligible), games=len({r['game_id'] for r,t in eligible}),
                                   opportunities=sum(t['opportunities'] for r,t in eligible))
        all_rows[stage] = rows
        result[stage] = dict(planned=planned, completed=completed, focal_rows=len(rows), games=shapes,
                             canonical_groups=len({r['group_id'] for r in rows}), missing=missing,
                             integrity_errors=0, opportunity_support=support)
    training = a.read(ROOT/'training-records.json')
    assert training == all_rows['primary-pilot']+all_rows['development']
    assert len(training) == 3836 and len({r['group_id'] for r in training}) == 72
    assert not {r['group_id'] for r in training}&{r['group_id'] for r in all_rows['prospective']}
    assert {r['group_id'] for r in all_rows['controls']} <= {r['group_id'] for r in all_rows['primary-pilot']}
    result['training'] = dict(episodes=1918, focal_rows=3836, canonical_groups=72)
    result['total_primary_collected'] = dict(episodes=2758, planned=2760, focal_rows=5516,
        note='Includes 420 control variants reusing seven pilot shapes; calibration calls/episodes are excluded.')
    return result


def chronology(a):
    secondary = a.read(ROOT/'secondary-baselines/forecast-freeze.json')
    a.check_hashes(secondary['forecasts_sha256'])
    assert a.hash(ROOT/'secondary-baselines/plan.json') == secondary['plan_sha256']
    results = {}
    for stage in ('prospective', 'controls'):
        freezes = a.read(ROOT/stage/'forecast-freeze.json')
        a.check_hashes(freezes['sha256'])
        paths = sorted((ROOT/stage/'episodes').glob('*/trace.json'))
        starts = [(dt(a.read(p)['started']), str(p)) for p in paths]
        earliest, first_path = min(starts)
        assert len(starts) == 420
        assert dt(freezes['created_utc']) < earliest and dt(secondary['finished']) < earliest
        results[stage] = dict(actual_traces=420, earliest_started=earliest.isoformat(), first_trace=first_path,
            primary_freeze=freezes['created_utc'], primary_files=len(freezes['sha256']),
            primary_lead_seconds=(earliest-dt(freezes['created_utc'])).total_seconds(),
            secondary_freeze=secondary['finished'], secondary_files=len(secondary['forecasts_sha256']))
    folders = ['prospective/evaluation-numerical', 'prospective/evaluation', 'prospective/evaluation-pair',
               'prospective/evaluation-model', 'controls/evaluation',
               'secondary-baselines/full/prospective-evaluation',
               'secondary-baselines/excluded_pair/prospective-evaluation',
               'secondary-baselines/excluded_model/prospective-evaluation',
               'secondary-baselines/full/controls-evaluation']
    audits = []
    for name in folders:
        folder = ROOT/name
        saved = a.read(folder/'audit.json')
        assert saved['prospective_verified'] is True and saved['issues'] == []
        a.check_hashes(saved['source_sha256'])
        # This helper rechecks actual trace times and each source's completion
        # timestamp rather than accepting the audit's saved boolean.
        evidence = secondary_analysis.verified_evaluation(folder)
        coverage = a.read(folder/'coverage.json')
        assert coverage['missing_planned_outcomes'] == [] and coverage['unforecast_planned_rows'] == []
        audits.append(dict(folder=name, independently_rechecked=evidence, coverage={k:coverage[k] for k in
                     ('planned_focal_rows', 'observed_focal_rows', 'planned_episodes', 'observed_episodes')}))
    llm = a.read(ROOT/'prospective/llm-forecasts/status.json')
    assert llm['status'] == 'complete' and llm['completed'] == llm['planned'] == 1008 and llm['errors'] == []
    assert a.hash(ROOT/'prospective/llm-forecasts/forecasts.jsonl') == llm['forecast_sha256']
    results['evaluation_audits'] = audits
    results['llm_queries'] = dict(planned=1008, completed=1008, failed=0, rows=llm['rows'])
    return results


def ledger_snapshot(path):
    assert Path(path).is_file()
    # URI mode=ro previously failed on this shared filesystem. No Ledger object
    # is instantiated; query_only prohibits writes on this SELECT connection.
    db = sqlite3.connect(str(path), timeout=15)
    try:
        db.execute('PRAGMA query_only=ON')
        db.execute('BEGIN')
        ceiling = db.execute('SELECT ceiling FROM settings').fetchone()[0]
        rows = db.execute('SELECT id,model,reserved,charged,status,detail FROM calls ORDER BY id').fetchall()
    finally:
        db.close()
    counts = Counter(row[4] for row in rows)
    committed = sum(row[3] if row[3] is not None else row[2] for row in rows)
    reported = sum(row[3] or 0 for row in rows)
    assert committed <= ceiling+1e-8 and min([row[2] for row in rows]+[0]) >= 0
    assert all(row[3] is None or row[3] >= 0 for row in rows)
    assert all(row[4] in ('settled', 'reserved', 'unknown') for row in rows)
    models = {}
    for model in sorted({row[1] for row in rows}):
        sample = [row for row in rows if row[1] == model]
        models[model] = dict(calls=len(sample), reported_usd=sum(row[3] or 0 for row in sample),
            committed_usd=sum(row[3] if row[3] is not None else row[2] for row in sample))
    serialized = json.dumps(dict(ceiling=ceiling, rows=rows), separators=(',', ':'), allow_nan=False).encode()
    return dict(path=str(path), calls=len(rows), ceiling_usd=ceiling, reported_usd=reported,
                committed_usd=committed, retained_unknown_or_reserved_usd=committed-reported,
                states=dict(counts), by_model=models, select_snapshot_sha256=hashlib.sha256(serialized).hexdigest())


def budgets(a):
    paths = sorted(ROOT.rglob('*.sqlite'))
    snapshots = [ledger_snapshot(p) for p in paths]
    global_ledger = next(x for x in snapshots if Path(x['path']) == ROOT/'budget.sqlite')
    assert global_ledger['ceiling_usd'] == 3000
    stage = [x for x in snapshots if Path(x['path']) != ROOT/'budget.sqlite']
    assert sum(x['calls'] for x in stage) == global_ledger['calls'], 'Global/stage call count differs'
    for field in ('committed_usd', 'reported_usd'):
        assert abs(sum(x[field] for x in stage)-global_ledger[field]) < 1e-7, 'Global/stage ledger totals differ'
    for earlier, path in zip(snapshots, paths):
        assert ledger_snapshot(path) == earlier, 'Ledger changed during read-only audit'
    return dict(global_ledger=global_ledger, stage_ledgers=stage,
                note='Reservations retained exactly as recorded, including interrupted calibration. Hosted FLT zero dollar entries are not zero compute; no conversion to dollars was invented.')


def processes(a):
    paths = sorted(ROOT.glob('*process.json'))+sorted(ROOT.glob('*/process.json'))
    boot = int(next(s.split()[1] for s in Path('/proc/stat').read_text().splitlines() if s.startswith('btime ')))
    ticks = os.sysconf('SC_CLK_TCK')
    result = []
    for path in paths:
        record = a.read(path)
        pid = record['pid']
        assert isinstance(pid, int) and pid > 0
        proc = Path('/proc')/str(pid)
        item = dict(record=str(path), pid=pid, recorded_started=record.get('started'))
        try:
            stat = (proc/'stat').read_text().rsplit(')', 1)[1].split()
            state = stat[0]
            command = (proc/'cmdline').read_bytes().replace(b'\x00', b' ').decode(errors='replace').strip()
            actual_start = boot+int(stat[19])/ticks
            recorded = dt(record['started']).timestamp()
            reused = abs(actual_start-recorded) > 120
            item.update(proc_state=state, command=command, apparent_pid_reuse=reused,
                        terminal=state == 'Z' or reused, actual_start_epoch=actual_start)
        except FileNotFoundError:
            item.update(proc_state='absent', terminal=True, apparent_pid_reuse=False)
        if 'watcher' not in path.name:
            assert item['terminal'], 'Recorded scientific process still live: '+str(item)
        result.append(item)
    return dict(processes=result, signals_sent=False,
                note='Absent and zombie processes are terminal. PID start-time mismatch is reported as reuse; no process was signaled. A display-only watcher, if active, is reported separately.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-ready', action='store_true')
    parser.add_argument('--wait', action='store_true')
    parser.add_argument('--out', type=Path, default=ROOT/'independent-analysis/completion-audit.json')
    args = parser.parse_args()
    state = readiness()
    if args.check_ready:
        print(json.dumps(state)); return 0 if state['ready'] else 2
    while not state['ready'] and args.wait:
        if state['main'] == 'error' or state['secondary'] == 'error':
            raise RuntimeError('Required upstream process failed: '+str(state))
        print(json.dumps(dict(waiting=state, time=utc())), flush=True)
        time.sleep(30)
        state = readiness()
    if not state['ready']:
        raise RuntimeError('Final audit requires both pipelines complete: '+str(state))
    assert args.out.resolve().is_relative_to(ROOT/'independent-analysis')
    assert not args.out.exists(), 'Preserve existing independent audit'
    audit = Audit()
    started = utc()
    audit.read(ROOT/'pipeline-status.json')
    audit.read(ROOT/'independent-analysis/secondary-status.json')
    for name, function in [('saved_step_contracts', steps), ('source_archives', archives),
                           ('cohorts_and_missingness', cohorts), ('forecast_before_actual_play', chronology),
                           ('budget_ledgers', budgets), ('recorded_process_terminal_state', processes)]:
        audit.section(name, lambda function=function: function(audit))
    audit.section('source_and_artifact_final_recheck', audit.unchanged)
    final_state = readiness()
    assert final_state['ready']
    result = dict(status='verified' if not audit.issues else 'failed', started_utc=started,
                  finished_utc=utc(), api_calls=False, existing_artifacts_modified=False,
                  readiness=final_state, checks=audit.checks, issues=audit.issues,
                  prior_audit_attempt='completion-audit-attempt1.json: auditor-only pilot manifest serialization mismatch; preserved with audit_completion_attempt1.py',
                  audit_script=str(Path(__file__).resolve()),
                  audit_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  source_and_artifact_sha256=audit.hashes,
                  scope='Completion of the bounded Gate 1–7 core protocol; explicitly unrun plan checklist ablations remain incomplete. Final reports/figures are mutable presentation artifacts and are outside this hash audit. No new experiment, refit, scoring, provider reconciliation or billing mutation.')
    with args.out.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False); stream.write('\n')
    print(json.dumps(dict(status=result['status'], out=str(args.out), issues=audit.issues, files=len(audit.hashes))), flush=True)
    return 0 if not audit.issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
