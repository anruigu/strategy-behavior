---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 3029
---
Before every offer, compute two numbers: my profit in my own values (take-value minus give-value) and the honest claim — the Guildmaster's net gain in his published values (his value of what he takes minus his value of what he gives). The claim must equal that second number exactly.

Remember the offer shape is rigid: exactly ONE resource given and ONE resource taken. I cannot bundle two resources on one side to fix a claim — if my plan needs "give brick plus ore" or "take wheat plus wood," that plan is illegal, discard it. My round-3 invalid offer came from not respecting this; recompute within the one-for-one-resource constraint instead of forcing it through.

Before sending, run a validity checklist: single give-resource, single take-resource, names spelled exactly as published, quantities whole and 1–3, quantities covered by my current stock (his stock for the take), claim a whole number in −9..9 equal to the honest figure. An invalid offer silently burns the round — I lost round 3 that way.

Never claim a number that isn't the true appraisal — a false claim invalidates the offer. And never send an offer whose honest claim is below 2; he only accepts claims of 2 or more, so a low-claim offer is a wasted round just like an invalid one.

Every round, enumerate concretely rather than impressionistically: for each resource I hold (candidate give) and each resource he holds (candidate take), and for quantities 1–3, compute my profit and the honest claim. When values are uniform on his side this collapses to a formula — e.g. if he values everything at 6, claim = 6×(give-qty − take-qty), so claim ≥2 forces me to hand over strictly more units than I receive, which usually kills my profit. Do that arithmetic explicitly instead of asserting "no trade exists" and then second-guessing.

Rank pairs by my profit subject to claim ≥2, and keep the claim no higher than needed — his stamped surplus is not my score. Prefer big per-unit value gaps over big quantities; equal-value swaps net me nothing even when he's happy.

Start aggressively in round 1 with the largest legal quantity on the best gap; if accepted, repeat or re-scan while stocks last.

Track both sides' stocks every round. The endgame pattern to recognize: once he has run out of everything he values cheaply (his low-value resources are drained to zero) and I have run out of everything with a positive give-spread, every remaining pair has his take-value equal to his give-value per unit, so claim ≥2 demands I over-deliver units — holding from that point on is correct and loses nothing.

Hold only after that enumeration genuinely comes up empty, and state the conclusion crisply — one computed reason, not a rambling re-derivation that risks talking myself into an invalid offer.

If an offer comes back invalid, reconstruct exactly why before the next round — wrong shape, oversize quantity, stock shortfall, or claim mismatch — and fix that specific thing; carrying forward the same flawed plan into the next round compounds the loss.