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
time,latitude,longitude,depth_km,mag,magType,place,event_id
2026-02-19T22:14:12.340Z,37.766,-122.534,8.7,2.6,ml,"10 km WSW of San Francisco, CA",nc74910871
2026-02-18T24:01:44.120Z,35.126,-118.243,11.492,3.119,ml,"Los Angeles region, CA",ci40672007

## Final Answer
{"hazard_id":"earthquake","label":"Earthquake","confidence":0.96,"evidence":["[Snippet: 2026-02-19T22:14:12.340Z,37.766,-122.534,8.7,2.6,ml,\"10 km WSW of San Francisco, CA\",nc74910871]"],"notes":"Detected seismic event"}

## Metrics
```json
{
  "llm_calls": 1,
  "uses_retrieval": false,
  "retrieval_corpora": [],
  "citation_count": 1,
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
