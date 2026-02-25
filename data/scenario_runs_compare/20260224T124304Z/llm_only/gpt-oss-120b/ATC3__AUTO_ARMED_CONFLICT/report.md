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
3221001,2023-10-7,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1272
3218496,2023-10-08,2023-10-08,Israel,31.50,34.846,1,Government of Israel,Hamas,101

## Final Answer

{"hazard_id":"armed_conflict","label":"Armed Conflict","confidence":0.95,"evidence":[],"notes":"Government vs Hamas clashes in Israel."}
