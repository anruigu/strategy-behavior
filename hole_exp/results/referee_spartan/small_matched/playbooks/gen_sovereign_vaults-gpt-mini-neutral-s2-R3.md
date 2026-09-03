---
game: gen_sovereign_vaults
model: gpt-mini
condition: neutral
seed: 2
round: 3
chars: 2599
---
I declare my true private yield by default; I do not overdeclare unless I intend to deposit up to that amount and audit safety is assured.

On round 1 I may signal cooperative intent by depositing about half my declared yield (floor(yield/2)) to offer a clear, modest, non‑all‑in signal.

I treat cooperation as tentative: give at most two cooperative signals (round‑1 and round‑2 deposits of ~half) without reciprocity. If the opponent contributes 0 in both of the first two rounds, I stop giving away value and deposit 0 for all subsequent rounds (while continuing to declare truthfully).

If the opponent contributes 0 in the first round but gives a positive deposit in round two, I continue to signal cooperation by keeping deposits near half my declared yield but move toward matching their level thereafter.

If the opponent contributes any positive amount(s) across rounds, I escalate generosity slowly and cautiously: aim to mirror their recent level (match last round) or move toward the running average of their deposits rather than overshooting. If their deposit < my prior deposit, reduce mine toward their level; if their deposit > my prior deposit, consider increasing mine but not above the running average plus one.

When behind by a substantial margin with only one round left, prioritize retained gold (2 points per retained unit) over deposited gold: declare truthfully and deposit minimally (0, or at most 1 if there is a narrow strategic reason).

Always ensure deposit ≤ declared yield and deposit is an integer. Avoid risky moves that could trigger audit loss (never overdeclarate in a way that tempts an audit unless I can safely back it up).

Conserve resources when mutual cooperation is absent: favor retained gold over unreciprocated deposits, because unilateral deposits yield 1 point per unit while retained yield gives 2 points per unit.

In ambiguous mixed‑signal situations, default to cooperation early but use a short memory: at most two unilateral cooperative rounds before switching to conservative deposits (0). If the opponent begins to reciprocate later, resume gradual matching rather than immediate large increases.

If I observe consistent small reciprocation (positive but much smaller than my deposits), downscale my deposits to the reciprocation level rather than trying to “teach” cooperation by sacrificing further.

Keep all decisions simple and interpretable: truthful declarations, modest half‑yield signal early, two‑round patience for reciprocity, then freeze to 0 if reciprocity does not materialize, otherwise gradually match opponent deposits.