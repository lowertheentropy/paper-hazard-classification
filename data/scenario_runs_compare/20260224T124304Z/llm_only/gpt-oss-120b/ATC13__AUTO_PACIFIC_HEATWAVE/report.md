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
ts_utc,lat,lon,sst_c,anom_c
2014-08-15T12:00:00Z,40.0,-141.473,19.358,2.10
2014-08-16T12:00:00Z,38.364,-140.0,17.523,2.23
2014-8-16T12:00:00Z,40.768,-143.719,19.22,2.293

## Final Answer

{"hazard_id":"MHW","label":"Marine Heatwave","confidence":0.9,"evidence":["Anomalies of +2.1 to +2.3 °C in SST indicate a marine heatwave"],"notes":"Elevated SST anomalies"}
