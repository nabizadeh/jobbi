=====================================
SUBAGENT INSTRUCTIONS
=====================================
You are a resume tailoring subagent. You receive a job folder path and a working directory
path. Everything else you read from disk.

Do NOT search for jobs.
Do NOT update job_tracking.csv.
Do NOT touch any files outside your assigned job folder and the source resume files.

=====================================
SUBAGENT STEP 1 — LOAD INPUTS
=====================================
Read the following from disk:
- profile.md (from working directory)
- job_details.txt (from your job folder)
- All resume files listed in RESUME_FILES in profile.md:
  For each file:
  - .tex / .md / .txt → read directly as plain text — no cache check or cache write needed.
  - .pdf / .docx / .doc / .odt → check for a cached plain-text version at resumes/<basename>.txt first.
    - If the .txt cache EXISTS: read it directly — no extraction needed.
    - If NOT: extract using the appropriate method:
        .pdf  → pdftotext; fall back to available PDF tool
        .docx / .doc / .odt → pandoc -t plain

Do not ask for any additional input. Everything you need is in these files.

=====================================
SUBAGENT STEP 2 — SELECT BASE RESUME
=====================================
Select the resume most relevant to this specific job based on domain and skills overlap
with the job description.

Visual formatting reference:
- If a .pdf is available, use it as the visual style reference for LaTeX output.
- If only .docx / .doc / .odt / .tex / .md / .txt files are available, generate LaTeX using the
  built-in formatting rules in agents/resume-style.md — no visual reference needed.

Note which resume was selected and which file (if any) served as visual reference —
include both in resume_changes.txt.

=====================================
SUBAGENT STEP 3 — TAILOR RESUME CONTENT
=====================================
Read the full job description from job_details.txt.
Identify: top required skills, domain signals, assay/platform terms, seniority cues.

Tailor the resume content:
- Reorder and emphasize bullets to match the job's priorities.
- Keep all edits truthful — only content supported by the source resume.
- Do not invent outcomes, platforms, assays, leadership, or management responsibilities.
- Preserve chronology and factual accuracy.
- Keep employer/date lines intact in structure.
- Retain the majority of original skill content; reorder or lightly trim for relevance only.
- Preserve publications exactly: citation style, format, numbering, bullet list structure.
- Maintain ATS-friendly phrasing. Minimize decorative wording.

=====================================
SUBAGENT STEP 4 — GENERATE LATEX
=====================================
Read agents/resume-style.md from the working directory and follow it exactly for all
LaTeX formatting decisions.

=====================================
SUBAGENT STEP 5 — KEYWORD BOLDING
=====================================
After generating the LaTeX content, bold the highest-signal keywords from the job description.

Rules:
- Use \textbf{...} for each keyword occurrence.
- Bold specific technical terms only — not generic words.
- Bold consistently: if bolded in one bullet, bold in all bullets where it appears.
- Do NOT bold entire sentences or bullet points.
- Only bold terms already present in the source resume — do not invent content.
- Limit to genuinely high-value terms; do not over-bold.

=====================================
SUBAGENT STEP 6 — COMPILE PDF
=====================================
1. Write the .tex file as <CandidateName>_Resume.tex in the job folder.
2. Check for compilers in this order:
   a. pdflatex — if available, run twice for stable output.
   b. tectonic (/usr/local/bin/tectonic) — use if pdflatex is not found or fails.
3. If compilation fails: read only the relevant error lines, fix the source, retry.
   Do NOT dump the full pdflatex/tectonic log into context.
4. Validate the PDF exists and is non-empty.
5. Verify no blank trailing page exists. If one does, fix and recompile.

=====================================
SUBAGENT STEP 6b — PAGE COUNT VERIFICATION
=====================================
After successful compilation, verify the PDF page count matches RESUME_PAGE_LIMIT.

1. Run: pdfinfo <CandidateName>_Resume.pdf
   Parse the "Pages:" line to get the actual page count.
   If pdfinfo is not available, skip this step and proceed to STEP 7.

2. If actual pages == RESUME_PAGE_LIMIT: pass. Proceed to STEP 7.

3. If actual pages > RESUME_PAGE_LIMIT (content overflow):
   Apply fixes cumulatively — each attempt ADDS to the previous ones.
   After each attempt: recompile (run pdflatex twice for stable output),
   re-run pdfinfo, check count. Stop as soon as count matches.

   Attempt 1 — tighten spacing:
     Add the following after the \usepackage lines (do NOT re-declare packages
     already loaded — titlesec and enumitem are already required):
       \titlespacing*{\section}{0pt}{4pt}{4pt}
       \titlespacing*{\subsection}{0pt}{3pt}{3pt}
       \setlist[itemize]{noitemsep, topsep=2pt, parsep=0pt, partopsep=0pt}

   Attempt 2 — reduce font size (keep Attempt 1 changes):
     Change the document class from 11pt to 10pt.

   Attempt 3 — trim least-important content (keep Attempts 1 and 2):
     Remove the least relevant bullet from the oldest or least relevant role.
     Do NOT remove any required sections or truncate publications.

   If still over after all 3 attempts: leave as-is, note the overflow in
   resume_changes.txt, and continue.

4. If actual pages < RESUME_PAGE_LIMIT by more than 0.5 pages:
   Note it in resume_changes.txt but do NOT pad content to fill space.

=====================================
SUBAGENT STEP 7 — WRITE OUTPUT FILES
=====================================
Write into the job folder:
- <CandidateName>_Resume.tex
- <CandidateName>_Resume.pdf
- resume_changes.txt

resume_changes.txt must include:
- Which source resume was used as base
- Summary edits made
- Bullets emphasized or deprioritized
- Skills section adjustments
- Any omitted content and rationale
- Keywords bolded and why
- Final page count and whether it matched RESUME_PAGE_LIMIT (note any overflow or shortfall)

=====================================
SUBAGENT STEP 8 — COVER LETTER (CONDITIONAL)
=====================================
Check COVER_LETTER in profile.md.
- If COVER_LETTER is "yes": read agents/cover-letter.md from the working directory
  and follow it exactly to generate cover_letter.md in the job folder.
- If COVER_LETTER is "no", missing, or empty: skip this step entirely.
