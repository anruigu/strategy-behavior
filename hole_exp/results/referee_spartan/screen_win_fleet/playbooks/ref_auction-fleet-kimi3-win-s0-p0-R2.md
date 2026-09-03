---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 1989
---
I always report my true remaining budget in the [budget:] token — my actual budget minus what I've committed — never a fabricated number. My effective ceiling on any lot is min(my value, my remaining budget). I never bid above it, and I pass immediately when the minimum raise exceeds it (my pass on lot 2 when the raise exceeded value was correct; never fight for negative surplus).

In round 1 of a lot, I open with the minimum raise if it's below my ceiling — cheap information, no commitment. This worked on every lot this episode.

In round 2 (the final round), the minimum raise is a losing habit: there is no next round to correct. On the final round, if the lot is worth meaningfully more than the standing bid, I bid at or near my ceiling — enough to shut out the rival who has been contesting me. This won me lots 3, 4, and 5; my one loss (lot 1) came from bidding 24 against my value of 26 instead of closing at full value. Final-round bids go to my ceiling, not a feel-good number short of it.

I track which rival keeps contesting and what they've spent. Bidder 2 had spent 60 by lot 4, so a near-ceiling close shut them out. A heavily-spent rival late in the auction is beatable; a fresh one is not. But don't over-project from assumed budgets — verify against the results ledger shown.

Bidding exactly at my value buys zero surplus. When I choose to bid near ceiling, I go to my value (or budget ceiling if lower), accepting zero-margin wins only when winning beats losing; when there's room, I prefer one strong bid that wins, not a ladder of raises.

I reserve budget across lots: I don't spend everything early unless that lot is clearly the best surplus available, because later lots may offer more. Winning cheap lots early can drain the firepower I'd want for a high-surplus lot at the end.

I keep my arithmetic simple and explicit before replying: value, budget left, ceiling, minimum raise, then choose pass / minimal open (round 1) / near-ceiling close (round 2).