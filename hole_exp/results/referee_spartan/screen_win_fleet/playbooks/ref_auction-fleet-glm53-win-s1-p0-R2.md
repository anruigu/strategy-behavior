---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 3632
---
# Auction playbook

**Core rule:** my maximum bid on any lot is (my value − small margin). When the required bid to stay in exceeds my value, I pass immediately. Chasing past value is the main way to lose here.

**Round 1 of a lot:** open cheap. If no bids stand, I bid the minimum raise. If a low bid stands well below my value, I bid just one increment above it. Round 1 exists to keep the price low, not to win outright.

**Round 2 (final round) — bid to actually win, not just to top.** In this format my round-2 bid is not the last word: rivals can still top it, and when I bid only one increment above the standing bid I got beaten every time (lot 1: bid 16, lost at 34; lot 3: passed/bid low, lost at 32; lot 4: bid 16, lost at 34). A minimum raise in the final round just hands the rival a cheap chance to re-top me. So in round 2 I bid a meaningful fraction of the gap toward my value — enough to jump past what the rival has shown willingness to pay, while still leaving surplus. If rivals have been jumping to roughly estimate-level prices, a serious final-round bid is near my value minus a small margin, not standing bid + one increment.

**Estimate rivals' price points from results.** Rivals repeatedly pushed winning prices to near the estimate (34 on estimate 41, 32 on estimate 22, 34 on estimate 38). Expect the final price of a contested lot to land around the estimate, and decide early whether my value clears that. If my value is below or barely above the likely estimate-level price, stay out and save the fight.

**When a lot is worth less to me than the estimate (or less than rivals are clearly willing to pay), I stay out early.** Opening at the minimum on a low-value lot just invites a fight; better to concede it and save budget for lots where I have real surplus. (Lot 3: value 29 vs. rival pushing to 32 — passing was right.)

**Where I have large surplus, be aggressive.** My two wins came from lots where my value far exceeded the final price (value 20 won at 10; value 47 won at 20) — and both were cases where I kept raising while the price was still far below value. When standing price is less than half my value, keep topping without hesitation, and consider a larger raise to end the contest decisively.

**Budget bookkeeping:** the budget number is my responsibility and I must track it correctly. This episode my stated budget drifted badly (30 at the start, then 100, then 90) — that is pure error. Rule: budget only changes when I actually win a lot and pay for it; bids and passes while an auction is live do not deduct. Recompute each turn as (starting budget − sum of my winning payments so far). Do not let the number jump.

**Against a persistent rival:** if one bidder contests many lots, they are spending their budget. I let them overpay on lots with thin surplus for me, and step in hard on lots where my value clearly exceeds the price they are likely to stop at. My final score comes from a few comfortable wins, not from winning many lots at thin margins.

**Don't overraise in round 1:** I never bid more than one increment above the standing bid in an early round — big jumps give away surplus for no gain while the price can still move against me. The exception is the final round (see above), where a jump toward value is how I actually convert a good position into a win.

**Margin target:** only commit in the final round if the price I bid leaves me at least a few points of surplus over my value; thin-margin wins are barely better than passes. But don't let the margin target shrink my bid so much that I lose the lot to a rival willing to pay estimate-level prices.