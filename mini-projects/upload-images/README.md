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
| [index.html](index.html) | Landing page — paste your form URL to **generate a QR code in the browser**, with buttons to the form and gallery. |
| [gallery.html](gallery.html) | A standalone page that calls the API and shows the reports in a grid with a lightbox. |

---

## Setup

> This project uses **Supabase** (hosted Postgres) so it works with **n8n Cloud** as well as
> self-hosted n8n. Any Postgres database works — just point the credential at it.

### 1. Create a Supabase project + the table

1. Create a free project at [supabase.com](https://supabase.com).
2. Open **SQL Editor**, paste the contents of [schema.sql](schema.sql), and click **Run**.
   This creates the `issue_reports` table (with the `image_data BYTEA` column).
3. Grab your connection details from **Project Settings ▸ Database ▸ Connection info**:
   `Host`, `Port` (`5432`), `Database` (`postgres`), `User` (`postgres`), and your password.

### 2. Add the Postgres (Supabase) credential in n8n

**Credentials ▸ Add credential ▸ Postgres**, then enter the Supabase values:

| Field | Value |
|-------|-------|
| **Host** | `db.<your-ref>.supabase.co` |
| **Database** | `postgres` |
| **User** | `postgres` |
| **Password** | your Supabase DB password |
| **Port** | `5432` |
| **SSL** | `require` ← **Supabase requires SSL** |

Click **Save** — n8n tests the connection (green tick = good).

### 3. Import the workflows into n8n

In n8n: **Workflows ▸ Import from File** for each of:

- `upload-image-postgressql.json`
- `issue-reports-api.json`

Both ship with a credential reference named **"Supabase Postgres"**. Open each Postgres node and
**select the credential you created in step 2** (the imported credential ID won't match yours).

### 4. Activate

- Open **Issue Reporting - Submit to Postgres** → click the **form trigger** node → copy the
  **Production URL** (e.g. `https://YOUR-N8N/form/<id>`). **Activate** the workflow.
- Open **Issue Reporting - Reports API** → **Activate** it. Its production URL is
  `https://YOUR-N8N/webhook/issue-reports`.

---

## Usage

### Share the form with a QR code
Open [index.html](index.html), paste your form's **Production URL** into the box, and click
**Generate** — a QR code is created right in the browser. The **Open the Form** button and the
URL update to match, and **Download QR** saves a PNG for a printed flyer. (Needs an internet
connection on first open, as it loads the `qrcodejs` library from a CDN.)

### Submit an issue
Scan the QR (or open the form URL), fill in **Name**, **Issue Summary**, **Date**, attach an
**Image** (`.jpg/.png/.gif/.webp`), and submit. You'll see a confirmation with the new report number.

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
