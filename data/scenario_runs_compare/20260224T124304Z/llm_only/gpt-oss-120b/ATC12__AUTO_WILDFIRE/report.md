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
latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-123.429,2024-07-15,2030,N,nominal,12.287
37.130,-121.470,2024-7-15,2036,N,high,35.1

## Final Answer

{"hazard_id":"H001","label":"Wildfire","confidence":0.92,"evidence":["[Knowledge: FRP values of 12.287 and 35.1 indicate active fires]"],"notes":"Detected fire radiative power suggests wildfire"}
