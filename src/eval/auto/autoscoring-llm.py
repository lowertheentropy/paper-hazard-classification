#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm.py  (ONE-SHOT BASELINE WITH MEMORY-ONLY RAG — optional, keyword-output)

Goal:
- Still a *single* LLM call (one-shot).
- Uses BM25 retrieval ONLY over Memory (memory snapshot) when Memory is available.
- If Memory is missing/empty (e.g., no-memory.json), it degrades gracefully:
  it runs one-shot with empty CONTEXT and marks uses_retrieval=False.

IMPORTANT CHANGE (for hazard runs):
- This baseline must NOT output hazard IDs (it does not see aggregated hazard cards).
- Instead, it MUST output a single-line JSON at the top where:
    predicted_hazard_id = exactly 5 keywords describing the phenomenon (comma-separated string).
  Humans can then compare keywords to the true hazard and mark true/false.

Deps:
  pip install openai rank-bm25 numpy

Usage:
  python3 llm.py --input request.json --out result.json --out_md report.md

request.json schema (subset-compatible with your runner):
{
  "question": "...",
  "llm": {"base_url":"http://localhost:1234/v1", "model":"...", "api_key":"...", "temperature":0.2, "max_tokens":4096},
  "retrieval": {
    "top_k": {"Memory": 30},         # optional; Memory-only
    "recent_k": {"Memory": 50},      # optional; Memory-only
    "per_doc_chars": 800,
    "min_citations": 2              # metric only; no rewrite
  },
  "corpora": {
    "Memory": "memory.json"         # optional; if missing/empty => no-context run
  }
}

Notes:
- If request.json contains other corpora, they are ignored.
- Inline citations are encouraged only when CONTEXT is present.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from rank_bm25 import BM25Okapi

try:
    from openai import OpenAI
except Exception as e:
    raise RuntimeError("Missing dependency: openai. Install with: pip install openai") from e


# =============================================================================
# Defaults
# =============================================================================

DEFAULT_BASE_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "gpt-oss-120b"
DEFAULT_API_KEY = "lm-studio"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 8192

# memory-only retrieval defaults
DEFAULT_TOP_K_MEMORY = 250
DEFAULT_RECENT_K_MEMORY = 250
DEFAULT_PER_DOC_CHARS = 10000

# metric only; no rewrite pass
DEFAULT_MIN_CITATIONS = 2

SYSTEM_DEFAULT = (
    "You are a careful assistant. "
    "Follow output-format rules exactly."
)

# ---- KEY CHANGE: force keyword-output instead of hazard ID ----
PROMPT_LLM_KEYWORDS_ONE_SHOT = """\
You are producing a baseline output for later human comparison.

You MUST output exactly this format:

1) Direct Answer:
- ONE LINE of VALID JSON (no code fences), schema:
  {{"predicted_hazard_id":"kw1, kw2, kw3, kw4, kw5","confidence":0.0,"notes":"short"}}

Rules for JSON:
- predicted_hazard_id MUST be exactly 5 keywords (comma-separated) describing the observed phenomenon/pattern.
- Keywords should be concrete (signals/indicators), NOT hazard names, NOT IDs, NOT ontology strings.
- confidence: 0.0–1.0
- notes: <= 20 words

2) Brief rationale (2–6 bullets):
- If CONTEXT is present, cite any critical statement with inline citations copied from CONTEXT.
- If CONTEXT is empty, explicitly say "no local context provided" once and reason from the snippet only.

CONTEXT:
{context}

QUESTION / SNIPPET:
{question}
"""


# =============================================================================
# Data model
# =============================================================================

@dataclass
class Item:
    content: str
    meta: Dict[str, Any]


def _safe_read_json(path: Path) -> Any:
    """Read JSON but tolerate empty files."""
    txt = path.read_text(encoding="utf-8")
    if not txt.strip():
        return None
    return json.loads(txt)


