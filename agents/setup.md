=====================================
SETUP STEP 1 — DETECT RESUME(S)
=====================================
Supported resume formats: .pdf, .docx, .doc, .odt, .tex, .md, .txt
Scan the `resumes/` subfolder for files with any of these extensions.
Ignore `DROP_YOUR_RESUME_HERE.txt` and any other non-resume files.

If NO supported resume files are found in `resumes/`:
- Print a clear message:
  "No resume found. Please place your resume file(s) in the resumes/ folder and run again.
   Supported formats: .pdf, .docx, .doc, .odt, .tex, .md, .txt"
- Stop. Do not continue.

If ONE OR MORE supported files are found:
- List them to the user.
- When scanning for .txt and .md files, skip any file whose basename (filename without
  extension) matches the basename of a PDF, DOCX, DOC, or ODT file also found in resumes/ —
  it is an auto-generated text cache, not a separate resume.
- For each remaining file:
  - .tex / .md / .txt → read directly as plain text — no cache check or cache write needed.
  - .pdf / .docx / .doc / .odt → check whether a cached plain-text version already exists at
    resumes/<basename>.txt (e.g. resumes/MyResume.pdf → resumes/MyResume.txt).
    - If the .txt cache EXISTS: read it directly — skip extraction.
    - If the .txt cache DOES NOT EXIST: extract content using the appropriate method,
      then immediately write the extracted text to resumes/<basename>.txt for future runs:
        .pdf  → pdftotext (preferred); fall back to reading with available PDF tool
        .docx / .doc / .odt → pandoc -t plain (if pandoc unavailable, report and skip that file)
- If a PDF and a non-PDF version of the same resume exist, flag the PDF as the visual
  formatting reference (regardless of which was cached first).
- Treat all successfully extracted files as the candidate's resume library.
- Use ALL of them to fill the profile blanks in SETUP STEP 2.
- If multiple resumes conflict on a detail, prefer the most recent or most complete value.

=====================================
SETUP STEP 2 — FILL PROFILE BLANKS
=====================================
Extract the following from the resume(s).
If a value can be confidently extracted, fill it automatically.
If a value is ambiguous or missing, mark it as MISSING.

--- IDENTITY ---
CANDIDATE_NAME: {{CANDIDATE_NAME}}
CANDIDATE_EMAIL: {{CANDIDATE_EMAIL}}
CANDIDATE_PHONE: {{CANDIDATE_PHONE}}
CANDIDATE_LINKEDIN: {{CANDIDATE_LINKEDIN}}
CANDIDATE_LOCATION: {{CANDIDATE_LOCATION}}

--- PROFESSIONAL PROFILE ---
CURRENT_ROLE: {{CURRENT_ROLE}}
CURRENT_EMPLOYER: {{CURRENT_EMPLOYER}}
YEARS_OF_EXPERIENCE: {{YEARS_OF_EXPERIENCE}}
EDUCATION_LEVEL: {{EDUCATION_LEVEL}}
EDUCATION_FIELD: {{EDUCATION_FIELD}}

--- JOB SEARCH PREFERENCES ---
TARGET_ROLES: {{TARGET_ROLES}}
LOCATION_PRIORITY_1: {{LOCATION_PRIORITY_1}}
LOCATION_PRIORITY_2: {{LOCATION_PRIORITY_2}}
LOCATION_PRIORITY_3: {{LOCATION_PRIORITY_3}}
SENIORITY_TARGET: {{SENIORITY_TARGET}}

--- DOMAIN & SKILLS ---
PRIMARY_DOMAINS: {{PRIMARY_DOMAINS}}
KEY_TECHNICAL_SKILLS: {{KEY_TECHNICAL_SKILLS}}
KEY_TOOLS_AND_PLATFORMS: {{KEY_TOOLS_AND_PLATFORMS}}
STRONGEST_SCIENTIFIC_THEMES: {{STRONGEST_SCIENTIFIC_THEMES}}

