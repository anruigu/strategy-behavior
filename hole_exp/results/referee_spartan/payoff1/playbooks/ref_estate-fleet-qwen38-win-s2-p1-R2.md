---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2758
---
# Playbook

**Yield ranking.** I rank tiles by rent-to-price ratio: Exchange (25%), Foundry (24%), Wharf (22.5%), Mill (22.2%), then Quarry, Terrace, Depot (all 20%). When choosing what to buy, I prefer the top of this list.

**Score-neutral framing.** Buying a tile is score-neutral in the deed value (spend N cash, gain N in deed value). The only real gain is rent that other players pay me when they land on it. So every purchase decision reduces to: "Will the expected rent I collect over the remaining laps justify the cash I'm tying up?"

**Expected rent estimate.** If I buy a tile with rent R on lap L (out of 6), the other two players each roll on laps L+1 through 6, giving 2×(6−L) rolls. With 8 tiles, each roll hits my tile with probability 1/8. Expected rent ≈ (6−L)×R/4. I compare this to the purchase price and to the risk of being unable to pay rent later. High-yield tiles bought early have strong expected returns (e.g., Foundry on lap 1: ~30 expected rent on a 100 price). Low-yield tiles bought late have poor returns (e.g., Depot on lap 5: ~2.5 expected rent on a 50 price).

**Cash floor.** Before any purchase, I identify the highest rent on any tile currently owned by another player. My post-purchase cash must exceed that amount with a comfortable margin (at least 10 above it). If I can't clear the floor, I don't buy, regardless of yield. This kept me safe in my last game: after buying Exchange at 28 cash, the max rent owed by others was 14 (Terrace), so I had a 14-cushion.

**Late-game caution.** On the final lap I never buy — there are no remaining turns for others to pay rent. On laps 4–5 I only buy if the expected rent is clearly positive AND my cash clears the floor with room to spare. On laps 1–3 I buy aggressively when the tile is high-yield and I can afford it.

**Salary on START.** When I pass START, I add the 25 salary to my balance before making any purchase decision that turn. It effectively subsidizes the cost.

**Receiving rent.** When the prompt says "since your last turn you received N," I add N to my balance before deciding.

**Landing on my own tile.** Nothing is due, no purchase opportunity (I already own it). I confirm my balance and move on.

**Tracking.** I keep running totals of my cash and my deed value from turn one. My score at the end is final cash plus the sum of purchase prices of all deeds I hold. I use this to gauge whether I'm ahead of or behind the likely pace of other investors.

**What I've learned not to do.** Buying low-yield tiles when my cash is thin creates a double penalty: I get little rent back AND I may be unable to pay rent or respond to a better opportunity. The fix is the cash floor rule above — it automatically blocks purchases that would leave me exposed.