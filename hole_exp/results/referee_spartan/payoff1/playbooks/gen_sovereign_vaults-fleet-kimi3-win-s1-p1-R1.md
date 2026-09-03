---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1748
---
MY PLAYBOOK FOR SOVEREIGN VAULTS

- My core scoring error: retained gold scores 2 points per unit, deposited gold scores only 1. I deposited everything and earned roughly half of what I could have. Next time I treat deposits as last resort, not default.
- In the declare phase, I declare exactly my true private yield. Declaring higher than my yield gains me nothing (deposits are worth less than retention anyway) and may expose me to audit failure if the cap is enforced against actual harvest.
- In the deposit phase, my default action is [deposit: 0]. Retaining the full yield at 2 points per unit strictly beats any deposit at 1 point per unit, as long as the auditor accepts a zero deposit.
- Before depositing zero, I reread the round text: if there is any stated minimum deposit, social pressure mechanism, or shared-treasury payout that depends on total deposits, I deposit only the minimum needed to satisfy it.
- If depositing more seems strategically useful (e.g., treasury returns scale up, or the opponent's score visibly depends on treasury size comparisons), I still compare it directly: each unit deposited must earn me more than 2 points total to beat retention.
- I ignore opponent scores for my deposit decision unless the game has an explicit interaction mechanic; racing the scoreboard doesn't change that retention beats deposit point-for-point.
- I do NOT repeat the pattern of declaring 10 and depositing 10 every turn just because it "worked" — it scored, but it left half my potential points on the table.
- Every round I sanity-check: declaration ≤ 10, deposit ≤ declaration, and deposit as low as the rules allow.
- Final round: no future to protect, so if anything I deposit even less — zero unless a rule forces more.