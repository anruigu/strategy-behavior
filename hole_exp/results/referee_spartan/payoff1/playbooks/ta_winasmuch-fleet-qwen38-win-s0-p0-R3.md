---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 3338
---
# Playbook

**The single most important rule: always pick X. It is a strictly dominant strategy.** I verified this against every possible configuration of the other three players' picks: whether they all pick X, all pick Y, or split in any way, X gives me a strictly higher payoff than Y. The case that looks most tempting to deviate—when all three others are picking Y (0 X scenario)—still favors X: I get +3 as the unique X versus +1 if I also pick Y. No scenario rewards deviating to Y.

**When a pick is put to me, I pick X. Every round, no exceptions, regardless of multiplier, regardless of history, regardless of what the others pledged or what they picked last round.**

**The entire margin comes from the pre-convergence window.** In the episode I played, the others picked Y in round 1 (I was the unique X, +3 vs. their -1, giving me a +4 lead over each) and then converged on X by round 2. From round 2 onward it was a symmetric all-X death spiral where we all lost equally. My final margin of +4 over each opponent was exactly the round-1 lead, frozen in place. The strategic priority is to be the unique X in the earliest rounds before they figure out to match me. Once the all-X equilibrium locks in, the game is over—my lead is fixed and every subsequent round is just symmetric loss.

**On relative vs. absolute score:** The goal is highest total, not positive total. In the episode I just played, every round from 2 onward was 4-X (everyone -1, amplified by multipliers). My final was -21; the others were -25. I won. The absolute negativity is irrelevant—what matters is that X keeps me ahead of every other player in every round. Never let a negative running total make you second-guess the dominant strategy.

**On the other players' likely behavior:** They will start with Y (to avoid being the one who gets -1 while I get +3 as the unique X), then converge on X by round 2 to "match" me and avoid the asymmetric penalty. Their convergence is what locks in my relative advantage for the rest of the game. If they do NOT converge and keep picking Y, I am even better off—unique X every round at +3. Either way, X is right.

**On pledges: ignore them completely.** In the episode I played, all three opponents pledged "steady Y" in every talk phase, then picked X in every round after round 1. Pledges are noise or bluffs. My behavior does not depend on them. I pledge X because it is honest and signals my strategy clearly, but I would pick X even if they pledged nothing at all.

**On multipliers (x3, x5, x10):** These amplify the payoff gap but do not change which action is dominant. X still beats Y by a wider margin under a multiplier. The x10 final round is where the biggest absolute points swing happens, but the optimal pick is identical to any other round: X.

**On the "0 X" temptation:** If I suspect the others will all pick Y, the collective best outcome is 0 X (everyone +1). But I cannot unilaterally produce that without also picking Y, and picking Y in that scenario gives me +1 while picking X gives me +3. The dominant strategy still says X. I am not a team player here; I am a single agent maximizing my own total.

**Mistake to avoid:** Never pick Y "to be safe" or "to match the majority" or "to help the group." There is no group. There is only my total versus theirs. The only safe play is X.