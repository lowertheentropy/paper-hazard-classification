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
event_id,ra_deg,dec_deg,t0_jd,tE_days,u0,chi2
GDR3-ML-001,266.234,-29.051,2387696.085,42.586,0.12,1.05
GDR3-ML-2,83.633,22.014,2452068.9,18.4,0.35,0.956

## Final Answer
{"hazard_id":"microlensing","label":"Microlensing Event","confidence":0.85,"evidence":["[Knowledge: event data includes tE_days and u0 typical for microlensing]"],"notes":"Astronomical transient"}

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
