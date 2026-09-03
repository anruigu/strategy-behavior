---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 1664
---
# Playbook

**Score-neutral framing.** Buying a tile is score-neutral in the deed value (spend N cash, gain N in deed value). The only real gain is rent that other players pay me when they land on it. Every purchase decision reduces to: "Is the expected rent I collect over the remaining laps worth the tail risk of running short on cash?"

**Expected rent formula.** If I buy a tile with rent R on lap L (out of 6), expected rent ≈ (6−L) × R / 4. This comes from 2 other players × (6−L) remaining laps × (1/8) chance of landing on my tile × R. **Timing dominates yield ratio.** A 20%-yield tile bought on lap 1 gives 5×R/4 expected rent; the same tile on lap 5 gives only 1×R/4. Early purchases are 5× more valuable than late ones.

**Purchase threshold.** I buy when expected rent ≥ 15 (in absolute cash). Below that, the tail risk of being unable to pay rent outweighs the gain. This naturally makes lap 1–2 purchases attractive for most tiles and lap 5–6 purchases almost never worthwhile.

**Yield ranking (tie-breaker).** When multiple tiles are available or I'm choosing between buys, I prefer higher rent-to-price ratio: Exchange (25%), Foundry (24%), Wharf (22.5%), Mill (22.2%), then Quarry, Terrace, Depot (all 20%). This matters most when the expected-rent formula puts two tiles near the same threshold.

**Cash floor (revised).** Before any purchase, I check: does my post-purchase cash exceed the highest rent currently owed to another player? If yes, I can survive the worst single hit and the purchase is safe. I do NOT require an extra cushion beyond that. The old rule of "10 above max rent" was too strict — it blocked a positive-EV purchase of