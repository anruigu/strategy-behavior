---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1624
---
### Playbook: Quiet Sonar

- **Rule Enforcement**: Always submit `[claim: hit]` on a hit and `[claim: miss]` on a miss; never attempt to fabricate a claim since the referee enforces strict adherence to the private result.

- **Hiding Strategy**:
  - Identify who shoots at me (e.g. Harbor shoots at Echo in the fixed ring) and rigorously monitor their exact shot history.
  - Never hide in any cell my shooter has fired at in the last 2-3 rounds, especially cells they repeat.
  - Do not hide in cells that were hit anywhere on the board last round, as bots often copy successful coordinates.
  - Never hide in the same cell twice in a row, and avoid obvious symmetric counter-picks (e.g. consistently picking 7 when avoiding 3/5).
  - Prefer truly dispersed, low-salience cells (e.g., 2, 6, 8, 9) rather than defaulting heavily to 1 or 7.

- **Firing Strategy**:
  - Systematically sweep unprobed cells against my target (e.g., Foxtrot) rather than re-firing misses; never repeat a cell I already fired and missed unless all 9 have been tested.
  - Track my target's own firing behavior and hiding tendencies: if they favor certain regions (edges vs. center), adjust sweep priority accordingly.
  - If a hit is confirmed on a target, assume they will flee; do not fire at the same coordinate on the immediate next round. Switch to an unprobed distant or adjacent cell.
  - If my target is being hit repeatedly by someone else, or if I notice other shooters scoring hits, use those public hit coordinates on the subsequent rounds as candidate targets if the target tends to be static, or explicitly avoid them if they evade.