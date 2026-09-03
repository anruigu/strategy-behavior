---
game: ref_auction
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1369
---
**Playbook for ref_auction**

- When I have the high value for a lot (value well above estimate), I open at the minimum raise rather than a small increment above the standing bid — the minimum raise keeps more room and doesn't signal strength.
- In round 2, I bid up to just under my true value, but I stop there. If the standing bid is already near or above my value, I pass immediately — winning at my value or above earns nothing or loses money.
- When a lot is worth less than its estimate to me, I do not open it. Opening at minimum "for cheap upside" is bad: opponents reliably overbid me in round 2, and I either lose the lot anyway or get tempted into bidding past my value. I only bid when the standing bid is meaningfully below my value.
- I never bid above my value to "protect" an earlier bid — sunk bids are sunk; each lot is judged fresh.
- I keep a strict cap per lot: never let my bid exceed my value for that lot minus a small margin, so every win has positive expected surplus.
- I state the budget accurately each time and track that total committed bids across lots don't exhaust my budget before high-value lots appear — budget discipline matters more than winning any single marginal lot.
- Round 1 bids should be minimal (minimum raise); real contest happens in round 2. Overbidding in round 1 just costs money if I win, and doesn't deter anyone.