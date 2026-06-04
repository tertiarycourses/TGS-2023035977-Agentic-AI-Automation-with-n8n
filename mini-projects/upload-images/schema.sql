-- ============================================================
-- Issue Reporting flow — Postgres schema
-- Run this once before activating the n8n workflows.
--
--   psql -h localhost -U <user> -d <database> -f schema.sql
--
-- The image is stored as a BYTEA column (raw binary). The
-- submission workflow base64-encodes the uploaded file and
-- inserts it with decode($6, 'base64'); the retrieval workflow
-- reads it back with encode(image_data, 'base64').
-- ============================================================

CREATE TABLE IF NOT EXISTS issue_reports (
    id              SERIAL       PRIMARY KEY,
    reporter_name   TEXT         NOT NULL,
    issue_summary   TEXT         NOT NULL,
    report_date     DATE         NOT NULL,
    image_filename  TEXT,
    image_mimetype  TEXT,
    image_data      BYTEA,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Fast "most recent first" listing for the gallery.
CREATE INDEX IF NOT EXISTS idx_issue_reports_created_at
    ON issue_reports (created_at DESC);

-- ------------------------------------------------------------
-- Handy queries
-- ------------------------------------------------------------

-- List reports without dumping the (large) binary image:
--   SELECT id, reporter_name, report_date, image_filename, created_at
--   FROM issue_reports
--   ORDER BY created_at DESC;

-- Pull one image back out as base64 (what the retrieval flow does):
--   SELECT image_mimetype, encode(image_data, 'base64') AS image_b64
--   FROM issue_reports
--   WHERE id = 1;
