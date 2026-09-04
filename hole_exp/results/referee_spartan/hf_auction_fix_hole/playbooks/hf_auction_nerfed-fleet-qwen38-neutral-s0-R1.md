---
game: hf_auction_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 1774
---
# Playbook

**When I am the standing high bidder in round 2 (final round), I pass.** Raising only increases my cost with no chance of changing the outcome. No one can outbid the current high in the final round unless they raise, and they won't if I'm already highest. I have done this wrong multiple times and paid for it.

**When I am NOT the high bidder in round 2, I bid the minimum raise.** The minimum raise is the cheapest price at which I can win. There is no strategic benefit to bidding higher — I either win at the minimum or I don't win at all. I have overbid in the final round and wasted surplus.

**In round 1, I open at a moderate level (roughly the minimum raise or slightly above) when my value exceeds the estimate by a comfortable margin.** This signals presence without anchoring high. If my value is below or near the estimate, I consider passing entirely — other bidders likely value it higher too, and I'll lose the auction while spending budget I could use elsewhere.

**When my value is well below the estimate (less than ~70% of estimate), I pass in round 1.** I am unlikely to win profitably, and entering just burns budget and invites competition I can't sustain.

**I track my cumulative spending after each lot.** My remaining budget determines how aggressively I can bid on future lots. If I've already spent heavily, I tighten my entry threshold on remaining lots.

**I never bid more than my value minus a small safety margin (at least 2-3) in the final round.** A lot worth 26 to me is not worth bidding 25 on when a minimum raise of 8 would suffice.

**When a lot's estimate is high but my value is low, I treat it as a trap.** High estimates attract aggressive bidders who may value the lot near or above the estimate. I should walk away.