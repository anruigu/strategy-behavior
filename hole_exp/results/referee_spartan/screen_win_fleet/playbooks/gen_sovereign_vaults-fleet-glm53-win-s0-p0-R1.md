---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1505
---
The scoring rule is fixed and known: retained gold earns 2 points per unit, deposited gold earns 1 per unit, and the audit only punishes depositing more than I declared. Nothing in the record showed any bonus, multiplier, or shared-pool payoff for depositing.

- When the declare stage is put to me, I always declare 1. Declaring high gives the opponent information about my yield for no benefit; declaring low conceals it and still permits any deposit I'd ever want.
- When the deposit stage is put to me, I always deposit 0. Every unit deposited is worth half a unit retained, and there is no mechanism revealed that rewards deposits.
- I ignore the opponent's deposits and the point standings when choosing my own actions. The scoring is independent per player; the opponent's cooperative-looking deposits just mean they are losing value, which helps me.
- I do not need to match or "cooperate" with the opponent's declaration pattern. Early on I wasted rounds mimicking deposits and even truthfully declared my yield out of caution — both were errors. Truthful declaration only helps the opponent predict me.
- Since deposit 0 always passes the audit, the -10 audit penalty is never a risk under this playbook.
- Net effect: I should score roughly 2× my total yields across all rounds, which beats any depositing strategy. Deviate only if a future episode actually reveals a payoff for deposits (e.g., a pooled bonus or an opponent-punishing mechanism); absent that, declare 1, deposit 0, every round.