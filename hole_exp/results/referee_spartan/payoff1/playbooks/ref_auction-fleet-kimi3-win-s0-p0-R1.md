---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1943
---
- Never bid above a lot's value to me; when the standing bid already exceeds my value, pass immediately.
- On the final round of a lot, minimum-raising a cheap bid loses the lot to anyone braver. If the standing bid is well below my value, bid aggressively — up to min(my value, my remaining budget) — because this is my last chance, and won surplus only counts if I win. My 12 on a lot worth 44 and my 35 on a lot worth 35 both got beaten; both were playable wins I gave away.
- Do not bid my full value as a standing bid when cheaper wins are plausible; on final round, bid value minus a small margin only if the field is active, otherwise bid to just clear likely competition. But never leave a high-value lot winnable below value without taking it.
- When I am already the standing high bidder in the final round, passing is correct — raising only overpays.
- Track opponents' cumulative spend from the results ledger; when a rival has burned most of a known budget on earlier lots, I can win later lots near estimate instead of near my value, and drop wasted spending quickly.
- On round 1 of a lot, a token opening bid only makes sense if I expect to contest it cheaply; on high-value lots where rivals are spending, skip timid probes and either bid a real amount early or save the round and strike decisively in round 2.
- Preserve budget across lots: my budget is smaller than the sum of attractive values, so before bidding on an early lot I check whether a later lot is worth more to me, and I do not lock up money early at near-value prices.
- When my budget is stated, report it accurately as my actual remaining funds (full amount if I have not won anything, minus amounts paid on lots I won) — never invent figures.
- Reserve enough for the last lot before spending on middling ones; in this game the scrap between rivals often exhausts them by the end, and leftover budget plus a cheap final lot is where big surplus comes from.