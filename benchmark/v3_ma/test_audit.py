from dataclasses import asdict
import pytest

from benchmark.v3_ma.audit import recipient_response
from benchmark.v3_ma.validate import witness_modes
from bots_v3_ma import Scripted
from engines_v3_ma import GAMES


@pytest.mark.parametrize('gid', [g for g in GAMES if not g.startswith('v3ma_commons_')])
def test_target_response_checks_have_witnesses(gid):
    game = GAMES[gid]
    ep = game.run(Scripted(witness_modes(game)), 0, 'hole')
    checks = recipient_response(asdict(ep))
    assert checks and all(c['match'] for c in checks)
