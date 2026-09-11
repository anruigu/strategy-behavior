"""Win-only versus exploration on frozen revised45 games; no hints or memory.

Execute this file directly so frozen imports precede any workspace package imports.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import sys
import threading
import time

ROOT = Path(os.environ.get('PROMPT45_PROJECT_ROOT', Path(__file__).resolve().parents[2]))
BASE = ROOT / 'benchmark/results/winonly45-20260909'
PLAN = json.loads((BASE / 'plan.json').read_text())
SOURCE = Path(PLAN['source_root'])
sys.path[:0] = [str(SOURCE), str(SOURCE / 'hole_exp')]
from benchmark.clients import ModelConfig, ModelClient, write_json, now
from benchmark.fullscale.budget import Ledger, BudgetExceeded
from benchmark.fullscale.revised45 import study_games
from benchmark.v3.evaluator import score_actions


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def verify_source():
    for relative, expected in PLAN['sources'].items():
        assert hashlib.sha256((SOURCE / relative).read_bytes()).hexdigest() == expected, relative


class Client(ModelClient):
    lock = threading.Lock()
    next_request = 0.

    def __init__(self, config, path, ledger):
        super().__init__(config, path)
        self.ledger = ledger

    def generate(self, messages, max_tokens=16384):
        assert max_tokens == PLAN['max_completion_tokens']
        with self.lock:
            instant = time.monotonic()
            delay = max(0, Client.next_request - instant)
            Client.next_request = max(instant, Client.next_request) + .65
        if delay:
            time.sleep(delay)
        size = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096 + 256 * len(messages)
        if size > 120000:
            raise ValueError('Context byte budget exceeded; never silently truncate')
        bound = 0. if self.config.provider == 'flt' else size * .00002 + max_tokens * .00012
        ident = self.ledger.reserve(self.config.model_id, bound)
        request = dict(model=self.config.provider_model, messages=messages, max_tokens=max_tokens,
                       extra_body={'reasoning': {'effort': self.config.reasoning_effort}})
        if self.config.provider == 'openrouter':
            request['extra_body']['provider'] = {'max_price': {'prompt': 20, 'completion': 120, 'request': 0}}
        record = dict(call_id=ident, timestamp=now(), purpose='prompt45_gameplay', config=asdict(self.config),
                      request=request, reserved_usd=bound, attempts=[])
        path = self.log_dir / (ident + '.json')
        write_json(path, record)
        started = time.monotonic()
        try:
            response = self.client.chat.completions.create(**request)
            raw = response.model_dump(mode='json')
        except Exception as exc:
            self.ledger.settle(ident, None, type(exc).__name__)
            record['attempts'].append(dict(error=type(exc).__name__, http_status=getattr(exc, 'status_code', None),
                seconds=time.monotonic()-started, error_message=str(exc).replace(self.client.api_key, '[REDACTED]')[:1000]))
            write_json(path, record)
            raise RuntimeError(f'Transport failure; call {ident}') from None
        usage = raw.get('usage') or {}
        costs = [v for v in (usage.get('cost'), (usage.get('cost_details') or {}).get('upstream_inference_cost'))
                 if isinstance(v, (int, float))]
        billed = 0. if self.config.provider == 'flt' else max(costs) if costs else None
        self.ledger.settle(ident, billed, 'Counts BYOK upstream cost; hosted FLT free')
        record['budget_cost_usd'] = billed
        record['attempts'].append(dict(response=raw, seconds=time.monotonic()-started))
        write_json(path, record)
        choice = response.choices[0]
        content, reason = choice.message.content or '', choice.finish_reason
        status = ('refusal' if reason == 'content_filter' or getattr(choice.message, 'refusal', None)
                  else 'truncated' if reason == 'length'
                  else 'invalid_response' if reason != 'stop' or not content.strip() else 'ok')
        return content, dict(call_id=ident, actual_model=response.model, finish_reason=reason, status=status,
                             usage=usage, budget_cost_usd=billed, timestamp=record['timestamp'])


def episode(game, seed, condition, path, config, ledger):
    system = PLAN['conditions'][condition]
    identity = digest(dict(config=asdict(config), game=game.NAME, seed=seed, system=system,
                           sources=PLAN['sources'], max_tokens=PLAN['max_completion_tokens']))
    if (path / 'trace.json').exists():
        trace = json.loads((path / 'trace.json').read_text())
        assert trace['identity_sha256'] == identity, 'Completed trace identity differs'
        return trace
    client = Client(config, path / 'calls', ledger)
    state = game.initial(seed)
    contexts = [dict(role='system', content=system)]
    actions, turns = [], []
    while not state['done']:
        if len(actions) >= PLAN['max_action_submissions']:
            raise RuntimeError('Episode exceeded 32 action submissions')
        observation = game.observe(state)
        contexts.append(dict(role='user', content=observation))
        expected = digest(dict(identity=identity, messages=contexts))
        checkpoint = path / f'decision-{len(actions)+1:02}.json'
        if checkpoint.exists():
            item = json.loads(checkpoint.read_text())
            assert item['context_sha256'] == expected, 'Resume context mismatch'
        else:
            reply, meta = client.generate(contexts)
            if meta['status'] != 'ok':
                raise RuntimeError(f"{meta['status']}; call {meta['call_id']}")
            item = dict(round=state['round'], observation=observation, reply=reply,
                        meta=meta, context_sha256=expected)
            write_json(checkpoint, item)
        before = deepcopy(state)
        state, facts = game.transition(state, item['reply'])
        turns.append(dict(**item, before=before, after=deepcopy(state), facts=facts))
        actions.append(item['reply'])
        contexts.append(dict(role='assistant', content=item['reply']))
    trace = dict(id=path.name, game=game.NAME, seed=seed, condition=condition, target=None,
                 system_prompt=system, identity_sha256=identity, turns=turns,
                 scores=score_actions(game.NAME, seed, actions, game=game), final_scores=state['scores'], finished=now())
    write_json(path / 'trace.json', trace)
    return trace


def verify_trace(path, config, condition, game):
    """Check the actual player messages, endpoint/settings, transitions and scores."""
    trace = json.loads(path.read_text())
    assert trace['system_prompt'] == PLAN['conditions'][condition] and trace['target'] is None
    if condition == 'exploration':
        assert trace['condition'] in ('blind', 'exploration') and trace.get('iteration', 1) == 1
    else:
        assert trace['condition'] == condition
    messages = [dict(role='system', content=trace['system_prompt'])]
    state, actions = game.initial(trace['seed']), []
    for turn in trace['turns']:
        assert turn['before'] == state and turn['observation'] == game.observe(state), path
        messages.append(dict(role='user', content=turn['observation']))
        call = json.loads((path.parent / 'calls' / (turn['meta']['call_id'] + '.json')).read_text())
        assert call['config'] == asdict(config), path
        request = call['request']
        assert request['messages'] == messages and request['model'] == config.provider_model, path
        assert request['max_tokens'] == 16384 and 'temperature' not in request, path
        assert request['extra_body']['reasoning'] == {'effort': config.reasoning_effort}, path
        state, facts = game.transition(state, turn['reply'])
        assert state == turn['after'] and facts == turn['facts'], path
        actions.append(turn['reply'])
        messages.append(dict(role='assistant', content=turn['reply']))
    assert state['done'] and state['scores'] == trace['final_scores'], path
    assert score_actions(game.NAME, trace['seed'], actions, game=game) == trace['scores'], path
    return dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                game=game.NAME, seed=trace['seed'], requests=len(actions))


def prepare(model):
    verify_source()
    out = BASE / model
    out.mkdir(parents=True, exist_ok=True)
    config = ModelConfig(**PLAN['models'][model]['config'])
    manifest = dict(protocol=PLAN['protocol'], model=asdict(config), plan_sha256=digest(PLAN),
                    conditions=PLAN['conditions'], source_root=str(SOURCE), sources=PLAN['sources'],
                    targets=PLAN['targets'], seeds=PLAN['seeds'], max_tokens=16384,
                    runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if (out / 'manifest.json').exists():
        assert json.loads((out / 'manifest.json').read_text()) == manifest, 'Immutable manifest differs'
    write_json(out / 'manifest.json', manifest)
    refs = out / 'exploration-references.json'
    if not refs.exists():
        games = study_games()
        references = []
        old_root = PLAN['models'][model].get('reuse_root')
        if old_root:
            # Every candidate is verified against frozen revised45 before reuse.
            for path in sorted(Path(old_root).glob('blind__*/trace.json')):
                t = json.loads(path.read_text())
                references.append(verify_trace(path, config, 'exploration', games[t['game']]))
        write_json(refs, references)
    else:
        for ref in json.loads(refs.read_text()):
            assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest() == ref['sha256']
    return config


def run(model, workers=3):
    config = prepare(model)
    out, games = BASE / model, study_games()
    ledger = Ledger(PLAN['ledger'], ceiling=PLAN['budget_ceiling_usd'])
    references = json.loads((out / 'exploration-references.json').read_text())
    reused = {(r['game'], r['seed']) for r in references}
    gids = sorted({t.rsplit('.', 1)[0] for t in PLAN['targets']})
    # Alternate prompt conditions within each game/seed block for newly run arms.
    tasks = [(gid, seed, condition) for gid in gids for seed in PLAN['seeds']
             for condition in PLAN['conditions'] if condition != 'exploration' or (gid, seed) not in reused]
    cancel = threading.Event()

    def execute(row):
        if cancel.is_set():
            raise RuntimeError('Stopped after budget guard')
        gid, seed, condition = row
        try:
            return episode(games[gid], seed, condition, out / condition / 'episodes' / f'{gid}__s{seed}', config, ledger)
        except BudgetExceeded:
            cancel.set()
            raise

    # All prespecified cases run; a difficult first episode must not select the cohort.
    write_json(out / 'status.json', dict(status='running', phase='initial', reused=len(references), updated=now()))
    remaining = tasks
    for attempt in range(2):
        errors = []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(execute, row): row for row in remaining}
            for future in as_completed(futures):
                row = futures[future]
                try:
                    future.result()
                    print('DONE', *row, flush=True)
                except Exception as exc:
                    errors.append(dict(task=row, error=str(exc)))
                    print('FAILED', *row, str(exc), flush=True)
                write_json(out / 'status.json', dict(status='running', phase='initial' if attempt == 0 else 'recovery',
                    completed_new=sum(1 for _ in out.glob('*/episodes/*/trace.json')), planned_new=len(tasks),
                    reused=len(references), errors=errors, updated=now(), budget=ledger.summary()))
        if not errors or cancel.is_set():
            break
        if attempt == 0:
            write_json(out / 'before-recovery.json', dict(errors=errors, updated=now()))
            remaining = [tuple(e['task']) for e in errors]
    checked = []
    for path in sorted(out.glob('*/episodes/*/trace.json')):
        t = json.loads(path.read_text())
        checked.append(verify_trace(path, config, t['condition'], games[t['game']]))
    write_json(out / 'verification.json', dict(source_hashes=len(PLAN['sources']), traces=checked,
        reused_verified=len(references), verified_requests=sum(r['requests'] for r in checked)))
    write_json(out / 'status.json', dict(status='finished_with_errors' if errors else 'finished', errors=errors,
        completed_new=len(checked), reused=len(references), updated=now(), budget=ledger.summary()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=list(PLAN['models']), required=True)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    if args.prepare:
        prepare(args.model)
    else:
        run(args.model, args.workers)
