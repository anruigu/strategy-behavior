---
game: gen_sovereign_vaults
model: gpt-mini
condition: neutral
seed: 2
round: 1
chars: 1608
---
When asked to declare, default to declaring my true private yield.

When I want to signal cooperation early, declare truthfully and deposit about half my yield (round down), unless I see the other player reciprocating.

When the other player contributes zero or consistently far less than me, stop giving away value: deposit 0 in subsequent rounds.

When the other player contributes positive and close to my contribution, match their average deposit to sustain cooperation (mirror last round or average of past contributions).

When I am trailing by a large margin with only one round left, prioritize high-value retained gold: declare truthfully and deposit as little as possible (0–1) to maximize the 2-point retained payoff.

Never plan a deposit that exceeds my declared number—do not underdeclare if I intend to deposit more, because audit failure costs −10 and zero round score.

Do not habitually overdeclare to “bluff” for reputational reasons; it didn’t produce extra score and makes no mechanical advantage (audits only check deposit ≤ declared), so only overdeclare if I specifically want to enable a larger (safe) deposit and I’m prepared to actually deposit up to that level.

If I see evidence the opponent is cooperating (nonzero deposits across rounds), increase my deposit generosity gradually (not all-in) to build mutual gains.

Conserve resources when mutual cooperation is absent: keep more private (retain) because retained gold scores 2 points each and is often superior to unreciprocated deposits.

Always ensure deposits are integers and within my declared amount before submitting.