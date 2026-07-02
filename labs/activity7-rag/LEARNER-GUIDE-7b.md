# Learner Guide — Setting Up the Vector Databases for the RAG Chatbot

**Project:** Cook & Bake Academy — Customer-Service RAG Chatbot
**Goal:** Upload 20 course brochures to Google Drive, then ingest them into a vector
database (**Supabase**, **Pinecone**, or **Qdrant**) so the website chatbot can answer
questions about course **duration, fees, locations** and more.

---

## 0. Big Picture

```
                ┌─────────────────────────────────────────────┐
  Brochures ──► │ Google Drive folder ("Course Brochures")     │
  (20 .txt)     └───────────────────┬─────────────────────────┘
                                    │  (Manual Trigger workflow)
                                    ▼
        n8n: List files ► Download ► Split ► Embed ► Upsert
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
        Supabase pgvector     Pinecone index        Qdrant collection
              └─────────────────────┴─────────────────────┘
                                    │  (CX Agent with RAG workflow)
                                    ▼
                  Website chatbot  ◄──  Webhook / Chat Trigger
```

You need **one** vector database to run the demo. This guide shows all three so you
can compare them. The workflows use different embedding models:

| Workflow | Embedding model | Dimensions |
|----------|-----------------|------------|
| Supabase upload | OpenAI `text-embedding-3-small` | **1536** |
| Qdrant upload | OpenAI `text-embedding-3-small` | **1536** |
| Pinecone upload + CX Agent | Google Gemini `gemini-embedding-001` | **3072** |

> ⚠️ **Dimension rule:** the DB/index/collection dimension **must** equal the
> embedding model's dimension or inserts will fail. If you change the embedding
> model, the vector dimension changes too (e.g. `text-embedding-3-large` = 3072).

---

## 1. Prerequisites

| Item | Where to get it |
|------|-----------------|
| n8n (cloud or self-hosted) | https://n8n.io |
| OpenAI API key (Supabase / Qdrant flows) | https://platform.openai.com/api-keys |
| Google Gemini API key (Pinecone flow + CX Agent) | https://aistudio.google.com/apikey |
| Google Drive OAuth credential | n8n → Credentials → Google Drive OAuth2 |
| A vector DB account | Supabase / Pinecone / Qdrant (below) |

---

## 2. Upload the Brochures to Google Drive

1. In Google Drive, create a folder named **`Course Brochures`**.
2. Upload all 20 `.txt` files from the local [`brochures/`](brochures/) folder.
3. Open the folder and copy its **folder ID** from the URL:
   `https://drive.google.com/drive/folders/`**`<THIS_IS_THE_FOLDER_ID>`**
4. You will paste this ID into the **"List Brochures in Folder"** node of each
   ingestion workflow (replace `REPLACE_WITH_DRIVE_FOLDER_ID`).

---

## 3A. Supabase (pgvector)

### Create the project
1. Go to https://supabase.com → **New project**. Note your project URL and the
   **service_role** key (Project Settings → API).

### Enable pgvector + create the table & search function
2. Open **SQL Editor** and run:

```sql
-- 1. Enable the vector extension
create extension if not exists vector;

-- 2. Table that n8n's Supabase Vector Store node expects
create table if not exists documents (
  id        bigserial primary key,
  content   text,             -- the chunk text
  metadata  jsonb,            -- {source, file_id, ...}
  embedding vector(1536)      -- MUST match OpenAI embedding dimension
);

-- 3. Similarity search function used by the retriever
create or replace function match_documents (
  query_embedding vector(1536),
  match_count int default 5,
  filter jsonb default '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where documents.metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- 4. (Optional but recommended) index for speed
create index if not exists documents_embedding_idx
  on documents using ivfflat (embedding vector_cosine_ops) with (lists = 100);
```

### Add the credential in n8n
3. n8n → **Credentials → New → Supabase API**. Host = your project URL,
   Service Role Secret = service_role key.

### Ingest
4. Import [`Activity7b-Supabase-Upload.json`](Activity7b-Supabase-Upload.json),
   set the Drive folder ID + credentials, and click **Execute workflow**.

---

## 3B. Pinecone

### Create the index
1. Go to https://app.pinecone.io → **Create index**.
   - **Name:** `course-brochures`
   - **Dimensions:** `3072` (matches the Google Gemini `gemini-embedding-001` model used by this flow)
   - **Metric:** `cosine`
   - Choose a serverless region (e.g. AWS `us-east-1`).
2. Copy your **API key** (left sidebar → API Keys).

### Add the credential in n8n
3. n8n → **Credentials → New → Pinecone API** → paste the API key.

### Ingest
4. Import [`Activity7b-Pinecone-Upload.json`](Activity7b-Pinecone-Upload.json).
   - In **Pinecone Vector Store (Insert)**, select the `course-brochures` index.
5. Set the Drive folder ID + credentials, then click **Execute workflow**.

