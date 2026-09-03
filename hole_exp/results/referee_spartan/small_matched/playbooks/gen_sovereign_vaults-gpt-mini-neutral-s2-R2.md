---
game: gen_sovereign_vaults
model: gpt-mini
condition: neutral
seed: 2
round: 2
chars: 2107
---
I declare my true private yield by default.

When I want to signal cooperation, I declare truthfully and deposit about half my yield (round down) on the first round to offer a clear, non‑all‑in cooperative signal.

If the opponent contributes zero in both of the first two rounds, I stop giving away value and deposit 0 in all subsequent rounds (declare truthfully but deposit 0), because continued unilateral deposits rarely pay off.

If the opponent contributes zero in just the first round but then gives a positive deposit in round two, I continue to signal cooperation (keep depositing ~half) and move toward matching their contributions.

When the opponent contributes positive amounts across rounds, I escalate my generosity gradually: match their recent level (mirror last round) or match the running average of their deposits to sustain cooperation without overcommitting.

When I am clearly trailing by a large margin with only one round left, prioritize retained gold: declare truthfully and deposit as little as possible (0–1) to maximize 2 points per retained unit.

Never plan a deposit that exceeds my declared number—always ensure deposit ≤ declared before submitting.

Do not habitually overdeclare to bluff; overdeclaring has no benefit unless I intend to actually deposit the larger amount and exposing a higher declared cap is safe. Prefer truthful declarations because audits only require deposit ≤ declared and honesty preserves audit safety.

Conserve resources when mutual cooperation is absent: favor retained gold (2 points per unit) over unreciprocated deposits (1 point per unit).

If the opponent contributes positive but significantly less than me, reduce my deposit towards matching their level rather than increasing mine; avoid chasing reciprocity by over‑depositing.

Keep deposits integer and within declared harvest; avoid risky moves that could trigger audit loss (−10 points).

In ambiguous cases (mixed signals), default to cooperation early but use a short memory: give at most two cooperative rounds without reciprocity before switching to conservative deposits (0).