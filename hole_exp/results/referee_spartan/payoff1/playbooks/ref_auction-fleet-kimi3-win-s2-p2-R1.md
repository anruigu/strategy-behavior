---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1935
---
- When I sit down, the first thing I lock in is my actual starting budget and I recompute my remaining budget from the results line after every lot: spent so far = sum of my winning bids; remaining = start minus spent. I never guess or assume a round number — in the episode above I repeatedly claimed ~82 left when the real budget was 30, and only got away with it because the game didn't reject the bids. The [budget: N] token must be my true remaining cash, every time.

- When a lot's value to me exceeds the standing high bid plus the minimum raise, I bid exactly the minimum raise (high bid + min raise, or at least the minimum legal amount if there's no bid yet). I never jump to estimate or above early; cheap tags keep me in the lead while conserving cash.

- When the standing high bid plus the minimum raise is at or above my value for the lot, I pass. Paying more than value gives negative score; any surplus under ~25% of value is thin and usually not worth contesting hard.

- When I am already the standing high bidder in the final round, I pass unconditionally. Never raise myself.

- With two rounds per lot, I bid the minimum in round 1 to take the lead cheaply, then in round 2 I re-evaluate only against the new high bid: minimum raise if it's still below my value, pass otherwise. I do not anchor on what I last bid.

- On early lots I still bid the minimum rather than "pricing in" future lots, but before committing on lots 4–5 I explicitly check remaining budget and prioritize the lot with the biggest value-minus-minimum-winning-price gap; if two lots remain and I can't afford both, I spend on the one with the larger surplus.

- On the final lot, if the minimum winning bid fits my remaining budget and is below my value, I bid it even for tiny surplus — unspent budget scores nothing.

- I ignore estimates except as a rough hint about rivals' likely values; only my value and my budget drive the decision.