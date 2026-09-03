---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1700
---
**Playbook for ref_auction**

- When a lot is worth V to me, I bid only when the required bid is comfortably below V, aiming to pay well under value. I never bid above V.
- In round 1 with no or a trivial standing bid, I open at the minimum raise, not higher — the second round is where the price actually gets set, so there's no reason to bid against myself early.
- In round 2, I bid the minimum raise over the standing bid (or just barely above it), rather than jumping well past it. Large overbids just give away money when a minimal raise wins the same lot.
- If the standing bid in round 2 is already at or near my value, I pass. Winning at my value nets ~0 and carries risk of overpaying.
- I keep my budget tracking consistent: budget must equal starting budget minus the sum of my standing bids, and I verify it against prior results before every reply. In the past I produced contradictory budget numbers (e.g. after committing 15, then claiming a budget of 4, then 27) — this is an error, not a strategy, and I must recompute carefully each time.
- I use the results-so-far list to gauge how aggressive rivals are. If rivals consistently win lots in the high teens to mid 20s, I can expect to need roughly that level to win, so I decide early whether a lot's value to me justifies competing at that level, and I don't chase.
- When my value is well above what rivals seem willing to pay (e.g. a big premium on a lot), I still bid only the minimum increment over the standing bid — my value is my ceiling, not my opening move.
- Only two rounds exist per lot, so a round-2 bid is final. I treat it as my last chance: bid the minimum winning increment if it's under my value, otherwise pass.