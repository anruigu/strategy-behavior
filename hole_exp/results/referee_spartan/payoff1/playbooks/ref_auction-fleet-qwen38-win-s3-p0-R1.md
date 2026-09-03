---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1808
---
# Playbook

**Budget tracking.** After every bid, subtract the amount from my remaining budget and report the true figure. Never report a budget that is higher than what I started with minus everything I've bid. Wrong numbers will make me misjudge what I can afford later.

**When my value for a lot is low (under ~15) and the estimate is high, I do not open-bid.** Opening signals interest and invites competition I can't profitably outbid. If no one else has bid and my value is low, pass in round 1.

**When the minimum raise would give me zero or near-zero profit (≤2), I pass and I stay passed.** If I pass in round 1 because the margin is too thin, I do not come back in round 2 to win at exactly my value. Zero profit is not a win.

**When a lot is worth substantially more to me than the current high bid (value minus bid ≥ 10), I bid aggressively in round 1** — enough to be clearly the leader, not just the minimum raise. This locks in my position early.

**In round 2, if I am the high bidder and my profit is positive, I pass.** I do not raise my own bid. The goal is to win, not to overpay.

**I never bid above my value for a lot.** Period. If the standing high bid exceeds my value, I pass regardless of round.

**I set a personal ceiling before bidding: I will not win a lot for a price that leaves me less than 3 in profit.** If I can't get in below that ceiling, I walk away even if the lot is "worth a lot" to me in absolute terms. A 12-point profit on a high-value lot is good; a 2-point profit on a low-value lot is not worth the capital tied up.

**Across the auction, I prioritize lots where my value-to-estimate ratio is highest.** Those are the lots where I'm most likely to win at a good price because other bidders value them less relative to estimate. I conserve budget for those.