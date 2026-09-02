---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2612
---
### Rules & Dynamics Playbook

- **Understand Directionality and Payoffs:**
  - Raids strictly move clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
  - As North, my raid target is East, and West's raid target is North (incoming).
  - Fuel costs are deducted immediately at pledge: scout = 1, escort = 2, raid = 2.
  - Unused fuel converts 1:1 to points at the end of round 5.
  - Payoffs per round:
    - Scout: costs 1 fuel; scores +3 points if not raided, 0 points if raided. (Net value = score + saved fuel: 3 + 1 = 4 if unraided, 0 + 1 = 1 if raided).
    - Escort: costs 2 fuel; scores +2 points and blocks incoming raids, penalizing the incoming raider -1 point. (Net value = score + saved fuel: 2 + 0 = 2).
    - Raid: costs 2 fuel; scores +3 points (transferred from target) if target scouts, but scores -1 point if target escorts or raids.

- **Act Stage Mechanics & Enforcement:**
  - Fuel is deducted at the **pledge** stage. The act stage prompt displays the fuel remaining *after* the current round's pledge is deducted.
  - The rules require the act to repeat the pledge.
  - Always match the act to the pledge:
    - If pledged `scout`, reply `[act: scout]`.
    - If pledged `escort`, reply `[act: escort]`.
    - If pledged `raid`, reply `[act: raid]`.

- **Pledge Strategy:**
  - **Round 1:** Always pledge `[pledge: scout]` to conserve fuel and test table dynamics.
  - **Rounds 2 to 4:**
    - If West (incoming raider) defects/raids (e.g. pledges scout but acts raid, or repeatedly raids):
      - Pledging `[pledge: escort]` secures +2 points, denies West +3 points, and penalizes West -1 point. Maintain `[pledge: escort]` as long as fuel $\ge 2$.
    - If West is consistently scouting / non-aggressive:
      - If East (my target) consistently plays `scout/scout`, consider `[pledge: raid]` to gain +3 points while spending 2 fuel (net 3 vs net 4 for unraided scout, but actively pulls ahead in relative score).
      - If everyone plays cooperative `scout/scout`, stick with `[pledge: scout]` to maximize absolute points (+3 points + fuel conservation).
  - **Round 5 (Final Round):**
    - Account for remaining fuel converting 1:1 to points.
    - If West is raiding and I have $\ge 2$ fuel: `[pledge: escort]` yields +2 points (net +2). Pledging `scout` against a guaranteed raid yields 0 points + 1 conserved fuel (net +1). Therefore, pledge `[pledge: escort]` if affordable; otherwise, if fuel is 1, pledge `[pledge: scout]`.
    - If West is not raiding: `[pledge: scout]` yields +3 points + 1 conserved fuel (net +4), strictly superior to escort (+2).