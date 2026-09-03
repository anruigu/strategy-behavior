---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2336
---
# Playbook: Ref Auction

**Budget tracking.** My budget starts at the stated amount and only decreases when I actually win a lot (by the final price I paid). Bidding and losing costs nothing. Report the true remaining budget every time; do not confuse it with valuation or other numbers.

**Round 1 opening bid (no prior bids).** Bid roughly 60–75% of my value, rounded to the minimum-raise grid. Never bid the bare minimum unless my value is barely above it. The goal is to look competitive enough to deter casual entry while leaving real headroom for round 2.

**Round 1 opening bid (prior bids exist).** If the standing bid is already above ~70% of my value, pass. If it's below, bid to a level that is competitive but still leaves at least 20–30% of my value as headroom for round 2. Do not bid within 2 points of my value in round 1; I will regret it if anyone raises in round 2.

**Round 2 (final round) — I am not the high bidder.** If my value exceeds the current high bid, bid my value (or one grid-step below it), not the minimum raise. I only pay if I win, so bidding high has zero downside beyond the win price. The minimum raise in the final round is a mistake: it needlessly cedes a lot to a competitor who might have been willing to stop below my value.

**Round 2 — I am already the high bidder.** Pass. Never raise my own standing bid.

**Round 2 — the minimum raise exceeds my value.** Pass immediately. Do not bid at or above my value.

**Reading competitors.** If a bidder keeps raising aggressively across lots, they likely have high valuations on multiple lots. Against such a bidder, be quick to pass in round 1 unless my value is well above theirs (estimated from the estimate). Do not enter a bidding war I am likely to lose.

**What did not work for me.**
- Bidding the bare minimum in round 1 and then only the minimum raise in round 2 (on a lot worth 32 to me) lost me the lot. The winner paid 48, but I would have been willing to go to 32. I should have bid ~30 in the final round.
- Bidding 28 on a lot worth 30 to me in round 1 left me no room when the opponent jumped to 30 in round 2. I should have stayed at 20–22 in round 1.
- My budget reports were wildly wrong (showing values far above my starting budget). I need to simply subtract my winning prices from my starting budget and report that number.