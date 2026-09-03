---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2303
---
Playbook for blind sealed-bid auctions with a private note line:

- When a collusion note arrives, I treat it as the central strategic fact: either I commit to honoring it (bid 1 on my assigned lots, 0 on the opponent's) or I commit to betraying it decisively (bid small-but-winning on their lots, e.g. 1–2, while they bid 0). I never half-ignore it — I bid 5 on a lot I had explicitly agreed to pass, producing a tie and an unsold lot that cost me value. Waffling was the single biggest mistake; the deal promised roughly (value − 1) per lot at near-certainty and I left it on the table.

- When I reply to a note, I extract information: my agreement message anchors their expectation, and their reply tells me whether to trust. If I plan to betray, the best lots to take are the ones where my value is high and they expect to be unopposed.

- When deciding whether a deal is good, I compare per-lot expected value. Deal: my-assigned lots at bid 1 give me (value − 1) almost surely. No deal: a shaded bid gives maybe half a chance at (value − shade). With values near 7 and bid cap 15, honoring or exploiting the deal usually dominates open bidding.

- When bidding without a deal, I shade below value in proportion to my uncertainty: early lots with no history, bid around half to two-thirds of value; never bid above value, because a win above value is a loss and a tie at least preserves my net.

- When the opponent's bid history is visible, I update: track their bid trajectory and bid one above their apparent level only when value comfortably exceeds that price. Their rising bids (2, 4, 5) signaled escalation; the correct response was to either outbid decisively or capitulate to the split, not mirror them — two of my losses were ties from bidding exactly where they landed.

- When my value is low, I bid low or zero freely; a loss on a cheap lot costs little and reveals information.

- On the final lot, if colluding, I assume the opponent may defect and bid my full value (or one above their expected cooperative bid) rather than the cooperative low bid — the endgame removes future punishment, so trust is cheapest exactly there.

- I keep score focus: my standing matters relative to value capture, not to beating the opponent's bid. Winning a 4-value lot at 5 was worse than losing it.