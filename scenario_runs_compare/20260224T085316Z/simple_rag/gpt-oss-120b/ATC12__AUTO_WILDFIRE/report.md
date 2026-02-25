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
latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-123.429,2024-07-15,2030,N,nominal,12.287
37.130,-121.470,2024-7-15,2036,N,high,35.1

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Wildfire","label":"Wildfire","confidence":0.99,"evidence":["[Knowledge:216 hazards:Hazard_Wildfire Wildfire] ... Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp","[Knowledge:68 hazards:Hazard_Forest_Fire Forest Fire] ... Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp"],"notes":"Active‑fire satellite record matches the Wildfire hazard definition"}
```

**Justification**
- The snippet lists satellite fire detections (lat/long, date, time, confidence, FRP) – exactly the sample fields described for **Hazard_Wildfire**. 【Knowledge:216】  
- The same column structure appears in the **Forest Fire** entry, but that card is a narrower subtype; the general Wildfire card covers all fire types (wildfire, forest fire, bushfire). 【Knowledge:68】  
- No other hazard cards contain these fire‑radiative‑power fields, making Wildfire the clear top‑match.
