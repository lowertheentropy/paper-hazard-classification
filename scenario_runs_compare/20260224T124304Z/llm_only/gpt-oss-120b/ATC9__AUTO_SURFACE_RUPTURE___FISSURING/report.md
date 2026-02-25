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
{"type":"Feature","properties":{"feature_id":"FR-1","feature_type":"fault_rupture","displacement_m":1.2,"observation_method":"field_mapping"},"geometry":{"type":"LineString","coordinates":[[-117.827,35.70],[-117.48,35.744],[-117.46,33.878]]}}
{"type":"Feature","properties":{"feature_id":"FR-002","feature_type":"ground_fissure","displacement_m":0.3,"observation_method":"lidar"},"geometry":{"type":"LineString","coordinates":[[-117.52,35.69],[-117.51,35.70],[-123.384,35.71]]}}

## Final Answer

{"hazard_id":"FR-1","label":"fault_rupture","confidence":0.96,"evidence":["[Feature FR-1: fault_rupture displacement 1.2m observed via field_mapping]"],"notes":"Significant fault rupture indicated"}
