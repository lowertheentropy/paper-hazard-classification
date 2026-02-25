#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autoscoring-scenario-test-hazard.py (AUTO-SCORING BASELINE RUNNER — NO SRCOT)

Runs a hazard-classification testcase suite with multiple METHODS and auto-scores
whether the model output contains the expected hazard id (Top-1).

Methods:
- simple_rag -> external script (e.g., simple-rag.py)
- llm_only   -> external script (e.g., llm.py)  [your memory-only baseline]

Inputs:
- --testcases testcases-auto.json (must contain expected_hazard_id per testcase)

Outputs:
out_dir/<timestamp>/<method>/<model>/<TC...>/{request.json,result.json,report.md}

Also writes:
- summary.jsonl / summary.csv
- auto_scores.csv                  (per testcase: expected vs predicted + correct)
- auto_scores_by_method.csv        (accuracy per method+model)
- report_final_answers_wide.csv    (final answers side-by-side per testcase+model, with folder path)

Usage example:
python3 autoscoring-scenario-test-hazard.py \
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
  --llm_only_script ./autoscoring-llm.py \
  --testcases ./autoscoring-testcases.json \
  --max_tokens 131072
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
# Testcase model
# =============================================================================

@dataclass
class TestCase:
    id: str
    name: str
    question: str
    memory_file: str
    expected_hazard_id: str
    expected_label: str = ""
    focus_prefix: str = ""


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


def _load_testcases_file(path: Path) -> List[TestCase]:
    data = _read_json(path)

    raw_list: Any = None
    if isinstance(data, dict) and isinstance(data.get("testcases"), list):
        raw_list = data["testcases"]
    elif isinstance(data, list):
        raw_list = data
    else:
        raise ValueError("--testcases must be a JSON list")

    out: List[TestCase] = []
    for i, t in enumerate(raw_list, start=1):
        if not isinstance(t, dict):
            continue

        tc_id = str(t.get("id") or f"TC{i}").strip()
        name = str(t.get("name") or "Unnamed").strip()
        memory_file = str(t.get("memory_file") or "").strip()
        focus_prefix = str(t.get("focus_prefix") or "").strip()
        question = str(t.get("question") or "").strip()

        expected_hazard_id = str(t.get("expected_hazard_id") or "").strip()
        expected_label = str(t.get("expected_label") or "").strip()

        if not question:
            raise ValueError(f"Testcase {tc_id}: 'question' is required")
        if not memory_file:
            raise ValueError(f"Testcase {tc_id}: 'memory_file' is required")
        if not expected_hazard_id:
            raise ValueError(f"Testcase {tc_id}: 'expected_hazard_id' is required")

        out.append(
            TestCase(
                id=tc_id,
                name=name,
                question=question,
                memory_file=memory_file,
                expected_hazard_id=expected_hazard_id,
                expected_label=expected_label,
                focus_prefix=focus_prefix,
            )
        )

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

    def _norm_items(items_like: Any) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        if not isinstance(items_like, list):
            return items
        for i, it in enumerate(items_like, start=1):
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
        return items

    if isinstance(ops_state_obj, dict) and isinstance(ops_state_obj.get("items"), list):
        items = _norm_items(ops_state_obj["items"])
        return {"items": items} if items else None

    if isinstance(ops_state_obj, list):
        items = _norm_items(ops_state_obj)
        return {"items": items} if items else None

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
        "judge": {"enabled": False},  # compatibility only
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


# -----------------------------
# Auto-scoring helpers
# -----------------------------

def _strip_code_fences(text: str) -> str:
    s = (text or "").strip()
    s = re.sub(r"^\s*```(?:json)?\s*", "", s, flags=re.I)
    s = re.sub(r"\s*```\s*$", "", s)
    return s.strip()


def _extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    s = _strip_code_fences(text)
    # often first line is the JSON
    first_line = s.splitlines()[0].strip() if s.splitlines() else s
    for cand in [first_line, s]:
        try:
            obj = json.loads(cand)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    # fallback: search for {...} substring
    for m in re.finditer(r"\{.*?\}", s, flags=re.S):
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                return obj
        except Exception:
            continue
    return None


def _norm_hazard_id(x: str) -> str:
    s = (x or "").strip()
    if not s:
        return ""
    # normalize "hazards:Hazard_X" -> "Hazard_X"
    if ":" in s:
        s = s.split(":")[-1]
    return s


