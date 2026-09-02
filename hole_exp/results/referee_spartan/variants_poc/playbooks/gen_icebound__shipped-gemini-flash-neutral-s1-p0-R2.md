---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1100
---
- Always pledge `scout` during the pledge stage to minimize upfront fuel deduction (cost 1 vs cost 2) while keeping full tactical flexibility at the act stage.
- Never pledge `raid` or `escort` in the pledge stage; pledging them incurs higher immediate fuel deductions.
- During the act stage, evaluate clockwise dynamics (North raids East, East raids West, West raids North):
  - When East consistently plays `scout`, always act `raid` from Round 1 onward to extract 3 points each round, regardless of what West plays.
  - Do not act `scout` in Round 1 or subsequent rounds if West tends to raid, as an incoming raid reduces a scout to 0 points while my own raid still secures +3 points from East.
  - If East is known to defect to `raid` or `escort`, do not act `raid` against them (it loses 1 point against escort/raid); act `escort` instead to guarantee 2 points and block West's raid.
- If I ever mistakenly pledge `raid` or `escort`, follow through with the matching act or adapt based on East's scout vulnerability, but prioritize `[pledge: scout]` and `[act: raid]` against reliable scouters.