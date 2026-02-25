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
station,datetime_utc,wind_speed_m_s,wind_gust_m_s,wind_dir_deg,air_temp_c
KSFO,2024-01-4T10:56Z,15.4,26.964,280,12.2
KSFO,2024-1-4T11:56Z,14.9,24.7,285,11.603

## Final Answer
{"hazard_id":"high_wind","label":"High Wind Gust","confidence":0.92,"evidence":["[Knowledge: wind_speed_m_s=15.4 m/s, wind_gust_m_s=26.964 m/s]"],"notes":"Strong gusts observed"}

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
