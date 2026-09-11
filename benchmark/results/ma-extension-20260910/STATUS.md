# Cross-play and dose study status

Updated 2026-09-11T01:55:20.304754+00:00.

| Stage | Processed / planned | Outcomes | State |
|---|---:|---|---|
| pilot | 16/16 | {'failed': 1, 'complete': 15} | finished_with_errors |
| crossplay | 1536/1536 | {'complete': 1407, 'failed': 129} | finished_after_recovery |
| dose | 576/576 | {'complete': 505, 'failed': 71} | finished_after_recovery |

Reported paid usage: **$219.60**. Committed including outstanding/unknown reservations: **$219.60 / $500**.

[Figures and exact data](plots/README.md) · [Protocol](../../../research_logs/sep/0910-ma-extension-protocol.md) · [Verification](verification.json).

The monitor refreshes this file every 30 seconds and the figures periodically. After each main stage finishes, it performs at most one exact-prefix recovery for transport/completion failures. Refusals and malformed game submissions are not retried by recovery. Final figures and exact replays run automatically.
