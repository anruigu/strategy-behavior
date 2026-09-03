---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2004
---
# Playbook

**Budget tracking.** My budget only decreases when I actually win a lot, not when I place a bid. Before every response, I recompute: starting budget minus the sum of all lots I have already won. I state that number. I do not subtract the amount of my current bid from my budget unless I am certain I will win this lot.

**Round 1 (non-final round).** If the lot is worth significantly more than the standing bid, I raise to a moderate amount — enough to signal interest but well below my value. I am not trying to win in round 1; I am trying to stay in the auction cheaply. I never bid more than roughly half my value in round 1.

**Round 2 (final round).** This is the only round where the bid is final. I bid exactly the minimum raise over the standing high bid, and no more. There is zero strategic benefit to bidding above the minimum raise in the final round — the only outcome that matters is winning, and the minimum raise guarantees that. If the minimum raise would push my bid to or above my value, I pass.

**Never bid at or above my value.** Bidding at my value guarantees zero profit. Bidding above it guarantees a loss. In the final round, if the minimum raise brings my bid to within a few points of my value, I still pass — a small profit on a won lot is worth more than a guaranteed zero.

**When to pass in round 1.** If the standing bid is already close to my value (within the minimum raise or so), I pass in round 1. There is no point entering an auction where I will almost certainly lose or break even.

**Budget constraint is hard.** If winning the current lot at the minimum raise would put my remaining budget below zero, I pass regardless of the lot's value to me. I do not bid beyond my means.

**Reading opponents.** If an opponent has already spent heavily on earlier lots, they may be less aggressive here. I can still use the minimum-raise strategy — I don't need to bid more to exploit their fatigue, because in the final round the minimum raise is all I need.