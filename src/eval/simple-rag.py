#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simple-rag.py  (HAZARD CLASSIFICATION ONE-SHOT BASELINE)

Goal:
- Build BM25 index over hazard_cards_v5.json (full data: labels, altLabels, links, risk, bm25_text_en,
  verbalized_en, sample data, sources, etc.)
- Optionally include Memory (einsatz logs) as auxiliary context (indicator-heavy matching).
- Exactly ONE LLM call.

Deps:
  pip install openai rank-bm25 numpy
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
DEFAULT_MAX_TOKENS = 131072

# For hazard classification, we usually want Knowledge-heavy retrieval.
DEFAULT_TOP_K = {"Knowledge": 250, "Memory": 6, "Experiences": 0, "Environment": 0, "OpsState": 0}
DEFAULT_RECENT_K = {"Memory": 10, "Environment": 0, "OpsState": 0, "Knowledge": 0, "Experiences": 0}
DEFAULT_PER_DOC_CHARS = 1600
DEFAULT_MIN_CITATIONS = 1

SYSTEM_DEFAULT = (
    "You are a careful assistant. "
    "Use ONLY the provided CONTEXT as data. "
    "If something is missing, say 'not specified' and do not guess."
)

# Retrieval display ordering (hazard task)
CORPUS_ORDER = ["Knowledge", "Memory", "Environment", "Experiences", "OpsState"]

PROMPT_HAZARD_CLASSIFY = """\
You are performing retrieval-conditioned hazard labeling.

Task:
- Pick exactly ONE best-matching hazard card (Top-1) for the given snippet.
- Output MUST be valid JSON in the 'Direct Answer' section (one line).
- Use ONLY CONTEXT as evidence.
- If the best hazard is unclear, still pick the best candidate and lower confidence.

Output format (Markdown):
1) Direct Answer
   - JSON (one line), schema:
     {{"hazard_id":"...","label":"...","confidence":0.0,"evidence":["[Knowledge:.. ...]","..."],"notes":"short"}}
2) Justification (2-6 bullet points, each with citations)

CONTEXT:
{context}

SNIPPET:
{snippet}
"""


# =============================================================================
# Data model
# =============================================================================

@dataclass
class Item:
    content: str
    meta: Dict[str, Any]


# =============================================================================
# Robust JSON reader (BOM/empty/JSONL-friendly)
# =============================================================================

def _read_json_flexible(path: str, *, corpus_name: str) -> Any:
    p = Path(path)

    if not path or not str(path).strip():
        raise ValueError(f"{corpus_name}: corpus path is an empty string")

    if not p.exists():
        raise FileNotFoundError(f"{corpus_name}: file not found: {p}")

    if p.is_dir():
        raise IsADirectoryError(f"{corpus_name}: expected a JSON file but got a directory: {p}")

    txt = p.read_text(encoding="utf-8", errors="strict")
    # Strip UTF-8 BOM and whitespace
    txt2 = txt.lstrip("\ufeff").strip()

    if not txt2:
        raise ValueError(f"{corpus_name}: JSON file is empty (or only whitespace): {p}")

    # Try standard JSON
    try:
        return json.loads(txt2)
    except json.JSONDecodeError:
        # Fallback: JSONL (one JSON object per line)
        lines = [ln.strip() for ln in txt2.splitlines() if ln.strip()]
        if lines:
            out = []
            ok_any = False
            for i, ln in enumerate(lines, start=1):
                try:
                    out.append(json.loads(ln))
                    ok_any = True
                except json.JSONDecodeError as e:
                    raise ValueError(f"{corpus_name}: JSONL parse failed at line {i} in {p}: {e}") from e
            if ok_any:
                return out

        preview = txt2[:200].replace("\n", "\\n")
        raise ValueError(f"{corpus_name}: Failed to parse JSON in {p}. First 200 chars: {preview!r}")


# =============================================================================
# Hazard-card normalization (PATCHED for hazard_cards_v5.json)
# =============================================================================

