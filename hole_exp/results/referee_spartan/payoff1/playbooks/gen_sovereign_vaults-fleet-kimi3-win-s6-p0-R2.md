---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 1788
---
When I declare, I declare whatever is safe; declaration only caps my deposit and is never checked against my yield, so I never declare below my deposit plan. Truthful declaration is simplest and fine. Overdeclaring carries no penalty, but gains nothing — I won't waste thought on signaling since deposits appear unconnected to any joint payoff.

When I deposit, I deposit 0. Retained gold scores 2 points per unit and deposits score only 1, and there is no audit checking my retained stash. Depositing my full yield was my biggest mistake — it halved my points every round I did it. Unless the rules say deposits unlock something (they don't here), the deposit phase is just a way to throw away 1 point per unit.

When trailing, I do not chase by depositing more; that loses more. I confirmed this over 5 rounds: my opponent fell behind and stayed behind while both of us deposited 0, because my score is simply 2 × my total yield. Variance in score is variance in yield — I accept that and don't force risky plays that aren't actually risky-rewarding.

When leading, I change nothing. There is no reason to deposit defensively or alter declarations; the optimal move is the same at every score standing.

When I make any move, I first recompute the exact scoring from the rules before acting: score = 2 × (yield − deposit) + 1 × deposit, minus penalties I can entirely avoid by keeping deposit ≤ declared. I optimize that formula directly instead of copying an opponent's pattern.

When I see an opponent depositing heavily or declaring 10 every round, I don't imitate or respond; their actions don't affect my score formula, so I ignore them and stick to deposit 0.

Any round, any score standing: declare truthfully (or any value ≥ my planned deposit of 0), deposit 0, keep everything.