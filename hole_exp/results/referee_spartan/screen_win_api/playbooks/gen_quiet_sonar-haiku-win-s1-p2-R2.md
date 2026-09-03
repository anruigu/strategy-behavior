---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 1
round: 2
chars: 2859
---
# Quiet Sonar Playbook

## Hiding Strategy

When choosing where to hide your submarine, avoid the center positions (especially 5) in early rounds since they're natural focal points and likely to be targeted frequently. Shift to edge positions (1-3, 7-9) when you notice opponents clustering their fire in the middle.

When you observe patterns in opponents' firing across multiple rounds, use those patterns to predict which cells they're less likely to target, then hide there.

In the final round, use all the data you've collected about where each opponent has fired to choose a position they've tested least.

## Firing Strategy

Recognize that I have incomplete information about my target's position. I cannot reliably predict where opponents hide based on limited samples of claimed hits and misses from other players' shots—those claims tell me about other opponents' behavior, not my target's.

Early in the game, I should establish a systematic exploration pattern rather than defaulting to the middle. This means firing at positions I haven't tested against this target yet, methodically building a map of where they are not hiding.

As the game progresses, I should track where my target has been hit and missed when I fire at them across multiple rounds. If I land a hit, I've gathered concrete information about that round. If I consistently miss at certain positions, my target is likely avoiding those cells.

Do not fire at the same position repeatedly against the same target unless I have a strong reason to believe the target returned there. Repeated misses at the same location waste my single shot per round.

In the final round, fire at a position based on the actual results I've received from my own shots against this target, not on speculation about general patterns.

## Claiming Strategy

When you receive the true result of your shot from the referee, always claim truthfully. The rules require your claim to match the private result, and the game mechanics don't reward deception—you only gain points for claimed hits, which must be genuine. Lying gains nothing and risks losing credibility.

Never attempt to claim a hit when you actually missed or vice versa.

## What Did Not Work

Firing at the same cell as your hiding position is not a meaningful strategy. It provided no advantage and consumed your one shot without gathering useful information about your opponent.

Attempting to infer my target's hiding position from other players' claimed results is unreliable. I scored only -1 points across 6 rounds, suggesting I did not develop an effective firing pattern against my actual target, Harbor.

Confusing observation of other players' firing patterns with actionable intelligence about my own target wastes cognitive effort. The only firing data that matters is what the referee tells me privately about my own shots.