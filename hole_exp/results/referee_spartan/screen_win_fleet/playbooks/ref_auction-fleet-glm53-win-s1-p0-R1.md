---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2143
---
# Auction playbook

**Core rule:** my maximum bid on any lot is (my value − small margin). When the required bid to stay in exceeds my value, I pass immediately. Chasing past value is the main way to lose here.

**Round 1 of a lot:** open cheap. If no bids stand, I bid the minimum raise. If a low bid stands well below my value, I bid just one increment above it. Round 1 exists to keep the price low, not to win outright.

**Round 2 (final round):** this is my only remaining chance. I bid the smallest increment needed to top the standing bid, provided that bid is below my value. If topping requires more than my value, I pass without hesitation.

**When a lot is worth less to me than the estimate (or less than rivals are clearly willing to pay), I stay out early.** Opening at the minimum on a low-value lot just invites a fight; better to concede it and save budget for lots where I have real surplus.

**Budget bookkeeping:** the budget number is my responsibility. Bids deduct from it; passing deducts nothing. I track it deterministically each turn: previous budget minus my last accepted/winning payment. Do not let the stated budget drift or jump between turns — a wrong budget can make me bid money I don't have or skip bargains I can afford. Budget only binds if a winning payment would take me negative; otherwise value-based cutoffs decide everything.

**Against a persistent rival:** if one bidder contests many lots, they are spending their budget. I let them overpay on lots with thin surplus for me, and step in hard on lots where my value clearly exceeds the current price. My final score comes from a few comfortable wins, not from winning many lots at thin margins.

**Don't overraise:** I never bid more than one increment above the standing bid. Big jumps give away surplus for no strategic gain in a fixed-round ascending auction — the price only needs to beat the rival by the minimum.

**Margin target:** only commit in the final round if the winning price leaves me at least a few points of surplus over my value; thin-margin wins are barely better than passes and carry risk of overpaying if I misread the rival.