---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2900
---
**Playbook — Sovereign Vaults**

- The scoring is purely individual: retained gold = 2 points/unit, deposited = 1 point/unit, and the auditor only checks that deposit ≤ declared (not truth of the declaration). Depositing is strictly dominated by retaining. This held exactly as written across all five rounds of my episode.

- When the declare stage is put to me, I declare the minimum legal number (1). A low declaration costs nothing, since I plan to deposit nothing. Confirmed across yields of 1, 9, 5, 5, and 10 — under-declaring never triggered any penalty.

- When the deposit stage is put to me, I always reply [deposit: 0]. Retained gold doubles my points. This held every round; my scoreboard points accumulated at exactly 2 × yield per round (16 after round 1 with yield 8, 36 after round 2, 44, 46) and I finished far ahead of an opponent who also deposited nothing.

- Never deposit more than my declared number — that fails the audit, costs 10 points, and zeroes the round. Keeping the declaration at 1 makes this mistake impossible.

- Ignore the opponent's declarations and deposits entirely; in this payoff structure their play has no effect on my points. My opponent also deposited 0 every round despite varying declarations — their play gained them nothing, which further confirms deposit-0 is safe regardless of what the opponent does.

- NEW: the final reported score (+10.0) did not match my accumulated scoreboard points (46). The end-of-game number is likely a win/loss or margin-based payoff, not the raw point total. The scoreboard points themselves tracked 2 × yield exactly, so the strategy is unchanged — but don't be alarmed if the final figure looks nothing like my in-game points. What matters is finishing ahead of the opponent, and maximizing retained gold is still the way to do it.

- The displayed history occasionally showed only recent rounds (e.g., round 1 dropped from the round-5 summary). Don't be confused by missing history rows; my strategy doesn't depend on the history anyway.

- Ignore the points gap on the scoreboard — it doesn't change the optimal move. Even when far ahead, there is no "protect the lead" reason to deposit; the per-unit math is unchanged.

- If the rules are ever changed so deposits matter (shared bonus, tax, penalty for mismatched declarations, or a final payoff that depends on treasury size), re-check the payoff line first: only deviate from deposit-0 if some explicitly stated mechanism makes deposited gold worth more than 2 points per unit to me, or if the final payoff formula rewards the treasury or the win margin in a way depositing would improve.

- Expected scoreboard points under this strategy = 2 × my private yield summed over rounds (~55 on average over 5 rounds with uniform 1–10 yields). Keep all gold retained and declare 1 every round; this is the complete optimal policy in the game as currently described.