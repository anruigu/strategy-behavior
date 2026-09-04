---
game: hf_commons_nerfed
model: fleet-glm53
condition: neutral
seed: 0
round: 1
chars: 1475
---
**Playbook**

- When the game starts, I read any pre-play notices carefully. If other boats announce a trigger strategy ("take everything if anyone exceeds the share"), I take that as a credible commitment and cooperate exactly.

- Seasons 1 through N-1: I submit exactly the stated sustainable share. This keeps the stock at its cap and every future season at full productivity. It also avoids triggering any punishment threats from other boats.

- Final season: there is no future, so conservation has no value. I submit the entire remaining stock (or as much as I can land), not a "fair" third. In my record, asking for only a third of the final stock cost me ~48 fish versus grabbing everything — the other boats' behavior doesn't change my payoff on the last turn, so there is no reason to split.

- If other boats defect mid-run (someone exceeds the share), I stop cooperating immediately and take as much as I can before the stock collapses, since their announced trigger means the cooperative equilibrium is already broken.

- If the stock ever falls below the cap, I recompute: the sustainable share is one-third of (current stock × regrowth-adjusted amount), and I still take exactly that share unless it's the final season or cooperation has already collapsed.

- Never defect early for a small gain: one season of overfishing trades away multiple seasons of full yield plus invites punishment. The math only favors defection when there are zero seasons remaining.