def _as_list(x: Any) -> List[str]:
    """
    Accepts:
      - list[str|...]
      - str
      - dict (e.g., {"und":[...]} or {"en":"Blackout"})
    Returns flat list[str] (deduped, order-preserving).
    """
    if x is None:
        return []
    out: List[str] = []

    if isinstance(x, list):
        out = [str(v).strip() for v in x if str(v).strip()]
    elif isinstance(x, str) and x.strip():
        out = [x.strip()]
    elif isinstance(x, dict):
        for _k, v in x.items():
            if isinstance(v, list):
                out.extend([str(z).strip() for z in v if str(z).strip()])
            elif isinstance(v, str) and v.strip():
                out.append(v.strip())

    # de-dupe preserve order
    seen = set()
    dedup: List[str] = []
    for s in out:
        if s not in seen:
            dedup.append(s)
            seen.add(s)
    return dedup


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
        parts: List[str] = []
        for v in x:
            if v is None:
                continue
            if isinstance(v, str) and v.strip():
                parts.append(v.strip())
            else:
                parts.append(str(v))
        return ", ".join(parts)
    return str(x).strip()


def _pick_first(d: Dict[str, Any], keys: List[str]) -> Any:
    for k in keys:
        if k in d and d.get(k) not in (None, "", [], {}):
            return d.get(k)
    return None


def _labels_to_label(card: Dict[str, Any]) -> str:
    """
    hazard_cards_v5 has labels: {"en":"Blackout"} (sometimes other language keys)
    """
    labels = card.get("labels")
    if isinstance(labels, dict) and labels:
        v = labels.get("en") or labels.get("und")
        if isinstance(v, str) and v.strip():
            return v.strip()
        for vv in labels.values():
            if isinstance(vv, str) and vv.strip():
                return vv.strip()
    v2 = _pick_first(card, ["label", "prefLabel", "name", "rdfs:label"])
    return str(v2).strip() if isinstance(v2, str) and str(v2).strip() else "not specified"


def hazard_card_to_item(card: Dict[str, Any], idx: int) -> Item:
    """
    Convert one hazard card (hazard_cards_v5.json style) into an Item for BM25 indexing.

    Goal: index *all* useful fields (labels, altLabels, links, sources, sampleData, risk/assessment,
    verbalizations, bm25_text_en, etc.) so that indicator-heavy snippets can match robustly.
    """

    def _get_label(card_obj: Dict[str, Any]) -> str:
        labels = card_obj.get("labels")
        if isinstance(labels, dict):
            for k in ("en", "und", "de"):
                v = labels.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip()
        v = _pick_first(card_obj, ["label", "prefLabel", "name", "rdfs:label"])
        if isinstance(v, str) and v.strip():
            return v.strip()
        return "not specified"

    def _flatten_strings(x: Any, *, max_items: int = 120) -> List[str]:
        out: List[str] = []

        def rec(v: Any) -> None:
            if len(out) >= max_items:
                return
            if v is None:
                return
            if isinstance(v, str):
                s = v.strip()
                if s:
                    out.append(s)
                return
            if isinstance(v, (int, float, bool)):
                out.append(str(v))
                return
            if isinstance(v, dict):
                for kk, vv in v.items():
                    if len(out) >= max_items:
                        break
                    if isinstance(kk, str) and kk.strip():
                        out.append(kk.strip())
                    rec(vv)
                return
            if isinstance(v, list):
                for vv in v:
                    if len(out) >= max_items:
                        break
                    rec(vv)
                return

        rec(x)

        seen = set()
        ded: List[str] = []
        for s in out:
            if s not in seen:
                ded.append(s)
                seen.add(s)
        return ded

    hazard_id = _pick_first(card, ["id", "@id", "hazard_id", "curie", "iri"]) or f"hazard:{idx}"
    label = _get_label(card)

    alt_raw = _pick_first(card, ["altLabel", "aliases", "aka", "synonyms"])
    alt_list: List[str] = _as_list(alt_raw)

    group = _pick_first(card, ["group", "hazardGroup", "category", "domain"]) or ""
    subtype = _pick_first(card, ["subtype", "hazardSubtype"]) or ""

    sources = card.get("sources") or card.get("source") or card.get("dc:source") or []
    sample = card.get("sampleData") or card.get("hasSampleData") or card.get("samples") or []
    verbalized = card.get("verbalized_en") or card.get("verbalized") or []
    bm25_text = card.get("bm25_text_en") or card.get("bm25_text") or ""

    links = card.get("links") or {}
    risk = card.get("risk") or {}

    parts: List[str] = []
    parts.append(f"HAZARD_ID: {hazard_id}")
    parts.append(f"LABEL: {label}")

    if group:
        parts.append(f"GROUP: {_stringify(group)}")
    if subtype:
        parts.append(f"SUBTYPE: {_stringify(subtype)}")

    if alt_list:
        parts.append("ALIASES: " + "; ".join([a for a in alt_list if a][:120]))

    if isinstance(bm25_text, str) and bm25_text.strip():
        parts.append("BM25_TEXT_EN: " + bm25_text.strip())

    vlist = _as_list(verbalized)
    if vlist:
        parts.append("VERBALIZED_EN: " + " ".join(vlist))

    if links:
        lflat = _flatten_strings(links, max_items=160)
        if lflat:
            parts.append("LINKS: " + " ".join(lflat))

    if risk:
        rflat = _flatten_strings(risk, max_items=200)
        if rflat:
            parts.append("RISK: " + " ".join(rflat))

    ssrc = _flatten_strings(sources, max_items=120)
    if ssrc:
        parts.append("SOURCES: " + " ".join(ssrc))

    ssamp = _flatten_strings(sample, max_items=240)
    if ssamp:
        parts.append("SAMPLE_DATA: " + " ".join(ssamp))

    # Compact JSON tail (capped) for schema drift
    try:
        tail = json.dumps(card, ensure_ascii=False)
        if len(tail) > 4000:
            tail = tail[:4000] + "…"
        parts.append("RAW_JSON_TAIL: " + tail)
    except Exception:
        pass

    meta = {
        "nummer": str(idx),
        "artikel": "hazard_card",
        "hazard_id": str(hazard_id),
        "label": str(label),
        "group": _stringify(group),
        "subtype": _stringify(subtype),
    }
    return Item(content="\n".join(parts).strip(), meta=meta)


