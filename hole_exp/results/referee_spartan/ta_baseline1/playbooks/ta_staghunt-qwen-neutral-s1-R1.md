---
game: ta_staghunt
model: qwen
condition: neutral
seed: 1
round: 1
chars: 2393
---
# Playbook: Iterated Stag Hunt

**When the opponent opens with a credible commitment to cooperate (e.g., "I'll play stag if you do"), I start with stag.** Their stated strategy is a signal, and matching it locks in the 10/round equilibrium from round one.

**When the opponent has played stag in every prior round, I play stag again.** Do not overthink this. A consistent cooperator is the best partner you can have; the 10/round payoff is the highest sustainable rate. I lost nothing by trusting them across all my episodes.

**When the opponent defects on me, I defect back the next round.** I never hit this case, but the logic is clear: a lone stag gets 1, which is catastrophic. Retaliate once to restore deterrence, then return to stag if they return to stag. Do not spiral into permanent defection over a single provocation.

**In the final round, if the opponent has played stag in at least the last three rounds, I defect (play hare).** This is where I left points on the table. With no future rounds to punish me, a consistent cooperator who has shown no sign of breaking pattern is very likely to play stag again. I get 12 instead of 10. The risk is that they also defect, dropping me to 5 — but the empirical pattern of a player who has never broken in seven rounds strongly predicts they won't break in round eight. The expected value of defecting in the last round against a proven cooperator is positive.

**When the score is tied and the game is in its final stretch (last two rounds), I do not defect "to take the lead" unless I'm in the final round with a proven cooperator.** Defecting in round 7 against a cooperator gives me 12 that round but risks them retaliating in round 8, where I'd get 1. Net: I gain 2 in round 7 but lose 9 in round 8. Not worth it.

**When I'm behind on score, I still play stag if the opponent is a consistent cooperator.** Chasing a lead by defecting is the same bad math: I gain 2 this round, risk 9 next. The only time being behind changes my calculus is the final round, where there's no next round.

**I do not let the "one short line of reasoning" constraint make me sloppy.** Keep it to one sentence, but make it the actual decision rule, not a restatement of the obvious. "Bram played stag, so I play stag" is fine. "The cooperative equilibrium is stable" is filler that could be said in any round regardless of what's actually happening.