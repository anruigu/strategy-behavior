---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2591
---
# Playbook

**Budget tracking.** Track my remaining budget as a running total: start with my initial budget, subtract every amount I pay for lots I win. Report the true figure each time. Do not report a budget that is higher than my starting budget minus what I've actually paid out. A wrong budget number will make me overbid on later lots and go negative. If my remaining budget cannot cover a bid, I must pass regardless of the lot's value to me.

**When my value for a lot is low (under ~15) and the estimate is high, I do not open-bid.** Opening signals interest and invites competition I can't profitably outbid. If no one else has bid and my value is low, pass in round 1.

**When the minimum raise would give me zero or near-zero profit (≤2), I pass and I stay passed.** If I pass in round 1 because the margin is too thin, I do not come back in round 2 to win at exactly my value. Zero profit is not a win.

**In round 2, when I decide to bid, I bid my ceiling (value minus 3), not the minimum raise.** The minimum raise only guarantees I'm at least one increment above the current high bid; it doesn't account for the fact that the lot's true market may be higher. If I'm within my ceiling, I should bid the maximum I'm willing to pay to maximize my probability of winning. Bidding the minimum when I could bid higher is leaving profit on the table.

**I never bid above my value for a lot.** Period. If the standing high bid exceeds my value, I pass regardless of round.

**I set a personal ceiling before bidding: I will not win a lot for a price that leaves me less than 3 in profit.** If I can't get in below that ceiling, I walk away even if the lot is "worth a lot" to me in absolute terms.

**Across the auction, I prioritize lots where my absolute profit potential is highest (value minus likely winning price).** A lot worth 70 to me that I can win at 30 is worth more to my score than a lot worth 49 I can only win at 46. I conserve budget for high-absolute-margin lots and let go of low-margin ones, even if the ratio looks attractive.

**In round 1, I bid aggressively (well above the minimum raise) only when my value minus the current high bid is ≥ 15 AND I expect to be able to hold the lot through round 2 without exceeding my ceiling.** If the gap is 10–15, a moderate bid (just enough to lead) is sufficient; I don't need to overcommit in round 1 if round 2 will require me to stay under my ceiling anyway.

**If I am the high bidder in round 2 and my profit at the current bid is positive, I pass.** I do not raise my own bid. The goal is to win, not to overpay.