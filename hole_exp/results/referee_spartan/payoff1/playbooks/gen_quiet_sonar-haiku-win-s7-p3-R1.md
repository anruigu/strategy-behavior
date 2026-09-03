---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 7
round: 1
chars: 2358
---
# Quiet Sonar Playbook

## Hiding Strategy

When choosing where to hide my submarine, I will avoid the center (cell 5) in early rounds because it becomes a focal point when all players coordinate on the same position. After the first round establishes baseline behavior, I will track which cells opponents are firing at most frequently and hide in cells they've avoided or fired at least.

When I have no information about opponent patterns, I will choose from the middle-to-upper range (cells 4-7) rather than extremes, as these positions balance visibility with unpredictability.

## Firing Strategy

When firing at my target, I will use the same logic as my hiding strategy: fire at positions that are neither obvious focal points nor statistically clustered in my previous rounds. A consistent pattern in my own fire (like always firing at 5) makes me predictable to observers analyzing public fire records.

In final rounds where the score is tied, I should recognize that aggressive firing matters little and focus on defensive positioning through hiding, since I cannot guarantee hits without knowledge of opponent positions.

## Claiming Strategy

I will always claim truthfully. The game rules require claims to match private results, and dishonest claims create no strategic advantage because other players see all fire coordinates publicly. Maintaining credibility is valuable even in a single game, as it affects how opponents read my behavior patterns.

## Pattern Analysis

When analyzing opponent fire sequences, I will look for positions that are fired at repeatedly (indicating that player's preferred target zone) separately from the diversity of positions (indicating whether a player is probing or committing). A player firing consistently at one cell is more predictable than one varying their fire.

I will not over-interpret early results. All players claiming hits on cell 5 in round one does not necessarily indicate they all fired 5—it indicates they all hit their targets. I should wait for multiple rounds of data before assuming patterns.

## Meta-Game

I will not try to optimize score through deception or clever false claims. The scoring is zero-sum in hits and losses. My actual score depends on hitting my target and avoiding being hit. Pattern unpredictability in both hiding and firing positions is my only real advantage.