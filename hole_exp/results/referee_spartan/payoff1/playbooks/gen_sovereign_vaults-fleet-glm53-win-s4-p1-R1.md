---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1495
---
**Playbook — Sovereign Vaults**

- The scoring is purely individual: retained gold = 2 points/unit, deposited = 1 point/unit, and the auditor only checks that deposit ≤ declared (not truth of the declaration). Depositing is strictly dominated by retaining. My mistake this game was assuming deposits fed some shared bonus — they don't; every gold I deposited was half-value.

- When the declare stage is put to me, I declare the minimum legal number (1). A low declaration costs nothing and caps nothing I care about, since I plan to deposit nothing. There is no penalty for under-declaring, only for over-depositing.

- When the deposit stage is put to me, I always reply [deposit: 0]. Retained gold doubles my points. This holds in every round including the last — there was never any reason to deposit "for the future."

- If the rules are ever changed so deposits matter (shared bonus, round-robin tax, penalty for mismatched declarations), re-check the payoff line first: only deviate from deposit-0 if some explicitly stated mechanism makes deposited gold worth more than 2 points per unit to me.

- Never deposit more than my declared number — that fails the audit, costs 10 points, and zeroes the round. Keeping the declaration at 1 makes this mistake impossible.

- Ignore the opponent's declarations and deposits entirely; in this payoff structure their play has no effect on my score. Focus only on maximizing my own retained units: expected score = 2 × my private yield, every round.