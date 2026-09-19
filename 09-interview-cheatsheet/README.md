# ⚡ Senior Tech Lead Interview Cheatsheets & Quick Revision Cards

> Rapid 5-minute refresher cards, architectural trade-off decision matrices, and leadership scenarios designed for high-yield revision before **Senior Technical Lead & SDE-2/3 interview rounds**.

---

## 📌 How to Use This Section
- Use this folder for rapid last-minute revision before your technical and architectural interview rounds.
- Add quick summary files inside `09-interview-cheatsheet/` as you complete topics across your knowledge base.

---

## 📑 Quick Revision Index & Flash Cards

### 1. 5-Minute Core Refresher Cards
- [ ] `01_javascript_v8_event_loop_card.md` — Call Stack, Microtasks vs Macrotasks, Memory GC, Closures in 60 seconds.
- [ ] `02_typescript_type_system_card.md` — `unknown` vs `any`, Generics, `infer`, Conditional types flashcard.
- [ ] `03_react18_fiber_rsc_card.md` — Fiber Render vs Commit, `useTransition`, Server Components vs Client Components.
- [ ] `04_node_libuv_streams_card.md` — Libuv 6 loop phases, Backpressure, Worker threads vs Clustering.
- [ ] `05_fastapi_asyncio_pydantic_card.md` — Python `asyncio`, `async def` vs `def` threadpool, Pydantic V2 validation.
- [ ] `06_genai_rag_vector_db_card.md` — HNSW vs IVF-PQ, Chunking, Hybrid Search, Reranking, Agentic ReAct loops.

### 2. Architectural Trade-off Decision Matrices
- [ ] `07_architecture_comparison_matrix.md` — Microservices vs Monolith, REST vs GraphQL vs gRPC, SQL vs NoSQL, RAG vs Fine-Tuning.

### 3. Senior Technical Lead & Behavioral Scenarios
- [ ] `08_senior_tech_lead_scenarios.md` — STAR method framework for SDE-2/3/Lead: Handling System Outages (RCA), Managing Technical Debt vs Product Deadlines, Architecture Refactoring under load.

---

## ⚖️ High-Yield Architectural Trade-off Quick Matrix

| Architectural Choice | Option A | Option B | When to Choose Option A | When to Choose Option B |
| :--- | :--- | :--- | :--- | :--- |
| **API Protocol** | **REST** | **gRPC** | Public APIs, Browser clients, Easy debugging | Internal microservices, High-throughput binary streaming |
| **Data Fetching** | **REST** | **GraphQL** | Fixed schemas, Simple caching | Complex nested data client requirements, Over-fetching prevention |
| **DB Model** | **PostgreSQL (RDBMS)** | **MongoDB (Document)** | ACID transactions, Complex relational joins | Dynamic unstructured schema, High horizontal write scaling |
| **GenAI Knowledge** | **RAG Pipeline** | **LLM Fine-Tuning** | Dynamic external data, Fresh information, Hallucination prevention | Domain style/tone adaptation, Specific syntax learning |
