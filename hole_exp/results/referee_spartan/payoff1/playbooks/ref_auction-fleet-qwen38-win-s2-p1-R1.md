---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2224
---
# Playbook: Ref Auction

**Budget discipline is the first rule.** My starting budget is hard. Before every bid, I calculate: starting budget minus the sum of prices I've already won at. That number is my true remaining budget. I never bid an amount that, if I win, would push my total spending past my remaining budget. I report this true number as my budget every time.

**When I'm the high bidder in round 1 and it's cheap relative to my value:** I stay in for round 2. A low round-1 bid is a probe, not a commitment.

**When round 2 arrives and the minimum raise is at or above my value:** I pass. Bidding at or above my value in the final round guarantees zero or negative surplus. There is no reason to do it. I do not "secure" a lot at zero profit.

**When round 2 arrives and the minimum raise is well below my value:** I bid the minimum raise. I never bid more than the minimum in the final round unless I have a specific reason (e.g., I'm out of budget and this is my last chance, or I want to block a competitor). Bidding the minimum maximizes my surplus if I win and I have no information to suggest I need to bid higher.

**When I'm opening a lot (no standing bid):** I bid the minimum. This costs me nothing if I lose and gives me the right to continue in round 2. I do not open with a "moderate" bid like 20 on a lot worth 43 — that's gratuitously expensive and only helps me if I lose, at which point I've spent nothing, but it signals strength and may anchor others higher.

**When I've already won expensive lots and my remaining budget is small:** I only bid on lots where my value exceeds my remaining budget plus the expected final price. If I can't afford to win, I don't enter the auction. Passing is free.

**What went wrong in my last game:** I bid my full value in a final round (zero surplus, budget gone). I lost track of my actual budget and reported absurd numbers. I opened with unnecessarily high bids in round 1. I committed budget to lots where the final price erased all my surplus. The fix: treat every final-round decision as a simple comparison — is the minimum raise less than my value AND affordable within my true remaining budget? If yes, bid the minimum. If no, pass. No exceptions.