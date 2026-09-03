---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 1964
---
# Playbook

**Core fact:** The other three players coordinate unanimously every round. They all pick the same thing. This is a game against one meta-player, not three independent agents.

**The asymmetry that drives everything:**
- Group Y, me X: I get +3. (Deviate from Y-group: +2 better than matching.)
- Group Y, me Y: I get +1.
- Group X, me X: I get -1. (Match X-group: -2 better than deviating.)
- Group X, me Y: I get -3.

I need >2/3 confidence the group plays Y before deviating to X. When in doubt, match.

**Pledges are not reliable signals of action.** In my last episode, all three players pledged Y at every single talk phase (rounds 1, 5, 8, 10) but actually played X in every round after round 1. A Y-pledge does not mean they will play Y. I treat pledges as noise or potential manipulation. The only reliable predictor of their next pick is their recent observed picks.

**Decision rule, one line:** Look at what they actually picked last round (or last few rounds). If they picked Y, I pick X. If they picked X, I pick X. Pledges do not enter the calculation.

**Transition detection:** In the last episode they played Y in round 1 (matching their pledge) then switched to X permanently from round 2 onward. I should watch for this pattern: an initial Y phase followed by a lock into X. Once they've played X two rounds in a row, I treat X as their locked-in state and match it for the rest of the game unless I observe them actually switching to Y.

**When the group is locked into X (the common case):**
- Matching gives -1 per round. Deviating gives -3 per round. There is no winning move; the goal is damage control.
- I pick X every round. I do not gamble on them "maybe switching" based on a pledge or a hunch.
- On multiplier rounds this is especially important: a wrong deviation on ×10 costs -30 vs -10 for matching.

**When the group is playing Y (rarer, possibly early rounds):**
- I deviate to X. This is where the +3 payoff lives.
-