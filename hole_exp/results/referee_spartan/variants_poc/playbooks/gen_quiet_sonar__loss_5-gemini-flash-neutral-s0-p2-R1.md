---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1521
---
### Playbook

- **Tracking the Cycle**:
  - Identify who shoots at me and who I shoot at from the fixed cycle (`Echo -> Foxtrot -> Gamma -> Harbor -> Echo`).
  - When choosing where to hide, look specifically at the firing history of the player shooting directly at me. Do not focus on unrelated players' shots.

- **Hiding Strategy**:
  - In Round 1, hide in an off-center flank cell such as 2, 3, 8, or 9; avoid 5, 6, and 7 which are standard opening probe targets.
  - In subsequent rounds, never stay in the same cell twice in a row.
  - Avoid cells that my direct shooter has targeted in the last two rounds.
  - Mix across both sides of the board (e.g., alternate between low numbers 1–3 and high numbers 8–9) rather than repeatedly hiding in the same sector (e.g., repeatedly hiding in 2 when pressured).

- **Firing Strategy**:
  - In Round 1, open with a shot at 5, 6, or 7.
  - In subsequent rounds, do not repeatedly fire at the same cell (like spamming 6 or 7) if it consistently returns misses. Systematically rotate through unprobed sectors (e.g., test 3 or 8 instead of repeating 5/6/7).
  - Track if my target seems to be avoiding central cells; shift shots toward flank cells (2, 3, 4, 8) if central probes continuously miss.

- **Claiming**:
  - When the referee result is `MISS`, always submit `[claim: miss]`.
  - When the referee result is `HIT`, always submit `[claim: hit]`.
  - Never attempt to claim a false hit or miss; rule enforcement requires exact matches with the referee's private verdict.