def _stringify(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, (int, float, bool)):
        return str(x)
    if isinstance(x, str):
        return x.strip()
    if isinstance(x, dict):
        return json.dumps(x, ensure_ascii=False)
    if isinstance(x, list):
        return ", ".join([str(v) for v in x if str(v).strip()])
    return str(x).strip()


def load_memory_items(path_or_inline: Any) -> List[Item]:
    """
    Memory loader (schema-tolerant). Accepts:
      - filepath string to JSON
      - inline list of event dicts (einsatz logs)
      - inline dict {"items":[{"content":..., "meta":...}, ...]}
    """
    raw: Any
    if path_or_inline is None:
        return []

    if isinstance(path_or_inline, str):
        p = Path(path_or_inline)
        if not p.exists():
            return []
        try:
            raw = _safe_read_json(p)
        except Exception:
            return []
        if raw is None:
            return []
    else:
        raw = path_or_inline

    # {"items":[...]} wrapper
    if isinstance(raw, dict) and isinstance(raw.get("items"), list):
        out: List[Item] = []
        for i, it in enumerate(raw["items"], start=1):
            if not isinstance(it, dict):
                continue
            content = it.get("content")
            meta = it.get("meta") or {}
            if isinstance(content, str) and content.strip():
                if not isinstance(meta, dict):
                    meta = {"meta": meta}
                meta.setdefault("nummer", str(meta.get("nummer") or i))
                meta.setdefault("artikel", str(meta.get("artikel") or meta.get("meta") or "memory_event"))
                out.append(Item(content=content.strip(), meta=meta))
        return out

    # list of event dicts
    if isinstance(raw, list):
        out2: List[Item] = []
        for i, ev in enumerate(raw, start=1):
            if not isinstance(ev, dict):
                continue
            content = ev.get("content") or ev.get("text") or ev.get("message") or ""
            if not isinstance(content, str) or not content.strip():
                continue
            meta = dict(ev)
            meta.pop("content", None)
            meta.setdefault("nummer", str(i))
            meta.setdefault("artikel", str(meta.get("meta") or "memory_event"))
            if not isinstance(meta.get("meta"), str):
                meta["meta"] = _stringify(meta.get("meta"))
            out2.append(Item(content=content.strip(), meta=meta))
        return out2

    return []


# =============================================================================
# BM25 (Memory-only)
# =============================================================================

def _tokenize(text: str) -> List[str]:
    return re.findall(r"\w+|\S", (text or "").lower(), flags=re.UNICODE)


def _doc_text(it: Item) -> str:
    parts = [it.content]
    for v in (it.meta or {}).values():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, (int, float)):
            parts.append(str(v))
        elif isinstance(v, list):
            parts.extend([str(x) for x in v if isinstance(x, (str, int, float))])
    return " ".join([p for p in parts if p])


class BM25Index:
    def __init__(self, items: List[Item]):
        self.items = items
        self.docs_tokens = [_tokenize(_doc_text(it)) for it in items]
        self.bm25 = BM25Okapi(self.docs_tokens) if self.docs_tokens else None

    def retrieve(self, query: str, top_k: int) -> List[Tuple[Item, float]]:
        if not self.items or self.bm25 is None:
            return []
        q = _tokenize(query)
        if not q:
            return []
        scores = self.bm25.get_scores(q)
        idx = np.argsort(scores)[::-1][:top_k]
        return [(self.items[i], float(scores[i])) for i in idx]


def _truncate_context(text: str, limit: int, *, mode: str = "tail") -> str:
    """Memory is log-like; tail is often more relevant."""
    if not limit or len(text) <= limit:
        return text

    if mode == "tail":
        tail = text[-limit:]
        nl = tail.find("\n")
        if 0 < nl < 200:
            tail = tail[nl + 1 :]
        return "…\n" + tail

    head = text[:limit]
    head = (head.rsplit(" ", 1)[0] or head).rstrip()
    return head + " …"


