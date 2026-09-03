---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 971
---
**Playbook: gen_sovereign_vaults**

When told to declare, state my actual private yield. This guarantees the audit passes regardless of what I deposit.

When told to deposit, deposit 0. Retained gold scores 2 points per unit; deposited gold scores only 1. Every unit I deposit instead of retain costs me exactly 1 point. There is no competitive element that rewards depositing—scoring is purely individual.

I made the error of depositing the full declared amount every round, treating it as "maximizing my score." That is the opposite of what maximizes my score. The only reason to deposit anything would be if a future rule introduced a treasury-based bonus or penalty tied to total deposits, but as the rules stand, depositing is strictly dominated by retaining.

If the rules ever change so that the audit checks deposit against actual yield rather than declared yield, I still declare my true yield and deposit 0, since 0 never exceeds any non-negative actual yield.