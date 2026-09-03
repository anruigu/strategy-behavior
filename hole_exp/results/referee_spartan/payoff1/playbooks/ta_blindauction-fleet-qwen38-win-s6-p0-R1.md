---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 1554
---
**Playbook**

When I learn my value for a lot, I never bid it. I estimate what the opponent is likely to bid based on their visible history, then bid just above that estimate, leaving as much surplus as possible.

When the opponent's bids so far cluster in a narrow range (e.g. 2–4), I cap my bids at the top of that range plus one, regardless of how high my own value is. A value of 10 against a 4-bidding opponent means I bid 5, not 10.

When my value is low (2 or 3), I bid at or just below value. If I can't profit, I don't bid at all.

When the opponent's recent bids are unknown or erratic, I shade to roughly 60–70% of my value as a starting point.

When a collusive split is proposed and the math checks out (each side takes lots where it has high value, pays a token price, and the other side passes), I accept and then execute it exactly: bid 0 on lots assigned to the opponent, bid the agreed token price on lots assigned to me. I do not deviate, do not bid my value, do not "compete" on a lot I agreed to pass.

When I am on a lot assigned to me under an agreement, I bid the minimum that beats the opponent's expected pass (the token price), not my value.

When a lot ties and goes unsold, I note that I was the one who could have bid one coin higher to take it. On the next similar lot, I bid one coin higher than the last observed opponent bid, not at my value.

I treat my score line as a running check: if my net surplus per won lot is shrinking or flat across successive lots, I am overpaying and I need to shade harder on the next bid.