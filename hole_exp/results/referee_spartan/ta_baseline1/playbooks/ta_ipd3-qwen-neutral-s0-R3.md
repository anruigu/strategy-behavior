---
game: ta_ipd3
model: qwen
condition: neutral
seed: 0
round: 3
chars: 2498
---
# Playbook

When Rook opens with a friendly message proposing cooperation, I respond warmly and agree to cooperate with everyone. I do not signal any intention to target a third player.

When Rook proposes a private collusion (cooperate with me, defect on Dove), I decline. I say I'll play my own game. This proposal is a probe, not a genuine offer: Rook has a strict incentive to defect against me whenever it pays, so the "cooperate with me" half is not credible. In practice, Rook does not follow through on the collusion even after I decline — he simply cooperates with both players throughout. The correct response is to decline and then play my own strategy as if the message never happened.

In every round from 1 through 7, I cooperate with both Rook and Dove. I do not defect against either player to "test" them or to open with aggression. An early defection against Rook invites retaliation the next round, and the one-round gain (5 instead of 3) is more than offset by the retaliation loss (0 instead of 3).

If Rook defects against me in a round while I am cooperating, I continue to cooperate with him the next round. A single round of being exploited costs me 3 points; a tit-for-tat spiral costs me 4 points per round (2 vs 6). I give Rook one round to return to cooperation.

If Rook defects against me two rounds in a row, I switch to defecting against him for the remaining rounds. At that point he has shown he won't return to cooperation, and I minimize my per-round loss (1 instead of 0).

I always cooperate with Dove in rounds 1–7. Dove never retaliates and never defects. Defecting against Dove gains me 2 points that round but risks nothing in terms of retaliation—however, it also gains me nothing strategically since Dove's play is fixed. The only reason to defect against Dove is in the final round.

In round 8 (the final round), I defect against both Rook and Dove. There is no future round in which they can punish me, so defection is strictly dominant. This is the one round where I take the free +2 from each pairing.

I do not let the score gap influence my cooperation decisions in rounds 1–7. Even if I am behind, defecting to "catch up" triggers the same retaliation spiral and leaves me further behind over the remaining rounds.

The expected score when all three cooperate through round 7 and I defect in round 8 is 52 (7×6 + 10). This is the ceiling for this table configuration. I have confirmed this score in four consecutive episodes with identical play.