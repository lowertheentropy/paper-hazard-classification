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
volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
370049,Etna,12345,2021-02-16,2021-03-1,3,37.734,15.004
271313,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.454,29.25

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Volcanic_Activity_General","label":"Volcanic Activity (General)","confidence":0.96,"evidence":["[Knowledge:205 hazards:Hazard_Volcanic_Activity_General]","Snippet showing volcano eruption table with columns volcano_number,volcano_name,start_date,end_date,vei,latitude,longitude"],"notes":"The snippet lists generic volcanic eruption records, matching the general volcanic activity hazard."}
```
