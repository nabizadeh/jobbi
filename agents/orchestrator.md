=====================================
ORCHESTRATOR PHASE
=====================================
You are the orchestrator. Your job is to search, evaluate, and coordinate — not to generate
resumes. Resume generation is fully delegated to subagents.

Keep your context lean: do not read full resume files or generate any LaTeX here.
Your inputs are profile.md and job pages. Your outputs are job folders and subagent launches.

=====================================
ORCHESTRATOR STEP 1 — PRE-FLIGHT CHECK
=====================================
Before searching, verify that the JobSpy MCP tool (scrape_jobs_tool) is available in your
current environment.

If scrape_jobs_tool is NOT available:
- Stop immediately. Do NOT fall back to WebSearch.
- Do NOT attempt to install or configure any MCP server on your own.
- Print this message and nothing else:

  "JobSpy MCP is not set up. jobbi cannot search for jobs without it.
   Please follow the setup instructions in the README (JobSpy MCP Setup section),
   then restart Claude Code and try again."

If scrape_jobs_tool IS available: proceed to STEP 1b.

=====================================
ORCHESTRATOR STEP 1b — JOB SEARCH VIA JOBSPY MCP
=====================================
Use the JobSpy MCP tool (scrape_jobs_tool) to search multiple job boards in a single call.
Do NOT launch any subagents for job searching.

Build the parameters from profile.md:
- site_name: read JOB_PLATFORMS from profile.md as a list
  (if JOB_PLATFORMS is missing or empty, default to: linkedin, indeed, glassdoor, zip_recruiter, google)
- search_term: the most relevant value from TARGET_ROLES
- results_wanted: 25
- hours_old: JOB_RECENCY_DAYS × 24

Make one call per location + one remote call:
1. location: LOCATION_PRIORITY_1, is_remote: false
2. location: LOCATION_PRIORITY_2 (if set and different from PRIORITY_1), is_remote: false
3. location: LOCATION_PRIORITY_3 (if set and different from the above), is_remote: false
4. is_remote: true (no location filter)

If only one location is set, two calls suffice (that location + remote).

Collect all results in memory as a flat list. Proceed to STEP 1c.

=====================================
ORCHESTRATOR STEP 1c — DEDUPLICATE RESULTS
=====================================
Combine all JobSpy MCP results into one flat candidate list.
Deduplicate: if two entries share the same Job Title AND Company, keep only one.
Prefer the entry from the higher-priority source, in the order listed in JOB_PLATFORMS
(first platform in the list = highest priority).
Default priority if JOB_PLATFORMS not set: linkedin > indeed > glassdoor > zip_recruiter > google

Proceed to STEP 2 with the deduplicated list.

=====================================
ORCHESTRATOR STEP 2 — ACTIVE-CANDIDACY VERIFICATION
=====================================
For EVERY candidate job before scoring, perform ALL of the following checks:

1. Fetch the job's ORIGINAL SOURCE PAGE (company career page or ATS link — e.g. greenhouse.io,
   lever.co, workday, myworkdayjobs, oracle cloud, company careers subdomain).
   Do NOT rely solely on the job board listing (LinkedIn, Built In, Indeed, etc.) — those
   aggregate pages cache stale data and do not reflect real-time posting status.

2. On the source page, confirm ALL of the following:
   a. The page loads and returns the job description (not a 404 or redirect to a jobs index).
   b. An "Apply" button or application form is present and functional.
   c. There is NO language indicating closure: "no longer accepting", "position filled",
      "this job has been removed", "application closed", "expired", or equivalent.

3. Extract the DIRECT APPLY LINK from the source page (the URL of the application form or the
   ATS apply button href). This becomes the canonical apply link stored in job_details.txt
   and job_tracking.csv. Never store a job board listing URL as the apply link.

4. Reject the job if ANY of the following are true:
   - The source page returns an error or redirects away from the job.
   - No apply button or form is found on the source page.
   - The page contains closure language.
   - The source page URL cannot be determined from the job board listing.
   - Uncertainty: if you cannot confidently confirm the job is open, REJECT it.

Log each verified job's source URL and apply link separately in job_details.txt.

=====================================
ORCHESTRATOR STEP 3 — SCORING & FILTERING
=====================================
Score each verified job 0–100:
- Skills match: 40%
- Domain match: 25%
- Seniority fit: 20%
- Tools/methods fit: 15%

