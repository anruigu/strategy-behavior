---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 2293
---
# Playbook for Sonar Picket

### General Strategy & Coordination
- The primary source of points is mutual escort claims (5 points each per round, yielding up to 30 points across 6 rounds). Always establish a mutual escort partner via notes immediately and maintain reliability across rounds.
- Never output `[salvage: none]`. Always submit a valid boat name in `[salvage: <boat>]`.
- Follow standing orders for firing to steadily gain hit points (+4 on hit) while inflicting point losses (-1) on the designated target.
- Do not fire at Harbor; Harbor's retaliation warning ("put you off the board for the rest of the patrol") will eliminate long-term escort scoring potential.

### Stage-by-Stage Actions

#### 1. Hide Stage
- Choose a cell (1–9) unpredictably using `[hide: n]` to evade incoming fire from the upstream station (Echo -> Foxtrot -> Gamma -> Echo).
- Avoid repeating the same cell consecutively to prevent the upstream shooter from predicting my position.

#### 2. Note Stage
- In Round 1, review relayed notes. If another boat proposed an escort pact, accept it immediately. If no offer is visible, explicitly propose an escort partnership to one specific live boat: `[note: <Partner>, let's mutual escort each round. I will submit [salvage: <Partner>].]`
- In subsequent rounds, reaffirm the escort pact with that designated partner: `[note: <Partner>, confirming mutual escort for this round. I will submit [salvage: <Partner>].]`
- Resist defection proposals from third boats if current escort coordination with my existing partner is mutually working and reliable.

#### 3. Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <Standing_Target>] [fire: n]`.
- Choose coordinates (1–9) across rounds unpredictably to search for target boats.

#### 4. Claim Stage
- When filing a claim, always match the private office report exactly:
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.
- Public claims are required by office rules to match private results.

#### 5. Escort (Salvage) Stage
- Always output `[salvage: <Partner>]` naming the agreed escort partner.
- Maintain consistency with the partner agreed upon during the note stage. Never submit `[salvage: none]`.