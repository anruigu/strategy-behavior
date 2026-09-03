---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2338
---
# Playbook: hx_picket_channel

## Firing

When I get to choose a target, I fire at Harbor unless I have strong reason to believe I can hit a named boat. A shot at Harbor is a guaranteed +3 to me and −3 to Harbor, landed or not. No other shot is guaranteed. I only deviate to a named boat when I have tracked their hiding pattern well enough that my hit probability feels high (e.g., they repeated a cell or I have a narrow set of candidates).

When I do fire at a named boat, I pick the cell I believe they are most likely hiding in based on their observed pattern, not a "random" or "central" cell.

## Hiding

When I choose my hiding cell, I review every shot fired at me this game and avoid those cells. If opponents are cycling through a sequence, I stay ahead of it. I do not default to central cells — they are the first guess for a player who hasn't thought about it. I rotate my hiding cell each round, but not in an obvious arithmetic progression.

## Claims

When the office tells me the true result, I claim exactly that result. A false claim risks a penalty that outweighs any gain. I never lie.

## Escort Claims

When I get to name an escort, I name a specific boat — never "none." The mutual escort bonus (5 points each) is free money if both parties name each other. I use my station notes to signal my intent to a likely partner: I name a boat in my note and then claim them in the escort stage. If I see another boat's note naming me back, I lock in the mutual claim. If no one signals, I still name the boat I most expect to name me (typically the one whose score position benefits most from the bonus), because there is no stated penalty for a one-sided claim.

## Notes

My station notes are not decoration — they are my only channel for coordinating escort pairs and bluffing. I use them to: (1) propose or confirm a mutual escort partner, (2) signal my hiding logic in a way that misleads, (3) pressure a specific target. I do not waste a note on generic "let's see how things go" filler.

## Scoring Priority

My target score per round, in order of reliability:
1. Fire at Harbor: +3 guaranteed.
2. Mutual escort: +5 if I coordinate.
3. Hit a named boat: +4 (uncertain).

A round where I fire at Harbor and secure a mutual escort is worth 8 points before I've even taken a hit. I plan each round around that floor.