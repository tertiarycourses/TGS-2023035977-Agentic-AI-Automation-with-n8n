---
name: wsq-assessment
description: Generate WSQ course assessments as professionally formatted Word documents (.docx) — a Written Assessment (WA) that tests KNOWLEDGE and a practical instrument that tests PRACTICAL ability, each as a question paper PLUS a model-answer / marking guide. Two builders are provided. build_assessment.py produces WA (SAQ) + PP (Practical Performance): the WA is open-ended short-answer knowledge questions drawn from the course slides, and the PP is activity-based practical tasks (LO1..LOn) whose model answers are the in-class lab build steps; both carry the WSQ house COVER PAGE (same as the Lesson Plan / Learner Guide — course title + logos + UEN + version-control record). build_wsq_assessment.py is the alternate WA + Case Study (CS) variant. ALL questions are OPEN-ENDED (no multiple choice). Use when creating or revising assessments, written/practical/case-study questions, answer keys, or marking guides for a WSQ course.
---

# WSQ Assessment → DOCX (Written + Practical/Case-Study)

Generate two WSQ assessment instruments, each as a **question paper** and a matching **model-answer / marking guide** (four DOCX total). Pick the builder that matches the course's assessment design:

| Builder | Instruments | Best for |
|---------|-------------|----------|
| **`build_assessment.py`** (primary) | **WA (SAQ)** knowledge + **PP (Practical Performance)** activity tasks | Hands-on courses where the practical is graded on tasks the learner built in class (e.g. the n8n / Tertiary courses). Carries the **WSQ house cover page** (course title + Tertiary & course logos + UEN + version-control record), identical to the Lesson Plan / Learner Guide. |
| **`build_wsq_assessment.py`** (alternate) | **WA** knowledge + **CS (Case Study)** one coherent scenario | Courses assessed via a single written case study rather than discrete practical tasks. |

## Hard rules (do not break)
- **NO multiple choice. Every question is OPEN-ENDED.** Short-answer with a ruled/boxed answer space; never emit a)/b)/c)/d) options.
- **The Written Assessment (WA) tests KNOWLEDGE.** Every question must be answerable from the course **slides / modules**. Tag each with a knowledge code (K1, K2, …) and cite the source in the answer key.
- **The practical instrument tests PRACTICAL ability.** For **PP**, each task maps to a learning outcome (LO1, LO2, …) and to an **activity the learner did in class**; the model answer **is the lab build steps** (name the exact triggers/actions and cite the activity). For **CS**, use **one coherent scenario** built from the in-class activities.
- **Everything is "covered in class."** Do not test content that is not in the slides or labs.
- **Keep the question/task count stable** when revising an existing assessment — update the wording and answers, don't change the count, unless asked.

## How to use `build_assessment.py` (WA + PP)
1. Copy `build_assessment.py` into the course repo's `assessment/` folder (it resolves the repo root as two levels up).
2. It reuses **`prodoc.py`** from the sibling **tertiary-lesson-plan** skill for the cover page + version control + page numbers, so both skills should be installed. The import auto-falls-back from the project `.claude/skills/` to `~/.claude/skills/`.
3. Edit the **CONFIG** block: `TITLE`, `Q_VER`/`A_VER` (file-name versions), the `*_VERSIONS` version-control rows, `ORG_LOGO`, `COURSE_LOGO`.
4. Fill the two content lists **from the course materials**:
   - `WRITTEN` — `(criterion, context, question, [model-answer points])`. Read the concept slides and turn each key concept into one open-ended knowledge question. Keep it to the concepts actually taught.
   - `SCENARIO` + `PRACTICAL` — one continuous scenario, then `(label, criterion, task_prompt, box_caption, [model build-step points])` per task. Each task maps to one LO and to a class activity; the model points **are** the lab procedure (cite the activity numbers).
5. Run `python3 assessment/build_assessment.py` → writes the four DOCX into `assessment/`:
   `WA (SAQ) - <Title> - <Q_VER>.docx`, `Answer to WA (SAQ) - <Title> - <A_VER>.docx`,
   `PP Assessment - <Title> - <Q_VER>.docx`, `Answer to PP Assessment - <Title> - <A_VER>.docx`.
6. Optionally render PDFs: `soffice --headless --convert-to pdf --outdir assessment assessment/*.docx`.

## Document format (WSQ house style)
- **Cover page** — same as the Lesson Plan / Learner Guide (Tertiary Infotech Academy logo, UEN, instrument name, "For", course logo, course title, TGS ref, "Conducted by", version) followed by a **Document Version Control Record** table.
- **Question paper** — centred title block; **A: Trainee Information** (name, last 3 NRIC digits + alphabet, date); **B: Instructions to Candidate**; **C:** the questions/tasks with **boxed answer space**; and a **For Official Use Only** block (Grade C / NYC, assessor name/NRIC/date/signature).
- **Answer document** — the model answers / marking guide: each question/task with "Suggestive answers (not exhaustive):" bullet points (WA cites the slide/module; PP lists the lab build steps and cites the activities).
- Body is **Arial 11**; every page has the copyright + page-number footer.

## Criterion tagging
- Written knowledge items → `K1, K2, …`.
- Practical/case-study tasks → `LO1, LO2, …` (or `A1, A2, …`). Keep the same numbering across the question paper and its answer key.

## Quality checklist before saving
- [ ] Zero multiple-choice questions anywhere.
- [ ] Every WA question traces to a slide/module; every PP/CS answer traces to a class activity/lab.
- [ ] One coherent PP scenario (not disconnected mini-cases).
- [ ] Cover page + version-control record present; question paper has Trainee Information, Instructions, boxed answers, and For Official Use Only.
- [ ] Answer-key wording is guidance ("award the mark where the candidate covers…"), not a rigid script.
- [ ] Old/mismatched assessment files (previous versions, other courses) removed from the output folder.