def load_items_any(path_or_inline: Any, *, corpus_name: str) -> List[Item]:
    """
    Accepts:
      - filepath string
      - inline list/dict

    Special handling:
      - Knowledge can be hazard_cards_v5.json in multiple shapes:
          * list of hazard-card dicts
          * {"hazards":[...]} or {"hazard_cards":[...]} or {"cards":[...]} or {"items":[...]}
          * {"card":{...}} / {"hazard":{...}}
      - Memory can be:
          * list of event dicts (einsatz logs)
          * {"items":[{"content":..., "meta":...}, ...]} form
    """
    raw: Any
    if isinstance(path_or_inline, str):
        raw = _read_json_flexible(path_or_inline, corpus_name=corpus_name)
    else:
        raw = path_or_inline

    # 1) items-wrapper (generic)
    if isinstance(raw, dict) and isinstance(raw.get("items"), list):
        raw_list = raw["items"]
        out: List[Item] = []
        for it in raw_list:
            if not isinstance(it, dict):
                continue
            content = it.get("content")
            meta = it.get("meta") or {}
            if isinstance(content, str) and content.strip():
                if not isinstance(meta, dict):
                    meta = {"meta": meta}
                out.append(Item(content=content.strip(), meta=meta))
        return out

    # 2) Knowledge dict wrappers used by some hazard exports
    if isinstance(raw, dict) and corpus_name.lower() == "knowledge":
        for key in ("hazards", "hazard_cards", "cards", "data"):
            if isinstance(raw.get(key), list):
                raw = raw[key]
                break
        if isinstance(raw, dict):
            for key in ("card", "hazard"):
                if isinstance(raw.get(key), dict):
                    raw = [raw[key]]
                    break

    # 3) raw list
    if isinstance(raw, list):
        if corpus_name.lower() == "knowledge":
            outk: List[Item] = []
            for i, card in enumerate(raw, start=1):
                if isinstance(card, dict):
                    outk.append(hazard_card_to_item(card, i))
            return outk

        # Memory list of log events (eventId/einsatzNr/content/...)
        outm: List[Item] = []
        for i, ev in enumerate(raw, start=1):
            if not isinstance(ev, dict):
                continue
            content = ev.get("content") or ev.get("text") or ev.get("message") or ""
            if not isinstance(content, str) or not content.strip():
                continue
            meta = dict(ev)
            meta.pop("content", None)
            meta.setdefault("artikel", meta.get("meta") or "memory_event")
            meta.setdefault("nummer", str(i))
            if not isinstance(meta.get("meta"), str):
                meta["meta"] = _stringify(meta.get("meta"))
            outm.append(Item(content=content.strip(), meta=meta))
        return outm

    raise ValueError(
        f"{corpus_name}: Unsupported JSON structure (expected list, or dict wrappers like "
        f"{{'items':[...]}}, {{'hazards':[...]}}, got {type(raw)})."
    )


