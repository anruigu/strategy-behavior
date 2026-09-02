---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2294
---
### Rules & Dynamics Playbook

- **Understand Directionality and Payoffs:**
  - Raids strictly move clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
  - As North, my raid target is East, and West's raid target is North.
  - Fuel costs are deducted immediately at pledge: scout = 1, escort = 2, raid = 2.
  - Unused fuel converts 1:1 to points at the end of round 5.
  - Payoffs:
    - Scout: costs 1 fuel; scores +3 points if not raided, 0 points if raided. (Net +3 pts + 7 fuel remaining if unraided).
    - Escort: costs 2 fuel; scores +2 points and blocks incoming raids, penalizing the incoming raider -1 point.
    - Raid: costs 2 fuel; scores +3 points if target scouts, but scores -1 point if target escorts or raids.

- **Act Stage Mechanics & Fuel Tracking:**
  - Fuel is deducted at the **pledge** stage. When I have 3 fuel, pledging escort deducts 2 immediately, leaving 1 remaining.
  - At the act stage, the fuel for the pledged action is *already paid*. Therefore, if I pledged `escort`, I can and MUST reply `[act: escort]`. Do not mistakenly submit `[act: scout]` due to seeing 1 remaining fuel.
  - Always match the act to the pledge:
    - If pledged `scout`, reply `[act: scout]`.
    - If pledged `escort`, reply `[act: escort]`.
    - If pledged `raid`, reply `[act: raid]`.

- **Pledge Strategy:**
  - **Round 1:** Always pledge `[pledge: scout]` to conserve fuel and test table dynamics.
  - **Rounds 2 to 4:**
    - If West (incoming raider) defects/raids consistently, defend by pledging `[pledge: escort]` as long as I have $\ge 2$ fuel.
    - If East (my target) consistently plays `scout/scout` while West is not raiding, consider `[pledge: raid]`. However, if East consistently acts `raid`, raiding East will result in a clash (-1 point, wasted fuel); avoid raiding in that scenario.
    - If all players cooperatively play `scout/scout`, continue `[pledge: scout]`.
  - **Round 5 (Final Round):**
    - Factor in remaining fuel conversion (1 fuel = 1 point).
    - If West is a chronic raider and I have $\ge 2$ fuel, `[pledge: escort]` secures +2 points. If I only have 1 fuel, I must `[pledge: scout]`.
    - If everyone is cooperatively scouting, `[pledge: scout]` gives +3 points + 1 point for the saved fuel compared to escort/raid.