# Resume Style Guide
#
# This file controls how jobbi formats your LaTeX resume.
# It is intentionally separated from the agent logic so you can customize it
# for your market, preferences, or local hiring norms without touching any
# other files.
#
# Common customizations:
#   - Add a photo (required in some countries, e.g. Denmark, Germany)
#   - Change section order (e.g. Education before Work Experience for recent grads)
#   - Adjust font size, margins, or spacing
#   - Add or remove sections (e.g. Languages, Certifications, Volunteer Work)
#   - Change date format or contact line style

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
