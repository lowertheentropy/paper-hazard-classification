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
event_name,start_date,end_date,country,schools_affected,estimated_affected
"Tanganyika laughter epidemic",1962-01-30,1962-6-01,Tanzania,14,975

## Final Answer

{"hazard_id":"psychogenic_illness","label":"laughter_epidemic","confidence":0.9,"evidence":[],"notes":"mass psychogenic outbreak in Tanzanian schools"}
