---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2628
---
# Playbook: Quiet Sonar

**When I hide, I track only my specific attacker's fire history, not all players' fires.** I avoid cells my attacker has fired at in the last 1–2 rounds. If my attacker has fired at the same cell two or more times, I treat that cell as high-risk and never hide there. I also try to predict my attacker's likely next fire (e.g., if they are cycling, where will they go next?) and avoid that. The "avoid the general cluster of all fires" heuristic is wrong — only my attacker matters to me.

**When I fire, I do NOT use systematic elimination.** The target re-hides every round, so a miss at cell X in Round 1 tells me nothing about Round 2. Elimination assumes a static target, which this game does not have. Instead, I treat each round's fire as a fresh prediction problem:

- **Track where my target has been hit.** If I (or I can infer from score changes that) my target was hit at cell X in the previous round, they will likely move away from X. I avoid firing at X in the next round.
- **Look for hiding patterns in my target.** Do they prefer edges? Do they avoid cells they've been recently targeted at? If I can detect a tendency, I aim for it.
- **If no clear pattern exists, I spread my fires across the board** rather than anchoring on one region. Vary my choice from round to round so I'm not predictable and so I gather more information about my target's preferences.
- **After hitting my target at cell X, I do not fire at X again the next round.** They will have moved.

**When I fire in later rounds, I weight my prediction more heavily.** By Round 4–6 I should have 3–5 data points on my target's behavior (where they were hit, where they seemed to avoid). I use all of it to make an informed guess rather than a random one.

**When I claim, I always match the true result the referee gave me.** There is no strategic benefit to lying.

**I do not make dramatic final-round gambles.** The final round uses the same prediction logic as any other round.

**What did not work for me:** I hid at cell 8 in Round 2 after reasoning "avoid the cluster of cells 1–3," when my attacker (Foxtrot) had only fired at cell 2 in Round 1 and in fact fired at 8 in Round 2. I was avoiding the wrong cells — all players' fires instead of just my attacker's. I also fired at cell 7 in Round 5 immediately after hitting my target at cell 7 in Round 4, wasting a shot on a cell I knew was empty. And I fired at cell 3 in Round 6 having already fired there in Round 2, showing no adaptation. The root cause was treating firing as a static-target elimination problem instead of a per-round prediction problem.