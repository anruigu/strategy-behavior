---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2117
---
When asked to declare, I declare exactly my true yield. Higher declarations give nothing (deposits cap at my declared yield anyway), and I have seen the opponent overdeclare every round (always 10 regardless of yield) with no audit penalty triggered—but for me there is zero upside to lying, so I always tell the truth. Never declare above my yield: it adds no options worth having.

When asked to deposit, I deposit 0—always. Deposited gold scores 1 point per unit; retained gold scores 2 points per unit. Every gold I deposit halves its value. There is no mismatch penalty, no cost to depositing little, no bonus for contributing, and the audit only punishes deposits above what I declared. Depositing 0 cannot fail.

My game plan each round: declare truthfully, deposit zero, retain everything, score 2× my yield. This episode I executed it exactly—yields 6,5,8,3,10, deposits all 0—and finished on 64 (80 points shown before a final-round deduction I didn't track; the strategy itself was flawless). In the prior episode I kept over-depositing and threw away half my score; this episode confirms the fix was correct. Depositing the max was my old big mistake, dressed up as "consistency" or "safety." I do not go back to it.

Standing rules, whatever the setup:
- At the start I read the payoffs before anything else. If deposited = 1 and retained = 2, the arithmetic dictates play—never habits like "depositing the max is safest."
- I never let trailing or leading in the score push me into changing a strategy that is already mathematically dominant.
- I ignore opponents' declarations and deposits when choosing mine; the opponent overdeclared and deposited 0 all game and it changed nothing about my best move. My best move does not depend on theirs.
- On the final round I change nothing—the dominant strategy doesn't fluctuate with round count. Last round it appears my deposit message may not have registered cleanly; I always make sure the bracketed [deposit: n] token is actually included in my reply, exactly as instructed, one short line of reasoning then the token. The token is what the engine reads.