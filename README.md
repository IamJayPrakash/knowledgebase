# 🧠 The Universal Tech & Senior Interview Knowledge Base

> A production-grade, zero-to-advanced engineering reference and technical interview preparation guide for **Software Engineers, Senior Technical Leads, Full-Stack Developers (MERN/MEAN), AI/LLM Engineers, and System Architects (0 to 8+ Years Experience)**.

---

## 🌟 The "6-Pillar" Learning Standard

Every concept and LeetCode problem in this repository is crafted using the **6-Pillar Educational Framework**:
1. 🐣 **Layman's Analogy (Hinglish & Real-World):** Crystal-clear everyday intuition so complete beginners grasp concepts effortlessly.
2. 📌 **Point-Wise Core Mechanics:** Concise breakdown of what happens under the hood without confusing jargon.
3. 📊 **Visual ASCII & Mermaid Diagrams:** Direct visual mapping of data structures, execution loops, and distributed architectures.
4. 💻 **Practical Code Implementations:** Comparing naive/brute-force vs optimal solutions with time/space complexities in JavaScript & Python.
5. 🎯 **The "Interview Pitch":** Exact, natural English phrasing to explain the concept confidently to an interviewer.
6. 💼 **Production War Story (STAR Method):** Real-world project scenarios detailing the Situation, Task, Action, and Business/System Metrics ($ \downarrow $ Latency, $ \uparrow $ Throughput).

---

## 🗺️ Master Curriculum & Interactive Index

```text
knowledgebase/
├── 01-core-web-and-performance/      # Web Core Vitals (LCP, INP, CLS), Bundle Splitting, CSS3, HTML5
├── 01-javascript/                    # V8 Engine, Event Loop, Closures, Prototypes, Memory Leaks
├── 02-typescript/                    # Generics, infer, Conditional Types, Utility Types, Mapped Types
├── 03-react/                         # Fiber Reconciler, Hooks Deep Dive, Concurrent Mode, Virtualization
├── 04-frontend-frameworks/           # Next.js App Router (RSC, SSR, ISR), Angular (Signals, DI, RxJS)
├── 04-node/                          # Libuv Event Loop (6 phases), Streams, Backpressure, Worker Threads
├── 05-fastapi/                       # Python Asyncio, Pydantic V2, ASGI/Starlette, Dependency Injection
├── 05-backend-and-runtimes/          # Java Spring Boot (IoC, JVM Generational GC, JPA/Hibernate)
├── 06-ai-genai/                      # Transformers, Vector DBs (HNSW), RAG Pipelines, LangGraph Agents
├── 07-system-design/                 # HLD (TinyURL, WhatsApp, Rate Limiter), LLD, Streaming RAG Architecture
├── 08-leetcode-dsa/                  # 🧮 Complete Blind 75 Solutions with Diagrams, Code & War Stories!
├── 10-testing-and-devops/            # Playwright E2E, Jest Unit Testing, Docker Multi-Stage, Kubernetes (K8s)
└── 11-interview-master-cheatsheets/  # TCS, Infosys, Accenture, Capgemini, JLL, Nagarro & Senior Lead STAR
```

---

## 🗂️ Module Directory & Direct Links

### 1. ⚡ Web Performance & Core Web Vitals
* [`01_core_web_vitals_lcp_inp_cls.md`](./01-core-web-and-performance/web-core-vitals/01_core_web_vitals_lcp_inp_cls.md) — Largest Contentful Paint (LCP), Interaction to Next Paint (INP), Cumulative Layout Shift (CLS).
* [`02_bundle_splitting_and_lazy_loading.md`](./01-core-web-and-performance/frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md) — Route-based code splitting, Dynamic imports, Tree shaking, Vendor chunking.

### 2. 🟨 JavaScript Core Engine & Asynchronous Internals
* [`README.md (JavaScript Index)`](./01-javascript/README.md) — Complete roadmap of Execution Contexts, V8 Engine, Mark-and-Sweep GC, Prototypes, and Microtask queues.
* [`01_v8_event_loop_and_microtasks.md`](./01-javascript/01_v8_event_loop_and_microtasks.md) — Call Stack, Microtask queue, Macrotask queue, Rendering steps, and Event Loop starvation.
* [`interview-questions/README.md`](./01-javascript/interview-questions/README.md) — Polyfills (`Promise.all`, `debounce`, `deepClone`), Output-based snippets, Memory leak debugging.

### 3. 🟦 TypeScript Engineering & Type Systems
* [`README.md (TypeScript Index)`](./02-typescript/README.md) — Basic Types, Unions, Generics, Conditional Types, Type Narrowing.
* [`01_generics_and_conditional_types.md`](./02-typescript/01_generics_and_conditional_types.md) — Pattern matching with `infer`, Distributive conditional types, Custom return types.
* [`interview-questions/README.md`](./02-typescript/interview-questions/README.md) — Custom utility implementations (`DeepReadonly`, `MyPick`, `MyOmit`), Branded types.

