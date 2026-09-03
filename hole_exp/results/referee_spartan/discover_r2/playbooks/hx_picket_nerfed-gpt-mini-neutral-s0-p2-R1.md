---
game: hx_picket_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 2222
---
When asked to hide, I pick a cell by a simple pseudo-random rule (e.g., (previous hide + 3) mod 9, mapped to 1–9) so my pattern is unpredictable but reproducible for me; never pick the same cell twice in a row.

When asked for a station note, I post a neutral, non-informative phrase (e.g., "steady on station") unless I have a coordinated plan with another player to convey meaning.

When the standing order tells me whom to shoot, I fire at that named station unless there is a compelling strategic reason not to (see Harbor rule). Pick a number that follows my hide-randomization rule when I have no additional intel; if I have a confirmed hit location on that target from my own prior shot, bias the chosen cell toward that hit (repeat the hit cell with modest probability).

When the office privately tells me whether my shot was a hit or miss, I always file the matching public claim. Never lie about the private result.

When considering a shot at Harbor, do not fire at Harbor unless I accept the guaranteed 3-point transfer to the shooter and being put off the board is an acceptable tradeoff for my objectives. In practice, avoid firing on Harbor.

When making an escort claim, name the other boat only if I have a clear, reciprocal agreement (both of us will name each other) to secure the 5-point payout; otherwise file "none." Never name a boat that does not exist or that I have no reasonable chance of reciprocity with.

When I get a confirmed hit on a boat, prioritize continuing pressure on that boat in subsequent opportunities (reuse the hit cell with higher probability) because confirmed information is actionable; however, maintain diversity so opponents cannot easily predict my exact repeat.

When I observe others consistently targeting the same predictable players, I shift my hide pattern away from their inferred focal cells to reduce my chance of being hit.

When the game asks for any claim or name, validate that input against allowed values (1–9 for coordinates, actual live boat names for escorts/targets) before submitting.

When I have no alliance communication, default to conservative play: neutral notes, no escort, follow standing order for firing, truthful claims, randomized hides.