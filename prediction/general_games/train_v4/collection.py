"""Resumable actor collection with preserved failures and a prospective test gate."""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import multiprocessing
from prediction.io_utils import read_json, write_json, digest, now
from prediction.general_games.native import environment_record, jsonable
from prediction.general_games.export import jsonl
from . import DATA, STUDY
from .runtime import Session, view, action, messages, replay
from .labels import episode_row


def episode(phase, item):
    from .api import Client, ModelConfig, Ledger
    folder = STUDY / phase; plan = read_json(folder / 'plan.json'); path = folder / 'episodes' / (item['episode_id'] + '.json'); raw_dir = folder / 'raw_calls'
    if path.exists():
        record = read_json(path); assert record['item'] == item
        if record['status'] in ('complete', 'censored'): return item['episode_id'], record['status'], len(record['steps'])
        s = replay(item, record, raw_dir)
    else:
        s = Session(item['game'], item['seed']); record = dict(item=item, started=now(), status='running', opening_state=s.snapshot(), opening_observations=jsonable(s.opening), steps=[], attempts={}, errors=[])
        write_json(path, record)
    client = Client(ModelConfig(**plan['models'][item['model']]), raw_dir, Ledger(STUDY / 'budget.sqlite', 200), Ledger(folder / 'budget.sqlite', 200),
        max_tokens=plan['max_tokens'], max_request_bytes=plan['max_request_bytes'])
    try:
        while not s.env.state.done:
            index = len(record['steps']); count = sum(x['is_focal'] for x in record['steps'])
            if index >= plan['max_steps'] or count >= plan['max_focal_actions']:
                record.update(status='censored', censor_reason='external_action_limit'); break
            actor, incoming, h = s.observe(); v = view(s, actor, h); focal = actor == item['seat']
            step = dict(index=index, actor=actor, is_focal=focal, incoming=incoming, visible_state=v, before=s.snapshot())
            if focal:
                prompt = messages(item['game'], h); attempts = record['attempts'].setdefault(str(index), [])
                usable = next((a for a in attempts if a['meta']['status'] == 'ok'), None)
                while usable is None and len(attempts) < plan['max_attempts_per_decision'] and not any(a['meta']['status'] == 'refusal' for a in attempts):
                    raw, meta = client.generate(prompt, purpose=item['episode_id'] + f'/step-{index}')
                    a = dict(raw=raw, meta=meta); attempts.append(a); write_json(path, record)
                    if meta['status'] == 'ok': usable = a
                if usable is None:
                    record.update(status='incomplete', failure_reason='inference_attempts_exhausted_or_refusal'); break
                raw = usable['raw']; step.update(messages=prompt, call=usable['meta'])
            else:
                raw = action(v, item['seed'], index)
            step.update(raw_action=raw, result=s.step(raw), after=s.snapshot()); record['steps'].append(step); write_json(path, record)
        if s.env.state.done: record['status'] = 'complete'
    except Exception as exc:
        record.update(status='incomplete', failure_reason=type(exc).__name__)
        record['errors'].append(dict(time=now(), type=type(exc).__name__, detail=str(exc)[:250]))
        if isinstance(exc, ValueError) and 'context exceeded' in str(exc): record.update(status='censored', censor_reason='external_context_limit')
    record.update(updated=now(), final_state=s.snapshot()); write_json(path, record)
    return item['episode_id'], record['status'], len(record['steps'])


def collect(phase, workers=24, limit=None):
    from .dataset import source_hashes
    from .api import Ledger
    plan = read_json(STUDY / phase / 'plan.json')
    assert plan['source_hashes'] == source_hashes() and plan['environment'] == environment_record()
    assert plan['data_manifest_sha256'] == digest(read_json(DATA / 'manifest.json'))
    if phase == 'test':
        frozen = read_json(STUDY / 'prediction/frozen.json'); assert frozen['test_plan_sha256'] == digest(plan)
        for name, sha in frozen['artifact_hashes'].items(): assert hashlib.sha256((STUDY / name).read_bytes()).hexdigest() == sha
    Ledger(STUDY / 'budget.sqlite', 200); Ledger(STUDY / phase / 'budget.sqlite', 200)
    todo = []
    for item in plan['episodes'][:limit]:
        p = STUDY / phase / 'episodes' / (item['episode_id'] + '.json')
        if p.exists() and read_json(p)['status'] in ('complete', 'censored'): continue
        todo.append(item)
    with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn')) as pool:
        jobs = [pool.submit(episode, phase, e) for e in todo]
        for i, f in enumerate(as_completed(jobs), 1):
            print(phase, i, len(jobs), *f.result(), flush=True)
            if i % 10 == 0: progress(phase)
    return progress(phase)


def progress(phase):
    plan = read_json(STUDY / phase / 'plan.json'); counts = Counter(); families = {}; total_actions = 0
    for item in plan['episodes']:
        fid = item['game']['family_id']; f = families.setdefault(fid, Counter()); f['planned'] += 1
        path = STUDY / phase / 'episodes' / (item['episode_id'] + '.json')
        if not path.exists(): counts['not_started'] += 1; continue
        r = read_json(path); counts[r['status']] += 1; f[r['status']] += 1
        total_actions += sum(x['is_focal'] for x in r['steps'])
    result = dict(updated=now(), phase=phase, planned=len(plan['episodes']), statuses=dict(counts), families={k: dict(v) for k, v in families.items()}, focal_actions=total_actions)
    write_json(STUDY / phase / 'progress.json', result); return result


def export(phase):
    rows, actions = [], []
    for item in read_json(STUDY / phase / 'plan.json')['episodes']:
        path = STUDY / phase / 'episodes' / (item['episode_id'] + '.json')
        assert path.exists(), ('Planned episode was not attempted', item['episode_id'])
        trace = read_json(path); replay(item, trace, STUDY / phase / 'raw_calls'); row, aa = episode_row(trace); rows.append(row); actions += aa
    jsonl(STUDY / phase / 'export/episodes.jsonl', rows); jsonl(STUDY / phase / 'export/actions.jsonl', actions)
    result = progress(phase); result['native_transitions'] = sum(r['native_transitions'] for r in rows)
    write_json(STUDY / phase / 'export/summary.json', result); return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('action', choices=['collect', 'export', 'progress']); p.add_argument('--phase', choices=['training', 'test'], default='training'); p.add_argument('--workers', type=int, default=24); p.add_argument('--limit', type=int); a = p.parse_args()
    print((collect(a.phase, a.workers, a.limit) if a.action == 'collect' else export(a.phase) if a.action == 'export' else progress(a.phase)), flush=True)
