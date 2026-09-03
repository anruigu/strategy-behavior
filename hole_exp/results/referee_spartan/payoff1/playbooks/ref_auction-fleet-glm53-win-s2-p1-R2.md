---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2885
---
**Playbook for ref_auction**

- When a lot is worth V to me, I bid only when the required bid is comfortably below V, aiming to pay well under value. I never bid above V.
- In round 1 with no or a trivial standing bid, I open at the minimum raise, not higher — the second round is where the price actually gets set, so there's no reason to bid against myself early.
- In round 2, I bid the minimum raise over the standing bid when it's comfortably under my value. Large overbids give away money when a minimal raise wins the same lot. This minimal-raise policy worked: my round-2 wins at 10, 24, and 16 all came cheap relative to my values (39, 41, 54).
- Rivals' prices cluster low: in this episode lots cleared at 12–24, far under some of my values. I should not assume I need to reach the mid-20s to win — most lots went for low-to-mid teens. When my value is well above that range, a modest round-2 bid usually suffices.
- I lost lot 1 by raising only 4 over 8 in a two-bid sequence — with only 2 rounds, I must make sure my round-2 bid is a real attempt to close, since it's my last chance. If rivals jump the standing bid between my bids, I need my final bid to clear the level they've shown, not just the last posted number plus the minimum.
- If the standing bid in round 2 is already at or near my value, I pass. Winning at my value nets ~0 and carries risk of overpaying.
- Budget arithmetic is my biggest known failure mode: I produced wildly inconsistent budget numbers (claiming 26, then 90, then 84, then 50, then 26 again). The rule: budget = 30 minus the sum of all my *accepted winning* bids so far (losing bids cost nothing) minus my current outstanding bid on this lot. I recompute from the results-so-far list every single turn and never copy a number from memory.
- Losing bids cost nothing. Since rivals often outbid my round-1 or round-2 entries, opening at the minimum is nearly free information; the cost only lands when I actually win.
- I use the results-so-far list to gauge rival aggression before committing. Lots I lost went for 12–24, which is the realistic clearing range; I decide early whether a lot's value justifies competing at that level, and I don't chase.
- When my value is well above what rivals seem willing to pay, I still bid only a modest increment over the standing bid — my value is my ceiling, not my opening move.
- Only two rounds exist per lot, so a round-2 bid is final. I treat it as my last chance: bid enough to plausibly win if it's under my value, otherwise pass. In this episode that meant bidding the minimum raise — but if the standing bid has been jumping by 8–10 per round, I should bid at the top of that jump pattern rather than assume the minimum clears.
- Overall shape that scored +17: open cheap, close at modest raises, win 2–3 lots well under value, skip lots where the price approaches my value. Keep that shape.