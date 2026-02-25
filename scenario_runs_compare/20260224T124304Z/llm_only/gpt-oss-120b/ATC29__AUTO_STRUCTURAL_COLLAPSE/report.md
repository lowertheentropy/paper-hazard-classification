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
incident_id,incident_date,borough,incident_type,building_class,injured_count,fatality_count,description
DOB-2120-124,2024-04-07,MANHATTAN,Collapse,Residential,2,0,"Partial wall collapse during renovation"
DOB-2123-2079,2023-11-19,BROOKLYN,Collapse,Commercial,0,1,"Scaffold/structure collapse"

## Final Answer

{"hazard_id":"COLLAPSE","label":"Structural Collapse","confidence":0.96,"evidence":["Partial wall collapse during renovation","Scaffold/structure collapse"],"notes":"Observed building and scaffold collapses"}
