# ⚡ 16 - Interview Master Cheatsheets, Behavioral STAR & Company Guides

> Rapid 5-minute refresher cards, system design quick recall tables, behavioral STAR scenario templates, and company-specific interview guides for **Senior Technical Lead & SDE-2/3 interview rounds**.

---

## 🗂️ Module Contents & Fast Revision Index

### 1. Rapid Recall Cheatsheets
* [**`01_fullstack_quick_recall_cheatsheet.md`**](./01_fullstack_quick_recall_cheatsheet.md)
  - 5-minute pre-interview revision card covering JS event loop, Prototypal inheritance, `this` rules, React diffing, Angular 21 Signals & Zoneless, and Node.js.
* [**`02_system_design_cheat_sheet.md`**](./02_system_design_cheat_sheet.md)
  - Back-of-the-envelope math, QPS calculations, hardware latency numbers, and CAP/PACELC trade-offs.

### 2. Behavioral Leadership & STAR Scenarios
* [**`interview-questions/behavioral_star_method_master_guide.md`**](./interview-questions/behavioral_star_method_master_guide.md)
  - High-stakes production outage war stories, senior technical disagreement handling, and leadership STAR templates with quantifiable metrics.

### 3. Service MNC Tier Guides
* [**`service-mnc-tier/tcs_interview_guide.md`**](./service-mnc-tier/tcs_interview_guide.md) — TCS Technical Round 1 & 2 guide.
* [**`service-mnc-tier/infosys_interview_guide.md`**](./service-mnc-tier/infosys_interview_guide.md) — Infosys Specialist Programmer & Senior Developer guide.
* [**`service-mnc-tier/wipro_interview_guide.md`**](./service-mnc-tier/wipro_interview_guide.md) — Wipro L1/L2 Technical rounds & microservices.
* [**`service-mnc-tier/cognizant_interview_guide.md`**](./service-mnc-tier/cognizant_interview_guide.md) — Cognizant CTS architecture & distributed systems guide.
* [**`service-mnc-tier/capgemini_interview_guide.md`**](./service-mnc-tier/capgemini_interview_guide.md) — Capgemini enterprise Java, MERN & Cloud guide.
* [**`service-mnc-tier/01_top_mnc_interview_questions_tcs_accenture.md`**](./service-mnc-tier/01_top_mnc_interview_questions_tcs_accenture.md) — High-frequency cross-MNC interview questions and simple, confident answers.

### 4. Product Companies & Startups
* [**`mid-tier-and-startups/jll_interview_guide.md`**](./mid-tier-and-startups/jll_interview_guide.md) — JLL scenario-based problem solving and secure auth architectures.
* [**`mid-tier-and-startups/nagarro_interview_guide.md`**](./mid-tier-and-startups/nagarro_interview_guide.md) — Nagarro design patterns and algorithmic rigor.
* [**`mid-tier-and-startups/startup_tech_lead_interview_guide.md`**](./mid-tier-and-startups/startup_tech_lead_interview_guide.md) — Series A-C Startup Tech Lead trade-offs, cloud cost reduction, and zero-to-one delivery.

---

## ⚖️ High-Yield Architectural Trade-off Quick Matrix

| Architectural Choice | Option A | Option B | When to Choose Option A | When to Choose Option B |
| :--- | :--- | :--- | :--- | :--- |
| **API Protocol** | **REST** | **gRPC** | Public APIs, Browser clients, Easy debugging | Internal microservices, High-throughput binary streaming |
| **Data Fetching** | **REST** | **GraphQL** | Fixed schemas, Simple caching | Complex nested data client requirements, Over-fetching prevention |
| **DB Model** | **PostgreSQL (RDBMS)** | **MongoDB (Document)** | ACID transactions, Complex relational joins | Dynamic unstructured schema, High horizontal write scaling |
| **GenAI Knowledge** | **RAG Pipeline** | **LLM Fine-Tuning** | Dynamic external data, Fresh information, Hallucination prevention | Domain style/tone adaptation, Specific syntax learning |
| **Java Concurrency** | **Platform Threads** | **Virtual Threads** | CPU-bound computation, Legacy JNI code | I/O-bound microservices, High-concurrency web requests |
