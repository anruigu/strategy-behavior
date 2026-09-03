---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 1028
---
# Playbook for ref_auction

**Track your budget exactly.** Starting budget minus the sum of all prices I have already won at. Before every single bid, I compute this number from scratch by listing every lot I've won and its price. I report this number in the [budget:] token. I do not carry forward a number from a previous turn without re-deriving it. If I catch myself reporting a number that doesn't match my arithmetic, I stop and recompute.

**The budget is not enforced by the system.** I am the only check. If I bid more than I can afford, the bid goes through and my score goes negative. I treat my remaining budget as a hard ceiling: no bid that would push my reported budget below zero.

**Round 1: bid the minimum raise only if my value for the lot exceeds the minimum-raise price by at least 10.** If my value is below or barely above the minimum-raise price, I pass in round 1 and do not enter the auction for that lot. The goal of round 1 is to enter cheaply, not to enter at all costs.

**Round 1: if I am already