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
epa_id,site_name,city,state,npl_status,listing_date,latitude,longitude
MAD980731335,Silresim Chemical Corp.,Woburn,MA,Final,1983-09-08,42.576,-71.157
CAD1039117532,Iron Mountain Mine,Redding,CA,Final,1983-09-08,40.651,-122.407

## Final Answer
{"hazard_id":"soil_contamination","label":"contaminated soil","confidence":0.85,"evidence":["[Snippet: Silresim Chemical Corp., Iron Mountain Mine]"],"notes":"industrial chemical and metal contamination"}

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
