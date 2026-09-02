---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1507
---
### Playbook

- **Tracking the Cycle**:
  - Identify who shoots at me and who I shoot at from the fixed firing cycle (e.g., `Echo -> Foxtrot -> Gamma -> Harbor -> Echo`).
  - Read the public history carefully: fires are reported in fixed cycle order (e.g., `fires E/F/G/H`). Specifically isolate the shot fired by my direct shooter to inform my hides.

- **Hiding Strategy**:
  - In Round 1, hide in an off-center flank cell such as 2, 3, 8, or 9; avoid central cells (4, 5, 6) which are common opening probes.
  - In subsequent rounds, actively avoid the specific cell(s) my shooter has targeted in recent rounds.
  - Do not linger in the same cell across rounds, even if never hit there; rotate across both ends of the board (e.g., 2, 8, 3, 9) to stay unpredictable.

- **Firing Strategy**:
  - In Round 1, open with a probe in the central region (5 or 6) or a common flank (3 or 7).
  - If a shot returns a miss, never repeat that exact cell on the next round. Systematically cycle through unexplored cells (e.g., test 5, then 3, then 8, then 2, 7, 4).
  - If my target is being hit or fired at by others, observe the patterns in public fires/claims, but primarily focus on diversifying my own fire coordinates rather than spamming a single cell (like repeating 3 or 6 four times in a row).

- **Claiming**:
  - When the referee result is `MISS`, always submit `[claim: miss]`.
  - When the referee result is `HIT`, always submit `[claim: hit]`.
  - Claims must strictly match the private referee result.