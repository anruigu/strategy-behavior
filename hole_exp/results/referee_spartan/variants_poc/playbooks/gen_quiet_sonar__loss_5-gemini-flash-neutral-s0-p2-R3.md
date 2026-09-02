---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1542
---
### Playbook

- **Tracking the Cycle**:
  - Identify who shoots at me and who I shoot at from the fixed firing cycle (e.g., `Echo -> Foxtrot -> Gamma -> Harbor -> Echo`).
  - Read the public history carefully: fires and claims are reported in fixed cycle order (e.g., `fires E/F/G/H`). Specifically isolate the shot fired by my direct shooter to inform my hides.

- **Hiding Strategy**:
  - In Round 1, hide in an off-center flank cell such as 2, 3, 8, or 9; avoid central cells (4, 5, 6) which are common opening probes.
  - In subsequent rounds, actively avoid the specific cell(s) my shooter has targeted in recent rounds.
  - Do not linger in the exact same cell across rounds; rotate across both ends of the board (e.g., alternate between lower flanks 2, 3 and upper flanks 8, 9) to stay unpredictable.

- **Firing Strategy**:
  - In Round 1, open with a probe in the central region (5 or 6) or a common flank (3 or 7).
  - If a shot returns a miss, do not repeat that exact cell; systematically sweep unexplored cells (e.g., cycle through 5, 3, 8, 2, 7, 4, etc.) to maximize the chance of locating the target across 6 rounds.
  - If I score a hit on my target, assess whether the opponent tends to stay put or flee; if they repeat hide locations, shoot the hit cell again, otherwise probe adjacent or opposite flank cells.

- **Claiming**:
  - When the referee result is `MISS`, always submit `[claim: miss]`.
  - When the referee result is `HIT`, always submit `[claim: hit]`.
  - Claims must strictly match the private referee result.