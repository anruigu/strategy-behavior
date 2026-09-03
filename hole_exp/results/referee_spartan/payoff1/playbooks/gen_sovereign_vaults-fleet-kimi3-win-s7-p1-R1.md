---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 1978
---
- Read the scoring before anything: deposited gold scores 1 point per unit, retained gold scores 2 points per unit. Never treat "maximize the deposit" as obviously correct — do the arithmetic first.
- When my private yield is 6 or more, I compare 2×yield (declare my true yield, deposit 0, retain everything) against 10 (declare 10, deposit 10). Retaining wins, so I declare my actual yield and deposit 0.
- When my private yield is 5 or less, declaring 10 and depositing 10 scores more than any truthful retain strategy — but only if deposits above yield don't trigger the audit penalty. I watch the round history: if anyone has already deposited above their yield without losing 10 points, the audit is a paper tiger and I declare 10, deposit 10 every remaining round.
- If the audit ever does fire against an over-deposit, I switch immediately to declaring exactly my yield and depositing 0, keeping the 2-points-per-unit retention.
- In phase order, I always decide declaration and deposit as a pair: the declaration is only a ceiling, so I set it equal to whatever amount I actually plan to put in, no higher — an inflated ceiling adds nothing if I'm not going to use it.
- I don't copy the opponent's line of play as a justification; a strategy that "worked" without penalty is evidence about the engine's rules, not about whether it's my best line. Score-wise, 10 points per round from max deposits is good, but 12–20 points per round from retaining strong yields is better, so I check that first before defaulting to the aggressive bluff.
- Track both scores each round; if I'm behind and retaining won't catch up, the safe bluff (declare 10, deposit 10) guarantees 10 and keeps pace, so I use it as the floor rather than getting cute with partial deposits.
- Never deposit a partial amount thinking it hedges — partial deposits only help if audit risk is real and correlated with deposit size; otherwise it's strictly dominated by either full retention or full deposit.