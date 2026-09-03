---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1498
---
# Sonar Picket Playbook

- **Boats and Roster**:
  - The live boats are strictly Echo, Foxtrot, and Gamma (plus Harbor). Non-existent names like "Delta" or "Beta" do not exist and must never be referenced, messaged, or named in salvage.

- **Escort Claims**:
  - The highest consistent point source is the mutual escort bonus (+5 points each round).
  - Never default to `[salvage: none]`.
  - In a 3-boat ring, two boats will pair up (e.g. Echo and Foxtrot). Actively break into the pairing by proposing to one specific live boat in notes (e.g., "Foxtrot, let's escort each other this round for +5").
  - In the escort stage, name the boat I explicitly offered to or agreed with (`[salvage: Echo]` or `[salvage: Foxtrot]`). Never name non-existent boats.

- **Notes Stage**:
  - Address only active, valid boats in the game (Echo or Foxtrot).
  - State concrete proposals: offer a mutual escort pairing every round to secure the +5 bonus.

- **Firing and Claims**:
  - Follow standing orders (`[target: <boat>] [fire: n]`) unless coordinating a deliberate alternative.
  - Do not fire at Harbor; the retaliation eliminates me from the board.
  - When the claim prompt arrives, strictly match the private result reported by the office (`[claim: hit]` if told hit, `[claim: miss]` if told miss). Falsely claiming a hit when told miss is invalid.

- **Hiding**:
  - Randomize hide coordinates across 1 to 9 each round to evade incoming fire from the upstream station. Vary firing coordinates as well.