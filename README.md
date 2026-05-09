# jobbi

An autonomous job search and resume tailoring agent for Claude Code.

Drop your resume in a folder, run Claude Code, and jobbi finds matching jobs, scores them, and generates a tailored PDF resume for each one — ready to submit.

---

## What it does

1. **First run:** reads your resume PDF(s), builds a personal profile, asks you to fill any gaps
2. **Every run after:** skips setup and goes straight to job hunting
3. Searches LinkedIn and official company career pages for roles posted in the last 14 days
4. Scores each job against your profile (skills, domain, seniority, tools)
5. Rejects weak matches; accepts only scores ≥ 70
6. For every accepted job: generates a tailored LaTeX resume, compiles it to PDF, and logs it to a tracking CSV

---

## Requirements

- [Claude Code](https://claude.ai/code) (CLI)
- A LaTeX distribution: [TeX Live](https://tug.org/texlive/), [MacTeX](https://tug.org/mactex/), or [Tectonic](https://tectonic-typesetting.github.io/)
- Your resume as a PDF

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/nabizadeh/jobbi.git
cd jobbi

# 2. Drop your resume into the resumes/ folder
cp /path/to/YourResume.pdf resumes/

# 3. Run Claude Code
claude
```

On first run, jobbi will:
- Detect your resume PDF(s)
- Extract your profile automatically
- Ask you only for anything it couldn't find
- Save a `profile.md` so setup never runs again
- Start searching for jobs

---

## File structure

```
jobbi/
├── AGENTS.md                          # Agent instructions (the brain)
├── .claude/settings.json              # Pre-approved commands (no permission prompts)
├── profile.md                         # Auto-generated on first run (gitignored)
├── job_tracking.csv                   # Cumulative job log across all runs (gitignored)
│
├── resumes/                           # Drop your resume(s) here
│   ├── DROP_YOUR_RESUME_HERE.txt      # Placeholder — do not delete
│   └── YourResume.pdf                 # Your resume (gitignored)
│
└── results/                           # All search output (gitignored)
    └── 2026-05-09/                    # One folder per day (or _2, _3 for multiple runs)
        └── Company_Role_001/          # One subfolder per accepted job
            ├── job_details.txt        # Full job info and match rationale
            ├── YourName_Resume.tex    # Tailored LaTeX source
            ├── YourName_Resume.pdf    # Compiled, submission-ready PDF
            └── resume_changes.txt     # What changed and why
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

If you provide both a PDF and a Word/LaTeX version of the same resume, the PDF is used as the visual formatting reference. All files contribute to content extraction.

## Multiple resumes

Place more than one resume file in `resumes/`. jobbi reads all of them and uses the most relevant one as the base for each job application.

---

## Re-running setup

Delete `profile.md` and run Claude Code again. jobbi will re-read your resumes and rebuild the profile from scratch.

---

## What jobbi will NOT do

- Activate LinkedIn Premium or make any purchases
- Overwrite your original resume PDFs
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
