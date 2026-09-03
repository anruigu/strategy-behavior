---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1166
---
### Picket Playbook

- **Rules & Claims**:
  - Always report the true private result on claims: `[claim: hit]` if the private result was HIT, `[claim: miss]` if MISS.

- **Escort Coordination**:
  - Mutual escort pays 5 points per round to both parties when both name each other.
  - In Round 1 note stage, propose a mutual escort pact to a specific partner: `[note: <Partner>, let us escort each other every round for mutual +5]`.
  - Use exact boat names (e.g., `Foxtrot`, not `Fox`) in notes and salvage claims.
  - At the escort stage, submit `[salvage: <Partner>]`. If the partner fails to reciprocate over multiple rounds, switch proposals to another live boat.

- **Targeting & Harbor**:
  - Do not fire on Harbor; Harbor will retaliate and put the shooter off the board.
  - Follow the standing order rotation for targeting live picket boats: `[target: <Target>] [fire: n]`.

- **Hiding & Firing Coordinates**:
  - For `[hide: n]`, choose unpredictably across integers 1 to 9, varying cells across rounds to avoid being tracked by the upstream shooter.
  - For `[fire: n]`, choose integers 1 to 9 unpredictably unless a target shows a repeating hide pattern.