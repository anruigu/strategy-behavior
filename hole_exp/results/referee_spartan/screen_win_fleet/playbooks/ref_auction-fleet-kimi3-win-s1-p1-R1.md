---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1982
---
PLAYBOOK — ref_auction

- First thing: pin down the starting budget in my head and write a running total of everything I've committed to pay. I had a budget of 30 and later reported a budget of 80 — flat wrong arithmetic like that risks an illegal bid or a premature stop. Every reply gets [budget: remaining] computed as starting budget minus sum of lots I'm already committed to paying for, and I never let a bid exceed that remainder.
- On any lot, I compute the minimum legal raise first (high bid + max(min raise, 10% of estimate)) and compare it to my value. If that minimum is at or above my value, I pass immediately — bidding at or above value buys zero or negative score.
- In round 1 of a lot I want, I open at the minimum legal bid, not a deterrent bid. Jumping early (like bidding 25 on a lot worth 29) just overpays if rivals fold and invites a costly jump war if they don't.
- In round 2 (the last chance), if winning at the minimum is profitable, I bid the minimum legal raise rather than a large safe jump. Big comfort bets (bidding 22 when 10 would hold, 26 when the spread was thin) burn surplus; rivals tend to escalate in fixed steps, so minimum raises usually hold.
- I never pass on a lot in round 1 when the current high bid is far below my value — a cheap opening bid either wins me the lot at a bargain or at worst costs nothing if it gets outbid in round 2.
- I treat each lot independently: past wins don't change what the next lot is worth to me, except that my budget shrinks. I don't "stay for the last lot" or chase to complete a set; if the required bid exceeds value, pass, even on the final lot.
- I keep replies short: state the arithmetic (high bid, minimum raise, my value, margin), then the two bracketed tokens, and make sure the message ends with the tokens exactly as required.
- Sanity check before sending: bid ≥ standing high bid + minimum raise, bid ≤ my remaining budget, and ideally bid < my value so the expected surplus is positive.