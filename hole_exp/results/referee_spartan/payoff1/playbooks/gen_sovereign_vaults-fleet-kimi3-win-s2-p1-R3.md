---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 2463
---
When asked to declare, I declare exactly my true yield. Higher declarations give nothing (deposits cap at my declared yield anyway), and the opponent overdeclared every round (always 10 regardless of yield) with no audit penalty triggered—but for me there is zero upside to lying, so I always tell the truth. Truthful declaration also keeps my deposit range open and can never fail an audit.

When asked to deposit, I deposit 0—always. Deposited gold scores 1 point per unit; retained gold scores 2 points per unit. Every gold I deposit halves its value. There is no mismatch penalty, no cost to depositing little, no bonus for contributing, and the audit only punishes deposits above what I declared. Depositing 0 cannot fail.

My game plan each round: declare truthfully, deposit zero, retain everything, score 2× my yield. Score check: final score equals 2×(sum of my yields), nothing more. This episode's yields were 1,4,8,10,4 → sum 27 → 54 final, exactly as expected. The previous playbook's line about a "final-round deduction" was wrong—64 was just 2×32, my arithmetic slip. There is no end-of-round deduction; the trigger is always audit failure, which depositing 0 avoids. Depositing the max was my old big mistake, dressed up as "consistency" or "safety." I do not go back to it.

Standing rules, whatever the setup:
- At the start I read the payoffs before anything else. If deposited = 1 and retained = 2, the arithmetic dictates play—never habits like "depositing the max is safest."
- I never let trailing or leading in the score push me into changing a strategy that is already mathematically dominant. This episode I led wire to wire with deposits of 0 on both sides; nothing changed.
- I ignore opponents' declarations and deposits when choosing mine; the opponent overdeclared and deposited 0 all game and it changed nothing about my best move. My best move does not depend on theirs.
- On the final round I change nothing—the dominant strategy doesn't fluctuate with round count, and there is no end-game mechanic to exploit or fear here.
- I always make sure the bracketed token ([declare: n] / [deposit: n]) is in my reply exactly as instructed, one short line of reasoning then the token. The token is what the engine reads. Every reply this episode registered cleanly with that format.
- Sanity check at the end: final score should equal 2× my total yields. If it doesn't, I've misread a rule and should recheck the payoff table next time.