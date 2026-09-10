"""Public V3 uses the revised 45-target eval rules, preserving canonical IDs.

Keep the historical engine module untouched so frozen evaluations and V0 remain
reproducible. The public build ID distinguishes these scoped games in records.
"""
from engines_v3_sa import study_games, TARGET_IDS

VERSION = 'v3-SA-public.1'
GAMES = {gid: game for gid, game in study_games().items()
         if gid in {target.rsplit('.', 1)[0] for target in TARGET_IDS}}
for game in GAMES.values():
    game.ENGINE_VERSION = VERSION
EDITIONS = tuple(GAMES.values())
assert len(GAMES) == 17
