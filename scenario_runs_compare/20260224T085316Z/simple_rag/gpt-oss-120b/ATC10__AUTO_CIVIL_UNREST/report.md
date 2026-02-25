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
id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-7,Israel,31.78,34.76,1,Government of Israel,Hamas,1217
3221002,2023-10-08,2023-10-8,Israel,31.266,34.45,1,Government of Israel,Hamas,100

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Armed_Conflict","label":"Armed Conflict","confidence":0.9,"evidence":["[Knowledge:7 hazards:Hazard_Armed_Conflict Armed Conflict] … Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best","[Knowledge:138 hazards:Hazard_One_Sided_Violence_UCDP One-sided Violence (UCDP)] … Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best"],"notes":"Snippet matches UCDP event‑level conflict dataset; best fit is the Armed Conflict hazard."}
