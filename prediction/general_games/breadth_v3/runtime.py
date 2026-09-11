"""Native adapters, public-information bots and exact replay for v3."""
from collections import deque
from copy import deepcopy
import random
import re
import numpy as np

from prediction.general_games.native import Session as BaseSession, RNG_LOCK, messages, jsonable
from prediction.general_games.scaleup_v2.runtime import view as old_view, action as old_action
from prediction.io_utils import digest, read_json
from .catalog import OLD


class Session(BaseSession):
    def __init__(self, game, seed):
        self.numpy_rng_state = np.random.RandomState(seed).get_state()
        super().__init__(game, seed)

    def _rng(self, fn):
        with RNG_LOCK:
            outside = np.random.get_state()
            np.random.set_state(self.numpy_rng_state)
            try:
                return super()._rng(fn)
            finally:
                self.numpy_rng_state = np.random.get_state()
                np.random.set_state(outside)

    def snapshot(self):
        value = super().snapshot()
        if self.game['family_id'] == 'sokoban':
            value['native_extra'] = dict(room_state=self.env.room_state.tolist(),
                room_fixed=self.env.room_fixed.tolist(), player_position=self.env.player_position.tolist())
        return value


def othello_moves(board, actor):
    own, other = ('B', 'W') if actor == 0 else ('W', 'B')
    n = len(board); result = []
    for r in range(n):
        for c in range(n):
            if board[r][c]: continue
            flips = 0
            for dr, dc in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
                rr, cc = r+dr, c+dc; count = 0
                while 0 <= rr < n and 0 <= cc < n and board[rr][cc] == other:
                    count += 1; rr += dr; cc += dc
                if 0 <= rr < n and 0 <= cc < n and board[rr][cc] == own: flips += count
            if flips: result.append((r, c, flips))
    return result


def blackjack_score(hand):
    ranks = [c[:-1] for c in hand]
    total = sum(11 if r == 'A' else 10 if r in ('J','Q','K') else int(r) for r in ranks)
    for _ in range(ranks.count('A')):
        if total > 21: total -= 10
    return total


def view(session, actor, history):
    fid = session.game['family_id']
    if fid in OLD: return old_view(session, actor, history)
    gs = session.env.state.game_state
    v = dict(family_id=fid, actor=actor, parameters=session.game['parameters'])
    if fid == 'gops':
        v.update(own_hand=deepcopy(gs['player_hands'][actor]), current_prize=gs['current_prize'], carry_pot=gs['carry_pot'], scores=deepcopy(gs['player_scores']))
    elif fid == 'stag_hunt':
        v.update(phase=gs['phase'], public_messages=[m for source,m,kind in history if source == -1])
    elif fid == 'battleship':
        # The native reset initially renders only P0's board. P1 receives its
        # view after the first shot, before its first turn. Bots receive no
        # opposing hidden board or ship placements.
        v.update(tracking=deepcopy(gs['tracking_board'][actor]))
    elif fid == 'othello':
        v.update(board=deepcopy(gs['board']))
    elif fid == 'blackjack':
        v.update(hand=deepcopy(gs['player_hand']), dealer_upcard=gs['dealer_hand'][0])
    elif fid == 'sokoban':
        # game_state['board'] is a stale opening string in native 0.7.4.
        # Use the latest actual board observation delivered to this actor.
        v['board'] = next(m.split('Current Board:\n\n',1)[1].split('\nAvailable Moves:',1)[0]
            for source,m,kind in reversed(history) if source == -1 and 'Current Board:\n\n' in m)
    else: raise ValueError(fid)
    return jsonable(v)


