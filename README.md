# Repository for the Paper: Hazard Classification for Natural and
Anthropogenic Disasters Using
Retrieval-Augmented Large Language Models

> **Paper:** *Hazard Classification for Natural and
Anthropogenic Disasters Using
Retrieval-Augmented Large Language Models*  

This repository contains the experimental code, hazard knowledge artifacts, and evaluation assets used in the paper. It demonstrates a **transparent, auditable, and resource-efficient** Retrieval-Augmented Generation (RAG) pipeline for **hazard classification** under constrained conditions (e.g., edge devices, limited connectivity, local execution).

The core idea is to combine:

- a **database/ontology-grounded hazard knowledge base** (OWL/RDF + JSON hazard cards),
- a deterministic lexical retriever (**Okapi BM25**),
- and a locally deployable LLM for **evidence-constrained hazard labeling** and operator-facing reasoning.

The system is designed to map **free-text, indicator-heavy, alias-heavy reports** (e.g., dispatch notes, monitoring snippets, incident narratives) to a **stable hazard label space**, while preserving provenance and interpretability.

---

## Project overview

Many hazard-related descriptions in operational settings do **not** arrive as canonical labels. Instead, they are reported as:

- symptoms / indicators,
- informal descriptions,
- aliases or colloquial names,
- partial telemetry snapshots,
- noisy free-text logs.

This repository demonstrates a **database-first hazard classification workflow** that addresses this problem by grounding LLM outputs in a curated hazard catalogue.

### Why this matters
Hazard classification in emergency-management-like settings often requires:

- **low latency**
- **offline / local capability**
- **auditable evidence linkage**
- **stable and explicit label spaces**
- **robustness to phrasing variation and alias-heavy reports**

The repository focuses on a **simple, transparent baseline** so that observed behavior can be attributed to:
1. the quality of the hazard representation, and  
2. the retrieval + evidence-constrained classification process,  
rather than opaque multi-stage optimization.

---

## What this repository contains

This repo is organized around **three main layers**:

### 1) Formal semantics layer (authoritative hazard ontology)
- Hazard concepts and relations represented in **OWL/RDF / JSON-LD**
- Stable identifiers (hazards, causes, consequences, risks, etc.)
- Typed relations and semantic structure for consistency and future interoperability

Main artifact (from the project root):
- `hazard_ontology.jsonld`

---

### 2) Retrieval layer (ontology-derived hazard card index)
- Compact hazard entries (“hazard cards”) optimized for lexical retrieval and prompting
- Includes:
  - canonical labels
  - aliases / alternative labels
  - indicators / keywords
  - triggers
  - impacts
  - cascading/secondary hazard links
  - provenance
  - sample data hooks (where available)
- Designed for **BM25 indexing** and **evidence-bounded LLM prompting**

Main artifacts:
- `hazard_cards.json`
- `hazards.xlsx` (spreadsheet view / curation support)

---

### 3) Evaluation + scoring layer
- Testcases, scenario runs, memory/no-memory variants, and scoring scripts
- Human rating summaries and auto-scoring support
- Comparison of simple RAG vs. LLM-only baselines in selected hazard scenarios

Main artifacts (examples from your current structure):
- `summary_rater1.csv`
- `summary_rater_2.csv`
- `summary_rater3.csv`
- `scenario_runs_compare/` (timestamped scenario run outputs)
- `scoring/` (testcases, memory variants, scoring configs)

---

## How this maps to the paper

This codebase corresponds to the paper’s main contributions:

- **Hazard ontology design (formal semantics layer)**  
  OWL/RDF-based hazard representation with stable identifiers and typed relations.

- **Ontology-derived hazard card index (retrieval layer)**  
  JSON hazard cards optimized for sparse retrieval (BM25) and evidence-bounded prompting.

- **Retrieval-conditioned hazard classification pipeline**  
  BM25 retrieval + LLM classification on compact retrieved context.

- **Human-centered evaluation (ODSC) + robustness probe**  
  Operator-centered assessment of usability and supplementary auto-scoring under perturbed inputs.

---

## Core design idea

The repository separates **semantics** and **retrieval** on purpose:

