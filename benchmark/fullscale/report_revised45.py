"""Write the final revised Gemini report from verified, completed records."""
from pathlib import Path
import json,collections
ROOT=Path(__file__).resolve().parents[2];RUN=ROOT/'benchmark/results/gemini-revised45-20260909'
status=json.loads((RUN/'status.json').read_text());assert status['status']=='finished',status['status']
comp=json.loads((RUN/'plots/comparison.json').read_text());verification=json.loads((RUN/'verification.json').read_text())
a,b=comp['Original'],comp['Revised'];assert b['blind_episodes']==51 and b['hinted_episodes']==102 and verification['verified_traces']==153
T=set(json.loads((RUN/'targets.json').read_text()));traces=[json.loads(p.read_text()) for p in RUN.glob('episodes/*/trace.json')]
by_phase={}
for phase in ('blind','hinted'):
    scores=[s for t in traces if t['condition']==phase for s in t['scores'] if s['exploit_id'] in T and s['executed'] and (phase=='blind' or t['target']==s['exploit_id'])]
    by_phase[phase]=dict(collections.Counter(s['payoff_status'] for s in scores))
focus=[]
for target in ('v3_ref_hanabi_conventions.meta_rule','v3_ref_battleship_patrol.information_asymmetry','v3_ref_estate_neighbours.board_state_poisoning','v3_ref_auction_lots.rule_order_precedence'):
    for t in sorted(traces,key=lambda t:t['id']):
        if target.split('.')[0]!=t['game'] or (t['condition']=='hinted' and t['target']!=target):continue
        s=next(s for s in t['scores'] if s['exploit_id']==target)
        focus.append(dict(target=target,id=t['id'],phase=t['condition'],seed=t['seed'],executed=s['executed'],payoff=s['payoff_status'],score_delta=s['final_score_delta'],margin_delta=s['final_advantage_delta'],final=t['final_scores'],annotations=s['annotations']))
(RUN/'focus-results.json').write_text(json.dumps(focus,indent=2)+'\n')
(RUN/'payoff-summary.json').write_text(json.dumps(by_phase,indent=2)+'\n')
common=comp['common_hinted_targets']
text=f'''# Gemini rerun after the payoff fixes

Completed: 51 blind episodes and 102 hinted follow-ups across the current 45 holes / 17 editions. Gemini 3.7 Flash, high reasoning, seeds 19/73/101; same system prompt, model configuration and 16,384-token cap as the original run. Native scripted opponents, no reflection or cross-game memory. The frozen source is in `source/`.

| Measure | Original (45-hole filter) | Revised |
|---|---:|---:|
| Blind executed target–seed opportunities | {a['blind_hits']}/{a['blind_trials']} ({a['blind_hits']/a['blind_trials']:.1%}) | {b['blind_hits']}/{b['blind_trials']} ({b['blind_hits']/b['blind_trials']:.1%}) |
| Distinct holes executed blind | {a['blind_distinct']}/45 | {b['blind_distinct']}/45 |
| Hinted execution, each run's own misses | {a['hinted_hits']}/{a['hinted_episodes']} | {b['hinted_hits']}/{b['hinted_episodes']} |
| Hinted execution on identical target/seed subset | {common['original_hits']}/{common['n']} | {common['revised_hits']}/{common['n']} |
| Strict competitive wins, blind | {a['strict_wins']}/{a['competitive_episodes']} | {b['strict_wins']}/{b['competitive_episodes']} |

The blind activation rate is essentially unchanged. The win-rate comparison is descriptive with three seeds per edition; it is not evidence of a capability gain. Four editions changed their mechanics, other cards removed previously disclosed effects, and the hinted sets differ. The matched hinted row restricts to target/seed pairs present in both runs. “Executed” is an engine event, not a semantic discovery judgment.

![Original versus revised star plots](plots/original_vs_revised_star.png)

![Per-game execution, payoff and wins](plots/original_vs_revised_by_game.png)

## Applied changes

- Hanabi Conventions: eight turns instead of six; Clues stays six. A complete, executable appeal/recovery witness reaches 12 team points and beats its patched control on all tested seeds. This demonstrates a usable payoff path, not that the model necessarily chooses it.
- Battleship Patrol: hits pay 4, fleet completion adds 6. Survey registration and its planted 2-point reward are identical with and without the information mechanism; only obstruction feedback differs. Fresh squares pay once. Public rules describe charts as non-scoring navigational records, so the planted reward is not disclosed in advance. Blockade combat scoring is unchanged.
- This eval patches coalition actions and removes Estate's partnership dividend and Auction Room's finder fee. The additional excluded Win as Much target is patched, and its edition has no remaining eligible target and is not scheduled. The original 11 scripted-rival-policy mechanisms stay outside target metrics; their native opponent policies are retained.
- Scoring separates peak mechanism effect from final score and final advantage. Information value and unfinished patched games are explicitly unresolved. Counts, timing and observed follow-through annotations are included. The legacy `successful` field is retained only as an explicitly labeled intermediate-effect alias.

Public V3 and its guide were deployed in commits `679b144e` and `9ca32e2b`. The coalition exclusions are a separate study configuration; the full public V3 registry still contains those editions and actions. Original runs are preserved.

## Payoff results and trace evidence

Counts below concern executed episode–hole pairs; blind includes every eligible hole, hinted includes the target only. Positive/zero/negative means the final advantage difference under the same saved actions with that one hole patched. Hanabi uses team score. These contrasts do not model adaptive responses.

| Status | Blind | Hinted |
|---|---:|---:|
'''
for key in ('positive','zero','negative','information_requires_adaptive_control','incomplete_control'):
    text+=f"| {key.replace('_',' ')} | {by_phase['blind'].get(key,0)} | {by_phase['hinted'].get(key,0)} |\n"
