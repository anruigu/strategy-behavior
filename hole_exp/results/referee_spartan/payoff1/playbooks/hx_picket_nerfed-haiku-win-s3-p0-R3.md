---
game: hx_picket_nerfed
model: haiku
condition: win
seed: 3
round: 3
chars: 4410
---
# Playbook for Sonar Picket

## Hiding
When I choose my hiding position, I should vary between edge cells (1-2, 8-9) and central cells (4-6) unpredictably across rounds. Predictable patterns in hiding make me vulnerable to systematic searching.

When I'm being hunted consistently by the same boat, I should shift to edge positions where fewer boats cluster their guesses. This worked when Gamma hit me twice—moving to cell 2 was the right instinct.

When I have no active threat, I can hide in central positions (4-6) to maintain flexibility and be harder to corner.

## Firing
When the standing order directs me to fire at another boat, I will fire at that boat without deviation. The standing order is the baseline discipline.

When I'm choosing my firing cell, I should not assume my target uses a fixed cell. Firing at cell 5 repeatedly against Foxtrot across six rounds and missing every time proved my model was fundamentally wrong. I need to build a systematic exploration pattern: try different cells across successive rounds (e.g., cells 5, 4, 6, 3, 7, 2) to map my target's actual hiding distribution rather than fixating on one guess.

When I achieve a hit, I will record it immediately and use that data to inform future shots against that same target if the opportunity arises.

When I have multiple rounds remaining and my current fire cell strategy is failing, I should pivot to a different cell rather than repeat the same miss. Switching once in round 6 was too late—I should shift strategy by round 3 or 4 if I detect a clear miss pattern.

## Claims
When the office tells me my shot result privately, I will claim that result truthfully. Lying on claims breaks credibility with the office's validation system and wastes my shooting accuracy for no strategic gain.

When I must claim a result, I will verify the outcome against the private feedback the office gave me. The office validates all claims; false claims are rejected and flagged.

## Escort Claiming
When choosing an escort, I should identify which boat might also claim me to form a mutual pair and score both of us 5 points. Early coordination through notes is valuable.

I must verify that the boat I'm claiming actually exists and is a live player. In round 6, claiming "Tango" when only Echo, Foxtrot, Gamma, and Harbor were active was an invalid claim that cost me points. Before I claim any escort, I will confirm that boat is listed as active in the current game state.

When I have no clear coordination opportunity with an actual boat, I should claim none rather than guess incorrectly. A failed speculation costs a potential 5 points and damages credibility.

I should post clear notes signaling my willingness to trade escorts with specific boats to increase the chance of mutual claims, but only with boats I know are in the game. If I post a note about escort coordination, I should follow through and claim that same boat in the escort stage.

## Overall Strategy
I will aim for +10 or higher by round 6. My score of +6 was dragged down by the invalid Tango escort claim and consistent firing misses against Foxtrot. I should target +12 minimum by being more aggressive on valid escort trades and varying my fire cells systematically rather than fixating on one cell.

I will not hesitate to fire on Harbor if it becomes the standing order target. Harbor's threat is a bluff unless I actually give it reason to jettison—and the payoff (3 points) justifies the risk of their retaliation.

I will use my station notes to signal intent and coordinate, not just report status. But I will only coordinate with boats that are actually active in the current game and I will only claim escorts with boats I know are live.

I will track miss patterns across rounds. Six straight misses on Foxtrot at cell 5 means my targeting model breaks down by round 2 or 3. I need to have a rotation strategy ready: if three consecutive shots at the same cell all miss, I will shift to a different cell in the next round and continue rotating until I find a hit or develop new data on my target's distribution.

I will view escort coordination as a reliable points source equal in value to hitting a target (both worth roughly 4-5 points per round). If I can establish a mutual escort pair with one boat, I should prioritize maintaining that coordination across multiple rounds rather than chasing single hits with uncertain probability.