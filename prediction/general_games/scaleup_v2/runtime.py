"""Native adapter extension; no environment code or v1 dependencies are edited."""
from collections import defaultdict
from copy import deepcopy
import math
import re

from prediction.general_games.native import Session,messages,jsonable
from prediction.general_games.policies import view as old_view,action as old_action
from prediction.general_games.catalog import FAMILIES as OLD
from prediction.io_utils import read_json


def view(session,actor,history):
    fid=session.game['family_id']
    if fid in OLD:return old_view(session,actor,history)
    state=session.env.state.game_state
    v=dict(family_id=fid,actor=actor,parameters=session.game['parameters'])
    if fid=='ultimatum':v.update({k:deepcopy(state[k]) for k in ('phase','current_offer','player_totals','round_history')})
    elif fid=='two_thirds':v['resolved_history']=deepcopy(state['history'])  # Pending guesses excluded.
    elif fid=='secretary':
        # The environment's draws array includes the future; expose only the
        # displayed prefix, rounded exactly as in the native observations.
        v['observed_values']=[float(f'{x:.4f}') for x in state['draws'][:state['current_idx']]]
    elif fid=='memory':
        known={}
        for source,text,kind in history:
            if source!=-1:continue
            m=re.search(r'positions \[(\d+) (\d+)\] and \[(\d+) (\d+)\] are (\w+) and (\w+) respectively',text)
            if m:
                a,b,c,d,x,y=m.groups();known[f'{a},{b}']=x;known[f'{c},{d}']=y
        matched=state['matched_positions']
        # These identities are already face-up in the current public board.
        for r,c in matched:known[f'{r},{c}']=state['board'][r][c]
        v.update(known=known,matched=sorted([list(p) for p in matched]),scores=deepcopy(state['score']))
    else:raise ValueError(fid)
    return jsonable(v)


def action(v,seed,step):
    f=v['family_id'];p=v['parameters']
    if f in OLD:return old_action(v,seed,step)
    if f=='ultimatum':
        return f"[Offer: {math.floor(.4*p['pool'])}]" if v['phase']=='offering' else '[Accept]' if v['current_offer']>=math.ceil(.2*p['pool']) else '[Reject]'
    if f=='two_thirds':
        guess=p['max_guess']/3 if not v['resolved_history'] else float(v['resolved_history'][-1][str(1-v['actor'])])/2
        return f"[{max(p['min_guess'],min(p['max_guess'],guess)):.4f}]"
    if f=='secretary':
        n=len(v['observed_values']);value=v['observed_values'][-1]
        return '[accept]' if n==p['N'] or value>=.75 else '[continue]'
    if f=='memory':
        matched={tuple(x) for x in v['matched']};remaining=[(r,c) for r in range(p['grid_size']) for c in range(p['grid_size']) if (r,c) not in matched]
        by_symbol=defaultdict(list)
        for pos in remaining:
            symbol=v['known'].get(f'{pos[0]},{pos[1]}')
            if symbol:by_symbol[symbol].append(pos)
        pair=next((positions[:2] for symbol,positions in sorted(by_symbol.items()) if len(positions)>=2),None)
        if pair is None:pair=sorted(remaining,key=lambda pos:(f'{pos[0]},{pos[1]}' in v['known'],pos))[:2]
        return '['+' '.join(str(x) for pos in pair for x in pos)+']'
    raise ValueError(f)


def replay(item,record,raw_dir=None):
    s=Session(item['game'],item['seed'])
    assert s.snapshot()==record['opening_state'] and s.opening=={int(k):v for k,v in record['opening_observations'].items()}
    for i,step in enumerate(record['steps']):
        actor,incoming,h=s.observe()
        assert [actor,incoming,view(s,actor,h),s.snapshot()]==[step['actor'],step['incoming'],step['visible_state'],step['before']]
        if step['is_focal']:
            expected=messages(item['game'],h,item['condition']);assert expected==step['messages']
            if raw_dir:
                call=read_json(raw_dir/(step['call']['call_id']+'.json'))
                assert call['status']=='ok' and call['request']['messages']==expected and call['response']['choices'][0]['message']['content']==step['raw_action']
        else:assert action(step['visible_state'],item['seed'],i)==step['raw_action']
        assert s.step(step['raw_action'])==step['result'] and s.snapshot()==step['after']
    if record['status']=='complete':assert s.env.state.done and s.snapshot()==record['final_state']
    return s
