---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1332
---
When I compute my score each round, I do it as 2×(declared−deposited) + 1×deposited, so every unit I deposit costs me 1 point compared to retaining it.

When the deposit stage is put to me, I deposit 0. Retained gold scores 2 per unit, deposited gold only 1, and there is no reward or requirement tied to depositing — the treasury gives me nothing back.

When the declare stage is put to me, I declare 10 regardless of my actual yield, because declaring high costs nothing (the declaration is not audited against the true yield, only the deposit is checked against the declaration) and it keeps open the option to deposit if the rules ever reward it.

I never hedge deposits "to be safe" — there is no audit risk as long as deposit ≤ declared, so any positive deposit is pure point loss.

I ignore the opponent's score when choosing my deposit; their depositing heavily is them bleeding points, not a threat I need to match.

I do not change strategy in late rounds or when trailing — since trailing was caused by my own over-depositing, the fix is to stop depositing, not to deposit more "to catch up."

What did not work: depositing the full declared amount every round, and reasoning that deposits "maximize points if credited" — they are credited at half the rate of retention, which is how I fell behind despite declaring high.