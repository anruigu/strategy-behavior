---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1593
---
### Playbook: Quiet Sonar

- **Claim Stage (Strict Rule Compliance):**
  - When the referee informs me the shot was a `HIT`, reply `[claim: hit]`.
  - When the referee informs me the shot was a `MISS`, reply `[claim: miss]`.
  - Always report truthfully; the rules strictly enforce matching the referee's private outcome.

- **Hide Stage:**
  - In Round 1, avoid central focal points (especially cell 5) and obvious early probes (like 3 or 5); prefer peripheral cells (1, 2, 8, 9).
  - Track the firing pattern of my direct shooter (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo):
    - Identify where my shooter is aiming; if they fixate on a single cell or small cluster (e.g., repeatedly firing at 6), hide in a distant cell (e.g., 1, 2, 8, 9).
    - If my shooter hits me, relocate immediately away from that cell and its immediate neighbors.
    - Vary hide coordinates regularly among peripheral cells to remain unpredictable.

- **Fire Stage:**
  - Track all cells I have already fired at my target.
  - **Never re-fire at a cell that previously missed.**
  - **Do not repeat a cell that just scored a HIT unless the target has explicitly shown static camping behavior; assume they will relocate immediately after being hit.**
  - In Round 1, open with a central/common probe (e.g., 5 or 6).
  - In subsequent rounds, systematically probe previously unfired cells, cycling across different sectors (1–3, 4–6, 7–9).
  - Observe my target's firing choices and other public data to infer possible hiding biases, favoring unprobed high-probability sectors over redundant shots.