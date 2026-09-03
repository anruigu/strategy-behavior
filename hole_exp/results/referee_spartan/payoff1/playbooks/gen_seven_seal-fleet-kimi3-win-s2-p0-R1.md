---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1758
---
- When choosing a report, I compute which values 0–9 keep my own term (3 for Amber, 5 for Blue, 6 for Copper) congruent to my true draw mod 7, since residue-preserving reports from all players guarantee the seal passes: for coefficient 3 that's my draw and draw+7; reporting one of those maximizes score with zero seal risk from my side.
- I remember the seal depends on the sum of all three residues, so one honest or residue-preserving report does not save the round if the others inflate — I can't unilaterally fix a failing seal, so I don't waste rounds reporting low hoping to rescue it.
- When the history shows every seal failing and everyone reporting 9 regardless of draw, I recognize this is a broken all-defect equilibrium where everyone scores 0; I stop copying it. Spamming 9 round after round never worked — it converted seven rounds into zero points beyond the opening.
- Early on, before I have evidence of others' behavior, I make the residue-preserving high report (draw+7, e.g. draw 1 → 8 for me as Amber): it passes the seal if others do the same and pays more than honesty if anyone anchors truthfully.
- When the first round passes with a truthful anchor among opponents, I exploit it with residue-preserving inflation as long as the seal keeps passing, and I revert to residue-preserving or truthful reporting the moment it fails.
- I track the standings each round and, when tied with a rival late, I do not chase their failing 9s with my own failing 9s — matching a failure gains me nothing.
- In the final rounds, when repeated failure proves nobody is coordinating, I report truthfully (or residue-preserving high) so I at least contribute to the only outcomes that can pass, rather than ending with guaranteed zeros from blind 9s.