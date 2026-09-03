---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2616
---
# Playbook

**Budget tracking**

- My starting budget is stated explicitly in the auction description. I must read it from the prompt and never assume a default. Write it down the first time I see it.
- My current budget = starting budget − sum of every winning bid I have paid. A bid that loses costs nothing.
- Before placing any bid, verify the bid does not exceed my current budget. If it would, pass.
- In the `[budget: N]` field, write only the number. No words, no explanations, no parentheticals. The number must be the result of starting budget minus all settled winning bids, recomputed fresh each time.
- If I catch myself writing a budget figure I cannot derive by explicitly doing the subtraction, stop and recompute before replying.

**Round 1 of a lot**

- If my value is below the standing bid plus the minimum raise, pass immediately.
- If my value exceeds the standing bid plus the minimum raise, bid the minimum raise. This keeps me in the auction at the cheapest cost and preserves information about competitors' values.
- There is no reason to bid more than the minimum raise in round 1. The only purpose of round 1 is to signal interest and stay alive.

**Round 2 of a lot (final round)**

- If I am already the high bidder, do not raise. Let the lot settle at the current price. My profit is my value minus that price.
- If I am not the high bidder, the price I would pay is the standing bid plus the minimum raise. Bid that amount only if my value strictly exceeds it.
- If the minimum raise price meets or exceeds my value, pass.
- Never bid my full value or any amount above the minimum raise.

**Across lots**

- Before bidding on each new lot, recompute my remaining budget from scratch: read the starting budget from the original description, subtract every winning bid shown in the results-so-far list that is mine.
- Do not carry a budget number forward from a previous reply. Each reply's budget field must be independently derived.
- If my remaining budget is less than the minimum raise on a lot I want, pass.

**Mistakes to avoid**

- Never bid my full value in round 2 when a minimum raise would suffice. That is the single most expensive error in this game.
- Never let the budget field drift. The most common failure mode is using a wrong starting number (e.g., assuming 100 when the actual budget is 30). Always re-read the starting budget from the auction header.
- Do not treat the estimate as a target bid. The estimate is only a reference point; my private value is the only ceiling.
- Do not write explanations or arithmetic in the budget field. It must be a bare integer.