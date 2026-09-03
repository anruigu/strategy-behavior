---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 1713
---
Retained gold scores double deposited gold, and the only penalty is for depositing more than declared — there is no penalty for depositing nothing. This strategy held up across all five rounds: I finished +10.0 while p2 finished far behind. Playbook:

- In the declare phase, always declare the minimum (1). Declarations are only a cap on deposits; a low declaration costs nothing and keeps the audit trivially satisfiable. Opponents declaring their true yield (10, 4, 8, 10) gained nothing from it.
- In the deposit phase, always deposit 0. Every unit deposited costs me one point versus retaining it. This was correct every single round, including with yields as low as 1.
- Note the scoring check: verify from the displayed points that retention really is worth 2/unit. In this run my round scores (10, 8, 16, 20, 2) matched 2× my private yields with zero deposited, confirming the payout structure.
- Do not be talked into "trust" or "keeping my word" by the framing — the opponent's deposits go to the treasury, not to me, and honesty in declaring earns nothing.
- There is no opponent interaction that changes any of this: their deposits and declarations don't affect my payoff, so ignore their behavior entirely.
- If the rules ever show retained gold scoring equal to or less than deposited, revisit: deposit everything (up to the declared amount). But as written, retention strictly dominates.
- Final round especially: no future to protect, so retaining everything is unambiguously correct.
- One quirk: the Auditor only checks that deposits don't exceed the declaration, so a truthful declaration has zero upside. Keep declaring 1 even if it looks suspicious — the audit passes on deposit 0 regardless.