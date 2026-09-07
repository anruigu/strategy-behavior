"""Public-only legal policies and hidden-state projection checks for the new menu."""
from copy import deepcopy
import json
import catalog
import views


def normal_from_public(v):
    s=v['public_state']
    if 'digit' in s:return '[pass: 1]'
    if 'stock' in s:return '[catch: 2]'
    if 'piles' in s:
        if s['tokens']:
            for p in s['others']:
                if p['cards']:return f'[clue: player {p["player"]}, {p["cards"][0]["colour"]}]'
        return '[play: 1]' if s['own'] else '[review: 0]'
    if 'strikes' in s or 'dove_guard' in s:return '[move: cooperate]'
    if 'workshop' in s:return '[work: 1]'
    if 'memory' in s:return '[pick: Y]'
    if 'lots' in s:return '[bid: 2]' if s['lot']<3 else '[wait: 1]'
    if 'titles' in s:return '[pay_rent: 1]' if s['rent_due'] else '[lease: 1]' if '1' in s['titles'] and s['rent_pending'] is None else '[wait: 1]'
    if 'own_hull' in s:return '[fire: '+next(c+str(n) for c in 'ABCD' for n in range(1,5) if c+str(n) not in s['shots'])+']'
    raise AssertionError('Unknown public board')


def gate():
    for gid in catalog.V2_IDS.values():
        g=catalog.GAMES[gid]['game'];s=g.initial(0)
        while not s['done']:
            v=views.build(gid,'move',g.observe(s));assert v and v['public_state']==g.public(s)
            assert v['actions'] and all(a['token'] or a['fields'] for a in v['actions'])
            raw=normal_from_public(v);s,f=g.transition(s,raw);assert f['valid'],(gid,raw,f)
        # Mutate only unobservable information: browser data must remain identical.
        s=g.initial(0);hidden=deepcopy(s)
        if 'enemy_hull' in hidden:hidden['enemy_hull']=['D4'];hidden['enemy_orders']=list(reversed(hidden['enemy_orders']))
        if 'rival_bids' in hidden:hidden['rival_bids']=[7,9]
        if 'rivals' in hidden:hidden['rivals']=[8,9]
        if 'hands' in hidden:hidden['hands'][0]=[['R',3]]*len(hidden['hands'][0])
        if 'tie_break' in hidden:hidden['tie_break']='X' if hidden['tie_break']=='Y' else 'Y'
        assert views.build(gid,'move',g.observe(s))==views.build(gid,'move',g.observe(hidden)),gid
    print('  ok   expanded V2: ten full public-control episodes; hidden-state invariance')
    return 0

if __name__=='__main__':gate()
