# Agentic AI Automation with n8n

Official courseware and hands-on lab materials for the 3-day WSQ course on building agentic AI automations with n8n — from a first form-to-email workflow to AI agents, webhooks, APIs, RAG chatbots and guarded, human-in-the-loop workflows.

| Course detail | Information |
|---|---|
| Course code | `TGS-2023035977` |
| Programme | WSQ |
| Duration | 3 days (24 hours) |
| Registration | [View course details and register](https://www.tertiarycourses.com.sg/wsq-agentic-ai-automation-with-n8n.html) |
| Funding | Up to 70% WSQ course fee funding (50% baseline for Singapore Citizens and PRs aged 21+; up to 70% for Singapore Citizens aged 40+ under MCES or SME-sponsored employees). Eligibility and terms apply. |

## About the course

Agentic AI moves AI from answering questions to doing work. This course teaches the **workflow-first** approach: the workflow owns the path, and AI and AI Agent nodes sit inside it where judgement is needed. You start with why agentic AI matters — the history of AI from 2023 to 2026, agentic AI vs AI agents, workflow first vs agent first, and AI security — and then build in [n8n](https://n8n.io) every day, using **n8n Assistant** to draft workflows from plain-English prompts and the free n8n **Gateway credits** for AI models.

Every topic ends in a lab you build and test yourself. On Day 3 you design and build a mini capstone with n8n Assistant and present it.

## Learning outcomes

By the end of the course you will be able to:

1. Build automated workflows in n8n using triggers, actions, nodes and flows.
2. Design AI agents with LLMs, memory and tools, triggered from chat or Telegram.
3. Apply Retrieval-Augmented Generation (RAG) to ground agents in your own documents.
4. Integrate external systems through webhooks, APIs and HTTP requests.
5. Apply human-in-the-loop approval and guardrails to secure agentic automations.

## Topics covered

1. **Workflow Automation with n8n** — why agentic AI, workflow first vs agent first, AI security principles, what n8n is, n8n training accounts, free AI credits, n8n Assistant, triggers, data-processing nodes, JSON and expressions, executions, credentials.
2. **AI Agents** — the model, memory, tools and instructions of an agent; model parameters; good vs bad instructions; MCP.
3. **Webhooks** — the inbound URL, GET vs POST, Test vs Production URL, responding to the caller.
4. **APIs and the HTTP Request Node** — request anatomy, status codes, API keys.
5. **Retrieval-Augmented Generation (RAG)** — chunking, embeddings, vector stores, grounding against hallucination.
6. **Security, Human-in-the-Loop and Guardrails** — where the human belongs, approval gates, input and output guardrails.
7. **Mini Capstone Project** — describe a business process to n8n Assistant, review and test what it builds, add a control, present.

## Labs

Each activity folder holds the importable n8n workflow (`.json`), a screenshot of the finished workflow and any data or web page the lab needs. Click-by-click steps are in the [Learner Guide](LEARNER-GUIDE.md).

| Activity | What you build |
|---|---|
| [Activity 1 — Flyer with QR Code](labs/activity1-flyer-form/) | An n8n Form that emails each sign-up to an admin, published as a QR code on an event flyer. |
| [Activity 2 — Data Table](labs/activity2-data-table/) | The same form, now saving every submission to an n8n Data Table. |
| [Activity 3a / 3b — Conditional Response](labs/activity3-conditional/) | IF-node routing to a Data Table (3a) or Google Sheets (3b), with a thank-you email on the other branch. |
| [Activity 4a / 4b — Telegram HR Agent](labs/activity4-telegram-agent/) | Ava, an HR policy chatbot on Telegram built with n8n Assistant from one prompt (4a), then given an Employees Data Table tool (4b). |
| [Activity 5 — Website Chatbot via Webhook](labs/activity5-investment-advisor/) | An Investment Advisor website whose enquiry form and chat widget both call one n8n webhook. |
| [Activity 6 — Finance APIs → Telegram](labs/activity6-finance-advisor/) | A day-trading agent that pulls Twelve Data candles and NewsAPI headlines and argues a Buy / Sell / Hold call. |
| [Activity 7a / 7b — RAG](labs/activity7-rag/) | A PDF-grounded Telegram bot (7a), and a Cook & Bake Academy support chatbot grounded in 20 brochures in a vector database (7b). |
| [Activity 8a / 8b / 8c — HR Service Portal](labs/activity8-guardrails/) | Human-in-the-loop leave approval, a GET-webhook dashboard, and an AI chatbot with input and output guardrails. |
| [Mini Capstone](labs/mini-capstone/) | Your own end-to-end workflow built with n8n Assistant, plus a worked Issue Reporting example. |
| [n8n installation](labs/n8n-installation/) | Docker Compose file to self-host n8n after the course. |

## Courseware package

| File | Format |
|---|---|
| Slide deck — v48 | [PowerPoint](courseware/Agentic%20AI%20Automation%20with%20n8n-v48.pptx) · [PDF](courseware/Agentic%20AI%20Automation%20with%20n8n-v48.pdf) |
| Learner Guide — v6.5 | [Word](courseware/LG-Agentic%20AI%20Automation%20with%20n8n.docx) · [PDF](courseware/LG-Agentic%20AI%20Automation%20with%20n8n.pdf) · [Markdown](LEARNER-GUIDE.md) |
| Lesson Plan — v3.2 | [Word](courseware/LP-Agentic%20AI%20Automation%20with%20n8n.docx) · [PDF](courseware/LP-Agentic%20AI%20Automation%20with%20n8n.pdf) |
| Facilitator Guide — v5.0 | [Word](courseware/FG_TGS-2023035977_Agentic%20AI%20Automation%20with%20n8n_v5.docx) · [PDF](courseware/FG_TGS-2023035977_Agentic%20AI%20Automation%20with%20n8n_v5.pdf) |

**Using the workflows:** in n8n, create a new workflow, open the **⋯** menu → **Import from File**, pick the activity `.json`, then re-select your own credentials on each node (imported workflows carry credential names, never secrets). For AI nodes, choose **Use Gateway credits** on n8n Cloud, or your own OpenAI / Gemini key.

## What is public and what is not

This repository is public. It contains the slides, Learner Guide, Lesson Plan, Facilitator Guide, lab workflows, lab data and web pages, and the scripts that build the courseware.

It does **not** contain the WSQ assessment (written assessment and practical performance papers and their answer keys), the Assessment Plan (which reproduces them with the marking rubric), source reference material, superseded courseware versions, or any credentials. Training-account passwords and API keys are given in class and are never committed.

## Provider

Developed and delivered by **Tertiary Infotech Academy Pte Ltd** (UEN 201200696W) — [Tertiary Courses Singapore](https://www.tertiarycourses.com.sg).

© 2026 Tertiary Infotech Academy Pte Ltd. Provided for educational use as part of WSQ course TGS-2023035977.
