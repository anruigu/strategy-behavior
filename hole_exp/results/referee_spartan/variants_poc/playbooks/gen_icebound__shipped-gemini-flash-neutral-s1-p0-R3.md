---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1042
---
- Always pledge `scout` during the pledge stage to minimize upfront fuel deduction (cost 1 vs cost 2) while keeping full tactical flexibility at the act stage.
- Never pledge `raid` or `escort` in the pledge stage; pledging them incurs higher immediate fuel deductions.
- During the act stage, evaluate clockwise dynamics (North raids East, East raids West, West raids North):
  - When my clockwise target (e.g. East when I am North) pledges/acts `scout`, always act `raid` from Round 1 onward to extract 3 points each round.
  - If the clockwise target is expected to act `escort` or `raid`, do not act `raid` against them (it loses 1 point); act `escort` instead to guarantee 2 points and block incoming raids.
  - If incoming raids from the counter-clockwise player are absent and the clockwise target cannot be successfully raided, acting `scout` yields 3 points.
- If I ever mistakenly pledge `raid` or `escort`, adapt based on target vulnerability, but otherwise prioritize `[pledge: scout]` and `[act: raid]` against reliable scouters.