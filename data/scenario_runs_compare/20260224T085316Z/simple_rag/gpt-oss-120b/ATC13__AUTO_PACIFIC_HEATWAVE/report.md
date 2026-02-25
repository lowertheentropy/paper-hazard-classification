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
ts_utc,lat,lon,sst_c,anom_c
2014-08-15T12:00:00Z,40.0,-141.473,19.358,2.10
2014-08-16T12:00:00Z,38.364,-140.0,17.523,2.23
2014-8-16T12:00:00Z,40.768,-143.719,19.22,2.293

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Pacific_Heatwave","label":"Pacific Heatwave","confidence":0.9,"evidence":["[Knowledge:141 hazards:Hazard_Pacific_Heatwave Pacific Heatwave] BM25_TEXT_EN: ... Daily gridded sea‑surface temperature (SST) values ... Sample data: ts_utc,lat,lon,sst_c,anom_c","[Knowledge:120 hazards:Hazard_Marine_Heatwave Marine Heatwave] BM25_TEXT_EN: ... Daily gridded sea‑surface temperature (NOAA OISST) used to detect marine heatwaves ... Sample data: date,lat,lon,sst_c,mhw_category,mhw_intensity_c"] ,"notes":"Snippet shows SST and anomaly values typical of a Pacific marine heatwave (The Blob)."} 
```
