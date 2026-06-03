# Agentic AI Automation with n8n — Step‑by‑Step Lab Guide

**Course Code:** TGS-2023035977
**Course page:** https://www.tertiarycourses.com.sg/wsq-agentic-ai-automation-with-n8n.html

This guide walks you through every hands‑on activity in the course. Each activity builds on the previous one, taking you from a simple form‑to‑email automation all the way to a Retrieval‑Augmented Generation (RAG) chatbot with a custom web front end.

> The completed workflow exports (`.json`) and web pages (`.html`) for every activity are in the matching folders:
> `activity1-automation/`, `activity2-ai-agent/`, `activity3-webhook/`, `activity4-rag/`.
> You can import any `.json` into n8n to compare against your own build.

---

## Table of Contents

1. [Before You Start — Setup & Prerequisites](#0-before-you-start)
2. [Activity 1 — Workflow Automation with Forms](#activity-1)
   - [1a — Design a Flyer with an n8n Form (Form → Email)](#activity-1a)
   - [1b — Conditional Routing with an IF node](#activity-1b)
   - [1c — Saving Submissions to a Data Table](#activity-1c)
3. [Activity 2 — Build an AI Agent (Chat + Tools + Memory)](#activity-2)
4. [Activity 3 — Expose the Agent via a Webhook + Custom Web UI](#activity-3)
5. [Activity 4 — RAG Chatbot with Vector Store & File Upload](#activity-4)
6. [Troubleshooting Cheat‑Sheet](#troubleshooting)
7. [Glossary](#glossary)

---

<a name="0-before-you-start"></a>
## 0. Before You Start — Setup & Prerequisites

### 0.1 Accounts & tools you need
| Item | Why | Where |
|---|---|---|
| **n8n account** (Cloud or self‑hosted) | The automation platform used for every activity | https://n8n.io |
| **OpenAI API key** | Powers the LLM (chat model & embeddings) in Activities 2–4 | https://platform.openai.com/api-keys |
| **Tavily API key** | Web‑search tool for the AI Agent | https://tavily.com |
| **Google / Gmail account** | Sending email in Activity 1 | Your Google account |
| **A modern browser** | To open the custom HTML pages in Activities 3–4 | Chrome / Edge / Safari |

### 0.2 Add your credentials in n8n (do this once)
In n8n, credentials are stored centrally and reused by nodes.

1. Open n8n → top‑left menu → **Credentials** → **Add credential**.
2. Create the following:
   - **OpenAI** → paste your OpenAI API key.
   - **Tavily API** → paste your Tavily API key.
   - **Gmail OAuth2** → click **Sign in with Google** and authorise n8n to send mail.
3. You'll select these credentials inside the nodes as you build each workflow.

> **Security tip:** Never paste API keys into the HTML files or share workflow exports that contain secrets. Credentials live only inside n8n's credential store.

### 0.3 How to import a finished workflow (optional reference)
1. In n8n click **Workflows → Add workflow → ⋯ (top‑right) → Import from File**.
2. Choose the `.json` from the activity folder.
3. Re‑select your own credentials on each node (imported credential IDs won't match yours).
4. Click **Save**, then toggle **Active** (or **Published**) when ready.

---

<a name="activity-1"></a>
## Activity 1 — Workflow Automation with Forms

**Goal:** Learn the core n8n building blocks — a **trigger**, **data**, **logic**, and an **action** — by capturing form submissions and emailing them. You'll build three increasingly capable versions.

Folder: [`activity1-automation/`](activity1-automation/)

---

<a name="activity-1a"></a>
### Activity 1a — Design a Flyer with an n8n Form (Form → Email)

**What you'll build:** A hosted enquiry form that emails you each submission.
Reference export: `Activity1a_ Design a Flyer with n8n form embedded.json`

**Workflow shape:** `On form submission (Form Trigger)` → `Send a message (Gmail)`

#### Steps
1. **Create a new workflow** → name it `Activity 1a – Flyer Form`.
2. **Add the trigger:** click **＋ → On form submission** (the n8n **Form Trigger**).
3. **Configure the form:**
   - **Form Title:** `Enquiry Form`
   - **Form Description:** `Enquiry about my service`
   - **Form Fields** (click *Add Field* for each):
     | Field Label | Field Type | Notes |
     |---|---|---|
     | `What's your name?` | Text | |
     | `What's your email` | Email | |
     | `What is your gender` | Radio (Dropdown) | Options: `Male`, `Female` |
     | `What is your favorite food?` | Textarea | |
4. **Add the action:** click the **＋** after the trigger → search **Gmail** → choose **Send a message**.
5. **Configure Gmail:**
   - **Credential:** select your Gmail OAuth2 credential.
   - **To:** your email (e.g. `angch@tertiaryinfotech.com`).
   - **Subject:** `New Enquiry`
   - **Email Type:** HTML.
   - **Message:** use expressions to pull the form answers. Click into the field, switch to **Expression**, and paste:
     ```
     Hi <br><br>
     There is a new enquiry. <br><br>
     Name: {{ $json["What's your name?"] }} <br>
     Email: {{ $json["What's your email"] }} <br>
     Gender: {{ $json["What is your gender"] }} <br>
     Food: {{ $json["What is your favorite food?"] }} <br>
     ```
     > Each `{{ $json["Field Label"] }}` reads the matching form field. The label must match **exactly**.
6. **Test it:**
   - Click **Execute workflow** (or open the **Form Trigger → Test URL**).
   - n8n shows the hosted form in a new tab. Fill it in and submit.
   - Check your inbox — you should receive the formatted enquiry email.
7. **Go live:** toggle the workflow **Active**. The **Production URL** of the Form Trigger is your public form link (you can embed it in a website/flyer via an `<iframe>`).

**Key concepts:** Form Trigger, the `$json` data object, expressions `{{ }}`, Gmail action node.

---

<a name="activity-1b"></a>
### Activity 1b — Conditional Routing with an IF node

**What you'll build:** A party‑RSVP form that only emails the team when someone answers **"Yes"**.
Reference export: `Activity1b_ Improved Flyer with Conditonal Route.json`

**Workflow shape:** `On form submission` → `IF` → (true) `Send a message` / (false) `No Operation`

#### Steps
1. Duplicate Activity 1a (or start fresh) → name it `Activity 1b – Conditional`.
2. **Update the form** (Form Trigger):
   - **Form Title / Description:** `Bowling Party Attendance`
   - **Fields:**
     | Field Label | Type | Options |
     |---|---|---|
     | `Name` | Text | |
     | `Email` | Email | |
     | `Tel` | Number | |
     | `Are you attending the bowling party` | Radio | `Yes`, `No` |
     | `Message` | Textarea | |
3. **Add an IF node** after the trigger (**＋ → IF**):
   - **Condition 1:**
     - **Value 1 (left):** Expression → `{{ $json["Are you attending the bowling party"] }}`
     - **Operator:** String → **is equal to**
     - **Value 2 (right):** `Yes`
   - The IF node now has two outputs: **true** (top) and **false** (bottom).
4. **On the `true` branch:** connect the **Gmail → Send a message** node:
   - **Subject:** `Operation Request`
   - **Message** (Expression):
     ```
     Hi Operation Team <br><br>
     There is a new operation request. The details are below: <br>
     Name: {{ $json.Name }} <br>
     Email: {{ $json.Email }} <br>
     Tel: {{ $json.Tel }} <br>
     Message: {{ $json.Message }} <br><br>
     Thanks <br>Operation
     ```
     > Because these field labels are single words (`Name`, `Email`…), you can use the shorthand `$json.Name` instead of `$json["..."]`.
5. **On the `false` branch:** add a **No Operation, do nothing** node (so the branch ends cleanly).
6. **Test:** submit the form once with **Yes** (expect an email) and once with **No** (expect no email).

**Key concepts:** Branching logic with the **IF** node, true/false outputs, the `NoOp` node.

---

<a name="activity-1c"></a>
### Activity 1c — Saving Submissions to a Data Table

**What you'll build:** Same RSVP form, but every response is **stored in an n8n Data Table** — "Yes" and "No" are tagged differently and an email still fires for attendees.
Reference export: `Activity1c_ Improved Flyer with Data Table.json`

**Workflow shape:** `On form submission` → `IF` → true → `Insert row (Attending = true)` → `Send a message`; false → `Insert row1 (Attending = false)`

#### Steps
1. **Create the Data Table first:**
   - Left menu → **Data Tables → Add Data Table** → name it `Bowling Party`.
   - Add columns: `Name` (string), `Email` (string), `Tel` (string/number), `Message` (string), `Attending` (boolean).
2. Start from your Activity 1b workflow → name it `Activity 1c – Data Table`.
3. **On the `true` branch, add a Data Table node** (**＋ → Data Table → Insert row**):
   - **Data Table:** select `Bowling Party`.
   - **Mapping:** Map each column to the form value (Expression):
     - `Name` → `{{ $('On form submission').item.json.Name }}`
     - `Email` → `{{ $('On form submission').item.json.Email }}`
     - `Tel` → `{{ $('On form submission').item.json.Tel }}`
     - `Message` → `{{ $('On form submission').item.json.Message }}`
     - `Attending` → `true`
     > `$('On form submission')` references the trigger node by name, so you can still reach the original form data after the IF split.
   - Connect this **Insert row** node to the **Gmail** node (so attendees are both saved *and* emailed).
4. **On the `false` branch, add another Insert row node** (`Insert row1`):
   - Same mapping, but set **`Attending` → `false`**. (No email on this branch.)
5. **Test:** submit a couple of "Yes" and "No" responses, then open the **Bowling Party** data table — you should see rows with the correct `Attending` flag.

**Key concepts:** **Data Tables** as lightweight built‑in storage, cross‑node references with `$('Node Name')`, persisting structured data for later querying (used heavily in Activities 2–4).

---

<a name="activity-2"></a>
## Activity 2 — Build an AI Agent (Chat + Tools + Memory)

**Goal:** Create a conversational **AI Agent** that can reason, remember context, search the web, and look up your **employee data table** — all from n8n's built‑in chat.

Folder: [`activity2-ai-agent/`](activity2-ai-agent/)
Reference export: `Activity2-AI Agent.json`

**Workflow shape:**
```
When chat message received (Chat Trigger) ─▶ AI Agent ─▶ (reply)
                                              ├─ OpenAI Chat Model   (the brain)
                                              ├─ Simple Memory        (remembers the conversation)
                                              ├─ Search in Tavily      (web search tool)
                                              └─ Get row(s) in Data table (employee data tool)
```

#### Prerequisite: an employee data table
Create a Data Table named **`Mock Employee Data`** with a handful of rows and columns such as `Name`, `Gender`, `Department`, `Role`, `Location`, `Food`, `Attending`. (Activities 2–4 all query this table.)

#### Steps
1. **New workflow** → `Activity 2 – AI Agent`.
2. **Add the trigger:** **＋ → On chat message** (the LangChain **Chat Trigger**). This gives you a built‑in chat window to test with.
3. **Add the AI Agent:** **＋ → AI Agent** (`@n8n/n8n-nodes-langchain.agent`). Connect the Chat Trigger into it.
4. **Attach the language model:** on the Agent's **Chat Model** port, add **OpenAI Chat Model**:
   - **Credential:** your OpenAI credential.
   - **Model:** `gpt-4.1-mini` (or another available chat model).
5. **Attach memory:** on the **Memory** port, add **Simple Memory** (Window Buffer Memory). This lets the agent remember earlier turns in the same session.
6. **Attach Tool #1 — Tavily web search:** on the **Tool** port, add **Search in Tavily**:
   - **Credential:** your Tavily API key.
   - Leave the query as the auto‑generated `$fromAI('Query')` — the agent decides what to search.
7. **Attach Tool #2 — Data Table lookup:** add **Get row(s) in Data table** (Data Table **Tool**):
   - **Data Table:** select `Mock Employee Data`.
   - **Operation:** Get row(s), **Return All: ON**.
   - **Tool Description:** describe it so the agent knows when to use it, e.g.
     *"Look up employee records (name, gender, department, role, location). Use this for any question about staff, headcount, or who works where."*
8. **Set the system prompt** (Agent → **Options → System Message**):
   ```
   You are a helpful assistant.
   If the user asks about the event/employee info, get the info from the Data Table tool.
   ```
9. **Test in chat:** open the chat panel (bottom of the canvas) and try:
   - "How many employees are in the Engineering department?" → agent calls the **Data Table** tool.
   - "What's the latest news about Qualcomm?" → agent calls **Tavily**.
   - Ask a follow‑up ("and how many of them are female?") to see **memory** in action.

**Key concepts:** The **AI Agent** pattern (LLM + tools + memory), tool selection by the model, `$fromAI()` dynamic tool inputs, grounding answers in your own data.

---

<a name="activity-3"></a>
## Activity 3 — Expose the Agent via a Webhook + Custom Web UI

**Goal:** Replace n8n's built‑in chat with a **webhook** so your own web page (a branded dashboard) can talk to the agent over HTTP.

Folder: [`activity3-webhook/`](activity3-webhook/)
Reference export: `Acitivty3-Webhook.json` · Web pages: `index.html` (+ `index1.html`…`index4.html` design variants)

**Workflow shape:**
```
Webhook (POST) ─▶ AI Agent ─▶ Respond to Webhook
                   ├─ OpenAI Chat Model
                   ├─ Search in Tavily
                   └─ Get row(s) in Data table
```

#### Part A — Build the webhook workflow in n8n
1. **New workflow** → `Activity 3 – Webhook Agent`. (Tip: copy your Activity 2 agent and swap the trigger.)
2. **Add a Webhook trigger** (**＋ → Webhook**):
   - **HTTP Method:** `POST`
   - **Path:** keep the auto‑generated id (e.g. `dd040a01-…`) — this becomes part of your URL.
   - **Respond:** **Using 'Respond to Webhook' Node**.
   - **Options → Add Option → Allowed Origins (CORS):** set to `*`
     *(Required so a browser page on a different origin can call it — otherwise you'll get a "couldn't reach the webhook" error.)*
3. **Connect Webhook → AI Agent.** Re‑attach the **OpenAI Chat Model**, **Tavily**, and **Get row(s) in Data table** tools (as in Activity 2).
4. **Feed the user's message into the agent.** In the Agent's **Text** field (Expression):
   ```
   {{ $json.body.message }}
   ```
   *(Our web page posts `{ "message": "...", "chatInput": "..." }`.)*
5. **Add a `Respond to Webhook` node** after the Agent:
   - **Respond With:** **JSON**
   - **Response Body** (Expression):
     ```
     {{ { "reply": $json.output } }}
     ```
     *(The Agent puts its answer in `output`; this returns `{ "reply": "..." }`, which the page displays.)*
6. **Save** and toggle the workflow **Active / Published**.
7. **Copy the Production URL** from the Webhook node — it looks like
   `https://<your-n8n-host>/webhook/dd040a01-…`.

#### Part B — Connect the web page
1. Open `activity3-webhook/index.html` in your browser (double‑click, or serve it locally).
2. Click the **⚙️ gear** in the chat header to reveal the **Webhook URL** field.
3. Paste your **Production URL** → **Save** (it's stored in the browser's localStorage).
4. Type a message and **Send**. The page POSTs to your webhook; the agent's reply appears in the chat.
   - The **"Sync from Database"** button also calls the same webhook with a stats prompt to populate the workforce dashboard from `Mock Employee Data`.

> `index1.html`–`index4.html` are alternative visual designs of the same dashboard — they all talk to the same webhook. Use whichever you like.

**Key concepts:** **Webhook** trigger vs. chat trigger, request/response over HTTP, **CORS**, **Respond to Webhook** shaping the JSON the front end expects, decoupling UI from automation.

---

<a name="activity-4"></a>
## Activity 4 — RAG Chatbot with Vector Store & File Upload

**Goal:** Give the agent a **knowledge base**. Users upload HR policy documents (SOPs) which are embedded into a **vector store**; the agent then answers policy questions from those documents (RAG) while still answering people/headcount questions from the **employee data table**.

Folder: [`activity4-rag/`](activity4-rag/)
Reference export: `Activity4-RAG.json` · Web page: `index.html` · Sample doc: `Qualcomm-HR-SOP.docx`

**Workflow shape — two flows in one workflow:**
```
INGESTION (upload):
  Webhook1 (POST, path 92c5dbda-…) ─▶ Simple Vector Store (Insert, key "sop")
                                        ├─ Embeddings OpenAI
                                        └─ Default Data Loader  (reads the uploaded file)

CHAT (query):
  Webhook (POST) ─▶ AI Agent ─▶ Respond to Webhook
                     ├─ OpenAI Chat Model
                     ├─ Get row(s) in Data table      (employee data)
                     ├─ Query Data Tool (Vector Store, retrieve "sop")  (SOP knowledge)
                     └─ Search in Tavily              (web fallback)
```

#### Part A — Build the ingestion flow (file → vector store)
1. Continue from your Activity 3 workflow (or import `Activity4-RAG.json`).
2. **Add a second Webhook** named `Webhook1`:
   - **HTTP Method:** `POST`
   - **Path:** `92c5dbda-24a8-4283-83b5-81c1e2b94210` (or your own id — keep it handy).
   - **Options → Allowed Origins (CORS):** `*`
3. **Add a Simple Vector Store** node → **Operation: Insert Documents** → **Memory Key:** `sop`.
4. On its **Embeddings** port add **Embeddings OpenAI** (your OpenAI credential).
5. On its **Document** port add a **Default Data Loader**:
   - **Type of Data:** **Binary** (so it reads the uploaded file).
   - **Binary property:** `file` (matches the field name the web page sends).
6. Connect `Webhook1 → Simple Vector Store`.

#### Part B — Add the SOP retrieval tool to the agent
1. **Add a Simple Vector Store** node in **retrieve‑as‑tool** mode → name it `Query Data Tool`:
   - **Memory Key:** `sop` (same store you inserted into).
   - **Tool Name:** `knowledge_base`
   - **Tool Description:** describe it as the HR SOP knowledge base (leave, MC, performance, PDPA, marketing, PR, data privacy) so the agent routes policy questions here.
   - Add its own **Embeddings OpenAI** on the embedding port.
2. Connect `Query Data Tool → AI Agent` (Tool port).

#### Part C — Tune the system prompt to route questions
Set the Agent's **System Message** so it picks the right tool:
```
You are the Operations Mission Control Assistant. Always use a tool before answering.
• HR POLICY / SOP questions (leave, MC, performance, PDPA, marketing, PR, data privacy)
  → use the 'knowledge_base' (SOP vector store).
• EMPLOYEE / HEADCOUNT questions (how many staff, gender, department, location)
  → use 'Get row(s) in Data table' (Mock Employee Data).
• Anything external/current → use Tavily.
Base every answer only on tool output; never guess. Be brief and cite the policy section
or the number of rows counted.
```

#### Part D — Connect the web page & upload a document
1. Open `activity4-rag/index.html`.
2. **Chat webhook (⚙️ gear):** paste the **chat** Production URL (the `dd040a01`‑style one) → Save.
3. **Knowledge Base card → upload webhook field:** paste the **`Webhook1`** Production URL (`…/webhook/92c5dbda-…`) → Save.
4. **Upload the SOP:** drag `Qualcomm-HR-SOP.docx` into the dropzone → **Upload to Knowledge Base**. This POSTs the file to `Webhook1`, which embeds it into the `sop` vector store.
5. **Ask policy questions** in the chat, e.g.:
   - "How many days of annual leave do I get?" → answered from the **SOP** (knowledge_base).
   - "When do I need to submit an MC?" → from the SOP.
   - "How many employees are in Engineering?" → from the **Data Table**.

> The sample document `Qualcomm-HR-SOP.docx` contains 7 policies (Leave, MC, Performance, PDPA, Marketing, Public Relations, Data Privacy). It's generated by `activity4-rag/make_sop.py` if you want to regenerate or edit it.

**Key concepts:** **RAG** (embed → store → retrieve), **vector store** + **embeddings**, **document loaders**, **binary file uploads** through a webhook, **tool routing** via the system prompt, separating ingestion from querying.

---

<a name="troubleshooting"></a>
## Troubleshooting Cheat‑Sheet

| Symptom | Likely cause | Fix |
|---|---|---|
| **"Couldn't reach the webhook"** in the browser | CORS not allowed | On the Webhook node → **Options → Allowed Origins (CORS) = `*`**, save & re‑publish. |
| Upload fails / nothing happens | Webhook method is **GET**, page sends **POST** | Set the Webhook **HTTP Method** to **POST**. |
| **"Workflow triggered, but it returned no content"** | Wrong URL in the chat field, or Respond node not returning JSON | Put the **chat** webhook URL (not the upload one) in the chat field; set **Respond to Webhook → JSON → `{{ { "reply": $json.output } }}`**. |
| Chat works but the answer is `[object Object]` / blank | The agent's output field isn't `output` | Check the Agent output; adjust the Respond body (e.g. `$json.text`). |
| Agent answers from memory instead of data | System prompt too weak / tool description vague | Strengthen the system prompt ("always use a tool first") and write clear **Tool Descriptions**. |
| Vector store returns nothing | Document never ingested, or wrong **Memory Key** | Upload the doc again; ensure insert and retrieve use the **same key** (`sop`). |
| Form expression shows blank in email | Field label mismatch | The label inside `{{ $json["..."] }}` must match the form field **exactly**. |
| Production URL 404s | Workflow not **Active/Published** | Toggle the workflow on; the test URL only works while "Listen for test event" is active. |

---

<a name="glossary"></a>
## Glossary

- **Trigger** — the node that starts a workflow (Form, Chat, Webhook).
- **Node** — a single step (action, logic, or tool) in a workflow.
- **Expression** — dynamic value in `{{ }}`, e.g. `{{ $json.Name }}`.
- **`$json`** — the data object flowing into the current node.
- **`$('Node Name')`** — reference data from a specific earlier node.
- **AI Agent** — an LLM that can choose and call tools, and keep memory.
- **Tool** — a capability the agent can invoke (web search, data lookup, knowledge base).
- **Memory** — keeps prior conversation turns so the agent has context.
- **Webhook** — an HTTP endpoint that lets external pages/apps trigger a workflow.
- **CORS** — browser security that must allow your page's origin to call the webhook.
- **Embeddings** — numeric vectors representing text meaning, used for semantic search.
- **Vector Store** — database of embeddings used to retrieve relevant chunks.
- **RAG (Retrieval‑Augmented Generation)** — retrieve relevant documents, then let the LLM answer using them.
- **Data Table** — n8n's built‑in lightweight table storage.

---

*End of guide. Build the activities in order — each one reuses skills from the last. The matching `.json` exports in every folder are working references you can import and compare against your own build.*
