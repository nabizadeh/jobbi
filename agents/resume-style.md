# Resume Style Guide
#
# This file controls how jobbi formats your LaTeX resume.
# It is intentionally separated from the agent logic so you can customize it
# for your market, preferences, or local hiring norms without touching any
# other files.
#
# HOW TO CUSTOMIZE:
# Edit the instructions below. The subagent reads this file and generates
# LaTeX accordingly. You do not need to write LaTeX yourself — just describe
# what you want in plain language and the subagent will implement it.
#
# See the CUSTOMIZATION EXAMPLES section at the bottom for ready-to-use
# recipes for common markets and preferences.

=====================================
SUBAGENT STEP 4 — GENERATE LATEX
=====================================
Generate a complete LaTeX resume that replicates the formatting of the source PDF.

Document requirements:
- Class: article, 11pt
- Single-column, ATS-friendly, no tables for core content
- Packages: geometry, enumitem, hyperref, titlesec
- No multicolumn layout, tikz graphics, heavily nested tables, or unusual glyph dependencies

Header:
- Candidate name centered on its own line
- Contact line centered below, items separated by vertical bars
- Compact, tight spacing

Sections:
- Use EXACTLY this order, every time:
    1. Header (name + contact — not a titled section)
    2. PROFESSIONAL SUMMARY
    3. WORK EXPERIENCE
    4. EDUCATION
    5. TECHNICAL SKILLS
    6. SELECTED PUBLICATIONS (omit only if the source resume contains no publications)
- Titles in uppercase, left-aligned
- Horizontal rule before every section (use \rule{\textwidth}{0.4pt})
- Rule must start on its own line — prepend \par if needed
- Section title starts on a new line after the rule, never on the same line

Experience/Education entries:
- Company/institution left, date right on the same line using \hfill
- Role/degree on the line below
- Do NOT use tables for date alignment

Bullets:
- Standard round bullets, compact itemize environments
- Wrapped lines align under text, not under bullet symbol

Page count: read RESUME_PAGE_LIMIT from profile.md and target exactly that many pages.
Do not exceed it. Do not fall more than half a page short of it.

=====================================
CUSTOMIZATION EXAMPLES
=====================================
The recipes below are NOT active. To use one, copy the relevant instructions
into the sections above, replacing the defaults.

─────────────────────────────────────
RECIPE 1: Photo in header
(Required in Denmark, Germany, and many other European markets)
─────────────────────────────────────
Replace the Header instructions above with:

  Header:
  - Add the graphicx package to the document preamble.
  - Use a two-column layout for the header only:
      Left column (75% of text width): candidate name (large, bold, left-aligned)
        and contact line below it (items separated by vertical bars).
      Right column (20% of text width): candidate photo, right-aligned.
  - Photo handling:
      1. Look for resumes/photo.jpg in the working directory.
      2. If found: copy it to the job folder, then include it in LaTeX
         with \includegraphics[width=2.8cm]{photo.jpg} (relative path works
         because the .tex file is compiled from the job folder).
      3. If NOT found: omit the photo column and fall back to the standard
         centered header. Do NOT fail or stop — just skip the photo.
  - Use a minipage environment for each column; separate with \hfill.
  - Compact, tight spacing below the header before the first section rule.
  - (The user places their photo once at resumes/photo.jpg — it is reused
    automatically for every job application.)

─────────────────────────────────────
RECIPE 2: Education before Work Experience
(Common for recent graduates or academic CVs)
─────────────────────────────────────
Replace the Sections order above with:

  Sections:
  - Use EXACTLY this order, every time:
      1. Header (name + contact — not a titled section)
      2. PROFESSIONAL SUMMARY
      3. EDUCATION
      4. WORK EXPERIENCE
      5. TECHNICAL SKILLS
      6. SELECTED PUBLICATIONS (omit only if the source resume contains no publications)

─────────────────────────────────────
RECIPE 3: Add a Languages section
(Common in Europe and international job markets)
─────────────────────────────────────
Add to the Sections order (insert after TECHNICAL SKILLS):

      6. LANGUAGES — list each language and proficiency level
         (e.g. English: Native, Danish: Conversational, German: Basic)
         Omit this section if no language information is present in the source resume.
      7. SELECTED PUBLICATIONS (if applicable)

─────────────────────────────────────
RECIPE 4: Larger margins / more breathing room
─────────────────────────────────────
Add to Document requirements:

  - Use geometry package with margins: top=1in, bottom=1in, left=0.85in, right=0.85in
    (default is tighter; adjust as needed)

─────────────────────────────────────
RECIPE 5: Smaller font for more content
(When content is dense and you need to fit more on fewer pages)
─────────────────────────────────────
Replace "Class: article, 11pt" with "Class: article, 10pt"

─────────────────────────────────────
COMBINING RECIPES
─────────────────────────────────────
Recipes can be combined. For example, a Danish CV with a photo and a
Languages section: apply Recipe 1 (photo header) and Recipe 3 (Languages),
leave everything else at the defaults.