--- SEARCH PREFERENCES ---
JOB_RECENCY_DAYS: {{JOB_RECENCY_DAYS}}
MIN_JOBS_PER_RUN: {{MIN_JOBS_PER_RUN}}
RESUME_PAGE_LIMIT: {{RESUME_PAGE_LIMIT}}
JOB_PLATFORMS: {{JOB_PLATFORMS}}

--- RESUME FILES ---
RESUME_FILES: {{RESUME_FILES}}

=====================================
SETUP STEP 3 — ASK USER FOR MISSING BLANKS
=====================================
After attempting auto-fill from the resume(s):

- If ALL blanks are filled: skip this step.
- If ANY blanks remain MISSING:
  - List only the missing fields clearly.
  - Ask the user to provide values, one field at a time or as a group.
  - Do NOT proceed to job searching until all required blanks are resolved.

Required fields (must be filled before continuing):
  CANDIDATE_NAME, CANDIDATE_EMAIL, TARGET_ROLES, PRIMARY_DOMAINS, LOCATION_PRIORITY_1

Optional fields (user may answer "skip" to leave blank):
  CANDIDATE_PHONE, CANDIDATE_LINKEDIN, LOCATION_PRIORITY_2, LOCATION_PRIORITY_3

Search preference fields — ask these explicitly with the defaults shown:

  JOB_RECENCY_DAYS:
    Ask: "How recent should job postings be?
      1  = past 24 hours
      2  = past 48 hours  (default)
      7  = past week
      14 = past 2 weeks
    Press Enter to use the default (2):"
    If user presses Enter or provides no input → use 2.

  MIN_JOBS_PER_RUN:
    Ask: "Minimum number of jobs to find per run? (default: 5):"
    If user presses Enter or provides no input → use 5.
    Do NOT lower quality standards to meet this number.

  RESUME_PAGE_LIMIT:
    Ask: "How many pages should the tailored resume be? (default: 2):"
    If user presses Enter or provides no input → use 2.

  JOB_PLATFORMS:
    Ask: "Which job boards should jobbi search? Available platforms:
      linkedin, indeed, glassdoor, zip_recruiter, google  (US/global)
      bayt                                                 (Middle East)
      naukri                                               (India)
      bdjobs                                               (Bangladesh)
    Enter a comma-separated list, or press Enter for the default:
    (default: linkedin, indeed, glassdoor, zip_recruiter, google):"
    If user presses Enter or provides no input → use: linkedin, indeed, glassdoor, zip_recruiter, google.
    Tip: remove platforms that have few listings in your market (e.g. remove glassdoor for Denmark).

=====================================
SETUP STEP 4 — SAVE profile.md
=====================================
Once all required blanks are filled, write a `profile.md` file in the current directory
using the filled values. Use this exact format:

---
# Candidate Profile
# Auto-generated by jobbi on first run. Edit manually if needed.
# Delete this file to re-run setup.

CANDIDATE_NAME: <value>
CANDIDATE_EMAIL: <value>
CANDIDATE_PHONE: <value>
CANDIDATE_LINKEDIN: <value>
CANDIDATE_LOCATION: <value>

CURRENT_ROLE: <value>
CURRENT_EMPLOYER: <value>
YEARS_OF_EXPERIENCE: <value>
EDUCATION_LEVEL: <value>
EDUCATION_FIELD: <value>

TARGET_ROLES: <value>
LOCATION_PRIORITY_1: <value>
LOCATION_PRIORITY_2: <value>
LOCATION_PRIORITY_3: <value>
SENIORITY_TARGET: <value>

PRIMARY_DOMAINS: <value>
KEY_TECHNICAL_SKILLS: <value>
KEY_TOOLS_AND_PLATFORMS: <value>
STRONGEST_SCIENTIFIC_THEMES: <value>

JOB_RECENCY_DAYS: <value>
MIN_JOBS_PER_RUN: <value>
RESUME_PAGE_LIMIT: <value>
JOB_PLATFORMS: <value>

RESUME_FILES: <value>
---

After saving, confirm to the user:
"Profile saved to profile.md. Setup complete. Starting job search now."

Then proceed to agents/orchestrator.md.
