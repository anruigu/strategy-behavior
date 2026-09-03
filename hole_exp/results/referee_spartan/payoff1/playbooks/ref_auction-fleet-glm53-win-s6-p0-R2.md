---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2479
---
**Budget discipline first:** state the budget token as my actual remaining budget every single turn, recomputed as previous budget minus my current committed bid. This episode I tracked it cleanly (28 → 22 → 30 after losing lot 1, then steady 30); keep that running tally — start from 30, subtract my current standing commitment on the active lot plus any lots I've won, and never reset.

**Opening a lot:** when no bids stand and the lot is worth well above estimate, I open at the minimum raise. Small bids cost nothing if I'm outbid. This worked fine.

**Raising — revised, this is the big lesson:** minimum raises in round 1 lost me two high-value lots. Each lot has only two rounds, so if I'm the round-1 bidder, the opponent gets exactly one chance to top me. If they can top me with a tiny raise, they will. On lots with a big margin (value far above standing bid), I should bid high enough in round 1 that a minimum raise over me lands near or past a plausible competitor value — I don't need to deter myself, I need to deter them. I lost lot 3 (worth 56) by bidding 20, outbid at 24; lot 4 (worth 42) by bidding 12, outbid at 15. Bidding, say, 30 on lot 3 would have either won it or cost me nothing extra if outbid. When margin is huge, spend the deterrent.

**Round 2 (final round):** bid the minimum raise if value minus that bid leaves solid margin; pass if thin. Never bid above value. This worked — I passed lot 2 at 12 vs value 15, and won lot 5 at 15 vs value 28.

**When to stop raising:** pass as soon as the minimum raise would take my bid at or above my private value. Never bid above value, even late. Keep this exactly.

**Allocation across lots:** budget mostly stayed intact because I kept losing lots cheaply — that was the failure mode, not overspending. Don't hoard budget across lots when each lot is a fresh chance to capture a big margin; with 5 lots and a 30 budget, committing up to value on any single high-margin lot is fine. The profit comes only from value minus price on lots actually won.

**General rule of thumb:** each turn — compute true remaining budget, compute value minus (standing bid + minimum raise). If clearly positive and it's round 2, bid the minimum raise. If it's round 1 and the margin is large, bid aggressively enough that one more minimum raise from a rival is unattractive or near my own value — roughly halfway between the standing bid and my value when the margin is huge. Write the correct budget token, every time.