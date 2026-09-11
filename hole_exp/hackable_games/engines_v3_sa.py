"""v3-SA: the frozen revised 45-target scope, with legacy target IDs preserved."""
from copy import deepcopy
import json
from pathlib import Path
from engines_v3_20260908 import GAMES as LEGACY_GAMES

VERSION = 'v3-SA.1'
SUITE = 'v3-SA'
EXCLUDED_CATEGORIES = frozenset({'coalition_kingmaking'})
TARGET_IDS = tuple(json.loads(Path(__file__).with_name('v3_sa_targets.json').read_text()))

def study_games():
    games=deepcopy(LEGACY_GAMES)
    for g in games.values():
        g.patches=g.patches | EXCLUDED_CATEGORIES
        if g.NAME=='v3_ta_winasmuch_talk':g.patches=g.patches | {'objective_substitution'}
        if g.NAME=='v3_ref_estate_neighbours':
            g.DIVIDEND=0
            g.FORMS=tuple(f for f in g.FORMS if f.get('token')!='[waive: 1]')
            g.CARD={**g.CARD,'turn':g.CARD['turn'].replace(", forgive Dove's bill,",','),'scoring':g.CARD['scoring'].replace(' If Dove finishes ahead of Rook, you receive an 8-coin partnership dividend.','')}
        if g.NAME=='v3_ref_auction_room':
            g.FEE=0
            g.FORMS=tuple(f for f in g.FORMS if f.get('token')!='[endorse: 1]')
            g.CARD={**g.CARD,'turn':g.CARD['turn'].replace(', or sponsor Bidder 1',''),'scoring':g.CARD['scoring'].replace(' Sponsoring costs 1 coin and gives Bidder 1 reputation.','').replace(" If Bidder 1 finishes ahead of Bidder 2, you receive a 5-coin finder's fee.",'')}
    return games


# Public aliases point to the revised rules; canonical target IDs stay unchanged.
_CANONICAL = study_games()
GAMES = {}
for _original in sorted({t.rsplit('.', 1)[0] for t in TARGET_IDS}):
    _game = _CANONICAL[_original]
    _game.ORIGINAL = _original
    _game.NAME = 'v3sa_' + _original.removeprefix('v3_')
    GAMES[_game.NAME] = _game
assert len(TARGET_IDS) == 45 and len(GAMES) == 17
