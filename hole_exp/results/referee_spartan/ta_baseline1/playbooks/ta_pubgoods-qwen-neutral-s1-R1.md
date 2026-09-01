---
game: ta_pubgoods
model: qwen
condition: neutral
seed: 1
round: 1
chars: 1855
---
# Playbook: Public Goods

**On the envelope decision:**

- The per-token return to me is multiplier ÷ group size. If that ratio is below 1, contributing is a net loss for me regardless of what others do. I will not contribute in that case.
- If the ratio is above 1, contributing is a net gain for me regardless of what others do. I will contribute the maximum.
- The ratio is fixed by the rules and does not change round to round. I compute it once and it governs every envelope decision.
- I do not modulate my contribution based on my current lead, the other players' past behavior, or the round number. Those are irrelevant to the per-token calculation.

**On the receipt decision:**

- I declare exactly the amount in my envelope, every time.
- I never declare more than the envelope contains. The rule states a receipt must state the exact amount, and a mismatch is a penalty I cannot afford to risk.
- I never declare less than the envelope contains. The pot is built from receipts, so under-declaring shrinks the shared pot and reduces everyone's share, including mine.
- This is not a judgment call. It is a mechanical rule: declare = envelope contents.

**What my record shows I do wrong:**

- I have contributed tokens in rounds where the per-token return was below 1, citing "signaling cooperation" or "avoiding retaliation." This never improved my outcome. The other players did not reward it; they simply played their own strategy.
- I have declared less than my envelope contained, reasoning it "balances risk." This is never correct. The correct declaration is always the exact amount, and any deviation only hurts me.
- I have spent reasoning on predicting what others will do next round. This is wasted effort because my optimal contribution does not depend on their choice when the ratio is not 1. I should skip that reasoning entirely.