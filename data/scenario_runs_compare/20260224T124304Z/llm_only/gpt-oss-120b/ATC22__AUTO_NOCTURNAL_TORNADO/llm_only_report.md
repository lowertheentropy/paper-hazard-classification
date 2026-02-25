# LLM Baseline Report (One-shot, keyword-output)

- **Mode:** `llm_keywords_one_shot`
- **Model:** `gpt-oss-120b`
- **Base URL:** `http://localhost:1234/v1`

## Question
Hazard classification (Top-1). Use ONLY CONTEXT as evidence.

Output requirements:
- Direct Answer: ONE-LINE JSON only, schema:
  {"hazard_id":"...","label":"...","confidence":0.0,"evidence":["[Knowledge:.. ...]"],"notes":"short"}
- Do not add any additional text.

SNIPPET:
EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-6-28 22:50:00,2021-06-28 22:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1047675,2021-6-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.34,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,30.79,-99.90,0,0,5000000,0

## Final Answer
{"hazard_id":"winter_storm","label":"Winter Storm","confidence":0.8,"evidence":[],"notes":"Highest property damage observed"}

## Metrics
```json
{
  "llm_calls": 1,
  "uses_retrieval": false,
  "retrieval_corpora": [],
  "citation_count": 0,
  "min_citations_threshold": 2,
  "has_min_citations": false,
  "top_k_memory": 250,
  "recent_k_memory": 250,
  "memory_items_loaded": 0,
  "output_mode": "keywords_only"
}
```

## Retrieved Context (Memory-only)
_none_
