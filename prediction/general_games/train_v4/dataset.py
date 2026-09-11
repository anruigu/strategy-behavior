"""Build native metadata, validate configurations, and freeze the collection plan."""
import json
from collections import Counter
from copy import deepcopy
from prediction.io_utils import digest, now, read_json, write_json
from prediction.general_games.native import environment_record, jsonable
from prediction.general_games.breadth_v3.collection import source_hashes as old_hashes
from prediction.scaleup.providers import configurations as model_configs
from . import ROOT, REPO, DATA, STUDY, VERSION
from .catalog import FAMILIES, TRAIN, HOLDOUT, VALIDATION, MODELS, TARGETS, design
from .runtime import Session, view, action, messages, replay
from .specifications import specification
from .labels import DEFINITIONS


def source_hashes():
    result = old_hashes()
    for name in ('__init__.py', 'catalog.py', 'dataset.py', 'runtime.py', 'labels.py', 'specifications.py', 'api.py', 'collection.py'):
        p = ROOT / name; result[str(p.relative_to(REPO))] = digest(p.read_text())
    for name in ('prediction/general_games/scaleup_v2/catalog.py', 'prediction/general_games/scaleup_v2/data/mechanics.v2.json',
                 'prediction/general_games/breadth_v3/study/prediction/breadth/mechanics.json'):
        result[name] = digest((REPO / name).read_text())
    return result


def observable(item, opening):
    g = item['game']
    return dict(family_id=g['family_id'], game_id=g['configuration_id'], structured=g['structured'], model=item['model'], seat=item['seat'],
        prompt='normal_with_native_format_reminder_v4', opening_messages=messages(g, opening[str(item['seat'])]),
        opponent_policy=FAMILIES[g['family_id']]['opponent_policy'])


def render_input(inputs, mechanics):
    compact = {k: v for k, v in mechanics.items() if k not in ('schema', 'family', 'player_protocol')}
    return ('Predict the focal model’s behavior before this native game begins.\n'
        + 'Targets: ' + json.dumps(DEFINITIONS, ensure_ascii=False) + '\n'
        + 'Focal actor and public game: ' + json.dumps({k: v for k, v in inputs.items() if k != 'opening_messages'}, ensure_ascii=False, sort_keys=True) + '\n'
        + 'Exact actor opening messages: ' + json.dumps(inputs['opening_messages'], ensure_ascii=False) + '\n'
        + 'Predictor-only mechanics: ' + json.dumps(compact, ensure_ascii=False, sort_keys=True)
        + '\nEstimate strict win probability, probability of any native-invalid submission, and expected normalized native score. Draws are not strict wins.')


