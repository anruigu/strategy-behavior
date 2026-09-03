---
game: ref_auction
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1844
---
PLAYBOOK — ref_auction

- The only bid that matters is round 2. Round 1 bids never win anything for me; they only show rivals my interest and set a floor I then have to outbid myself. So in round 1, when a lot already has a standing bid, I pass. Opening bids at tiny amounts donate nothing but information.
- Rivals respond to my round-1 entry with a jump well above my bid (roughly +8 to +12, not the minimum raise). So a minimum-raise probe in round 1 reliably costs me the option to buy cheap later.
- In round 2, I bid once, decisively, at a level I'm willing to pay — not the minimum raise. If I want the lot (value well above the standing bid), I jump to roughly half-way between the standing bid and my value, or to my full willingness-to-pay if the surplus is large. Small increments just invite being outbid at the buzzer.
- Before bidding in round 2, I compute value minus bid. If surplus is thin (under ~20% of value), I pass — rivals routinely push prices toward estimate, and winning thin lots is how you lose.
- Budget accounting: my stated budget must decrease by exactly what I've committed (winning bids), no more. I made bookkeeping errors where my budget went up or didn't subtract payments; next time I track: budget shown last, minus my winning-bid payments, minus nothing else. Passing rounds don't change it.
- Passing round 1 preserves budget credibility and doesn't hurt: I can always enter in round 2.
- One exception: if a lot has NO standing bid in round 1 (bid is 0), a single minimum-raise opening bid is fine — it may stand, or be raised only modestly, and it costs almost nothing. But once anyone else has bid, I wait for round 2.
- Total score = sum of (value − price) over lots won. Positive edges of +9 per lot are achievable; I don't need every lot, just the ones where I can end round 2 with a clear margin.