---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 845
---
**Playbook**

**Opening a lot (no standing bid, round 1):**
- If my value is ≥ 35 (high-value lot): bid a moderate amount — roughly the minimum raise plus a small buffer (not 50% of value). The goal is to signal interest and establish a floor, not to lock in a price. Others will respond, so an aggressive early bid just gives them a reference point to top.
- If my value is < 35 (low/moderate-value lot): bid the minimum raise only. I'm testing the field cheaply. If no one responds, I can raise in round 2 at a lower total cost. If someone does respond, I reassess.
- If my value minus the minimum bid is less than 3: pass immediately. The margin is too thin to justify the risk.

**Round 2 (final round) — I am the high bidder:**
- Pass. Do not raise my own bid. I lock in the price at the current level.

**Round 2 — I am NOT the high bidder