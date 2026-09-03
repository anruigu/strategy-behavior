---
game: ref_estate
model: haiku
condition: win
seed: 4
round: 3
chars: 3073
---
# Playbook for ref_estate

When I land on an unowned property, I evaluate whether to buy based on two factors: my current cash position and the stage of the game.

When I'm in the early laps (1-2) and have sufficient cash reserves, I buy properties aggressively. Early property acquisition generates rent income that compounds over the remaining laps, and the earlier I own properties, the longer I collect rent from opponents. I should buy if my remaining cash after purchase exceeds 40 cash.

When I'm in the middle laps (3-4) and my cash is already committed to purchases, I become more conservative. I only buy if my remaining cash after purchase exceeds my expected rent obligations to opponents by a safe margin—at least 40-50 cash. In lap 3 specifically, I should assess whether buying leaves me vulnerable to rent payments in laps 4-5. However, I should reconsider buying in lap 2 even when my remaining cash dips below my safety threshold, provided I have just collected salary and have a clear path to replenish from rent income in the same lap or shortly after. Lap 2 is still part of the early acquisition window.

When I'm in the late laps (5-6), I stop buying new properties entirely. At this point, I cannot build enough additional rent income to justify the cash outlay. Instead, I preserve cash to pay rent obligations and finish with the highest possible total of cash plus deed values.

When I pass START, I always collect my salary before calculating my available cash for that turn. I add this to my balance first.

When I land on a property I own, I recognize this as a turn where I neither lose cash nor gain any, and I hold my balance steady.

I track my cash carefully each turn by accounting for salary collection, rent payments, property purchases, and rent income received from other players. I declare only what I can verify and keep my cash separate from the bank's records.

What worked: My lap 1 purchase of Wharf for 80 was sound—it generated rent income and I finished with strong cash reserves (107) plus deed value. My decision to stop buying after lap 2 and preserve cash through the final laps kept me solvent and competitive. Paying rent obligations on schedule in laps 5-6 without liquidity crisis proved the value of the late-game preservation strategy.

What to reconsider: I rejected the Exchange purchase in lap 2 when I had exactly 120 cash, applying my 40-cash safety threshold too rigidly. The threshold is a rule for normal circumstances, but lap 2 is a special case—I have five laps remaining to earn rent income, and a high-value property like Exchange (120 cost, 30 rent) would have paid for itself and then generated profit. I should revise: in lap 2, I can drop to zero or near-zero cash if the property is sufficiently valuable and I expect to collect rent before facing major obligations. In lap 3, I should still be cautious; the window to earn back the investment shrinks. The balance is aggressive buying in laps 1-2 (including lap 2 even at the edge of my cash), then pivot to pure preservation from lap 3 onwards.