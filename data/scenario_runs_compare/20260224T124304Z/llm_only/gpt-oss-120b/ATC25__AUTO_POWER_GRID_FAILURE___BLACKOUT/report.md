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
timestamp_utc,fips,customers_out,customers_total,outage_pct
2024-2-17T18:15Z,12086,35214,873402,3.794
2024-2-15T19:30Z,11456,40110,873402,4.59

## Final Answer

{"hazard_id":"power_outage","label":"Power Outage","confidence":0.92,"evidence":["[Knowledge: timestamp_utc shows outage data with customers_out and outage_pct]"],"notes":"Observed electricity service interruption"}
