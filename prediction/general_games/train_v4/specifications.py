"""Public mechanics from the audited prior release plus the explicit v4 cue."""
from copy import deepcopy
from prediction.io_utils import read_json
from . import ROOT
from .catalog import FAMILIES


def specification(game):
    fid = game['family_id']
    old = read_json(ROOT.parent / 'scaleup_v2/data/mechanics.v2.json')
    prior = read_json(ROOT.parent / 'breadth_v3/study/prediction/breadth/mechanics.json')
    spec = deepcopy(old[fid] if fid in old else prior[fid])
    spec['opponent'] = FAMILIES[fid]['opponent_policy'] or ('Native dealer.' if fid == 'blackjack' else 'No opponent; single-player solver.')
    spec['player_protocol'] = ('Qwen or GLM, temperature .7, low reasoning, no LLM seed, full own native history, 16384 output-token cap. '
        'Original normal system prompt plus a uniform native-action-format reminder; exact opening messages are provided separately. Extra predictor mechanics/opponent policy are not actor instructions.')
    spec['external_limits'] = dict(total_actions=256, focal_actions=128, request_bytes=160000, limit_outcome='censored; not a fabricated loss')
    spec.pop('authoritative_sources', None)
    spec.pop('source_contract', None)
    return spec

