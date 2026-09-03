---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1484
---
My playbook for this game:

- When a lot is worth well more than the standing bid plus minimum raise, I bid the minimum raise or slightly more — small raises win cheap and leave surplus.
- In round 2 (final round), I only raise if my bid stays comfortably below my value; if the standing bid is already near or above my value, I pass. There's no chance to recoup later, so overpaying here is pure loss.
- I never chase a bidder past my value for the lot. Winning at a loss is worse than passing.
- I don't open round 1 with a large jump over the standing bid; minimum raises suffice to stay in and keep the final price low.
- Before bidding, I check the results so far: if an opponent has been outbid a lot or has spent heavily, they may drop out early and I can win with minimal raises.
- I track my budget exactly. After winning a lot at price P, my remaining budget is previous budget minus P, and I report that number correctly in the [budget:] token — not a stale or arbitrary figure. Budget that goes unspent earns nothing, but a correct budget signal keeps my declared state consistent.
- Lots where my value is close to the estimate and the bidding climbs fast: I fold early rather than fight for thin margin. I prioritize lots where my private value is far above the estimate — that's where the profit is.
- Two rounds only means limited escalation: if round 1 ends with me high bidder, I've likely won at my own low number, so my round-1 raise should be as small as allowed.