# =============================================================================
# BM25
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
        self.bm25 = BM25Okapi(self.docs_tokens)

    def retrieve(self, query: str, top_k: int) -> List[Tuple[Item, float]]:
        q = _tokenize(query)
        if not q:
            return []
        scores = self.bm25.get_scores(q)
        idx = np.argsort(scores)[::-1][:top_k]
        return [(self.items[i], float(scores[i])) for i in idx]


def _ordered_corpora(indexes: Dict[str, BM25Index]) -> List[str]:
    present = set(indexes.keys())
    ordered = [c for c in CORPUS_ORDER if c in present]
    for c in indexes.keys():
        if c not in ordered:
            ordered.append(c)
    return ordered


def _truncate_context(text: str, limit: int) -> str:
    if not limit or len(text) <= limit:
        return text
    head = text[:limit]
    head = (head.rsplit(" ", 1)[0] or head).rstrip()
    return head + " …"


def format_hits(hits: List[Tuple[Item, float]], corpus_name: str, per_doc_chars: int = 1200) -> str:
    lines: List[str] = []
    for it, _score in hits:
        meta = it.meta or {}
        nummer = meta.get("nummer", "?")
        artikel = meta.get("artikel", "") or ""
        hazard_id = meta.get("hazard_id", "") or ""
        label = meta.get("label", "") or ""

        if corpus_name.lower() == "knowledge" and (hazard_id or label):
            cite = f"[{corpus_name}:{nummer} {hazard_id} {label}]".strip()
        else:
            einsatz = meta.get("einsatzNr") or ""
            event_id = meta.get("eventId") or ""
            tag = f"#{einsatz}" if einsatz else (f"evt:{event_id}" if event_id else "")
            cite = f"[{corpus_name}:{nummer} {tag} {artikel}]".strip()

        txt = it.content or ""
        if per_doc_chars and len(txt) > per_doc_chars:
            txt = _truncate_context(txt, per_doc_chars)

        lines.append(f"{cite} {txt}")
    return "\n\n".join(lines)


def _dedupe_hits(hits: List[Tuple[Item, float]]) -> List[Tuple[Item, float]]:
    seen = set()
    out = []
    for it, sc in hits:
        key = (it.meta or {}).get("nummer") or id(it)
        if key in seen:
            continue
        seen.add(key)
        out.append((it, sc))
    return out


