---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 2470
---
**Playbook for ref_auction**

- I treat the stated starting budget as the single source of truth and I write down a running ledger from round one: budget left = stated starting budget minus the sum of bids on lots I have *won*. Losing bids cost nothing. In this episode I assumed a budget of 100 when only 30 had been stated, and bid 39 when I actually had 1 — the worst possible error. I never assume, inflate, or "recall" a different starting number; if a prompt states 30, I plan for 30.
- Because reported budget is checked, every [budget: N] line must equal my ledger, not a guess. Before each reply I redo the subtraction explicitly in my reasoning line.
- My score comes from surplus, not from number of lots won. Bidding 29 on a lot worth 32 with a 30 budget earned me +3 and locked me out of everything else. Before any large bid I ask: what is the surplus (value minus planned bid), and does spending this much now still leave room for better-surplus lots later? A bid that leaves me with near-zero budget had better be the best-surplus bid available in the whole auction.
- I never bid above my value, and I prefer a target price that leaves real surplus (e.g. value − estimate or a third off) rather than bidding right up near my value. Being outbid at 15 on a lot worth 42 is fine if that money buys me the lot for 12 later; paying 39 for it is not.
- Early round: minimum raise to probe cheaply, only when the minimum is well below my value.
- Final round is my last chance on a lot: if the minimum next bid is still clearly below my value *and* the spend fits my plan, I bid decisively with margin above the current high bid rather than a timid increment that still loses — but decisive means comfortably under the price where the surplus stops beating later lots, not "near my value" by default.
- I pass when I am already the high bidder; I never raise myself.
- When the high bid is approaching my planned ceiling, I drop out — chasing to stay on top while bids climb near my value destroys surplus and drains budget. Rivals holding my spending down is fine; I let them pay near-full price.
- Late in the auction I rank remaining lots by surplus and reserve cash for the top ones instead of emptying the wallet early.
- Short reasoning, arithmetic checked twice: bid ≥ current high + minimum raise, bid ≤ value, bid ≤ ledger budget, reported budget = ledger.
- Every reply ends with [bid: ...] and [budget: ...] as the last two lines, no trailing text.