def format_hits(hits: List[Tuple[Item, float]], per_doc_chars: int = 800) -> str:
    lines: List[str] = []
    for it, _score in hits:
        meta = (it.meta or {}) if isinstance(it.meta, dict) else {"meta": it.meta}
        nummer = meta.get("nummer", "?")
        spez = meta.get("spezifikation") or meta.get("artikel") or ""

        einsatz_nr = meta.get("einsatzNr") or meta.get("einsatznr") or meta.get("incidentNr") or meta.get("incident") or ""
        event_id = meta.get("eventId") or meta.get("event_id") or ""
        incident_tag = f"#{einsatz_nr}" if einsatz_nr else (f"evt:{event_id}" if event_id else "")

        cite_parts = [f"Memory:{nummer}"]
        if incident_tag:
            cite_parts.append(incident_tag)
        if spez:
            cite_parts.append(str(spez).strip())
        cite = ("[" + " ".join(cite_parts) + "]").strip()

        txt = it.content or ""
        if per_doc_chars and len(txt) > per_doc_chars:
            txt = _truncate_context(txt, per_doc_chars, mode="tail")

        lines.append(f"{cite} {txt}")
    return "\n\n".join(lines)


def _dedupe_hits(hits: List[Tuple[Item, float]]) -> List[Tuple[Item, float]]:
    seen = set()
    out: List[Tuple[Item, float]] = []
    for it, sc in hits:
        key = (it.meta or {}).get("nummer") or id(it)
        if key in seen:
            continue
        seen.add(key)
        out.append((it, sc))
    return out


def build_memory_context(
        memory_items: List[Item],
        query: str,
        *,
        top_k: int,
        recent_k: int,
        per_doc_chars: int,
) -> Tuple[str, Dict[str, str]]:
    if not memory_items:
        return "", {"Memory": ""}

    idx = BM25Index(memory_items)

    hits: List[Tuple[Item, float]] = []
    if top_k > 0:
        hits.extend(idx.retrieve(query, top_k))

    if recent_k > 0:
        recent_items = memory_items[-recent_k:]
        hits.extend([(it, -1.0) for it in reversed(recent_items)])

    hits = _dedupe_hits(hits)
    block = format_hits(hits, per_doc_chars=per_doc_chars)
    full = f"### Memory\n{block}".strip() if block.strip() else ""
    return full, {"Memory": block}


# =============================================================================
# LLM client (ONE CALL ONLY)
# =============================================================================

class LocalChat:
    def __init__(self, base_url: str, model: str, api_key: str = DEFAULT_API_KEY):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def chat(self, system: str, user: str, temperature: float, max_tokens: int) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": (system or "").strip()},
                {"role": "user", "content": (user or "").strip()},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        raw = resp.model_dump() if hasattr(resp, "model_dump") else json.loads(resp.json())
        msg = (((raw or {}).get("choices") or [{}])[0].get("message") or {})
        return (msg.get("content") or "").strip()


def count_inline_citations(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(r"\[[A-Za-z]+:[^\]]+\]", text))


def render_markdown(res: Dict[str, Any]) -> str:
    meta = res.get("meta", {}) or {}
    out: List[str] = []
    out.append("# LLM Baseline Report (One-shot, keyword-output)\n")
    out.append(f"- **Mode:** `{meta.get('mode','llm_keywords_one_shot')}`")
    out.append(f"- **Model:** `{meta.get('model','')}`")
    out.append(f"- **Base URL:** `{meta.get('base_url','')}`")
    out.append("")
    out.append("## Question")
    out.append(meta.get("question", "") or "_not specified_")
    out.append("")
    out.append("## Final Answer")
    out.append(res.get("final", "") or "_not specified_")
    out.append("")
    out.append("## Metrics")
    metrics = res.get("metrics", {}) or {}
    out.append("```json")
    out.append(json.dumps(metrics, ensure_ascii=False, indent=2))
    out.append("```")
    out.append("")
    out.append("## Retrieved Context (Memory-only)")
    ctx = (res.get("contexts", {}) or {}).get("pass1", {}) or {}
    mem_block = ctx.get("Memory", "")
    if isinstance(mem_block, str) and mem_block.strip():
        out.append("### Memory")
        out.append("```")
        out.append(mem_block.replace("```", "``\\`"))
        out.append("```")
        out.append("")
    else:
        out.append("_none_")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# =============================================================================
