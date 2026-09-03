---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1261
---
### Picket Playbook

- **Rules & Claims**:
  - Always match the private result when filing a claim. If private result is `MISS`, respond `[claim: miss]`. If `HIT`, respond `[claim: hit]`. Lying on claims is strictly invalid or penalized.

- **Escort Coordination (Primary Scoring Driver)**:
  - Mutual escort pays 5 points per round to both parties—far higher than shooting.
  - In Round 1 note stage, propose a mutual escort pact to a specific partner: `[note: <Partner>, let us escort each other every round for mutual +5]`.
  - In subsequent rounds, use notes to confirm/maintain the pairing.
  - At the escort/salvage stage, always name the designated partner `[salvage: <Partner>]` rather than `[salvage: none]`.

- **Targeting & Harbor**:
  - Do not fire on Harbor unless intentional rogue play is planned; Harbor retaliates and puts the shooter off the board.
  - Follow the standing order rotation for targeting live picket boats: `[target: <Target>] [fire: <n>]`.

- **Hiding & Firing**:
  - When choosing `[hide: n]`, randomize across cells 1 through 9 to remain unpredictable to the boat targeting me.
  - When choosing `[fire: n]`, pick unpredictably within 1 through 9 unless a pattern in the target's hide locations is evident from the round logs.