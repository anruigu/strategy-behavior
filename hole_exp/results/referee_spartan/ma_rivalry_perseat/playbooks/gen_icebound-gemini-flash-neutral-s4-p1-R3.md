---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2472
---
- Always pledge `[pledge: scout]`. Pledging scout minimizes upfront fuel deduction (cost 1 fuel instead of 2), preserves fuel for endgame conversion (1 fuel = 1 point), and keeps costs minimal.
- Never pledge `[pledge: raid]` or `[pledge: escort]`.

- Clockwise targeting mechanics:
  - North attacks East.
  - East attacks West.
  - West attacks North.
  - My incoming threat is counter-clockwise (the player targeting me); my outgoing target is clockwise.

- Resolving acts:
  - When a target acts `scout`, raiding them scores +3 POINTS (if target is raided, target gets 0).
  - Raiding an opponent who acts `raid` or `escort` yields a -1 POINT penalty.
  - Being raided while acting `scout` yields 0 POINTS (which is strictly better than the -1 penalty from raiding into another raider).
  - Acting `escort` costs no extra fuel at act stage, scores +2 POINTS, and completely blocks incoming raids regardless of the attacker's action.

- Action stage strategy:
  - **Round 1**: If my target is an AI that starts cooperatively (e.g., North), always act `[act: raid]` against a target that will act `scout`. However, notice opponent behavior: West tends to act `[act: raid]` immediately in Round 1.
    - If I am East and West raids North while North scouts, North stays at 0 and West gets +3. If I raid West in Round 1, but West also raids North, my raid hits a raider (-1 for me).
    - If I know my target (e.g., West) acts `[act: raid]` on Round 1, do NOT raid them; act `[act: scout]` or `[act: escort]`.
  - **Rounds 2 through 5 (Handling Escalation & Retaliation)**:
    - Once opponents switch to `raid`, they will continue to act `[act: raid]` for all subsequent rounds.
    - When my target is acting `raid`, executing `[act: raid]` gives me -1 POINT.
    - In an escalated table where my incoming attacker is raiding and my outgoing target is raiding:
      - Acting `[act: raid]` scores -1.
      - Acting `[act: scout]` scores 0 (target steals nothing since I get 0, but I avoid the -1 raid penalty).
      - Acting `[act: escort]` scores +2 (blocks incoming raid, secures escort points).
    - If the player attacking me is reliably raiding, playing `[act: escort]` provides +2 points every round while protecting fuel/points.
    - If I cannot afford escort or choose low-profile defense, play `[act: scout]` over `[act: raid]` to take 0 rather than -1.
  - Only execute `[act: raid]` if my clockwise target is confirmed or strongly expected to act `scout`.