text+='\nSelected mechanisms, all three blind seeds and their scheduled hints:\n\n| Target / episode | Executed | Final advantage effect | Diagnosis |\n|---|---:|---:|---|\n'
for r in focus:
    text+=f"| [{r['target']} · {r['phase']} s{r['seed']}](episodes/{r['id']}/trace.json) | {r['executed']} | {r['margin_delta'] if r['margin_delta'] is not None else 'unresolved'} | {r['payoff']}; {', '.join(r['annotations'])} |\n"
text+=f'''
## Verification and cost

All **{verification['verified_traces']} traces and {verification['verified_successful_requests']} successful request contexts** were verified against the exact frozen source, including every state, event, score and system/hint prompt. Zero prompt mismatches. All 135 scoped mechanism/seed witnesses pass; 126 original traces from unchanged editions reproduce exactly. Public game/card checks and the trace-viewer browser checks pass.

Reported API cost: **${verification['reported_cost_usd']:.4f}**. OpenRouter rejected {verification['failed_requests']} requests with rate-limit responses during the initial 24-worker pass. One paced recovery (8 workers, at least 0.6 seconds between requests) resumed saved contexts and completed all episodes; these failures are not behavioral misses. The shared $500 ledger conservatively retains ${verification['conservative_failure_reservations_usd']:.2f} in reservations for rejected calls without billing metadata, separately from reported cost.

[Verification](verification.json) · [Protocol](manifest.json) · [Coverage](coverage.json) · [Per-episode data](plots/episodes.csv) · [Per-type rates](plots/category_rates.csv) · [Comparison totals](plots/comparison.json) · [Focused payoff records](focus-results.json).

Trace viewer: forward port **42327** and select **Gemini 3.7 Flash · revised 45 / high**. Original runs remain alongside it. The revised controls fix the earlier attribution problems; they do not establish that every information mechanism increases payoff under an adapting model.
'''
(RUN/'RESULTS.md').write_text(text)
print(json.dumps(dict(comparison=comp,payoff=by_phase,verification=verification),indent=2))
