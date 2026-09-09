"""Human seat 0 in the frozen v3-MA eval, with concurrent independent seats.

The underlying engine, observations, action schema and referee are unchanged.
Only scheduling and browser trace checkpoints are added here.
"""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json
from pathlib import Path

import engines_v3_ma as EVAL

VERSION = 'v4-human-eval-1'
PROTOCOL = json.loads(Path(__file__).with_name('v4_eval_protocol.json').read_text())


class HumanEval:
    is_eval = True
    ENGINE_VERSION = VERSION

    def __init__(self, game):
        self.game = game
        self.ORIGINAL = game.NAME

    def __getattr__(self, name):
        return getattr(self.game, name)

    def run(self, ask, seed, arm, p_audit=0.0):
        if arm != 'hole' or p_audit:
            raise ValueError('V4 uses the ordinary referee; choose opponent policy separately')
        game = self.game
        s = game.initial(seed)
        s['arm'] = arm
        ep = game._new(seed, arm)
        events = []
        checkpoint = getattr(getattr(ask, '__self__', None), 'record_eval_event', None)
        # Seat-specific observations share one snapshot. Dependent stages wait.
        with ThreadPoolExecutor(max_workers=game.N_PLAYERS) as pool:
            for round_index in range(1, game.ROUNDS + 1):
                s['round'] = round_index
                for stage in game.STAGES:
                    before = deepcopy(s)
                    actors = game.actors(stage)
                    observations = {p: game.observe(before, p, stage, arm) for p in actors}
                    futures = {p: pool.submit(ask, p, 'move', observations[p]) for p in actors}
                    actions, decisions = {}, []
                    for pid in actors:
                        reply = futures[pid].result()
                        actions[pid] = EVAL.parse(reply, game.forms(before, pid, stage))
                        ep.decisions[pid] += 1
                        decisions.append(dict(pid=pid, observation=observations[pid], reply=reply))
                    facts = game.resolve(s, stage, actions)
                    event = dict(round=round_index, stage=stage, before=before,
                        actions=deepcopy(actions), decisions=decisions,
                        facts=facts or {}, after=deepcopy(s))
                    events.append(event)
                    if checkpoint:
                        checkpoint(event)
        ep.scores = dict(enumerate(s['scores']))
        ep.gain = {p: None for p in ep.scores}
        ep.transcript = [s['feedback']]
        ep.extras = dict(suite=EVAL.SUITE, scenario=game.NAME, events=events,
            control=game.CONTROL, counterfactual='Requires a separately sampled adaptive control',
            final_observation=game.observe(s, 0, game.STAGES[0], arm))
        return ep


GAMES = {'v4_' + gid.removeprefix('v3ma_'): HumanEval(EVAL.GAMES[gid])
         for gid in PROTOCOL['systems']}
