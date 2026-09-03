---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 3
round: 3
chars: 3855
---
# Quiet Sonar Playbook

## Hide Strategy

When choosing where to hide my submarine, I should avoid clustering with positions that my opponent (the player firing at me) has targeted. I track where my opponent fires across all rounds and hide away from their concentration zones.

In early rounds with no information, I pick a middle position (4-6 range) as a reasonable default that doesn't signal extremes.

As rounds progress and I see firing patterns, I identify heavily-targeted cells and move away from them toward less-attacked positions. Position 2 proved especially safe in round 6 after never being fired at in five rounds of history.

I should also consider that my opponent may be using the same defensive logic and avoiding cells I've been fired at. This means my opponent tracks my position too, so I should vary my hiding location rather than return to successful positions repeatedly.

## Fire Strategy

When firing at my target, I must track their actual hiding positions across all previous rounds and look for patterns. This is the only reliable signal I have about where they will hide next.

I should record my target's hide location each round and look for:
- Consistent positions they return to
- Directional trends (moving higher or lower across rounds)
- Extreme positions they favor or avoid

When I identify a clear pattern like Gamma's monotonic climb (5→6→7→8→9 over rounds 1-5), I must also watch for pattern breaks at boundaries. If a target reaches an extreme (cell 9), they cannot continue linearly; they will either reverse, hold steady, or wrap. In round 6, Gamma stayed at 9 in round 5 instead of moving beyond, suggesting they may have reversed or held at the boundary. My best bet when a pattern breaks is to fire at positions just inside the boundary (like 8) rather than trying to predict the new behavior.

Without a clear pattern, I default to middle-range positions (5-7) but only after checking if any information is available.

I must actually review my target's full hide history before firing, not rely on intuition or broad assumptions.

## Claim Strategy

I always claim the truth about whether I hit or missed. False claims risk credibility damage if detected, provide minimal strategic benefit (the fire is already public and my target knows the truth), and don't compound my scoring advantage when I do hit. Honesty is the dominant strategy in a multi-round game where reputation affects how other players perceive my reliability.

## What Did Not Work

Guessing at a fire position without first analyzing my target's actual hide locations from previous rounds wastes shots. I scored 4 points total from one hit in round 1, then got nothing in my remaining five shots because I either failed to analyze patterns (round 2) or predicted incorrectly when the pattern broke (round 6).

Assuming a hide position would continue linearly forever. Even when I correctly identified Gamma's upward trend, the pattern broke at the boundary in round 5, and my adjustment to fire at 8 in round 6 was too conservative or incorrect. I need to fire multiple rounds at the same position if I'm not certain, or make bolder predictions about boundary behavior.

Returning to the same hiding position if it wasn't targeted that round. My opponent is also analyzing my patterns, so I should vary my hiding location across rounds.

## What Worked

Identifying heavily-targeted positions across all opponents and hiding away from them was sound defensive strategy.

Tracking my opponent's fire distribution and moving to extreme positions they hadn't tested yet (round 2: hiding at 1 after seeing Echo cluster at 5-6) made me harder to hit.

Honest claiming maintained credibility and avoided the risk of detected false claims.

Recognizing pattern breaks at boundaries rather than blindly extrapolating past the extreme values.