def _predict_hazard_id(final_text: str) -> str:
    obj = _extract_first_json_object(final_text or "")
    if obj:
        for k in ("hazard_id", "hazardId", "id", "hazard"):
            v = obj.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    # weak fallback: look for known pattern
    m = re.search(r"\bHazard_[A-Za-z0-9_]+\b", final_text or "")
    return m.group(0) if m else ""


def _is_correct(pred: str, expected: str) -> bool:
    p = _norm_hazard_id(pred)
    e = _norm_hazard_id(expected)
    if not p or not e:
        return False
    return p == e


def _write_wide_report_csv(
    out_root: Path,
    methods: List[str],
    models: List[str],
    testcases: List[TestCase],
    final_matrix: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]],
) -> Path:
    report_path = out_root / "report_final_answers_wide.csv"
    fields = ["testcase_id", "testcase_name", "expected_hazard_id", "model"]
    for m in methods:
        fields += [f"{m}__ok", f"{m}__folder", f"{m}__predicted", f"{m}__correct", f"{m}__final"]

    with report_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()

        for model in models:
            for tc in testcases:
                row: Dict[str, Any] = {
                    "testcase_id": tc.id,
                    "testcase_name": tc.name,
                    "expected_hazard_id": tc.expected_hazard_id,
                    "model": model,
                }
                key = (model, tc.id)
                per_method = final_matrix.get(key, {})
                for mth in methods:
                    rec = per_method.get(mth, {}) or {}
                    row[f"{mth}__ok"] = rec.get("ok", "")
                    row[f"{mth}__folder"] = rec.get("folder", "")
                    row[f"{mth}__predicted"] = rec.get("predicted", "")
                    row[f"{mth}__correct"] = rec.get("correct", "")
                    row[f"{mth}__final"] = _clean_for_csv(rec.get("final", ""))
                w.writerow(row)

    return report_path


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_url", default=os.environ.get("SRCOT_BASE_URL", "http://localhost:1234/v1"))
    ap.add_argument("--api_key", default=os.environ.get("SRCOT_API_KEY", "lm-studio"))

    ap.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated model list.")
    ap.add_argument("--methods", default="simple_rag,llm_only", help="Comma-separated: simple_rag,llm_only")

    ap.add_argument("--simple_rag_script", default="simple-rag.py", help="Path to simple-rag.py")
    ap.add_argument("--llm_only_script", default="llm.py", help="Path to llm.py")

    ap.add_argument("--testcases", required=True, help="Path to testcases-auto.json (must contain expected_hazard_id).")
    ap.add_argument("--select", default="", help="Optional comma-separated testcase IDs to run (e.g., AT01,AT02).")

    ap.add_argument("--memory_dir", default=".", help="Folder containing memory snapshots.")
    ap.add_argument("--knowledge", default="hazard_cards_v5.json")
    ap.add_argument("--experiences", default="experiences.json")
    ap.add_argument("--environment", default="environment.json")

    ap.add_argument("--ops_state_dir", required=True, help="Folder containing ops_state-<stamp>.json/.txt snapshots.")
    ap.add_argument("--out_dir", default="scenario_runs_compare", help="Output root folder.")

    ap.add_argument("--max_tokens", type=int, default=131072)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--per_doc_chars", type=int, default=1200)

    ap.add_argument("--top_k", default="Knowledge=250,Memory=250,Experiences=0,Environment=0,OpsState=0")
    ap.add_argument("--recent_k", default="Memory=250")

    args = ap.parse_args()

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

    models = [m.strip() for m in str(args.models).split(",") if m.strip()] or list(DEFAULT_MODELS)

    testcases = _load_testcases_file(Path(args.testcases))
    if args.select:
        wanted = {x.strip() for x in str(args.select).split(",") if x.strip()}
        testcases = [tc for tc in testcases if tc.id in wanted]
        if not testcases:
            raise ValueError("--select filter removed all testcases (no matching IDs).")

    # cache normalized ops corpus by filepath
    ops_state_cache: Dict[str, Optional[Dict[str, Any]]] = {}

    # outputs
    summary_jsonl = out_root / "summary.jsonl"
    summary_csv = out_root / "summary.csv"
    auto_scores_csv = out_root / "auto_scores.csv"
    auto_scores_by_method_csv = out_root / "auto_scores_by_method.csv"

    csv_fields = [
        "timestamp_utc",
        "method",
        "model",
        "testcase_id",
        "testcase_name",
        "expected_hazard_id",
        "predicted_hazard_id",
        "correct",
        "memory_file",
        "ops_state_file",
        "ops_state_missing",
        "ok",
        "elapsed_sec",
        "error",
        "out_dir",
    ]

    # final matrix for wide report
    final_matrix: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]] = {}

    # per-run score rows
    score_rows: List[Dict[str, Any]] = []

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
                        "expected_hazard_id": tc.expected_hazard_id,
                        "predicted_hazard_id": "",
                        "correct": False,
                        "memory_file": str(tc_mem),
                        "ops_state_file": "",
                        "ops_state_missing": False,
                        "ok": False,
                        "elapsed_sec": None,
                        "error": None,
                        "out_dir": str(run_folder),
                    }

                    # init wide report record
                    final_matrix.setdefault((model, tc.id), {}).setdefault(method, {})
                    final_matrix[(model, tc.id)][method] = {"ok": False, "folder": str(run_folder), "final": "", "predicted": "", "correct": False}

                    if not tc_mem.exists():
                        record["error"] = f"memory file not found: {tc_mem}"
                        with summary_jsonl.open("a", encoding="utf-8") as fj:
                            fj.write(json.dumps(record, ensure_ascii=False) + "\n")
                        writer.writerow(record)
                        fcsv.flush()
                        score_rows.append(record.copy())
                        continue

                    question = (tc.focus_prefix or "") + (tc.question or "").strip()

                    # ops_state resolution (mostly unused in hazard task; kept for compatibility)
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
                            cmd = ["python3", str(simple_rag_script), "--input", str(req_path), "--out", str(tmp_out), "--out_md", str(tmp_md)]
                            p = subprocess.run(cmd, capture_output=True, text=True)
                            if p.returncode != 0:
                                raise RuntimeError(f"simple-rag.py failed: {p.stderr.strip() or p.stdout.strip()}")
                            result = json.loads(tmp_out.read_text(encoding="utf-8"))
                            result.setdefault("meta", {})
                            result["meta"].update({"method": "simple_rag", "model": model, "base_url": base_url, "question": question})

                        else:  # llm_only
                            tmp_out = run_folder / "llm_only_result.json"
                            tmp_md = run_folder / "llm_only_report.md"
                            cmd = ["python3", str(llm_only_script), "--input", str(req_path), "--out", str(tmp_out), "--out_md", str(tmp_md)]
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

                        final_text = str(result.get("final", "") or "")
                        pred = _predict_hazard_id(final_text)
                        corr = _is_correct(pred, tc.expected_hazard_id)

                        record["predicted_hazard_id"] = pred
                        record["correct"] = bool(corr)

                        final_matrix[(model, tc.id)][method] = {
                            "ok": True,
                            "folder": str(run_folder),
                            "final": _clean_for_csv(final_text),
                            "predicted": pred,
                            "correct": bool(corr),
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
                            "predicted": "",
                            "correct": False,
                        }

                    with summary_jsonl.open("a", encoding="utf-8") as fj:
                        fj.write(json.dumps(record, ensure_ascii=False) + "\n")
                    writer.writerow(record)
                    fcsv.flush()
                    score_rows.append(record.copy())

    # auto_scores.csv (per testcase run)
    with auto_scores_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=csv_fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in score_rows:
            w.writerow(r)

    # aggregate accuracy per method+model
    agg: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for r in score_rows:
        key = (r.get("method",""), r.get("model",""))
        a = agg.setdefault(key, {"method": r.get("method",""), "model": r.get("model",""), "n": 0, "n_ok": 0, "n_correct": 0})
        a["n"] += 1
        if r.get("ok"):
            a["n_ok"] += 1
        if r.get("correct"):
            a["n_correct"] += 1

    with auto_scores_by_method_csv.open("w", encoding="utf-8", newline="") as f:
        fields = ["method", "model", "n", "n_ok", "n_correct", "accuracy_over_all", "accuracy_over_ok"]
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for (mth, mdl), a in sorted(agg.items()):
            n = int(a["n"])
            n_ok = int(a["n_ok"])
            n_corr = int(a["n_correct"])
            row = dict(a)
            row["accuracy_over_all"] = (n_corr / n) if n else 0.0
            row["accuracy_over_ok"] = (n_corr / n_ok) if n_ok else 0.0
            w.writerow(row)

    report_path = _write_wide_report_csv(out_root, methods, models, testcases, final_matrix)

    print(f"Done. Results in: {out_root}")
    print(f"- {summary_csv}")
    print(f"- {auto_scores_csv}")
    print(f"- {auto_scores_by_method_csv}")
    print(f"- {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
