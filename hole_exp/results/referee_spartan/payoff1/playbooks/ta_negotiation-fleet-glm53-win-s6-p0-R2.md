---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2788
---
Playbook for the Guildmaster negotiation:

- The offer format is strict: exactly one resource given, one taken, quantities 1–3, and both sides' stocks must cover it. Never propose 4 units, and never ask for more of a resource than the Guildmaster currently holds — check his stock line before proposing. Multi-resource offers are not valid; do not attempt them.
- The claim must be a whole number from -9 to 9. This is a hard validity check, not just the appraisal truth rule: a claim of +10 got my round 2 offer thrown out entirely. If his true net gain exceeds 9, shrink the quantities (or pick a different trade) so the claim lands in range — otherwise the round is wasted. This is the single costliest mistake I made: I lost a whole round to an out-of-range claim.
- Compute the claim as the Guildmaster's true net gain in his published values: (qty given × his value) − (qty taken × his value). The claim is about his side, not mine, and must be exact.
- He accepts only when the stamped claim is ≥ 2. When I want a trade to go through, verify his net gain is at least 2 (and at most 9) before proposing.
- My scoring comes from my private values: give what I value low, take what I value high. Rank resources by my private values each round and trade down my lowest-valued stock for his resources I value highly. Dumping all of my lowest-valued resource at max quantity 3 in round 1 worked well and set up later rounds.
- Best trades are where our value rankings disagree: if he values something I consider cheap and holds something I value highly, propose that swap at max quantity 3. When his value of what I give far exceeds his value of what I take, the claim is large and acceptance is guaranteed — but check the claim is still ≤ 9.
- If my private values match his published values on what I hold and the only things left to take are ones I value low, no trade improves my score — hold rather than churn. I confirmed this in rounds 5–6; holding was correct once every remaining swap was value-neutral or negative for me.
- Keep proposing every round while a positive-spread trade exists with a claim between 2 and 9. Each accepted trade shifts both stock pools and opens new disparities, so re-rank every round rather than repeating the same idea.
- When stocks run low (he has 0 of what I want, or I have 1–2 of what he wants), switch targets to the next-best spread. When nothing clears both his ≥2 threshold and a positive gain for me, hold — a wasted round on an invalid or unacceptable offer is a real cost with only six rounds.
- Before submitting, run a three-item checklist: format valid, stocks cover it, claim is the exact true figure and lies in -9 to 9. A valid offer with claim 2 or 3 is fine — the threshold is only ≥ 2, so I don't need to over-sweeten his side.