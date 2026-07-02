#!/usr/bin/env python3
"""Push WSQ courseware to the user's Google Drive courseware folder, archiving old versions.

Usage:  python3 gdrive_push.py <drive-folder-link-or-id> [--repo DIR] [--dry-run]

Routing (folders matched case-insensitively under the given root; created if missing):
  Master Trainer Slides : slides .pptx + .pdf
  Learner Guide         : LG .docx + .pdf, plus the slides .pdf
  Lesson Plan           : LP .docx + .pdf
  Assessment            : all assessment .docx (question papers + answer keys)

Before each upload, any existing Drive file of the same "family" (same base name
ignoring the -vNN / vN version suffix, same extension) is MOVED to an "Archive"
subfolder inside that folder — nothing is ever deleted.

Transport: a local n8n webhook proxy (workflow "GDrive Courseware Push (proxy)",
path /gdrive-ops) that signs Google Drive REST calls with the n8n "Google Drive
account" OAuth2 credential. See setup_proxy.py to (re)create it.
"""
import glob
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import uuid

PROXY = os.environ.get("GDRIVE_PROXY_URL", "http://localhost:5678/webhook/gdrive-ops")
API = "https://www.googleapis.com/drive/v3"
COMMON = "supportsAllDrives=true"


def multipart(fields, file_field=None, file_path=None):
    boundary = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    if file_field and file_path:
        fn = os.path.basename(file_path)
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; "
                 f"filename=\"{fn}\"\r\nContent-Type: application/octet-stream\r\n\r\n").encode()
        body += open(file_path, "rb").read() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def drive(op, url, payload=None, file_path=None):
    fields = {"op": op, "url": url}
    if payload is not None:
        fields["payload"] = json.dumps(payload)
    body, ctype = multipart(fields, "file" if file_path else None, file_path)
    req = urllib.request.Request(PROXY, data=body, headers={"Content-Type": ctype}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw = r.read().decode()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Drive proxy error ({op} {url}): HTTP {e.code} {e.read().decode()[:400]}")
    if not raw.strip():
        raise SystemExit(
            "Empty response from the n8n Drive proxy — the Google Drive call failed inside n8n.\n"
            "Most likely cause: the n8n 'Google Drive account' credential has not completed OAuth.\n"
            "Fix: open n8n (http://localhost:5678) -> Credentials -> 'Google Drive account' -> "
            "'Sign in with Google', then re-run this push.\n"
            "Otherwise check n8n -> Executions for the failed 'GDrive Courseware Push (proxy)' run.")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit(f"Drive proxy returned non-JSON ({op}): {raw[:400]}")


def q(query):
    return urllib.parse.quote(query, safe="")


def list_children(folder_id, extra=""):
    query = f"'{folder_id}' in parents and trashed=false{extra}"
    url = (f"{API}/files?q={q(query)}&fields=files(id,name,mimeType)&pageSize=1000"
           f"&{COMMON}&includeItemsFromAllDrives=true")
    return drive("get", url).get("files", [])


def ensure_folder(name, parent_id, match_hint=None):
    hint = (match_hint or name).lower()
    for f in list_children(parent_id, " and mimeType='application/vnd.google-apps.folder'"):
        if hint in f["name"].strip().lower():
            return f["id"], f["name"], False
    made = drive("post", f"{API}/files?{COMMON}", payload={
        "name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]})
    return made["id"], name, True


def family_prefix(filename):
    stem, _ = os.path.splitext(filename)
    m = re.match(r"^(.*?)\s*[-–]?\s*v\d+\s*$", stem, re.IGNORECASE)
    return (m.group(1).rstrip(" -–") if m else stem).lower()


def archive_old(folder_id, folder_name, archive_id, new_filename, dry):
    prefix = family_prefix(new_filename)
    ext = os.path.splitext(new_filename)[1].lower()
    moved = []
    for f in list_children(folder_id, " and mimeType!='application/vnd.google-apps.folder'"):
        name = f["name"]
        if not name.lower().endswith(ext):
            continue
        if not family_prefix(name).startswith(prefix):
            continue
        moved.append(name)
        if dry:
            continue
        cur = drive("get", f"{API}/files/{f['id']}?fields=parents&{COMMON}")
        parents = ",".join(cur.get("parents", [folder_id]))
        drive("patch", f"{API}/files/{f['id']}?addParents={archive_id}&removeParents={parents}&{COMMON}")
    for name in moved:
        print(f"    archived: {name}  ->  {folder_name}/Archive/")
    return moved


def upload(path, folder_id, dry):
    fn = os.path.basename(path)
    if dry:
        print(f"    would upload: {fn}")
        return
    created = drive("upload", f"https://www.googleapis.com/upload/drive/v3/files?uploadType=media&{COMMON}",
                    file_path=path)
    fid = created.get("id") or SystemExit(f"upload failed: {created}")
    cur = drive("get", f"{API}/files/{fid}?fields=parents&{COMMON}")
    parents = ",".join(cur.get("parents", []))
    drive("patch", f"{API}/files/{fid}?addParents={folder_id}&removeParents={parents}&{COMMON}",
          payload={"name": fn})
    print(f"    uploaded: {fn}")


def newest(pattern):
    hits = sorted(glob.glob(pattern), key=os.path.getmtime)
    return hits[-1] if hits else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    repo = "."
    if "--repo" in sys.argv:
        repo = sys.argv[sys.argv.index("--repo") + 1]
    if not args:
        raise SystemExit("Usage: gdrive_push.py <drive-folder-link-or-id> [--repo DIR] [--dry-run]\n"
                         "The Google Drive courseware folder link MUST be supplied by the user.")
    m = re.search(r"folders/([A-Za-z0-9_-]{10,})", args[0])
    root = m.group(1) if m else args[0]

    cw = os.path.join(repo, "courseware")
    deck_ppt = newest(os.path.join(cw, "*-v*.pptx"))
    if not deck_ppt:
        raise SystemExit(f"No versioned slide deck found in {cw}")
    deck_pdf = os.path.splitext(deck_ppt)[0] + ".pdf"
    lg_docx = newest(os.path.join(cw, "LG-*.docx")); lg_pdf = newest(os.path.join(cw, "LG-*.pdf"))
    lp_docx = newest(os.path.join(cw, "LP-*.docx")); lp_pdf = newest(os.path.join(cw, "LP-*.pdf"))
    assessments = sorted(glob.glob(os.path.join(repo, "assessment", "*.docx")))

    routing = [
        ("Master Trainer Slides", "master trainer", [deck_ppt, deck_pdf]),
        ("Learner Guide", "learner guide", [lg_docx, lg_pdf, deck_pdf]),
        ("Lesson Plan", "lesson plan", [lp_docx, lp_pdf]),
        ("Assessment", "assess", assessments),
    ]
    print(f"Root folder: {root}{'  (DRY RUN)' if dry else ''}")
    for canonical, hint, files in routing:
        files = [f for f in files if f and os.path.exists(f)]
        if not files:
            print(f"  {canonical}: no local files found — skipped"); continue
        fid, real_name, created = ensure_folder(canonical, root, hint)
        aid, _, _ = ensure_folder("Archive", fid, "archiv")
        print(f"  {real_name}{' (created)' if created else ''}:")
        for path in files:
            archive_old(fid, real_name, aid, os.path.basename(path), dry)
            upload(path, fid, dry)
    print("Done." if not dry else "Dry run complete — nothing was modified.")


if __name__ == "__main__":
    main()
