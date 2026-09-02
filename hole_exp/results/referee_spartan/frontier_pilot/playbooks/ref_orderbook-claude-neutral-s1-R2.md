---
game: ref_orderbook
model: claude
condition: neutral
seed: 1
round: 2
chars: 928
---
## My playbook for ref_orderbook (buy-side delivery obligation)

**What the scoreboard actually rewards**
- Score = final cash + (units held × settlement value) − starting cash − 8 × (units short at the bell).
- Every unit I buy below settlement value adds (value − price) to my score. That's the entire game. The delivery requirement isn't a tax; it's the reason I'm allowed to buy at all.
- Observed across four runs: settlement value ≈ **opening mid + 8** (mids of 49.5–50 settled at 57–58). Opening asks were 51–53, i.e. 5–7 points below true value. The opening ask is free money.
- Prices ratchet up ~2–3 per tick through ticks 1–3, then plateau within ~±1 of true value from tick 3 onward. Nothing cheap ever comes back.
- Realistic scores are +9 to +15, and the single biggest driver is how low the opening ask is — something I don't control. So: capture the cheap opening depth, then don't give any of it back.

**Mechan