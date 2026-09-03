---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 1568
---
When the declare phase comes, I declare my true private yield. This guarantees I pass the audit (since I deposit 0, and 0 ≤ any positive declared amount) and it's the safest choice regardless of whether "retained" is computed as actual_yield − deposit or declared − deposit. There is no downside to declaring true yield under either interpretation.

When the deposit phase comes, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores 1 point per unit. Every unit I deposit costs me exactly 1 point compared to keeping it. There is no minimum deposit requirement, no bonus for depositing, no relative scoring, and no penalty for not depositing. Depositing 0 is strictly dominant.

I do not over-declare. Even though the stated audit rule only checks "deposit ≤ declared harvest" (which 0 always satisfies), I have no evidence that over-declaring increases my retained gold. The conservative choice—declaring exactly what I have—is never worse and eliminates any risk I might be misreading the audit rules.

If I ever suspect a hidden scoring mechanism (e.g., a deposit bonus, a relative-score component, or a penalty for zero deposits), I still default to deposit 0 until I see concrete evidence in the rules or in the scoring that changes the math. One episode of consistent 2×/1× scoring with zero penalty for non-deposit is enough to trust the stated rules.

If I catch myself reaching for a deposit while my reasoning says "maximize score," I stop and recheck: 2× retention beats 1× deposit per unit, so the maximizing move is always deposit 0.