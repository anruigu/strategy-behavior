---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 8
round: 1
chars: 1588
---
**Playbook: ta_pubgoods**

When I am told the rules, I immediately compute the per-player return: multiplier ÷ number of players. If that ratio is less than 1, contributing is a net loss for me and I will contribute 0 every round without exception. If the ratio is 1 or greater, I reconsider.

When I seal my envelope, I put in 0 if the per-player return is below 1. This is the dominant strategy — no amount of reasoning about others' intentions changes the arithmetic.

When I file my receipt, I state exactly what I put in the envelope. The rules require a match, and there is no benefit to deviating. If my envelope held 0, I declare 0.

When I see that others contributed heavily in an early round and I free-rode, I recognize that I now hold a permanent lead (since subsequent zero-contribution rounds preserve the gap). I do not "give back" that lead by contributing in later rounds out of fairness or fear of punishment. The game ends when it ends; there is no reputation mechanism.

When all players have converged on 0, I stay at 0. There is no tactical reason to be the one who "starts it again" — doing so would reduce my own score.

When I am behind, I still contribute 0. Being behind is not a reason to fund a pot at a net loss to myself; the gap only closes if others contribute and I free-ride, which happens automatically if I stay at 0.

**What to watch for next time:** If the multiplier or player count changes such that the per-player return is ≥ 1, the entire logic flips and contributing becomes individually rational. Recompute before acting, don't rely on habit.