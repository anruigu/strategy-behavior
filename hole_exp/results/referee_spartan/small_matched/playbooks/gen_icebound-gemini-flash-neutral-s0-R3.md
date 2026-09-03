---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1186
---
### Playbook for Icebound

- **Pledge Stage:**
  - Always submit `[pledge: scout]` in every round regardless of player position, remaining fuel, or previous round history.
  - Pledging scout only deducts 1 fuel upfront while preserving complete tactical flexibility and concealing intent.
  - Never pledge `raid` or `escort` directly.

- **Act Stage:**
  - **Rounds 1–2:**
    - If the counter-clockwise player has not raided me, submit `[act: scout]` to harvest 3 points cleanly while maintaining fuel.
    - If the counter-clockwise player is expected to raid or has shown immediate aggression, submit `[act: escort]`.
  - **Rounds 3–5:**
    - If my clockwise target pledged `scout`, defect and submit `[act: raid]`. This gains +3 points (stealing from target) while having only paid 1 fuel for the pledge.
    - If my clockwise target pledged `escort` or `raid`:
      - If the counter-clockwise player is likely to raid, submit `[act: escort]`.
      - Otherwise, submit `[act: scout]`.

- **Formatting Rules:**
  - Output at most one short line of reasoning followed immediately by the bracketed action token (`[pledge: scout]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`).