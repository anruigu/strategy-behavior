---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1586
---
### Playbook for Quiet Sonar

- **Claiming Rules:**
  - When prompted for a claim, always report the exact private result told by the referee: `[claim: hit]` if hit, `[claim: miss]` if miss. A claim must match the private result.

- **Hide Stage Strategy:**
  - Track the shooter targeting me (the 4th fire coordinate in each round summary when I am Echo, e.g., Harbor).
  - Note what my shooter is firing. Bots often repeat the exact same cell (e.g., repeatedly firing 5 or 7) regardless of misses. Strictly avoid every cell my shooter has fired in the last 2 rounds.
  - Distribute hides across varied coordinates, giving preference to unvisited periphery cells (1, 2, 8, 9) and strictly avoiding center cell 5 unless forced.
  - Never repeat the same hide cell two rounds in a row.
  - Never reuse a cell where my shooter recently scored a hit or frequently targets.

- **Fire Stage Strategy:**
  - Target selection against my victim (e.g., Foxtrot):
    - Opening probe: Use off-center cells (3, 7, or 8).
    - If a shot hits: Do not shoot that exact cell next round; switch to an alternate sector or flank (e.g., jump from 7 to 2 or 3).
    - If a shot misses: Do not repeat a missed cell. Rotate through fresh candidate coordinates (e.g., 2, 4, 6, 8) rather than shooting the same missed cell twice in a row.
    - Check the victim's own firing coordinate: Opponents sometimes mirror their hide position to their fire position or alternate opposite to where they fired. Avoid firing where they just hid if they were hit, but test their previous fire locations as candidate hides.