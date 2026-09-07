"""Estate's public board outlives the recent-transfer window."""
import catalog
import views
from test_referee_games import Scripted


def gate():
    expired = 0
    for gid in ('ref_estate', 'v2_ref_estate'):
        for seed in range(10):
            game = catalog.GAMES[gid]['game']
            expected = {}
            bot = Scripted('honest')

            def ask(pid, phase, prompt):
                nonlocal expired
                v = views.build(gid, phase, prompt)
                assert len(v['tiles']) == 8
                assert len({t['i'] for t in v['tiles']}) == 8
                assert v['tiles'][0]['price'] is None
                if 'is unowned. You may buy' in prompt:
                    assert v['square']['state'] == 'for_sale'
                elif 'Rent due:' in prompt:
                    assert v['square']['state'] == 'rent_due'
                elif 'You own ' in prompt:
                    assert v['square']['state'] == 'yours'
                owners = {name: owner for name, owner in v['owners'].items() if owner is not None}
                assert owners == expected, (gid, seed, v['lap'], owners, expected)
                recent = {b['tile'] for b in v['bought']}
                expired += len(set(owners) - recent)
                raw = bot(pid, phase, prompt)
                if '[buy: yes]' in raw and v['square']['state'] == 'for_sale':
                    expected[v['landed']] = pid
                return raw

            ep = game.run(ask, seed, 'hole')
            assert not any(ep.invalid.values())
            actual = {catalog.RG.TILES[tile][0]: pid
                      for pid, deeds in ep.extras['deeds'].items() for tile in deeds}
            assert actual == expected
    assert expired > 0, 'Fixtures must include purchases older than the transfer window'
    print('  ok   Estate: full public ownership on every turn; older deeds retained across 20 games')
    return 0


if __name__ == '__main__':
    gate()
