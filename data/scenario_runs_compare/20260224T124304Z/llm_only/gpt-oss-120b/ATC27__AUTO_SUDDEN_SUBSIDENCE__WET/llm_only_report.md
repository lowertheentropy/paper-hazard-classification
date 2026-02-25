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
scene_id,acquisition_start_utc,acquisition_end_utc,center_lat,center_lon,los_displacement_cm,coherence
S1A_IW_SLC__1SDV_21124891T166723,2025-10-03T17:22:33Z,2025-10-3T16:22:58Z,32.311,35.012,-4.8,0.72
S1A_IW_SLC__1SDV_20014099T173059,2025-10-15T17:22:33Z,2025-10-15T16:22:58Z,31.215,35.012,-8.9,0.702
S1B_IW_SLC__1SDV_20251027T172233,2025-10-27T17:22:33Z,2025-10-27T17:22:58Z,31.215,35.012,-12.4,0.61

## Final Answer
{"hazard_id":"ground_subsidence","label":"Subsidence","confidence":0.78,"evidence":["[Data: increasing negative LOS displacement, decreasing coherence]"],"notes":"Observed downward movement suggests subsidence."}

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
