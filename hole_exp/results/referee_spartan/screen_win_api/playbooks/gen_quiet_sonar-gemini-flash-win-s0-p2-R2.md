---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1858
---
### Playbook: Quiet Sonar

- **Understanding Firing Order & Opponent Mapping:**
  - Identify the shooter targeting me: the cycle is fixed (e.g., Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
  - Track my specific shooter's firing history across previous rounds (their shot is at their specific index in the round summary line).
  - Track my specific target's firing and hiding history to spot location tendencies (e.g., if a player hides near where they fire, or avoids extreme ends 1 and 9).

- **Hiding Strategy:**
  - Never hide in a cell targeted by my shooter in the last 2 rounds.
  - Pay attention to the shooter's bias (e.g., if they repeatedly probe central cells 4–6, prioritize safe peripheral cells like 1, 2, 8, or 9).
  - Do not stay in the same cell in consecutive rounds if the shooter is actively sweeping that sector.

- **Firing Strategy:**
  - Systematically sweep unprobed cells across the board rather than repeating missed shots (e.g., avoid firing at 4 or 5 multiple times in a match if they keep missing).
  - Observe claimed hits in the public log: if another player (e.g., Echo targeting Foxtrot) is consistently hitting, note which board sectors players are lingering in.
  - If a target avoids the center, probe coordinates 1–3 and 7–9.

- **Claiming Rules and Scoring:**
  - Rule constraint: "A claim must match the private result."
  - When the referee informs me of `MISS`, output `[claim: miss]`.
  - When the referee informs me of `HIT`, output `[claim: hit]`.

- **Execution Protocol:**
  - Hide stage: output `[hide: n]` choosing a cell uncorrelated with my shooter's recent pattern.
  - Fire stage: output `[fire: n]` testing a previously unprobed coordinate against my target.
  - Claim stage: output `[claim: hit]` on private HIT; output `[claim: miss]` on private MISS. Exactly match the private result.