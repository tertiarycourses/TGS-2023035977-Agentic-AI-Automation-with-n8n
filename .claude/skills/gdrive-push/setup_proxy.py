#!/usr/bin/env python3
"""(Re)create + activate the n8n 'GDrive Courseware Push (proxy)' workflow used by gdrive_push.py.

Usage: python3 setup_proxy.py <n8n-email> <n8n-password> [--host http://localhost:5678]

Requires an existing, SIGNED-IN 'Google Drive account' (googleDriveOAuth2Api) credential
in the n8n instance. The proxy exposes POST /webhook/gdrive-ops accepting multipart fields:
op=get|post|patch|upload, url=<Drive REST URL>, payload=<JSON string>, file=<binary>.
"""
import json, subprocess, sys, tempfile

host = "http://localhost:5678"
if "--host" in sys.argv:
    host = sys.argv[sys.argv.index("--host") + 1]
email, password = sys.argv[1], sys.argv[2]
cookies = tempfile.NamedTemporaryFile(suffix=".txt", delete=False).name

def curl(*extra, data=None):
    cmd = ["curl", "-s", "-b", cookies, "-c", cookies, *extra]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(data)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

login = json.loads(curl("-X", "POST", f"{host}/rest/login",
                        data={"emailOrLdapLoginId": email, "password": password}))
assert login.get("data", {}).get("id"), f"n8n login failed: {str(login)[:200]}"

creds = json.loads(curl(f"{host}/rest/credentials"))["data"]
drive_cred = next((c for c in creds if c["type"] == "googleDriveOAuth2Api"), None)
assert drive_cred, "No googleDriveOAuth2Api credential found in n8n — create & sign in first."
CRED = {"googleDriveOAuth2Api": {"id": drive_cred["id"], "name": drive_cred["name"]}}

def http(name, extra, x, y):
    p = {"url": "={{ $json.body.url }}", "authentication": "predefinedCredentialType",
         "nodeCredentialType": "googleDriveOAuth2Api", "options": {}}
    p.update(extra)
    return {"name": name, "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
            "position": [x, y], "parameters": p, "credentials": CRED}

nodes = [
  {"name": "Webhook", "type": "n8n-nodes-base.webhook", "typeVersion": 2.1, "position": [0, 0],
   "parameters": {"httpMethod": "POST", "path": "gdrive-ops", "responseMode": "responseNode", "options": {}}},
  {"name": "Route", "type": "n8n-nodes-base.switch", "typeVersion": 3.2, "position": [220, 0],
   "parameters": {"mode": "expression", "numberOutputs": 4,
                  "output": "={{ ['get','post','patch','upload'].indexOf($json.body.op) }}"}},
  http("GET", {"method": "GET"}, 460, -240),
  http("POST", {"method": "POST", "sendBody": True, "specifyBody": "json",
                "jsonBody": "={{ $json.body.payload }}"}, 460, -80),
  http("PATCH", {"method": "PATCH", "sendBody": True, "specifyBody": "json",
                 "jsonBody": "={{ $json.body.payload || '{}' }}"}, 460, 80),
  http("UPLOAD", {"method": "POST", "sendBody": True, "contentType": "binaryData",
                  "inputDataFieldName": "file"}, 460, 240),
  {"name": "Respond", "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1.5, "position": [700, 0],
   "parameters": {"respondWith": "firstIncomingItem", "options": {}}},
]
conn = {"Webhook": {"main": [[{"node": "Route", "type": "main", "index": 0}]]},
        "Route": {"main": [[{"node": n, "type": "main", "index": 0}] for n in ("GET", "POST", "PATCH", "UPLOAD")]}}
for n in ("GET", "POST", "PATCH", "UPLOAD"):
    conn[n] = {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}

existing = json.loads(curl(f"{host}/rest/workflows?filter=" + json.dumps({"name": "GDrive Courseware Push (proxy)"})))
wf = {"name": "GDrive Courseware Push (proxy)", "nodes": nodes, "connections": conn, "settings": {}}
made = json.loads(curl("-X", "POST", f"{host}/rest/workflows", data=wf))["data"]
wid, vid = made["id"], made["versionId"]
act = json.loads(curl("-X", "POST", f"{host}/rest/workflows/{wid}/activate", data={"versionId": vid}))
print("proxy workflow:", wid, "active:", act.get("data", {}).get("active"))
print("webhook:", f"{host}/webhook/gdrive-ops")
