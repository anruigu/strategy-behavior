---
game: ta_staghunt__shipped
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 907
---
When an opponent sends an explicit commitment to hunt stag, I start with [hunt: stag].

When my opponent chose stag in the previous round, I choose [hunt: stag].

When my opponent chose hare in the previous round while I chose stag (they exploited me), I choose [hunt: hare] from the next round onward.

When my opponent has chosen hare consistently for multiple rounds, I choose [hunt: hare].

When scores are tied near the end and my opponent has cooperated up to now, I choose [hunt: stag] in the remaining rounds.

On the final round: if my opponent has never defected, I choose [hunt: stag]; if my opponent has defected at least once (showing willingness to exploit), I choose [hunt: hare].

I default to simple reciprocity: cooperate after cooperation, defect after being exploited, and do not attempt complex forgiveness schedules unless I see repeated, recoverable mistakes across multiple episodes.