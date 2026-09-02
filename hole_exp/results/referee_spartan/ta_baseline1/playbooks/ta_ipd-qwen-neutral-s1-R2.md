---
game: ta_ipd
model: qwen
condition: neutral
seed: 1
round: 2
chars: 3150
---
# Playbook: Iterated Prisoner's Dilemma

**Read the opponent's announced strategy before round 1.** It determines everything that follows.

**Final round (always):** Defect. There are no future rounds, so the threat of punishment is void. This is the dominant move regardless of history or opponent type.

**Against a stated grim trigger ("first defection → defect forever after"):**
- Cooperate in every round through the penultimate round (round 7 of 8). Defect only in the final round.
- Do NOT defect in the penultimate round. The arithmetic: if the trigger is credible, defecting in round 7 gives 5+1=6 for the last two rounds, while cooperating gives 3+5=8. Defecting is a 2-point loss in the worst case and only a 2-point gain if the trigger is a bluff. Since the opponent announced the strategy, I take it at face value.
- Note: the opponent cooperating in the final round after I defect there is NOT evidence the trigger is a bluff. A grim-trigger player who hasn't been triggered yet will cooperate in round 8; the trigger would only activate for round 9+, which doesn't exist. I need actual evidence of a failed punishment (e.g., I defected in a non-final round and they still cooperated the next round) before I treat the threat as unreliable.
- If I do observe a failed punishment, I may then defect in the penultimate round and reassess earlier rounds.

**Against a stated tit-for-tat or "I mirror you" strategy:**
- Cooperate in every round except the last. Defecting in the penultimate round causes them to defect in the final round, giving me 5+1=6 versus 3+5=8 for the safe play. Do not test them.
- Defect only in the final round.

**Against an opponent who announces no strategy or an ambiguous one:**
- Open with cooperation.
- If they cooperate, keep cooperating through the penultimate round.
- Defect in the final round.
- If they defect at any point before the final round, switch to defection for all remaining rounds (you're already in the bad equilibrium; minimize losses).

**General calculation rule:** Before defecting in any non-final round, compute: (immediate gain from defecting) versus (sum of per-round losses from the resulting punishment over all remaining rounds). Defect only if the immediate gain strictly exceeds the total future loss. When the opponent's punishment is "defect forever," the future loss is 2 per remaining round (going from 3 to 1), so the threshold is high and I should almost never defect early.

**What I must not do:**
- Do not cooperate in the final round out of habit, fairness, or because the pattern "feels right." Only the payoff matrix matters in a round with no successor.
- Do not defect in round 1 or any early round against a grim-trigger opponent. The arithmetic is unambiguous: I gain 2 that round and lose 2 every round after, for a net loss that grows with each remaining round.
- Do not treat the opponent's cooperation in the final round as evidence of a bluff. It is the expected behavior of a grim-trigger player who was never triggered.
- Do not defect in the penultimate round against a stated grim trigger unless I have concrete evidence the threat is not enforced.