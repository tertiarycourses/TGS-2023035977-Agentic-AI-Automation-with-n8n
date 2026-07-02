#!/usr/bin/env bash
# Single-command aligned build of all courseware from the skill sources.
# Produces (in courseware/): the versioned PPT, LP and LG as DOCX + PDF,
# with page-numbered Tables of Contents in the LP and LG PDFs.
#
# Pipeline: run the python-pptx / python-docx generators, render to PDF with
# LibreOffice, inject a static page-numbered TOC (LibreOffice can't update the
# TOC field headless here), then re-render the LP/LG PDFs.
set -euo pipefail
cd "$(dirname "$0")/../../.."          # repo root
REPO="$(pwd)"
CW="$REPO/courseware"
SKILLS="$REPO/.claude/skills"
SOFFICE="${SOFFICE:-soffice}"

echo "==> Generate PPT / LP / LG"
python3 "$SKILLS/tertiary-course-slides/make_slides.py"
python3 "$SKILLS/tertiary-lesson-plan/make_lesson_plan.py"
python3 "$SKILLS/tertiary-learner-guide/make_learner_guide.py"

PPT="$(ls -t "$CW"/Agentic\ AI\ Automation\ with\ n8n-v*.pptx | head -1)"
LP="$CW/LP-Agentic AI Automation with n8n.docx"
LG="$CW/LG-Agentic AI Automation with n8n.docx"

echo "==> Render PDFs (pass 1)"
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$PPT"  >/dev/null 2>&1
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LP"   >/dev/null 2>&1
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LG"   >/dev/null 2>&1

echo "==> Inject page-numbered Table of Contents (LP + LG)"
python3 "$CW/build/inject_toc.py" "$LP" "${LP%.docx}.pdf" 2
python3 "$CW/build/inject_toc.py" "$LG" "${LG%.docx}.pdf" 2

echo "==> Render PDFs (pass 2 — with built TOC)"
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LP"   >/dev/null 2>&1
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LG"   >/dev/null 2>&1

echo "==> Done. Artifacts in courseware/:"
ls -1 "$CW"/*.pptx "$CW"/*.docx "$CW"/*.pdf
