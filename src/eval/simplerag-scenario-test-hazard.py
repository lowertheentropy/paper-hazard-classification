#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simplerag-scenario-test-hazard.py (BASELINE COMPARISON RUNNER — NO SRCOT)

Runs the same testcase suite with multiple METHODS:

- simple_rag -> calls external script simple-rag.py via subprocess (retrieval baseline)
- llm_only   -> calls external script llm.py via subprocess (NO retrieval baseline)

Outputs:
out_dir/<timestamp>/<method>/<model>/<TC...>/{request.json,result.json,report.md}

Also writes:
- summary.jsonl / summary.csv
- report_final_answers_wide.csv  (final answers side-by-side per testcase+model, with folder path)

Usage example:
python3 simplerag-scenario-test-hazard.py \
  --base_url http://localhost:1234/v1 \
  --api_key lm-studio \
  --memory_dir . \
  --knowledge ./hazard_cards_v5.json \
  --experiences ./experiences.json \
  --environment ./environment.json \
  --ops_state_dir ./scenario-01 \
  --models gpt-oss-120b \
  --methods simple_rag,llm_only \
  --simple_rag_script ./simple-rag.py \
  --llm_only_script ./llm.py \
  --testcases ./testcases.json \
  --max_tokens 131072

Notes:
- simple_rag_script and llm_only_script must exist if the method is enabled.
- ops_state snapshots are resolved strictly by timestamp:
    ops_state_dir/ops_state-<memoryStamp>.json OR .txt
  No fallbacks. If missing: OpsState is not injected; run continues.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# =============================================================================
# Prompts (defaults only; dynamic suites are loaded via --testcases)
# =============================================================================

PROMPT_STATUS = (
    "Status Report: Welche Einsätze laufen gerade? "
    "Erstelle eine kurze Liste sowie eine kleine Gesamtzusammenfassung in ein paar Sätzen: "
    "EinsatzNr, Titel, Prio, Domain, Ort, Beschickung (zugeteilt/aktiv), letzter Stand (aus Logs). "
    "Wenn etwas fehlt: 'not specified'."
)

# =============================================================================
# Testcase model
# =============================================================================

@dataclass
class TestCase:
    id: str
    name: str
    question: str
    memory_file: str
    focus_prefix: str = ""


DEFAULT_TESTCASES: List[TestCase] = [
    TestCase(id="TC1", name="STATUS_REPORT", question=PROMPT_STATUS, memory_file="scenario-01/memory-1769410530238.json"),
]

DEFAULT_MODELS = ["openai/gpt-oss-120b"]


# =============================================================================
# Helpers
# =============================================================================

def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _now_stamp() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def _sanitize(s: str) -> str:
    out = []
    for ch in s:
        if ch.isalnum() or ch in ("-", "_", "."):
            out.append(ch)
        else:
            out.append("_")
    return "".join(out)[:120].strip("_") or "x"


def _load_manifest(path: Path) -> Dict[str, Any]:
    data = _read_json(path)
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    return data


def _load_testcases_file(path: Path) -> List[TestCase]:
    data = _read_json(path)

    if isinstance(data, dict) and isinstance(data.get("testcases"), list):
        raw_list = data["testcases"]
    elif isinstance(data, list):
        raw_list = data
    else:
        raise ValueError("--testcases must be a JSON list or {\"testcases\": [...]}")

    out: List[TestCase] = []
    for i, t in enumerate(raw_list, start=1):
        if not isinstance(t, dict):
            continue

        tc_id = str(t.get("id") or f"TC{i}").strip()
        name = str(t.get("name") or "Unnamed").strip()
        memory_file = str(t.get("memory_file") or "").strip()
        focus_prefix = str(t.get("focus_prefix") or "").strip()
        question = str(t.get("question") or "").strip()

        if not question:
            raise ValueError(f"Testcase {tc_id}: 'question' is required in testcases.json")
        if not memory_file:
            raise ValueError(f"Testcase {tc_id}: 'memory_file' is required in testcases.json")

        out.append(TestCase(id=tc_id, name=name, question=question, memory_file=memory_file, focus_prefix=focus_prefix))

    if not out:
        raise ValueError("--testcases file contained no valid testcases")
    return out


