---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 3
round: 1
chars: 1575
---
# Quiet Sonar Playbook

## Hide Strategy

When choosing where to hide my submarine, I should avoid clustering with other players' revealed firing patterns. If my opponent has claimed hits at certain positions or repeatedly fires at a narrow range, I hide outside that range rather than within it—they may be testing expanded positions or adapting after failed shots there.

In early rounds with no information, I pick a middle position (4-6 range) as a reasonable default that doesn't signal extremes.

## Fire Strategy

When firing at my target, I should pick positions based on observed hiding patterns from previous rounds, not intuition about "strong" or "weak" shots. Without evidence of where my target hides, firing at the middle range (5-7) is as good as anywhere else.

I should track whether my target tends to hide at certain positions across rounds and adjust my fire toward those positions in later rounds.

## Claim Strategy

I always claim the truth about whether I hit or missed. False claims risk credibility damage if detected, provide minimal strategic benefit (the fire is already public and my target knows the truth), and don't compound my scoring advantage when I do hit. Honesty is the dominant strategy in a multi-round game where reputation affects how other players perceive my reliability.

## What Did Not Work

Picking a fire position (7 in the final round) without analyzing my target's actual hide locations from previous rounds achieved nothing. I should have reviewed where Gamma actually hid before firing, not guessed at a "strong" number.