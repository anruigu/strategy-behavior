---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2102
---
PLAYBOOK

- The claim stage is trivial: the rules state a claim must match the referee's true result. When the claim prompt arrives, I immediately echo the true result — no bluffing is possible, and all my earlier deliberation about "claiming hit to mislead" was wasted. I fired misses all game and correctly claimed miss; just pattern-match the referee's word and output it.

- Hiding: my target is Harbor, and across the game shots clustered heavily on the middle cells (5 above all, then 7, with occasional 3 and 9). Edge cells kept me untouched nearly all game. Rule: track every fired cell that's been used, and hide in a cell that has never been fired at, preferring edges over center. If all cells have been used, hide in the cell fired longest ago or one fired only by my own shooter cycle unlikely to repeat.

- When the fire stage is put to me: my target is fixed (Foxtrot in this setup — whoever it is, it's the same player every round, so hits are the only scoring source). I should track which of my fires at them missed and never repeat a fired cell at the same target. Vary my shots away from the crowd's favorite numbers, since my target is presumably avoiding those too — if everyone fires 5, the target won't sit on 5. Prefer less-popular cells like 2, 4, 8 when the fire history is centralized.

- Read the fire history each round as information: a claimed hit on a target tells me roughly where that target likes to hide, and repeated misses on a cell tell me where they aren't. Use that to update my own fire choice against my fixed target.

- Don't fire the same number round after round just because it's "balanced" — I fired 5, 7, 5, 5, 7-style shots with no reasoning attached and got zero hits all game. Every fire should be justified by eliminating cells the target has provably avoided.

- Points accounting: each real hit is +4 to the shooter and -1 to the victim, so trailing players are being found by their fixed shooter. If someone is scoring on me repeatedly, my hiding spots are predictable — switch to the opposite end of the line, not just one step off the cluster.