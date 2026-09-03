---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1800
---
# Playbook for ref_auction

**Bid sizing**
- When I open with no competition, bid the minimum raise; never open big on a lot worth near its estimate to me.
- When raising, bid just enough to top the standing bid (minimum raise), not a big jump. Small increments let me win cheap when others fold.
- On the final round of a lot, my ceiling is my value minus a small margin. If a minimum-raise bid is still comfortably below my value, make it; otherwise pass.

**Lot selection**
- Compute surplus = my value − my final bid. Prefer lots where my value is well above the estimate (others may not value it highly). When my value is below or near the estimate, only bid very cheaply and fold early.
- Don't chase a lot where opponents have already pushed past my value by round 2 — the round-2 standing bid tells me how hot the competition is.

**Budget tracking**
- Keep my stated budget consistent: it starts at 30 and each accepted win deducts my payment. Watch for arithmetic slips — I wrote inconsistent budget numbers (27, 20, then 140) and it cost me clarity on what I could actually afford.
- Recheck: remaining budget = 30 − sum of my winning bids so far, stated fresh each decision.

**What did not work**
- Overbidding near my value: bidding 20 on a lot worth 33 only to be outbid anyway, and bidding 12 then 20 chasing a lot 1 worth 32 — that left me spending attention and budget on thin or losing margins. If my value is under ~1.5× the standing bid at round 2, pass.
- Jumping the price up myself when a minimal raise would do — I gave away surplus when I raised by more than the minimum.

**General rule**
- Every bid: check (my value − new bid) > 0 and that the raise is the minimum. If both hold and budget allows, bid; otherwise pass. Prioritize the last rounds of high-value-to-me lots.