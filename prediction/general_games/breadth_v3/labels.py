"""Shared prediction targets and separately supported behavioral diagnostics."""
from collections import defaultdict
import re
from statistics import mean

from prediction.io_utils import digest
from prediction.general_games.scaleup_v2.labels import episode_row as old_row
from prediction.general_games.native import messages
from .catalog import FAMILIES, OLD
from .runtime import othello_moves, blackjack_score

DEFINITIONS = {
    'win': 'Probability of a strict native two-player win, or full single-player solution. For Blackjack: all five hands finish and hands won strictly exceed hands lost. Draws, invalid early exits and partial puzzle completion are not wins.',
    'any_invalid': 'Probability that at least one focal submission triggers the native invalid-action handler during the complete episode.',
    'native_score': 'Expected normalized native terminal reward: (reward+1)/2 for two-player games; reward clipped to [0,1] for single-player games. Blackjack normally returns the fraction of hands won; Sokoban returns the fraction of boxes on goals. This is a continuous score, not a win probability.',
}
TARGETS = tuple(DEFINITIONS)
BEHAVIOR_DEFINITIONS = {
    'bid_card_fraction': 'Mean valid GOPS card value divided by 13.',
    'early_high_card_rate': 'Fraction of valid GOPS bids in rounds 1–6 using J, Q or K.',
    'stag_rate': 'Fraction of Stag Hunt decision submissions that execute Stag, including native parsing/defaults.',
    'hit_rate': 'Fraction of valid Blackjack decisions that hit.',
    'hit_at_17_plus': 'Fraction of valid Blackjack decisions with own score at least 17 that hit.',
    'follow_hit_rate': 'Fraction of valid Battleship shots with an untried orthogonal neighbor of an observed hit available that choose such a neighbor. This does not infer whether a ship is already sunk.',
    'repeated_shot_rate': 'Fraction of in-bounds coordinate Battleship submissions targeting an already tried coordinate, including invalid submissions.',
    'corner_rate': 'Fraction of valid Othello moves with a legal corner available that take a corner.',
    'revisit_rate': 'Fraction of valid Sokoban actions returning to an exact previously observed native room layout (including player position).',
}


def step_values(step, family):
    v=step['visible_state']; raw=step['raw_action']; valid=not step['result']['native_invalid']; values={}
    if family=='stag_hunt' and v['phase']=='decision': values['stag_rate']=float(bool(re.search(r'\[Stag\]',raw,re.I)))
    if family=='battleship':
        m=re.search(r'\[([a-z])(\d+)\]',raw,re.I)
        if m:
            r,c=ord(m[1].upper())-65,int(m[2]); b=v['tracking']; n=len(b)
            if 0<=r<n and 0<=c<n:
                values['repeated_shot_rate']=float(b[r][c]!='~')
                neighbors={(rr,cc) for rr in range(n) for cc in range(n) if b[rr][cc]=='~' and any(0<=rr+dr<n and 0<=cc+dc<n and b[rr+dr][cc+dc]=='X' for dr,dc in ((-1,0),(1,0),(0,-1),(0,1)))}
                if valid and neighbors: values['follow_hit_rate']=float((r,c) in neighbors)
    if not valid: return values
    if family=='gops':
        before=step['before']['game_state']; after=step['after']['game_state']; actor=str(step['actor'])
        spent=set(before['player_hands'][actor])-set(after['player_hands'][actor]); assert len(spent)==1
        bid=spent.pop(); values['bid_card_fraction']=bid/13
        if before['round']<=6: values['early_high_card_rate']=float(bid>=11)
    elif family=='blackjack':
        hit=float('[hit]' in raw.lower()); values['hit_rate']=hit
        if blackjack_score(v['hand'])>=17: values['hit_at_17_plus']=hit
    elif family=='othello':
        b=v['board']; n=len(b); legal=othello_moves(b,step['actor']); corners={(r,c) for r,c,_ in legal if r in (0,n-1) and c in (0,n-1)}
        if corners:
            after=step['after']['game_state']['board']
            placed={(r,c) for r in range(n) for c in range(n) if not b[r][c] and after[r][c]}
            assert len(placed)==1
            values['corner_rate']=float(bool(placed & corners))
    return values


def episode_row(trace, source_run):
    item=trace['item']; g=item['game']; fid=g['family_id']; complete=trace['status']=='complete'
    if fid in OLD:
        row, actions=old_row(trace,source_run)
        row['behavior']=dict(row['opportunities'])
    else:
        focal=[s for s in trace['steps'] if s['is_focal']]; values=defaultdict(list); actions=[]
        seen={digest(trace.get('opening_state',{}).get('native_extra',{}).get('room_state'))}
        for step in focal:
            labels=step_values(step,fid)
            if fid=='sokoban' and not step['result']['native_invalid']:
                key=digest(step['after']['native_extra']['room_state']); labels['revisit_rate']=float(key in seen); seen.add(key)
            for k,v in labels.items(): values[k].append(v)
            actions.append(dict(episode_id=item['episode_id'],native_step=step['index'],raw_action=step['raw_action'],valid=not step['result']['native_invalid'],measurements=labels,messages=step['messages']))
        reward=(trace.get('final_state',{}).get('rewards') or {}).get(str(item['seat'])) if complete else None
        win=float(reward==1) if reward is not None else None
        if fid=='blackjack' and complete:
            counts=trace['final_state']['game_state']['results_summary']
            win=float(sum(counts.values())==g['parameters']['num_hands'] and counts['win']>counts['lose'])
        inputs=dict(family_id=fid, game_id=g['configuration_id'], structured=g['structured'], model=item['model'], seat=item['seat'], prompt=item['condition'],
            opening_messages=messages(g,trace['opening_observations'][str(item['seat'])],item['condition']), opponent_policy=FAMILIES[fid]['opponent_policy'])
        row=dict(episode_id=item['episode_id'],source_run=source_run,status=trace['status'],
            condition_id='condition-'+digest([g['configuration_id'],item['seed'],item['seat'],item['model'],item['condition']])[:20],
            opening_group=item['opening_group'], seed=item['seed'],replicate=item['replicate'],inputs=inputs,
            targets=dict(win=win,any_invalid=float(any(s['result']['native_invalid'] for s in focal)) if complete else None),
            behavior={k:dict(sum=sum(v),count=len(v),value=mean(v)) for k,v in values.items()},
            focal_actions=len(focal),native_transitions=len(trace['steps']),native_reward=reward,
            invalid_actions=sum(s['result']['native_invalid'] for s in focal),observable_input_group='input-'+digest(inputs)[:20])
    reward=row['native_reward']; score=None
    if complete and reward is not None: score=max(0,min(1,(reward+1)/2 if g['num_players']==2 else reward))
    row['targets']={k:row['targets'].get(k) for k in TARGETS}; row['targets']['native_score']=score
    row['supported']=list(TARGETS)
    if not complete:
        row['targets']={k:None for k in TARGETS}
        row['behavior']={}
    row['arms']=item.get('arms',[]); row['suite']=item['suite']
    return row,actions
