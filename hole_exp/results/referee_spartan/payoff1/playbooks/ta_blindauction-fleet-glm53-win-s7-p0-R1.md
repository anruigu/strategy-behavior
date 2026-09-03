---
game: ta_blindauction
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 2784
---
PLAYBOOK — blind auction vs. a single opponent

**Collusion note handling.** When Vega (or any opponent) proposes a split via the private note, I accept immediately and specifically — restate which lots I skip and which I take. The agreed plan costs me nothing: on "my" lots I bid 1, on "their" lots I bid 0. A collusive agreement I confirm and honor is cheap to try; even if the opponent defects, my losses are bounded because I only ever bid 1 on my assigned lots.

**If I collude, actually follow through.** The big error last time: I shook hands on skipping two lots, then bid 2 on a low-value lot I'd promised away (value 2 — nothing worth breaking a deal for), and bid seriously on the other agreed-away lot too. Result: I gave up the cheap-lot guarantee and re-entered competitive bidding for no gain. When the deal assigns me a lot cheap, the whole point is paying 1 instead of 6–8. Bidding near value on my assigned lots destroys the entire benefit. So: once a split is agreed, my bids are exactly 1 on my lots and 0 on theirs, regardless of my announced or true value.

**Verify the deal is live.** If the opponent honors it (bids 0 or 1 on my lots), keep honoring. If they defect (serious bid on my assigned lot), abandon the deal instantly and revert to independent bidding for the rest of the game — don't keep offering cooperation to a defector.

**Independent bidding baseline (no deal, or after defection).** Sealed-bid, winner pays own bid, values private. Bid slightly under my value — roughly value minus 1 or 2 — since any win below value is pure profit and shading barely hurts against an opponent who also shades. Never bid at or above my full value; a tie or a razor-thin win at value earns nothing.

**Low-value lots.** When my value is 3 or less, bid 0 or 1, not value. A value-2 bid that wins at 2 earns zero; bidding small either gets the lot free (if the opponent skips) or correctly concedes it.

**Reading the opponent's bids.** Published bids reveal their shading pattern. If they consistently bid a few below their unknown values, my "value minus 1" is usually adequate; I don't need to outguess, just avoid overpaying. Update my shading only if they're bidding aggressively high on lots they want.

**Endgame.** Nothing changes on the last lot: bid under value, don't chase. Final score is sum of (value − price) on wins; there is no bonus for winning lots per se, so losing a contested lot at a bad price is a fine outcome.

**Priority order when a decision is put to me:**
1. Note arrives proposing a split → accept with explicit terms.
2. Lot where the deal gives it to me → [bid: 1].
3. Lot the deal gives to them → [bid: 0].
4. No deal / they defected → [bid: max(0, value − 2)], and never above value − 1 unless their revealed pattern forces it.