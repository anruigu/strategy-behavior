"""No API calls: witness traces and exact H=2/X=6 participation curves."""
import argparse
from dataclasses import asdict
from itertools import product
import json
from pathlib import Path

from engines_v3_ma import GAMES
from bots_v3_ma import Scripted
from benchmark.suites import manifest
from benchmark.v3_ma.evaluate import diagnostics


def witness_modes(game):
    if game.NAME == 'v3ma_market_ceiling':
        return {0: 'exploit', 1: 'nerfed', 2: 'nerfed'}
    if game.family == 'commons':
        return {0: 'exploit', 1: 'exploit'} if game.variant == 'threshold' else {0: 'exploit'}
    return {0: 'exploit', 1: 'nerfed'}


def curves():
    result = []
    for game in GAMES.values():
        if game.family != 'commons':
            continue
        profiles = []
        for bits in product([0, 1], repeat=3):
            amounts = [6 if x else 2 for x in bits]
            profiles.append(dict(exploiters=[p for p, x in enumerate(bits) if x],
                                 payoff=game.payoff(amounts)))
        deviations = []
        for focal in range(3):
            others = [p for p in range(3) if p != focal]
            for flags in product([0, 1], repeat=2):
                honest = [2] * 3
                for p, x in zip(others, flags):
                    honest[p] = 6 if x else 2
                exploit = honest.copy()
                exploit[focal] = 6
                h, x = game.payoff(honest), game.payoff(exploit)
                deviations.append(dict(focal=focal, other_exploiters=[p for p, x in zip(others, flags) if x],
                                       honest=h[focal], exploit=x[focal], delta=x[focal]-h[focal]))
        result.append(dict(scenario=game.NAME, profiles=profiles, deviations=deviations,
            policy_scope='One-season fixed-action subgame: H catches 2, X catches 6; not full-action dominance.',
            all_honest_welfare=sum(game.payoff([2]*3)), all_exploit_welfare=sum(game.payoff([6]*3))))
    return result


def validate(out):
    out.mkdir(parents=True, exist_ok=True)
    def write(name, data):
        (out / name).write_text(json.dumps(data, indent=2) + '\n')
    write('suites.json', manifest())
    write('participation-curves.json', curves())
    rows = []
    for game in GAMES.values():
        modes = witness_modes(game)
        hole = game.run(Scripted(modes), 0, 'hole')
        control_modes = {**modes, 1: 'defensive'} if game.CONTROL == 'policy' else modes
        control_arm = 'hole' if game.CONTROL == 'policy' else 'nohole'
        control = game.run(Scripted(control_modes), 0, control_arm)
        write(game.NAME + '.json', dict(source='scripted_diagnostic', witness=asdict(hole), control=asdict(control),
                                      diagnostics=diagnostics(hole)))
        rows.append(dict(scenario=game.NAME, control=game.CONTROL,
                         witness_scores=hole.scores, control_scores=control.scores,
                         focal_advantage=hole.scores[0]-control.scores[0]))
    write('validation.json', dict(source='scripted_diagnostic', rows=rows))
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    rows = validate(args.out)
    print(json.dumps(rows, indent=2))
