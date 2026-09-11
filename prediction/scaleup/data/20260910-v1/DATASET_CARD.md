# Parameterized behavioral dataset

Built 3,256 base games and 2,800 controlled counterparts across 24 families and 20 mechanisms.

These files define playable game instances. Model behavior lives in a separately collected run. validation_fixtures.jsonl contains scripted witnesses only.

| Family | Mechanism | Base variants | Witness-positive variants |
|---|---|---:|---:|
| certificate_office | unchecked_self_report | 184 | 158 |
| shared_fishery | unenforced_limits | 240 | 240 |
| inspection_dock | undelivered_punishment | 112 | 112 |
| amendment_office | rule_order_precedence | 184 | 176 |
| appeals_court | meta_rule | 184 | 184 |
| signal_relay | information_overflow | 184 | 161 |
| sealed_archive | information_asymmetry | 112 | 112 |
| convention_table | signaling_encoding | 112 | 112 |
| conversion_market | resource_conversion | 112 | 86 |
| workshop_grants | state_reset_refresh | 112 | 112 |
| voucher_bank | resource_duplication | 184 | 184 |
| canal_routes | board_state_poisoning | 112 | 112 |
| priority_queue | turn_order | 112 | 112 |
| closing_market | phase_boundary | 112 | 112 |
| settlement_race | terminal_condition | 112 | 112 |
| escrow_partnership | threat_commitment | 184 | 184 |
| survey_contract | objective_substitution | 112 | 112 |
| reserve_conflict | sacrificial_negative_value | 112 | 112 |
| coalition_council | coalition_kingmaking | 112 | 112 |
| aid_reservations | denial_griefing | 112 | 112 |
| public_works | ordinary strategic control | 112 | 0 |
| launch_coordination | ordinary strategic control | 120 | 0 |
| trust_exchange | ordinary strategic control | 112 | 0 |
| sealed_tender | ordinary strategic control | 112 | 0 |

Witness-positive means at least one tested environment seed produced the mechanism effect; it does not imply positive net payoff. Neutral doses remain included. See validation.json for exact checks and coverage.
