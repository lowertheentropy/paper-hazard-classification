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
3221001,2023-10-07,2023-10-07,Israel,30.892,33.876,1,Government of Israel,Hamas,1200
3271258,2023-10-08,2023-11-08,Israel,32.791,36.298,1,Government of Israel,Hamas,105

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_War","label":"War","confidence":0.9,"evidence":["[Knowledge:208 hazards:Hazard_War ... Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best]","[Knowledge:138 hazards:Hazard_One_Sided_Violence_UCDP ... Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best]"],"notes":"The snippet is an event‑level conflict record (date, location, actors, fatalities) matching the UCDP war/armed‑conflict sample rows; 'War' is the most direct generic label."}
