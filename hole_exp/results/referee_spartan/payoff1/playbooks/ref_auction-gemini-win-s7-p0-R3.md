---
game: ref_auction
model: gemini
condition: win
seed: 7
round: 3
chars: 1456
---
When the game begins, I find my exact starting budget in the very first prompt (Lot 1, round 1). Because early prompts may be truncated in later rounds, I cannot rely on looking back at the first prompt. Instead, I must explicitly state my true starting budget and current remaining budget in the text of every single reply.

To calculate my current remaining budget, I look at my most recent reply's reasoning or `[budget: N]` token to find my previous budget, and subtract the exact prices of any lots I have won since then (found in the "Results so far" section). I must never assume a default starting budget like 100.

When I submit my decision, I strictly report this calculated remaining budget in the `[budget: N]` token.

When I evaluate a lot, I determine my absolute maximum bid, which is the lower of my true remaining budget and the lot's value to me. I must never bid more than my current remaining budget.

When the standing high bid plus the minimum raise exceeds my maximum bid, I output `[bid: pass]`.

When I am in round 1 for a lot I want, I bid the minimum required raise to take the lead without inflating the price too early.

When I am in round 2 (the final round) for a lot I want, I bid strongly and closer to my maximum bid rather than just making the minimum raise. Making only minimum raises in the final round does not work, as it leaves me vulnerable to being outbid by players acting after me with no opportunity to counter.