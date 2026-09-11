"""Synthetic continuation tests: no subprocess/model/Fleet calls or real outcomes."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from prediction.improve.post_training import (METHODS, NUMERICAL, Work, execution_lock,
    hashes, normalize_scope, record_evidence, verify_record_inputs, selection_contract, run, save, sha)
from prediction.improve.prospective_design import forecast_coverage

TMP = '/shared/allie/home/.codex/tmp'


class FakeWork:
    def __init__(self, proceed=True): self.events = []; self.proceed = proceed
    def prepare(self): self.events.append('prepare')
    def step(self, name, fn, *args): return fn()
    def audit_training(self): self.events.append('audit_training')
    def score_development(self): self.events.append('score_development')
    def apply_gate(self): self.events.append('gate'); return self.proceed
    def prompts(self): self.events.append('prompts')
    def freeze(self): self.events.append('freeze')
    def players(self): self.events.append('players')
    def collect(self): self.events.append('collect')
    def score_fresh(self): self.events.append('score_fresh')
    def render(self): self.events.append('render')


def fixture(root, status='complete'):
    save(root/'fleet-runtime/main-submit.json', {'response': {'name': 'existing-job'}})
    save(root/'training-freeze.json', {'absolute_conservative_deadline': '2026-09-10T20:00:00+00:00'})
    if status:
        save(root/'fleet-runtime/training-status.json', {'fleet_run_id': 'existing-job', 'status': status})


def forecast_fixture():
    queries = [dict(row_id='q1', game_id='g1', group_id='shape1', model='a', opponent='b', family='harmony',
                    applicability=dict(cooperative_action=0, cooperation=True, coordination=False))]
    scope = dict(scope_id='full', setting='full', query_row_ids=['q1'])
    rows = [dict(**{k: queries[0][k] for k in ('row_id','game_id','group_id','model','opponent')},
                 method=m, fold_id='full', split='fresh_full', target=t, prediction=None if t=='coordination' else .4)
            for m in METHODS for t in ('action0','cooperation','coordination')]
    return scope, queries, rows


class PostTrainingTests(unittest.TestCase):
    def test_default_dryrun_never_constructs_services_or_writes_state(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root = Path(folder)
            def forbidden(*args): raise AssertionError('Default constructed executable services')
            result = run(root, work_factory=forbidden)
            self.assertEqual(result['status'], 'dry_run')
            self.assertFalse(result['paid_calls']); self.assertFalse(result['fleet_calls'])
            self.assertEqual(list(root.iterdir()), [])

    def test_negative_gate_stops_before_prompted_or_player_calls(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder, patch('prediction.improve.post_training.competitors', return_value=[]):
            root = Path(folder); fixture(root); work = FakeWork(False)
            result = run(root, True, work_factory=lambda *a: work)
            self.assertEqual(result['status'], 'stopped_at_development_gate')
            self.assertEqual(work.events, ['prepare','audit_training','score_development','gate','render'])

    def test_positive_or_inconclusive_gate_freezes_before_players_and_finishes_neutrally(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder, patch('prediction.improve.post_training.competitors', return_value=[]):
            root = Path(folder); fixture(root); work = FakeWork()
            result = run(root, True, work_factory=lambda *a: work)
            self.assertEqual(work.events, ['prepare','audit_training','score_development','gate','prompts','freeze','players','collect','score_fresh','render'])
            self.assertEqual(result['status'], 'fresh_results_complete_interpretation_pending')
            self.assertNotIn('success', result['interpretation'].lower())

    def test_wait_reads_existing_job_only_and_failure_or_deadline_stops(self):
        for mode in ('wait', 'error', 'deadline'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(dir=TMP) as folder, patch('prediction.improve.post_training.competitors', return_value=[]):
                root = Path(folder); fixture(root, 'error' if mode=='error' else 'running'); work = FakeWork(False)
                sleeps = []
                def sleep(seconds):
                    sleeps.append(seconds)
                    save(root/'fleet-runtime/training-status.json', {'fleet_run_id':'existing-job','status':'complete'})
                result = run(root, True, deadline='1970-01-01T00:00:10+00:00', poll=3,
                             clock=lambda: 20 if mode=='deadline' else 0, sleep=sleep, work_factory=lambda *a: work)
                if mode=='wait': self.assertEqual(sleeps, [3]); self.assertIn('score_development', work.events)
                else:
                    self.assertEqual(result['status'], 'training_blocked')
                    self.assertEqual(work.events, ['prepare','render']); self.assertEqual(sleeps, [])
                    self.assertIn('technical', result['behavioral_conclusion'])

    def test_terminal_local_monitor_without_completed_worker_blocks_without_wait_or_calls(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder, patch('prediction.improve.post_training.competitors', return_value=[]):
            root=Path(folder); fixture(root, 'running'); work=FakeWork()
            save(root/'fleet-runtime/main-monitor/completion.json', {'name':'existing-job','status':'failed'})
            result=run(root, True, work_factory=lambda *a: work, sleep=lambda seconds:self.fail('Slept after terminal monitor'))
            self.assertEqual(result['status'],'training_blocked')
            self.assertEqual(work.events,['prepare','render'])

    def test_foreign_training_job_is_rejected_without_downstream_actions(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder, patch('prediction.improve.post_training.competitors', return_value=[]):
            root = Path(folder); fixture(root)
            save(root/'fleet-runtime/training-status.json', {'fleet_run_id':'other-job','status':'complete'})
            work = FakeWork()
            with self.assertRaisesRegex(ValueError, 'Different Fleet job'): run(root, True, work_factory=lambda *a: work)
            self.assertEqual(work.events, ['prepare'])

    def test_execution_lock_and_live_competitor_reject_second_owner(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root = Path(folder)
            with patch('prediction.improve.post_training.competitors', return_value=[]):
                with execution_lock(root):
                    with self.assertRaisesRegex(RuntimeError, 'lock'):
                        with execution_lock(root): pass
            with patch('prediction.improve.post_training.competitors', return_value=[4321]):
                with self.assertRaisesRegex(RuntimeError, 'competing'):
                    with execution_lock(root): pass

    def test_completed_step_reuse_verifies_direct_and_nested_artifacts(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root = Path(folder); source = root/'source.py'; source.write_text('frozen')
            work = Work(root, 0); work.folder.mkdir(); work.plan = {'input_sha256': hashes([source])}
            save(work.folder/'plan.json', work.plan)
            output, audit = root/'forecasts.jsonl', root/'audit.json'; count=[]
            def operation():
                count.append(1); output.write_text('forecast')
                save(audit, {'output_sha256': hashes([output])})
            work.step('score', operation, [source], [audit])
            work.step('score', operation, [source], [audit]); self.assertEqual(count, [1])
            output.write_text('altered')
            with self.assertRaisesRegex(ValueError, 'changed'): work.step('score', operation, [source], [audit])
            output.write_text('forecast'); source.write_text('changed source')
            with self.assertRaisesRegex(ValueError, 'changed'): work.step('score', operation, [source], [audit])

    def test_running_step_with_live_child_never_relaunches(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root=Path(folder); work=Work(root,0); work.folder.mkdir(); work.plan={'input_sha256':{}}
            save(work.folder/'plan.json', work.plan)
            save(work.folder/'steps/call.json',dict(status='running',child_pid=555,
                 contract=dict(plan_sha256=sha(work.folder/'plan.json'),input_sha256={})))
            with patch('prediction.improve.post_training.alive',return_value=True):
                with self.assertRaisesRegex(RuntimeError,'still alive'):
                    work.step('call',lambda:self.fail('Relaunched a live child'))

    def test_normalization_keeps_failed_kimi_in_all_method_support(self):
        scope, queries, rows = forecast_fixture()
        rows = [r for r in rows if not (r['method']=='llm_few_shot' and r['target']=='action0')]
        normalized = normalize_scope(scope, queries, rows)
        missing = next(r for r in normalized if r['method']=='llm_few_shot' and r['target']=='action0')
        self.assertIsNone(missing['prediction'])
        coverage = forecast_coverage([scope], queries, normalized, METHODS, NUMERICAL)
        self.assertFalse(coverage['ready'])
        exclusion = dict(scope_id='full', method='llm_few_shot',reason='bounded technical failure',created_utc='2026-09-10T12:00:00+00:00')
        allowed = forecast_coverage([scope], queries, normalized, METHODS, NUMERICAL, [exclusion])
        self.assertTrue(allowed['ready'])
        cell = next(c for c in allowed['support'] if c['target']=='action0')
        self.assertEqual(cell['all_method_common_row_ids'], [])
        self.assertEqual(cell['numerical_common_row_ids'], ['q1'])

    def test_normalization_rejects_missing_numeric_duplicate_scope_and_role_errors(self):
        for mode in ('missing','duplicate','scope','opponent','outcome'):
            with self.subTest(mode=mode):
                scope, queries, rows = forecast_fixture()
                if mode=='missing': rows.pop(0)
                elif mode=='duplicate': rows.append(dict(rows[0]))
                elif mode=='scope': rows[0]['fold_id']='family_harmony'
                elif mode=='opponent': rows[0]['opponent']='wrong'
                else: rows[0]['successes']=1
                with self.assertRaises(ValueError): normalize_scope(scope,queries,rows)

    def test_existing_evaluation_cannot_omit_a_newly_required_forecast_input(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root=Path(folder); a=root/'numeric.jsonl'; b=root/'prompted.jsonl'
            a.write_text('numeric'); b.write_text('prompted'); marker=root/'audit.json'
            save(marker, {'source_sha256': hashes([a])})
            with self.assertRaisesRegex(ValueError, 'omitted'):
                verify_record_inputs(marker, [a,b])
            save(marker, {'source_sha256': hashes([a,b])})
            verify_record_inputs(marker, [a,b])

    def test_explicit_retry_paths_select_retry_and_ignore_only_known_prior_failure(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder, patch('prediction.improve.post_training.competitors', return_value=[]):
            root=Path(folder); fixture(root,'error'); original=sha(root/'fleet-runtime/main-submit.json')
            submission=root/'fleet-runtime/retry-1-submit.json'; config=root/'fleet-runtime/retry-1-config.json'
            monitor=root/'fleet-runtime/retry-1-monitor'
            save(submission,{'response':{'name':'retry-job-123','run_dir':str(root/'fleet-runtime/retry-1')}})
            save(config,{'name':'retry-job','run_dir':str(root/'fleet-runtime/retry-1')})
            save(root/'fleet-runtime/main-monitor/completion.json',{'name':'existing-job','status':'failed'})
            work=FakeWork(False); sleeps=[]
            def sleep(seconds):
                sleeps.append(seconds)
                save(root/'fleet-runtime/training-status.json',{'fleet_run_id':'retry-job-123','status':'complete'})
            result=run(root,True,work_factory=lambda *a:work,clock=lambda:0,sleep=sleep,
                       submission='fleet-runtime/retry-1-submit.json',config=config,monitor_dir=monitor)
            self.assertEqual(result['status'],'stopped_at_development_gate')
            self.assertEqual(len(sleeps),1)
            self.assertEqual((work.submission_path,work.config_path,work.monitor_dir),(submission,config,monitor))
            self.assertEqual(original,sha(root/'fleet-runtime/main-submit.json'))

    def test_work_prepare_binds_exact_retry_artifacts_and_monitor_directory(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root=Path(folder); fixture(root,'error')
            for name in ('gate-protocol.json','baseline-protocol.json','transformer-protocol.json','budget-policy.json',
                         'development-few-shot/forecasts.manifest.json'):
                save(root/name,{})
            save(root/'training-freeze.json',{'relative_sha256':{}})
            save(root/'inference-source-manifest.json',{'files':{}})
            save(root/'prospective-design/scopes.json',[])
            (root/'development-few-shot/forecasts.jsonl').write_text('')
            work=Work(root,0)
            work.submission_path=root/'fleet-runtime/retry-1-submit.json'
            work.config_path=root/'fleet-runtime/retry-1-config.json';work.monitor_dir=root/'fleet-runtime/retry-1-monitor'
            save(work.submission_path,{'response':{'name':'retry-job-123','run_dir':str(root/'fleet-runtime/retry-1')}})
            save(work.config_path,{'name':'retry-job','run_dir':str(root/'fleet-runtime/retry-1'),'bootstrap':'scipy'})
            with patch('prediction.improve.post_training.verify_prepared',return_value={}): work.prepare()
            self.assertEqual(work.plan['existing_fleet_run_id'],'retry-job-123')
            self.assertEqual(work.plan['monitor_dir'],str(work.monitor_dir))
            for path in (work.submission_path,work.config_path,root/'fleet-runtime/main-submit.json'):
                self.assertEqual(work.plan['input_sha256'][str(path)],sha(path))
            work.monitor_dir=root/'fleet-runtime/other-monitor'
            with patch('prediction.improve.post_training.verify_prepared',return_value={}):
                with self.assertRaisesRegex(ValueError,'Immutable'):work.prepare()

    def test_selected_submission_config_mismatch_and_cross_run_paths_rejected(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root=Path(folder);submission=root/'submit.json';config=root/'config.json'
            save(submission,{'response':{'name':'retry-abc','run_dir':str(root/'runtime')}})
            save(config,{'name':'different','run_dir':str(root/'runtime')})
            with self.assertRaisesRegex(ValueError,'name differs'):selection_contract(root,submission,config,root/'monitor')
            with self.assertRaisesRegex(ValueError,'inside this run'):run(root,submission='/shared/allie/another-run/submit.json')

    def test_scalar_prompt_manifest_hashes_verify_exact_source_and_output(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root=Path(folder);source=root/'source.jsonl';output=root/'forecasts.jsonl';marker=root/'forecasts.manifest.json'
            source.write_text('saved source');output.write_text('joined output')
            save(marker,{'source':str(source),'source_sha256':sha(source),'output_sha256':sha(output)})
            evidence=record_evidence(marker)
            self.assertEqual(evidence[str(output)],sha(output))
            self.assertEqual(record_evidence(marker,output),evidence)
            verify_record_inputs(marker,[source])
            output.write_text('altered output')
            with self.assertRaisesRegex(ValueError,'changed'):record_evidence(marker)
            unbound=root/'unbound.json';save(unbound,{'output_sha256':'a'*64})
            with self.assertRaisesRegex(ValueError,'artifact path'):record_evidence(unbound)

    def test_remote_evidence_paths_are_mapped_without_changing_hash_requirements(self):
        with tempfile.TemporaryDirectory(dir=TMP) as folder:
            root=Path(folder); data=root/'data.json'; data.write_text('{}')
            remote=str(data).replace('/shared/','/mnt/sfs/',1)
            marker=root/'complete.json';save(marker,{'output_sha256':{remote:sha(data)}})
            self.assertEqual(record_evidence(marker)[str(data)],sha(data))
            data.write_text('{"changed":true}')
            with self.assertRaises(ValueError):record_evidence(marker)


if __name__=='__main__':unittest.main()
