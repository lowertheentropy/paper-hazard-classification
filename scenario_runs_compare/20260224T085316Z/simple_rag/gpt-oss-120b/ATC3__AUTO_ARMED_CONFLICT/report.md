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
3221001,2023-10-7,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1272
3218496,2023-10-08,2023-10-08,Israel,31.50,34.846,1,Government of Israel,Hamas,101

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_One_Sided_Violence_UCDP","label":"One-sided Violence (UCDP)","confidence":0.95,"evidence":["[Knowledge:138 hazards:Hazard_One_Sided_Violence_UCDP One-sided Violence (UCDP)] … Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best","The snippet shows columns id, date_start, date_end, country, latitude, longitude, type_of_violence, side_a, side_b, best with values matching the sample rows for one‑sided violence in the UCDP dataset."],"notes":"Matches conflict event data (type_of_violence=1) indicating one‑sided violence between government and Hamas."}
```

**Justification**
- The snippet’s columns (`id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best`) are identical to the sample rows listed for **Hazard_One_Sided_Violence_UCDP**【Knowledge:138…】.  
- `type_of_violence` is set to 1, which in UCDP denotes *one‑sided violence* (civilian targeting).  
- The actors (`Government of Israel` vs `Hamas`) and fatality counts align with the example rows provided for this hazard.  
- No other hazard cards describe this exact event‑level conflict format; broader categories like Armed Conflict or War are less specific.
