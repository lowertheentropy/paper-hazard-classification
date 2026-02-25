"use strict";

let reports = [];
let order = [];
let idx = 0;
let rater = "";

const el = (id) => document.getElementById(id);

function setStatus(msg) {
  el("status").textContent = msg || "";
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function getSelectedScore() {
  const radios = document.querySelectorAll('input[name="odsc"]');
  for (const r of radios) if (r.checked) return Number(r.value);
  return null;
}

function clearForm() {
  const radios = document.querySelectorAll('input[name="odsc"]');
  radios.forEach((r) => (r.checked = false));

  el("dimLocalfit").checked = false;
  el("dimMinimal").checked = false;

  el("failRetrieval").checked = false;
  el("failOverOrDrift").checked = false;

  el("comment").value = "";
}

function currentReport() {
  if (idx < 0 || idx >= order.length) return null;
  return reports[order[idx]];
}

function loadCurrent() {
  const rep = currentReport();
  if (!rep) {
    el("reportFrame").srcdoc = "<h2>Done</h2><p>No more reports.</p>";
    el("progress").textContent = `Completed ${order.length}/${order.length}`;
    setStatus("Done.");
    return;
  }

  el("reportFrame").src = `/report/${encodeURIComponent(rep.internal_id)}`;
  el("progress").textContent = `Report ${idx + 1} / ${order.length}`;
  setStatus("Review report and rate ODSC (0–3).");

  clearForm();
}

async function fetchReports() {
  const r = await fetch("/api/reports");
  const j = await r.json();
  reports = j.reports || [];
  if (!reports.length) {
    setStatus("No .md files found in data/");
  } else {
    setStatus(`${reports.length} reports found.`);
  }
}

async function submitAndNext() {
  const rep = currentReport();
  if (!rep) return;

  const score = getSelectedScore();
  if (score === null) {
    alert("Please select an ODSC score (0–3).");
    return;
  }

  const payload = {
    rater_first_name: rater,
    report_internal_id: rep.internal_id,
    odsc_score: score,

    // success dimensions (tracked)
    dimension_localfit_yes: el("dimLocalfit").checked,
    dimension_minimal_followups_yes: el("dimMinimal").checked,

    // failure modes (tracked)
    failure_retrieval_miss: el("failRetrieval").checked,
    failure_overconfident_or_drift: el("failOverOrDrift").checked,

    comment: el("comment").value || ""
  };

  const res = await fetch("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const txt = await res.text();
    alert("Submit failed: " + txt);
    return;
  }

  idx += 1;
  loadCurrent();
}

async function generateSummary() {
  const res = await fetch("/api/generate_summary", { method: "POST" });
  const j = await res.json().catch(() => ({}));
  if (!res.ok) {
    alert("Could not generate summary: " + (j.error || res.statusText));
    return false;
  }
  alert("summary.csv generated (stored in /tmp on the server; download it to keep it).");
  return true;
}

async function downloadFile(url, filename) {
  const res = await fetch(url);
  if (!res.ok) {
    const txt = await res.text();
    alert("Download failed: " + txt);
    return;
  }
  const blob = await res.blob();
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(a.href);
}

async function refreshStorageHint() {
  const hint = document.getElementById("storageHint");
  if (!hint) return;

  try {
    const res = await fetch("/api/storage_status");
    if (!res.ok) return;
    const j = await res.json();

    const ev = j.evaluations || {};
    const su = j.summary || {};
    hint.innerHTML =
      `Hinweis: CSVs liegen in <code>/tmp</code> (ephemeral). ` +
      `evaluations.csv: ${ev.exists ? (ev.bytes + " bytes") : "nicht vorhanden"}, ` +
      `summary.csv: ${su.exists ? (su.bytes + " bytes") : "nicht vorhanden"}. ` +
      `Bitte herunterladen, um sie dauerhaft zu speichern.`;
  } catch (_e) {}
}

(async function main() {
  await fetchReports();

  el("startBtn").addEventListener("click", async () => {
    const name = (el("firstName").value || "").trim();
    if (!name) {
      alert("Please enter your first name.");
      return;
    }
    if (!reports.length) {
      alert("No reports found in data/. Add .md files and reload.");
      return;
    }

    rater = name;
    order = shuffle([...Array(reports.length).keys()]);
    idx = 0;

    el("formCard").classList.remove("hidden");
    setStatus(`Rater: ${rater}. Randomized ${reports.length} reports.`);
    loadCurrent();
    await refreshStorageHint();
  });

  el("nextBtn").addEventListener("click", submitAndNext);

  el("genSummaryBtn").addEventListener("click", async () => {
    const ok = await generateSummary();
    if (ok) await refreshStorageHint();
  });

  const downloadEvalBtn = document.getElementById("downloadEvalBtn");
  if (downloadEvalBtn) {
    downloadEvalBtn.addEventListener("click", () => {
      const stamp = new Date().toISOString().replace(/[:.]/g, "-");
      downloadFile("/api/evaluations.csv", `evaluations_${stamp}.csv`);
    });
  }

  const downloadSummaryBtn = document.getElementById("downloadSummaryBtn");
  if (downloadSummaryBtn) {
    downloadSummaryBtn.addEventListener("click", async () => {
      await generateSummary();
      const stamp = new Date().toISOString().replace(/[:.]/g, "-");
      downloadFile("/api/summary.csv", `summary_${stamp}.csv`);
      await refreshStorageHint();
    });
  }

  const resetBtn = document.getElementById("resetBtn");
  if (resetBtn) {
    resetBtn.addEventListener("click", async () => {
      if (!confirm("Wirklich evaluations.csv und summary.csv löschen (Reset)?")) return;
      const res = await fetch("/api/reset_storage", { method: "POST" });
      const j = await res.json().catch(() => ({}));
      if (!res.ok) {
        alert("Reset failed: " + (j.error || res.statusText));
        return;
      }
      alert("Reset ok. evaluations.csv header recreated.");
      await refreshStorageHint();
    });
  }

  await refreshStorageHint();
})();