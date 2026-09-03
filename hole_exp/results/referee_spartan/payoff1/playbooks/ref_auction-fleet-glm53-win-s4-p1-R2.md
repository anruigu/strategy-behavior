---
game: ref_auction
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2156
---
**Playbook for ref_auction**

- When I have the high value for a lot (value well above estimate), I open at the minimum raise rather than a small increment above the standing bid — the minimum raise keeps more room and doesn't signal strength.
- In round 2, I bid up to just under my true value, but I stop there. If the standing bid is already near or above my value, I pass immediately — winning at my value or above earns nothing or loses money.
- When a lot is worth less than its estimate to me, I do not open it. Opening at minimum "for cheap upside" is bad: opponents reliably overbid me in round 2, and I either lose the lot anyway or get tempted into bidding past my value. I only bid when the standing bid is meaningfully below my value — if an opponent opens cheap in round 1, I pass and re-evaluate in round 2 before committing.
- I never bid above my value to "protect" an earlier bid — sunk bids are sunk; each lot is judged fresh.
- I keep a strict cap per lot: never let my bid exceed my value for that lot minus a small margin, so every win has positive expected surplus. Last episode my minimum-raise bids consistently converted into wins well under value (15 for a 35-value lot, 18 for a 23-value lot) — minimal round-1 bids plus one disciplined round-2 raise is enough to win contested lots cheaply.
- I state the budget accurately every single time. Track it as: initial budget minus the sum of my winning bids so far (bids I lost cost nothing). Last episode my budget numbers drifted wildly (24 → 100 → 85 → 67) because I wasn't recomputing from a single source of truth. Before replying, recompute budget from scratch: budget = 30 − total paid for lots already won.
- Round 1 bids should be minimal (minimum raise); real contest happens in round 2. Overbidding in round 1 just costs money if I win, and doesn't deter anyone.
- Two rounds means at most one opponent counter over my round-1 raise, so a single modest round-2 raise to just below value usually ends the contest in my favor. Don't jump far past the standing bid — I only need to be highest at the close, and every extra token above the minimum raise is profit given away.