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
oe425_id,incident_start_utc,event_type,states_affected,customers_affected,major_system_impacts
OE417-2123-0156,2024-1-13T03:20Z,Transmission outage,"TX,LA",210000,Yes
OE392-1921-0091,2025-8-22T14:05Z,Severe weather,"FL",450000,Yes

## Final Answer
{"hazard_id":"transmission_outage","label":"Transmission outage","confidence":0.5,"evidence":[],"notes":"Based on first record; ambiguous without context"}

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
