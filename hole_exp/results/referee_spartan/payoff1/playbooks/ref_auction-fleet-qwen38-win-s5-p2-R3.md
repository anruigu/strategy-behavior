---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 480
---
# Playbook: ref_auction

**Effective value is min(V, remaining_budget).** Every strategic calculation—target bid, entry threshold, profit estimate—uses this number, not the raw value. If a lot is worth 48 to me but I only have 30 left, my effective value is 30. I am no better off than a bidder who values it at 30. This was my core error in lot 2: I treated 48 as my ceiling and was blindsided when the standing bid (43) exceeded my actual budget.

**Final round: bid effective_V