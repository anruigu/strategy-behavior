"""Read-only training diagnostics; writes a new immutable audit, never fits/scores."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {}


def read(path):
    path = Path(path)
    raw = path.read_bytes()
    INPUTS[str(path)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def main():
    created = datetime.now(timezone.utc).isoformat()
    completion = read(ROOT/'baselines/completion.json')
    run = read(ROOT/'baselines/run.json')
    artifacts = read(ROOT/'baselines/fits.json')
    folds = {f['fold_id']: f for f in read(ROOT/'data/folds.json')}
    # Only train_examples is inspected; development labels are never used.
    train = read(ROOT/'data/data.json')['train_examples']
    protocol = read(ROOT/'transformer-protocol.json')
    preflight = read(ROOT/'fleet-runtime/model-preflight.json')
    backend = read(ROOT/'fleet-runtime/retry-3/worker-backend.json')
    targets = ['action0', 'cooperation', 'coordination']
    assert completion['status'] == 'complete' and completion['folds'] == len(folds) == 10
    assert completion['run_id'] == run['run_id'] == preflight['fleet']['fleet_run_id']
    assert completion['forecast_rows'] == sum(len(f['test'])*3*7 for f in folds.values())
    optimizers = []
    fold_counts = []
    for fid, artifact in artifacts.items():
        fold = folds[fid]
        assert artifact['training_row_ids'] == fold['train_row_ids']
        selected = [train[i] for i in fold['train']]
        assert [e['row_id'] for e in selected] == artifact['training_row_ids']
        fold_counts.append(dict(fold_id=fid, examples=len(selected), groups=len(fold['train_groups'])))
        for target, methods in artifact['fits'].items():
            assert len(methods) == 7
            for method, fit in methods.items():
                if 'optimizer' not in fit:
                    continue
                optimizer = fit['optimizer']
                assert optimizer['converged'] and all(math.isfinite(v) for v in optimizer['coefficients'])
                assert math.isfinite(optimizer['objective']) and math.isfinite(optimizer['gradient_max'])
                optimizers.append(dict(fold_id=fid, target=target, method=method,
                    **{k: v for k, v in optimizer.items() if k != 'coefficients'}))
    assert len(optimizers) == 90
    selected_folds = ['family_anti_coordination', 'family_chicken']
    inspected = []
    for fid in selected_folds:
        for kind in ('frozen', 'lora'):
            folder = ROOT/'transformer'/kind/fid
            complete = read(folder/'complete.json')
            artifact = read(folder/'artifact.json')
            assert complete['status'] == 'complete'
            remote_artifact = str(folder/'artifact.json').replace('/shared/', '/mnt/sfs/', 1)
            assert complete['output_sha256'][remote_artifact] == INPUTS[str(folder/'artifact.json')]
            fold = artifact['contract']['fold']
            diagnostics = artifact['diagnostics']
            assert fold == folds[fid]
            assert artifact['training_row_ids'] == fold['train_row_ids']
            assert diagnostics['fleet']['fleet_run_id'] == completion['run_id']
            selected = [train[i] for i in fold['train']]
            support = [len({e['group_id'] for e in selected if e['targets'][t]['opportunities'] > 0}) for t in targets]
            assert diagnostics['supported_groups'] == support
            assert artifact['supported_targets'] == [True, True, True]
            if kind == 'lora':
                assert diagnostics['optimization_success'] is True
                assert diagnostics['optimizer_steps'] == diagnostics['expected_steps'] == 62
                assert math.isfinite(diagnostics['final_training_objective'])
            else:
                assert diagnostics['final_objective'] < diagnostics['initial_objective']
                assert math.isfinite(diagnostics['maximum_gradient'])
            inspected.append(dict(method=artifact['contract']['method'], fold_id=fid,
                examples=len(selected), groups=len(artifact['training_groups']),
                supported_targets=artifact['supported_targets'], diagnostics=diagnostics,
                versions=artifact['contract']['versions'], completion_finished_utc=complete['finished_utc'],
                objective_change_from_warm_start=(diagnostics['final_training_objective']-
                    diagnostics['warm_start_training_objective']) if kind == 'lora' else None))
    observed_markers = sorted(str(p.relative_to(ROOT)) for p in (ROOT/'transformer').glob('*/*/complete.json')
                              if p.parent.name not in selected_folds)
    scope = dict(inspected_transformer_fits=4, planned_transformer_fits=20,
        inspected_frozen_heads=2, inspected_lora_fits=2,
        other_completion_markers_observed_but_not_audited=observed_markers,
        first_two_lora_folds=selected_folds,
        full_training_complete_claim=False)
    elapsed = (datetime.fromisoformat(completion['created_utc'])-
               datetime.fromisoformat(completion['started_utc'])).total_seconds()
    method_summaries = {}
    for method in ('calibrated_payoff_dominant', 'normalized_logistic', 'combined_logistic'):
        rows = [r for r in optimizers if r['method'] == method]
        method_summaries[method] = dict(optimizers=len(rows),
            iterations=[min(r['iterations'] for r in rows), max(r['iterations'] for r in rows)],
            maximum_gradient=max(r['gradient_max'] for r in rows),
            ridge_counts=dict(Counter(str(r['alpha']) for r in rows)))
    train_counts = dict(examples=len(train), groups=len({e['group_id'] for e in train}),
        opportunities={t: sum(e['targets'][t]['opportunities'] for e in train) for t in targets},
        supported_groups={t: len({e['group_id'] for e in train if e['targets'][t]['opportunities'] > 0}) for t in targets})
    value = dict(schema='improve-training-diagnostics-initial-v1', created_utc=created,
        status='verified_initial_completed_training_artifacts', fleet_run_id=completion['run_id'],
        scope=scope, source_artifact_sha256=INPUTS,
        baseline=dict(completed_folds=10, target_method_fits=210, saved_optimized_fits=90,
            all_saved_optimizers_report_success=True, elapsed_seconds=elapsed,
            versions={k: run[k] for k in ('numpy', 'scipy')}, method_summaries=method_summaries,
            maximum_gradient=max(o['gradient_max'] for o in optimizers),
            optimizers_with_raw_gradient_at_most_1e_8=sum(o['gradient_max'] <= 1e-8 for o in optimizers),
            fold_counts=fold_counts, optimizer_diagnostics=optimizers),
        training_counts=train_counts, transformer=inspected,
        runtime=dict(preflight_status=preflight['status'], versions=preflight['versions'], cuda=preflight['cuda'],
            gpu=preflight['gpu'], token_lengths=preflight['token_lengths'], token_limit=protocol['input']['max_tokens'],
            preflight_pooled_shape=preflight['pooled_shape'], preflight_pooled_finite=preflight['pooled_finite'],
            worker_attention_backend=backend['after']),
        limitations=[
            'Baseline optimizer success does not imply the raw maximum gradient meets 1e-8: L-BFGS-B also stops on relative objective change; exact termination messages were not saved.',
            'Both inspected frozen heads reduced finite full-training objectives but missed the frozen 1e-6 gradient tolerance. maximum_iterations=200 records the configured cap, not a saved actual iteration count; closure evaluations include line-search calls.',
            'Both inspected LoRA fits completed exactly two epochs/62 steps, but their final full-training objectives exceeded the same-fold frozen warm-start objectives. optimization_success means fixed-step completion, not convergence or improvement.',
            'The first observed stochastic minibatch loss is not a full-training initial objective and must not be compared directly with the final full-training loss.',
            'Training objective comparisons do not establish held-out predictive performance. One fixed optimization seed and schedule remain the declared scope.'
        ], heldout_scoring_performed=False, empirical_fitting_performed_locally=False,
        model_loading_or_api_calls=False)
    source = Path(__file__)
    INPUTS[str(source)] = hashlib.sha256(source.read_bytes()).hexdigest()
    for path, expected in INPUTS.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
    out = ROOT/'training-diagnostics-initial.json'
    with out.open('x') as handle:
        json.dump(value, handle, indent=2, allow_nan=False); handle.write('\n')
    lines = [
        f'The initial training audit found no finite-value, training-scope, target-support, or fixed-step completion failures in the inspected artifacts. This is a partial audit: all ten baseline folds and the first two completed LoRA folds with their matching frozen heads (4 of 20 transformer fits), as of {created}.',
        '',
        f'All 90 saved baseline optimizers report successful termination in 6–166 iterations; coefficients and objectives are finite. The ten-fold baseline stage took {elapsed:.1f} seconds. Maximum raw gradient is 6.63e-7; only 27/90 meet 1e-8, so successful termination should not be described as universal gradient-tolerance convergence. Exact SciPy termination messages were not retained.',
        '',
        '| Held-out family defining training fold | Frozen initial → final objective | Frozen maximum gradient | LoRA final objective | Change from frozen warm start | Fixed LoRA steps |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for fid in selected_folds:
        f = next(r['diagnostics'] for r in inspected if r['fold_id'] == fid and r['method'] == 'qwen3_frozen_head')
        l = next(r for r in inspected if r['fold_id'] == fid and r['method'] == 'qwen3_lora_head')
        d = l['diagnostics']
        lines.append(f"| {fid} | {f['initial_objective']:.6f} → {f['final_objective']:.6f} | {f['maximum_gradient']:.3g} | {d['final_training_objective']:.6f} | +{l['objective_change_from_warm_start']:.6f} | 62/62 |")
    lines += ['',
        'Both frozen heads missed the configured 1e-6 gradient tolerance. Their 209/215 closure evaluations include line-search calls; the artifact records the configured 200-iteration cap, not actual optimizer iteration counts. LoRA finished its fixed two epochs with finite diagnostics, but both full-training objectives worsened from the frozen starting point. These are reportable optimization limitations; neither proves worse held-out prediction. The first stochastic minibatch loss is not a comparable full-training starting loss.',
        '',
        'Training counts match the fixed scopes: 1,152 aggregated contexts across 72 shapes; action/cooperation/coordination have 30,688/22,368/17,888 opportunities across 72/52/42 supported shapes. Both audited fold pairs support all three targets, with matching row IDs and supported-group counts.',
        '',
        'Runtime: Python 3.12 worker environment, PyTorch 2.11.0+cu128, Transformers 5.8.0, PEFT 0.18.1, NumPy 2.3.5, SciPy 1.15.3, Safetensors 0.8.0, CUDA 12.8 on NVIDIA B300 SXM6. The recorded backend disables only cuDNN SDPA. Technical preflight passed with finite 2,560-dimensional representations; input lengths 266–284 fit the 512-token limit. Preflight lengths include metadata-only queries; no held-out outcome scores were computed.',
        '',
        'The fixed single optimization seed and schedule remain unchanged. No empirical fitting, model loading, inference/API calls, or held-out scoring occurred during this audit. This audit does not certify the remaining transformer fits.',
        '',
        'Detailed diagnostics and before/after-verified source hashes: [training-diagnostics-initial.json](training-diagnostics-initial.json). Reproducible read-only inspection and immutable audit writer: [audit_initial_training.py](independent-analysis/audit_initial_training.py). Rerunning preserves this initial snapshot by refusing to overwrite it.',
    ]
    with (ROOT/'training-diagnostics-initial.md').open('x') as handle:
        handle.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(output=str(out), inspected=scope, maximum_baseline_gradient=value['baseline']['maximum_gradient'])))


if __name__ == '__main__':
    main()
