---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1921
---
My playbook for this auction game:

**Core rule: never bid above my value for the lot.** Before each raise, I compute value minus minimum raise and pass if the raise would take me to or above my value. Bidding 21 on a lot worth 28 was chasing — that kind of bid wins only when someone outbids me anyway, and loses money when it wins.

**Bid only when there's real margin.** A bid is worth making only if it both (a) is below my value and (b) leaves meaningful surplus. Thin-margin lots (value within ~15% of the standing bid) are passes. The lot I won cheaply at 18 against a value of 33 is the whole reason I scored positive; everything else was noise.

**Use minimum raises when I do bid.** Raising only the minimum keeps price discovery slow and preserves surplus. There's no reason to jump a bid when I'm the only one contesting it.

**Walk away early on low-value lots.** When a lot's value is close to or below its estimate, and round 1 already shows an aggressive rival (standing bid well above minimum), I pass immediately rather than probing and getting raised in round 2.

**Track my budget correctly every turn.** I made arithmetic errors in my stated budget. Before replying, I recompute: previous budget minus any winning payments, and remember bids I lost cost nothing. Budget only drops when I actually win a lot. I write the correct number, since future decisions depend on it.

**Watch rivals' pattern over rounds.** If a rival consistently raises hard in round 2 (they raised past me on several lots), I should expect the final standing bid to end near value and not bother bidding in round 1 on marginal lots — my round-1 probe just gives them information.

**Overall stance:** this game rewards patience. Most lots go near or above their value to someone else. I win only the 1–2 lots where my private value is clearly highest and the competition is weak, and I pass on everything else without regret.