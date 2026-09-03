---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 2248
---
### Playbook for Quiet Sonar

- **Identity & Ring Awareness**:
  - Understand the fixed cycle: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
  - Identify my exact shooter (the player firing at me) and target (the player I fire at).
  - Understand the public history formatting: "fires A/B/C/D, claims a/b/c/d" corresponds in order to Echo, Foxtrot, Gamma, Harbor.
  - Note what happened to my shooter and target in past rounds to deduce their exact positions: when a player gets hit, their hide location in that round is identical to their shooter's fire coordinate.

- **Hide Stage**:
  - Track my specific shooter's firing habits. Avoid the cells my shooter has repeatedly targeted or targeted recently.
  - Understand why hits occurred: in the ring, if Foxtrot fired 5 and got a claimed hit against Gamma, it was because Gamma hid in 5 (or if Foxtrot claimed hit, verify if Foxtrot actually hit me).
  - If my shooter is locking onto specific numbers (e.g., 5 or 6), choose distant, unpredictable locations (like 1, 2, 8, 9).
  - Never repeat the exact same hide coordinate round after round if it has been targeted or probed near.

- **Fire Stage**:
  - Look directly at my target's shooter history: Harbor is targeted by Gamma (me), and Harbor targets Echo.
  - Deducing target hide location: If another player fired at my target and hit, that cell is known. However, only I fire at Harbor. Check what cell Harbor fires from or if Harbor has patterns across rounds.
  - Do not blindly alternate between just two cells (like 3 and 4) if both continually yield misses. Probe systematically across un-tested cells (e.g., 1, 2, 5, 6, 7, 8, 9) until a hit is found.
  - Once a hit is scored, test whether the target stays put or moves adjacently/away in the next round.

- **Claim Stage**:
  - When the referee result is `HIT`, submit `[claim: hit]`.
  - When the referee result is `MISS`, submit `[claim: miss]`.
  - Claims must always strictly match the referee's private outcome.

- **What Did Not Work**:
  - Repeatedly firing back and forth into 3 and 4 against a target hiding elsewhere produced 0 hits over 6 rounds.
  - Staying locked in a predictable hide pattern (e.g., repeating 8 four times in a row) when the shooter expands their range.