#!/usr/bin/env python3
"""jobbi — interactive job dashboard generator.
Reads job_tracking.csv, writes dashboard.html, opens it in the browser.
Status (applied / interviewing / accepted / rejected) is stored in localStorage
and survives HTML regeneration as long as the browser data is not cleared.
"""

import csv
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CSV_PATH = "job_tracking.csv"
OUTPUT_PATH = "dashboard.html"

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>jobbi — job dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:          #0f1117;
  --surface:     #1a1d27;
  --surface2:    #22263a;
  --border:      #2d3147;
  --text:        #e2e8f0;
  --subtext:     #94a3b8;
  --accent:      #6366f1;
  --accent-h:    #818cf8;
  --s-none:      #475569;
  --s-applied:   #3b82f6;
  --s-interview: #f59e0b;
  --s-accepted:  #22c55e;
  --s-rejected:  #ef4444;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 14px;
  line-height: 1.5;
  min-height: 100vh;
}

/* ── Header ── */
.header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}
.logo      { font-size: 20px; font-weight: 700; color: var(--accent); letter-spacing: -0.5px; }
.generated { color: var(--subtext); font-size: 12px; }

/* ── Stats bar ── */
.stats {
  display: flex;
  gap: 10px;
  padding: 16px 24px 12px;
  flex-wrap: wrap;
}
.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 9px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 74px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  user-select: none;
}
.stat:hover                         { border-color: var(--accent); }
.stat.active                        { border-color: var(--accent); background: var(--surface2); }
.stat-number                        { font-size: 20px; font-weight: 700; line-height: 1; }
.stat-label                         { font-size: 10px; color: var(--subtext); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px; }
.stat[data-f="all"]          .stat-number { color: var(--text); }
.stat[data-f="none"]         .stat-number { color: var(--s-none); }
.stat[data-f="applied"]      .stat-number { color: var(--s-applied); }
.stat[data-f="interviewing"] .stat-number { color: var(--s-interview); }
.stat[data-f="accepted"]     .stat-number { color: var(--s-accepted); }
.stat[data-f="rejected"]     .stat-number { color: var(--s-rejected); }

/* ── Toolbar ── */
.toolbar {
  padding: 0 24px 14px;
  display: flex;
  gap: 10px;
  align-items: center;
}
.search-input {
  flex: 1;
  max-width: 380px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  padding: 7px 12px;
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s;
}
.search-input:focus       { border-color: var(--accent); }
.search-input::placeholder { color: var(--subtext); }
.row-count { color: var(--subtext); font-size: 12px; margin-left: 4px; }

/* ── Table ── */
.table-wrap {
  padding: 0 24px 48px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 780px;
}

thead tr {
  border-bottom: 2px solid var(--border);
}

th {
  padding: 9px 14px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  color: var(--subtext);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  user-select: none;
  background: var(--bg);
}
th.sortable {
  cursor: pointer;
}
th.sortable:hover { color: var(--text); }
th.asc  .arrow::after { content: ' ↑'; color: var(--accent); }
th.desc .arrow::after { content: ' ↓'; color: var(--accent); }
th.asc, th.desc { color: var(--text); }

tbody tr {
  border-bottom: 1px solid var(--border);
  border-left: 3px solid transparent;
  transition: background 0.1s;
}
tbody tr:hover                           { background: var(--surface); }
tbody tr[data-status="applied"]          { border-left-color: var(--s-applied); }
tbody tr[data-status="interviewing"]     { border-left-color: var(--s-interview); }
tbody tr[data-status="accepted"]         { border-left-color: var(--s-accepted); }
tbody tr[data-status="rejected"]         { border-left-color: var(--s-rejected); opacity: 0.45; }

td { padding: 10px 14px; vertical-align: middle; }

.td-company {
  font-size: 13px;
  font-weight: 600;
  color: var(--accent);
  white-space: nowrap;
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.td-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  min-width: 200px;
}
.td-loc, .td-date, .td-source {
  font-size: 12px;
  color: var(--subtext);
  white-space: nowrap;
}
.td-score { text-align: center; white-space: nowrap; }
.score-num { font-weight: 700; font-size: 14px; }

