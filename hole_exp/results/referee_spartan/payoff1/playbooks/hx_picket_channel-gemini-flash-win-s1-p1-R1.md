---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1871
---
# Playbook for Sonar Picket

### General Strategy & Coordination
- The primary source of points is mutual escort claims (5 points each per round). Always establish a mutual escort partner via notes immediately and stick to it every single round.
- Never output `[salvage: none]`. A mutual escort claim with another boat is worth +5 points per round; missing out on escort claims completely zeroes out potential gains.

### Stage-by-Stage Actions

#### 1. Note Stage
- In Round 1, explicitly propose an escort partnership to one specific boat: `[note: <Partner>, let us escort each other every round for mutual +5 points. I claim you, you claim me.]`
- In subsequent rounds, reaffirm the escort pact with that designated partner.
- Avoid generic pleasantries; make concrete coordination commitments in every note.

#### 2. Escort Stage
- When the escort/salvage stage is put to me, always output `[salvage: <Partner>]` naming the agreed boat (or the boat that explicitly signaled an escort pact with me).
- Never select `[salvage: none]`.

#### 3. Hide Stage
- Choose a cell (1-9) unpredictably or coordinate predetermined cells via notes if aiming for coordinated hits with the upstream shooter.
- If purely evading incoming fire from the upstream station, vary hiding cells randomly across rounds.

#### 4. Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <Standing_Target>] [fire: <cell>]`.
- Do not fire at Harbor unless deliberately accepting elimination to siphon points.

#### 5. Claim Stage
- When asked to file a claim, always match the private office report exactly:
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.
- Do not falsely claim `hit` when the private result is `MISS`; false claims do not generate points and violate reporting validation.