def build_context(
    indexes: Dict[str, BM25Index],
    query: str,
    top_k: Dict[str, int],
    per_doc_chars: int,
    recent_k: Optional[Dict[str, int]] = None,
) -> Tuple[str, Dict[str, str]]:
    recent_k = recent_k or {}
    per: Dict[str, str] = {}
    blocks: List[str] = []

    for corpus in _ordered_corpora(indexes):
        idx = indexes[corpus]
        k = int(top_k.get(corpus, 0))
        rk = int(recent_k.get(corpus, 0))

        hits: List[Tuple[Item, float]] = []
        if k > 0:
            hits.extend(idx.retrieve(query, k))

        if rk > 0:
            recent_items = idx.items[-rk:]
            hits.extend([(it, -1.0) for it in reversed(recent_items)])

        hits = _dedupe_hits(hits)
        block = format_hits(hits, corpus_name=corpus, per_doc_chars=per_doc_chars)
        per[corpus] = block
        if block.strip():
            blocks.append(f"### {corpus}\n{block}")

    return "\n\n".join(blocks).strip(), per


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
    out.append("# Simple RAG Hazard Report (One-shot)\n")
    out.append(f"- **Mode:** `{meta.get('mode','simple_rag_hazard_one_shot')}`")
    out.append(f"- **Model:** `{meta.get('model','')}`")
    out.append(f"- **Base URL:** `{meta.get('base_url','')}`")
    out.append("")
    out.append("## Snippet / Question")
    out.append(meta.get("question", "") or "_not specified_")
    out.append("")
    out.append("## Final Answer")
    out.append(res.get("final", "") or "_not specified_")
    out.append("")
    out.append("## Metrics")
    out.append("```json")
    out.append(json.dumps(res.get("metrics", {}) or {}, ensure_ascii=False, indent=2))
    out.append("```")
    out.append("")
    out.append("## Retrieved Context")
    ctx = (res.get("contexts", {}) or {}).get("pass1", {}) or {}
    if isinstance(ctx, dict) and any((isinstance(v, str) and v.strip()) for v in ctx.values()):
        for corpus, block in ctx.items():
            if not isinstance(block, str) or not block.strip():
                continue
            out.append(f"### {corpus}")
            out.append("```")
            out.append(block.replace("```", "``\\`"))
            out.append("```")
            out.append("")
    else:
        out.append("_none_")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# =============================================================================
# Runner
# =============================================================================

def run_simple_rag_hazard_one_shot(req: Dict[str, Any]) -> Dict[str, Any]:
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
    top_k = ret_cfg.get("top_k") or dict(DEFAULT_TOP_K)
    recent_k = ret_cfg.get("recent_k") or dict(DEFAULT_RECENT_K)
    per_doc_chars = int(ret_cfg.get("per_doc_chars", DEFAULT_PER_DOC_CHARS))
    min_citations = int(ret_cfg.get("min_citations", DEFAULT_MIN_CITATIONS))

    corpora = req.get("corpora") or {}
    if not isinstance(corpora, dict) or not corpora:
        raise ValueError("request.corpora must be a dict of corpus_name -> items")

    # Build indexes (hazard-aware loader)
    indexes: Dict[str, BM25Index] = {}
    for corpus_name, source in corpora.items():
        # Hard fail on empty string path (common runner bug)
        if isinstance(source, str) and not source.strip():
            raise ValueError(f"corpora.{corpus_name} is an empty string path")

        items = load_items_any(source, corpus_name=corpus_name)
        if items:
            for i, it in enumerate(items, start=1):
                it.meta = it.meta if isinstance(it.meta, dict) else {"meta": it.meta}
                it.meta.setdefault("nummer", str(i))
                it.meta.setdefault("artikel", str(it.meta.get("artikel") or it.meta.get("meta") or corpus_name))
            indexes[corpus_name] = BM25Index(items)

    context, per_corpus = build_context(
        indexes, question, top_k=top_k, per_doc_chars=per_doc_chars, recent_k=recent_k
    )

    # extract snippet if present
    snippet = question
    m = re.search(r"\bSNIPPET:\s*(.*)\s*$", question, flags=re.S | re.I)
    if m:
        snippet = m.group(1).strip()

    chat = LocalChat(base_url=base_url, model=model, api_key=api_key)
    final = chat.chat(
        SYSTEM_DEFAULT,
        PROMPT_HAZARD_CLASSIFY.format(context=context, snippet=snippet),
        temperature=temperature,
        max_tokens=max_tokens,
    ).strip()

    c_count = count_inline_citations(final)
    return {
        "final": final,
        "contexts": {"pass1": per_corpus, "pass2": {}},
        "metrics": {
            "citation_count": c_count,
            "min_citations_threshold": min_citations,
            "has_min_citations": bool(c_count >= min_citations),
            "uses_retrieval": True,
            "llm_calls": 1,
        },
        "meta": {"mode": "simple_rag_hazard_one_shot", "model": model, "base_url": base_url, "question": question},
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

    req = _read_json_flexible(args.input, corpus_name="request")
    if args.base_url:
        req.setdefault("llm", {})["base_url"] = args.base_url
    if args.model:
        req.setdefault("llm", {})["model"] = args.model

    res = run_simple_rag_hazard_one_shot(req)

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