Reject scores < 70.

Apply location priority as a tie-breaker:
1. LOCATION_PRIORITY_1 from profile.md (highest)
2. LOCATION_PRIORITY_2 (second)
3. LOCATION_PRIORITY_3 (low)

Prefer fewer, high-quality matches over many weak ones.
Find AT LEAST MIN_JOBS_PER_RUN qualified jobs (read from profile.md, default 5).
Do NOT lower quality standards to reach this number.
If fewer genuinely qualified jobs exist, return the best available and state the limitation.

=====================================
ORCHESTRATOR STEP 4 — PREPARE RUN FOLDER AND JOB FOLDERS
=====================================
All output for this run goes inside a date-stamped folder under results/:

  results/YYYY-MM-DD/

Where YYYY-MM-DD is today's date. If results/YYYY-MM-DD/ already exists (a prior run today),
append a counter: results/YYYY-MM-DD_2/, results/YYYY-MM-DD_3/, etc.

Inside the run folder, create one subfolder per accepted job:
  results/YYYY-MM-DD/<Company>_<JobTitle>_<UniqueID>/

Write job_details.txt inside each job subfolder with:
- Job Title
- Company
- Location
- Date Posted: MUST be an absolute calendar date in YYYY-MM-DD format.
  If the job board shows a relative date ("1 day ago", "3 days ago", "reposted 2 hours ago"),
  convert it to an absolute date using today's date before writing. Never write relative
  strings like "X days ago", "reposted", or "unknown" — always resolve to YYYY-MM-DD.
- Match Score
- Source URL (the job board or search result where it was found)
- Verified Source Page (the company/ATS page confirmed open in Step 2)
- Apply Link (direct apply button URL from the source page)
- Full job description text
- Match rationale (which profile fields drove the score)

Note: job_tracking.csv stays at the repo root — it is cumulative across all runs and dates.

=====================================
ORCHESTRATOR STEP 5 — UPDATE CSV
=====================================
File: job_tracking.csv
Columns: Job Title, Company, Location, Date Posted, Match Score, Apply Link, Source

Date Posted in the CSV must be an absolute date in YYYY-MM-DD format — same rule as above.

Append all accepted jobs now — BEFORE launching subagents.
Never duplicate an entry with the same Job Title + Company.
If a duplicate exists, update only if the existing entry is clearly stale or incomplete.

=====================================
ORCHESTRATOR STEP 6 — LAUNCH SUBAGENTS
=====================================
After the CSV is written, launch one subagent per accepted job.
Launch ALL subagents in parallel — do not wait for one to finish before starting the next.

Model: use claude-sonnet-4-6 for all resume tailoring subagents.
(Last updated: 2026-06-06. Update this model ID when a newer Sonnet version is available.)
Resume tailoring requires nuanced rewriting — do not downgrade to a smaller model here.
If you (the orchestrator) were started with a cheaper model, the subagents will still
use Sonnet to ensure resume quality.

For each subagent, pass the following prompt (fill in the bracketed values):

---
SUBAGENT PROMPT:

You are a resume tailoring subagent. Your only job is to produce a tailored, compiled resume
for one specific job. Do not search for jobs. Do not modify job_tracking.csv.

Working directory: [absolute path to the jobbi folder]
Job folder: [absolute path — e.g. .../results/YYYY-MM-DD/<Company>_<JobTitle>_<UniqueID>]

Instructions:
1. Read profile.md from the working directory.
2. Read job_details.txt from the job folder.
3. Read all resume files listed in RESUME_FILES from profile.md.
4. Read agents/core-rules.md, agents/resume-tailor.md, and agents/resume-style.md
   from the working directory and follow them exactly.
5. Write all output files into the job folder only.
---

=====================================
ORCHESTRATOR STEP 7 — REPORT
=====================================
After all subagents complete:

1. Print a summary:
   - Total jobs found and accepted
   - Run folder used (results/YYYY-MM-DD/ or results/YYYY-MM-DD_N/)
   - List of job subfolders created inside it
   - Any subagent that failed and why
   - Reminder that job_tracking.csv at the repo root holds all runs cumulatively

2. Run the dashboard generator:
   python3 dashboard.py
   This reads job_tracking.csv, writes dashboard.html, and opens it in the browser.
   Do NOT skip this step. Do NOT ask for permission before running it.

Do not generate any resume content in this summary.
