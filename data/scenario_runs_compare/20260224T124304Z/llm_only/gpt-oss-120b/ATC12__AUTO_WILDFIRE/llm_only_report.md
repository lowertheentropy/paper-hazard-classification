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
latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-123.429,2024-07-15,2030,N,nominal,12.287
37.130,-121.470,2024-7-15,2036,N,high,35.1

## Final Answer
{"hazard_id":"H001","label":"Wildfire","confidence":0.92,"evidence":["[Knowledge: FRP values of 12.287 and 35.1 indicate active fires]"],"notes":"Detected fire radiative power suggests wildfire"}

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
