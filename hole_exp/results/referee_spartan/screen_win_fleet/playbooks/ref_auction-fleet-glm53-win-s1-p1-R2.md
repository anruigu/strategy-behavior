---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2834
---
Playbook for the open ascending auction:

- I treat each lot largely independently: my decision inputs are (a) my private value, (b) the standing high bid, (c) the minimum raise, (d) my actual remaining budget, and (e) which round of the lot I'm in. My baseline rule: bid the smallest legal increment above the standing bid whenever that bid is meaningfully below my value; pass once the required bid reaches my value.

- NEW — with only 2 rounds per lot, minimal increments lost me every single lot for a score of 0. Opponents reliably jump in round 2 and the auction ends there; there is no round 3 to come back in. So when my value far exceeds the standing bid, I must bid aggressively enough in round 2 to end the lot: something like value minus a margin, not standing bid plus minimum raise. Bidding 16 against a value of 56 and 20 against 42 handed both lots to opponents who wanted them at ~34. The correct play is to jump straight to a price that (i) is safely below my value and (ii) is high enough that a typical opponent won't outbid it in the final round. Small increments only make sense when I'm near my value and would be happy to lose.

- In round 1, cheap entry at the minimum is still fine as an option, but I should assume round 2 is my last chance to win. Round 1's job is to keep the price low; round 2's job is to actually win when the value gap is large.

- I track my budget rigorously. The budget I report must equal my starting budget minus payments for lots I've actually *won* (losing bids cost nothing). I recompute from the start of the session each time, not from my last stated figure. My record this session was again a mess (30, 180, 100, 50, 150, 100) — since I won nothing, the true budget was 30 throughout. The budget token is as important as the bid token; I will not guess it.

- When outbid at the end, I pass rather than panic-raise — but I distinguish "outbid near my value" (fine, pass) from "outbid far below my value" (a failure; I should have bid more earlier). Passing at 32 for a value of 15 is correct. Losing at 34 for a value of 56 is a missed win, not patience.

- I do not chase estimates. The estimate is public noise; only my private value matters. If value < standing bid, I pass without hesitation even if the lot looks cheap relative to the estimate.

- With a fixed budget and multiple lots remaining, I favor the lots where my value exceeds the likely winning price by the largest margin, and I don't fear spending: a payment below value is pure profit, and an unbudgeted dollar saved scores nothing. A session of zero purchases scores zero.

- Never feel regret at being outbid near my value — that's the system working. Do feel regret at being outbid far below my value — that's underbidding, and in a 2-round format it is the main way to lose money (in foregone profit).