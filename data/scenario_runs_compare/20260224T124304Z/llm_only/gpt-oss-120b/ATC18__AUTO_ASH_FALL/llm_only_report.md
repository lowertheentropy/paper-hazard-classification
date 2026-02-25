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
volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
370049,Etna,12345,2021-02-16,2021-03-1,3,37.734,15.004
271313,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.454,29.25

## Final Answer
{"hazard_id":"volcanic_eruption","label":"Volcanic Eruption","confidence":0.9,"evidence":[],"notes":"Based on VEI values indicating eruption activity"}

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
