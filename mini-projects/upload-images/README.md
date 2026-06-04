# 🛠️ Mini-Project — Issue Reporting Flow (n8n + Postgres)

A small end-to-end app: users submit an **issue report** (name, photo, issue summary, date)
through an n8n form. The report **and the uploaded image** are stored in **Postgres**, and a
companion API + gallery page lets you **retrieve and view them later**.

```
                          ┌─────────────────────────────┐
  User fills n8n form ──▶ │  Issue Reporting - Submit    │
  (Name, Image,          │  Form ▶ Image→Base64 ▶ INSERT │ ──▶  Postgres
   Summary, Date)        └─────────────────────────────┘        (issue_reports,
                                                                  image as BYTEA)
                          ┌─────────────────────────────┐              │
  Gallery page  ────────▶ │  Issue Reporting - Reports   │ ◀── SELECT ──┘
  (gallery.html)          │  API: GET /issue-reports     │
        ▲                 └─────────────────────────────┘
        └──── images rendered from base64 data URIs ◀──── JSON
```

## Files

| File | What it is |
|------|-----------|
| [upload-image-postgressql.json](upload-image-postgressql.json) | **Submission** workflow — the n8n form that writes a report + image into Postgres. |
| [issue-reports-api.json](issue-reports-api.json) | **Retrieval** workflow — a `GET /webhook/issue-reports` API returning all reports (images as base64 data URIs). |
| [schema.sql](schema.sql) | Postgres table (`issue_reports`) the workflows read/write. |
| [gallery.html](gallery.html) | A standalone page that calls the API and shows the reports in a grid with a lightbox. |

---

## Setup

### 1. Create the table

Run the schema once against the same Postgres database your n8n Postgres credential points to:

```bash
psql -h localhost -U <user> -d <database> -f schema.sql
```

### 2. Import the workflows into n8n

In n8n: **Workflows ▸ Import from File** for each of:

- `upload-image-postgressql.json`
- `issue-reports-api.json`

Both ship with a Postgres credential reference named **"n8n Postgres (Local)"**. Open each
Postgres node and select (or re-create) your own Postgres credential if it differs.

### 3. Activate

- Open **Issue Reporting - Submit to Postgres** → click the **form trigger** node → copy the
  **Production URL** (e.g. `http://localhost:5678/form/<id>`). **Activate** the workflow.
- Open **Issue Reporting - Reports API** → **Activate** it. Its production URL is
  `https://n8n.srv923061.hstgr.cloud/webhook/issue-reports` (or
  `http://localhost:5678/webhook/issue-reports` for a local n8n).

---

## Usage

### Submit an issue
Open the form URL, fill in **Name**, **Issue Summary**, **Date**, attach an **Image**
(`.jpg/.png/.gif/.webp`), and submit. You'll see a confirmation with the new report number.

### View the reports
Open [gallery.html](gallery.html) in a browser (double-click, or serve it). The Reports API URL
box is pre-filled with `https://n8n.srv923061.hstgr.cloud/webhook/issue-reports` — adjust it if
needed, click **Load Reports**, and the submitted issues appear as cards. Click any image to
enlarge it.

> Tip: click **Save URL** so the gallery remembers the API endpoint in your browser.

---

## How the image round-trip works

- **Storing** — the form's binary file is converted to base64 by the *Image to Base64*
  (`Extract from File`) node, then inserted with `decode($6, 'base64')` so it lands in the
  `image_data BYTEA` column as raw bytes. Filename and MIME type are stored alongside it.
- **Retrieving** — the API reads it back with
  `encode(image_data, 'base64')` and prefixes the MIME type to build a ready-to-use
  `data:<mime>;base64,<…>` URI, so the gallery can drop it straight into an `<img src>`.

## Database

`issue_reports` columns:

| column | type | notes |
|--------|------|-------|
| `id` | `SERIAL` | primary key |
| `reporter_name` | `TEXT` | from the form **Name** field |
| `issue_summary` | `TEXT` | from **Issue Summary** |
| `report_date` | `DATE` | from **Date** |
| `image_filename` | `TEXT` | original upload filename |
| `image_mimetype` | `TEXT` | e.g. `image/png` |
| `image_data` | `BYTEA` | the image bytes |
| `created_at` | `TIMESTAMPTZ` | defaults to `now()` |

## Troubleshooting

- **Gallery says "Failed to load"** — make sure the *Reports API* workflow is **active**, the
  URL ends in `/webhook/issue-reports`, and CORS is allowed (the webhook node sets
  `Access-Control-Allow-Origin: *`).
- **Insert fails on the image** — confirm the form file field is labelled exactly **Image**
  (the submission query references `binary['Image']`). If you rename it, update the
  *Insert Issue Report* node's `queryReplacement`.
- **No image shows but the row exists** — the upload may have been empty; `image_data` is
  nullable and the gallery shows "No image" in that case.