> ⚠️ **Namespace rule — upload and retrieval MUST use the same namespace.**
> The upload flow and the CX Agent's retriever both use the **default namespace**
> (the Namespace option is left empty in both Pinecone nodes). If you set a
> namespace on one side (e.g. `brochures`), you must set the **identical**
> namespace on the other side — otherwise the agent searches an empty namespace
> and returns no results.

> 💡 **One brochure = one chunk.** The 20 course brochures are very similar to
> each other (same structure, similar wording), so splitting them into small
> chunks makes retrieval mix up content from different courses. The flow's
> **Whole-Brochure Splitter** uses chunk size `4000` with `0` overlap so each
> brochure stays intact as a single vector — the agent always retrieves whole
> brochures and never confuses one course's fees or schedule with another's.

> 💡 Pinecone is fully managed and serverless — no schema/SQL needed, just the
> index dimension + metric.

---

## 3C. Qdrant

### Option 1 — Qdrant Cloud
1. Go to https://cloud.qdrant.io → create a free cluster.
2. Copy the **cluster URL** (e.g. `https://xxx.aws.cloud.qdrant.io:6333`) and an **API key**.

### Option 2 — Self-host with Docker
```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage" \
  qdrant/qdrant
# Dashboard: http://localhost:6333/dashboard
```

### Create the collection (optional — n8n can auto-create)
```bash
curl -X PUT http://localhost:6333/collections/course-brochures \
  -H "Content-Type: application/json" \
  -d '{ "vectors": { "size": 1536, "distance": "Cosine" } }'
```

### Add the credential in n8n
3. n8n → **Credentials → New → Qdrant API** → URL + API key.

### Ingest
4. Import [`Activity7b-Qdrant-Upload.json`](Activity7b-Qdrant-Upload.json),
   select the `course-brochures` collection, set Drive folder + credentials,
   and click **Execute workflow**.

---

## 4. Verify the Ingestion

| DB | How to check |
|----|--------------|
| **Supabase** | Table Editor → `documents` should have rows with `content` + `embedding`. |
| **Pinecone** | Index → the **default namespace** shows a non-zero vector count. |
| **Qdrant** | Dashboard → collection `course-brochures` → Points count > 0. |

Supabase/Qdrant split each brochure into ~1–3 chunks (**30–60 vectors** total).
Pinecone keeps one brochure = one chunk, so expect exactly **20 vectors**.

---

## 5. Connect the Chatbot (CX Agent with RAG)

1. Import / open [`Activity7b-CX-Agent.json`](Activity7b-CX-Agent.json) (the answering workflow).
   It uses a **Webhook (POST) → AI Agent → Respond to Webhook** chain, with a
   **Pinecone retriever tool** (Gemini embeddings) and a **Google Gemini chat model**.
2. Point its **Pinecone Vector Store** retriever at the same `course-brochures`
   index you ingested into above — same embedding model (Gemini, 3072-dim) and
   **same namespace** as the upload flow (both use the default namespace).
3. **Activate** the workflow and copy the webhook **Production URL**.
4. In [`website/script.js`](website/script.js), set:
   ```js
   const CONFIG = { WEBHOOK_URL: "https://YOUR-N8N-HOST/webhook/xxxx", ... };
   ```
5. Open `website/index.html`, click the 💬 chat button, and ask:
   *"How much is the sourdough course?"* / *"How long is the French Pastry course?"*
   / *"Where are you located?"*

> Until you set `WEBHOOK_URL`, the chatbot runs a built-in local fallback that
> answers from the embedded course data, so the page is demoable offline.

---

## 6. Quick Comparison

| | Supabase (pgvector) | Pinecone | Qdrant |
|---|---|---|---|
| Type | Postgres + extension | Managed SaaS | Open-source / SaaS |
| Setup effort | SQL table + function | Just create an index | Collection (auto-creatable) |
| Self-host? | Yes | No | Yes (Docker) |
| Best when | You already use Postgres | Zero-ops, scale fast | Self-hosted / full control |
| Cost to start | Free tier | Free tier | Free / your own server |

---

## 7. Troubleshooting

- **"expected X dimensions, got N"** → embedding model ≠ DB dimension (OpenAI
  `text-embedding-3-small` = 1536, Gemini `gemini-embedding-001` = 3072). Recreate
  the index/table/collection at the correct size, or switch the embedding model.
- **No results from chatbot (Pinecone)** → the upload and retrieval **namespaces
  don't match**. Check the Namespace option in both the insert node and the CX
  Agent's Pinecone retriever — leave both empty (default namespace) or set both
  to the identical value.
- **Chatbot mixes up courses / quotes the wrong fees** → the brochures were split
  into small chunks. Because the brochures are so similar, keep **one brochure =
  one chunk** (chunk size 4000, overlap 0) so each retrieval returns a complete,
  unambiguous brochure.
- **No results from chatbot** → confirm the retriever points at the *same* store you
  ingested into and uses the *same* embedding model.
- **Google Drive node returns 0 files** → wrong folder ID, or the OAuth account
  doesn't have access to that folder.
- **Empty `content` in Supabase** → ensure the **Default Data Loader** is connected
  to the vector store's `ai_document` input and the Text Splitter to the loader.
```
