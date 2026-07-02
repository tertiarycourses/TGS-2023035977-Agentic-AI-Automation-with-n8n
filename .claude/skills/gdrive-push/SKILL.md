---
name: gdrive-push
description: Push the current WSQ courseware (slides PPT/PDF, Learner Guide, Lesson Plan, assessments) to the user's Google Drive courseware folder, auto-archiving old versions. Use when the user runs /gdrive-push or asks to upload/push courseware to Google Drive. ALWAYS requires the user-supplied Drive folder link.
---

# GDrive Push — WSQ courseware to Google Drive

Uploads the course's current artifacts into the right subfolders of a Google Drive
courseware folder, moving superseded versions into an `Archive` subfolder first.
**Upload-only: nothing on Drive is ever deleted.**

## HARD RULE — user input required

**NEVER push without the user-provided Google Drive folder link.** If the user did not
include the courseware folder link (e.g. `/gdrive-push <link>`), ASK for it first
(AskUserQuestion) and wait. Do not fall back to a remembered, default, or previously
used folder. Confirm the link before the first real (non-dry-run) push of a session.

## Routing

| Drive subfolder (created if missing) | Files pushed |
|---|---|
| Master Trainer Slides | slide deck `.pptx` + `.pdf` (current version only) |
| Learner Guide | `LG-*.docx` + `LG-*.pdf` + the slides `.pdf` |
| Lesson Plan | `LP-*.docx` + `LP-*.pdf` |
| Assessment | all `assessment/*.docx` (WA + PP papers and answer keys) |

Before each upload, existing Drive files of the same family (same base name ignoring
the `-vNN` version suffix, same extension) are MOVED to `<subfolder>/Archive/`.
Subfolders are matched case-insensitively (e.g. an existing "Assessments" folder is
reused, not duplicated).

## How to run

```bash
python3 <this-skill-dir>/gdrive_push.py "<drive-folder-link>" --repo "<course repo>" --dry-run   # preview
python3 <this-skill-dir>/gdrive_push.py "<drive-folder-link>" --repo "<course repo>"             # real push
```

Always run `--dry-run` first and show the user the plan; then do the real push.
Report per-folder what was archived and uploaded.

## Transport / prerequisites

The script talks to a local n8n webhook proxy (`POST http://localhost:5678/webhook/gdrive-ops`,
workflow **"GDrive Courseware Push (proxy)"**) which signs Google Drive REST calls with the
n8n **Google Drive account** OAuth2 credential.

- If the proxy workflow is missing: recreate it with `python3 setup_proxy.py <n8n-email> <n8n-password>`.
- If calls fail with "Unable to sign without access token": the n8n Drive credential has
  not completed OAuth — the user must open n8n → Credentials → *Google Drive account* →
  **Sign in with Google** once, then retry.
- Override the proxy URL with env `GDRIVE_PROXY_URL` if n8n runs elsewhere.
