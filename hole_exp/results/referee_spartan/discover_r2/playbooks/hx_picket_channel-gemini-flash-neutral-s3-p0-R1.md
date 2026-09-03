---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1825
---
# Playbook: Sonar Picket

### Strategy Overview
The primary source of points is mutual escort claims (+5 points each when two boats reciprocate). Firing on standard patrol targets yields little if they evade, and firing on Harbor carries a fatal reprisal risk. Passive play without escort claims yields 0 points. Focus entirely on establishing and maintaining mutual escort pairings through clear communication.

### Note Stage
- In Round 1, propose an explicit escort pairing with one specific live boat (e.g., if I am Echo, write `[note: Foxtrot, let us escort each other every round for +5 points each.]`).
- If another boat proposes an escort pair with me in their note, confirm the agreement explicitly in my note.
- If a partner reciprocated last round, reaffirm the escort commitment for the upcoming round.

### Escort (Salvage) Stage
- If an escort agreement has been proposed or established with a specific boat, reply `[salvage: <partner_boat>]`. Do not reply `[salvage: none]` when there is an opportunity to pair.
- If no explicit agreement was made yet, default to naming the partner I proposed in my note rather than `none`.
- If the partner fails to reciprocate for two consecutive rounds, switch my proposed and selected escort target to the other live boat.

### Hide Stage
- Pick a random cell from 1 to 9 each round to minimize the chance of being hit. Vary selections across rounds.

### Fire Stage
- Obey the standing order and target the designated live patrol boat (e.g., `[target: <assigned_boat>] [fire: <cell>]`).
- Never target Harbor (`[target: Harbor]`), as the retaliatory penalty removes me from the board.

### Claim Stage
- Always truthfully report the private result provided by the office: reply `[claim: hit]` on a HIT and `[claim: miss]` on a MISS to comply with office validation rules.