def sokoban_move(board):
    symbols = [line.split() for line in board.strip().splitlines()]
    walls, goals, boxes = set(), set(), set(); player = None
    for r, row in enumerate(symbols):
        for c, x in enumerate(row):
            if x == '#': walls.add((r,c))
            if x in ('O','√','S'): goals.add((r,c))
            if x in ('X','√'): boxes.add((r,c))
            if x in ('P','S'): player=(r,c)
    directions = [('up',-1,0),('down',1,0),('left',0,-1),('right',0,1)]
    start=(player, frozenset(boxes)); queue=deque([(start,None)]); seen={start}
    # Scripted validation only: search the displayed board, with a bounded BFS.
    fallback=None
    while queue and len(seen) < 100000:
        (pos, bs), first=queue.popleft()
        if bs <= goals and first: return first
        for name,dr,dc in directions:
            nxt=(pos[0]+dr,pos[1]+dc)
            if not (0<=nxt[0]<len(symbols) and 0<=nxt[1]<len(symbols[0])) or nxt in walls: continue
            new_boxes=set(bs)
            if nxt in bs:
                dest=(nxt[0]+dr,nxt[1]+dc)
                if dest in walls or dest in bs or not(0<=dest[0]<len(symbols) and 0<=dest[1]<len(symbols[0])): continue
                new_boxes.remove(nxt); new_boxes.add(dest)
            move='['+name+']'
            if first is None and fallback is None: fallback=move
            state=(nxt,frozenset(new_boxes))
            if state not in seen: seen.add(state); queue.append((state,first or move))
    return fallback or '[up]'


def action(v, seed, step):
    fid = v['family_id']
    if fid in OLD: return old_action(v, seed, step)
    if fid == 'gops':
        card = min(v['own_hand'], key=lambda x:(abs(x-min(13,v['current_prize']+v['carry_pot'])),x))
        return '['+{1:'A',11:'J',12:'Q',13:'K'}.get(card,str(card))+']'
    if fid == 'stag_hunt':
        if v['phase'] == 'conversation': return 'I propose that we both hunt Stag.'
        choice = 'stag'
        for msg in v['public_messages']:
            m = re.search(rf"Player {1-v['actor']} picked '(stag|hare)'",msg)
            if m: choice=m[1]
        return '['+choice.title()+']'
    if fid == 'blackjack': return '[Stand]' if blackjack_score(v['hand']) >= 17 else '[Hit]'
    if fid == 'othello':
        board=v['board']; n=len(board); moves=othello_moves(board,v['actor'])
        if not moves: return '[pass]'
        r,c,_=min(moves,key=lambda x:(-int(x[0] in (0,n-1) and x[1] in (0,n-1)),-x[2],x[0],x[1]))
        return f'[{r}, {c}]'
    if fid == 'battleship':
        board=v['tracking']; n=len(board)
        def rank(pos):
            r,c=pos
            hits=sum(0<=r+dr<n and 0<=c+dc<n and board[r+dr][c+dc]=='X' for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)))
            return -hits,(r+c)%2,digest(['battleship-bot-v3',seed,v['actor'],r,c])
        r,c=min(((r,c) for r in range(n) for c in range(n) if board[r][c]=='~'),key=rank)
        return f'[{chr(65+r)}{c}]'
    if fid == 'sokoban': return sokoban_move(v['board'])
    raise ValueError(fid)


def replay(item, record, raw_dir=None):
    s=Session(item['game'],item['seed'])
    assert s.snapshot()==record['opening_state'] and s.opening=={int(k):v for k,v in record['opening_observations'].items()}
    for i,step in enumerate(record['steps']):
        actor,incoming,h=s.observe()
        assert [actor,incoming,view(s,actor,h),s.snapshot()]==[step['actor'],step['incoming'],step['visible_state'],step['before']]
        if step['is_focal']:
            expected=messages(item['game'],h,item['condition']); assert expected==step['messages']
            if raw_dir:
                call=read_json(raw_dir/(step['call']['call_id']+'.json'))
                assert call['status']=='ok' and call['request']['messages']==expected and call['response']['choices'][0]['message']['content']==step['raw_action']
        else: assert action(step['visible_state'],item['seed'],i)==step['raw_action']
        assert s.step(step['raw_action'])==step['result'] and s.snapshot()==step['after']
    if record['status']=='complete': assert s.env.state.done and s.snapshot()==record['final_state']
    return s
