# Report

- Method: `simple_rag`
- Model: `gpt-oss-120b`

## Question

Hazard classification (Top-1). Use ONLY CONTEXT as evidence.

Output requirements:
- Direct Answer: ONE-LINE JSON only, schema:
  {"hazard_id":"...","label":"...","confidence":0.0,"evidence":["[Knowledge:.. ...]"],"notes":"short"}
- Do not add any additional text.

SNIPPET:
report_id,ts_utc,lat,lon,platform,issue_type,impact,notes
NAVCEN-1,2025-04-03T19:22:00Z,36.85,28.27,maritime,"jamming suspected","loss_of_fix","Intermittent GPS signal; reverted to inertial nav"
NAVCEN-2,2025-04-04T5:10:00Z,26.571,55.27,aviation,"spoofing suspected","position_jump","Reported sudden position offset; RAIM alert"

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_GNSS_Disruption_Jamming_Spoofing_Outage","label":"GNSS Disruption","confidence":0.93,"evidence":["[Snippet] NAVCEN-1 ... \"jamming suspected\",\"loss_of_fix\"","[Snippet] NAVCEN-2 ... \"spoofing suspected\",\"position_jump\"","[Knowledge:72] Keywords: GNSS jamming; GNSS spoofing; timing loss; navigation errors"],"notes":"Intermittent GPS signal loss and sudden position jumps indicate GNSS disruption via jamming or spoofing."}
```