def build():
    if (DATA / 'manifest.json').exists():
        m = read_json(DATA / 'manifest.json'); assert m['source_hashes'] == source_hashes()
        return m
    items = design(); instances = []; fixtures = []; games = {}; specs = {}; plans = {'training': [], 'test': []}; queries = []
    for ii, base in enumerate(items):
        g, seed = base['game'], base['seed']; s = Session(g, seed); opening = jsonable(s.opening); snapshot = s.snapshot()
        inst = dict(base, opening_state=snapshot, opening_observations=opening, opening_group='open-v4-' + digest([g['configuration_id'], snapshot])[:20])
        instances.append(inst); cfg = g['configuration_id']; specs[cfg] = specification(g)
        if cfg not in games:
            games[cfg] = g; steps = []
            for index in range(256):
                actor, incoming, h = s.observe(); v = view(s, actor, h); before = s.snapshot(); raw = action(v, seed, index); result = s.step(raw)
                assert not result['native_invalid'], (g['family_id'], seed, index, raw, result)
                steps.append(dict(index=index, actor=actor, incoming=incoming, visible_state=v, before=before, is_focal=False,
                    raw_action=raw, result=result, after=s.snapshot()))
                if result['done']: break
            assert s.env.state.done, (g['family_id'], seed, 'scripted fixture exceeded native action allowance')
            trace = dict(status='complete', opening_state=snapshot, opening_observations=opening, steps=steps, final_state=s.snapshot())
            replay(dict(game=g, seed=seed), trace)
            fixtures.append(dict(configuration_id=cfg, seed=seed, provenance='scripted_validation_not_actor_data', trace=trace))
        for seat in range(g['num_players']):
            for model in MODELS:
                item = dict(game=g, seed=seed, seat=seat, model=model, condition='normal', actor_protocol='format_v4', small=base['small'],
                    suite=base['suite'], instance_id=base['instance_id'], opening_group=inst['opening_group'])
                if base['phase'] == 'test':
                    inputs = observable(item, opening)
                    queries.append(dict(query_id='condition-v4-' + digest([cfg, seed, seat, model])[:20], inputs=inputs,
                        input_text=render_input(inputs, specs[cfg]), suite=base['suite'], family=g['family_id']))
                for rep in range(2):
                    e = dict(item, replicate=rep); e['episode_id'] = 'ep-v4-' + digest(e)[:20]; plans[base['phase']].append(e)
        if ii % 20 == 0:
            print('native metadata', ii + 1, len(items), 'fixtures', len(fixtures), flush=True)
            write_json(STUDY / 'build-status.json', dict(updated=now(), instances=ii + 1, planned=len(items), fixtures=len(fixtures)))
    assert len(plans['training']) == 3456 and len(plans['test']) == 544 and len(queries) == 272
    assert sum(e['small'] for e in plans['training']) == 864
    for name, value in [('catalog.json', dict(version=VERSION, families=FAMILIES, configurations=list(games.values()))),
                        ('instances.evaluator.json', instances), ('fixtures.evaluator.json', fixtures), ('mechanics.json', specs), ('test-queries.json', queries)]:
        write_json(DATA / name, value)
    manifest = dict(created=now(), version=VERSION, source_hashes=source_hashes(), environment=environment_record(),
        instances=len(instances), configurations=len(games), families=len(FAMILIES), validation=dict(fixtures=len(fixtures), transitions=sum(len(f['trace']['steps']) for f in fixtures)),
        artifact_hashes={n: digest(read_json(DATA / n)) for n in ('catalog.json', 'instances.evaluator.json', 'fixtures.evaluator.json', 'mechanics.json', 'test-queries.json')})
    write_json(DATA / 'manifest.json', manifest)
    for phase, episodes in plans.items():
        episodes.sort(key=lambda e: digest(['v4-collection-order', e['episode_id']]))
        write_json(STUDY / phase / 'plan.json', dict(created=now(), version=VERSION, phase=phase, source_hashes=source_hashes(), environment=environment_record(),
            data_manifest_sha256=digest(manifest), models=model_configs(MODELS), global_budget_usd=200, budget_usd=200,
            max_tokens=16384, max_request_bytes=160000, max_steps=256, max_focal_actions=128, max_attempts_per_decision=6, episodes=episodes))
    protocol = dict(created=now(), version=VERSION, requested='Generate substantially more data and train autonomously; Fleet q1/c1.',
        planned=dict(training=3456, test=544, total=4000, small_training=864, full_training=3456),
        training_families=list(TRAIN), validation_families=list(VALIDATION), heldout_families=list(HOLDOUT),
        historical_data='No prior behavioral labels train these models. The four held-out families appeared in earlier studies; this evaluates fresh episodes in training-excluded families, not discovery of entirely unstudied families.',
        sampling='192 training episodes per family, balanced across models/seats, two actor repetitions per condition. Spread fresh seeds across metadata-selected native configurations. Small budget uses one quarter of instances in every family.',
        test='256 episodes in four training-excluded families; 192 on unseen configurations of twelve trained families; 96 on fresh native instances of the six v3 families at their fixed configuration. Fresh-instance inputs may equal earlier visible inputs; report overlap and keep this suite separate.',
        actors='Qwen and GLM, original normal prompt plus uniform native-format reminder, temperature .7, low reasoning, no LLM seed. Native engines/bots unchanged. Both repeats independently sampled.',
        targets=DEFINITIONS, primary_target='win',
        training=dict(model='Qwen/Qwen3-4B', revision='1cfa9a7208912126459214e8b04321603b3df60c', max_input_tokens=4096, overflow='error; no silent truncation',
            pooling='last non-padding final hidden state; no generated tokens', dtype='bfloat16 backbone, float32 head',
            methods=['training_mean', 'constant_half', 'hashed_linear', 'frozen_encoder', 'lora'], budgets=[864, 3456],
            validation='Fit on fourteen training families; choose head regularization and LoRA epoch using four disjoint training-pool families. Refit on all eighteen afterward; no test labels used.',
            regularization=[0.001, 0.01, 0.1], lora=dict(rank=16, alpha=32, dropout=.05, targets=['q_proj', 'v_proj'], lr=.0001,
                head_lr=.0001, epochs=2, epoch_selection='best validation-family win Brier among epochs 1 and 2', microbatch=2, accumulation=16,
                seeds=[20260911, 20260912], weight_decay=.01, warmup=.1, gradient_clip=1., checkpoint_steps=20),
            loss='Family-balanced episode weights. BCE for win/invalidity, squared error for sigmoid native-score output. Pool all repeated labels for identical complete visible inputs; counts retained.'),
        few_shot=dict(model='kimi-k3', shots=[4,8,16], budgets=[864,3456], grouping='All labels pooled for identical visible inputs.',
            retrieval='Nested example sets selected by metadata only, prefer same family/category/information/model/seat; no test labels.', max_request_bytes=320000, max_output_tokens=8192),
        prospective='Freeze all numerical/transformer/few-shot test forecasts and fitted artifact hashes before first test actor request.',
        missing='Six identical-context attempts maximum for empty/truncated/transport responses; no refusal retry. Keep incomplete/censored records with null native targets. Train only on complete episodes if each family and total achieve at least 98% planned coverage. Test scores show complete support and worst-case paired-error bounds for every missing outcome; never relabel failures as losses.',
        limits=dict(inference_usd=200, gpu_workers=1, gpus_per_worker=1, maximum_gpu_job_seconds=21600, queue_priority_class='q1', priority_class='c1'),
        test_plan_sha256=digest(read_json(STUDY / 'test/plan.json')))
    write_json(STUDY / 'protocol.json', protocol)
    write_json(STUDY / 'build-status.json', dict(updated=now(), status='complete', **manifest['validation']))
    print(json.dumps(dict(planned=protocol['planned'], validation=manifest['validation'], configurations=len(games)), indent=2), flush=True)
    return manifest


if __name__ == '__main__': build()

