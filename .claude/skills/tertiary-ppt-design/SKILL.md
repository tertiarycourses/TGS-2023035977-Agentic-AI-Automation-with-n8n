---
name: tertiary-ppt-design
description: Best-practice design system and rules for building highly professional, visual training/course slide decks with python-pptx (Tertiary Infotech house style). Use whenever creating or polishing a .pptx deck so the result is clean, white-theme, visual, and consistent — large readable fonts, brand colours, icon/card layouts, screenshots and diagrams instead of walls of text. Pair with the tertiary-course-slides skill.
---

# PPT Design & Presentation — Best Practices

Apply these when generating or refining a course/training deck (python-pptx).

## Theme & format
- **16:9** (13.333 × 7.5 in). **All-white slides — never dark/black backgrounds.**
- **Font: Arial** for every run. Brand colours: blue `#1F6FEB`, teal `#10B981`, ink `#161B26`, grey `#5B6372`, violet `#7C3AED`, light `#F5F8FC`.
- Cover with the **course title + n8n & Tertiary Infotech Academy logos + UEN**; footer on every content slide = course/code (left), `© 2026 Tertiary Infotech Academy Pte Ltd` (center), slide number (right).

## Typography (make it presentable — large fonts)
- Slide **title ≈ 28–30 pt**, kicker label ≈ 14 pt (brand colour, uppercase).
- **Body bullets ≈ 18–20 pt** (never below 16 pt). Two-column body ≈ 17 pt. Card body ≈ 14 pt.
- Section dividers: title ≈ 40 pt, big faint topic number ≈ 72 pt.
- Step slides: one step, big numbered circle + step text ≈ 24 pt.

## Be visual, not wordy (reference style — Business Process Automation deck)
- **≤ 5 bullets per slide**, one idea per bullet — and bullets only for admin/recap slides. Concept slides use components:
  - **Chevron flow strips** (`chev_strip`): outlined boxes (bold title + small grey sub-caption) joined by ▶ — for any mechanism or pipeline (webhook round-trip, RAG ingestion/retrieval, expression resolution, approval suspension). Two stacked strips (red "manual" vs green "automated") make a powerful before/after.
  - **Outlined concept cards** (`ncards`): white cards with a colored border, numbered badge, colored title and 1–2 line body — for enumerations (triggers, data nodes, model parameters, tools).
  - **Two-panel comparisons** (`two_panel`): solid colored header bars over outlined bullet panels — GET vs POST, Test vs Production URL, Generative vs Agentic AI, MCP server vs client.
  - **Data tables** (`data_table`): colored header row + striped rows, first column bold — mappings and multi-way comparisons (trigger→lab, vector DBs, human in/on/out of the loop).
  - **Takeaway band** (`takeaway`): ONE bold boxed sentence at the bottom stating the rule to remember — most concept slides should end with one.
  - **Good/bad callout pairs**: green ✓ vs red ✗ outlined boxes (good vs bad instructions, picker vs typed expressions).
  - **Screenshot slides**: real product screenshots (websites, the n8n canvas) beside short bullets.
- Add the **real workflow screenshot** AND (where the lab has one) the **website screenshot** for every hands-on activity; a **gallery** for sample student work.

## Structure of a course deck
1. Cover → admin (digital attendance/TRAQOM, trainer ×2 profile cards, ground rules, LMS, lesson plan, learning outcomes, lab journey, briefing, assessment, assessment flow).
2. Per topic: a **section divider** (outlined rounded box: kicker + title + subtitle + "Applied in Activity N"), concept slides built from the components above, then per activity **exactly ONE lab slide** — intro line + workflow chevron strip of the actual nodes + n8n canvas screenshot + bottom LAB band (ACT chip · lab name · stack meta · "steps in the Learner Guide") — plus a website slide if the lab has a web front-end. **NEVER one-step-per-slide runs or "Test it" step slides — step-by-step detail lives in the Learner Guide only.**
3. **Lunch/tea-break** divider slides; recap slides at the end of each day; assessment admin repeated at the end; a Thank-You close.

## Consistency & alignment
- Activity titles and topic numbering must **match the Learner Guide and Lesson Plan exactly** (e.g. Activity 8a = Leave Approval HITL, 8b = Dashboard, 8c = Guardrails).
- Reuse helper functions (`concept`, `chev_strip`, `ncards`, `two_panel`, `data_table`, `takeaway`, `lab_slide`, `website_lab`, `content`, `website_slide`, `gallery_slide`, `img_slide`, `section`, `tile_grid`, `flow_h`, `trainer_slide`) so spacing/fonts stay uniform.

Implementation lives in the **tertiary-course-slides** skill (`make_slides.py`).
