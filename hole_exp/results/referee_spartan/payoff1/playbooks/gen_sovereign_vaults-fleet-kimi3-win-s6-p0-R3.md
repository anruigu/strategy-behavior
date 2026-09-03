---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 2240
---
When I declare, I declare whatever is safe; declaration only caps my deposit and is never checked against my yield, so I never declare below my deposit plan. Truthful declaration is simplest and fine. Overdeclaring carries no penalty, but gains nothing — I won't waste thought on signaling since deposits appear unconnected to any joint payoff.

When I deposit, I deposit 0. Retained gold scores 2 points per unit and deposits score only 1, and there is no audit checking my retained stash. Depositing my full yield was my biggest mistake — it halved my points every round I did it. Unless the rules say deposits unlock something (they don't here), the deposit phase is just a way to throw away 1 point per unit.

When trailing, I do not chase by depositing more; that loses more. I confirmed this over 5 rounds: my opponent deposited 0 every round too, just like me, and beat me purely because his yields were higher (9/7/8/7/5 vs my 1/6/8/4/5). My score is simply 2 × my total yield — I cannot fix yield variance with play, so I accept it and don't force moves that cost points.

When leading, I change nothing. There is no reason to deposit defensively or alter declarations; the optimal move is the same at every score standing.

When I make any move, I first recompute the exact scoring from the rules before acting: score = 2 × (yield − deposit) + 1 × deposit, minus penalties I can entirely avoid by keeping deposit ≤ declared. I optimize that formula directly instead of copying an opponent's pattern.

When I see an opponent depositing heavily or declaring 10 every round, I don't imitate or respond; their actions don't affect my score formula, so I ignore them and stick to deposit 0. If yields are ever revealed in the round history, I use them only to sanity-check my expectation of the final score, never to change my play.

If a future variant gives the treasury a payout, a threshold bonus, or a competitive edge (e.g., highest depositor wins a prize), I recompute before assuming deposit 0 is still optimal — the deposit-0 rule follows from the scoring formula, and I follow the formula, not the habit.

Any round, any score standing: declare truthfully (or any value ≥ my planned deposit of 0), deposit 0, keep everything.