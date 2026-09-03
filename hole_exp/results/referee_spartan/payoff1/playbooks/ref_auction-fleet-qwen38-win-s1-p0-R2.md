---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 1979
---
# Playbook

**Budget tracking is non-negotiable.** My starting budget is the number given at the top of the auction. Before every bid, I compute: remaining budget = starting budget minus the sum of final prices I have already paid for lots I won. I write that exact number in the `[budget:]` token. I do not guess, round, or carry over a stale number. If my proposed bid would exceed my remaining budget, I lower it to my remaining budget or pass.

**In round 1, open at the minimum raise to enter without overcommitting.** If there's no standing bid, open at the minimum raise. If there is a standing bid, raise by the minimum, provided the result is below my value. Round 1 is just to get into the auction; the real decision is round 2.

**In round 2, bid a meaningful fraction of my value, not just the minimum raise.** The minimum raise is too weak because other bidders can still outbid me after I act. Instead, I bid roughly 60–75% of my value for the lot (rounded to a valid increment above the standing high), unless the standing high is already near or above that target. This deters competitors who have moderate values while still leaving me positive surplus if I win. If the minimum raise itself already meets or exceeds 60–75% of my value, I bid the minimum raise.

**If the standing high bid is already at or above my value for the lot, I pass immediately.** No point in a losing bid.

**I never bid my full value.** My value is a ceiling. The goal is to win at the lowest price that is likely to deter competitors, which is usually 60–75% of my value in round 2.

**Before bidding, I check whether winning this lot would leave me too little budget for remaining lots I value highly.** If so, I may lower my round-2 target or pass entirely. I don't treat each lot in isolation.

**If I am the only bidder (no one else has raised), I can afford to bid closer to the minimum raise** since there's no one to deter. In that case, the minimum raise is sufficient to win.