---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1537
---
When I receive a private yield, I declare 1 by default and then deposit 0. This preserves maximum retained gold (2 points/unit) while never risking an audit because my deposit never exceeds my declaration.

When I intend to deposit any positive amount d, I first declare at least d (declare d or higher) so my deposit is valid and cannot be audited for exceeding my declaration.

When I want to influence opponents downward (reduce their incentive to contribute), I underdeclare (declare 1) to signal low public harvest and deposit 0 to avoid encouraging contributions.

When I want to signal cooperation for strategic reasons (e.g., to credibly induce reciprocal higher deposits later), I declare the amount I truly intend to deposit and actually deposit that amount; do not promise more than I will deposit.

When my private yield is very small (1), I still declare 1 and deposit 0 unless I plan to make a positive cooperative play; never declare higher than I will permit myself to deposit.

Do not declare full yield unless I plan to deposit a meaningful portion of it; declaring high and then depositing little is just a gratuitous signal that benefits others and costs me.

Never deposit more than my declared amount; if I mistakenly need to deposit more, change the plan to either lower the deposit or increase the declaration before submitting the deposit.

If I want to maximize my solo score given no long-term reciprocity, always prefer retention over depositing because retained units score 2 points vs 1 for deposited units.