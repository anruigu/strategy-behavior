---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 2142
---
# Playbook for Sonar Picket

### General Strategy & Coordination
- The primary source of points is mutual escort claims (5 points each per round, yielding up to 30 points across 6 rounds). Always establish a mutual escort partner via notes immediately and stick to it every single round.
- Never output `[salvage: none]`. A mutual escort claim with another boat is worth +5 points per round; missing out on escort claims completely zeroes out potential gains.
- Follow standing orders for firing to maintain steady play unless an intentional deviation is coordinated.

### Stage-by-Stage Actions

#### 1. Note Stage
- In Round 1, check incoming notes. If another boat proposed an escort pact, agree immediately. If not, explicitly propose an escort partnership to one specific live boat: `[note: <Partner>, let us escort each other every round for mutual +5 points. I claim you, you claim me.]`
- In subsequent rounds, reaffirm the escort pact with that designated partner: `[note: <Partner>, confirming mutual escort for this round. I will submit [salvage: <Partner>].]`
- Keep notes direct, unambiguous, and focused on confirming the escort agreement.

#### 2. Escort Stage
- Always output `[salvage: <Partner>]` naming the agreed boat (or the boat that explicitly signaled an escort pact with me).
- Never select `[salvage: none]`.

#### 3. Hide Stage
- Choose a cell (1–9) unpredictably to evade incoming fire from the upstream station (Echo -> Foxtrot -> Gamma -> Echo).
- Avoid repeating the same cell consecutively to prevent the upstream shooter from zeroing in.

#### 4. Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <Standing_Target>] [fire: <cell>]`.
- Vary firing coordinates across rounds across likely evasion spots (cells 1–9).
- Do not fire at Harbor unless deliberately accepting elimination to siphon points.

#### 5. Claim Stage
- When asked to file a claim, always match the private office report exactly:
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.
- Public claims must match private results exactly.