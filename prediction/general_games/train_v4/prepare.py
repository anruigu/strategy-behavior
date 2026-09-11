"""Prepare label-free preflight inputs and count-preserving training pools."""
from collections import Counter, defaultdict
import hashlib
from statistics import mean
from prediction.io_utils import read_json, write_json, digest, now
from prediction.general_games.export import jsonl
from . import ROOT, DATA, STUDY
from .catalog import TRAIN, HOLDOUT, VALIDATION, TARGETS
from .dataset import observable, render_input


def metadata():
    instances = {x['instance_id']: x for x in read_json(DATA / 'instances.evaluator.json')}; specs = read_json(DATA / 'mechanics.json'); texts = {}
    for phase in ('training', 'test'):
        for item in read_json(STUDY / phase / 'plan.json')['episodes']:
            inst = instances[item['instance_id']]; inputs = observable(item, inst['opening_observations'])
            text = render_input(inputs, specs[item['game']['configuration_id']]); texts.setdefault(digest(text), text)
    write_json(STUDY / 'metadata-inputs.json', dict(created=now(), label_free=True, input_texts=list(texts.values()), count=len(texts)))
    m = read_json(ROOT.parents[2] / 'prediction/results/improve-20260910/model/manifest.json')
    write_json(STUDY / 'model-manifest.json', m)
    p = read_json(STUDY / 'protocol.json')
    training = dict(p['training'], created=now(), study_protocol_sha256=digest(p),
        normalization='Per-example RMS normalization of last nonpadding hidden state; no fitted test statistics.',
        hashed_linear='512 signed log-count hashed alphanumeric text features with per-example RMS normalization; no vocabulary fitting.',
        head='Three-output linear head; zero initial weights and training-only marginal-logit biases; weighted BCE/BCE/sigmoid-MSE.',
        frozen_optimizer='LBFGS max_iter=150, strong_wolfe; positive L2 weight penalty; lambda chosen on four validation families.',
        lora_primary='Arithmetic mean of the two prescribed optimization-seed forecasts; preserve each seed separately.',
        validation_metric='Family-balanced event win Brier computed from pooled first and second label moments.',
        split_rule='All validation families excluded from development fits; final models refit on all eighteen training families. No test actor labels exist during fit or selection.',
        model_manifest_sha256=digest(m), metadata_inputs_sha256=digest(list(texts.values())))
    write_json(STUDY / 'training-protocol.json', training)
    print('Prepared', len(texts), 'distinct label-free model inputs', flush=True)


def pool(rows, specs):
    groups = defaultdict(list)
    for row in rows: groups[digest(row['inputs'])].append(row)
    result = []
    for key, rr in sorted(groups.items()):
        inputs = rr[0]['inputs']; assert all(r['inputs'] == inputs for r in rr)
        result.append(dict(id='input-' + key[:20], family=inputs['family_id'], inputs=inputs,
            input_text=render_input(inputs, specs[inputs['game_id']]), count=len(rr), episode_ids=[r['episode_id'] for r in rr],
            targets={t: mean(r['targets'][t] for r in rr) for t in TARGETS},
            target_square_means={t: mean(r['targets'][t] ** 2 for r in rr) for t in TARGETS}))
    return result


def training():
    rows = [read_json(p) for p in []]  # No evaluator checkpoint is a model input.
    import json
    rows = [json.loads(line) for line in (STUDY / 'training/export/episodes.jsonl').read_text().splitlines()]
    complete = [r for r in rows if r['status'] == 'complete']; assert len(rows) == 3456
    coverage = Counter(r['inputs']['family_id'] for r in complete)
    assert all(coverage[f] / 192 >= .98 for f in TRAIN), ('Training coverage below predeclared gate', dict(coverage))
    specs = read_json(DATA / 'mechanics.json'); arms = {}
    for budget in ('small', 'full'):
        selected = [r for r in complete if budget == 'full' or r['small']]
        expected = 48 if budget == 'small' else 192
        counts = Counter(r['inputs']['family_id'] for r in selected)
        assert all(counts[f] / expected >= .98 for f in TRAIN), ('Budget coverage below gate', budget, dict(counts))
        arms[budget] = pool(selected, specs)
        jsonl(STUDY / 'training/exports' / (budget + '-episodes.jsonl'), [dict(episode_id=r['episode_id'], inputs=r['inputs'], targets=r['targets'], condition_id=r['condition_id']) for r in selected])
        jsonl(STUDY / 'training/exports' / (budget + '-pooled.jsonl'), arms[budget])
    assert not set(HOLDOUT) & {r['family'] for r in arms['full']}
    payload = dict(created=now(), training_protocol=read_json(STUDY / 'training-protocol.json'), target_order=list(TARGETS),
        arms=arms, validation_families=list(VALIDATION), test_queries=read_json(DATA / 'test-queries.json'),
        coverage=dict(planned=len(rows), complete=len(complete), by_family=dict(coverage)),
        source_hashes=dict(training_rows=hashlib.sha256((STUDY / 'training/export/episodes.jsonl').read_bytes()).hexdigest(),
            test_query_metadata=digest(read_json(DATA / 'test-queries.json')), preparation=digest(__import__('pathlib').Path(__file__).read_text())))
    write_json(STUDY / 'training-package.json', payload)
    write_json(STUDY / 'training-package-manifest.json', dict(created=now(), package_sha256=hashlib.sha256((STUDY / 'training-package.json').read_bytes()).hexdigest(),
        labels='Training only; test_queries contain no outcomes.', arms={k: dict(visible_inputs=len(v), episode_labels=sum(r['count'] for r in v), families=len({r['family'] for r in v})) for k, v in arms.items()}))
    print(read_json(STUDY / 'training-package-manifest.json'), flush=True)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('action', choices=['metadata', 'training']); a = p.parse_args()
    metadata() if a.action == 'metadata' else training()

