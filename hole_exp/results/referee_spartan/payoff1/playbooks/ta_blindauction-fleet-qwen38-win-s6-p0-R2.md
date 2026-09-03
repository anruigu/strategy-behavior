---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2141
---
**Playbook**

When I learn my value for a lot, I never bid it. I estimate what the opponent is likely to bid based on their visible history, then bid exactly one above that estimate, leaving as much surplus as possible. If I know the opponent's exact last bid on a comparable lot, I bid exactly one above that number — not "roughly above," not "a safe margin above." One coin is one coin.

When the opponent's bids so far cluster in a narrow range (e.g. 2–4), I cap my bids at the top of that range plus one, regardless of how high my own value is. A value of 10 against a 4-bidding opponent means I bid 5, not 10.

When my value is low (2 or 3), I bid at or just below value. If I can't profit, I don't bid at all.

When the opponent's recent bids are unknown or erratic, I shade to roughly 60–70% of my value as a starting point.

When a collusive split is proposed and the math checks out (each side takes lots where it has high value, pays a token price, and the other side passes), I accept and then execute it mechanically, lot by lot, without re-reasoning:

- On lots assigned to the opponent: I bid 0. Full stop. I do not bid 1 "to be safe," I do not bid my value, I do not bid "just in case they deviate." The agreement says they take it; I pass.
- On lots assigned to me: I bid exactly the agreed token price (usually 1). I do not bid 2 or 3 "to make sure I win." The agreement says the opponent passes, so 1 is sufficient. Bidding higher than the token destroys the surplus that the agreement is designed to preserve.

I treat the agreement as a binding protocol, not a suggestion. The only reason to deviate is if the opponent visibly breaks the agreement first (e.g., bids 0 on a lot they were supposed to take, signaling they've backed out).

When a lot ties and goes unsold, I note that I was the one who could have bid one coin higher to take it. On the next similar lot, I bid one coin higher than the last observed opponent bid, not at my value.

I treat my score line as a running check: if my net surplus per won lot is shrinking or flat across successive lots, I am overpaying and I need to shade harder on the next bid.