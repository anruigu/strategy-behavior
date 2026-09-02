---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 3752
---
# Playbook

**Budget tracking.** At the start of the auction my budget is 30. Every time I win a lot, I subtract the price I paid from my remaining budget. I must report this number accurately on every bid. If my remaining budget is less than the minimum raise, I cannot bid and must pass.

**Budget allocation across lots is the most important constraint.** With 30 budget and 5 lots, I must treat each lot as a fraction of my total resources. I should aim to spend no more than 40% of my remaining budget on any single lot (i.e., no more than 12 early on, less as budget shrinks). In episodes 2 and 4 I spent 28–30 on one lot and had nothing left for three or four more lots where I had positive value. That capped my score at +21 to +30. The goal is to win multiple lots at modest prices, not one lot at a high price.

**Round 1: open low — at the minimum raise or slightly above.** My previous rule of "open at 50–70% of value" was too aggressive and burned budget. Opening at the minimum raise (or 1–2 increments above it) accomplishes the same goal of entering the auction while preserving budget for R2 and for later lots. In my best episode (+77), I opened at 15 on a lot worth 28 (54% of value) and at 8 on a lot worth 56 (14% of value) — the low opening on the high-value lot is what let me win it cheaply. I should default to the minimum raise in R1 unless I have a very large surplus AND plenty of budget remaining.

**Round 2: do NOT assume that passing as the high bidder locks in the win.** In multiple episodes I passed in R2 while being the standing high bidder, and another bidder raised after me and took the lot. Passing in R2 means I am willing to lose. If I want to win the lot, I must bid in R2 at a price that makes it unattractive for others to raise. The question in R2 is: "What is the maximum I should bid such that (a) it's below my value, (b) it's within my remaining budget, and (c) it's high enough that I'm comfortable paying it?" I bid that amount. If no such amount exists (i.e., the minimum raise already exceeds my value or budget), I pass.

**Round 2: if I am NOT the high bidder, bid the minimum raise only if it is comfortably below my value AND I have budget to spare.** "Comfortably" means at least 30% below my value. If the minimum raise leaves me with less than 30% surplus, I pass — the lot is not worth the budget risk given I may need funds for later lots.

**Prioritize lots where my value far exceeds the estimate, but cap my bid by budget, not by value.** A lot worth 56 to me with an estimate of 39 is my top priority, but if my remaining budget is 14, I should not bid 14 in R1 hoping to deter. I should bid the minimum in R1, see what happens, and in R2 bid a price that balances deterrence against preserving budget for remaining lots.

**Pass early and often when the current bid already exceeds my value or when my surplus is thin relative to my remaining budget needs.** If the standing high bid is at or above my value, I pass immediately. If my surplus on this lot is small (value within 10% of estimate) and I have lots remaining where I might have a bigger edge, I pass to conserve.

**Do not let a single lost lot change my aggression on the next one.** Each lot is independent. I evaluate each one on its own value-versus-bid-versus-budget math.

**In R1, if someone has already bid and the minimum raise would put me at or above my value, I pass.** I do not enter a lot in R1 if the resulting price leaves me with zero or negative surplus.

**When I have very little budget remaining (less than 2× the minimum raise), I only bid on lots where my value is at least 3× the minimum raise.** Otherwise the risk of losing the lot after spending my last funds is too high relative to the gain.