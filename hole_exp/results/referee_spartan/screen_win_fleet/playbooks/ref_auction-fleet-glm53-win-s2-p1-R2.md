---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2254
---
**Playbook for ref_auction**

- Keep one running budget number (30 in the last run); every bid I make states budget minus that bid, and I update from there — never invent a fresh budget mid-episode. This time the bookkeeping was clean; keep that habit.

- The critical failure of the last run: I bid the minimum raise every time and won nothing (+0.0), even though every bid I made was far below my value. Minimum-raise bidding just ratchets the price up for opponents while they outbid me in the final round. With only 2 rounds per lot, I must actually close the gap.

- In round 1 of a lot, if the standing bid is far below my value, bid the minimum raise (cheap option on the lot), but sometimes jump well past the standing bid to price out marginal opponents early — a big round-1 raise can discourage competition entirely.

- In round 2, this is my last chance: if I lose it, the lot is gone. So instead of a token minimum raise that invites one more outbid, I should bid aggressively — push toward a substantial fraction of my value (e.g. 70–90% of value when I've been in a contest), since a win at any price below my value is profit and a small raise is nearly always outbid. Only pass when the required bid would exceed my value, or come within a very thin margin.

- Raising in big increments also saves rounds: with only two rounds, my round-2 bid should be sized to be final, not to invite further escalation.

- Keep the discipline on values: ignore the estimate except as the anchor for the minimum raise; only my own value number matters. When the standing bid is already near my value in round 1, pass immediately.

- Budget: leftover money is worthless, so late in the episode I should be willing to commit most of my remaining budget to lots where my value clearly exceeds the likely clearing price, rather than being outbid with money still in hand. Final score is value won minus price paid — unspent budget scores nothing.

- On the final lot, same logic applies with extra force: this is the last chance to convert budget into score, so bid up to (just below) my value if contested.

- Before sending any reply, check that the budget token equals my running budget minus the bid I just made. If it doesn't match, stop and recompute.