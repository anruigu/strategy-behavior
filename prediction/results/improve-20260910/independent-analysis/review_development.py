"""Read saved scores and verify their interpretation; no fitting or rescoring."""
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {}
TARGETS = ('action0', 'cooperation', 'coordination')
HEADS = ('qwen3_frozen_head', 'qwen3_lora_head')
STRONG = ('calibrated_payoff_dominant', 'normalized_logistic', 'combined_logistic', 'family')


def local(path):
    return Path(str(path).replace('/mnt/sfs/', '/shared/', 1))


def sha(path):
    return hashlib.sha256(local(path).read_bytes()).hexdigest()


def read(path):
    path = local(path); raw = path.read_bytes()
    INPUTS[str(path)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def verify(table):
    for path, expected in table.items():
        assert sha(path) == expected, path


def interval_text(value):
    return f"{value['improvement']:+.4f} [{value['lower']:+.4f}, {value['upper']:+.4f}]"


def main():
    output = ROOT/'development-review.json'
    assert not output.exists() and not (ROOT/'development-review.md').exists()
    folder = ROOT/'development-evaluation'
    audit = read(folder/'audit.json')
    assert audit['status'] == 'verified' and not audit['incomplete_override'] and not audit['omitted_forecasts']
    verify(audit['source_sha256']); verify(audit['source_code_sha256']); verify(audit['output_sha256'])
    INPUTS.update({str(local(p)): h for p, h in audit['output_sha256'].items()})
    scores = read(folder/'scores.json'); pairs = read(folder/'paired-comparisons.json')
    gate = read(ROOT/'development-gate.json'); protocol = read(ROOT/'gate-protocol.json')
    training = read(ROOT/'training-diagnostics-final.json')
    verify(gate['input_sha256']); verify(training['source_artifact_sha256'])
    assert gate['protocol'] == protocol
    assert scores['bootstrap_repetitions'] == 500 and scores['seed'] == 20260910
    index = {(r['support'], r['split'], r['target'], r['method']): r
             for r in scores['scores'] if r['family'] == 'all'}
    pindex = {(r['support'], r['split'], r['target'], r['baseline'], r['method']): r
              for r in pairs if r['family'] == 'all'}
    coverage = scores['coverage']
    assert len(coverage) == 24
    for cell in coverage:
        assert cell['common_examples'] == cell['planned_eligible_examples']
        assert set(cell['omitted_or_null_by_method'].values()) == {0}
    for split, methods in scores['available_methods_by_split'].items():
        assert ('llm_few_shot' in methods) == (split == 'development')
        assert len(methods) == (10 if split == 'development' else 9)
    assert audit['method_declared_scopes']['llm_few_shot'] == [['development', 'full']]
    group_sets = defaultdict(dict)
    for line in (folder/'group-level.jsonl').read_text().splitlines():
        row = json.loads(line)
        key = row['support'], row['split'], row['target'], row['method']
        assert row['group_id'] not in group_sets[key]
        group_sets[key][row['group_id']] = {k: row[k] for k in ('examples', 'opportunities', 'successes', 'episodes', 'family')}
    support_checks = []
    for split in scores['available_methods_by_split']:
        for target in TARGETS:
            reference = group_sets['numerical_only', split, target, 'calibrated_payoff_dominant']
            for support in ('numerical_only', 'all_methods'):
                methods = next(c['methods'] for c in coverage if (c['support'], c['split'], c['target']) == (support, split, target))
                for method in methods:
                    assert group_sets[support, split, target, method] == reference
            support_checks.append(dict(split=split, target=target, games=len(reference),
                examples=sum(r['examples'] for r in reference.values()),
                opportunities=sum(r['opportunities'] for r in reference.values()),
                exact_game_identity_and_count_support_equal=True))
    gate_checks = []
    for split in ('family', 'development'):
        for target in TARGETS:
            best = min(STRONG, key=lambda m: (index['numerical_only', split, target, m]['event_brier'], m))
            for method in HEADS:
                pair = pindex['numerical_only', split, target, best, method]
                interval = pair['game_bootstrap']['intervals']['event_brier']
                difference = index['numerical_only', split, target, best]['event_brier']-index['numerical_only', split, target, method]['event_brier']
                assert abs(difference-interval['improvement']) < 1e-12
                match = [c for c in gate['cells'] if (c['split'], c['target'], c['method']) == (split, target, method)]
                assert len(match) == 1 and match[0]['strongest_declared_baseline'] == best
                assert all(match[0][k] == interval[k] for k in ('improvement', 'lower', 'upper'))
                negative = interval['improvement'] < 0 and interval['upper'] < protocol['meaningful_brier_gain']
                assert match[0]['negative'] == negative
                gate_checks.append(dict(split=split, target=target, method=method, baseline=best,
                    baseline_brier=index['numerical_only', split, target, best]['event_brier'],
                    transformer_brier=index['numerical_only', split, target, method]['event_brier'],
                    interval=interval, negative=negative))
    assert len(gate_checks) == 12 and all(c['negative'] for c in gate_checks)
    assert all(c['interval']['upper'] < 0 for c in gate_checks)
    assert gate['status'] == 'stop_consistent_negative_development' and gate['proceed'] is False
    no_fresh = dict(player_status_exists=(ROOT/'fresh-prospective/status.json').exists(),
        trace_count=len(list((ROOT/'fresh-prospective/episodes').glob('*/trace.json'))),
        collected_outcomes_directory_exists=(ROOT/'fresh-collected').exists(),
        fresh_score_directory_exists=(ROOT/'fresh-evaluation').exists())
    assert not any(no_fresh.values())
    selected_pairs = [r for r in pairs if r['support'] == 'numerical_only' and r['family'] == 'all'
        and r['split'] in ('family', 'development') and r['baseline'] in ('calibrated_payoff_dominant', 'qwen3_frozen_head')]
    source = Path(__file__); INPUTS[str(source)] = sha(source)
    verify(INPUTS); verify(audit['source_sha256'])
    value = dict(schema='improve-independent-development-review-v1', created_utc=datetime.now(timezone.utc).isoformat(),
        source_artifact_sha256=INPUTS, score_audit_source_and_output_hashes_verified=True,
        gate_independently_recomputed=True, gate_status=gate['status'], gate_cells=gate_checks,
        source_forecast_rows=audit['forecast_rows'], exact_support_checks=support_checks,
        kimi_scope='Reused saved forecasts on old21 development only; absent from all retrospective folds.',
        aggregate_scores=[r for r in scores['scores'] if r['family'] == 'all' and
            (r['support'] == 'numerical_only' or r['method'] == 'llm_few_shot')],
        fixed_comparator_and_head_contrasts=selected_pairs,
        fresh_observation_checks=no_fresh, training_diagnostics=training['summary'],
        interpretation='This fixed Qwen3-4B representation and two-epoch LoRA setup failed the declared development resource gate; this does not establish impossibility of useful transformer fine-tuning.',
        fitting_or_new_forecast_scoring_performed=False, api_calls=False)
    lines = [
        'The fixed development stop is correct. Both Qwen heads are worse than the strongest declared numerical comparator on every target in both leave-family-out evaluation and old21 development. All twelve saved paired Brier intervals have upper bounds below zero, satisfying the stronger condition needed to exclude a +0.005 meaningful gain. No fresh player status, traces, collected outcomes, or fresh evaluation exists.', '',
        'All values below use equal mass per eligible canonical game and event weights within a game. Intervals are the saved 95% percentile intervals from 500 whole-game bootstrap samples; positive baseline-minus-head gain favors the head.', '',
        '| Split / target | Strongest declared numerical comparator | Its Brier | Calibrated theory Brier | Frozen Brier | LoRA Brier |',
        '|---|---|---:|---:|---:|---:|',
    ]
    for split in ('family', 'development'):
        for target in TARGETS:
            cell = next(c for c in gate_checks if c['split'] == split and c['target'] == target)
            get = lambda method: index['numerical_only', split, target, method]
            lines.append(f"| {split} / {target} | {cell['baseline']} | {cell['baseline_brier']:.6f} | {get('calibrated_payoff_dominant')['event_brier']:.6f} | {get(HEADS[0])['event_brier']:.6f} | {get(HEADS[1])['event_brier']:.6f} |")
    lines += ['', 'The following contrasts use the same fixed calibrated-theory comparator throughout, avoiding selection of the point-best comparator for the scientific comparison.', '',
        '| Split / target | Calibrated theory minus frozen Brier [95% interval] | Calibrated theory minus LoRA Brier [95% interval] |',
        '|---|---:|---:|']
    for split in ('family', 'development'):
        for target in TARGETS:
            intervals = [pindex['numerical_only', split, target, 'calibrated_payoff_dominant', m]['game_bootstrap']['intervals']['event_brier'] for m in HEADS]
            lines.append(f'| {split} / {target} | {interval_text(intervals[0])} | {interval_text(intervals[1])} |')
    lines += ['',
        'The gate-selected old21 comparators are normalized logistic for action, combined logistic for cooperation, and the family mean for coordination. Their Brier-gain intervals against frozen/LoRA are:', '',
        '| Old21 target | Strongest minus frozen | Strongest minus LoRA |', '|---|---:|---:|']
    for target in TARGETS:
        cells = [next(c for c in gate_checks if (c['split'], c['target'], c['method']) == ('development', target, m)) for m in HEADS]
        lines.append(f"| {target} | {interval_text(cells[0]['interval'])} | {interval_text(cells[1]['interval'])} |")
    lines += ['',
        'Calibrated theory also has lower log loss than either head on all six split/target combinations, with all corresponding game-bootstrap intervals below zero. On LOFO, its action/cooperation/coordination log losses are 0.4699/0.2680/0.4147, compared with frozen 0.8538/1.1067/1.2358 and LoRA 0.8630/1.1991/1.2742. On old21 they are 0.4230/0.2232/0.4138, versus frozen 0.7065/0.7130/0.5508 and LoRA 0.7010/0.6722/0.5657. Calibrated theory has lower point ECE in all six cells; ten-bin ECE is descriptive and is not a proper scoring rule.', '',
        'The LOFO seven-family sensitivity retains negative Brier and log-loss intervals for both heads versus calibrated theory on all three targets. Only seven family clusters exist, with fewer families structurally eligible for some targets; these intervals are a sensitivity check, not precise uncertainty for a broad population of strategic families.', '',
        'LoRA is not a consistent improvement over the frozen head. On old21 its Brier gains are +0.0070 action, +0.0107 cooperation, and −0.0064 coordination; all three game-bootstrap intervals cross zero. Under LOFO it worsens cooperation Brier by 0.0184 (frozen-minus-LoRA interval [−0.0273, −0.0096]); action and coordination Brier differences are uncertain. The training-only finding that all ten LoRA objectives worsened is distinct from these held-out comparisons.', '',
        'Reused Kimi few-shot forecasts exist only on old21 development and cover every eligible context. Its Brier scores are 0.131262/0.061827/0.141496 and log losses 0.390862/0.221719/0.423962 for action/cooperation/coordination. It has the lowest observed action Brier among these candidates, but no Kimi-versus-theory paired interval was produced by the fixed scorer; this point ranking is not a claim of established superiority. Kimi was not evaluated on LOFO or the corrected within-family splits.', '',
        'The corrected within-family interpolation/extrapolation point results also favor the simple comparators. Frozen/LoRA Briers are respectively 0.260750/0.258120, 0.217070/0.213034, 0.261694/0.249645 for interpolation; 0.335210/0.343889, 0.283933/0.279071, 0.192926/0.192756 for extrapolation. The corresponding strongest declared numerical scores are 0.134322/0.068722/0.137459 and 0.142669/0.070901/0.134333. These are reported checks, not additional architecture-selection gates.', '',
        'Support was verified using saved group identities and counts, not just equal totals: all 24 split/target/support cells retain every eligible context and have identical game/count support across their candidate methods. LOFO action/cooperation/coordination uses 72/52/42 games, 1,152/832/672 contexts and 30,688/22,368/17,888 opportunities. Old21 uses 21/14/12 games, 336/224/192 contexts and 6,720/4,480/3,840 opportunities. There are no omitted forecasts or incomplete-coverage overrides. Structurally undefined targets are excluded rather than treated as zero.', '',
        'Interpretation is bounded: 72 training shapes, four fixed players, seven sampled strategic families, one model revision, one optimization seed, and one two-epoch LoRA schedule. Old21 outcomes were already inspected in the earlier POC, so this is development evidence, not a new prospective replication. The bootstrap holds fitted models fixed, resamples whole games without refitting, and supplies no multiplicity or comparator-selection adjustment. Action0 is an encoded action coordinate, not a universal cooperation label.', '',
        'Optimization was finite and operationally complete, but none of the ten frozen heads met strict gradient tolerance, and all ten LoRA full-training objectives increased from their same-fold frozen warm starts (+0.041544 to +0.068589). The negative result applies to this fixed representation/training procedure. It does not show that all transformer fine-tuning, other representations, or better-optimized heads cannot predict behavior.', '',
        'Verified sources: [scores](development-evaluation/scores.json), [paired intervals](development-evaluation/paired-comparisons.json), [scoring audit](development-evaluation/audit.json), [fixed gate](development-gate.json), and [training diagnostics](training-diagnostics-final.md). Exact extracted values, gate recomputation, support checks and source hashes are in [development-review.json](development-review.json). This review only reads saved results; it performs no fitting, new forecast scoring, or API calls.'
    ]
    with output.open('x') as handle:
        json.dump(value, handle, indent=2, allow_nan=False); handle.write('\n')
    with (ROOT/'development-review.md').open('x') as handle:
        handle.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(gate_verified=True, support_cells=24, forecast_rows=audit['forecast_rows'], fresh=no_fresh)))


if __name__ == '__main__':
    main()