/* ── Status select ── */
.td-status { white-space: nowrap; }
.status-select {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 5px;
  color: var(--subtext);
  padding: 5px 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  outline: none;
  width: 136px;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
}
.status-select[data-s="applied"]      { color: var(--s-applied);   border-color: var(--s-applied);   background: rgba(59,130,246,0.12); }
.status-select[data-s="interviewing"] { color: var(--s-interview);  border-color: var(--s-interview); background: rgba(245,158,11,0.12); }
.status-select[data-s="accepted"]     { color: var(--s-accepted);   border-color: var(--s-accepted);  background: rgba(34,197,94,0.12); }
.status-select[data-s="rejected"]     { color: var(--s-rejected);   border-color: var(--s-rejected);  background: rgba(239,68,68,0.12); }

/* ── Apply button ── */
.td-apply { white-space: nowrap; }
.apply-link {
  display: inline-block;
  padding: 5px 12px;
  background: var(--accent);
  color: #fff;
  border-radius: 5px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.15s;
}
.apply-link:hover   { background: var(--accent-h); }
.no-link {
  display: inline-block;
  padding: 5px 12px;
  background: var(--surface2);
  color: var(--border);
  border-radius: 5px;
  font-size: 12px;
  font-weight: 600;
  cursor: default;
}

.empty-row td {
  text-align: center;
  color: var(--subtext);
  padding: 48px;
  font-size: 14px;
}
</style>
</head>
<body>

<div class="header">
  <span class="logo">jobbi</span>
  <span class="generated">updated __GENERATED_AT__</span>
</div>

<div class="stats" id="stats"></div>

<div class="toolbar">
  <input class="search-input" id="search" type="text" placeholder="Search title, company, location…">
  <span class="row-count" id="row-count"></span>
</div>

<div class="table-wrap">
  <table>
    <thead>
      <tr id="thead-row">
        <th class="sortable" data-col="company">Company<span class="arrow"></span></th>
        <th class="sortable" data-col="title">Job Title<span class="arrow"></span></th>
        <th>Location</th>
        <th class="sortable" data-col="date">Posted<span class="arrow"></span></th>
        <th class="sortable desc" data-col="score" style="text-align:center">Score<span class="arrow"></span></th>
        <th>Status</th>
        <th>Apply</th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>
</div>

<script>
const JOBS = __JOBS_JSON__;

const STATUS_ORDER = ['none','applied','interviewing','accepted','rejected'];
const STATUS_OPTS  = [
  { v:'none',         label:'— Pending' },
  { v:'applied',      label:'✓ Applied' },
  { v:'interviewing', label:'⟳ Interviewing' },
  { v:'accepted',     label:'★ Accepted' },
  { v:'rejected',     label:'✕ Rejected' },
];

function lsKey(j) { return 'jobbi__' + (j['Company']||'') + '__' + (j['Job Title']||''); }
function getStatus(j)    { return localStorage.getItem(lsKey(j)) || 'none'; }
function saveStatus(j,s) { localStorage.setItem(lsKey(j), s); }

function scoreColor(raw) {
  const n = parseInt(raw) || 0;
  if (n >= 90) return '#22c55e';
  if (n >= 80) return '#14b8a6';
  return '#f59e0b';
}

let activeFilter = 'all';
let sortCol = 'score';
let sortDir = 'desc';

/* ── Stats ── */
function counts() {
  const c = { all:JOBS.length, none:0, applied:0, interviewing:0, accepted:0, rejected:0 };
  JOBS.forEach(j => c[getStatus(j)]++);
  return c;
}

function renderStats() {
  const c = counts();
  const defs = [
    { f:'all',          label:'Total' },
    { f:'none',         label:'Pending' },
    { f:'applied',      label:'Applied' },
    { f:'interviewing', label:'Interviewing' },
    { f:'accepted',     label:'Accepted' },
    { f:'rejected',     label:'Rejected' },
  ];
  document.getElementById('stats').innerHTML = defs.map(d =>
    `<div class="stat ${activeFilter===d.f?'active':''}" data-f="${d.f}" onclick="setFilter('${d.f}')">
       <span class="stat-number">${c[d.f]}</span>
       <span class="stat-label">${d.label}</span>
     </div>`
  ).join('');
}

function setFilter(f) { activeFilter = f; render(); }

/* ── Sort headers ── */
document.getElementById('thead-row').addEventListener('click', e => {
  const th = e.target.closest('th.sortable');
  if (!th) return;
  const col = th.dataset.col;
  if (sortCol === col) { sortDir = sortDir === 'asc' ? 'desc' : 'asc'; }
  else { sortCol = col; sortDir = col === 'score' ? 'desc' : 'asc'; }
  render();
});

