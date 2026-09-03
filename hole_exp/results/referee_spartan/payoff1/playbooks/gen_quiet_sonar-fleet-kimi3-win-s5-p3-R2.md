---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2720
---
When the claim stage reaches me, I stop treating it as a decision — the rules force my claim to match the private result, so I report the true result immediately with no talk of bluffing, honesty, or credibility. That stage earns nothing by deliberation.

When firing, I accept that a chain-of-four with private hides gives me almost no signal, so I play it as a coverage and unpredictability problem, not a guessing-hot-hand problem. I enforce my own rotation rule mechanically: before writing [fire: n] I check my last two fires and refuse to repeat either — this episode I fired 3 in rounds 3, 4, 5 and 6 despite the rule being in my playbook, and got zero hits from it. Rotation is worthless if I don't actually execute it.

I treat repeated identical fire lines in the public history as information about my opponents, not noise. This episode both Echo and Gamma fired 6 every single round from round 3 onward — perfectly static players. When I detect a static opponent, I exploit it fully: if the static player is my predator, I simply never hide on their fixed cell; if my target is being shot by a static player and keeps getting hit, my target is also static, which tells me nothing directly about their hide but confirms nobody is adapting.

When hiding, I build a running frequency table of my predator's public fires across all prior rounds and hide in their cold zone; with a perfectly static predator this becomes trivial — just avoid their one cell. Against a static predator my choice within the other eight cells barely matters for safety, so I pick one and stop agonizing; against an adaptive predator I rotate among two or three cells inside the cold zone so a lucky hit teaches them nothing reusable.

I accept that my offense may score near zero in this format — one target, one shot per round, nine cells, and a target who can dodge my last public fire. My expected hits are low no matter what, so the real margin is defensive: every round I avoid my predator's line is worth the same as a fourth of a hit, and I lost this episode entirely on the early rounds before I started tracking. I build the predator frequency table from round 1, not after the damage is done; with no data I hide at edges (1 or 9) rather than center cells, since untested opponents cluster mid-band.

I read the score deltas each round to confirm who was actually hit and whose fire patterns are changing; if my predator shifts their firing band, I shift my hiding band the next round rather than anchoring to old data.

I keep my reasoning short and put all of it into hide/fire choices; the claim line is a formality, and my fire reasoning stops once I have confirmed I am rotating cells and not converging on one number.