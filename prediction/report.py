"""One continuously refreshed Markdown entry point with directly embedded plots."""
import argparse
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prediction.io_utils import now, read_json


def optional(path, default=None):
    return read_json(path) if path.exists() else default


def render(run_root, target):
    import os
    def link(path):
        return os.path.relpath(path, target.parent)
    gates = optional(run_root/'gates.json', {'decisions': []})
    pipeline = optional(run_root/'pipeline-status.json', {'status':'running'})
    conclusion = optional(run_root/'conclusions.json')
    study_status = {'complete_through_gate7': 'Core Gate 1–7 pilot complete',
                    'informative_negative': 'Stopped at an informative negative result'}.get(pipeline['status'], pipeline['status'])
    rows = ['# Predicting behavior in repeated matrix games', '',
            f"Updated {now()}. **Study status: {study_status}.**", '',
            'The study tests payoff-only predictions made before an eight-round, simultaneous symmetric 2×2 interaction. '
            'Players maximize their own total points, see complete public history, and receive neutral A/B labels. '
            'The predictor can know the focal and opponent model identities. All rates are computed from actions; no LLM judges are used.', '',
            '[Research plan](plan.md) · [Plan coverage and unrun items](plan-coverage.md) · [Execution decisions](execution.md) · [Consolidated literature map](literature.md) · [Predictive-work literature](literature-prediction.md) · '
            '[Repeated-game literature](literature-games.md) · [Agent-identification literature](literature-identification.md) · '
            '[Measurement formulas](measurements.md) · [Independent audit](audit.md) · [Reproduction and artifact guide](README.md) · [Pilot interpretation](pilot-interpretation.md) · [Prediction interpretation](numerical-interpretation.md) · [Secondary interpretation](secondary-interpretation.md) · [Prospective interpretation](prospective-interpretation.md) · [Control interpretation](controls-interpretation.md)', '']
    if conclusion:
        rows += ['## Research readout', '', conclusion['summary'], '']
        rows += ['- '+finding for finding in conclusion.get('findings',[])]
        rows += ['']
    prospective = optional(run_root/'secondary-baselines/full/prospective-comparison/scores.json')
    prospective_guard = optional(run_root/'secondary-baselines/full/prospective-comparison/supervisor-audit.json', {})
    if prospective and prospective_guard.get('status') == 'verified':
        lookup = {(item['target'], item['method']): item for item in prospective['scores'] if item['split'] == 'prospective'}
        rows += ['### Main prospective comparison', '',
                 'Brier scores on 21 new payoff shapes from the same seven training archetypes; lower is better. '
                 'Cooperation is supported on 14 shapes and coordination on 12. All methods use the same supported outcomes. '
                 'Point differences do not establish a winner; paired intervals and calibration appear below.', '',
                 '| Predictor | Action choice | Mutual cooperation | Coordination |', '|---|---:|---:|---:|']
        for method,label in (('pair','Ordered model/opponent mean'), ('family','Game-family mean'),
                             ('nash','Original stationary Nash selector'),
                             ('secondary_payoff_dominant','Payoff-dominant selector (secondary)'),
                             ('combined_logistic_both','Combined logistic + both identities'),
                             ('combined_mlp_both','Combined MLP + both identities'),
                             ('llm_zero_shot','Kimi zero-shot'), ('llm_few_shot','Kimi three-example few-shot'),
                             ('llm_game_theory','Kimi game-theory prompt')):
            values = [lookup.get((target_name,method),{}).get('event_brier') for target_name in ('action0','cooperation','coordination')]
            rows += ['| '+label+' | '+' | '.join('undefined' if value is None else f'{value:.4f}' for value in values)+' |']
        rows += ['', 'The secondary selector was designed after the pilot, then frozen before these new games were played. '
                 'This cohort tests new payoffs within familiar archetypes; family holdouts provide the separate structural-transfer test.', '']
    rows += ['## Progress and spending', '',
             'Primary players: **Claude Haiku 4.5, Kimi K3, Qwen 3.8 27B, GPT-OSS-20B**.', '',
             '| Stage | Completed matches | Planned matches | State |', '|---|---:|---:|---|']
    pilot_collection = optional(run_root/'primary-pilot/final-collection/summary.json')
    if pilot_collection:
        rows += [f"| Primary pilot (24 shapes) | {pilot_collection['complete_episodes']} | {pilot_collection['planned_episodes']} | Audited; two bounded-retry failures retained as missing |"]
    for name in ('development','prospective','controls'):
        state = optional(run_root/name/'status.json')
        if state:
            rows.append(f"| {name} | {state.get('completed',0)} | {state.get('planned',0)} | {state['status']} |")
    rows += ['', 'The pilot combines verified unchanged pairings and GPT-OSS replacement pairings. '
             'Gemma calibration traces are preserved and excluded after a response-truncation reliability revision; '
             '[the execution record](execution.md#collection-calibration-revision) explains the decision. '
             'The 21 control configurations reuse seven known shapes and do not add 21 independent games.']
    forecast_state=optional(run_root/'prospective/llm-forecasts/status.json')
    if forecast_state:
        rows += ['',f"Prompted forecasts: **{forecast_state.get('completed',0)}/{forecast_state.get('planned',0)} valid** "
                 f"({forecast_state.get('status','running')}; {len(forecast_state.get('errors',[]))} failed queries). "
                 'Zero-shot, few-shot, and game-theory forecasts are completed before new-game player collection.']
    if (run_root/'budget.sqlite').exists():
        # Ordinary SELECT-only connections use the same locking mode as the
        # active writers; SQLite URI read-only mode fails on this shared mount.
        try:
            with sqlite3.connect(str(run_root/'budget.sqlite'), timeout=10) as database:
                paid, committed, calls = database.execute('SELECT COALESCE(SUM(charged),0), COALESCE(SUM(COALESCE(charged,reserved)),0), COUNT(*) FROM calls').fetchone()
            rows += ['', f'Reported inference charges: **${paid:,.2f}**. Including pending/unknown reservations: **${committed:,.2f}**. '
                     f'{calls:,} requests recorded against the **$3,000 ceiling**. Hosted FLT requests count as calls and tokens but use the existing hosted allocation.']
        except sqlite3.Error as exc:
            rows += ['', 'The live budget table is temporarily unavailable to this report (' + type(exc).__name__ + '). '
                     'Each runner status retains its latest budget snapshot; the inference clients still enforce the ledger ceiling.']
    rows += ['', '## Gate decision history', '',
             'Decisions are shown in execution order. Later entries and the research readout above describe the final scope and findings.', '']
    for decision in gates['decisions']:
        stamp = decision.get('time', '')
        clock_label = ' ('+stamp[11:16]+' UTC)' if stamp else ''
        rows.append(f"- **Gate {decision['gate']}{clock_label}: {decision['decision']}.** {decision['reason']}")
    diagnostic=optional(run_root/'primary-pilot/diagnostics/diagnostics.json')
    if diagnostic:
        collection=read_json(run_root/'primary-pilot/final-collection/summary.json')
        rows += ['', '## Pilot measurement repeatability', '',
                 f"The final pilot contains {collection['complete_episodes']} valid matches out of {collection['planned_episodes']} planned. Balanced repeat halves each include both action-label orientations. "
                 'Game correlations compare aggregate rates; cell correlations compare game × focal model × opponent rates. '
                 'Opportunity counts are focal measurement denominators, not independent sample sizes. Conditional targets can retain different subsets.', '',
                 '| Target | Eligible games | Paired games | Game r [95% interval] | Cell r | Focal opportunities |',
                 '|---|---:|---:|---|---:|---:|']
        def number(value):
            return 'undefined' if value is None else f'{value:.3f}'
        for target_name in ('action0','first_action0','cooperation','coordination','retaliation','forgiveness','exploitation'):
            item=diagnostic['targets'][target_name]
            support=item['support']; game=item['split_half']['game']; cell=item['split_half']['cell']
            interval=game.get('intervals',{}).get('pearson',{})
            bounds=f" [{number(interval.get('lower'))}, {number(interval.get('upper'))}]" if interval else ''
            rows += [f"| {target_name} | {support['eligible_games']} | {game['paired_points']} | {number(game['pearson'])}{bounds} | {number(cell['pearson'])} | {support['opportunities']:,} |"]
        rows += ['', '[Detailed pilot interpretation and support caveats](pilot-interpretation.md). Strong repeatability is not itself a test of prediction accuracy.', '']
    rows += ['', '## Prediction results', '']
    found_scores = False
    evaluations=(('pilot','evaluation','Pilot grouped validation'),
                 ('development','evaluation','Combined training-set grouped validation'),
                 ('prospective','evaluation','New games: numerical and prompted forecasts on common support'),
                 ('prospective','evaluation-numerical','New games: numerical forecasts on their full common support'),
                 ('prospective','evaluation-pair','New games and excluded Kimi/GPT-OSS pairing'),
                 ('prospective','evaluation-model','New games and excluded GPT-OSS model'),
                 ('controls','evaluation','Frozen forecasts under payoff and presentation controls'))
    for name,folder,title in evaluations:
        score_path=run_root/name/folder/'scores.json'
        summary = optional(score_path)
        if not summary:
            continue
        found_scores = True
        rows += [f'### {title}', '',
                 '| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |', '|---|---|---|---:|---:|---:|']
        selected = [r for r in summary['scores'] if r.get('event_brier') is not None
                    and r['split'] in ('family','prospective','prospective_pair','prospective_model','prospective_controls')
                    and r['method'] in ('marginal','pair','family','nash','raw_logistic','combined_logistic_both','combined_mlp_both','llm_zero_shot','llm_few_shot','llm_game_theory')]
        for score in selected:
            rows.append(f"| {score['split']} | {score['target']} | {score['method']} | {score['event_brier']:.3f} | {score['rate_mae']:.3f} | {score['groups']} |")
        rows += ['', f"[All scores, support, calibration and uncertainty]({link(score_path)})."]
        if name in ('pilot','development'):
            lookup={(r['split'],r['target'],r['method']):r for r in summary['scores']}
            rows += ['', 'Transfer tests for the same combined logistic predictor with both model identities (Brier score; lower is better). '
                     'Pair and model holdouts reuse known game shapes; their accuracy does not establish new-game transfer.', '',
                     '| Test | Target | Ordered context mean | Original Nash selector | Combined logistic | Shape groups |',
                     '|---|---|---:|---:|---:|---:|']
            for split in ('family','random_group','interpolation','extrapolation','pair','model'):
                for target_name in ('action0','cooperation','coordination'):
                    cells=[lookup.get((split,target_name,method),{}) for method in ('pair','nash','combined_logistic_both')]
                    if not cells[-1] or cells[-1].get('event_brier') is None:
                        continue
                    values=['undefined' if cell.get('event_brier') is None else f"{cell['event_brier']:.3f}" for cell in cells]
                    rows += [f"| {split} | {target_name} | {' | '.join(values)} | {cells[-1]['groups']} |"]
        contrasts=[r for r in summary.get('comparisons_to_pair',[]) if r['target'] in ('action0','cooperation','coordination')
                   and r['method'] in ('raw_logistic','combined_logistic_both','combined_mlp_both')
                   and r['split'] in ('family','prospective','prospective_pair','prospective_model','prospective_controls')]
        if contrasts:
            rows += ['', 'Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):', '',
                     '| Target | Predictor | Improvement | Interval |', '|---|---|---:|---|']
            for item in contrasts:
                delta=item['improvement'].get('event_brier')
                interval=item.get('intervals',{}).get('event_brier',{})
                if delta is None:
                    continue
                bounds=f"[{interval['lower']:.3f}, {interval['upper']:.3f}]" if interval else 'unavailable'
                rows += [f"| {item['target']} | {item['method']} | {delta:.3f} | {bounds} |"]
    if not found_scores:
        rows += ['No completed prediction evaluation yet. Pilot trajectories are being collected and audited.']
    secondary_evaluations=(
        ('independent-analysis/pilot-secondary','Pilot saved-fold sensitivity; retrospective'),
        ('independent-analysis/development-secondary','Combined training saved-fold sensitivity; retrospective'),
        ('secondary-baselines/full/prospective-comparison','New games; secondary forecasts frozen before play'),
        ('secondary-baselines/excluded_pair/prospective-comparison','New games and excluded pairing; secondary prospective test'),
        ('secondary-baselines/excluded_model/prospective-comparison','New games and excluded model; secondary prospective test'),
        ('secondary-baselines/full/controls-comparison','Payoff and presentation controls; secondary prospective test'))
    secondary_plots=[]
    for folder,title in secondary_evaluations:
        directory=run_root/folder
        verified=optional(directory/'supervisor-audit.json',{})
        if verified.get('status')!='verified':
            continue
        summary=optional(directory/'scores.json')
        if not summary:
            continue
        if not secondary_plots:
            rows += ['', '## Secondary baseline checks', '',
                     'These methods were designed after viewing the pilot and are separate from the original 15 methods and gate criteria. '
                     'The payoff-dominant selector chooses a highest-payoff symmetric pure stage equilibrium when available; tied choices form a joint mixture of coordinated conventions. '
                     'The event-weighted context mean matches the event-scoring objective for conditional targets. '
                     'Prospective labels below require both a forecast-before-play audit and unchanged inputs throughout analysis. '
                     '[Definitions and audit interfaces](secondary-baselines-cli.md).', '']
        # Keep a sentinel even if a valid comparison has no plots.
        secondary_plots.append(None)
        rows += [f'### {title}', '',
                 '| Test | Target | Predictor | Brier ↓ | Log loss ↓ | Calibration ECE ↓ | Shape groups |', '|---|---|---|---:|---:|---:|---:|']
        methods=('nash','combined_logistic_both','combined_mlp_both','llm_zero_shot','llm_few_shot','llm_game_theory',
                 'secondary_payoff_dominant','secondary_pair_event')
        splits=('family','extrapolation','prospective','prospective_pair','prospective_model','prospective_controls')
        for item in summary['scores']:
            if item['target'] not in ('action0','cooperation','coordination') or item['method'] not in methods or item['split'] not in splits or item.get('event_brier') is None:
                continue
            rows += [f"| {item['split']} | {item['target']} | {item['method']} | {item['event_brier']:.3f} | {item['event_log_loss']:.3f} | {item['calibration_ece']:.3f} | {item['groups']} |"]
        contrasts=[item for item in summary.get('comparisons_to_secondary',[]) if item['baseline']=='secondary_payoff_dominant'
                   and item['method']=='combined_logistic_both' and item['target'] in ('action0','cooperation','coordination') and item['split'] in splits]
        if contrasts:
            rows += ['', 'Combined-logistic Brier improvement over the payoff-dominant selector (positive is better):', '',
                     '| Test | Target | Improvement | Descriptive 95% interval |', '|---|---|---:|---|']
            for item in contrasts:
                delta=item['improvement'].get('event_brier'); interval=item.get('intervals',{}).get('event_brier',{})
                if delta is None:
                    continue
                bounds=f"[{interval['lower']:.3f}, {interval['upper']:.3f}]" if interval else 'unavailable'
                rows += [f"| {item['split']} | {item['target']} | {delta:.3f} | {bounds} |"]
        rows += ['',f"[Complete secondary scores and support]({link(directory/'scores.json')}) · [Input stability audit]({link(directory/'supervisor-audit.json')}).",'']
    sensitivity = optional(run_root/'controls/sensitivity/controls-analysis.json')
    sensitivity_step = optional(run_root/'steps/after-control-sensitivity.json', {})
    if sensitivity and sensitivity_step.get('status') == 'complete':
        rows += ['', '## Payoff and presentation sensitivity', '',
                 'Changes are percentage points in the observed event rate. Label swaps compare balanced pilot trials after undoing the action permutation. '
                 'Scale, offset, and text variants compare later trials with historical pilot anchors, matching game and ordered model/opponent context. '
                 'There is no concurrent untransformed baseline or shared random seed, so calendar or serving changes can contribute. '
                 'Intervals resample whole source shapes; an interval spanning zero does not establish invariance.', '',
                 '| Comparison | Target | Change (pp) | Descriptive 95% interval | Shapes | Matched contexts |',
                 '|---|---|---:|---|---:|---:|']
        for variant, label in (('action_labels','Swapped − unswapped labels'), ('scale3','Payoffs ×3 − original'),
                               ('offset10','Payoffs +10 − original'), ('abstract_text','Abstract text − matrix')):
            for target_name in ('action0','cooperation','coordination'):
                item = sensitivity['comparisons'][variant]['targets'][target_name]['aggregate']
                point = item['mean_change']
                ci = item.get('intervals',{}).get('mean_change',{})
                estimate = 'undefined' if point is None else f'{100*point:+.2f}'
                bounds = (f"[{100*ci['lower']:+.2f}, {100*ci['upper']:+.2f}]"
                          if ci.get('lower') is not None and ci.get('upper') is not None else 'undefined')
                rows += [f"| {label} | {target_name} | {estimate} | {bounds} | {item['eligible_groups']} | {item['paired_cells']} |"]
        rows += ['', 'The controls reuse seven known shapes; mutual cooperation is supported on five and coordination on four. '
                 'Full forecast scores and matched behavioral changes use different support rules. '
                 'Conditional-rate changes can also reflect different opportunity sets. '
                 '[Control interpretation, predictor sensitivity, and per-variant accuracy](controls-interpretation.md).', '']
    variant_path = run_root/'independent-analysis/control-variant-breakdown/scores.json'
    variants = optional(variant_path)
    if variants and variants.get('original_common_support_preserved') is True:
        index = {(item['variant'],item['target'],item['method']):item for item in variants['scores']}
        rows += ['### Forecast accuracy by control variant', '',
                 'Descriptive Brier point scores from the saved forecasts, preserving the original common supported observations. '
                 'This breakdown was added after collection; it does not refit predictors or supply new significance tests. '
                 'Seven source shapes support action choice, five cooperation, and four coordination.', '',
                 '| Target | Predictor | Scale ×3 | Offset +10 | Abstract text |', '|---|---|---:|---:|---:|']
        for target_name in ('action0','cooperation','coordination'):
            for method,label in (('family','Game-family mean'),('structural_logistic','Normalized-feature logistic'),
                                 ('combined_logistic_both','Combined logistic + identities'),
                                 ('combined_mlp_both','Combined MLP + identities'),
                                 ('secondary_payoff_dominant','Payoff-dominant selector (secondary)')):
                values = [index.get((variant,target_name,method),{}).get('event_brier')
                          for variant in ('scale3','offset10','abstract_text')]
                rows += ['| '+target_name+' | '+label+' | '+' | '.join('undefined' if value is None else f'{value:.4f}' for value in values)+' |']
        rows += ['', f'[Complete per-variant scores, support, and derivation]({link(variant_path)}).', '']
    rows += ['', '## Inline figures', '',
             'The transfer heatmaps show the same fixed combined-logistic predictor against the ordered context mean. '
             'Green means improvement over that baseline; comparisons with the original and secondary equilibrium selectors are reported separately. '
             'Intervals are descriptive and conditional on fixed fitted forecasts. Different holdouts answer different transfer questions.', '']
    plots = sorted((run_root/'report-figures').glob('*.png')) if (run_root/'report-figures/derivation.json').exists() else []
    for name in ('primary-pilot','pilot','development','prospective','controls'):
        for folder in ('diagnostics','evaluation','evaluation-numerical','evaluation-pair','evaluation-model','label-analysis','sensitivity'):
            if name=='pilot' and folder=='diagnostics' and (run_root/'primary-pilot/diagnostics').exists():
                continue
            directory = run_root/name/folder
            if directory.exists():
                plots.extend(sorted(directory.rglob('*.png')))
    secondary_figure_root=run_root/'report-figures/secondary'
    for derivation in sorted(secondary_figure_root.glob('*/derivation.json')):
        if read_json(derivation).get('status')=='verified_derived_figure':
            plots.extend(sorted(derivation.parent.glob('*.png')))
    for derivation in sorted((run_root/'report-figures/prospective').glob('*/derivation.json')):
        manifest = read_json(derivation)
        if manifest.get('status') != 'verified_derived_figure':
            continue
        replacements = [Path(path) for path in manifest.get('figures', [])]
        if not replacements or not all(path.is_file() for path in replacements):
            continue
        omitted = {Path(path).resolve() for path in manifest.get('replaces_png_paths', [])}
        plots = [plot for plot in plots if plot.resolve() not in omitted]
        plots.extend(replacements)
    for plot in plots:
        rows += [f"![{plot.stem.replace('_',' ')}]({link(plot)})", '']
    if not plots:
        rows += ['Figures appear here once sufficient complete trajectories are available.', '']
    rows += ['## Interpretation and artifacts', '',
             'Completion of the core gate sequence does not mean every checklist item in the broader plan was run. '
             'Controlled training-composition and fixed-game rollout-label-noise ablations remain unrun; '
             'per-condition empirical confidence intervals are not exported. Counts, variances, and aggregate game/episode uncertainty are available. '
             'The global parameter-region splits change family composition rather than isolate within-family extrapolation. '
             '[The coverage audit](plan-coverage.md) records these limitations and the Gate 8 exclusions.', '',
             'The literature already contains learned strategic-behavior predictors and few-shot agent identification. '
             'The narrower question here is transfer of pre-interaction, payoff-based forecasts in autonomous repeated cross-play. '
             'Grouped validation and prospective forecasts are reported separately; conditional rates with no opportunities remain undefined. '
             'These predictors estimate expected event probabilities and rates, not a joint distribution of complete phenotype vectors or trajectories. '
             'For conditional targets, logistic training weights opportunity counts while the mean baselines and rate regressors weight eligible row rates. '
             'Conditional Brier gains can therefore partly reflect different training objectives; they do not alone isolate the added value of game structure. '
             'The primary action, mutual-cooperation and coordination targets have fixed eight-round opportunities and avoid this denominator-weighting discrepancy. '
             'Retaliation and forgiveness are observational summaries. Exploitation denotes a specified asymmetric payoff-extraction event and does not establish intent.', '',
             f"[Frozen player source]({link(run_root/'source-manifest.json')}) · [Gate records]({link(run_root/'gates.json')}) · "
             '[Numerical methods and reproduction](modeling-cli.md).', '']
    completion_path = run_root/'independent-analysis/completion-audit.json'
    if completion_path.exists():
        rows += [f'[Final completion, chronology, and budget audit]({link(completion_path)}).', '']
    inventory_path = run_root/'report-figures/figure-inventory-final.json'
    if inventory_path.exists():
        rows += [f'[Exportable figure inventory: PNG, SVG, and PDF]({link(inventory_path)}).', '']
    target.parent.mkdir(parents=True, exist_ok=True)
    from uuid import uuid4
    temporary = target.with_name(target.name + '.' + uuid4().hex + '.tmp')
    temporary.write_text('\n'.join(rows))
    os.replace(temporary, target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'prediction/REPORT.md')
    args = parser.parse_args()
    render(args.run_root, args.output)
