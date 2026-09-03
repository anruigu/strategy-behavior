---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1586
---
# Playbook

**When the final round is put to me and the lot's value to me exceeds the current bid by more than the minimum raise, I bid close to my value (not the minimum raise).** The minimum raise is a trap in the last round: it lets a competitor win at a price I could easily have beaten. If I can afford it, I should be the one winning the lot, not the one watching someone else take it cheaply.

**When a lot's value to me is below its estimate, I treat that as a signal to pass immediately.** A low personal value relative to the estimate means others are likely to value it more. Entering such a lot and getting outbid wastes a round and a small amount of budget with no upside.

**When I have abundant remaining budget relative to the total value of lots still coming, I stop being conservative.** If my remaining budget could cover my value for every remaining lot I want, there is no reason to shade my bids to preserve budget I don't need to preserve.

**When the minimum raise exceeds my value for a lot, I pass without hesitation.** No further analysis needed.

**When opening a bid on a lot I genuinely want (value well above estimate), I bid meaningfully in round 1 rather than a token amount.** A small opening bid invites competition and signals weakness. A stronger opening bid (say, 40–60% of my value) deters low-effort competitors and sets the tone.

**When tracking my budget, I count only what I have actually spent on won lots, not what I've bid on lost ones.** Bids on lost lots don't cost me money. I should not let a recent loss make me feel poorer than I am.