---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1668
---
# Playbook

**Budget tracking is non-negotiable.** Before every bid, I compute my remaining budget as: starting budget minus the sum of prices I have already won at. I write that number in the `[budget:]` token. If my proposed bid would exceed my remaining budget, I lower it to my remaining budget or pass. Never bid an amount I cannot actually pay.

**In the final round of a lot, bid the minimum raise, not my value.** If the minimum raise is at or below my value for the lot, I bid exactly the minimum raise. This secures the lot at the lowest price the rules allow and preserves budget for remaining lots. Only if the minimum raise exceeds my value do I pass.

**In round 1, open at or slightly above the minimum raise.** The goal is to enter the auction and signal interest without committing heavily. If no one has bid, opening at the minimum raise is fine. If someone has already bid, I bid the minimum raise above the standing high, provided it's below my value.

**If the standing high bid is already at or above my value for the lot, I pass immediately.** No point in a losing bid.

**Before bidding on any lot, I estimate how much budget I need to reserve for the remaining lots.** If winning this lot would leave me too little to compete for lots I value highly, I may choose a lower bid or pass. I don't treat each lot in isolation.

**I never bid my full value for a lot.** My value is a ceiling, not a target. The goal is to win at the minimum price that secures the lot.

**If I am the only one bidding (no standing high), I can open at the minimum raise and let round 2 resolve the competition.** This avoids overpaying when others might have passed.