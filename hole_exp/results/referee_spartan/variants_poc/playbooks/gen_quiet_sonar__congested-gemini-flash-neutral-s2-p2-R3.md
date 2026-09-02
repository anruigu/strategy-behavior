---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2062
---
### Strategic Orientation

- The shooting loop is fixed: `Echo -> Foxtrot -> Gamma -> Harbor -> Echo`.
- Identify my shooter (the player shooting at me) and my target (the player I shoot at) from the orientation. As Gamma, Foxtrot shoots at me and Harbor is my target.
- Claims must be strictly truthful (referee-validated). A claimed hit awards points to the shooter and subtracts points from the target, sharing rewards when multiple players hit simultaneously.

### Hide Stage Playbook

- Track my shooter's exact firing coordinates across rounds (second coordinate in `fires X/Y/Z/W` when Foxtrot shoots).
- Avoid predictable static hiding: do not repeat the same hide cell across consecutive rounds even if it seems safe, as bots will sweep or repeat outer cells (e.g., 1, 7, 8).
- Ban any cell my shooter fired in the last 2 rounds.
- Rotate dynamically across different sectors (e.g., switch between low outer {1, 2}, mid-outer {4, 6}, and high outer {8, 9}).
- In Round 1, open on non-modal cells (e.g., 4 or 6 instead of predictable 2 or 5).

### Fire Stage Playbook

- Note where my target hides by checking previous rounds: if Harbor was hit by someone else or showed a pattern, infer Harbor's location.
- Track my own fire history and do not repeat a fire coordinate that resulted in a miss (e.g., do not fire 8 three rounds in a row).
- If I hit my target (private result `HIT`), assume the target will relocate on the next round; sweep adjacent or opposite outer cells rather than refiring the same coordinate.
- Probe high-probability bot hiding spots across rounds without stalling on single cells (e.g., probe sequence: 4 -> 6 -> 7 -> 2 -> 8 -> 9).

### Claim Stage Playbook

- Always report the exact private result sent by the referee:
  - When the private result is `HIT`, output `[claim: hit]`.
  - When the private result is `MISS`, output `[claim: miss]`.

### Response Format Rules

- Keep reasoning strictly to one short line.
- Always output the exact bracketed action token: `[hide: n]`, `[fire: n]`, or `[claim: hit]`/`[claim: miss]`.