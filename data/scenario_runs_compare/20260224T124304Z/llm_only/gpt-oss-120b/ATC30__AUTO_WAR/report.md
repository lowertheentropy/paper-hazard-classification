# Report

- Method: `llm_only`
- Model: `gpt-oss-120b`

## Question

Hazard classification (Top-1). Use ONLY CONTEXT as evidence.

Output requirements:
- Direct Answer: ONE-LINE JSON only, schema:
  {"hazard_id":"...","label":"...","confidence":0.0,"evidence":["[Knowledge:.. ...]"],"notes":"short"}
- Do not add any additional text.

SNIPPET:
id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,30.892,33.876,1,Government of Israel,Hamas,1200
3271258,2023-10-08,2023-11-08,Israel,32.791,36.298,1,Government of Israel,Hamas,105

## Final Answer

{"hazard_id":"conflict","label":"Armed Conflict","confidence":0.95,"evidence":[],"notes":"Government-Hamas clashes in Israel"}
