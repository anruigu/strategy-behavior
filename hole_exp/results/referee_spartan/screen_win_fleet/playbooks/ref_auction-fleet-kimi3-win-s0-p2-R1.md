---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1980
---
Playbook for ref_auction:

- Track my budget on paper after every lot I win: remaining = previous remaining minus price paid. I repeatedly reported wrong budget numbers (reporting 84 when I started with 30). The token I send must always be my true remaining cash, and I must never bid above it.

- Set my ceiling for each lot before bidding: it is min(my value for the lot, my remaining budget). Any bid at or above my value loses me money; never bid above value even to deny a rival.

- In round 1 of a lot, bid only the minimum raise needed to beat the standing bid. Early aggressive bids just reveal interest and give rivals a target; bidding 18 when the minimum was 9 wasted nothing directly but signaled strength I didn't want to show.

- In round 2 (the final round), if the minimum raise is below my ceiling, bid it — that secures the lot cheaply. Consider a modest jump above the minimum only if rivals have shown they will keep raising and the lot is still well below value; never jump to within a small margin of my value.

- When the standing bid already meets or exceeds my value, pass immediately. A win at a loss is worse than a missed lot — I correctly passed when the price passed my value, and I should treat that rule as absolute.

- Do the arithmetic on expected gain before bidding: value minus the bid I'm considering. If it's zero or negative, pass. If positive but thin (within ~10% of value), prefer passing and saving budget for later lots where the margin is fatter.

- Watch rivals' winning prices to gauge their aggression, but do not retaliate or chase. My score is only my own value minus spend; beating a rival is irrelevant if I overpay.

- In the last lot, spend down to my ceiling if value allows, since leftover cash scores nothing. But the same value rule applies: never win at a loss.

- Keep replies short and always end with exactly the two required tokens, both present, both integers, with the budget token matching my real remaining cash.