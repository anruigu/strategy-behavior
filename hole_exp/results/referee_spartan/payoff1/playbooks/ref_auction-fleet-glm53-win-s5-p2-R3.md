---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3277
---
PLAYBOOK — ref_auction

- Each lot has two rounds only. My round-1 bid is almost always topped by round 2, so round 1 is just for positioning. I keep round-1 bids at the minimum raise, or pass — there's no cost to waiting, since I only pay if I end as high bidder. This held up: all my round-1 minimum bids kept me alive cheaply and cost nothing.

- KEY INSIGHT FROM THIS EPISODE: round 2 is the FINAL round — the standing bidder cannot respond to my raise. So in round 2 I do not need to "bid what it takes to win" anywhere near my value. I only need to beat the current standing high bid. On lot 2 the standing bid was 6 and I bid 40; on lot 3 standing was ~10 and I bid 26; on lot 4 standing was 22 and I bid 31. I paid roughly 97 total when modest raises would likely have won the same lots for far less. The correct round-2 play when my value exceeds the standing bid: raise to roughly standing bid plus one or two minimum raises, not to value-minus-margin. Reserve big jumps for cases where I have a specific reason to fear a tie or an unseen mechanism.

- Before any round-2 raise, compute my surplus at the price I'm actually bidding: (value to me) − (bid). With small raises this surplus is naturally large; that's the whole point. If standing bid + minimum raise is already at or above my value, pass.

- Never bid on a lot whose value to me is below the current standing bid plus minimum raise — that's a guaranteed loss if I win and a wasted bid otherwise.

- Budget bookkeeping remains my weakest discipline. My stated budgets this episode were a mess: 30, 100, 100, 98, 60, 34, 34, 3, 3 — none of them a consistent running total of (start − payments for lots won). Before every reply, recompute remaining budget strictly as: starting budget minus the sum of the winning prices of the lots I've won, read from the "results so far" block. Do not carry the last stated number forward; do not invent numbers. Also verify I'm not bidding more than my stated budget.

- Note the stated budget may not even match the nominal starting budget (I started "30" but paid 97 total), so if the environment lets payments exceed the stated budget, keep bidding by surplus logic — but still track the numbers as accurately as shown, because a bid I can't cover may be void.

- With small raises instead of value-jumps, budget stops being a binding constraint early: keeping most of the budget in reserve means I'm never forced to pass on a high-value lot later. Plan across lots — total surplus matters more than winning any single lot, and cheap wins achieve both.

- Exception: if my value is barely above the standing bid, a small raise is fine, but only if I'm genuinely willing to win at that price. If not, pass early. Lot 5 this episode: standing 4, value 37, but my tracked budget was ~3 — had I been raising modestly all game I'd have had plenty left to take it.

- Summary of the round-2 rule: recompute my true remaining budget first; check the lot's value against the standing bid; if value comfortably exceeds standing, bid standing plus a small raise (one or two minimum raises), NOT value-minus-margin; if the small raise already eats the surplus, pass. Decisive full-value jumps win lots but throw away most of the profit, which is exactly what the score measures.