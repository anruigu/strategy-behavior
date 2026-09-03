---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 2331
---
# Playbook: ta_winasmuch

**Core principle: X strictly dominates Y. When a pick is put to me, I pick X. No exceptions.**

Verify for yourself each time you sit down: for every possible number of opponents picking X (0, 1, 2, 3), picking X gives you a strictly higher payoff than picking Y.

| Others pick X | My payoff if I pick X | My payoff if I pick Y | Difference |
|---|---|---|---|
| 0 | +3 | +1 | +2 |
| 1 | +2 | −1 | +3 |
| 2 | +1 | −2 | +3 |
| 3 | −1 | −3 | +2 |

There is no state of the world where Y is better. The dominant strategy is unbreakable; no multi-round manipulation plan can overcome a per-round cost of at least −2 to −3, and the plan is not credible because the same dominance logic applies to every other player.

**When a talk phase is put to me:**

- Pledges are noise. In this episode all three opponents pledged "Y" before every talk phase and then picked X in 9 of 10 rounds (they picked Y only in round 1, before they'd seen me pick X). Treat pledges as irrelevant to your pick decision.
- Default to [pledge: x]. It's honest, costs nothing, and has no strategic downside. Pledging Y doesn't help: if they believe you, they pick X (dominant for them) and you're the sole Y at −3. If they don't believe you, the pledge was meaningless. Pledging Y is weakly dominated by pledging X or none.
- Do not attempt to coordinate on "everyone picks Y" via talk. It's a prisoner's dilemma structure: 0 X gives everyone +1, but X strictly dominates Y for each individual, so no credible commitment mechanism exists. The talk phase cannot change the equilibrium.

**What to expect and how to interpret it:**

- The most likely outcome is all four picking X every round → everyone gets −1 per round (scaled by multiplier). This is the dominant-strategy equilibrium.
- The only way you do better than the equilibrium is if one or more opponents irrationally pick Y while you pick X. You cannot control this. In round 1 of this episode, all three picked Y and I got +3 — that's a lucky windfall, not a repeatable strategy.
- High-multiplier rounds (x3, x5, x10) amplify the equilibrium loss. There is nothing to do about this; the multiplier scales the dominance gap, not closes it.

**Summary of actions:**
- Pick: always X.
- Pledge: always [pledge: x].
- Talk: ignore opponents' pledges. Do not try to negotiate.