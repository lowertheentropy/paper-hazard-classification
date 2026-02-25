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
sample data for high water ... 5000 liters/minute/m2

site_no,ts_utc,discharge_cfs,gage_height_ft,qualifiers
01646500,2025-9-29T12:00:00Z,27517,18.42,A
1692320,2025-09-29T12:15:00Z,30677,18.77,A
1651968,2025-09-29T12:30:00Z,32600,19.10,A
01646500,2025-9-28T12:45:00Z,33358,19.576,A

## Final Answer
{"hazard_id":"flood","label":"High Water Flooding","confidence":0.96,"evidence":["sample data for high water ... 5000 liters/minute/m2"],"notes":"Elevated discharge and gage heights indicate flooding"}

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
