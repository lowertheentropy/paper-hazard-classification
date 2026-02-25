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
time_utc,lat,lon,dust_aod_550,total_aod_561,so2_kg_m2
2024-2-18T11:00Z,28.0,-15.0,0.65,0.80,0.00002
2024-02-18T12:00Z,30.675,-10.0,0.58,0.72,0.00001

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Sand_Dust_Storm","label":"Sand/Dust Storm","confidence":0.95,"evidence":["[Knowledge:160 hazards:Hazard_Sand_Dust_Storm Sand/Dust Storm]","time_utc,lat,lon,dust_aod_550,total_aod_561,so2_kg_m2\n2024-02-18T11:00Z,28.0,-15.0,0.65,0.80,0.00002"] ,"notes":"Dust aerosol optical depth measurements are characteristic of sand/dust storm observations."} 
```
