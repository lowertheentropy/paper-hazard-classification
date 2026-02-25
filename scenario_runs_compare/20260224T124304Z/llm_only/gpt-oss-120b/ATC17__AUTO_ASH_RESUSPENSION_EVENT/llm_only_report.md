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
time_utc,lat,lon,dust_aod_550,total_aod_561,so2_kg_m2
2024-2-18T11:00Z,28.0,-15.0,0.65,0.80,0.00002
2024-02-18T12:00Z,30.675,-10.0,0.58,0.72,0.00001

## Final Answer
{"hazard_id":"dust_storm","label":"Dust Storm","confidence":0.92,"evidence":["[Snippet: dust_aod_550 values 0.65 and 0.58 indicate elevated dust aerosol]"],"notes":"Elevated AOD suggests dust event"}

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
