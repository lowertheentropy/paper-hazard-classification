#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jsonld_csv_converter_v5.py

Methodology v5 converter:
- Reads OWL/RDF JSON-LD (list of node objects) for *structure* (links, risk/assessment graph, labels if present)
- Reads hazards.csv for *content* (names, groups, keywords/altLabel, sources, hasSampleData, extra link columns)
- Merges both into LLM/BM25-friendly "hazard cards" JSON (stable CURIE ids + auto verbalization)

Inputs (per your v5 notes):
- JSON-LD: hazard_ontology_v5.jsonld
- CSV: hazards.csv
  * keywords live in CSV as "Keywords" + "Keywords (German)" (treated like altLabel/keywords)
  * sources live in CSV as "Source" (and sometimes also in JSON-LD as dc:source)
  * sample data lives in CSV as "hasSampleData" (and sometimes also in JSON-LD as hazards:hasSampleData)
  * extra links from CSV:
      - causedByHazard IDs  -> causedByHazard
      - causedByActivity IDs -> causedByActivity
      - hasConsequence IDs -> hasConsequence
      - createsRisk IDs -> createsRisk
      - relatedToActivity IDs -> relatedToActivity
    (all values expected as semicolon-separated CURIEs; NaN allowed)

Usage:
  python3 jsonld_csv_converter_v5.py \
      hazard_ontology_v5.jsonld \
      hazards.csv \
      hazard_cards_v5.json