### Formal layer (meaning / consistency)
The ontology captures what a hazard *is* and how it relates to other entities:
- `causedBy`
- `hasConsequence`
- `createsRisk`
- `mitigatedBy`
- scope / horizon / assessment context (where modeled)

### Retrieval layer (discoverability under real text)
The hazard-card JSON makes the same knowledge retrievable from noisy text by adding:
- aliases (`altLabel`)
- lexical anchors / keywords
- verbalized relation phrases
- concatenated BM25-friendly text fields
- provenance and sample-data snippets

This makes the system more resilient when inputs describe **indicators** rather than canonical hazard names.

---

## Main scripts and components

### `src/eval/simple-rag.py`
Main simple-RAG evaluation/classification runner (BM25 + LLM). Typical responsibilities:

1. Load hazard-card JSON (and optionally memory/event context)
2. Build or query a BM25 retriever
3. Retrieve top-k hazard candidates for each snippet
4. Construct an evidence-bounded prompt
5. Run LLM classification / justification
6. Save outputs for scoring / comparison

---

### `src/eval/simplerag-scenario-test-hazard.py`
Scenario-oriented hazard evaluation script (likely for predefined hazard testcases / vignettes). Typically used to:

- run structured hazard test sets,
- inspect retrieval behavior,
- compare outputs across scenarios,
- generate traceable run artifacts for later review.

### `src/converter/jsonld_csv_converter_v5.py`
Converter utility for transforming ontology-derived data into tabular / CSV-compatible formats (e.g., for inspection, curation, or downstream scoring workflows).

### `src/odsc-ui/`
UI tooling for ODSC-related review/rating workflows (web interface components and server).

---

## Scoring and evaluation assets

The `scoring/` directory contains the inputs used for structured evaluation and robustness probing, including:

- `testcases.json` — main testcase definitions
- `autoscoring-testcases.json` — cases for auxiliary auto-scoring / robustness probe
- `no-memory.json` — memory-disabled baseline context
- `memory-*.json` — scenario-specific memory snapshots / operational context variants
- `experiences.json` — supporting metadata/config used in scoring workflows (project-specific)

The repository root also contains human-rater summaries:
- `summary_rater1.csv`
- `summary_rater_2.csv`
- `summary_rater3.csv`

These support aggregation and comparison of operator-centered ratings (e.g., ODSC).

---

## Limitations

This codebase reflects the paper’s prototype scope and inherits important limitations:

- Hazard coverage is curated and not exhaustive
- Retrieval quality remains sensitive to lexical mismatch and alias coverage
- BM25 is transparent but limited compared with stronger hybrid retrievers
- LLM outputs may still overgeneralize or hallucinate without strict prompting
- Human-centered evaluation (ODSC) is structured but not a full clinical/operational validation
- The system is not an operational dispatch or command automation tool

---

## Safety, scope, and intended use

This repository is a **research prototype** for hazard classification and evidence-bounded interpretation.

It is **not**:
- a medical device,
- a certified emergency-management system,
- a clinical decision support tool,
- or an autonomous operational decision engine.

It must **not** be used for diagnosis, treatment decisions, emergency command decisions, or automated high-stakes actions without qualified human oversight.

All examples are illustrative and do not replace professional judgment, validated guidance, or applicable regulations.

---

## Declarations

### AI-Assisted Language Editing
Parts of the linguistic editing, sentence restructuring, and grammatical refinement of the associated article and/or repository documentation were supported by AI-based tools (e.g., DeepL, ChatGPT GPT-5.2, Claude Sonnet 4.5) to improve readability and linguistic clarity. However, the scientific content, conceptual development, data analysis, and all critical analyses were carried out by the authors without automated assistance. The use of such tools was limited to language optimization and did not affect the intellectual or methodological integrity of the work.

### Scope and Non-Medical Disclaimer
This work evaluates system output quality against **project-defined requirements** and provided reference materials, focusing on consistency, traceability, and controllability (e.g., evidence linkage, gap detection, conflict flagging). It is **not** a demonstration of clinical validity, evidence-based medicine (EBM), or guideline adherence, and it does not establish medical correctness or operational effectiveness of any measures. The system is a general-purpose software prototype and **not** a medical application/device; it is **not** intended for diagnosis, treatment decisions, or emergency management automation, nor for use in automated high-stakes systems without a qualified human in the loop.

