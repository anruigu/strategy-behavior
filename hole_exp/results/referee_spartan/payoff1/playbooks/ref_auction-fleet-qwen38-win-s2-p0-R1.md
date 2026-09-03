---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2392
---
# Playbook: ref_auction

**Budget tracking.** At every decision, my budget is my starting budget minus the total I paid for all lots already won. I must track this precisely and never let a bid exceed what I can actually afford.

**Prioritization across lots.** Before each lot, I compare my value for that lot against my remaining budget and the number of lots still to come. I don't need to win every lot. I commit budget to lots where my value is high relative to the expected clearing price, and I'm willing to pass on lots where the expected profit is thin.

**Round 1 (a round 2 will follow).**

- If no one has bid and the lot is worth a lot to me, I open at roughly 50–60% of my value. This puts me in the auction without committing my full margin.
- If someone has already bid, I raise to a level that is competitive but still well below my value (aim for the current bid plus a few minimum-raise increments, not a large jump). I want to signal presence and see if opponents escalate.
- If my value is only barely above the current bid, I pass now and save my budget for later lots.

**Round 2 (final round — the round I keep getting wrong).**

- I do not bid the minimum raise to win. In this episode I bid the minimum on two lots and lost both because opponents raised again. The minimum raise invites a counter.
- If I want the lot, I bid at 85–95% of my value. This is the bid that is hard to outbid without the opponent also paying close to their own value.
- I only bid the minimum raise in the final round when my value is within one minimum-raise of the current bid, because the profit is so thin that the risk of a counter isn't worth taking.
- I do not bid a "moderate" amount like 70% of my value in the final round. That is the worst of both worlds: high enough to signal interest, low enough to get outbid. I either commit near my value or I pass.

**When to pass in the final round.**

- If the current bid is at or above my value, I pass.
- If my remaining profit at my value (value minus current bid) is less than one minimum-raise and I have other lots ahead that I value more, I pass.

**Opening bids in a fresh lot (no standing bid).**

- I open low enough to preserve margin for a potential round-2 raise, but not so low that I look like a token bidder. Roughly 30–50% of my value is a reasonable opening when I expect competition.

**What clearly did not work.**