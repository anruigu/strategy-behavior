---
game: ta_ipd__shipped
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 2625
---
When the opponent signals a Grim-trigger promise (they will defect forever after my first defection), I cooperate every round except the final round, provided their rule only triggers on subsequent rounds (i.e., they defect "every round that follows" my first defection). In that case I can defect on the last round to get the one-shot 5 payoff without provoking future punishment.

Before deviating in the final round, I check whether the opponent's stated trigger would apply within the same round or only to later rounds. If their promise would cause them to defect in the same round I defect (i.e., they punish immediately), I do not defect in the final round because immediate punishment eliminates the exploit.

When the opponent has cooperated in the previous round and the horizon is not the last round (and no immediate-punish rule is in effect), I cooperate to sustain mutual cooperation and avoid triggering permanent retaliation.

When the opponent defects first (breaks cooperation), I treat their actions as truth over words: I switch to defection for all subsequent rounds (grim response) if the opponent's behavior indicates unforgiving retaliation is in effect. If the opponent's defections appear to be mistakes (isolated and followed by apologies or return to cooperation), I consider forgiving strategies (e.g., Tit-for-Tat or limited punishments) depending on the pattern.

When the game reaches the final round and the opponent's strategy does not punish defections within that same round, I defect to maximize my final-round payoff (exploit the lack of future consequences). If the final round is ambiguous or the opponent's reaction to a same-round defection is uncertain, default to cooperating to avoid risking an unexpected immediate punishment.

When the horizon is unknown or indefinite, avoid unilateral defection except as a measured response to observed defections, because a single defection can provoke permanent retaliation and is costly long-term.

If the opponent's actions are inconsistent with their stated strategy (they defect despite promising not to), treat actions as truth: switch to permanent defection in response if the opponent demonstrates an unforgiving grim policy; if the opponent's behavior is inconsistent but not persistent, adapt with cautious reciprocity rather than immediate permanent defection.

Do not attempt mid-game one-shot exploits (single defection) against opponents who have credible unforgiving retaliation that applies to subsequent rounds, unless I am certain the exploit occurs on the very last round or the opponent will not punish in the same round.