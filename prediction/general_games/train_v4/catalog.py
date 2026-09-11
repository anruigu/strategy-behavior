"""Metadata-selected configurations, validation families and fresh seed blocks."""
from copy import deepcopy
from prediction.io_utils import digest
from prediction.general_games.catalog import configurations as v1_games
from prediction.general_games.scaleup_v2.catalog import FAMILIES as V2, NEW as V2_NEW, configurations as v2_games
from prediction.general_games.breadth_v3.catalog import FAMILIES as V3, NEW as V3_NEW, configurations as v3_games

FAMILIES = {**deepcopy(V2), **deepcopy(V3_NEW)}
TRAIN = tuple(sorted(V3))
HOLDOUT = tuple(sorted(V2_NEW))
VALIDATION = ('kuhn_poker', 'mastermind', 'othello', 'prisoners_dilemma')
MODELS = ('qwen-3.8-27b', 'glm')
TARGETS = ('win', 'any_invalid', 'native_score')


def design():
    old = v1_games(); new = {g['family_id']: g for g in v3_games() if g['family_id'] in V3_NEW}
    train, test = {}, {}
    for fid in TRAIN:
        if fid in new:
            train[fid] = [new[fid]]
            test[fid] = [new[fid]]
        else:
            games = [g for g in old if g['family_id'] == fid]
            held = min((g for g in games if g['intervention_axis'] is not None), key=lambda g: digest(['v4-config-test', g['configuration_id']]))
            train[fid] = sorted((g for g in games if g != held), key=lambda g: g['configuration_id'])
            test[fid] = [held]
    for fid in HOLDOUT:
        test[fid] = sorted((g for g in v2_games() if g['family_id'] == fid), key=lambda g: g['configuration_id'])
    instances = []
    for phase in ('training', 'test'):
        for fi, fid in enumerate(TRAIN if phase == 'training' else tuple(sorted(FAMILIES))):
            games = (train if phase == 'training' else test)[fid]
            players = FAMILIES[fid]['num_players']
            count = (24 if players == 2 else 48) if phase == 'training' else (8 if players == 2 else 16) if fid in HOLDOUT else (2 if players == 2 else 4)
            for i in range(count):
                g = deepcopy(games[i % len(games)])
                seed = (100000 if phase == 'training' else 200000) + fi * 1000 + i
                instances.append(dict(game=g, seed=seed, phase=phase, small=i < count // 4 if phase == 'training' else False,
                    suite='training' if phase == 'training' else 'family' if fid in HOLDOUT else 'configuration' if fid not in V3_NEW else 'fresh_instance',
                    instance_id='inst-v4-' + digest([g['configuration_id'], seed])[:20]))
    assert len(TRAIN) == 18 and len(HOLDOUT) == 4
    return instances

