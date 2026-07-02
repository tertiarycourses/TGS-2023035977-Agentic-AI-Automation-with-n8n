<div align="center">

# Agentic AI Automation with n8n

[![Course](https://img.shields.io/badge/WSQ_Course-TGS--2023035977-1f6feb?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-agentic-ai-automation-with-n8n.html)
[![n8n](https://img.shields.io/badge/Built_with-n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![OpenAI](https://img.shields.io/badge/LLM-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com)
[![RAG](https://img.shields.io/badge/Pattern-RAG-34d399?style=for-the-badge)](#activity-7a--7b--retrieval-augmented-generation-rag)
[![License](https://img.shields.io/badge/License-Educational-fbbf24?style=for-the-badge)](#license)

**Hands-on lab workflows and web apps for building agentic AI automations with n8n — from form-to-email flows to a Retrieval-Augmented Generation (RAG) chatbot grounded in your own documents.**

[📘 Course Page](https://www.tertiarycourses.com.sg/wsq-agentic-ai-automation-with-n8n.html) · [📖 Step-by-Step Guide](LEARNER-GUIDE.md) · [🐛 Report Bug](https://github.com/tertiarycourses/TGS-2023035977-Agentic-AI-Automation-with-n8n/issues) · [💡 Request Feature](https://github.com/tertiarycourses/TGS-2023035977-Agentic-AI-Automation-with-n8n/issues)

![Cook & Bake Academy — RAG customer-support chatbot (Activity 7b)](screenshot.png)

</div>

> [!NOTE]
> **These are the official hands-on lab materials for the WSQ course:**
> ### 🎓 WSQ — Agentic AI Automation with n8n
> **Course Code:** `TGS-2023035977` · by Tertiary Courses / Tertiary Infotech
> **Course page:** https://www.tertiarycourses.com.sg/wsq-agentic-ai-automation-with-n8n.html

---

## Lab Activities

**Activity 1 — Flyer with QR Code** · Form Trigger → Gmail + a QR code on an event flyer.
![Activity 1](labs/activity1-flyer-form/Activity1-Flyer-Form.png)

**Activity 2 — Capture Submissions in a Data Table** · Every form submission saved to an n8n Data Table alongside the email.
![Activity 2](labs/activity2-data-table/Activity2-Data-Table.png)

**Activity 3 — Conditional Response** · IF-node routing: "Yes" saves to a Data Table (3a) / Google Sheets (3b); "No" sends a thank-you email.
![Activity 3](labs/activity3-conditional/Activity3a-Conditional-Data-Table.png)

**Activity 4 — Telegram AI Agent** · Telegram-triggered AI agent with memory (4a) + a Data Table tool for HR lookups (4b).
![Activity 4](labs/activity4-telegram-agent/Activity4a-Telegram-Agent.png)

**Activity 5 — Website Chatbot via Webhook (Investment Advisor)** · A public landing page with an enquiry form and a floating AI chatbot, both wired to one n8n webhook.
![Activity 5](labs/activity5-investment-advisor/Activity5-website.png)

**Activity 6 — Finance API → Telegram (AI Day Trader)** · Pulls Twelve Data candles + NewsAPI headlines, then replies with a Buy/Sell/Hold call. A live dashboard shows the chart and quote stats.
![Activity 6](labs/activity6-finance-advisor/Activity6-website.png)

### Activity 7a & 7b — Retrieval-Augmented Generation (RAG)

**Activity 7a — RAG Chatbot: Upload a PDF, Ask in Telegram** · A web page extracts text from a PDF (an IT-Support FAQ) and uploads it to n8n, which embeds it into an in-memory vector store with Google Gemini. A Telegram bot then answers **only** from that document.
![Activity 7a](labs/activity7-rag/Activity7a-RAG-Telegram.png)

**Activity 7b — Customer-Support RAG Agent (Cook & Bake Academy)** · Ingest 20 course brochures from Google Drive into a **vector database**, then a CX Agent answers website-chat questions about course duration, fees, and schedule — grounded in the brochures. Shown across **three** vector stores: **Supabase (pgvector)**, **Pinecone**, and **Qdrant**.
![Activity 7b](labs/activity7-rag/Activity7b-CX-Agent.png)

**Activity 8 — HR Service Portal (Security & Guardrails)** · One portal backed by three workflows: human-in-the-loop leave approval (8a), a live leave-balance dashboard (8b), and an AI chatbot wrapped in input/output guardrails (8c).
![Activity 8](labs/activity8-guardrails/Activity8-website.png)

---

## About

This repository contains the complete, working lab materials for the **WSQ Agentic AI Automation with n8n** course (**TGS-2023035977**) by Tertiary Courses / Tertiary Infotech. Each activity is a self-contained, importable [n8n](https://n8n.io) workflow — several paired with a polished HTML front end — that builds progressively from basic automation to a full **Retrieval-Augmented Generation (RAG)** agent grounded in a vector database.

### What you'll learn

| # | Activity | Concepts |
|---|----------|----------|
| **1** | **Flyer with QR Code** | Form Trigger → Gmail, expressions, QR-code generation |
| **2** | **Capture Data in a Data Table** | n8n Data Tables, storing submissions |
| **3a / 3b** | **Conditional Response** | IF-node branching → Data Table (3a) / Google Sheets persistence (3b) |
| **4a / 4b** | **Telegram AI Agent** | Telegram Trigger, AI Agent, memory, Data Table tool |
| **5** | **Website Chatbot (Investment Advisor)** | Webhook trigger, CORS, `Respond to Webhook`, branded front end |
| **6** | **Finance API → Telegram (Day Trader)** | HTTP Request, Twelve Data + NewsAPI, multi-timeframe analysis |
| **7a** | **RAG Chatbot (PDF → Telegram)** | PDF upload, embeddings (Gemini), in-memory vector store, retrieve-as-tool |
| **7b** | **Customer-Support RAG Agent** | Google Drive ingestion, vector databases — Supabase, Pinecone (Gemini embeddings), Qdrant |
| **8a / 8b / 8c** | **HR Service Portal (Guardrails)** | Human-in-the-loop approval, live dashboard, pre/post LLM guardrails |
| **Capstone** | **Mini Capstone** | End-to-end build (Issue Reporting: form + image → Postgres + gallery) |

> 📖 **Full walkthrough:** see **[LEARNER-GUIDE.md](LEARNER-GUIDE.md)** for detailed, click-by-click instructions (with workflow diagrams) for every activity. Slides, the Learner Guide and the Lesson Plan are in [`courseware/`](courseware/).

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Automation Platform** | [n8n](https://n8n.io) (cloud trial or local Docker; workflows, triggers, Data Tables) |
| **LLM** | OpenAI (chat + `text-embedding-3-small`) and Google Gemini (chat + `gemini-embedding-001`) |
| **Agent Framework** | n8n LangChain nodes (AI Agent, Memory, Vector Store, Tools) |
| **Vector Databases** | In-memory store · Supabase (pgvector) · Pinecone · Qdrant |
| **Chat / Messaging** | Telegram (Bot trigger + send) |
| **APIs & Data** | Twelve Data + NewsAPI (HTTP Request), Google Drive |
| **Email / Storage** | Gmail (OAuth2), Google Sheets |
| **Front End** | Vanilla HTML / CSS / JavaScript (no build step), PDF.js |
| **Courseware** | Slides (`python-pptx`), Learner Guide + Lesson Plan (`python-docx`) |

---

## Architecture

```
DAY 1 — Workflow Automation + AI Agents
  Act 1  Form Trigger ─▶ Gmail                         (flyer + QR code)
  Act 2  Form Trigger ─▶ Gmail + Data Table            (capture data)
  Act 3a Form ─▶ IF ─▶ Data Table / Gmail              (conditional)
  Act 3b Form ─▶ IF ─▶ Google Sheets / Gmail           (persistent)
  Act 4a Telegram ─▶ AI Agent (+ memory) ─▶ reply
  Act 4b Telegram ─▶ AI Agent + Data Table tool ─▶ reply

DAY 2 — Webhooks · APIs · RAG
  Act 5  Website ─▶ Webhook ─▶ AI Agent ─▶ Respond      (Investment Advisor)
  Act 6  Telegram ─▶ HTTP (Twelve Data + NewsAPI) ─▶ AI Agent ─▶ reply  (Day Trader)
  Act 7a Web upload ─▶ Embeddings (Gemini) ─▶ Vector Store │ Telegram ─▶ Agent + knowledge_base ─▶ reply
  Act 7b Drive ─▶ split ─▶ Embeddings (OpenAI / Gemini) ─▶ Supabase / Pinecone / Qdrant │ Website ─▶ Webhook ─▶ CX Agent ─▶ reply

DAY 3 — Security & Guardrails + Capstone
  Act 8a Form ─▶ Manager Approval (Send & Wait) ─▶ IF ─▶ confirm / decline
  Act 8b Webhook ─▶ Code ─▶ Respond JSON (leave dashboard)
  Act 8c Webhook ─▶ Input guardrail ─▶ AI Agent ─▶ Output guardrail ─▶ Respond / Blocked
  Capstone  Issue Reporting: Form + image ─▶ Postgres + retrieval API + gallery
```

---

## Project Structure

```
TGS-2023035977-Agentic-AI-Automation-with-n8n/
├── LEARNER-GUIDE.md                  # Full step-by-step lab guide (start here)
├── README.md
├── screenshot.png                    # Cook & Bake Academy RAG site (Activity 7b)
│
├── labs/                             # All hands-on lab activities (one folder each)
│   ├── n8n-installation/             # Docker Compose for self-hosting n8n
│   ├── activity1-flyer-form/         # Act 1: Form → Gmail (+ flyer samples)
│   ├── activity2-data-table/         # Act 2: + Data Table
│   ├── activity3-conditional/        # Act 3a/3b: IF → Data Table / Google Sheets
│   ├── activity4-telegram-agent/     # Act 4a/4b: Telegram AI agent
│   ├── activity5-investment-advisor/ # Act 5: Webhook website chatbot (HTML app)
│   ├── activity6-finance-advisor/    # Act 6: Finance API → Telegram (HTML dashboard)
│   ├── activity7-rag/                # Act 7a/7b: RAG — PDF→Telegram + vector-DB CX agent
│   │   ├── Activity7a-RAG-Telegram.json   · Activity7a-upload.html · it-faq.pdf
│   │   ├── Activity7b-{Supabase,Pinecone,Qdrant}-Upload.json · Activity7b-CX-Agent.json
│   │   ├── brochures/                # 20 mock course brochures (.txt)
│   │   └── website/                  # Cook & Bake Academy site + RAG chat widget
│   ├── activity8-guardrails/         # Act 8a/8b/8c: HR Service Portal + guardrails
│   └── mini-capstone/issue-tracking/ # Capstone: Form + image → Postgres + gallery
│
└── courseware/                       # Course slides, Lesson Plan + Learner Guide
    ├── Agentic AI Automation with n8n-v43.pptx   # 3-day slide deck (+ PDF)
    ├── LG-Agentic AI Automation with n8n.docx    # detailed step-by-step (+ PDF)
    └── LP-Agentic AI Automation with n8n.docx    # 3-day lesson plan (+ PDF)
```

---

## Getting Started

### Prerequisites
- An [**n8n**](https://n8n.io) account (Cloud or self-hosted via [`labs/n8n-installation/`](labs/n8n-installation/))
- An [**OpenAI API key**](https://platform.openai.com/api-keys) and/or a [**Google Gemini key**](https://aistudio.google.com/) (embeddings + chat)
- A **Telegram bot token** (from [@BotFather](https://t.me/BotFather))
- A **Gmail** account (Activity 1 email / Activity 8 approvals)
- *(Activity 6)* free [Twelve Data](https://twelvedata.com) + [NewsAPI](https://newsapi.org) keys
- *(Activity 7b)* one vector database — [Supabase](https://supabase.com), [Pinecone](https://pinecone.io) or [Qdrant](https://qdrant.io)

### 1. Clone the repo
```bash
git clone https://github.com/tertiarycourses/TGS-2023035977-Agentic-AI-Automation-with-n8n.git
cd TGS-2023035977-Agentic-AI-Automation-with-n8n
```

### 2. Import a workflow into n8n
1. In n8n: **Workflows → Add workflow → ⋯ → Import from File**.
2. Pick a `.json` from the matching `labs/activity*/` folder.
3. Re-select **your own credentials** on each node — imported credential IDs won't match yours.
4. **Save**, then toggle **Active / Published**.

### 3. Run the web apps (Activities 5, 6, 7 & 8)
The pages are pure static HTML — just open them, or serve locally:
```bash
cd labs/activity7-rag/website
python3 -m http.server 8000
# then open http://localhost:8000/index.html
```
- Set the webhook / production URL in the page (gear icon or `script.js`).
- **Activity 7a:** open `Activity7a-upload.html`, paste the `rag-upload` webhook URL, drop `it-faq.pdf`, then chat with your Telegram bot.
- **Activity 7b:** follow [`labs/activity7-rag/LEARNER-GUIDE-7b.md`](labs/activity7-rag/LEARNER-GUIDE-7b.md) to ingest the brochures into Supabase / Pinecone / Qdrant.

> ⚠️ **CORS:** each n8n Webhook node must have **Options → Allowed Origins (CORS) = `*`** so the browser page can call it. All workflow exports in this repo already include this.

For complete, click-by-click setup, see **[LEARNER-GUIDE.md](LEARNER-GUIDE.md)**.

---

## Contributing

Contributions, fixes, and improvements are welcome:

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Commit your changes: `git commit -m "Add my improvement"`
4. Push the branch: `git push origin feature/my-improvement`
5. Open a **Pull Request**

Found a bug or have an idea? Open an [issue](https://github.com/tertiarycourses/TGS-2023035977-Agentic-AI-Automation-with-n8n/issues).

---

## License

This material is provided for **educational use** as part of the WSQ course **TGS-2023035977**. © Tertiary Infotech Pte. Ltd. All rights reserved.

---

## Developed By

**Tertiary Infotech Pte. Ltd.** — [Tertiary Courses](https://www.tertiarycourses.com.sg)
Course: [WSQ Agentic AI Automation with n8n (TGS-2023035977)](https://www.tertiarycourses.com.sg/wsq-agentic-ai-automation-with-n8n.html)

## Acknowledgements

- [n8n](https://n8n.io) — the workflow automation platform
- [OpenAI](https://openai.com) & [Google Gemini](https://aistudio.google.com/) — chat & embedding models
- [Supabase](https://supabase.com), [Pinecone](https://pinecone.io), [Qdrant](https://qdrant.io) — vector databases
- Course trainers and learners of TGS-2023035977

---

<div align="center">

⭐ **If this helped you learn agentic automation, star the repo!**

Powered by [Tertiary Infotech Academy Pte Ltd](https://www.tertiaryinfotech.com/)

[📘 Course Page](https://www.tertiarycourses.com.sg/wsq-agentic-ai-automation-with-n8n.html) · [📖 Step-by-Step Guide](LEARNER-GUIDE.md)

</div>