Notes:
- IDs remain stable CURIEs; we do NOT "string replace" ids with text.
- Verbalization is generated via generic predicate templates + labels/derived labels.
"""

import argparse
import json
import math
import re
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


# -------------------- IRI constants --------------------
RDFS_LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
SKOS_PREFLABEL = "http://www.w3.org/2004/02/skos/core#prefLabel"
SKOS_ALTLABEL = "http://www.w3.org/2004/02/skos/core#altLabel"

DC_TERMS_SOURCE = "http://purl.org/dc/terms/source"
DC_ELEM_SOURCE = "http://purl.org/dc/elements/1.1/source"

RDF_TYPE = "@type"
ID = "@id"
OWL_NAMED_INDIVIDUAL = "http://www.w3.org/2002/07/owl#NamedIndividual"

HAZARDS_BASE = "http://www.hazardontology.org/hazards#"
HAZARDS_PREFIX = "hazards:"

HAS_SAMPLE_DATA = HAZARDS_BASE + "hasSampleData"

# Object properties (ontology)
PREDICATE_MAP: Dict[str, str] = {
    HAZARDS_BASE + "atLocation": "atLocation",
    HAZARDS_BASE + "relatedToActivity": "relatedToActivity",
    HAZARDS_BASE + "causedBy": "causedBy",
    HAZARDS_BASE + "hasConsequence": "hasConsequence",
    HAZARDS_BASE + "createsRisk": "createsRisk",
}

RISK_PREDICATE_MAP: Dict[str, str] = {
    HAZARDS_BASE + "exposes": "exposes",
    HAZARDS_BASE + "mitigatedBy": "mitigatedBy",
    HAZARDS_BASE + "hasAssessment": "hasAssessment",
}

ASSESSMENT_PREDICATE_MAP: Dict[str, str] = {
    HAZARDS_BASE + "assessesRisk": "assessesRisk",
    HAZARDS_BASE + "hasLikelihood": "hasLikelihood",
    HAZARDS_BASE + "hasSeverity": "hasSeverity",
    HAZARDS_BASE + "hasRiskLevel": "hasRiskLevel",
}

# CSV link columns (methodology v5)
CSV_LINK_COLS: Dict[str, str] = {
    "causedByHazard IDs": "causedByHazard",
    "causedByActivity IDs": "causedByActivity",
    "hasConsequence IDs": "hasConsequence",
    "createsRisk IDs": "createsRisk",
    "relatedToActivity IDs": "relatedToActivity",
    # optional: allow atLocation if you add it later
    "atLocation IDs": "atLocation",
}

TEMPLATES_EN: Dict[str, str] = {
    # core
    "atLocation": "Location: {items}.",
    "relatedToActivity": "Related activity: {items}.",
    "causedBy": "Caused by: {items}.",
    "hasConsequence": "Consequences: {items}.",
    "createsRisk": "Creates risk: {items}.",
    # v5 split
    "causedByHazard": "Caused by hazard(s): {items}.",
    "causedByActivity": "Caused by activity/condition(s): {items}.",
    # risk
    "exposes": "Exposes: {items}.",
    "mitigatedBy": "Mitigation: {items}.",
    "hasAssessment": "Assessment: {items}.",
    "assessesRisk": "Assesses risk: {items}.",
    "hasLikelihood": "Likelihood: {items}.",
    "hasSeverity": "Severity: {items}.",
    "hasRiskLevel": "Risk level: {items}.",
    # retrieval extras
    "keywords_en": "Keywords: {items}.",
    "keywords_de": "Schlüsselwörter: {items}.",
    "sources": "Sources: {items}.",
    "sample": "Sample data: {items}.",
}


# -------------------- helpers --------------------
def ensure_list(x: Any) -> List[Any]:
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def is_nan(x: Any) -> bool:
    try:
        return isinstance(x, float) and math.isnan(x)
    except Exception:
        return False


def iri_to_curie(iri: str) -> str:
    if isinstance(iri, str) and iri.startswith(HAZARDS_BASE):
        return HAZARDS_PREFIX + iri[len(HAZARDS_BASE):]
    return iri


def curie_or_iri_local_name(x: str) -> str:
    if x.startswith(HAZARDS_PREFIX):
        return x.split(":", 1)[1]
    if "#" in x:
        return x.rsplit("#", 1)[1]
    if "/" in x:
        return x.rsplit("/", 1)[1]
    return x


def derive_label_from_local_name(local: str) -> str:
    local2 = re.sub(
        r"^(Hazard|Risk|Consequence|Activity|Agent|Location|Assessment|Failure|Process|Likelihood|Severity|Control)_(.+)$",
        r"\2",
        local,
    )
    tokens: List[str] = []
    for part in local2.split("_"):
        part_spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", part)
        tokens.extend(part_spaced.split())

    if not tokens:
        return local2

    out = []
    for i, t in enumerate(tokens):
        if t.isupper() and len(t) <= 6:
            out.append(t)
        else:
            out.append(t.lower() if i > 0 else t.capitalize())
    return " ".join(out)


def pick_label(node: Dict[str, Any], preferred_lang: str = "en") -> Optional[str]:
    for pred in (RDFS_LABEL, SKOS_PREFLABEL):
        vals = node.get(pred)
        if not vals:
            continue
        vals = ensure_list(vals)
        best = None
        fallback = None
        for v in vals:
            if isinstance(v, dict) and "@value" in v:
                if v.get("@language") == preferred_lang:
                    return str(v["@value"])
                if "@language" not in v:
                    fallback = str(v["@value"])
                if best is None:
                    best = str(v["@value"])
        return fallback or best
    return None


def objects_from_pred(node: Dict[str, Any], pred_iri: str) -> List[str]:
    out: List[str] = []
    for obj in ensure_list(node.get(pred_iri)):
        if isinstance(obj, dict) and ID in obj:
            out.append(obj[ID])
        elif isinstance(obj, str):
            out.append(obj)
    return out


def literal_values(node: Dict[str, Any], pred_iri: str) -> List[str]:
    vals = ensure_list(node.get(pred_iri))
    out_all: List[str] = []
    for v in vals:
        if isinstance(v, dict) and "@value" in v:
            out_all.append(str(v["@value"]))
        elif isinstance(v, str):
            out_all.append(v)
    # de-dup preserve order
    seen = set()
    ordered = []
    for s in out_all:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    return ordered


def split_semicolon_list(s: Any) -> List[str]:
    if s is None or is_nan(s):
        return []
    if isinstance(s, list):
        items = [str(x).strip() for x in s if str(x).strip()]
        return unique_preserve(items)
    txt = str(s).strip()
    if not txt:
        return []
    parts = [p.strip() for p in txt.split(";")]
    return unique_preserve([p for p in parts if p])


def unique_preserve(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def build_index(nodes: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for n in nodes:
        if isinstance(n, dict) and ID in n:
            idx[n[ID]] = n
    return idx


def build_label_map_curie(idx: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    labels: Dict[str, str] = {}
    for iri, node in idx.items():
        lab = pick_label(node, "en")
        if lab:
            labels[iri_to_curie(iri)] = lab
    return labels


def label_for_id(x: str, labels_by_curie: Dict[str, str]) -> str:
    cur = iri_to_curie(x) if isinstance(x, str) and x.startswith("http") else str(x)
    if cur in labels_by_curie:
        return labels_by_curie[cur]
    return derive_label_from_local_name(curie_or_iri_local_name(cur))


def is_named_individual(node: Dict[str, Any]) -> bool:
    return OWL_NAMED_INDIVIDUAL in ensure_list(node.get(RDF_TYPE))


def is_hazard_individual(node: Dict[str, Any]) -> bool:
    iri = node.get(ID, "")
    return (
        is_named_individual(node)
        and isinstance(iri, str)
        and (iri.startswith(HAZARDS_BASE + "Hazard_") or "#Hazard_" in iri)
    )


def verbalize_section(
    key: str,
    items: List[str],
    labels_by_curie: Dict[str, str],
    templates: Dict[str, str],
) -> Optional[str]:
    if not items:
        return None
    tmpl = templates.get(key)
    if not tmpl:
        return None
    rendered = "; ".join(label_for_id(i, labels_by_curie) for i in items)
    return tmpl.format(items=rendered)


def verbalize_links_en(
    links: Dict[str, List[str]],
    labels_by_curie: Dict[str, str],
) -> List[str]:
    lines: List[str] = []
    for key, items in links.items():
        line = verbalize_section(key, items, labels_by_curie, TEMPLATES_EN)
        if line:
            lines.append(line)
    return lines


# -------------------- conversion --------------------
def extract_ontology_hazards(idx: Dict[str, Dict[str, Any]], labels_by_curie: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """
    Build hazard cards from JSON-LD only (structure-first),
    later merged/overwritten by CSV content.
    """
    out: Dict[str, Dict[str, Any]] = {}

    for iri, node in idx.items():
        if not is_hazard_individual(node):
            continue

        hazard_curie = iri_to_curie(iri)
        hazard_label_en = pick_label(node, "en") or derive_label_from_local_name(curie_or_iri_local_name(hazard_curie))

        links: Dict[str, List[str]] = {}
        for pred_iri, short_key in PREDICATE_MAP.items():
            objs = objects_from_pred(node, pred_iri)
            if objs:
                links[short_key] = [iri_to_curie(o) for o in objs]

        # sources / sampleData / altLabel might exist in JSON-LD too
        sources = unique_preserve(literal_values(node, DC_TERMS_SOURCE) + literal_values(node, DC_ELEM_SOURCE))
        sample_data = literal_values(node, HAS_SAMPLE_DATA)

        # altLabel in ontology if present (rare)
        alt_raw = node.get(SKOS_ALTLABEL)
        alt = {"und": []}
        if alt_raw:
            vals = ensure_list(alt_raw)
            items = []
            for v in vals:
                if isinstance(v, dict) and "@value" in v:
                    items.append(str(v["@value"]))
                elif isinstance(v, str):
                    items.append(v)
            alt["und"] = unique_preserve([x.strip() for x in items if str(x).strip()])

        card = {
            "id": hazard_curie,
            "type": "hazards:Hazard",
            "labels": {"en": hazard_label_en},
            "links": links,
            "sources": sources,
            "sampleData": sample_data,
            "altLabel": alt if alt.get("und") else {},
        }
        out[hazard_curie] = card

    return out


def merge_csv_into_cards(
    cards: Dict[str, Dict[str, Any]],
    csv_path: str,
    labels_by_curie: Dict[str, str],
) -> Dict[str, Dict[str, Any]]:
    df = pd.read_csv(csv_path)

    # basic validation / helpful error
    required_cols = ["Hazard ID", "Hazard Name"]
    for c in required_cols:
        if c not in df.columns:
            raise SystemExit(f"CSV missing required column: {c}")

    for _, row in df.iterrows():
        hazard_id = str(row.get("Hazard ID")).strip()
        if not hazard_id:
            continue

        card = cards.get(hazard_id, {
            "id": hazard_id,
            "type": "hazards:Hazard",
            "labels": {},
            "links": {},
            "sources": [],
            "sampleData": [],
            "altLabel": {},
        })

        # --- content fields from CSV ---
        name_en = row.get("Hazard Name")
        if name_en is not None and not is_nan(name_en) and str(name_en).strip():
            card.setdefault("labels", {})
            card["labels"]["en"] = str(name_en).strip()

        # optional metadata
        for col, out_key in [
            ("Description", "description"),
            ("Hazard Group", "group"),
            ("Hazard Subtype", "subtype"),
        ]:
            val = row.get(col)
            if val is not None and not is_nan(val) and str(val).strip():
                card[out_key] = str(val).strip()

        # keywords (treated as altLabel/keywords)
        kw_en = split_semicolon_list(row.get("Keywords"))
        kw_de = split_semicolon_list(row.get("Keywords (German)"))

        # store language-keyed altLabel
        alt = card.get("altLabel") or {}
        if kw_en:
            alt["en"] = unique_preserve((alt.get("en") or []) + kw_en)
        if kw_de:
            alt["de"] = unique_preserve((alt.get("de") or []) + kw_de)
        card["altLabel"] = alt

        # flattened keywords for retrieval convenience
        flat_keywords = unique_preserve((card.get("keywords") or []) + kw_en + kw_de)
        if flat_keywords:
            card["keywords"] = flat_keywords

        # sources
        src = row.get("Source")
        if src is not None and not is_nan(src) and str(src).strip():
            card["sources"] = unique_preserve((card.get("sources") or []) + [str(src).strip()])

        # sample data
        sd = row.get("hasSampleData")
        if sd is not None and not is_nan(sd) and str(sd).strip():
            card["sampleData"] = unique_preserve((card.get("sampleData") or []) + [str(sd).strip()])

        # --- v5 link columns (CSV) ---
        links = card.get("links") or {}

        # merge any csv-specified link lists (these are CURIEs already)
        for csv_col, link_key in CSV_LINK_COLS.items():
            if csv_col not in df.columns:
                continue
            items = split_semicolon_list(row.get(csv_col))
            if not items:
                continue
            links[link_key] = unique_preserve((links.get(link_key) or []) + items)

        card["links"] = links
        cards[hazard_id] = card

    return cards


def enrich_risk_assessment_from_ontology(
    cards: Dict[str, Dict[str, Any]],
    idx: Dict[str, Dict[str, Any]],
    labels_by_curie: Dict[str, str],
) -> None:
    """
    If a hazard has createsRisk, follow the JSON-LD graph:
      hazard -> Risk -> Assessment
    and attach compact nested blocks (keeps ids stable).
    """
    for hazard_id, card in cards.items():
        links = card.get("links") or {}
        creates_risk = links.get("createsRisk") or []
        if not creates_risk:
            continue

        # take first risk for compactness
        risk_curie = creates_risk[0]
        risk_iri = HAZARDS_BASE + curie_or_iri_local_name(risk_curie) if risk_curie.startswith(HAZARDS_PREFIX) else risk_curie
        risk_node = idx.get(risk_iri)
        if not risk_node:
            continue

        risk_links: Dict[str, List[str]] = {}
        for pred_iri, short_key in RISK_PREDICATE_MAP.items():
            objs = objects_from_pred(risk_node, pred_iri)
            if objs:
                risk_links[short_key] = [iri_to_curie(o) for o in objs]

        risk_block: Dict[str, Any] = {
            "id": risk_curie,
            "type": "hazards:Risk",
            "links": risk_links,
        }

        # assessment
        has_assess = risk_links.get("hasAssessment") or []
        if has_assess:
            assess_curie = has_assess[0]
            assess_iri = HAZARDS_BASE + curie_or_iri_local_name(assess_curie) if assess_curie.startswith(HAZARDS_PREFIX) else assess_curie
            assess_node = idx.get(assess_iri)
            if assess_node:
                assessment_links: Dict[str, List[str]] = {}
                for pred_iri, short_key in ASSESSMENT_PREDICATE_MAP.items():
                    objs = objects_from_pred(assess_node, pred_iri)
                    if objs:
                        assessment_links[short_key] = [iri_to_curie(o) for o in objs]
                risk_block["assessment"] = {
                    "id": assess_curie,
                    "type": "hazards:RiskAssesment",
                    "links": assessment_links,
                }

        card["risk"] = risk_block


def finalize_verbalization(cards: Dict[str, Dict[str, Any]], labels_by_curie: Dict[str, str]) -> None:
    """
    Add verbalized_en + bm25_text_en deterministically from:
    - links (including v5 split causedByHazard/causedByActivity if present)
    - keywords (en/de)
    - sources
    - sampleData
    """
    for _, card in cards.items():
        links = card.get("links") or {}
        verbalized: List[str] = []

        # stable ordering improves determinism + BM25 predictability
        ordered_link_keys = [
            "atLocation",
            "relatedToActivity",
            "causedByHazard",
            "causedByActivity",
            "causedBy",          # if ontology used the generic property
            "hasConsequence",
            "createsRisk",
        ]
        for k in ordered_link_keys:
            if k in links:
                line = verbalize_section(k, links.get(k) or [], labels_by_curie, TEMPLATES_EN)
                if line:
                    verbalized.append(line)

        # keywords lines (separate en/de if available)
        alt = card.get("altLabel") or {}
        kw_en = alt.get("en") or []
        kw_de = alt.get("de") or []
        if kw_en:
            verbalized.append(TEMPLATES_EN["keywords_en"].format(items="; ".join(kw_en)))
        if kw_de:
            verbalized.append(TEMPLATES_EN["keywords_de"].format(items="; ".join(kw_de)))

        # sources
        src = card.get("sources") or []
        if src:
            verbalized.append(TEMPLATES_EN["sources"].format(items="; ".join(src)))

        # sample data
        sd = card.get("sampleData") or []
        if sd:
            verbalized.append(TEMPLATES_EN["sample"].format(items="; ".join(sd)))

        card["verbalized_en"] = verbalized
        card["bm25_text_en"] = " ".join(verbalized)

        # also verbalize nested risk/assessment if present (optional, compact)
        if "risk" in card and isinstance(card["risk"], dict):
            rlinks = card["risk"].get("links") or {}
            rverb = verbalize_links_en(rlinks, labels_by_curie)
            card["risk"]["verbalized_en"] = rverb
            if "assessment" in card["risk"] and isinstance(card["risk"]["assessment"], dict):
                alinks = card["risk"]["assessment"].get("links") or {}
                averb = verbalize_links_en(alinks, labels_by_curie)
                card["risk"]["assessment"]["verbalized_en"] = averb


def convert(jsonld_path: str, csv_path: str) -> Dict[str, Any]:
    # load JSON-LD
    with open(jsonld_path, "r", encoding="utf-8") as f:
        nodes = json.load(f)
    if not isinstance(nodes, list):
        raise SystemExit("Expected JSON-LD as a list of node objects at top-level.")

    idx = build_index(nodes)
    labels_by_curie = build_label_map_curie(idx)

    # 1) structure-first cards from ontology
    cards = extract_ontology_hazards(idx, labels_by_curie)

    # 2) merge CSV content + v5 link columns
    cards = merge_csv_into_cards(cards, csv_path, labels_by_curie)

    # 3) enrich hazard->risk->assessment from ontology graph where possible
    enrich_risk_assessment_from_ontology(cards, idx, labels_by_curie)

    # 4) finalize verbalization + bm25 text
    finalize_verbalization(cards, labels_by_curie)

    hazards_sorted = sorted(cards.values(), key=lambda x: x.get("id", ""))

    return {
        "meta": {
            "schema_version": "hazard-cards-v5",
            "namespaces": {HAZARDS_PREFIX[:-1]: HAZARDS_BASE},
            "inputs": {
                "jsonld": jsonld_path,
                "csv": csv_path,
            },
            "notes": (
                "Merged ontology (structure) + hazards.csv (content). "
                "Keywords are sourced from CSV and stored as skos-like altLabel plus a flattened keywords list. "
                "Sources are taken from CSV Source and/or dc:source in JSON-LD. "
                "Sample data is taken from CSV hasSampleData and/or hazards:hasSampleData in JSON-LD. "
                "IDs remain stable CURIEs; verbalization is generated via templates (no per-hazard handcrafted text)."
            ),
        },
        "hazards": hazards_sorted,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonld", help="Path to JSON-LD file (hazard_ontology_v5.jsonld)")
    ap.add_argument("csv", help="Path to hazards.csv")
    ap.add_argument("output", help="Path to output JSON file (hazard cards v5)")
    args = ap.parse_args()

    out = convert(args.jsonld, args.csv)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(out.get('hazards', []))} hazard cards to: {args.output}")


if __name__ == "__main__":
    main()