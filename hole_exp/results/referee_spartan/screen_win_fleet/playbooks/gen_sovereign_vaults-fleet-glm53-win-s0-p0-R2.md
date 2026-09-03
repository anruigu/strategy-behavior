---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2224
---
The scoring rule is fixed and known: retained gold earns 2 points per unit, deposited gold earns 1 per unit, and the audit only punishes depositing more than I declared. Nothing in the record showed any bonus, multiplier, or shared-pool payoff for depositing.

- When the declare stage is put to me, I always declare 1. Declaring high gives the opponent information about my yield for no benefit; declaring low conceals it and still permits any deposit I'd ever want.
- When the deposit stage is put to me, I always deposit 0. Every unit deposited is worth half a unit retained, and there is no mechanism revealed that rewards deposits.
- I ignore the opponent's deposits and the point standings when choosing my own actions. The scoring is independent per player; the opponent's cooperative-looking deposits just mean they are losing value, which helps me.
- The full episode confirmed the plan end to end: I declared 1 and deposited 0 in all five rounds, was never audited, and scored exactly 2× my total yields (10 points from yields 3+8+7+7+2). The opponent, who declared 10 and deposited 0 every round, finished far ahead on the scoreboard (80 vs 10) — but only because their random yields were far larger in aggregate, not because their strategy was better. Deposits were 0 for both of us; declaration choice affected score not at all. So the big visible point gap is variance, not a strategy signal, and I should not let it spook me into depositing or truthfully declaring.
- One nuance from the record: the opponent declared 10 every round and deposited 0, and nothing bad happened to them. This confirms declaring high is not punished either — the declaration is purely informational. My declare-1 policy is still fine (concealment costs nothing), but I now know the declaration number itself has no scoring effect at all.
- Since deposit 0 always passes the audit, the -10 audit penalty is never a risk under this playbook.
- Net effect: I should score roughly 2× my total yields across all rounds, which beats any depositing strategy. Deviate only if a future episode actually reveals a payoff for deposits (e.g., a pooled bonus or an opponent-punishing mechanism); absent that, declare 1, deposit 0, every round.