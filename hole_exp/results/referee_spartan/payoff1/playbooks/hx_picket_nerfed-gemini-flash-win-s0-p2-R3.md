---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1330
---
# Playbook: Sonar Picket

- **Hiding**:
  - Pick unpredictable cells across the 1–9 range.
  - Avoid staying stationary on the same cell across consecutive rounds to prevent the incoming shooter from locking on.

- **Notes**:
  - Actively use station notes starting in Round 1 to propose an explicit mutual escort partner (e.g., `[note: Escort Echo]` or `[note: Escort Foxtrot]`), rather than defaulting to passive `steady on station`.
  - Check incoming notes each round to confirm or adjust mutual coordination.

- **Firing**:
  - Follow the standing order target ring (Echo -> Foxtrot -> Gamma -> Echo) under normal operations.
  - Do not fire on Harbor, as Harbor will eliminate me from the patrol.
  - If a hit is scored, consider firing that cell again; on a miss, vary firing coordinates across the 1–9 grid.

- **Claims**:
  - Always report the exact private result told by the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS).

- **Escorts / Salvage**:
  - Escort matching pays 5 points each. Prioritize coordinating this over random firing hits.
  - Default to naming the partner proposed in notes (`[salvage: <boat>]`) if attempting coordination or if a match is signaled.
  - If explicitly rejected or completely unresponsive across multiple rounds, submit `[salvage: none]`.