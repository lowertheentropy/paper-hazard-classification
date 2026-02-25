#!/usr/bin/env node
"use strict";

const express = require("express");
const fs = require("fs");
const fsp = fs.promises;
const path = require("path");
const { marked } = require("marked");
const sanitizeHtml = require("sanitize-html");

const app = express();
const PORT = process.env.PORT || 3000;

const ROOT = __dirname;

// Read-only on Vercel at runtime: keep markdown here
const DATA_DIR = path.join(ROOT, "data");
const PUBLIC_DIR = path.join(ROOT, "public");

// Writable on Vercel: use /tmp for evaluations + summary
const TMP_ROOT = process.env.TMPDIR || "/tmp";
const WRITE_DIR = path.join(TMP_ROOT, "odsc-eval");

const EVAL_CSV = path.join(WRITE_DIR, "evaluations.csv");
const SUMMARY_CSV = path.join(WRITE_DIR, "summary.csv");

function ensureDir(p) {
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
}
ensureDir(WRITE_DIR);

app.use(express.json({ limit: "1mb" }));
app.use(express.static(PUBLIC_DIR));

function csvEscape(v) {
  if (v === null || v === undefined) return "";
  const s = String(v).replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
}

async function listReports() {
  const files = await fsp.readdir(DATA_DIR);
  const mdFiles = files.filter((f) => f.toLowerCase().endsWith(".md")).sort();
  return mdFiles.map((f) => ({
    internal_id: f.replace(/\.md$/i, ""),
    filename: f
  }));
}

async function loadReportMarkdown(internalId) {
  const filePath = path.join(DATA_DIR, `${internalId}.md`);
  if (!filePath.startsWith(DATA_DIR)) throw new Error("Invalid id");
  return await fsp.readFile(filePath, "utf-8");
}