def _load_ops_state(path: str) -> Any:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"ops_state not found: {p}")
    if p.suffix.lower() == ".json":
        return _read_json(p)
    return p.read_text(encoding="utf-8")


def _extract_memory_stamp(mem_path: Path) -> str:
    m = re.search(r"memory-(\d+)\.json$", mem_path.name)
    return m.group(1) if m else ""


def _resolve_ops_state_path_timestamp_only(*, tc_mem: Path, ops_state_dir: Path) -> Optional[Path]:
    stamp = _extract_memory_stamp(tc_mem)
    if not stamp:
        return None
    cand_json = ops_state_dir / f"ops_state-{stamp}.json"
    if cand_json.exists():
        return cand_json
    cand_txt = ops_state_dir / f"ops_state-{stamp}.txt"
    if cand_txt.exists():
        return cand_txt
    return None


def _normalize_ops_state_to_corpus(ops_state_obj: Any) -> Optional[Dict[str, Any]]:
    if ops_state_obj is None:
        return None

    if isinstance(ops_state_obj, dict) and isinstance(ops_state_obj.get("items"), list):
        items = []
        for i, it in enumerate(ops_state_obj["items"], start=1):
            if not isinstance(it, dict):
                continue
            content = str(it.get("content", "") or "").strip()
            if not content:
                continue
            meta = it.get("meta") if isinstance(it.get("meta"), dict) else {"meta": str(it.get("meta", "") or "")}
            meta.setdefault("meta", "global_ops_state")
            meta.setdefault("artikel", "overview")
            meta.setdefault("nummer", str(meta.get("nummer") or i))
            items.append({"content": content, "meta": meta})
        return {"items": items}

    if isinstance(ops_state_obj, list):
        items = []
        for i, it in enumerate(ops_state_obj, start=1):
            if not isinstance(it, dict):
                continue
            content = str(it.get("content", "") or "").strip()
            if not content:
                continue
            meta = it.get("meta") if isinstance(it.get("meta"), dict) else {"meta": str(it.get("meta", "") or "")}
            meta.setdefault("meta", "global_ops_state")
            meta.setdefault("artikel", "overview")
            meta.setdefault("nummer", str(meta.get("nummer") or i))
            items.append({"content": content, "meta": meta})
        return {"items": items}

    if isinstance(ops_state_obj, str) and ops_state_obj.strip():
        return {"items": [{"content": ops_state_obj.strip(), "meta": {"meta": "global_ops_state", "artikel": "overview", "nummer": "1"}}]}

    return None


def _parse_kv(spec: str) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for part in (spec or "").split(","):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        try:
            out[k.strip()] = int(v.strip())
        except Exception:
            pass
    return out


def _build_request(
    *,
    question: str,
    base_url: str,
    api_key: str,
    model: str,
    max_tokens: int,
    temperature: float,
    per_doc_chars: int,
    top_k: Dict[str, int],
    recent_k: Dict[str, int],
    knowledge_path: Path,
    experiences_path: Path,
    environment_path: Path,
    memory_path: Path,
    ops_state_corpus: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    corpora: Dict[str, Any] = {
        "Knowledge": str(knowledge_path) if knowledge_path.exists() else {"items": []},
        "Experiences": str(experiences_path) if experiences_path.exists() else {"items": []},
        "Environment": str(environment_path) if environment_path.exists() else {"items": []},
        "Memory": str(memory_path),
    }
    if isinstance(ops_state_corpus, dict) and isinstance(ops_state_corpus.get("items"), list) and ops_state_corpus["items"]:
        corpora["OpsState"] = ops_state_corpus

    return {
        "question": question,
        "llm": {
            "base_url": base_url,
            "model": model,
            "api_key": api_key,
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
        "retrieval": {
            "top_k": top_k,
            "recent_k": recent_k,
            "per_doc_chars": per_doc_chars,
        },
        "corpora": corpora,
        # kept for request-compatibility; baseline runner does not use it
        "judge": {"enabled": False},
    }


def _render_md(result: Dict[str, Any]) -> str:
    meta = result.get("meta", {}) or {}
    return (
        "# Report\n\n"
        f"- Method: `{meta.get('method', meta.get('mode',''))}`\n"
        f"- Model: `{meta.get('model','')}`\n\n"
        "## Question\n\n"
        f"{meta.get('question','')}\n\n"
        "## Final Answer\n\n"
        f"{result.get('final','')}\n"
    )


def _clean_for_csv(s: Any) -> str:
    if s is None:
        return ""
    t = str(s)
    return t.replace("\r\n", "\n").replace("\r", "\n")


def _write_wide_report_csv(
    out_root: Path,
    methods: List[str],
    models: List[str],
    testcases: List[TestCase],
    final_matrix: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]],
) -> Path:
    report_path = out_root / "report_final_answers_wide.csv"

    fields = ["testcase_id", "testcase_name", "model"]
    for m in methods:
        fields += [f"{m}__ok", f"{m}__folder", f"{m}__final"]

    with report_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()

        for model in models:
            for tc in testcases:
                row: Dict[str, Any] = {
                    "testcase_id": tc.id,
                    "testcase_name": tc.name,
                    "model": model,
                }
                key = (model, tc.id)
                per_method = final_matrix.get(key, {})

                for m in methods:
                    rec = per_method.get(m, {})
                    row[f"{m}__ok"] = rec.get("ok", "")
                    row[f"{m}__folder"] = rec.get("folder", "")
                    row[f"{m}__final"] = _clean_for_csv(rec.get("final", ""))

                w.writerow(row)

    return report_path


