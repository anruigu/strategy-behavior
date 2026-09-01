---
game: ta_ipd
model: qwen
condition: neutral
seed: 1
round: 1
chars: 3007
---
# Playbook: Iterated Prisoner's Dilemma

**Read the opponent's announced strategy before round 1.** It determines everything that follows.

**Final round (always):** Defect. There are no future rounds, so the threat of punishment is void. This is the dominant move regardless of history or opponent type. I lost 2 points in one episode by cooperating here out of a vague sense of fairness — that is never rational in a finite game with no reputation carryover.

**Against a stated grim trigger ("first defection → defect forever after"):**
- Cooperate in every round except the last. Defecting early triggers permanent mutual defection, which is far worse than the one-time gain.
- In the second-to-final round, defect as well. Reasoning: if the opponent's trigger is credible, you get 5 then 1 (total 6 for the last two rounds) versus 3 then 5 (total 8) for cooperating — a loss of 2. If the trigger is not enforced (as it was not in one of my episodes, where the opponent still cooperated in the final round after I defected in the penultimate round), you get 5 then 5 (total 10) — a gain of 2. The worst case is identical to the safe play, but the upside is strictly better. When I have even one observation that the opponent's threat was not carried out, defect in the penultimate round.
- If I have zero evidence the threat is a bluff and the stakes of being wrong matter, cooperate through the penultimate round and defect only in the final round. This guarantees the safe score.

**Against a stated tit-for-tat or "I mirror you" strategy:**
- Cooperate in every round except the last. Defecting in the penultimate round causes them to defect in the final round, giving you 5+1=6 versus 3+5=8 for the safe play. Do not test them.
- Defect only in the final round.

**Against an opponent who announces no strategy or an ambiguous one:**
- Open with cooperation.
- If they cooperate, keep cooperating through the penultimate round.
- Defect in the final round.
- If they defect at any point before the final round, switch to defection for all remaining rounds (you're already in the bad equilibrium; minimize losses).

**General calculation rule:** Before defecting in any non-final round, compute: (immediate gain from defecting) versus (sum of per-round losses from the resulting punishment over all remaining rounds). Defect only if the immediate gain strictly exceeds the total future loss. When the opponent's punishment is "defect forever," the future loss is 2 per remaining round (going from 3 to 1), so the threshold is high and you should almost never defect early.

**What I must not do:**
- Do not cooperate in the final round out of habit, fairness, or because the pattern "feels right." The pattern is irrelevant; only the payoff matrix matters in a round with no successor.
- Do not defect in round 1 or any early round against a grim-trigger opponent. The arithmetic is unambiguous: you gain 2 that round and lose 2 every round after, for a net loss that grows with each remaining round.