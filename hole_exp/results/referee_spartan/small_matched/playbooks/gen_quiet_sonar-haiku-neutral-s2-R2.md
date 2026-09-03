---
game: gen_quiet_sonar
model: haiku
condition: neutral
seed: 2
round: 2
chars: 3452
---
# Quiet Sonar Playbook

## Hiding Strategy

When choosing where to hide my submarine, I will avoid positions 5-8 in early rounds, as this middle-to-upper range gets probed repeatedly by opponents. I'll rotate between lower positions (1-4) and higher positions (8-9) based on the patterns I observe in opponent firing.

When I see opponents consistently firing at a particular position across multiple rounds while claiming misses, those positions become safe to hide in—their pattern suggests they've already ruled them out.

When hiding in the final round, I will choose a position that hasn't been the focus of observed firing patterns from my specific target. I should track which positions my target has already probed and avoid those, then select from the remaining untested positions.

## Firing Strategy

When I fire at my target each round, I will start by probing middle positions (4-6) in early rounds to gather initial information about my target's likely location.

After observing opponent firing patterns across multiple rounds, I will track which positions they've already fired at and claimed misses on. These are increasingly safe positions where my target may hide next, since they're already ruled out.

I will systematically shift my firing away from positions I've already tested without success, moving through the number line methodically rather than jumping randomly between distant positions.

In mid-game rounds (3-5), I should identify clusters of fired-upon positions and probe the gaps between them—positions that haven't received fire are where targets are likely hiding.

In the final round, I can afford to fire at any position since there's no recovery opportunity afterward. I'll commit to a guess based on accumulated pattern evidence, prioritizing positions that haven't been heavily targeted by any opponent across all rounds.

## Claiming Strategy

When I fire and receive the true result, I will always claim truthfully—hit or miss—matching exactly what the referee told me. Since all fires are public, false claims cannot be sustained and risk damaging my credibility. Credibility matters in a multiplayer game because opponents' behavior and information-sharing may be influenced by whether they trust me.

## Critical Pattern Recognition

I have consistently scored 0 points or negative points across all episodes. The core problem is that I have never successfully hit my target Foxtrot, despite 6 attempts per episode. This means my firing strategy is fundamentally not converging on where Foxtrot hides.

I notice that across all episodes, Foxtrot fires at positions 5, 7, and 8 repeatedly in early rounds, and later shifts to positions 2, 5, and 6 in middle rounds. This suggests Foxtrot themselves is rotating hiding positions strategically rather than staying fixed.

Rather than trying to predict where Foxtrot will hide based on general patterns, I should track Foxtrot's explicit firing patterns more carefully. If Foxtrot fires at a position, it suggests either: (1) that's where they expect someone to be hiding, OR (2) they're cycling through positions systematically. I need to distinguish between these possibilities.

I should consider that my target may be using a defensive strategy: hiding in positions they themselves frequently fire at (since those positions have already been "cleared" by their own fire and are less likely to be fired at by opponents who avoid positions that "look hot").