# =============================================================================
# Main runner
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_url", default=os.environ.get("SRCOT_BASE_URL", "http://localhost:1234/v1"))
    ap.add_argument("--api_key", default=os.environ.get("SRCOT_API_KEY", "lm-studio"))

    ap.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated model list.")
    ap.add_argument("--methods", default="simple_rag,llm_only", help="Comma-separated: simple_rag,llm_only")

    ap.add_argument("--simple_rag_script", default="simple-rag.py", help="Path to simple-rag.py")
    ap.add_argument("--llm_only_script", default="llm.py", help="Path to llm.py")

    ap.add_argument("--testcases", default="", help="Optional testcases.json. If set, overrides --manifest testcases.")
    ap.add_argument("--select", default="", help="Optional comma-separated testcase IDs to run (e.g., TC1,TC3).")
    ap.add_argument("--manifest", default="", help="Optional JSON manifest (models/testcases). Ignored if --testcases is provided.")

    ap.add_argument("--memory_dir", default=".", help="Folder containing memory-*.json snapshots.")
    ap.add_argument("--knowledge", default="hazard_cards_v5.json")
    ap.add_argument("--experiences", default="experiences.json")
    ap.add_argument("--environment", default="environment.json")

    ap.add_argument("--ops_state_dir", required=True, help="Folder containing ops_state-<stamp>.json/.txt snapshots.")
    ap.add_argument("--out_dir", default="scenario_runs_compare", help="Output root folder.")

    ap.add_argument("--max_tokens", type=int, default=131072)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--per_doc_chars", type=int, default=1200)

    ap.add_argument("--top_k", default="Knowledge=250,Memory=250,Experiences=250,Environment=250,OpsState=250")
    ap.add_argument("--recent_k", default="Memory=250,Environment=250,OpsState=250,Knowledge=250,Experiences=250")

    args = ap.parse_args()

    # methods (NO srcot)
    methods = [m.strip().lower() for m in str(args.methods).split(",") if m.strip()]
    valid_methods = {"simple_rag", "llm_only"}
    methods = [m for m in methods if m in valid_methods] or ["simple_rag"]

    base_url = str(args.base_url)
    api_key = str(args.api_key)

    out_root = Path(args.out_dir) / _now_stamp()
    _safe_mkdir(out_root)

    knowledge_path = Path(args.knowledge)
    experiences_path = Path(args.experiences)
    environment_path = Path(args.environment)
    memory_dir = Path(args.memory_dir)

    ops_state_dir = Path(args.ops_state_dir)
    if not ops_state_dir.exists():
        raise FileNotFoundError(f"--ops_state_dir not found: {ops_state_dir}")

    simple_rag_script = Path(args.simple_rag_script)
    llm_only_script = Path(args.llm_only_script)

    if "simple_rag" in methods and not simple_rag_script.exists():
        raise FileNotFoundError(f"--simple_rag_script not found: {simple_rag_script}")
    if "llm_only" in methods and not llm_only_script.exists():
        raise FileNotFoundError(f"--llm_only_script not found: {llm_only_script}")

    top_k = _parse_kv(args.top_k)
    recent_k = _parse_kv(args.recent_k)

    # models
    if args.manifest:
        man = _load_manifest(Path(args.manifest))
        models = [str(x).strip() for x in (man.get("models") or DEFAULT_MODELS) if str(x).strip()]
    else:
        models = [m.strip() for m in str(args.models).split(",") if m.strip()] or list(DEFAULT_MODELS)

    # testcases
    if args.testcases:
        testcases = _load_testcases_file(Path(args.testcases))
    elif args.manifest:
        man = _load_manifest(Path(args.manifest))
        tcs_raw = man.get("testcases", [])
        testcases2: List[TestCase] = []
        for i, t in enumerate(tcs_raw, start=1):
            if not isinstance(t, dict):
                continue
            testcases2.append(
                TestCase(
                    id=str(t.get("id", "")).strip() or f"TC{i}",
                    name=str(t.get("name", "")).strip() or "Unnamed",
                    question=str(t.get("question", "")).strip(),
                    memory_file=str(t.get("memory_file", "")).strip(),
                    focus_prefix=str(t.get("focus_prefix") or "").strip(),
                )
            )
        testcases = testcases2 or DEFAULT_TESTCASES
    else:
        testcases = DEFAULT_TESTCASES

    if args.select:
        wanted = {x.strip() for x in str(args.select).split(",") if x.strip()}
        testcases = [tc for tc in testcases if tc.id in wanted]
        if not testcases:
            raise ValueError("--select filter removed all testcases (no matching IDs).")

    ops_state_cache: Dict[str, Optional[Dict[str, Any]]] = {}

    summary_jsonl = out_root / "summary.jsonl"
    summary_csv = out_root / "summary.csv"

    csv_fields = [
        "timestamp_utc",
        "method",
        "model",
        "testcase_id",
        "testcase_name",
        "memory_file",
        "ops_state_file",
        "ops_state_missing",
        "ok",
        "elapsed_sec",
        "error",
        "out_dir",
    ]

    final_matrix: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]] = {}

    with summary_csv.open("w", encoding="utf-8", newline="") as fcsv:
        writer = csv.DictWriter(fcsv, fieldnames=csv_fields)
        writer.writeheader()

        for method in methods:
            for model in models:
                for tc in testcases:
                    tc_mem = Path(tc.memory_file)
                    if not tc_mem.is_absolute():
                        tc_mem = memory_dir / tc_mem

                    run_ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
                    run_folder = out_root / method / _sanitize(model) / f"{tc.id}__{_sanitize(tc.name)}"
                    _safe_mkdir(run_folder)

                    record: Dict[str, Any] = {
                        "timestamp_utc": run_ts,
                        "method": method,
                        "model": model,
                        "testcase_id": tc.id,
                        "testcase_name": tc.name,
                        "memory_file": str(tc_mem),
                        "ops_state_file": "",
                        "ops_state_missing": False,
                        "ok": False,
                        "elapsed_sec": None,
                        "error": None,
                        "out_dir": str(run_folder),
                    }

                    final_matrix.setdefault((model, tc.id), {}).setdefault(method, {})
                    final_matrix[(model, tc.id)][method] = {"ok": False, "folder": str(run_folder), "final": ""}

                    if not tc_mem.exists():
                        record["error"] = f"memory file not found: {tc_mem}"
                        with summary_jsonl.open("a", encoding="utf-8") as fj:
                            fj.write(json.dumps(record, ensure_ascii=False) + "\n")
                        writer.writerow(record)
                        fcsv.flush()
                        continue

                    question = (tc.focus_prefix or "") + (tc.question or "").strip()

                    # Resolve ops_state strictly by timestamp (used by simple_rag; harmless for llm_only)
                    ops_state_corpus: Optional[Dict[str, Any]] = None
                    ops_path = _resolve_ops_state_path_timestamp_only(tc_mem=tc_mem, ops_state_dir=ops_state_dir)
                    if ops_path:
                        record["ops_state_file"] = str(ops_path)
                        cache_key = str(ops_path)
                        if cache_key in ops_state_cache:
                            ops_state_corpus = ops_state_cache[cache_key]
                        else:
                            try:
                                ops_obj = _load_ops_state(cache_key)
                                ops_state_corpus = _normalize_ops_state_to_corpus(ops_obj)
                            except Exception:
                                ops_state_corpus = None
                            ops_state_cache[cache_key] = ops_state_corpus
                    else:
                        record["ops_state_missing"] = True

                    req = _build_request(
                        question=question,
                        base_url=base_url,
                        api_key=api_key,
                        model=model,
                        max_tokens=int(args.max_tokens),
                        temperature=float(args.temperature),
                        per_doc_chars=int(args.per_doc_chars),
                        top_k=top_k,
                        recent_k=recent_k,
                        knowledge_path=knowledge_path,
                        experiences_path=experiences_path,
                        environment_path=environment_path,
                        memory_path=tc_mem,
                        ops_state_corpus=ops_state_corpus,
                    )

                    req_path = run_folder / "request.json"
                    res_path = run_folder / "result.json"
                    md_path = run_folder / "report.md"
                    _write_json(req_path, req)

                    t0 = time.time()
                    result: Dict[str, Any] = {}

                    try:
                        if method == "simple_rag":
                            tmp_out = run_folder / "simple_rag_result.json"
                            tmp_md = run_folder / "simple_rag_report.md"
                            cmd = [
                                "python3",
                                str(simple_rag_script),
                                "--input",
                                str(req_path),
                                "--out",
                                str(tmp_out),
                                "--out_md",
                                str(tmp_md),
                            ]
                            p = subprocess.run(cmd, capture_output=True, text=True)
                            if p.returncode != 0:
                                raise RuntimeError(f"simple-rag.py failed: {p.stderr.strip() or p.stdout.strip()}")
                            result = json.loads(tmp_out.read_text(encoding="utf-8"))
                            result.setdefault("meta", {})
                            result["meta"].update({"method": "simple_rag", "model": model, "base_url": base_url, "question": question})

                        else:  # llm_only
                            tmp_out = run_folder / "llm_only_result.json"
                            tmp_md = run_folder / "llm_only_report.md"
                            cmd = [
                                "python3",
                                str(llm_only_script),
                                "--input",
                                str(req_path),
                                "--out",
                                str(tmp_out),
                                "--out_md",
                                str(tmp_md),
                            ]
                            p = subprocess.run(cmd, capture_output=True, text=True)
                            if p.returncode != 0:
                                raise RuntimeError(f"llm.py failed: {p.stderr.strip() or p.stdout.strip()}")
                            result = json.loads(tmp_out.read_text(encoding="utf-8"))
                            result.setdefault("meta", {})
                            result["meta"].update({"method": "llm_only", "model": model, "base_url": base_url, "question": question})

                        elapsed = round(time.time() - t0, 3)

                        _write_json(res_path, result)
                        md_path.write_text(_render_md(result), encoding="utf-8")

                        record["ok"] = True
                        record["elapsed_sec"] = elapsed

                        final_text = _clean_for_csv(result.get("final", ""))
                        final_matrix[(model, tc.id)][method] = {
                            "ok": True,
                            "folder": str(run_folder),
                            "final": final_text,
                        }

                    except Exception as e:
                        elapsed = round(time.time() - t0, 3)
                        record["ok"] = False
                        record["elapsed_sec"] = elapsed
                        record["error"] = f"{type(e).__name__}: {e}"
                        (run_folder / "error.txt").write_text(record["error"], encoding="utf-8")

                        final_matrix[(model, tc.id)][method] = {
                            "ok": False,
                            "folder": str(run_folder),
                            "final": "",
                        }

                    with summary_jsonl.open("a", encoding="utf-8") as fj:
                        fj.write(json.dumps(record, ensure_ascii=False) + "\n")
                    writer.writerow(record)
                    fcsv.flush()

    report_path = _write_wide_report_csv(
        out_root=out_root,
        methods=methods,
        models=models,
        testcases=testcases,
        final_matrix=final_matrix,
    )

    print(f"Done. Results in: {out_root}")
    print(f"- {summary_jsonl}")
    print(f"- {summary_csv}")
    print(f"- {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())