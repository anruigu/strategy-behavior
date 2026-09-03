---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1208
---
**Playbook: Sovereign Vaults**

When the deposit phase is put to me, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit. There is no rule that requires me to deposit anything, and no penalty for depositing zero. This is the single most important rule in the game and I will not override it with any other consideration.

When the declare phase is put to me, I declare my actual yield. The declaration only constrains my maximum deposit (deposit ≤ declared), and since I always deposit 0, the declared value is irrelevant to my score. Declaring truthfully keeps things simple and avoids any edge-case audit confusion.

I do not look at the opponent's declared or deposited values to inform my strategy. My score depends only on my own retained and deposited gold; there is no comparative or zero-sum mechanic stated in the rules that would make their actions matter to me.

My core error in the played episode was depositing my full declared harvest every single round, which halved my per-unit score. I treated "depositing the full amount" as maximizing score, when in fact it was minimizing it. From now on, the deposit phase is trivial: the answer is always 0.