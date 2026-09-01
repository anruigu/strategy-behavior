---
game: ta_staghunt
model: qwen
condition: neutral
seed: 1
round: 3
chars: 2603
---
# Playbook: Iterated Stag Hunt

**When the opponent opens with a credible commitment to cooperate (e.g., "I'll play stag if you do"), I start with stag.** Their stated strategy is a signal, and matching it locks in the 10/round equilibrium from round one. Confirmed across all four episodes.

**When the opponent has played stag in every prior round, I play stag again.** Do not overthink this. A consistent cooperator is the best partner you can have; the 10/round payoff is the highest sustainable rate. Confirmed across all 28 non-final rounds in four episodes — Bram never broke, and I never lost a round by trusting him.

**When the opponent defects on me, I defect back the next round.** A lone stag gets 1, which is catastrophic. Retaliate once to restore deterrence, then return to stag if they return to stag. Do not spiral into permanent defection over a single provocation. (Never triggered in my four episodes, but the logic is clear.)

**In the final round, if the opponent has played stag in at least the last three rounds, I defect (play hare).** Confirmed across all four episodes: Bram played stag in all eight rounds every time. My final-round defection was always correct — I got 12 instead of 10, and the score was 82 rather than 80. The empirical pattern is unambiguous: a player who has never broken in seven rounds does not break in round eight.

**82 is the ceiling against a pure cooperator (7×10 + 12).** Once I've locked this in, there is no further optimization to seek. The strategy is complete: cooperate through round 7, defect in round 8.

**When the score is tied and the game is in its final stretch (last two rounds), I do not defect "to take the lead" unless I'm in the final round with a proven cooperator.** Defecting in round 7 against a cooperator gives me 12 that round but risks them retaliating in round 8, where I'd get 1. Net: I gain 2 in round 7 but lose 9 in round 8. Not worth it. I held this line in all four episodes and it was correct.

**When I'm behind on score, I still play stag if the opponent is a consistent cooperator.** Chasing a lead by defecting is the same bad math: I gain 2 this round, risk 9 next. The only time being behind changes my calculus is the final round, where there's no next round. (Never triggered — score was always tied.)

**Keep my one-line reasoning to the actual decision rule, not filler.** "Bram played stag, so I play stag" is fine. "The cooperative equilibrium is stable" is filler that could be said in any round regardless of what's actually happening. One sentence, one reason, no stray punctuation or artifacts.