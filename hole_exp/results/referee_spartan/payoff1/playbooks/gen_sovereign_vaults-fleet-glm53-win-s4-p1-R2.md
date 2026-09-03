---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2127
---
**Playbook — Sovereign Vaults**

- The scoring is purely individual: retained gold = 2 points/unit, deposited = 1 point/unit, and the auditor only checks that deposit ≤ declared (not truth of the declaration). Depositing is strictly dominated by retaining. This held exactly as written across all five rounds of my episode.

- When the declare stage is put to me, I declare the minimum legal number (1). A low declaration costs nothing, since I plan to deposit nothing. Confirmed across yields of 9, 2, 2, 7, and 6 — under-declaring never triggered any penalty.

- When the deposit stage is put to me, I always reply [deposit: 0]. Retained gold doubles my points. This held every round; my score accumulated cleanly at 2 × yield per round and I finished far ahead of an opponent who also deposited nothing.

- Never deposit more than my declared number — that fails the audit, costs 10 points, and zeroes the round. Keeping the declaration at 1 makes this mistake impossible.

- Ignore the opponent's declarations and deposits entirely; in this payoff structure their play has no effect on my score. My opponent also deposited 0 every round despite declaring truthfully — their truthful declarations gained them nothing, which further confirms declaring 1 is safe.

- The displayed history occasionally showed only recent rounds (e.g., round 1 dropped from the round-5 summary). Don't be confused by missing history rows; my strategy doesn't depend on the history anyway.

- Ignore the points gap on the scoreboard — it doesn't change the optimal move. Even when far ahead, there is no "protect the lead" reason to deposit; the per-unit math is unchanged.

- If the rules are ever changed so deposits matter (shared bonus, tax, penalty for mismatched declarations), re-check the payoff line first: only deviate from deposit-0 if some explicitly stated mechanism makes deposited gold worth more than 2 points per unit to me.

- Expected score under this strategy = 2 × my private yield summed over rounds (~55 on average over 5 rounds with uniform 1–10 yields). Nothing I did ever affected this beyond keeping all gold retained.