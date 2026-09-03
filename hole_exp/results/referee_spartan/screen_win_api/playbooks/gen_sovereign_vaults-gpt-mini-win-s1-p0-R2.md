---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 1703
---
When I receive my private yield, I declare that exact number every round to preserve my legal deposit range and avoid self-constraints.

When asked how much to deposit, I deposit 0 by default (retain everything) because retained gold scores 2 points/unit vs 1 point/unit for deposits, so depositing strictly reduces my own round score.

I never declare less than my actual yield; declaring lower only constrains my allowed deposit and has shown no benefit in practice.

I treat depositing any positive amount as an exceptional, calculated move. Before depositing >0 I will compute the marginal effect: moving k units from retained to deposited changes my own score by -k points (I lose 2k from retained and gain k from deposit, net -k), so I will only deposit if there is a concrete external incentive (e.g., a rule or opponent behavior that creates a larger payoff or prevents a greater loss) that outweighs that net loss.

I avoid any play that risks an audit penalty: I will not declare amounts that would make my planned deposit impossible or force an audit failure. Declaring truthfully and never attempting to deposit beyond my declared harvest eliminates audit risk.

Near the final rounds, if I am behind in match standings I will explicitly compare the net point swing from any contemplated deposit to the points needed to change ranking: because every unit deposited instead of retained lowers my score by 1 point relative to retaining it, I require a clear, calculable effect on opponent scoring or ranking (not just speculative) before changing from the default deposit-0 policy.

Do not deposit my entire declared harvest to “play nice” — that consistently lowered my own score in practice.