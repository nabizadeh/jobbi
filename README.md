# jobbi

<p align="center">
  <img src="Jobbi_Logo.png" alt="jobbi logo" width="600"/>
</p>

An autonomous job search and resume tailoring agent for Claude Code.

Drop your resume in a folder, run Claude Code, and jobbi finds matching jobs, scores them, and generates a tailored PDF resume for each one — ready to submit.

---

## What it does

1. **First run:** reads your resume file(s), builds a personal profile, asks you to fill any gaps
2. **Every run after:** skips setup and goes straight to job hunting
3. Searches your configured job boards (LinkedIn, Indeed, and others) and verifies each posting is still open
4. Scores each job against your profile (skills, domain, seniority, tools)
5. Rejects weak matches; accepts only scores ≥ 70
6. For every accepted job: generates a tailored LaTeX resume, compiles it to PDF, and logs it to a tracking CSV

---

## Requirements

- [Claude Code](https://claude.ai/code) (CLI)
- A LaTeX distribution: [TeX Live](https://tug.org/texlive/), [MacTeX](https://tug.org/mactex/), or [Tectonic](https://tectonic-typesetting.github.io/)
- Your resume (PDF, Word, LaTeX, Markdown, or plain text)
- JobSpy MCP server (see setup below)

---

## JobSpy MCP Setup

jobbi uses the [JobSpy MCP server](https://github.com/chinpeerapat/jobspy-mcp-server) to search job boards. Run the setup script once before your first run:

```bash
bash setup.sh
```

The script will:
- Install the JobSpy MCP server into `~/tools/jobspy-mcp-server`
- Configure Claude Code automatically (merges into your existing `~/.claude/settings.json`)
- Tell you exactly what it's doing at each step

**Requirements:** git and [uv](https://docs.astral.sh/uv/getting-started/installation/) (uv will be auto-installed if missing). macOS and Linux only — Windows users run this inside WSL.

After the script finishes, **restart Claude Code** for the MCP server to take effect.

> **To verify:** after restarting, ask Claude: `List the available MCP tools.` — you should see `scrape_jobs_tool`. If it's missing, jobbi will stop and tell you rather than attempting to install anything on its own.

> **To uninstall:** delete `~/tools/jobspy-mcp-server` and remove the `"jobspy"` entry from `~/.claude/settings.json`.

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/nabizadeh/jobbi.git
cd jobbi

# 2. Install JobSpy MCP (one-time setup — see JobSpy MCP Setup section above)
bash setup.sh
# → restart Claude Code after this step

# 3. Drop your resume into the resumes/ folder
cp /path/to/YourResume.pdf resumes/   # or .txt, .md, .docx, .tex

# 4. Run Claude Code
claude

# 5. Paste this prompt to kick things off:
# "Search for jobs — read my resume, set up my profile, and find matching jobs."
```

Once you send that prompt, jobbi will:
- Detect your resume file(s)
- Extract your profile automatically
- Ask you only for anything it couldn't find
- Save a `profile.md` so setup never runs again
- Start searching for jobs

---

## What to type

Once Claude Code is open in the jobbi directory, paste one of these prompts:

**First run** — profile setup + job search:
```
Search for jobs — read my resume, set up my profile, and find matching jobs.
```

**Later runs** — skip setup, go straight to job search:
```
Find new job matches and generate tailored resumes.
```

**Revise a resume** — after jobs have been found:
```
Update the [Company] resume — [describe the change, e.g. "shorten the summary" or "remove the third bullet in the most recent role"].
```

**Refresh the dashboard** — without running a new search:
```
Regenerate the dashboard from job_tracking.csv.
```

---

## File structure

```
jobbi/
├── AGENTS.md                          # Entry point — routes to agents/ modules
├── agents/                            # Modular agent instructions
│   ├── core-rules.md                  # Hard rules for all agents
│   ├── setup.md                       # First-run profile setup
│   ├── orchestrator.md                # Job search and subagent coordination
│   ├── resume-tailor.md               # Resume tailoring logic
│   ├── resume-style.md                # LaTeX formatting — edit to customize for your market
│   └── revision.md                    # Post-generation resume revision
├── setup.sh                           # One-command JobSpy MCP installer
├── .claude/settings.json              # Pre-approved commands (no permission prompts)
├── profile.md                         # Auto-generated on first run (gitignored)
├── job_tracking.csv                   # Cumulative job log across all runs (gitignored)
│
├── resumes/                           # Drop your resume(s) here
│   ├── DROP_YOUR_RESUME_HERE.txt      # Placeholder — do not delete
│   └── YourResume.pdf                 # Your resume — any supported format (gitignored)
│
└── results/                           # All search output (gitignored)
    └── 2026-05-09/                    # One folder per day (or _2, _3 for multiple runs)
        └── Company_Role_001/          # One subfolder per accepted job
            ├── job_details.txt        # Full job info and match rationale
            ├── YourName_Resume.tex    # Tailored LaTeX source
            ├── YourName_Resume.pdf    # Compiled, submission-ready PDF
            ├── resume_changes.txt     # What changed and why
            └── cover_letter.md        # Cover letter draft (if COVER_LETTER: yes)
```

---

## Permissions

jobbi ships with a `.claude/settings.json` that pre-approves the specific commands it needs — LaTeX compilers (`pdflatex`, `tectonic`), Python, and safe file operations (`ls`, `find`, `mkdir`, `cp`, `grep`, etc.).

This means Claude Code will run those commands without interrupting you for confirmation. Nothing destructive (`rm`, `curl` to external APIs, etc.) is pre-approved. You can inspect or tighten the list at any time by editing `.claude/settings.json`.

---

## Supported resume formats

| Format | Notes |
|---|---|
| `.pdf` | Preferred — used as visual reference for LaTeX output |
| `.docx` / `.doc` | Microsoft Word — requires `pandoc` |
| `.odt` | OpenDocument (LibreOffice) — requires `pandoc` |
| `.tex` | LaTeX source — read directly, no conversion needed |
| `.md` / `.txt` | Plain text / Markdown — read directly, no conversion needed |

If you provide both a PDF and a plain-text version of the same resume, the PDF is used as the visual formatting reference. All files contribute to content extraction.

## Multiple resumes

Place more than one resume file in `resumes/`. jobbi reads all of them and uses the most relevant one as the base for each job application.

---

## Re-running setup

Delete `profile.md` and run Claude Code again. jobbi will re-read your resumes and rebuild the profile from scratch.

You can also edit `profile.md` directly at any time — for example, to change `JOB_PLATFORMS` without a full re-setup.

---

## What jobbi will NOT do

- Activate LinkedIn Premium or make any purchases
- Overwrite your original resume files
- Invent experience, publications, or skills not in your resume
- Use unverified or unofficial job sources — secondary sources (Indeed, Glassdoor, Built In, ZipRecruiter, etc.) are cross-referenced against the primary listing before being accepted

---

## Examples

See the [`examples/`](examples/) folder for:
- A sample `profile.md.example` showing the expected profile format
- A sample job output folder with `job_details.txt` and `resume_changes.txt`

---

## License

MIT
