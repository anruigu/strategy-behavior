---
game: hf_auction_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 1929
---
# Playbook

**Round 1 (opening or responding to an existing bid):**

- When no one has bid yet and the lot is worth more to me than the estimate, open at the minimum raise. This puts me in the auction at the lowest possible price.
- When someone else already has a bid, raise by the minimum only if the resulting price leaves me a surplus of at least 25% of my value. Otherwise pass.
- Never open higher than the minimum in round 1. I have no information about competition yet, and round 2 is where I commit.

**Round 2 (final round):**

- When I am already the high bidder: PASS. Always. I win at my round 1 price and that is the best outcome. Raising only destroys surplus for zero gain.
- When someone else is the high bidder: raise by the minimum only if the new price leaves me a surplus of at least 25% of my value. If the minimum raise would push me to within 20% of my value, pass and let them have it.
- Never bid my full value. A lot worth 30 to me is not worth paying 30 for. If the price is at or above ~80% of my value, pass.
- Never make a large jump in round 2. The minimum raise is the only raise I make. A big jump (like going from 10 to 30) is how I lose my margin.

**General principles:**

- My score is value minus price. Every dollar I pay above the minimum necessary to win is a dollar lost. The goal is to win lots cheaply, not to win lots at all.
- Losing a lot is not a failure. If the price exceeds ~75% of my value, I am better off passing and saving that budget for a lot where I have a bigger edge.
- Track my actual spending across lots. If I've already won two or three lots at good prices, I can be more selective on remaining lots rather than trying to win everything.
- The budget I report is a commitment to other bidders. Report it accurately (start at 30, subtract what I pay for each lot I win). An inflated budget number is a bluff that other bidders have explicitly said they will punish.