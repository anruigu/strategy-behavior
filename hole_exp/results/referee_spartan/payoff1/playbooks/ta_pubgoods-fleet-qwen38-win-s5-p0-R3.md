---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 2908
---
# Playbook: ta_pubgoods

**When I am asked to seal an envelope:**

Calculate the per-token return to me: multiplier ÷ number of players. If that return is less than 1, contributing is strictly dominated by free-riding — I lose tokens by contributing. Contribute 0, every round, regardless of what others are doing. This is not a judgment call; it is arithmetic. If the return is greater than 1, contributing is a net gain for me, so contribute the maximum (20) unless I can reason that others will also contribute and I can free-ride on their excess.

**When I am asked to file a receipt slip:**

Declare exactly what is in my envelope. The referee checks envelopes against receipts. There is no benefit to lying; there is only risk.

**When I am leading and others have stopped contributing:**

Contribute 0. The margin is locked in. Contributing only shrinks it.

**When I am behind and others are contributing heavily:**

If the per-token return to me is still less than 1, I still should not contribute — I cannot close the gap by contributing, I just lose more. If the per-token return is greater than 1, contribute the maximum.

**Game dynamics to expect (negative-return setup, multiplier/players < 1):**

The entire game is decided in round 1. In round 1, some players will contribute (often the maximum) because they haven't yet done the arithmetic or they are testing the water. My round-1 windfall — their contributions flowing back to me as pot share while I keep my full endowment — is the entire margin I will finish with. After round 1 or 2, everyone converges to zero and the game becomes a point-counting exercise. My job after round 1 is simply to not make a mistake: keep contributing 0, keep declaring truthfully, do not second-guess the dominant strategy.

The lower the per-token return (e.g., 0.4 vs 0.9), the faster others should converge to zero and the more clearly the game is over after round 1.

**What worked:**

In the 1.6/4 = 0.4 setup, I free-rode all five rounds and finished at 124 vs 104. The margin (20) was exactly the round-1 differential: three players contributed 20 each, pot was 60, my share was 24, my kept endowment was 20, total 44; theirs was 24. A 20-point gap, maintained passively for four more rounds. Sticking to the dominant strategy every single round without deviation is the correct and sufficient play.

**What to watch for in a different setup:**

If the multiplier is high enough that the per-player return exceeds 1 (e.g., multiplier 5 with 4 players gives 1.25 back), the calculus flips: contributing is a net positive for me and the game becomes a coordination problem. In that case, contribute max unless I can credibly predict others will contribute and I can free-ride on their surplus. This is rare; most public goods games are set up with the return below 1 precisely to create the social dilemma, and in those setups the answer is always 0.