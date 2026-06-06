=====================================
RESUME REVISION MODE
=====================================
If the user asks to change, fix, update, or tweak a resume after generation, enter
revision mode. Do NOT start a new job search. Do NOT regenerate the resume from scratch.

Trigger phrases (examples):
- "change the summary in the Genentech resume"
- "remove the LNP bullet from the insitro application"
- "the font looks wrong in Revolution Medicines"
- "reword the third bullet in my Recursion resume"

Revision workflow:
1. Identify the target job folder from the user's description.
   - Search results/ subfolders and any root-level job folders by company/role name.
   - If ambiguous, list the matching folders and ask the user to confirm.
2. Read the existing <CandidateName>_Resume.tex from that folder.
   Do NOT read the source resume files — the .tex file is the working document.
3. Make ONLY the specific changes the user requested.
   - Do not rewrite sections the user did not mention.
   - Do not re-tailor or re-score for the job.
   - Do not add or remove keyword bolding beyond what was asked.
   - Preserve all other content exactly as it is.
4. Recompile the PDF:
   - Use tectonic if pdflatex is unavailable (same fallback order as resume-tailor.md Step 6).
   - If compilation fails: read only the relevant error lines, fix, retry.
   - Do NOT dump the full compiler log into context.
   - Validate the PDF exists, is non-empty, and has no blank trailing page.
5. Confirm to the user what changed and that the PDF was recompiled successfully.
   Append a brief note to resume_changes.txt describing the revision and date.

Hard rules for revision mode:
- NEVER regenerate the .tex from scratch unless the user explicitly asks for it.
- NEVER overwrite the source resume files in resumes/.
- NEVER modify job_tracking.csv or job_details.txt during a revision.
- If the user asks for a change that would require fabricating experience,
  refuse and explain why, then suggest a truthful alternative.
