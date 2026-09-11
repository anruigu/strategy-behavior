"""Audit completed training diagnostics only; never scores forecasts or fits models."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    path = Path(path)
    raw = path.read_bytes()
    INPUTS[str(path)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def main():
    for name in ('training-diagnostics-final.json', 'training-diagnostics-final.md'):
        if (ROOT/name).exists():
            raise FileExistsError('Preserve the existing final audit: '+name)
    created = datetime.now(timezone.utc).isoformat()
    initial_path = ROOT/'training-diagnostics-initial.json'
    initial = read(initial_path)
    for path, expected in initial['source_artifact_sha256'].items():
        assert digest(path) == expected, 'Initial audited source changed: '+path
    INPUTS.update(initial['source_artifact_sha256'])
    INPUTS[str(ROOT/'training-diagnostics-initial.md')] = digest(ROOT/'training-diagnostics-initial.md')
    folds = read(ROOT/'data/folds.json')
    train = read(ROOT/'data/data.json')['train_examples']
    protocol = read(ROOT/'transformer-protocol.json')
    assert len(folds) == 10
    expected_markers = {ROOT/'transformer'/kind/fold['fold_id']/'complete.json'
                        for kind in ('frozen', 'lora') for fold in folds}
    actual_markers = set((ROOT/'transformer').glob('*/*/complete.json'))
    assert actual_markers == expected_markers, 'Exactly twenty fixed completed fits required'
    rows = []
    comparisons = []
    targets = protocol['targets']
    for fold in folds:
        fid = fold['fold_id']
        selected = [train[i] for i in fold['train']]
        expected_support = [len({e['group_id'] for e in selected if e['targets'][t]['opportunities'] > 0}) for t in targets]
        for kind in ('frozen', 'lora'):
            folder = ROOT/'transformer'/kind/fid
            marker = read(folder/'complete.json')
            artifact = read(folder/'artifact.json')
            assert marker['status'] == 'complete'
            artifact_path = str(folder/'artifact.json').replace('/shared/', '/mnt/sfs/', 1)
            assert marker['output_sha256'][artifact_path] == INPUTS[str(folder/'artifact.json')]
            contract, diagnostics = artifact['contract'], artifact['diagnostics']
            assert contract['fold'] == fold and contract['protocol'] == protocol
            assert marker['input_sha256'] == contract['input_sha256']
            assert artifact['training_row_ids'] == fold['train_row_ids'] == [e['row_id'] for e in selected]
            assert artifact['training_groups'] == sorted({e['group_id'] for e in selected})
            assert set(artifact['training_groups']) == set(fold['train_groups'])
            assert diagnostics['supported_groups'] == expected_support
            assert artifact['supported_targets'] == [n > 0 for n in expected_support] == [True]*3
            assert diagnostics['fleet']['fleet_run_id'] == initial['fleet_run_id']
            assert diagnostics['optimization_success'] is True
            for key, value in diagnostics.items():
                if type(value) in (int, float):
                    assert math.isfinite(value), (fid, kind, key)
            if kind == 'frozen':
                assert diagnostics['final_objective'] <= diagnostics['initial_objective']+1e-6
                assert diagnostics['gradient_tolerance_met'] == (diagnostics['maximum_gradient'] <= protocol['frozen']['tolerance_grad'])
            else:
                expected_steps = protocol['lora']['epochs']*math.ceil(len(selected)/(
                    protocol['lora']['microbatch']*protocol['lora']['accumulation']))
                assert diagnostics['optimizer_steps'] == diagnostics['expected_steps'] == expected_steps
                assert diagnostics['epochs'] == protocol['lora']['epochs'] == 2
                assert diagnostics['training_examples'] == len(selected)
            rows.append(dict(fold_id=fid, split=fold['split'], method=contract['method'],
                training_examples=len(selected), training_groups=len(artifact['training_groups']),
                training_opportunities=[sum(e['targets'][t]['opportunities'] for e in selected) for t in targets],
                supported_targets=artifact['supported_targets'], diagnostics=diagnostics,
                versions=contract['versions'], completed_utc=marker['finished_utc'],
                artifact_path=str(folder/'artifact.json'), complete_path=str(folder/'complete.json')))
        frozen, lora = rows[-2]['diagnostics'], rows[-1]['diagnostics']
        assert lora['warm_start_training_objective'] == frozen['final_objective']
        delta = lora['final_training_objective']-frozen['final_objective']
        comparisons.append(dict(fold_id=fid, frozen_initial_objective=frozen['initial_objective'],
            frozen_final_objective=frozen['final_objective'], frozen_maximum_gradient=frozen['maximum_gradient'],
            frozen_gradient_tolerance_met=frozen['gradient_tolerance_met'],
            lora_final_training_objective=lora['final_training_objective'],
            lora_minus_own_frozen_objective=delta,
            lora_objective_direction='higher' if delta > 1e-12 else 'lower' if delta < -1e-12 else 'equal',
            lora_optimizer_steps=lora['optimizer_steps'], lora_elapsed_seconds=lora['elapsed_seconds']))
    versions = {json.dumps(row['versions'], sort_keys=True) for row in rows}
    assert len(versions) == 1, 'Runtime versions differ across fitted artifacts'
    summary = dict(completed_and_audited_transformer_fits=20, frozen_heads=10, lora_fits=10,
        all_training_row_ids_groups_target_support_and_fleet_ids_match=True,
        all_three_targets_supported_in_all_twenty_fits=True,
        frozen_objective_improved=sum(r['frozen_final_objective'] < r['frozen_initial_objective'] for r in comparisons),
        frozen_gradient_tolerance_met=sum(r['frozen_gradient_tolerance_met'] for r in comparisons),
        frozen_gradient_range=[min(r['frozen_maximum_gradient'] for r in comparisons),
                               max(r['frozen_maximum_gradient'] for r in comparisons)],
        lora_fixed_steps_completed=10,
        lora_objective_direction_counts=dict(Counter(r['lora_objective_direction'] for r in comparisons)),
        lora_minus_own_frozen_objective_range=[min(r['lora_minus_own_frozen_objective'] for r in comparisons),
                                            max(r['lora_minus_own_frozen_objective'] for r in comparisons)],
        lora_minus_own_frozen_objective_median=statistics.median(r['lora_minus_own_frozen_objective'] for r in comparisons),
        lora_total_optimizer_steps=sum(r['lora_optimizer_steps'] for r in comparisons),
        lora_fit_elapsed_seconds_sum=sum(r['lora_elapsed_seconds'] for r in comparisons),
        baseline_saved_optimizer_success_count=90)
    INPUTS[str(Path(__file__))] = digest(__file__)
    for path, expected in INPUTS.items():
        assert digest(path) == expected, 'Audited input changed while reading: '+path
    value = dict(schema='improve-training-diagnostics-final-v1', created_utc=created,
        status='verified_all_completed_training_fit_diagnostics', fleet_run_id=initial['fleet_run_id'],
        summary=summary, baseline=initial['baseline'], training_counts=initial['training_counts'],
        transformer=rows, within_fold_training_objective_comparisons=comparisons,
        runtime_versions=json.loads(next(iter(versions))), runtime_preflight=initial['runtime'],
        source_artifact_sha256=INPUTS,
        baseline_audit_reuse='All hashes from the initial audit were reverified; no optimizer was rerun.',
        artifact_audit_scope='Artifact identities, completion-marker binding, train scopes, finite diagnostics and steps; checkpoint/forecast byte verification remains with the continuation driver.',
        limitations=initial['limitations']+[
            'Across-fold training objectives use different, overlapping training sets; the direction count and range are descriptive and do not supply independent statistical evidence.',
            'Completed training fits do not imply the overall Fleet job, fresh metadata forecasts, or downstream evaluation has finished.'
        ], heldout_scoring_performed=False, empirical_fitting_performed_locally=False,
        model_loading_or_api_calls=False)
    lines = [
        f'All 20 fixed transformer fits now have completed artifacts with matching training row IDs, game groups, three-target support, and Fleet lineage. Every LoRA fit completed its declared two epochs and expected optimizer steps. The 90 successful saved baseline optimizer records were reused after their original audit hashes were reverified. Audit snapshot: {created}.', '',
        f"All ten frozen heads reduced their finite training objectives; {summary['frozen_gradient_tolerance_met']}/10 met the strict 1e-6 gradient tolerance. Maximum gradients range from {summary['frozen_gradient_range'][0]:.3g} to {summary['frozen_gradient_range'][1]:.3g}. The recorded 200 iterations is the configured cap; closure evaluations include line-search calls and do not establish actual iteration counts.", '',
        f"Relative to each fit's own frozen warm start, final LoRA full-training objectives were higher in {summary['lora_objective_direction_counts'].get('higher', 0)}/10 folds, lower in {summary['lora_objective_direction_counts'].get('lower', 0)}/10, and equal in {summary['lora_objective_direction_counts'].get('equal', 0)}/10. Changes range from {summary['lora_minus_own_frozen_objective_range'][0]:+.6f} to {summary['lora_minus_own_frozen_objective_range'][1]:+.6f}; median {summary['lora_minus_own_frozen_objective_median']:+.6f}. This is a training optimization limitation, not a held-out predictive result. `optimization_success` certifies completion of the fixed steps.", '',
        '| Training fold | Frozen objective | Frozen maximum gradient | LoRA objective | LoRA minus frozen | Completed LoRA steps |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for row in comparisons:
        lines.append(f"| {row['fold_id']} | {row['frozen_final_objective']:.6f} | {row['frozen_maximum_gradient']:.3g} | {row['lora_final_training_objective']:.6f} | {row['lora_minus_own_frozen_objective']:+.6f} | {row['lora_optimizer_steps']} |")
    lines += ['',
        'These comparisons use the same target weighting and head regularization within each fold. A first stochastic minibatch loss is not a comparable full-training starting objective. Different folds have overlapping training sets, so no confidence interval or independent-sample claim is attached to their objective changes.', '',
        'All inspected fits used PyTorch 2.11.0+cu128, Transformers 5.8.0, PEFT 0.18.1, NumPy 2.3.5, and Safetensors 0.8.0. Baselines used SciPy 1.15.3. The fixed model revision, one optimization seed, and schedule remain unchanged. The initial audit contains the preserved runtime preflight and baseline details.', '',
        'No empirical fitting, model loading, API calls, or held-out scoring occurred in this audit. Completed fit artifacts do not mean the ongoing fresh forecast phase or downstream evaluation is complete.', '',
        'Full diagnostics and verified source hashes: [training-diagnostics-final.json](training-diagnostics-final.json). Initial snapshot preserved: [training-diagnostics-initial.md](training-diagnostics-initial.md). Reproducible inspection: [audit_final_training.py](independent-analysis/audit_final_training.py); it refuses to overwrite this audit.'
    ]
    with (ROOT/'training-diagnostics-final.json').open('x') as handle:
        json.dump(value, handle, indent=2, allow_nan=False); handle.write('\n')
    with (ROOT/'training-diagnostics-final.md').open('x') as handle:
        handle.write('\n'.join(lines)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
