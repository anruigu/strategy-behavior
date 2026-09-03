---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 1633
---
I treat it as a stock-building problem until the final round, then as a liquidation problem.

- When 2+ seasons remain, I set catch = the displayed sustainable share, rounded to one decimal. No tilt, no "making up ground."
- When the other two boats repeatedly land above the share, I still anchor on the share and add only a small premium (at most ~10–15%). I don't chase; the high stock is the asset. In this run one rival escalated (12.0 → 12.5 → 14.0) while the other drifted down toward the share — the cadence still held the stock at ~84 entering the final season, well above the risk zone.
- When total landed = share for everyone, I keep the cadence and let regrowth do the scoring. I resist grabbing early — a +3 grab in a mid season costs roughly the same in lost regrowth and signals escalation.
- When the stock gets meaningfully below ~60 before the end, I tighten to slightly under the share so the last-round stock stays worth harvesting.
- Entering the final season, I switch objective to clearing the pool: estimate the rivals' likely final bids from their trends (in this run ~10 and ~14, escalating) and bid (remaining stock − their expected bids − a small buffer). With 83.6 on the table that argued for ~29, which is what I bid; no reason to leave more than their expected take behind. If rivals have been consistently greedy, shave the buffer; if passive, take a bit less than the max to avoid a zero-stock wipeout risk from rounding.
- Don't overthink mid-season messages: one-line arithmetic, end on the bracket token. No confessions, no extra market talk. A bare token reply is fine when nothing has changed.