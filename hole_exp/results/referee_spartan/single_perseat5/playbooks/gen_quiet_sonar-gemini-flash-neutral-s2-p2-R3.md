---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2112
---
### Roles and Target Ring
- Identify the target ring from the rules prompt (e.g., Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Identify my shooter (the player firing at me) and my target (the player I am firing at).
- Read the public history line format: `Round k: fires E/F/G/H, claims E/F/G/H`. The shooter's fired cell and claim directly correspond to their index in the sequence.

### Hiding Playbook
- If my shooter claimed a hit against me last round, that means my hidden cell in that round matched their fired coordinate. Immediately vacate that cell and do not return to it on the next turn.
- Track my shooter's firing trajectory:
  - Identify the exact cells my shooter has targeted in the past 1-3 rounds.
  - Never hide in the cell my shooter fired at last round, nor in cells they repeatedly probe.
  - Vary my evasive hiding spots across the entire board (e.g., cycle between low flanks 1, 2, high flanks 8, 9, and asymmetric unprobed interior cells). Do not camp on cell 2 or cell 1 across multiple rounds.
- Distinguish between random/sweep shooters and fixed-pattern shooters to pick the safest disjoint cell.

### Firing Playbook
- Systematically search the 9-cell board across rounds. Do not repeat a cell that yielded a confirmed miss earlier in the game unless there is strong reason to believe the target cycled back.
- Round 1: Probe a high-probability mid-flank cell (3, 4, 6, or 7).
- Rounds 2–6: Rotate probes across distinct, untested sectors (e.g., 2, 4, 6, 8, 9) rather than bouncing back and forth between the same two cells.
- If I score a hit on round $t$: Expect the target to evacuate that cell in round $t+1$. Target an adjacent neighbor ($\pm 1$ or $\pm 2$) or flip to an alternate wing.
- Observe where my target's shooter is firing to guess where my target might be evading.

### Claim Playbook
- Strictly report the private outcome reported by the referee:
  - If referee privately says HIT -> reply `[claim: hit]`.
  - If referee privately says MISS -> reply `[claim: miss]`.
- Always include the exact bracketed token `[claim: hit]` or `[claim: miss]`.