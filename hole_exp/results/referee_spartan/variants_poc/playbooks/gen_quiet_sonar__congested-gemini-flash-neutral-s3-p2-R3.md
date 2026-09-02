---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1956
---
### Playbook for Quiet Sonar

#### Hiding
- Identify who is shooting at me based on the fixed target ring (Echo $\to$ Foxtrot $\to$ Gamma $\to$ Harbor $\to$ Echo). For instance, when I am Gamma, Foxtrot is my shooter (2nd position in the fire list: Echo/Foxtrot/Gamma/Harbor).
- Notice that opponents with high hit rates often predict simple deterministic dodging patterns (e.g., alternating between 2, 5, and 8, or picking the current round's unused digits). Break predictability by adopting high-entropy hiding selections across the entire board (1 through 9).
- Check the recent history of my shooter's firing coordinates:
  - Identify all cells my shooter has targeted in the past 3 rounds.
  - Actively evade those recently fired coordinates, but avoid falling back to the exact same "safe" numbers every alternate round.
  - Do not reuse the same hiding spot two rounds in a row unless testing a completely stationary bot.
- Edge cells (1, 9) and asymmetric off-center cells (e.g., 2, 8, 3, 7) are viable, but must be randomized across rounds to prevent shooters from locking onto a repeating sequence.

#### Firing
- Identify my assigned target in the ring (e.g., as Gamma, my target is Harbor, the 4th player).
- Track previous fires against my target to ensure I do not re-probe cells that were already confirmed misses, unless cycling after exhausting all 9 cells.
- Systematically sweep through candidate cells across the line (1 through 9). Check the public fires and hits if any information about my target's past hiding positions is revealed.
- If my target was previously hit at a specific cell $c$, do not fire at $c$ on the very next round unless they have proven to never relocate. Prioritize adjacent or complementary unprobed positions.

#### Claiming
- When the referee returns `HIT`, always submit `[claim: hit]`.
- When the referee returns `MISS`, always submit `[claim: miss]`. Claims must strictly match the private referee result.