# Runner
# =============================================================================

def run_llm_keywords_one_shot(req: Dict[str, Any]) -> Dict[str, Any]:
    question = str(req.get("question", "") or "").strip()
    if not question:
        raise ValueError("request.question is required")

    llm_cfg = req.get("llm") or {}
    base_url = str(llm_cfg.get("base_url", DEFAULT_BASE_URL))
    model = str(llm_cfg.get("model", DEFAULT_MODEL))
    api_key = str(llm_cfg.get("api_key", DEFAULT_API_KEY))
    temperature = float(llm_cfg.get("temperature", DEFAULT_TEMPERATURE))
    max_tokens = int(llm_cfg.get("max_tokens", DEFAULT_MAX_TOKENS))

    ret_cfg = req.get("retrieval") or {}
    top_k = int((ret_cfg.get("top_k") or {}).get("Memory", DEFAULT_TOP_K_MEMORY))
    recent_k = int((ret_cfg.get("recent_k") or {}).get("Memory", DEFAULT_RECENT_K_MEMORY))
    per_doc_chars = int(ret_cfg.get("per_doc_chars", DEFAULT_PER_DOC_CHARS))
    min_citations = int(ret_cfg.get("min_citations", DEFAULT_MIN_CITATIONS))

    corpora = req.get("corpora") or {}
    mem_src = corpora.get("Memory")  # optional

    memory_items = load_memory_items(mem_src)

    # Ensure stable 'nummer' + 'artikel' for citations
    for i, it in enumerate(memory_items, start=1):
        if not isinstance(it.meta, dict):
            it.meta = {"meta": it.meta}
        it.meta.setdefault("nummer", str(i))
        it.meta.setdefault("artikel", str(it.meta.get("artikel") or it.meta.get("meta") or "Memory"))

    context_full, per = build_memory_context(
        memory_items,
        query=question,
        top_k=top_k,
        recent_k=recent_k,
        per_doc_chars=per_doc_chars,
    )

    uses_retrieval = bool(context_full.strip())

    # -----------------------------
    # ONE AND ONLY LLM CALL
    # -----------------------------
    chat = LocalChat(base_url=base_url, model=model, api_key=api_key)
    final = chat.chat(
        SYSTEM_DEFAULT,
        PROMPT_LLM_KEYWORDS_ONE_SHOT.format(context=context_full, question=question),
        temperature=temperature,
        max_tokens=max_tokens,
    ).strip()

    c_count = count_inline_citations(final)
    return {
        "final": final,
        "contexts": {"pass1": per, "pass2": {}},
        "metrics": {
            "llm_calls": 1,
            "uses_retrieval": uses_retrieval,
            "retrieval_corpora": ["Memory"] if uses_retrieval else [],
            "citation_count": c_count,
            "min_citations_threshold": min_citations,
            "has_min_citations": bool(c_count >= min_citations),
            "top_k_memory": top_k,
            "recent_k_memory": recent_k,
            "memory_items_loaded": len(memory_items),
            "output_mode": "keywords_only",
        },
        "meta": {"mode": "llm_keywords_one_shot", "model": model, "base_url": base_url, "question": question},
    }


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to request.json")
    ap.add_argument("--base_url", default="", help="Override base_url")
    ap.add_argument("--model", default="", help="Override model")
    ap.add_argument("--out", default="", help="Optional output JSON path")
    ap.add_argument("--out_md", default="", help="Optional output Markdown path")
    args = ap.parse_args()

    req = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if args.base_url:
        req.setdefault("llm", {})["base_url"] = args.base_url
    if args.model:
        req.setdefault("llm", {})["model"] = args.model

    res = run_llm_keywords_one_shot(req)

    txt = json.dumps(res, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(txt, encoding="utf-8")
    else:
        print(txt)

    if args.out_md:
        Path(args.out_md).write_text(render_markdown(res), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())