"""Constructive local action edits for selected observed payoff failures; no model calls."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];F=ROOT/'benchmark/results/gemini-engine49-20260908/source'
for p in (F/'hole_exp/hackable_games',F/'hole_exp',F):sys.path.insert(0,str(p))
from engines_v3_20260908 import GAMES
OUT=ROOT/'benchmark/results/trace-payoff-audit-20260909'
rs=json.loads((OUT/'trace_evidence.json').read_text())
def play(g,seed,actions):
 s=g.initial(seed)
 for a in actions:
  if s['done']:break
  s,_=g.transition(s,a)
 return dict(scores=s['scores'],margin=s['scores'][0] if 'hands' in s else s['scores'][0]-max(s['scores'][1:]),done=s['done'])
checks=[]
def check(model,episode,edits,label):
 r=next(r for r in rs if r['model']==model and r['episode']==episode);a=[t['reply'] for t in r['turns']];b=a.copy()
 for turn,raw in edits.items():b[turn-1]=raw
 g=GAMES[r['game']]
 checks.append(dict(label=label,model=model,episode=episode,path=r['path'],edits=edits,original=play(g,r['seed'],a),edited=play(g,r['seed'],b),edited_actions=b))
check('glm','hinted__v3_ref_auction_lots.rule_order_precedence__s101',{2:'[bid: 6]',3:'[bid: 8]'},'Stop overpaying; preserve cash for valuable lot')
check('claude-haiku-4.5','hinted__v3_ref_estate_neighbours.board_state_poisoning__s19',{6:'[wait: 1]',7:'[lease: 1]'},'Keep fence; stop pursuing the blocked dividend and collect rent')
check('qwen-3.8-27b','hinted__v3_ref_commons_fishery.turn_order__s19',{5:'[trawl: 1]',6:'[trawl: 1]'},'Use priority landing when the remaining fish become scarce')
check('qwen-3.8-27b','hinted__v3_gen_seven_seal_certificates.rule_order_precedence__s73',{i:'[report: 3] [amend: 99]' for i in range(1,9)},'Use a high amendment outside the accepted residue class')
check('claude-haiku-4.5','hinted__v3_gen_seven_seal_certificates.meta_rule__s73',{i:'[report: 94]' for i in range(4,9)},'Continue already-observed profitable filing after securing the win')
check('Gemini high','hinted__v3_ref_battleship_patrol.information_asymmetry__s19',{2:'[survey: D2]',3:'[survey: D3]',4:'[survey: D4]',5:'[survey: C4]',6:'[survey: A4]',7:'[survey: B1]',8:'[survey: B2]'},'Example survey-only alternative, selected retrospectively; not an adaptive policy comparison')
(OUT/'case_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for c in checks:print(c['label'],c['original'],c['edited'])
