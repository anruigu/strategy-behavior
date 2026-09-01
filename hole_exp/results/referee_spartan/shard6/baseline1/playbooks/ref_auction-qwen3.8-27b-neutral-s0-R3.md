---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 3045
---
# Playbook

**Budget: 30.** This is stated in the rules at the top of each episode. I track it from the start: remaining = 30 minus the sum of all lots I have won so far. I report this number every time. I do not guess, do not say "unknown," do not assume 100.

**Core principle: In round 2, bid to win the lot when my value is well above the standing high bid, not just to stay in.**

My old rule of "always bid the minimum raise in round 2" was too passive. It meant I systematically lost lots where my value was high but the competition bid a bit above the minimum. Since round 2 is final, a higher bid costs me nothing if I still lose, and captures real surplus if I win.

**Round 1:**
- If the current high bid (plus minimum raise) is below my value, bid the minimum raise. I am staying in cheaply, not trying to win yet.
- If the current high bid plus minimum raise is at or above my value, pass. No positive surplus is possible.
- Never open high. No benefit to signaling in round 1.

**Round 2 (final round):**
- If I am the current high bidder: pass. My standing bid is already in place; raising only increases what I pay.
- If I am not the current high bidder:
  - Compute the minimum raise bid: standing_high + min_raise.
  - If minimum raise bid ≥ my value: pass. No positive surplus.
  - If minimum raise bid < my value: bid the midpoint between the minimum raise bid and my value. That is: bid = minimum_raise_bid + (my_value − minimum_raise_bid) / 2.
    - This is higher than the minimum raise, so I am more likely to win.
    - If I win, I still capture meaningful surplus (roughly half the gap between the minimum and my value).
    - If I lose, I lose nothing (same as bidding the minimum).
  - Cap my bid at my remaining budget. If the midpoint exceeds my remaining budget, bid my remaining budget (or pass if even the minimum raise exceeds it).

**Budget management:**
- Starting budget is 30. I subtract the winning price of each lot I win.
- Before bidding in round 2, I check: can I afford the bid? If my remaining budget is less than the minimum raise, I pass.
- As my budget depletes, I become more selective. With 10 left and 3 lots remaining, I only bid on lots where my value is very high (≥ 25 or so) so that even a modest win gives positive surplus.
- I do not spread my budget thin across many lots. Two well-chosen wins at good surplus beat three thin-margin wins.

**Pass rule:**
- If minimum raise bid ≥ my value, pass.
- If my remaining budget < minimum raise bid, pass.
- Zero or negative expected surplus is never worth bidding.

**What I will not do:**
- I will not bid "unknown" or a non-numeric budget. I compute 30 minus my wins every time.
- I will not bid the bare minimum raise in round 2 when my value is well above the standing bid. That leaves surplus on the table and lets opponents pick off lots I actually want.
- I will not bid my full value. The midpoint rule keeps me at a comfortable surplus if I win.
- I will not overspend my 30 budget across lots. I track it and cap my bids accordingly.