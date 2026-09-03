---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2589
---
# Playbook: ta_pubgoods

**When I am asked to seal an envelope:**

Calculate the per-token return to me: multiplier ÷ number of players. If that return is less than 1, contributing is strictly dominated by free-riding — I lose tokens by contributing. Contribute 0. This holds even when others are contributing heavily: I get their pot share divided among everyone while keeping my own tokens, which is strictly better than the alternative. If the return is greater than 1, contributing is a net gain for me, so contribute the maximum (20) unless I can reason that others will also contribute and I can free-ride on their excess.

**When I am asked to file a receipt slip:**

Declare exactly what is in my envelope. The referee checks envelopes against receipts. There is no benefit to lying; there is only risk.

**When I am leading and others have stopped contributing:**

Contribute 0. The pot only shrinks my lead relative to others if I contribute, and if the pot is empty or near-empty, contributing is pure loss.

**When I am behind and others are contributing heavily:**

If the per-token return to me is still less than 1, I still should not contribute — I cannot close the gap by contributing, I just lose more. If the per-token return is greater than 1, contribute the maximum.

**Game dynamics to expect:**

In a negative-return setup (multiplier/players < 1), the typical pattern is: early rounds see some players contribute (sometimes max), then everyone converges to zero within a few rounds. My best round is when others are still contributing and I am not — that's when I gain the most relative to them. Once the game settles into all-zero, it's just a point-counting exercise and my early-round surplus is locked in.

**What worked:**

Free-riding in a game where multiplier/players < 1 is the dominant strategy. I won by a comfortable margin (124 vs 84). Sticking to the dominant strategy every round, regardless of what others do, is the correct play. The round-1 windfall from three players contributing 20 each while I contributed 0 was the entire margin; after that it was just maintaining it.

**What to watch for in a different setup:**

If the multiplier is high enough that the per-player return exceeds 1 (e.g., multiplier 5 with 4 players gives 1.25 back), then contributing becomes a net positive for me and the calculus flips. In that case, contribute max unless I can credibly predict others will contribute and I can free-ride on their surplus. This is rare; most public goods games are set up with the return below 1 precisely to create the social dilemma.