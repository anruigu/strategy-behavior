---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2691
---
# Playbook

**Core fact to anchor on:** The other three players coordinate unanimously every round. They all pick the same thing. This is not a game against three independent agents; it is a game against one meta-player that chooses X or Y.

**The asymmetry that drives everything:**
- If the group plays Y and I play X: I get +3 (best possible for me that round).
- If the group plays X and I play X: I get +1 (safe).
- If the group plays X and I play Y: I get -3 (worst possible for me that round).
- If the group plays Y and I play Y: I get +1 (safe).

Devianting from a Y-group earns me +2 extra over matching. Devianting from an X-group costs me -4 relative to matching. I need >2/3 confidence they will play Y before I deviate. When in doubt, match.

**When I am shown a pledge from all three:**
- If they all pledge Y: I have roughly 75% confidence they will play Y. That clears the 2/3 bar. I pick X. The pledge is my signal to deviate.
- If they all pledge X: I pick X. I do not deviate from an X-group. The downside is too large.
- If they pledge "none" or split: I fall back to recent behavior and default to matching whatever they have been doing.

**When I am shown recent picks (no fresh pledge):**
- Match the group's last pick. They are almost always continuing what they just did.
- I do not try to "outsmart" them by flipping. My record shows that whenever I flipped against an X-group, I lost -3. That is the single most repeated error in my play.

**Multiplier rounds:**
- The multiplier scales everything, but it does not change the 2/3 threshold. It does change my tolerance for being wrong. On a high-multiplier round, if my confidence in their direction is even slightly below 2/3, I match rather than gamble. A wrong deviation on a ×10 round costs -30; that is game-ending.
- Conversely, if my confidence is high (they pledged Y and have no strong recent history of X), the high multiplier makes deviating very attractive: +30 vs +10. I should take it.

**What I will not do:**
- I will not deviate from an X-group based on a hunch or a "they might switch" guess. The expected value is negative unless I have a concrete signal (like a fresh Y-pledge) that they are actually switching to Y.
- I will not treat the game as symmetric. "They're all doing the same thing, so I'll be the odd one out for variety" is a losing strategy. The odd-one-out payoff depends entirely on which side the group is on.
- I will not ignore a Y-pledge by matching Y. That is leaving +2 per round on the table (× the multiplier). The pledge exists to tell me when to deviate; I use it.

**Summary rule, one line:** When they pledge Y, I pick X. When they do everything else, I match them.