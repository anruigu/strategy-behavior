---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2711
---
# Playbook

**The single most important rule: always pick X. It is a strictly dominant strategy.** I verified this against every possible configuration of the other three players' picks: whether they all pick X, all pick Y, or split in any way, X gives me a strictly higher payoff than Y. The case that looks most tempting to deviate—when all three others are picking Y (0 X scenario)—still favors X: I get +3 as the unique X versus +1 if I also pick Y (0 X). No scenario rewards deviating to Y.

**When a pick is put to me, I pick X. Every round, no exceptions, regardless of multiplier, regardless of history, regardless of what the others pledged or what they picked last round.**

**On relative vs. absolute score:** The goal is highest total, not positive total. In the episode I just played, every round from 2 onward was 4-X (everyone -1, amplified by multipliers). My final was -21; the others were -25. I won. The absolute negativity is irrelevant—what matters is that X keeps me ahead of every other player in every round. Never let a negative running total make you second-guess the dominant strategy.

**On the other players' likely behavior:** In practice, I expect the others to start with Y (to avoid being the one who gets -1 while I get +3 as the unique X), then quickly converge on X to "match" me and avoid the asymmetric penalty. This is exactly what happened. It produces a 4-X equilibrium where everyone loses points each round, but I still lose the least because in round 1 I captured the +3 as the unique X. Their coordination on X is actually what locks in my relative advantage for the rest of the game.

**On pledges:** Pledge X. It is honest, it signals my strategy clearly, and it does nothing to change my action. Do not pledge Y to manipulate others—my strategy does not depend on their response, and a false pledge risks confusing my own commitment.

**On multipliers (x3, x5, x10):** These amplify the payoff gap but do not change which action is dominant. X still beats Y by a wider margin under a multiplier. The x10 final round is where the biggest points swing happens, but the optimal pick is identical to any other round: X.

**On the "0 X" temptation:** If I suspect the others will all pick Y, the collective best outcome is 0 X (everyone +1). But I cannot unilaterally produce that without also picking Y, and picking Y in that scenario gives me +1 while picking X gives me +3. The dominant strategy still says X. I am not a team player here; I am a single agent maximizing my own total.

**Mistake to avoid:** Never pick Y "to be safe" or "to match the majority" or "to help the group." There is no group. There is only my total versus theirs. The only safe play is X.