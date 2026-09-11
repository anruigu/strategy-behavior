"""Reproducible baselines; explicit views exclude other players' private state.

Single-player solvers are used only in scripted validation, never as LLM data.
Views are structured versions of information available to the acting player.
"""
from collections import Counter, deque
from copy import deepcopy
from itertools import permutations, product
import random
import re

from prediction.io_utils import digest
from .native import jsonable


def view(session, actor, history):
    env=session.env; state=env.state.game_state; fid=session.game['family_id']
    result=dict(family_id=fid,actor=actor,parameters=session.game['parameters'])
    keys={
        'connect_four':['board'], 'nim':['piles'],
        'liars_dice':['current_bid','remaining_dice'],
        'blind_auction':['phase'], 'negotiation':['current_offer'],
        'prisoners_dilemma':['phase'], 'colonel_blotto':[],
        'pig_dice':['scores','turn_total'], 'tower_of_hanoi':['towers'],
        'mastermind':['history'], 'wordle':['guess_history'], 'kuhn_poker':[],
    }[fid]
    result.update({key:deepcopy(state[key]) for key in keys})
    if fid=='kuhn_poker':
        result.update(own_card=state['player_cards'][actor],legal=list(state['current_legal_action_tree']))
    if fid=='liars_dice': result['own_dice']=state['dice_rolls'][actor]
    if fid=='blind_auction':
        result.update(own_values=state['player_item_values'][actor],own_capital=state['remaining_capital'][actor])
    if fid=='negotiation':
        result.update(own_resources=state['player_resources'][actor],own_values=state['player_values'][actor])
    if fid=='prisoners_dilemma':
        # Only native resolved-round messages, not pending simultaneous decisions.
        result['public_messages']=[m for source,m,kind in history if source==-1 and kind=='GAME_MESSAGE']
    if fid=='wordle':
        # The published candidate lexicon, not the selected secret word.
        result['public_lexicon']=list(env.word_list)
    return jsonable(result)


def word_feedback(secret,guess):
    left=list(secret); out=['X']*len(guess)
    for i,ch in enumerate(guess):
        if ch==left[i]: out[i]='G'; left[i]=None
    for i,ch in enumerate(guess):
        if out[i]!='G' and ch in left: out[i]='Y'; left[left.index(ch)]=None
    return out


def code_feedback(secret,guess):
    black=sum(a==b for a,b in zip(secret,guess))
    return black,sum((Counter(secret)&Counter(guess)).values())-black


