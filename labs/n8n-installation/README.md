# Installing n8n Locally (Docker Compose)

A quick guide to self-hosting n8n on your own machine for the labs, and exposing it
to the internet with **ngrok** so that **webhooks** and the **Telegram** trigger work.

---

## 1. Prerequisites

- **Docker Desktop** — install from <https://www.docker.com/products/docker-desktop/> and make sure it is running.
- A terminal opened in this folder (`labs/n8n-installation/`).

---

## 2. Start n8n

```bash
docker compose up -d
```

- `-d` runs it in the background.
- Open **http://localhost:5678** and create your **owner account** (first run only).
- Your workflows and credentials are saved in the `n8n_data` Docker volume, so they
  survive restarts and upgrades.

| Task | Command |
|------|---------|
| View logs | `docker compose logs -f` |
| Stop (keep data) | `docker compose down` |
| Update to latest | `docker compose pull` then `docker compose up -d` |
| Reset everything | `docker compose down -v` *(⚠️ deletes the `n8n_data` volume)* |

### What the compose file sets

- `N8N_SECURE_COOKIE=false` — lets you log in over plain `http://localhost` (no HTTPS locally).
- `GENERIC_TIMEZONE=Asia/Singapore` — schedules and timestamps use Singapore time.
- `n8n_data` volume — persistent storage for your workflows/credentials.

---

## 3. Expose n8n to the internet with ngrok

Webhooks (Activity 6) and the Telegram trigger (Activities 4, 5, 7) need a **public HTTPS
URL** that external services can call. `localhost:5678` is not reachable from the internet,
so we tunnel it with **ngrok**.

### 3.1 Install & authenticate ngrok

1. Sign up (free) at <https://dashboard.ngrok.com/signup> and copy your **authtoken**.
2. Install ngrok (macOS): `brew install ngrok` — or download from <https://ngrok.com/download>.
3. Register your token once:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

### 3.2 Start the tunnel

```bash
ngrok http 5678
```

ngrok prints a public URL, e.g.:

```
Forwarding   https://1a2b-3c4d.ngrok-free.app -> http://localhost:5678
```

Copy that **https** URL — that is your public n8n address.

> Keep the ngrok terminal open while you work. On the free plan the URL **changes every
> time you restart ngrok**, so you'll repeat step 4 whenever it changes.

---

## 4. Point n8n at the public URL (`WEBHOOK_URL`)

By default n8n builds webhook and Telegram URLs from `localhost`, which the outside world
cannot reach. Tell n8n its public address by setting **`WEBHOOK_URL`** (and the matching
host/protocol) in `docker-compose.yml`.

1. Open `docker-compose.yml` and **uncomment** these lines under `environment:`, replacing
   the placeholder with your current ngrok URL:

   ```yaml
       - WEBHOOK_URL=https://1a2b-3c4d.ngrok-free.app/
       - N8N_HOST=1a2b-3c4d.ngrok-free.app
       - N8N_PROTOCOL=https
   ```

   - `WEBHOOK_URL` — the public base URL n8n uses to generate **Production** webhook URLs (include the trailing `/`, no path).
   - `N8N_HOST` — the hostname only (no `https://`, no `/`).
   - `N8N_PROTOCOL=https` — because ngrok terminates HTTPS.

2. Recreate the container so the new env is applied:

   ```bash
   docker compose up -d
   ```

3. In any **Webhook** node, the **Production URL** now shows your ngrok address, e.g.
   `https://1a2b-3c4d.ngrok-free.app/webhook/...`. Use that URL in your website page or
   give it to Telegram/BotFather.

> **CORS:** for browser pages calling a webhook (Activity 6), set the Webhook node's
> **Options → Allowed Origins (CORS)** to `*`.

### When the ngrok URL changes

Each new `ngrok http 5678` gives a new URL. Update the three values above and run
`docker compose up -d` again. (A reserved **ngrok static domain** — free tier allows one —
avoids this; pass it with `ngrok http --domain=your-name.ngrok-free.app 5678` and set that
domain as `WEBHOOK_URL`/`N8N_HOST`.)

---

## 5. Quick checklist

- [ ] `docker compose up -d` → http://localhost:5678 loads and you can log in.
- [ ] `ngrok http 5678` is running and shows an `https://…ngrok-free.app` URL.
- [ ] `WEBHOOK_URL`, `N8N_HOST`, `N8N_PROTOCOL` set in `docker-compose.yml` and re-applied.
- [ ] A Webhook node's **Production URL** uses the ngrok address.
- [ ] Telegram bot / website points at that public URL.

---

<sub>Part of the WSQ course **Agentic AI Automation with n8n** (TGS-2023035977) · © 2026 Tertiary Infotech Academy Pte Ltd · www.tertiarycourses.com.sg</sub>
