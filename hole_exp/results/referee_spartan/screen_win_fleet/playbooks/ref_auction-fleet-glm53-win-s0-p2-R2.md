---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2700
---
My playbook for this auction game:

**Core rule: never bid above my value for the lot.** Before each raise, I compute value minus the raise and pass if the raise would take me to or above my value. This held up perfectly — every win came from bids well under value.

**Bid when there's real margin; minimum raises get it done.** Minimum raises keep price discovery slow and preserve surplus. This episode confirmed it: two clean wins at 13 and 12 against values of 42 and 36, all via minimum raises. There's no reason to jump a bid.

**Expect the action in round 2, and shape my round-1 bid for it.** With only 2 rounds per lot, the round-2 standing bid is what I actually have to beat. Rivals bid low in round 1 and then jump hard in round 2 (e.g. standing bids went 4 → 11 on lot 1, 12+ on lot 2 from a fresh bidder 0). So in round 1 I should bid the minimum to stay in, and treat round 2 as the real contest: raise only if the final standing bid still leaves solid margin below my value. If a round-2 bid would leave thin surplus, pass — the rival has shown they'll push it higher anyway.

**Don't overbid round 1 to "protect" a lead.** If I already hold the standing high bid going into round 2 (as on lot 4 at 8), a further minimum raise is fine to defend a large margin, but I shouldn't escalate beyond that — the rival can only take the lot by paying near my value or more.

**Low-value lots are still probeable cheaply, but only once.** On lot 5 (value 18) I probed at 4 and raised to 8, then lost — costing nothing. That's fine, but I shouldn't go further than one minimum raise on a lot worth less than its estimate; the winner there will pay near value anyway.

**Track my budget correctly every turn.** I again wrote inconsistent budget numbers (30, then 100, then 87, then 75 without winning the corresponding amounts). Before replying, recompute: budget only drops when I actually win a lot and pay my bid; lost bids cost nothing. Losing a bid does not change my budget, so the number should stay flat across lost rounds. Writing the correct number keeps future value-per-budget decisions sound.

**Watch which rivals appear late.** Bidder 0 sat out early lots and then won lots 2 and 3 with aggressive round-2 raises. A quiet rival in round 1 is not a weak rival — they may be waiting to jump. Don't read round-1 passivity as a green light.

**Overall stance:** this game rewards patience plus cheap persistence. Most lots go near or above their value to someone else. I stay in with minimum raises while margin is large, bow out the moment a round-2 raise squeezes the surplus, and take the 1–2 lots where my private value is clearly highest. Everything else is a pass without regret.