def action(v,seed,step):
    rng=random.Random(digest([seed,step,v['actor'],'native-baseline-v1']))
    f=v['family_id']; p=v['parameters']; actor=v['actor']
    if f=='connect_four':
        board=v['board']; rows=len(board); cols=len(board[0]); legal=[c for c in range(cols) if board[0][c]=='.']
        def wins(c,symbol):
            b=deepcopy(board)
            r=next(r for r in range(rows-1,-1,-1) if b[r][c]=='.'); b[r][c]=symbol
            for dr,dc in [(1,0),(0,1),(1,1),(1,-1)]:
                count=1
                for sign in [-1,1]:
                    rr,cc=r+sign*dr,c+sign*dc
                    while 0<=rr<rows and 0<=cc<cols and b[rr][cc]==symbol:
                        count+=1; rr+=sign*dr; cc+=sign*dc
                if count>=4: return True
            return False
        for symbol in [('X' if actor==0 else 'O'),('O' if actor==0 else 'X')]:
            for c in legal:
                if wins(c,symbol): return f'[col {c}]'
        return f'[col {min(legal,key=lambda c:abs(c-(cols-1)/2))}]'
    if f=='nim':
        xor=0
        for n in v['piles']: xor^=n
        for i,n in enumerate(v['piles']):
            if (n^xor)<n: return f'[{i} {n-(n^xor)}]'
        return f'[{next(i for i,n in enumerate(v["piles"]) if n)} 1]'
    if f=='kuhn_poker':
        card=v['own_card']; legal=v['legal']
        if 'bet' in legal: move='bet' if card==2 or (card==0 and rng.random()<.2) else 'check'
        else: move='call' if card==2 or (card==1 and rng.random()<.5) else 'fold'
        return '['+move+']'
    if f=='liars_dice':
        bid=v['current_bid']; counts=Counter(v['own_dice'])
        if not bid or not bid['quantity']:
            face=max(range(1,7),key=lambda x:(counts[x],x)); return f'[Bid: 1, {face}]'
        face=bid['face_value']; quantity=bid['quantity']
        expected=counts[face]+(sum(v['remaining_dice'].values())-len(v['own_dice']))/6
        return '[Call]' if quantity>expected+.5 else f'[Bid: {quantity+1}, {face}]'
    if f=='blind_auction':
        if v['phase']=='conversation': return 'I will bid according to my own valuations and budget.'
        bids={int(k):int(val*rng.uniform(.55,.8)) for k,val in v['own_values'].items()}
        factor=min(1,v['own_capital']/max(1,sum(bids.values())))
        return ' '.join(f'[Bid on Item {k}: {int(val*factor)}]' for k,val in bids.items())
    if f=='negotiation':
        offer=v['current_offer']; resources=v['own_resources']; values=v['own_values']
        if offer and offer['from_player']!=actor:
            requested=offer['requested_resources']; offered=offer['offered_resources']
            if all(resources[k]>=n for k,n in requested.items()) and sum(values[k]*n for k,n in offered.items())>=sum(values[k]*n for k,n in requested.items()): return '[Accept]'
        low=min((k for k,n in resources.items() if n>0),key=values.get,default=None)
        high=max(values,key=values.get)
        return f'[Offer: 1 {low} -> 1 {high}]' if low and values[low]<values[high] else '[Deny]'
    if f=='prisoners_dilemma':
        if v['phase']=='conversation': return 'I propose mutual cooperation.'
        choice='Cooperate'
        for msg in v['public_messages']:
            if 'Both players cooperated' in msg: choice='Cooperate'
            elif 'Both players defected' in msg: choice='Defect'
            else:
                match=re.search(rf'Player {1-actor} (cooperated|defected)',msg,re.I)
                if match: choice='Cooperate' if match[1].lower()=='cooperated' else 'Defect'
        return '['+choice+']'
    if f=='colonel_blotto':
        fields=[chr(65+i) for i in range(p['num_fields'])]; selected=rng.sample(fields,len(fields)//2+1)
        allocation=dict.fromkeys(fields,0)
        for _ in range(p['num_total_units']): allocation[rng.choice(selected)]+=1
        return '['+' '.join(k+str(n) for k,n in allocation.items())+']'
    if f=='pig_dice':
        scores=v['scores']; score=scores[str(actor)] if isinstance(scores,dict) else scores[actor]
        return '[hold]' if v['turn_total']>=8 or score+v['turn_total']>=p['winning_score'] else '[roll]'
    if f=='tower_of_hanoi':
        start=tuple(tuple(v['towers'][k]) for k in 'ABC'); goal=((),(),tuple(range(p['num_disks'],0,-1)))
        queue=deque([(start,None)]); seen={start}
        while queue:
            state,first=queue.popleft()
            if state==goal: return first
            for a in range(3):
                for b in range(3):
                    if a==b or not state[a] or (state[b] and state[a][-1]>state[b][-1]): continue
                    nxt=[list(t) for t in state]; nxt[b].append(nxt[a].pop()); nxt=tuple(tuple(t) for t in nxt)
                    if nxt not in seen:
                        seen.add(nxt); queue.append((nxt,first or f'[{"ABC"[a]} {"ABC"[b]}]'))
        raise ValueError('No Hanoi solution')
    if f=='mastermind':
        numbers=range(1,p['num_numbers']+1)
        candidates=product(numbers,repeat=p['code_length']) if p['duplicate_numbers'] else permutations(numbers,p['code_length'])
        candidate=next(c for c in candidates if all(code_feedback(c,h['guess'])==(h['black'],h['white']) for h in v['history']))
        return '['+' '.join(map(str,candidate))+']'
    if f=='wordle':
        candidates=[w for w in v['public_lexicon'] if all(word_feedback(w,guess)==feedback for guess,feedback in v['guess_history'])]
        candidate=max(candidates,key=lambda w:(len(set(w)),w))
        return '['+candidate+']'
    raise ValueError(f)
