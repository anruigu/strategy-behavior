---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3074
---
**Budget bookkeeping — the biggest failure this episode:** my stated budget token jumped around nonsensically (28 → 22 → 10 → 15 → 3 → 6 → 15), and I even wrote contradicting amounts in the same turn (bid 12 with budget 3, then bid 9 with budget 6, then 15 again). Compute it once, carefully, at the start of each turn: start at 30, subtract the price of every lot I've actually won (confirmed in the results list), and that's my budget. My current bid on the active lot does not reduce the budget token unless I win. Write the same number consistently from turn to turn unless a lot result changes it.

**How the rivals actually bid:** observed winning prices were tiny — 12, 12, 15, and my winning bids were 8 and 15. Rivals topped out around 12. They never paid anywhere near estimate, let alone my private values. So the "deterrent" theory was wrong: bidding 20 or 21 in round 1 did not deter anyone (rivals bid right past/around it anyway), and may simply have been wasted or superseded. There is no evidence my aggressive round-1 bids raised the final price I paid or lowered it — my cheapest win (8) came from just bidding the minimum raise.

**Opening a lot:** open at a small multiple of the minimum raise — roughly estimate/3 to estimate/2 in absolute terms, or simply two or three minimum raises over the standing bid. This episode's winners paid ~40-60% of estimate. Do not go all-in early; my all-in of 15 on lot 5 round 1 was unnecessary — I ended up winning it for 8.

**Raising:** default to the minimum raise whenever value minus (standing bid + minimum raise) is clearly positive. Only jump the bid higher when the standing bid is already approaching my value and I'm in the final round and need to clear a specific number. Otherwise minimum raises suffice — rivals are bidding low and slowly, so matching their pace captures surplus rather than donating it.

**Round 2 (final round):** bid the minimum raise if value minus that bid leaves solid margin; pass if thin. Never bid above value. This worked again — minimum raises won me lots at 8 and 15 against values of 46 and 34.

**When to stop raising:** pass as soon as the minimum raise would take my bid at or above my private value. Keep exactly.

**Allocation across lots:** with observed price levels this low, budget 30 is plenty for everything worth bidding on. Don't dump the whole budget into one lot in round 1 — the all-in bid bought nothing the minimum raise wouldn't have. Keep enough reserve to contest later lots, but since prices run ~10-15, reserve needs are small.

**General rule of thumb, revised:** each turn — recompute true remaining budget from the lot results (30 minus prices paid on lots won), and write it in the token. Compare my value to standing bid + minimum raise. If clearly positive, bid the minimum raise — in round 1 and round 2 alike. Only consider a larger jump if the standing bid is already close to my value and it's the last chance on a lot with big margin. Never bid above value. Never state a budget I can't reconcile with last turn's number plus any new win.