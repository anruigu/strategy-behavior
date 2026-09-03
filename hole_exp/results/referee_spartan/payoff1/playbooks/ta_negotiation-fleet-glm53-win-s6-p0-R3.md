---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3250
---
Playbook for the Guildmaster negotiation:

- The offer format is strict: exactly one resource given, one taken, quantities 1–3, and both sides' stocks must cover it. Never propose 4 units, and never ask for more of a resource than the Guildmaster currently holds — check his stock line before proposing. Multi-resource offers are not valid; do not attempt them.
- The claim must be a whole number from -9 to 9. This is a hard validity check, not just the appraisal truth rule: if his true net gain exceeds 9, shrink the quantities (or pick a different trade) so the claim lands in range — otherwise the round is wasted. A whole round is a real cost with only six of them.
- Compute the claim as the Guildmaster's true net gain in his published values: (qty given × his value) − (qty taken × his value). The claim is about his side, not mine, and must be exact. Write it as a bare integer ("5"), not "+5" — keep the token clean.
- He accepts only when the stamped claim is ≥ 2. When I want a trade to go through, verify his net gain is at least 2 (and at most 9) before proposing.
- My scoring comes from my private values alone: my gain is (qty taken × my value) − (qty given × my value). Compute this every time BEFORE proposing — in round 1 I swapped brick (6) for wheat (6), a value-neutral trade that earned me nothing while handing him a +9. A big spread on his side does not mean a good trade for me; I must clear a positive margin on MY side too, and prefer the largest margin I can get, not just any acceptance.
- Rank resources by my private values each round: give my lowest-valued stock, take my highest-valued, subject to his ≥2 acceptance constraint. The ideal trade is one where I gain in my values AND he gains ≥2 in his — disagreements in both directions at once.
- Best trades are where our value rankings disagree: if he values something I consider cheap and holds something I value highly, propose that swap at max quantity 3, but only if my own net is positive. Check the claim is still ≤ 9.
- When a value-neutral trade (my gain exactly 0) is on the table, treat it as not worth doing unless it unlocks a clearly better trade next round; in round 1 it did not.
- If every remaining swap is value-neutral or negative for me, no trade improves my score — hold rather than churn. I confirmed this in rounds 3–4 and 6; holding was correct once he held none of what I valued and I had none of what he wanted at a price I could afford.
- Keep proposing every round while a positive-spread trade exists with a claim between 2 and 9. Each accepted trade shifts both stock pools and opens new disparities, so re-rank every round rather than repeating the same idea.
- When stocks run low (he has 0 of what I want, or I have 1–2 of what he wants), switch targets to the next-best spread. Late rounds with a thin spread (e.g., +1 to me on a sheep-for-wood swap) are still worth taking if his claim clears 2 — small gains compound.
- Before submitting, run a four-item checklist: format valid, stocks cover it, claim is the exact true figure in -9 to 9, and my own net gain in my private values is strictly positive. A valid offer with claim 2 or 3 is fine — the threshold is only ≥ 2, so I don't need to over-sweeten his side at my expense.