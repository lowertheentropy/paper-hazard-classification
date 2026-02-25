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
tile_id,date_yyyymm,avg_radiance_nW_cm2_sr,cloud_free_obs
75N58W,202401,12.34,18
75N060W,202402,11.98,16

## Final Answer

{"hazard_id":"radiation_anomaly","label":"Radiation Anomaly","confidence":0.3,"evidence":["[Snippet: avg_radiance_nW_cm2_sr values 12.34 and 11.98]"],"notes":"moderate radiance observed"}
