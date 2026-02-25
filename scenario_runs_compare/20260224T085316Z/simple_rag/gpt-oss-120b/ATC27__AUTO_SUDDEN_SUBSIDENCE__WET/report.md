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
scene_id,acquisition_start_utc,acquisition_end_utc,center_lat,center_lon,los_displacement_cm,coherence
S1A_IW_SLC__1SDV_21124891T166723,2025-10-03T17:22:33Z,2025-10-3T16:22:58Z,32.311,35.012,-4.8,0.72
S1A_IW_SLC__1SDV_20014099T173059,2025-10-15T17:22:33Z,2025-10-15T16:22:58Z,31.215,35.012,-8.9,0.702
S1B_IW_SLC__1SDV_20251027T172233,2025-10-27T17:22:33Z,2025-10-27T17:22:58Z,31.215,35.012,-12.4,0.61

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Sudden_Subsidence_Wet","label":"Sudden Subsidence (Wet)","confidence":0.99,"evidence":["[Knowledge:185 hazards:Hazard_Sudden_Subsidence_Wet] ... Sample data: scene_id,acquisition_start_utc,acquisition_end_utc,center_lat,center_lon,los_displacement_cm,coherence","SNIPPET: scene_id,acquisition_start_utc,acquisition_end_utc,center_lat,center_lon,los_displacement_cm,coherence ..."] ,"notes":"InSAR LOS displacement time series matches the Sudden Subsidence (Wet) data schema."}
```