### 4. ⚛️ Modern Frontend Frameworks (React, Next.js, Angular)
* [`README.md (React Index)`](./03-react/README.md) — Virtual DOM, Fiber architecture, Hooks under the hood, Concurrent React.
* [`01_fiber_reconciler_and_concurrent_mode.md`](./03-react/01_fiber_reconciler_and_concurrent_mode.md) — Work loop, Render vs Commit phases, Double buffering, `useTransition`.
* [`01_app_router_and_react_server_components.md`](./04-frontend-frameworks/nextjs/01_app_router_and_react_server_components.md) — Next.js App Router, Server Components vs Client Components, Streaming SSR.
* [`01_angular_architecture_and_signals.md`](./04-frontend-frameworks/angular/01_angular_architecture_and_signals.md) — Angular Signals, Fine-grained reactivity, Dependency Injection, Standalone components.

### 5. 🟢 Backend Runtimes (Node.js, FastAPI, Java Spring Boot)
* [`README.md (Node.js Index)`](./04-node/README.md) — Node architecture, Libuv 6 phases, Streams, Buffers, Worker Threads, Clustering.
* [`01_libuv_event_loop_phases.md`](./04-node/01_libuv_event_loop_phases.md) — Detailed breakdown of Timers, Pending, Poll, Check, and Close phases.
* [`README.md (FastAPI Index)`](./05-fastapi/README.md) — Asyncio Event Loop, `async def` vs `def`, Pydantic V2 Rust core, ASGI/Starlette.
* [`01_springboot_architecture_and_jvm.md`](./05-backend-and-runtimes/java-springboot/01_springboot_architecture_and_jvm.md) — Spring Boot Inversion of Control (IoC), JVM Generational GC, JPA/Hibernate.

### 6. 🤖 AI & GenAI Systems Engineering
* [`README.md (AI & GenAI Index)`](./06-ai-genai/README.md) — Transformers, Vector DBs (HNSW vs IVF-PQ), RAG pipelines, Agentic AI, vLLM serving.
* [`interview-questions/README.md`](./06-ai-genai/interview-questions/README.md) — Multi-agent LangGraph workflows, Hybrid Search (BM25 + Dense Vectors), Hallucination reduction.

### 7. 🏗️ System Design (HLD & LLD)
* [`README.md (System Design Index)`](./07-system-design/README.md) — High-Level Design (Load Balancers, Caching, Kafka, Sharding), Low-Level Design (SOLID, GoF Patterns).
* [`interview-questions/README.md`](./07-system-design/interview-questions/README.md) — TinyURL, WhatsApp, Distributed Rate Limiter, Notification Service, Streaming RAG System.

### 8. 🧮 Complete Blind 75 LeetCode Problem Set
* **[`08-leetcode-dsa/README.md`](./08-leetcode-dsa/README.md)** — **All 75 curated Blind 75 problems solved** across 18 pattern directories with Hinglish intuition, Layman analogies, Visual ASCII diagrams, Python & JS solutions, and Production War Stories!

### 9. 🧪 Testing & DevOps
* [`01_playwright_e2e_testing_guide.md`](./10-testing-and-devops/testing-playwright-jest/01_playwright_e2e_testing_guide.md) — Playwright cross-browser automation, Auto-waiting, Network mocking, Jest unit testing.
* [`01_docker_kubernetes_production_setup.md`](./10-testing-and-devops/devops-docker-kubernetes-cicd/01_docker_kubernetes_production_setup.md) — Multi-stage Docker builds, Kubernetes Pods/Services, Ingress, Horizontal Pod Autoscaling (HPA).

### 10. 🎯 MNC & Senior Technical Lead Cheatsheets
* [`01_top_mnc_interview_questions_tcs_accenture.md`](./11-interview-master-cheatsheets/service-mnc-tier/01_top_mnc_interview_questions_tcs_accenture.md) — High-frequency questions and simple, confident answers for TCS, Infosys, Accenture, and Capgemini.
* [`09-interview-cheatsheet/README.md`](./09-interview-cheatsheet/README.md) — 5-minute refresher cards, Architecture comparison matrices, Senior Lead STAR behavioral scenarios.

---

## 🚀 Git Quick Reference

```bash
# Clone the repository
git clone https://github.com/IamJayPrakash/knowledgebase.git

# Navigate into the project
cd knowledgebase

# Pull latest notes & updates
git pull origin main
```

---
*Maintained by **Jay Prakash** — Senior Full Stack & AI Systems Engineer*
