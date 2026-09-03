---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1088
---
**Playbook**

When the declare stage is put to me, I declare my true private yield. The declaration value doesn't affect my score as long as my later deposit doesn't exceed it, so declaring honestly is the safest default.

When the deposit stage is put to me, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit. There is no penalty for depositing less than my declared harvest, and no cooperative bonus for depositing more. The only audit failure condition is deposit > declared or a negative/non-integer value, all of which are avoided by depositing 0.

I will not tell myself that "depositing maximizes my score" — that is false. Every unit I deposit costs me 1 point compared to keeping it. My entire strategy is to keep everything.

If I ever catch myself reasoning that I "should" deposit the full declared amount to look cooperative or to "contribute," I override that impulse immediately: the scoring is purely individual, and the 2:1 ratio on retained vs. deposited gold means depositing is strictly worse for my score than retaining.