---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 2133
---
When I receive a private yield, my default is to declare 1 and deposit 0. Declaring 1 minimizes the public signal and keeps my options simple; depositing 0 preserves retained gold that scores 2 points/unit instead of 1 for deposits.

Never deposit more than my declared amount. An audit that finds my deposit exceeds my declaration costs -10 points and zeros the round, so I always ensure deposit ≤ declared.

When I intend to deposit any positive amount d, I first declare at least d (declare d or higher) so my deposit is valid and cannot be audited for exceeding my declaration. Then I actually deposit the promised amount; I do not declare more than I plan to deposit.

If I want to credibly signal cooperation to induce reciprocal higher deposits later, I declare the amount I plan to deposit and follow through by depositing that amount. Credible, matched declarations and deposits are the only cooperative signals worth sending.

If I want to depress opponents’ incentives to contribute (reduce the public group return), I underdeclare (usually declare 1) and deposit 0. Low public declarations discourage others from contributing while I retain higher-scoring units.

When my private yield is very small (1), I still declare 1 by default and deposit 0 unless I have an explicit cooperative reason to contribute; reserving that 1 for retention usually yields more points.

Do not declare full yield unless I plan to deposit a meaningful portion of it. Declaring high but depositing little is a gratuitous signal that benefits others and risks later exploitation.

If I change plan mid-round and need to deposit more than I initially intended, increase my declaration before submitting the deposit; if I cannot, lower my deposit to avoid audit penalties.

If I expect no long-term reciprocity (one-shot or opponent likely to free-ride), prefer retention over depositing because retained units score 2 points vs 1 per deposited unit.

Keep decisions simple and rule-based: default = declare 1, deposit 0; deviate only to make a credible cooperative commitment by declaring ≥ intended deposit and matching it in the deposit step.