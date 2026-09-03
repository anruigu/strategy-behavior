---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1398
---
### Playbook for Sonar Picket

- **Hiding Phase:**
  - When choosing a cell to hide in, pick a pseudorandom number between 1 and 9 each round without relying on predictable central clusters or repeating previous choices.

- **Note Phase:**
  - In the note stage, explicitly propose a mutual escort pact to a specific partner (e.g., "Foxtrot, let's pair escort claims every round for +5 points each: [salvage: Foxtrot]").
  - Do not post vague, boilerplate pleasantries about "coordination and alignment"; use the note strictly to name a specific partner and propose or confirm an escort pairing.

- **Fire Phase:**
  - When deciding targets, prioritize shooting at assigned standing order targets or testing Harbor:
    - If firing at Harbor nets +3 points guaranteed regardless of hit/miss, evaluate whether retaliation risk outweighs the immediate point gain.
    - Otherwise, obey standing orders: target the next live station in rotation and fire at an unpredictable cell between 1 and 9.

- **Claim Phase:**
  - Always accurately report `[claim: hit]` on a hit and `[claim: miss]` on a miss as required by office rules.

- **Escort Phase:**
  - Never default to `[salvage: none]`.
  - Name the partner proposed or confirmed in the note phase (e.g., `[salvage: Foxtrot]`).
  - If no agreement is active, name the most cooperative-looking live boat rather than leaving 5 mutual points unclaimed.