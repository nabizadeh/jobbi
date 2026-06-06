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
COMPANY_BLOCKLIST: {{COMPANY_BLOCKLIST}}
COMPANY_PRIORITY: {{COMPANY_PRIORITY}}

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
COVER_LETTER: {{COVER_LETTER}}

--- RESUME FILES ---
RESUME_FILES: {{RESUME_FILES}}

=====================================
SETUP STEP 3 — ASK USER FOR MISSING BLANKS
=====================================
After attempting auto-fill from the resume(s):

- If ALL blanks are filled: skip this step.
- If ANY blanks remain MISSING:
  - Ask ONE field at a time. Wait for the user's response before asking the next.
  - Do NOT list all missing fields at once. Do NOT collect all answers in one prompt.
  - Do NOT proceed to job searching until all required blanks are resolved.

Required fields (must be filled before continuing):
  CANDIDATE_NAME, CANDIDATE_EMAIL, TARGET_ROLES, PRIMARY_DOMAINS, LOCATION_PRIORITY_1

Optional fields (user may answer "skip" to leave blank):
  CANDIDATE_PHONE, CANDIDATE_LINKEDIN, LOCATION_PRIORITY_2, LOCATION_PRIORITY_3

Ask ALL of the following fields one at a time, in this exact order.
Wait for the user's response after each before moving to the next.
Do NOT show multiple questions at once.

For questions marked USE ASKUSERQUESTION: present them using the AskUserQuestion tool
so the user gets an interactive selectable list (arrow keys + Enter).
For open-ended questions: ask as plain text.

Company preference fields (plain text — open-ended answers):

  1. COMPANY_BLOCKLIST:
     Ask: "Any companies to never show in results?
     Enter a comma-separated list, or press Enter to skip:"
     If skipped or empty → leave blank.

  2. COMPANY_PRIORITY:
     Ask: "Any companies you're especially interested in? (they'll get a score boost)
     Enter a comma-separated list, or press Enter to skip:"
     If skipped or empty → leave blank.

Search preference fields:

  3. JOB_RECENCY_DAYS — USE ASKUSERQUESTION:
     Question: "How recent should job postings be?"
     Options:
       - "Past 24 hours"         → value: 1
       - "Past 48 hours"         → value: 2  (Recommended)
       - "Past week"             → value: 7
       - "Past 2 weeks"          → value: 14

  4. MIN_JOBS_PER_RUN — USE ASKUSERQUESTION:
     Question: "Minimum number of jobs to find per run?"
     Options:
       - "3 jobs"   → value: 3
       - "5 jobs"   → value: 5  (Recommended)
       - "10 jobs"  → value: 10
       - "15 jobs"  → value: 15

  5. RESUME_PAGE_LIMIT — USE ASKUSERQUESTION:
     Question: "How many pages should the tailored resume be?"
     Options:
       - "1 page"   → value: 1
       - "2 pages"  → value: 2  (Recommended)
       - "3 pages"  → value: 3

  6. COVER_LETTER — USE ASKUSERQUESTION:
     Question: "Generate a cover letter for each job alongside the resume?"
     Options:
       - "No — resume only"      → value: no   (Recommended)
       - "Yes — include a cover letter" → value: yes
     Note: you can place writing_sample.txt in resumes/ to help jobbi match your tone.

  7. JOB_PLATFORMS — USE ASKUSERQUESTION with multiSelect: true:
     Question: "Which job boards should jobbi search? Select all that apply."
     Options (select multiple):
       - "LinkedIn"      → value: linkedin
       - "Indeed"        → value: indeed
       - "Glassdoor"     → value: glassdoor
       - "ZipRecruiter"  → value: zip_recruiter
       - "Google Jobs"   → value: google
     Default if none selected or user skips: linkedin, indeed, glassdoor, zip_recruiter, google
     Note: Glassdoor has few listings in some markets (e.g. Denmark) — deselect it if that's your case.
     Note: bayt (Middle East), naukri (India), bdjobs (Bangladesh) can be added manually to
     profile.md if needed — they exceed the 4-option limit here.

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
COMPANY_BLOCKLIST: <value>
COMPANY_PRIORITY: <value>

PRIMARY_DOMAINS: <value>
KEY_TECHNICAL_SKILLS: <value>
KEY_TOOLS_AND_PLATFORMS: <value>
STRONGEST_SCIENTIFIC_THEMES: <value>

JOB_RECENCY_DAYS: <value>
MIN_JOBS_PER_RUN: <value>
RESUME_PAGE_LIMIT: <value>
JOB_PLATFORMS: <value>
COVER_LETTER: <value>

RESUME_FILES: <value>
---

After saving, confirm to the user:
"Profile saved to profile.md. Setup complete. Starting job search now."

Then proceed to agents/orchestrator.md.
