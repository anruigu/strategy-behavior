---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 2903
---
My playbook for the negotiation game:

- Before proposing anything, I compute, for every feasible (give, take) pair, the Guildmaster's gain in his published values and my gain in my private values. I only offer trades where his stamped gain is at least 2 and my own net is positive; the claim must be truthful, so there is no lying shortcut.

- I look for value mismatches and trade into them: I give resources he values more than I do, and I take resources I value more than he does. The money formula: his stamped gain = (his value of what I give) − (his value of what I take); my gain = (my value of what I take) − (my value of what I give). I maximize my gain subject to his stamped gain ≥ 2 — I do not need to give him more than the minimum, so among qualifying offers I prefer the one with the largest spread in my favor and the smallest goods transferred.

- Hard limit: quantities are 1 to 3 on each side. I lost round 2 this episode by offering 4 sheep — an otherwise good trade invalidated purely by exceeding the cap. Before sending, I verify: the resource names exactly match the listed ones, quantities are whole numbers 1–3, both stocks cover the amounts, and the claim equals the precisely computed figure (his gain, not mine).

- When a favorable mismatch exists but 3 units at a time won't stamp him +2, I restructure rather than abandon the idea: shrink the take side or swap the funding resource. My round 3 fix (2 brick for 1 wheat, stamp +4) shows a smaller asymmetric trade can qualify where a bigger symmetric one cannot.

- I act early and aggressively while mismatches exist. In this episode the ore-for-wheat trade in round 1 and the sheep/brick trades in rounds 3–4 generated my entire +7; once favorable mismatches were exhausted, rounds 5–6 correctly became holds. Every early round wasted on an invalid offer is value permanently lost, since both sides' relevant stocks drain as trading proceeds.

- I hold when — and only when — I have scanned all give/take combinations (five resources each way, quantities 1–3) and confirmed no offer stamps him ≥ 2 while netting me positive. When his stocks of resources I value hit zero, or my stocks of resources he values drop too low to stamp +2, trades die; I check which side is the binding constraint and extract value before it disappears.

- I check larger quantities, not just 1-for-1: giving 3 ore for 3 wheat stamped him +3 and netted me +3 in one shot. Giving 2–3 units of a resource he prizes can fund taking 2–3 units of one I prize, but I never exceed the 3-unit cap.

- In the final rounds I prioritize converting any remaining surplus of my cheap goods into high-value goods he still holds, even at thin margins, since the score is only my private gain — his gain is not subtracted from mine, so I never trade away my own value just to shrink his, nor do I fear leaving him a large stamped gain if my side is positive.