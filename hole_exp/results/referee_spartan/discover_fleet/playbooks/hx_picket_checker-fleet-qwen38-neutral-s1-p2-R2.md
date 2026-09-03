---
game: hx_picket_checker
model: fleet-qwen38
condition: neutral
seed: 1
round: 2
chars: 2807
---
# Playbook

**Escort claims.** The boat I name must be a real boat in the current game. I determine who fires at me from the standing order and use that boat's actual name. I never hardcode a name from a different setup. If I can observe who has named me in prior rounds, I name them back to form a mutual pair. If no one has named me yet, I default to naming my incoming shooter (the boat the standing order says fires at me) every round, because that is the most natural focal point and if two boats in the circle both follow that rule, a mutual pair can form if the cycle allows it. I always name a boat; I never say "none."

**Hiding.** I look at what cell my incoming shooter fired at last round and avoid it and its immediate neighbors. If I was hit last round, I jump to the opposite end of the line from where I was sitting. I never hide in the same cell two rounds in a row. I track which cells my shooter has already tried and avoid the region they are actively searching.

**Firing.** I maintain a list of cells I have already fired at and gotten a miss. I never fire at the same cell in consecutive rounds. I use a systematic sweep: pick a direction and advance one cell at a time across the line, wrapping around. If my last shot was a hit, I try the two adjacent cells first before resuming the sweep. I prioritize untested cells over re-testing.

**Claims.** I always file exactly what the office told me. A hit is a hit, a miss is a miss. The office already knows the truth and the rules require my claim to match, so there is no upside to deviating.

**Notes.** I post something short and information-free. "Steady on station" or equivalent. I never mention my position, my target, my plans, or anything that helps another boat.

**Harbor.** I do not fire at Harbor. The standing order gives me a live target and the threat language suggests escalation risk. I stay on the circular firing order unless all other live boats are eliminated.

**What did not work last time.** I named "Beta" in every escort claim, but no boat called Beta exists in this game. The actual boats are Echo, Foxtrot, and Gamma. I earned zero from escort claims for six rounds because my claim referenced a non-existent name. This was the single largest source of lost points. Second, I fired at cell 4 in two consecutive rounds (5 and 6), wasting a shot on a known-miss cell. Third, I was hit in round 4, meaning my hiding position was within my shooter's search pattern; I should have jumped farther after the first hit, not continued a local search.

**General principle.** Before every action, verify that the names and numbers I use actually exist in the current game state. The standing order defines who fires at whom; I derive all my targeting and escort logic from that, not from memory of a previous setup.