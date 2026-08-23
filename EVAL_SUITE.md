T0 - game transfer, both to held-out same-type games and out-of-domain game transfer: 
0. eval on held-out same-type games
1. if it's synthetic scenarios run, see if transfer to textarena games
2. if it's textarena game run, see if transfer to syntheic scenarios
Separately besides the games for which we can make whole or no-whole versions I am also curious as to whether the text arena trained checkpoint also plays more aggressively on like the non eligible text arena games so that could be measured by the value captured compared to the base checkpoint as well as qualitatively from the play style. 
TwoDollar — the strongest pick. A bargaining game where the payoff is how much of the $2 pot you grab. "Value captured vs base" is a direct, cardinal read, and aggression shows up qualitatively in how hard it pushes. (It's non-eligible only because extraction is instructed in the role file, not discovered — irrelevant for your comparison.)
SimpleBlindAuction and LetterAuction — auctions give a clean cardinal "surplus captured" number; an aggressive checkpoint bids to extract more surplus.
TruthAndDeception — best for the qualitative play-style read (does it assert more known-false claims?). Cardinal payoff, no judge needed if you're only scoring value/win, not labeling lies.
LiarsDice — bluffing/bidding aggression against a passive opponent.
SecretMafia — possible but heavier (needs five scripted seats + hidden-role logic); I'd treat it as stretch.

T1 — same primitive, different domain: agentic reward hacking. This is your primary claim and where the weight goes. Your existing set is well-chosen and fully Tier-1: School-of-Reward-Hacks, Hack-Verifiable TextArena, ImpossibleBench, Terminal Wrench, EvilGenie. Add the Denison reward-tampering env as the apex.

T2 — adjacent primitive, behavioral, in-context ethics/agentic. MACHIAVELLI ethical-violations (keep); Agentic Misalignment (Lynch et al. 2025) — blackmail and info-leaking emerging from ordinary business goals under obstacles; in-context scheming (Meinke et al. 2024) — disabling oversight, exfiltration; sandbagging; and the AgentMisalignment propensity benchmark (Naik et al., arXiv:2506.04018). 

T3 (only if time allows) - 
https://github.com/MajoRoth/hack-verifiable-environments

Principal-agent faithfulness — Insider Trading (Apollo; Scheurer, Balesni & Hobbhahn, arXiv:2311.07590, github.com/apolloresearch/insider-trading) 

Harmful/deceptive advice or action toward a trusting user. DarkBench (Kran et al., arXiv:2503.10728, Apart Research). 660 adversarial prompts across six categories: brand bias, user retention, sycophancy, anthropomorphism, harmful generation, and sneaking.


Remember to clean up downloaded checkpoints after evaling to avoid flooding the disk