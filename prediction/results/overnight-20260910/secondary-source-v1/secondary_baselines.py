"""Secondary controls designed after pilot inspection; never change primary gates.

Only local deterministic prediction and count pooling. No inference clients.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

from prediction.games import make_game, payoff
from prediction.modeling import TARGETS, load_records, pair_id, supported_target
from prediction.prospective import build_rows, canonical_hash, validate_compatible

VERSION = 'secondary-post-pilot-v1'
EQUILIBRIUM_METHOD = 'secondary_payoff_dominant'
CONTEXT_METHOD = 'secondary_pair_event'
EQUILIBRIUM_TARGETS = ('action0', 'first_action0', 'cooperation', 'coordination')
ROOT = Path(__file__).resolve().parent


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def configuration(include_pair_event=False):
    return dict(version=VERSION, classification='secondary_post_pilot_control',
                motivation='Designed after inspecting pilot numerical results; not an original preregistered primary method.',
                methods=[EQUILIBRIUM_METHOD]+([CONTEXT_METHOD] if include_pair_event else []),
                primary_methods_and_gate_criteria_unchanged=True,
                equilibrium_targets=list(EQUILIBRIUM_TARGETS), context_targets=list(TARGETS),
                equilibrium_rule='Among symmetric pure stage Nash profiles choose maximal common payoff. Equal-payoff maximizers share equal joint-profile mass. If no symmetric pure profile exists, use the existing independent symmetric mixed equilibrium.',
                tie_interpretation='Mixture of coordinated pure-equilibrium conventions / balanced-display marginal; not independent action mixing and not a protocol-provided public randomizer.',
                display_conditioning='Forecasts marginalize the balanced display swaps and ignore trial_id/swap. Literal choosing displayed A would instead predict canonical action0=1-swap for each trial.',
                payoff_tie_tolerance='1e-9 times payoff range; matches normalized game-comparison tolerance.',
                context_weighting='Compute N_g from all supported training opportunities in each game, then p_context=sum_g(S_g_context/N_g)/sum_g(N_g_context/N_g). Equal-game event weights are defined globally before restricting ordered contexts, matching the logistic/event-Brier objective.',
                context_fallback='Unknown ordered context uses all-training equal-game event-weighted mean; target with no eligible training events predicts null.',
                limitations=['Stage-equilibrium selection is a behavioral comparator, not an equilibrium claim for finite repeated interaction.',
                             'Conditional event weights change the training objective relative to the original equal-row ordered-context baseline.',
                             'Pilot comparisons are post hoc; pre-outcome freezing on new games can establish secondary prospective evaluation only.'])


def source_hashes():
    names = ('secondary_baselines.py', 'games.py', 'modeling.py', 'prospective.py')
    return {str(ROOT/name): sha((ROOT/name).read_bytes()) for name in names}


def new_path(path):
    path = Path(path).resolve()
    if not path.is_relative_to(Path('/shared/allie')):
        raise ValueError('Artifacts must remain under /shared/allie')
    if path.exists():
        raise FileExistsError('Refusing to overwrite secondary artifact: '+str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_new_json(path, value):
    with Path(path).open('x') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')


def equilibrium_distribution(game):
    """Joint canonical profile masses, retaining correlation in pure-profile ties."""
    symmetric = [profile for profile in game['pure_nash'] if profile[0] == profile[1]]
    if symmetric:
        values = [payoff(game, *profile)[0] for profile in symmetric]
        best = max(values)
        span = max(game['payoffs'].values())-min(game['payoffs'].values())
        selected = [profile for profile, value in zip(symmetric, values) if best-value <= 1e-9*span]
        mass = 1./len(selected)
        return dict(rule='payoff_dominant_symmetric_pure' if len(selected) == 1 else 'tied_coordinated_conventions',
                    profiles=[dict(actions=list(profile), probability=mass) for profile in selected],
                    independent=False, marginalize_display_swap=True)
    features = game['features']
    if features['all_indifferent']:
        q = .5
    elif features['has_interior_mixed_equilibrium']:
        q = features['mixed_equilibrium_action0_probability']
    else:
        raise ValueError('No symmetric pure or supported symmetric mixed stage equilibrium')
    return dict(rule='independent_symmetric_mixed', independent=True, marginalize_display_swap=True,
                profiles=[dict(actions=[a, b], probability=(q if a == 0 else 1-q)*(q if b == 0 else 1-q))
                          for a in (0, 1) for b in (0, 1)])


def equilibrium_prediction(game, target, player_index=0, distribution=None):
    if target not in EQUILIBRIUM_TARGETS:
        return None
    if type(player_index) is not int or player_index not in (0, 1):
        raise ValueError('player_index must be canonical focal role 0 or 1')
    distribution = equilibrium_distribution(game) if distribution is None else distribution
    if target in ('action0', 'first_action0'):
        return sum(row['probability'] for row in distribution['profiles'] if row['actions'][player_index] == 0)
    if target == 'cooperation':
        action = game['applicability']['cooperative_action']
        if action is None:
            return None
        selected = {(action, action)}
    else:
        if not game['applicability']['coordination']:
            return None
        selected = {tuple(profile) for profile in game['applicability']['coordination_outcomes']}
    return sum(row['probability'] for row in distribution['profiles'] if tuple(row['actions']) in selected)


def pooled_game_mean(rows, target):
    """Exact count pooling within eligible groups; null/zero exposure is excluded."""
    groups = defaultdict(lambda: dict(successes=0, opportunities=0, rows=0))
    for row in rows:
        cell = supported_target(row, target)
        if cell is None:
            continue
        if not row.get('group_id'):
            raise ValueError('Training rows require canonical group_id')
        bucket = groups[str(row['group_id'])]
        bucket['successes'] += cell['successes']
        bucket['opportunities'] += cell['opportunities']
        bucket['rows'] += 1
    counts = [dict(group_id=key, **value) for key, value in sorted(groups.items())]
    return dict(prediction=sum(c['successes']/c['opportunities'] for c in counts)/len(counts) if counts else None,
                eligible_rows=sum(c['rows'] for c in counts), eligible_groups=len(counts), group_counts=counts)


def fit_contexts(rows):
    contexts = defaultdict(list)
    for row in rows:
        if not isinstance(row.get('model'), str) or not isinstance(row.get('opponent'), str):
            raise ValueError('Training records require ordered model/opponent identities')
        contexts[row['model'], row['opponent']].append(row)
    fits = {}
    for target in TARGETS:
        fallback = pooled_game_mean(rows, target)
        totals = {group['group_id']: group['opportunities'] for group in fallback['group_counts']}
        cells = []
        for (model, opponent), subset in sorted(contexts.items()):
            cell = pooled_game_mean(subset, target)
            weighted_successes = sum(group['successes']/totals[group['group_id']] for group in cell['group_counts'])
            weighted_opportunities = sum(group['opportunities']/totals[group['group_id']] for group in cell['group_counts'])
            cell.update(prediction=weighted_successes/weighted_opportunities if weighted_opportunities else None,
                        weighted_successes=weighted_successes, weighted_opportunities=weighted_opportunities)
            cells.append(dict(model=model, opponent=opponent, **cell))
        fits[target] = dict(fallback=fallback, contexts=cells)
    return fits


def context_prediction(fits, row, target):
    target_fit = fits[target]
    context = next((cell for cell in target_fit['contexts'] if (cell['model'], cell['opponent']) ==
                    (row['model'], row['opponent']) and cell['eligible_rows'] > 0), None)
    if context is not None:
        return context['prediction'], None, context['eligible_rows']
    fallback = target_fit['fallback']
    reason = 'unknown or unsupported ordered context: equal-game event population mean' if fallback['prediction'] is not None else 'no eligible training events for target'
    return fallback['prediction'], reason, fallback['eligible_rows']


def fit_bundle(records, artifact, training_source=None):
    """records=None saves only the payoff rule; a list adds the secondary context fit."""
    path = new_path(artifact)
    include = records is not None
    value = dict(created_utc=timestamp(), configuration=configuration(include), source_sha256=source_hashes(),
                 training_rows=len(records) if include else 0,
                 training_sha256=canonical_hash(records) if include else None,
                 training_source_sha256=sha(Path(training_source).read_bytes()) if training_source else None,
                 training_source=str(Path(training_source).resolve()) if training_source else None,
                 context_fits=fit_contexts(records) if include else {})
    write_new_json(path, value)
    return value


def validate_metadata(rows):
    """Require complete label-free focal metadata, retaining exact order for hashing."""
    episodes, games = defaultdict(list), {}
    for row in rows:
        if 'targets' in row or any(row.get(key) is not None for key in ('value', 'successes', 'opportunities')):
            raise ValueError('Forecast input must contain no outcome labels or target counts')
        required = ('episode_id', 'player_index', 'game_id', 'group_id', 'family', 'model', 'opponent',
                    'trial_id', 'representation', 'swap', 'payoffs', 'features')
        if any(key not in row for key in required):
            raise ValueError('Forecast requires complete planned focal metadata')
        game = make_game(row['game_id'], **row['payoffs'])
        if any(row[key] != game[key] for key in ('group_id', 'family', 'payoffs', 'features')):
            raise ValueError('Planned payoff/group/features are inconsistent')
        if row['game_id'] in games and games[row['game_id']] != game:
            raise ValueError('Conflicting planned game identity')
        if row.get('pair', pair_id(row)) != pair_id(row):
            raise ValueError('Inconsistent unordered pair ID')
        games[row['game_id']] = game
        episodes[row['episode_id']].append(row)
    for group in episodes.values():
        if len(group) != 2 or {row['player_index'] for row in group} != {0, 1}:
            raise ValueError('Each planned episode requires exactly both focal roles')
        a, b = sorted(group, key=lambda row: row['player_index'])
        if (a['model'], a['opponent']) != (b['opponent'], b['model']):
            raise ValueError('Focal roles have conflicting player identities')
        if any(a[key] != b[key] for key in ('game_id', 'trial_id', 'representation', 'swap')):
            raise ValueError('Focal rows disagree about their planned episode')
    if not rows:
        raise ValueError('No planned metadata rows')
    return games


def _validate_primary(path, rows):
    path = Path(path)
    raw = path.read_bytes()
    manifest_path = path.with_suffix('.manifest.json')
    manifest = json.loads(manifest_path.read_text())
    if manifest['forecast_sha256'] != sha(raw) or manifest['input_sha256'] != canonical_hash(rows):
        raise ValueError('Primary forecast hash/input identity does not match immutable metadata')
    forecasts = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if manifest['rows'] != len(forecasts):
        raise ValueError('Primary forecast row count mismatch')
    planned = {(row['episode_id'], row['player_index']): row for row in rows}
    seen = set()
    for forecast in forecasts:
        key = (forecast['episode_id'], forecast['player_index'], forecast['target'], forecast['method'])
        if key in seen:
            raise ValueError('Duplicate primary forecast key')
        seen.add(key)
        if key[:2] not in planned:
            raise ValueError('Unexpected primary episode/focal role')
        validate_compatible(forecast, planned[key[:2]], 'Primary forecast')
        if any(forecast.get(k) is not None for k in ('value', 'successes', 'opportunities')):
            raise ValueError('Primary forecasts already contain labels')
        p = forecast.get('prediction')
        if p is not None and (type(p) not in (float, int) or not math.isfinite(p) or not 0 <= p <= 1):
            raise ValueError('Invalid primary probability')
    return forecasts, {str(path.resolve()): sha(raw), str(manifest_path.resolve()): sha(manifest_path.read_bytes())}


def forecast_bundle(artifact, rows, output, primary_forecasts=None, stage_root=None):
    output = new_path(output)
    companion = new_path(output.with_suffix('.manifest.json'))
    artifact = Path(artifact)
    raw_artifact = artifact.read_bytes()
    bundle = json.loads(raw_artifact)
    if bundle['configuration'] != configuration(bool(bundle['context_fits'])) or bundle['source_sha256'] != source_hashes():
        raise ValueError('Secondary artifact configuration/source differs from the current frozen implementation')
    games = validate_metadata(rows)
    if stage_root:
        stage_root = Path(stage_root)
        if build_rows(json.loads((stage_root/'manifest.json').read_text())) != rows:
            raise ValueError('Metadata differs from the complete target stage manifest')
        if any((stage_root/name).exists() for name in ('episodes', 'process.json', 'status.json')):
            raise ValueError('Secondary forecasts must be first frozen before any target stage starts')
    forecasts, sources = _validate_primary(primary_forecasts, rows) if primary_forecasts else ([], {})
    methods = {row['method'] for row in forecasts}
    if methods & set(bundle['configuration']['methods']):
        raise ValueError('Primary input already contains a secondary method; do not duplicate forecasts')
    distributions = {key: equilibrium_distribution(game) for key, game in games.items()}
    for index, row in enumerate(rows):
        game, distribution = games[row['game_id']], distributions[row['game_id']]
        for method in bundle['configuration']['methods']:
            targets = EQUILIBRIUM_TARGETS if method == EQUILIBRIUM_METHOD else TARGETS
            for target in targets:
                if method == EQUILIBRIUM_METHOD:
                    p = equilibrium_prediction(game, target, row['player_index'], distribution)
                    fallback, count = None, 0
                else:
                    p, fallback, count = context_prediction(bundle['context_fits'], row, target)
                forecasts.append(dict(row, row_index=index, method=method, target=target, prediction=p,
                    split='secondary_frozen', fold='fitted', value=None, successes=None, opportunities=None, eligible=False,
                    fallback=fallback, training_count=count, secondary_post_pilot=True, marginalize_display_swap=True,
                    secondary_rule=distribution['rule'] if method == EQUILIBRIUM_METHOD else 'ordered_context_equal_game_event_mean'))
    # Source bytes must remain stable during the deterministic export.
    sources[str(artifact.resolve())] = sha(raw_artifact)
    for path, expected in sources.items():
        if sha(Path(path).read_bytes()) != expected:
            raise ValueError('A frozen source changed during secondary forecasting')
    with output.open('x') as handle:
        for row in forecasts:
            handle.write(json.dumps(row, allow_nan=False)+'\n')
    write_new_json(companion, dict(created_utc=timestamp(), artifact_sha256=sha(raw_artifact),
        input_sha256=canonical_hash(rows), forecast_sha256=sha(output.read_bytes()), rows=len(forecasts),
        artifact_training_sha256=bundle['training_sha256'], classification='secondary_post_pilot_control',
        configuration=bundle['configuration'], source_forecast_and_artifact_sha256=sources,
        additional_source_sha256=bundle['source_sha256'],
        stage_root=str(Path(stage_root).resolve()) if stage_root else None,
        prospectivity='Must be verified against actual trace start times by the unchanged prospective scorer; post-pilot design is not original preregistration.'))
    return forecasts


MATCH_FIELDS = ('row_index', 'episode_id', 'player_index', 'game_id', 'group_id', 'family', 'model',
                'opponent', 'pair', 'trial_id', 'representation', 'swap', 'target', 'split', 'fold',
                'value', 'successes', 'opportunities', 'eligible')


def _base_key(row):
    return row['split'], row['fold'], row['episode_id'], row['player_index'], row['target']


def validate_joined(primary, secondary):
    """Match outcomes and complete focal support before any comparative scoring."""
    references, seen = {}, set()
    for row in primary+secondary:
        key = _base_key(row)
        method_key = key+(row['method'],)
        if method_key in seen:
            raise ValueError('Duplicate method forecast in comparison')
        seen.add(method_key)
        if key in references and any(row.get(field) != references[key].get(field) for field in MATCH_FIELDS):
            raise ValueError('Comparison rows disagree on outcomes or focal/fold metadata')
        references[key] = row
        p = row.get('prediction')
        if p is not None and (type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1):
            raise ValueError('Invalid saved comparison probability')
    primary_keys = {_base_key(row) for row in primary}
    if not {_base_key(row) for row in secondary} <= primary_keys:
        raise ValueError('Secondary comparison includes an unexpected test outcome/fold')
    primary_focals = {key[:-1] for key in primary_keys}
    if {key[:-1] for key in map(_base_key, secondary)} != primary_focals:
        raise ValueError('Comparison inputs do not cover the same complete focal support')
    for source in (primary, secondary):
        by_method_target = defaultdict(set)
        for row in source:
            by_method_target[row['method'], row['target']].add(_base_key(row)[:-1])
        if any(keys != primary_focals for keys in by_method_target.values()):
            raise ValueError('A comparison method/target is missing planned focal rows')
    return primary+secondary


def secondary_contrasts(rows, bootstrap):
    from prediction.analysis import score_rows, paired_improvement_intervals, _valid, _prediction_key
    grouped = defaultdict(lambda: defaultdict(dict))
    for row in rows:
        grouped[row['split'], row['target']][row['method']].update(
            {_prediction_key(row): row} if _valid(row) else {})
    contrasts = []
    for (split, target), methods in sorted(grouped.items()):
        common = set.intersection(*(set(values) for values in methods.values())) if methods else set()
        if not common:
            continue
        aligned = {method: [values[key] for key in sorted(common)] for method, values in methods.items()}
        for baseline in (EQUILIBRIUM_METHOD, CONTEXT_METHOD):
            if baseline not in aligned:
                continue
            base_score = score_rows(aligned[baseline])
            for method, predictions in aligned.items():
                if method == baseline:
                    continue
                metric = score_rows(predictions)
                contrasts.append(dict(split=split, target=target, method=method, baseline=baseline,
                    positive_means_improvement=True, common_rows=len(common),
                    improvement={key: base_score[key]-metric[key] for key in ('rate_mae', 'event_brier', 'event_log_loss')},
                    intervals=paired_improvement_intervals(aligned[baseline], predictions, repetitions=bootstrap)))
    return contrasts


def _write_comparison(rows, output, audit, bootstrap):
    from prediction.analysis import summarize_predictions
    from prediction.prospective import plot_scores
    output = new_path(output)
    summary = summarize_predictions(rows, bootstrap=bootstrap)
    summary['comparisons_to_secondary'] = secondary_contrasts(rows, bootstrap)
    summary['secondary_classification'] = audit['classification']
    output.mkdir()
    with (output/'joined-predictions.jsonl').open('x') as handle:
        for row in rows:
            handle.write(json.dumps(row, allow_nan=False)+'\n')
    write_new_json(output/'scores.json', summary)
    write_new_json(output/'secondary-comparisons.json', summary['comparisons_to_secondary'])
    plot_scores(summary, output, audit.get('prospective_verified', False))
    write_new_json(output/'audit.json', dict(audit, created_utc=timestamp(),
        output_sha256={str(path.resolve()): sha(path.read_bytes()) for path in output.iterdir() if path.is_file()}))
    return summary


def _validate_scored_sources(audit, joined):
    """A saved scoring audit alone does not hash its exported joined rows."""
    numeric, prompted = {}, {}
    for source in audit['sources']:
        forecasts = [json.loads(line) for line in Path(source['path']).read_text().splitlines() if line.strip()]
        for row in forecasts:
            if source['kind'] == 'numerical':
                key = row['episode_id'], row['player_index'], row['target'], row['method']
                numeric[key] = row
            else:
                key = row['game_id'], row['model'], row['opponent'], row['target'], row['method']
                prompted[key] = row
    record_paths = [path for path, value in audit['source_sha256'].items() if value == audit['records_sha256']]
    if not record_paths:
        raise ValueError('Evaluation audit does not identify the outcome snapshot')
    records = {(row['episode_id'], row['player_index']): row for row in load_records(record_paths[0])}
    planned = None
    for path in audit['source_sha256']:
        if Path(path).name == 'manifest.json':
            manifest = json.loads(Path(path).read_text())
            if 'episodes' in manifest and 'games' in manifest:
                planned = {(row['episode_id'], row['player_index']): (index, row)
                           for index, row in enumerate(build_rows(manifest))}
                break
    if planned is None:
        raise ValueError('Verified scoring audit does not identify its planned stage manifest')
    for row in joined:
        focal = row['episode_id'], row['player_index']
        if focal not in planned or row['row_index'] != planned[focal][0]:
            raise ValueError('Joined focal/index differs from the audited stage manifest')
        validate_compatible(row, planned[focal][1], 'Joined forecast')
        source = numeric.get((row['episode_id'], row['player_index'], row['target'], row['method']))
        if source is None:
            source = prompted.get((row['game_id'], row['model'], row['opponent'], row['target'], row['method']))
        if source is None or source['prediction'] != row['prediction']:
            raise ValueError('Joined probability does not match its audited frozen source forecast')
        if row['fold'] != 'frozen' or row['split'] != audit['effective_split']:
            raise ValueError('Joined fold/split differs from its prospective scoring audit')
        original = records.get((row['episode_id'], row['player_index']))
        cell = supported_target(original, row['target']) if original else None
        raw_cell = original.get('targets', {}).get(row['target'], {}) if original else {}
        expected = dict(value=cell['value'] if cell else None, successes=raw_cell.get('successes'),
                        opportunities=raw_cell.get('opportunities'), eligible=cell is not None,
                        outcome_observed=original is not None)
        if any(row.get(key) != value for key, value in expected.items()):
            raise ValueError('Joined outcomes differ from the audited original outcome snapshot')


def compare(primary_evaluation, secondary_evaluation, output, bootstrap=500):
    sources, audits, row_sets = {}, [], []
    for folder in map(Path, (primary_evaluation, secondary_evaluation)):
        audit_path, rows_path = folder/'audit.json', folder/'joined-predictions.jsonl'
        audit_raw, rows_raw = audit_path.read_bytes(), rows_path.read_bytes()
        audit = json.loads(audit_raw)
        if audit.get('prospective_verified') is not True:
            raise ValueError('Both source evaluations must have verified prospective audits')
        if not audit.get('source_sha256'):
            raise ValueError('Source evaluation lacks its audited immutable source hashes')
        for path, expected in audit['source_sha256'].items():
            if sha(Path(path).read_bytes()) != expected:
                raise ValueError('Audited source bytes changed before secondary comparison: '+path)
        sources.update({str(audit_path.resolve()): sha(audit_raw), str(rows_path.resolve()): sha(rows_raw)})
        audits.append(audit)
        joined = [json.loads(line) for line in rows_raw.splitlines() if line.strip()]
        _validate_scored_sources(audit, joined)
        row_sets.append(joined)
    if any(audits[0].get(field) != audits[1].get(field) for field in ('records_sha256', 'requested_split', 'effective_split')):
        raise ValueError('Source evaluations differ in outcome snapshot or split')
    rows = validate_joined(*row_sets)
    for path, expected in sources.items():
        if sha(Path(path).read_bytes()) != expected:
            raise ValueError('Comparison input changed while validating')
    audit = dict(classification='secondary_post_pilot_prospective_comparison', prospective_verified=True,
                 source_evaluation_sha256=sources, source_audits=audits,
                 source_code_sha256=source_hashes(), configuration=configuration(True),
                 rationale='Concatenate already-scored pre-outcome forecasts. This is an offline analysis artifact, not a newly frozen forecast or a backdated prediction.')
    return _write_comparison(rows, output, audit, bootstrap)


def retrospective(records_path, evaluation, output, bootstrap=500):
    """Post hoc baseline sensitivity using exactly saved primary training/test folds."""
    records = load_records(records_path)
    evaluation = Path(evaluation)
    config = json.loads((evaluation/'run_config.json').read_text())
    if config['input_sha256'] != canonical_hash(records):
        raise ValueError('Retrospective records differ from the original numerical input')
    folds = json.loads((evaluation/'folds.json').read_text())
    primary = [json.loads(line) for line in (evaluation/'predictions.jsonl').read_text().splitlines() if line.strip()]
    by_fold = {}
    for fold in folds:
        key = fold['kind'], fold['name']
        if key in by_fold:
            raise ValueError('Duplicate saved fold')
        train, test = fold['train'], fold['test']
        if (len(train) != len(set(train)) or len(test) != len(set(test)) or set(train) & set(test) or
                any(type(index) is not int or not 0 <= index < len(records) for index in train+test)):
            raise ValueError('Invalid or overlapping saved fold indices')
        if {records[i]['episode_id'] for i in train} & {records[i]['episode_id'] for i in test}:
            raise ValueError('Saved fold separates focal rows of an episode')
        by_fold[key] = fold
    for row in primary:
        key = row['split'], row['fold']
        if key not in by_fold or row['row_index'] not in by_fold[key]['test']:
            raise ValueError('Primary prediction does not match saved held-out indices')
        record = records[row['row_index']]
        for field in ('episode_id', 'player_index', 'game_id', 'group_id', 'family', 'model', 'opponent', 'trial_id', 'representation', 'swap'):
            if row.get(field) != record.get(field):
                raise ValueError('Primary saved identity differs from retrospective input')
        cell = supported_target(record, row['target'])
        expected = dict(value=cell['value'] if cell else None, successes=cell['successes'] if cell else None,
                        opportunities=cell['opportunities'] if cell else None, eligible=cell is not None)
        if any(row.get(field) != value for field, value in expected.items()):
            raise ValueError('Primary saved labels differ from retrospective records')
    games = {row['game_id']: make_game(row['game_id'], **row['payoffs']) for row in records}
    distributions = {key: equilibrium_distribution(game) for key, game in games.items()}
    secondary, fit_audit = [], []
    # Iterate saved primary cells so unsupported method-target combinations do
    # not introduce a different test population or a freshly generated split.
    cells = {}
    for row in primary:
        cells.setdefault((row['split'], row['fold'], row['row_index'], row['target']), row)
    for key, fold in by_fold.items():
        training = [records[index] for index in fold['train']]
        fits = fit_contexts(training)
        fit_audit.append(dict(split=key[0], fold=key[1], train=fold['train'], test=fold['test'],
                              training_sha256=canonical_hash(training), context_fits=fits))
        for (split, name, index, target), original in cells.items():
            if (split, name) != key:
                continue
            record = records[index]
            for method in (EQUILIBRIUM_METHOD, CONTEXT_METHOD):
                if method == EQUILIBRIUM_METHOD:
                    if target not in EQUILIBRIUM_TARGETS:
                        continue
                    p = equilibrium_prediction(games[record['game_id']], target, record['player_index'], distributions[record['game_id']])
                    fallback, count = None, 0
                else:
                    p, fallback, count = context_prediction(fits, record, target)
                secondary.append(dict(original, method=method, prediction=p, fallback=fallback,
                                      training_count=count, secondary_post_pilot=True))
    joined = validate_joined(primary, secondary)
    inputs = [Path(records_path), evaluation/'run_config.json', evaluation/'folds.json', evaluation/'predictions.jsonl']
    audit = dict(classification='secondary_post_pilot_retrospective_sensitivity', prospective_verified=False,
                 source_sha256={str(path.resolve()): sha(path.read_bytes()) for path in inputs},
                 source_code_sha256=source_hashes(), configuration=configuration(True), fold_fit_audit=fit_audit,
                 limitation='Methods were motivated by observed pilot results; these saved-fold comparisons are post hoc and do not alter primary methods, original predictions, or gate criteria.')
    return _write_comparison(joined, output, audit, bootstrap)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    fitting = commands.add_parser('fit', help='save deterministic payoff rule and optional training-only event context fit')
    fitting.add_argument('--artifact', required=True)
    fitting.add_argument('--training-records', help='omit for payoff comparator only; provide to add secondary_pair_event')
    forecasting = commands.add_parser('forecast', help='freeze complete target metadata before target rollouts')
    forecasting.add_argument('--artifact', required=True)
    forecasting.add_argument('--input', required=True, help='full label-free prospective metadata JSON/JSONL')
    forecasting.add_argument('--output', required=True)
    forecasting.add_argument('--primary-forecasts', help='optionally copy existing primary forecast rows into a NEW combined export')
    forecasting.add_argument('--stage-root', help='verify exact manifest metadata and reject any already-started target stage')
    comparing = commands.add_parser('compare', help='compare separately verified prospective evaluations without creating a new forecast')
    comparing.add_argument('--primary-evaluation', required=True)
    comparing.add_argument('--secondary-evaluation', required=True)
    comparing.add_argument('--out', required=True)
    comparing.add_argument('--bootstrap', type=int, default=500)
    retro = commands.add_parser('retrospective', help='post hoc sensitivity using preserved primary fold membership')
    retro.add_argument('--records', required=True)
    retro.add_argument('--evaluation', required=True)
    retro.add_argument('--out', required=True)
    retro.add_argument('--bootstrap', type=int, default=500)
    args = parser.parse_args(argv)
    if args.command == 'fit':
        result = fit_bundle(load_records(args.training_records) if args.training_records else None,
                            args.artifact, args.training_records)
        print(json.dumps(dict(artifact=args.artifact, methods=result['configuration']['methods'])))
    elif args.command == 'forecast':
        result = forecast_bundle(args.artifact, load_records(args.input), args.output,
                                 args.primary_forecasts, args.stage_root)
        print(json.dumps(dict(output=args.output, rows=len(result), classification='secondary_post_pilot_control')))
    else:
        result = (compare(args.primary_evaluation, args.secondary_evaluation, args.out, args.bootstrap)
                  if args.command == 'compare' else retrospective(args.records, args.evaluation, args.out, args.bootstrap))
        print(json.dumps(dict(output=args.out, scores=len(result['scores']), classification=result['secondary_classification'])))


if __name__ == '__main__':
    main()