function updateSortHeaders() {
  document.querySelectorAll('th.sortable').forEach(th => {
    th.classList.remove('asc','desc');
    if (th.dataset.col === sortCol) th.classList.add(sortDir);
  });
}

/* ── Render ── */
function render() {
  const q = document.getElementById('search').value.toLowerCase();

  let jobs = JOBS.filter(j => {
    if (activeFilter !== 'all' && getStatus(j) !== activeFilter) return false;
    if (q) {
      const hay = [(j['Job Title']||''),(j['Company']||''),(j['Location']||'')].join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  jobs = [...jobs].sort((a,b) => {
    let av, bv;
    if (sortCol === 'score')   { av = parseInt(a['Match Score'])||0; bv = parseInt(b['Match Score'])||0; }
    else if (sortCol === 'date')    { av = a['Date Posted']||''; bv = b['Date Posted']||''; }
    else if (sortCol === 'company') { av = (a['Company']||'').toLowerCase(); bv = (b['Company']||'').toLowerCase(); }
    else if (sortCol === 'title')   { av = (a['Job Title']||'').toLowerCase(); bv = (b['Job Title']||'').toLowerCase(); }
    if (av < bv) return sortDir === 'asc' ? -1 : 1;
    if (av > bv) return sortDir === 'asc' ?  1 : -1;
    return 0;
  });

  renderStats();
  updateSortHeaders();
  document.getElementById('row-count').textContent = jobs.length + ' of ' + JOBS.length + ' jobs';

  const tbody = document.getElementById('tbody');
  if (!jobs.length) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="7">No jobs match this filter.</td></tr>';
    return;
  }

  tbody.innerHTML = jobs.map(j => {
    const idx    = JOBS.indexOf(j);
    const status = getStatus(j);
    const score  = j['Match Score'] || '—';
    const link   = (j['Apply Link']||'').trim();

    const opts = STATUS_OPTS.map(o =>
      `<option value="${o.v}" ${status===o.v?'selected':''}>${o.label}</option>`
    ).join('');

    const applyEl = link
      ? `<a class="apply-link" href="${link}" target="_blank" rel="noopener noreferrer">Apply →</a>`
      : `<span class="no-link">—</span>`;

    return `<tr data-status="${status}" id="r${idx}">
  <td class="td-company" title="${j['Company']||''}">${j['Company']||''}</td>
  <td class="td-title">${j['Job Title']||''}</td>
  <td class="td-loc">${j['Location']||'—'}</td>
  <td class="td-date">${j['Date Posted']||'—'}</td>
  <td class="td-score"><span class="score-num" style="color:${scoreColor(j['Match Score'])}">${score}</span></td>
  <td class="td-status">
    <select class="status-select" data-s="${status}" onchange="changeStatus(${idx}, this)">
      ${opts}
    </select>
  </td>
  <td class="td-apply">${applyEl}</td>
</tr>`;
  }).join('');
}

function changeStatus(idx, sel) {
  const j = JOBS[idx];
  const s = sel.value;
  saveStatus(j, s);
  sel.dataset.s = s;
  const row = document.getElementById('r'+idx);
  if (row) row.dataset.status = s;
  renderStats();
  if (activeFilter !== 'all') render();
}

document.getElementById('search').addEventListener('input', render);
render();
</script>
</body>
</html>"""


def read_jobs():
    p = Path(CSV_PATH)
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def build_html(jobs):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    jobs_json = json.dumps(jobs, ensure_ascii=False, indent=2)
    return (
        HTML
        .replace("__JOBS_JSON__", jobs_json)
        .replace("__GENERATED_AT__", generated_at)
    )


def open_browser(path):
    abs_path = Path(path).resolve()
    if sys.platform == "darwin":
        subprocess.run(["open", str(abs_path)])
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", str(abs_path)])
    elif sys.platform == "win32":
        os.startfile(str(abs_path))


def main():
    jobs = read_jobs()
    html = build_html(jobs)
    Path(OUTPUT_PATH).write_text(html, encoding="utf-8")
    n = len(jobs)
    print(f"Dashboard → {OUTPUT_PATH}  ({n} job{'s' if n != 1 else ''})")
    open_browser(OUTPUT_PATH)


if __name__ == "__main__":
    main()