function renderMarkdownToHtml(md) {
  const raw = marked.parse(md || "", { mangle: false, headerIds: true });
  const clean = sanitizeHtml(raw, {
    allowedTags: sanitizeHtml.defaults.allowedTags.concat([
      "img","h1","h2","h3","h4","h5","h6","span"
    ]),
    allowedAttributes: {
      a: ["href", "name", "target", "rel"],
      img: ["src", "alt", "title"],
      "*": ["class", "id"]
    },
    allowedSchemes: ["http", "https", "data", "mailto"],
    transformTags: {
      a: sanitizeHtml.simpleTransform("a", { rel: "noopener noreferrer", target: "_blank" })
    }
  });

  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Report</title>
  <style>
    body { font-family: -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 18px; line-height: 1.45; }
    pre, code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
    pre { padding: 12px; overflow: auto; border: 1px solid #ddd; border-radius: 10px; background: #fafafa; }
    code { background: #fafafa; padding: 2px 6px; border-radius: 6px; }
    h1,h2,h3 { line-height: 1.2; }
    blockquote { border-left: 4px solid #ddd; margin: 12px 0; padding: 6px 12px; color: #444; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
    th { background: #f3f3f3; }
    .cite { color: #666; }
  </style>
</head>
<body>
${clean}
</body>
</html>`;
}

async function ensureEvalCsv() {
  if (fs.existsSync(EVAL_CSV)) return;

  const header = [
    "timestamp_utc",
    "rater_first_name",
    "report_internal_id",
    "odsc_score",
    "dimension_localfit_yes",
    "dimension_minimal_followups_yes",
    "failure_retrieval_miss",
    "failure_overconfident_or_drift",
    "comment"
  ].join(",") + "\n";

  await fsp.writeFile(EVAL_CSV, header, "utf-8");
}

app.get("/api/reports", async (_req, res) => {
  try {
    const reports = await listReports();
    res.json({ reports });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.get("/report/:internalId", async (req, res) => {
  try {
    const internalId = String(req.params.internalId || "").trim();
    const md = await loadReportMarkdown(internalId);
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    res.send(renderMarkdownToHtml(md));
  } catch (_e) {
    res.status(404).send("Report not found");
  }
});

app.post("/api/submit", async (req, res) => {
  try {
    await ensureEvalCsv();

    const body = req.body || {};
    const ts = new Date().toISOString();

    const rater = String(body.rater_first_name || "").trim();
    const reportId = String(body.report_internal_id || "").trim();

    if (!rater) return res.status(400).json({ error: "Missing rater_first_name" });
    if (!reportId) return res.status(400).json({ error: "Missing report_internal_id" });

    const score = Number(body.odsc_score);
    if (!Number.isFinite(score) || score < 0 || score > 3) {
      return res.status(400).json({ error: "odsc_score must be 0..3" });
    }

    const b01 = (x) => (x ? 1 : 0);

    const row = [
      ts,
      rater,
      reportId,
      score,
      b01(body.dimension_localfit_yes),
      b01(body.dimension_minimal_followups_yes),
      b01(body.failure_retrieval_miss),
      b01(body.failure_overconfident_or_drift),
      String(body.comment || "").trim()
    ].map(csvEscape).join(",") + "\n";

    await fsp.appendFile(EVAL_CSV, row, "utf-8");
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.post("/api/generate_summary", async (_req, res) => {
  try {
    if (!fs.existsSync(EVAL_CSV)) {
      return res.status(400).json({ error: "No evaluations.csv yet." });
    }

    const csv = await fsp.readFile(EVAL_CSV, "utf-8");
    const lines = csv.split("\n").filter((l) => l.trim().length > 0);
    if (lines.length <= 1) {
      return res.status(400).json({ error: "No evaluation rows yet." });
    }

    const header = parseCsvLine(lines[0]);
    const idxCol = (name) => header.indexOf(name);

    const iRater = idxCol("rater_first_name");
    const iReport = idxCol("report_internal_id");
    const iScore = idxCol("odsc_score");

    const perReport = new Map();
    const perRater = new Map();
    let totalSum = 0;
    let totalCount = 0;

    for (let i = 1; i < lines.length; i++) {
      const row = parseCsvLine(lines[i]);
      const rater = row[iRater] || "";
      const report = row[iReport] || "";
      const score = Number(row[iScore]);
      if (!Number.isFinite(score)) continue;

      totalSum += score;
      totalCount += 1;

      if (!perReport.has(report)) perReport.set(report, { sum: 0, count: 0 });
      perReport.get(report).sum += score;
      perReport.get(report).count += 1;

      if (!perRater.has(rater)) perRater.set(rater, { sum: 0, count: 0 });
      perRater.get(rater).sum += score;
      perRater.get(rater).count += 1;
    }

    const out = [];
    out.push("section,key,count,avg_odsc");

    for (const [reportId, v] of [...perReport.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
      out.push(["per_report", reportId, v.count, (v.sum / v.count).toFixed(3)].join(","));
    }

    for (const [r, v] of [...perRater.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
      out.push(["per_rater", r, v.count, (v.sum / v.count).toFixed(3)].join(","));
    }

    if (totalCount > 0) out.push(["overall", "ALL", totalCount, (totalSum / totalCount).toFixed(3)].join(","));

    await fsp.writeFile(SUMMARY_CSV, out.join("\n") + "\n", "utf-8");
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.get("/api/evaluations.csv", async (_req, res) => {
  try {
    if (!fs.existsSync(EVAL_CSV)) return res.status(404).send("evaluations.csv not created yet");
    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.send(await fsp.readFile(EVAL_CSV, "utf-8"));
  } catch (e) {
    res.status(500).send(String(e));
  }
});

app.get("/api/summary.csv", async (_req, res) => {
  try {
    if (!fs.existsSync(SUMMARY_CSV)) return res.status(404).send("summary.csv not generated yet");
    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.send(await fsp.readFile(SUMMARY_CSV, "utf-8"));
  } catch (e) {
    res.status(500).send(String(e));
  }
});

// NEW: storage status for UI hint
app.get("/api/storage_status", async (_req, res) => {
  try {
    const statOrNull = async (p) => {
      try {
        const st = await fsp.stat(p);
        return { exists: true, bytes: st.size };
      } catch (_e) {
        return { exists: false, bytes: 0 };
      }
    };
    res.json({
      write_dir: WRITE_DIR,
      evaluations: await statOrNull(EVAL_CSV),
      summary: await statOrNull(SUMMARY_CSV),
    });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

// NEW: reset storage (delete CSVs in /tmp and recreate header)
app.post("/api/reset_storage", async (_req, res) => {
  try {
    // delete files if present
    if (fs.existsSync(EVAL_CSV)) await fsp.unlink(EVAL_CSV);
    if (fs.existsSync(SUMMARY_CSV)) await fsp.unlink(SUMMARY_CSV);
    await ensureEvalCsv();
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

function parseCsvLine(line) {
  const out = [];
  let cur = "";
  let inQ = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQ) {
      if (ch === '"') {
        if (i + 1 < line.length && line[i + 1] === '"') {
          cur += '"';
          i++;
        } else {
          inQ = false;
        }
      } else {
        cur += ch;
      }
    } else {
      if (ch === ",") {
        out.push(cur);
        cur = "";
      } else if (ch === '"') {
        inQ = true;
      } else {
        cur += ch;
      }
    }
  }
  out.push(cur);
  return out;
}

app.listen(PORT, () => {
  console.log(`ODSC eval running at http://localhost:${PORT}`);
  console.log(`Reports (read-only): ${DATA_DIR}`);
  console.log(`Writes (tmp): ${WRITE_DIR}`);
});