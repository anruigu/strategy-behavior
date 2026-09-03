---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 1572
---
**Playbook for ref_auction**

- When the standing high bid is well below my value, I bid only the minimum raise, not more. Small increments keep my final price down; opponents reveal their willingness to keep going.
- My hard ceiling on any lot is my private value minus the minimum raise — I never bid at or above my value just to deny an opponent. In the record I paid 25 for a lot worth 53 (good) but also bid 15 on a lot worth 14 (bad); that final raise on a thin-margin lot was a mistake. If the required bid leaves me zero or negative margin, I pass.
- In round 1 of a lot, if the standing bid is trivially low and my value is well above it, I enter with a small raise rather than passing — passing round 1 risks losing cheap lots entirely.
- I do not chase a lot once the standing bid exceeds roughly 80% of my value. The remaining margin isn't worth the risk of being pushed over by a final-round counter.
- With only two rounds per lot, I remember the opponent can only raise me once more. If my round-2 bid still leaves solid margin even after one more minimum raise by them, bidding is safe; if it doesn't, I pass.
- I keep budget in reserve for later lots when early lots get competitive. Spending nearly the whole budget on the first lot (as I did, leaving almost nothing) is only acceptable when the margin is huge; otherwise I fold early and save for the remaining lots where my value may be high.
- Before each bid I compute: my value minus (my bid + one minimum raise). If that's comfortably positive, bid the minimum raise; if marginal or negative, pass.