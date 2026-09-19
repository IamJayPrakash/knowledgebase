# 🧠 The Universal Tech & Senior Interview Knowledge Base

> A production-grade, zero-to-advanced engineering reference and technical interview preparation repository for **Software Engineers, Senior Technical Leads, Full-Stack Developers (MERN/MEAN), Java/Spring Boot Engineers, AI/LLM Specialists, and System Architects (0 to 8+ Years Experience)**.

---

## 🌟 The "6-Pillar" Pedagogical Gold Standard

Every single concept, architectural breakdown, and LeetCode solution in this repository strictly adheres to the **6-Pillar Educational Framework**:
1. 🐣 **Layman's Analogy (Hinglish + Everyday Real-World ELI5):** Crystal-clear everyday intuition so anyone, from absolute beginners to experienced engineers, grasps concepts effortlessly.
2. 📌 **Point-Wise Core Mechanics & Edge Cases:** Concise breakdown of what happens under the hood without confusing academic jargon.
3. 📊 **Visual ASCII & Mermaid Architecture Diagrams:** Direct visual mapping of data structures, runtime memory models, execution event loops, and distributed cloud architectures.
4. 💻 **Practical Code Implementations:** Naive/brute-force vs optimal solutions with **line-by-line comments** in JavaScript, TypeScript, Python, and Java.
5. 🎯 **The "Interview Pitch":** Exact, natural English phrasing to explain the concept confidently and authoritatively to an interviewer.
6. 💼 **Production War Story (STAR Method):** Real-world project scenarios detailing the Situation, Task, Action, and Business/System Metrics ($ \downarrow $ Latency, $ \uparrow $ Throughput, 0 outages).

---

## 🗺️ Master 16-Tier Directory Architecture

```text
knowledgebase/
├── 01-web-core-and-performance/     # Web Core Vitals (LCP, INP, CLS), Critical Rendering Path, Image/Font Optimization
├── 02-javascript/                   # V8 Engine, Event Loop, Closures, Prototypes, ES6 Classes, CJS vs ESM, DOM Events
├── 03-typescript/                   # Types, Generics, infer, Conditional Types, Mapped Types, Nominal Branding, tsconfig
├── 04-react/                        # Virtual DOM, Fiber Reconciler, Hooks Deep Dive, Memoization, React 19 Actions
├── 05-angular-21/                   # Modern Angular 21: Signals, Default Zoneless, @defer, inject(), RxJS Interop
├── 06-nextjs/                       # Next.js 15 App Router: Server Components, Server Actions, 4-Tier Caching, Middleware
├── 07-backend-node/                 # Libuv Event Loop (6 phases), Streams & Backpressure, Worker Threads, Express Architecture
├── 08-backend-python-fastapi/       # Python Asyncio, Pydantic V2, Dependency Injection DAG, Rate Limiting Middleware
├── 09-backend-java-springboot/      # Core Java 21, Virtual Threads (Loom), Generational ZGC, Spring Boot 3 JWT & Resilience4j
├── 10-backend-ruby-and-stacks/      # Ruby on Rails MVC, Active Record, Sidekiq Background Jobs, MEAN vs MERN Architecture
├── 11-databases-and-caching/        # PostgreSQL (MVCC, Partitioning), Redis (Redlock, PubSub), MongoDB Aggregation
├── 12-ai-and-genai/                 # Vector Embeddings (HNSW), RAG Pipelines, LangGraph Agents, LoRA Fine-Tuning, vLLM Serving
├── 13-system-design/                # HLD (Netflix, Uber, TinyURL, WhatsApp) & LLD (Parking Lot, Distributed Rate Limiter)
├── 14-leetcode-blind-75/            # 🧮 Complete Blind 75 Solutions with 3 Evolution Versions, Visuals & War Stories!
├── 15-testing-and-devops/           # Playwright E2E, Jest Unit Testing, Docker Multi-Stage, GitHub Actions CI/CD, Kubernetes
└── 16-interview-master-guides/      # 5-Min Recall Cards, System Design Cheat Sheet, Behavioral STAR Guide, MNC & Startup Guides
```

---

## 🔍 Master Keyword & Topic Quick Finder

Use this index or `CTRL+F` to jump directly to any concept across the knowledge base:

| Topic / Keyword | Core Concept Covered | Direct File Link |
| :--- | :--- | :--- |
| **Angular Signals** | `signal()`, `computed()`, `effect()`, signal inputs | [`05-angular-21/01_angular21_signals_and_reactivity.md`](./05-angular-21/01_angular21_signals_and_reactivity.md) |
| **Angular Zoneless** | Angular 21 default zoneless, removing `zone.js` | [`05-angular-21/02_angular21_zoneless_architecture.md`](./05-angular-21/02_angular21_zoneless_architecture.md) |
| **Angular Defer** | `@defer`, `@placeholder`, `@loading`, `@error` | [`05-angular-21/03_angular21_defer_block_and_lazy_loading.md`](./05-angular-21/03_angular21_defer_block_and_lazy_loading.md) |
| **Angular Inject** | Standalone components, `inject()` API, functional guards | [`05-angular-21/04_angular21_standalone_components_and_inject.md`](./05-angular-21/04_angular21_standalone_components_and_inject.md) |
| **Angular RxJS Interop** | `toSignal()`, `toObservable()`, stream bridging | [`05-angular-21/05_angular21_rxjs_interop_to_signal.md`](./05-angular-21/05_angular21_rxjs_interop_to_signal.md) |
| **Java Virtual Threads** | Project Loom, $M:N$ mapping, carrier threads, unmounting | [`09-backend-java-springboot/04_java21_virtual_threads_and_structured_concurrency.md`](./09-backend-java-springboot/04_java21_virtual_threads_and_structured_concurrency.md) |
| **Java JVM & ZGC** | Eden/Tenured heap, Generational ZGC ($< 1\text{ms}$ pauses) | [`09-backend-java-springboot/05_jvm_garbage_collectors_zgc_g1_tuning.md`](./09-backend-java-springboot/05_jvm_garbage_collectors_zgc_g1_tuning.md) |
| **ConcurrentHashMap** | Bucket treeification (Red-Black Tree), CAS & synchronized node | [`09-backend-java-springboot/06_concurrenthashmap_and_thread_safe_collections.md`](./09-backend-java-springboot/06_concurrenthashmap_and_thread_safe_collections.md) |
| **Spring Security JWT** | `SecurityFilterChain`, stateless sessions, `@PreAuthorize` | [`09-backend-java-springboot/02_springboot_security_jwt_oauth2.md`](./09-backend-java-springboot/02_springboot_security_jwt_oauth2.md) |
| **Spring Resilience4j** | Circuit breaker states (Closed, Open, Half-Open), Retries | [`09-backend-java-springboot/03_springboot_microservices_and_resilience4j.md`](./09-backend-java-springboot/03_springboot_microservices_and_resilience4j.md) |
| **React Fiber** | Work loop, double buffering, render vs commit | [`04-react/01_fiber_reconciler_and_concurrent_mode.md`](./04-react/01_fiber_reconciler_and_concurrent_mode.md) |
| **React 19 Actions** | `useActionState`, `useOptimistic`, React Compiler | [`04-react/10_react19_actions_use_hook_compiler.md`](./04-react/10_react19_actions_use_hook_compiler.md) |
| **React Memoization** | `React.memo`, `useMemo`, `useCallback`, referential equality | [`04-react/06_memoization_usememo_usecallback_react_memo.md`](./04-react/06_memoization_usememo_usecallback_react_memo.md) |
| **Next.js Server Actions** | `"use server"`, RPC mutations, Zod validation | [`06-nextjs/02_server_actions_and_mutations.md`](./06-nextjs/02_server_actions_and_mutations.md) |
| **Next.js 4-Tier Cache** | Request Memoization, Data Cache, Full Route, Router Cache | [`06-nextjs/03_caching_and_revalidation_deep_dive.md`](./06-nextjs/03_caching_and_revalidation_deep_dive.md) |
| **Event Loop (JS)** | Microtask checkpoints, macrotasks, UI render ticks | [`02-javascript/10_event_loop_microtasks_macrotasks.md`](./02-javascript/10_event_loop_microtasks_macrotasks.md) |
| **Deep Clone** | Handling cycles with WeakMap, Date, RegExp, Map/Set | [`02-javascript/interview-questions/coding_deep_clone.md`](./02-javascript/interview-questions/coding_deep_clone.md) |
| **TypeScript Generics** | `extends` constraints, `keyof` lookup | [`03-typescript/04_generics_and_constraints.md`](./03-typescript/04_generics_and_constraints.md) |
| **TypeScript infer** | Pattern extraction, recursive `DeepAwaited` | [`03-typescript/05_conditional_types_and_infer.md`](./03-typescript/05_conditional_types_and_infer.md) |
| **Node.js Streams** | 64KB buffers, `highWaterMark`, backpressure `pipeline` | [`07-backend-node/02_streams_buffers_and_backpressure.md`](./07-backend-node/02_streams_buffers_and_backpressure.md) |
| **Node Worker Threads** | Cluster multi-process vs `worker_threads` shared memory | [`07-backend-node/03_worker_threads_cluster_and_scaling.md`](./07-backend-node/03_worker_threads_cluster_and_scaling.md) |
| **FastAPI Pydantic V2** | Rust core validation, field and model validators | [`08-backend-python-fastapi/02_pydantic_v2_validation_and_serialization.md`](./08-backend-python-fastapi/02_pydantic_v2_validation_and_serialization.md) |
| **PostgreSQL MVCC** | `xmin`/`xmax` headers, Autovacuum, Partial Indexes | [`11-databases-and-caching/sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md`](./11-databases-and-caching/sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md) |
| **PostgreSQL Partitioning**| Range/List/Hash declarative partitions, partition pruning | [`11-databases-and-caching/sql-postgresql/02_postgresql_partitioning_and_replication.md`](./11-databases-and-caching/sql-postgresql/02_postgresql_partitioning_and_replication.md) |
| **Redis Distributed Lock** | Atomic Redlock (`SET NX PX`), Lua script release | [`11-databases-and-caching/redis-caching/02_redis_distributed_locking_and_pubsub.md`](./11-databases-and-caching/redis-caching/02_redis_distributed_locking_and_pubsub.md) |
| **Vector Search (HNSW)** | Hierarchical Navigable Small World, Cosine similarity | [`12-ai-and-genai/02_vector_search_embeddings_and_hnsw.md`](./12-ai-and-genai/02_vector_search_embeddings_and_hnsw.md) |
| **LangGraph Multi-Agent** | Cyclic state machines, ReAct loops, tool calling | [`12-ai-and-genai/03_agentic_workflows_langgraph_and_tool_calling.md`](./12-ai-and-genai/03_agentic_workflows_langgraph_and_tool_calling.md) |
| **LLM LoRA & Quantization**| Low-Rank Adaptation, QLoRA, GGUF, AWQ, 4-bit weights | [`12-ai-and-genai/04_llm_fine_tuning_lora_and_quantization.md`](./12-ai-and-genai/04_llm_fine_tuning_lora_and_quantization.md) |
| **vLLM Serving** | PagedAttention, KV Cache fragmentation, continuous batching | [`12-ai-and-genai/05_production_llm_serving_vllm_and_guardrails.md`](./12-ai-and-genai/05_production_llm_serving_vllm_and_guardrails.md) |
| **HLD Netflix Streaming** | Transcoding pipeline, HLS/DASH 2s chunks, Open Connect CDN | [`13-system-design/03_hld_netflix_video_streaming.md`](./13-system-design/03_hld_netflix_video_streaming.md) |
| **HLD Uber Ride Matching** | Uber H3 hexagonal spatial indexing, real-time dispatch | [`13-system-design/04_hld_uber_ride_matching_spatial_indexing.md`](./13-system-design/04_hld_uber_ride_matching_spatial_indexing.md) |
| **LLD Parking Lot** | Multi-floor OOP design, Factory & Strategy fee patterns | [`13-system-design/05_lld_parking_lot_system.md`](./13-system-design/05_lld_parking_lot_system.md) |
| **LLD Rate Limiter** | Token Bucket and Sliding Window algorithms in Python | [`13-system-design/06_lld_distributed_rate_limiter.md`](./13-system-design/06_lld_distributed_rate_limiter.md) |
| **LeetCode Two Sum** | Hash map memory foundation, 3 evolution versions | [`14-leetcode-blind-75/01-arrays-and-hashing/01_two_sum.md`](./14-leetcode-blind-75/01-arrays-and-hashing/01_two_sum.md) |
| **DSA Pattern Heuristics** | Master algorithm recognition matrix & code skeletons | [`14-leetcode-blind-75/interview-questions/dsa_patterns_cheat_sheet_and_meta_heuristics.md`](./14-leetcode-blind-75/interview-questions/dsa_patterns_cheat_sheet_and_meta_heuristics.md) |
| **5-Min Quick Recall** | Fullstack high-frequency refresher card | [`16-interview-master-guides/01_fullstack_quick_recall_cheatsheet.md`](./16-interview-master-guides/01_fullstack_quick_recall_cheatsheet.md) |
| **Behavioral STAR Guide** | Outage response & senior technical disagreement stories | [`16-interview-master-guides/interview-questions/behavioral_star_method_master_guide.md`](./16-interview-master-guides/interview-questions/behavioral_star_method_master_guide.md) |

---

## 🗂️ Module-by-Module Directory Links

### 01. ⚡ Web Performance & Core Web Vitals ([`01-web-core-and-performance/`](./01-web-core-and-performance/))
* [`web-core-vitals/01_core_web_vitals_lcp_inp_cls.md`](./01-web-core-and-performance/web-core-vitals/01_core_web_vitals_lcp_inp_cls.md)
* [`web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md`](./01-web-core-and-performance/web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md)
* [`web-core-vitals/03_cls_cumulative_layout_shift_debugging.md`](./01-web-core-and-performance/web-core-vitals/03_cls_cumulative_layout_shift_debugging.md)
* [`frontend-performance-optimization/01_critical_rendering_path_and_paint.md`](./01-web-core-and-performance/frontend-performance-optimization/01_critical_rendering_path_and_paint.md)
* [`frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md`](./01-web-core-and-performance/frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md)
* [`frontend-performance-optimization/03_image_and_font_optimization.md`](./01-web-core-and-performance/frontend-performance-optimization/03_image_and_font_optimization.md)

### 02. 🟨 JavaScript Core Engine & Asynchronous Internals ([`02-javascript/`](./02-javascript/))
* **Core Topics:** Data types, Execution contexts, Closures, V8 Garbage Collection, Prototypes, `this` binding, ES6 Classes desugared, Event Loop, Promises, Async/Await, CommonJS vs ESM, Proxy & Reflect, DOM Event Delegation.
* **Coding Challenges:** Deep clone with circular references, Currying, EventEmitter, Debounce/Throttle, Promise.all polyfill, Memory leak diagnostics.

### 03. 🟦 TypeScript Engineering & Type Systems ([`03-typescript/`](./03-typescript/))
* **Core Topics:** Basic types, Unions & Intersections, Interfaces vs Type Aliases, Generics & Constraints, Conditional Types & `infer`, Mapped Types & Template Literals, Utility Types from scratch, Function Utility Types, Nominal Branding, `.d.ts` Ambient declarations, `tsconfig.json` architecture.
* **Interview Challenges:** Custom `DeepPartial`, `FlattenObjectKeys`, `RequireAtLeastOne`.

### 04. ⚛️ React & Concurrent Architecture ([`04-react/`](./04-react/))
* **Core Topics:** Fiber Reconciler, Virtual DOM diffing & keys, State hooks & linked lists, `useEffect` vs `useLayoutEffect`, Memoization (`useMemo`/`useCallback`/`React.memo`), Context API vs Zustand, Custom hooks, Suspense & Streaming SSR, React 19 Actions.
* **Machine Coding:** Autocomplete Search with Debounce & Cache, DOM Virtualized Windowing List.

### 05. 🅰️ Modern Angular 21 Architecture ([`05-angular-21/`](./05-angular-21/))
* [`01_angular21_signals_and_reactivity.md`](./05-angular-21/01_angular21_signals_and_reactivity.md) — Writable signals, `computed()`, `effect()`, signal inputs.
* [`02_angular21_zoneless_architecture.md`](./05-angular-21/02_angular21_zoneless_architecture.md) — Angular 21 default zoneless change detection and signal dirty marking.
* [`03_angular21_defer_block_and_lazy_loading.md`](./05-angular-21/03_angular21_defer_block_and_lazy_loading.md) — `@defer`, `@placeholder`, `@loading`, `@error` triggers.
* [`04_angular21_standalone_components_and_inject.md`](./05-angular-21/04_angular21_standalone_components_and_inject.md) — Standalone components, `inject()` API, functional guards.
* [`05_angular21_rxjs_interop_to_signal.md`](./05-angular-21/05_angular21_rxjs_interop_to_signal.md) — `toSignal()` and `toObservable()` bridging.
* [`interview-questions/angular21_top_interview_questions.md`](./05-angular-21/interview-questions/angular21_top_interview_questions.md) — Angular 21 senior Q&A.

### 06. ▲ Next.js 15 Fullstack Framework ([`06-nextjs/`](./06-nextjs/))
* [`01_app_router_and_react_server_components.md`](./06-nextjs/01_app_router_and_react_server_components.md) — Server Components vs Client Components.
* [`02_server_actions_and_mutations.md`](./06-nextjs/02_server_actions_and_mutations.md) — Type-safe RPC mutations with `"use server"` and Zod validation.
* [`03_caching_and_revalidation_deep_dive.md`](./06-nextjs/03_caching_and_revalidation_deep_dive.md) — 4-tier Caching (Request Memoization, Data Cache, Full Route, Router Cache).
* [`04_middleware_and_authentication.md`](./06-nextjs/04_middleware_and_authentication.md) — Edge routing, auth guards, and rewrite headers.

### 07. 🟢 Backend Node.js & Express ([`07-backend-node/`](./07-backend-node/))
* [`01_libuv_event_loop_phases.md`](./07-backend-node/01_libuv_event_loop_phases.md) — Libuv 6 event loop phases.
* [`02_streams_buffers_and_backpressure.md`](./07-backend-node/02_streams_buffers_and_backpressure.md) — Binary chunks, `highWaterMark`, and backpressure drainage.
* [`03_worker_threads_cluster_and_scaling.md`](./07-backend-node/03_worker_threads_cluster_and_scaling.md) — Cluster multi-process vs Worker Threads shared memory.
* [`04_memory_leaks_and_profiling.md`](./07-backend-node/04_memory_leaks_and_profiling.md) — Programmatic heap snapshots and leak diagnostics.
* [`express/01_express_architecture_and_routing.md`](./07-backend-node/express/01_express_architecture_and_routing.md) — Express middleware pipeline and modular routers.
* [`express/03_express_error_handling_and_logging.md`](./07-backend-node/express/03_express_error_handling_and_logging.md) — Centralized error middleware and SIGTERM graceful shutdown.

### 08. 🐍 Python FastAPI & Concurrency ([`08-backend-python-fastapi/`](./08-backend-python-fastapi/))
* [`01_asyncio_event_loop_and_concurrency.md`](./08-backend-python-fastapi/01_asyncio_event_loop_and_concurrency.md) — Python coroutines and async I/O.
* [`02_pydantic_v2_validation_and_serialization.md`](./08-backend-python-fastapi/02_pydantic_v2_validation_and_serialization.md) — Rust-powered validation core and model serialization.
* [`03_dependency_injection_system.md`](./08-backend-python-fastapi/03_dependency_injection_system.md) — `Depends()` DAG and `yield` resource teardown.
* [`04_background_tasks_and_celery.md`](./08-backend-python-fastapi/04_background_tasks_and_celery.md) — In-process tasks vs distributed Celery queues.
* [`05_high_performance_asgi_starlette_uvicorn.md`](./08-backend-python-fastapi/05_high_performance_asgi_starlette_uvicorn.md) — ASGI architecture, Uvicorn, and `def` vs `async def` threadpools.
* [`interview-questions/coding_rate_limiting_middleware.md`](./08-backend-python-fastapi/interview-questions/coding_rate_limiting_middleware.md) — Distributed sliding window rate limiting.

### 09. ☕ Core Java 21 & Spring Boot 3 ([`09-backend-java-springboot/`](./09-backend-java-springboot/))
* [`01_springboot_architecture_and_jvm.md`](./09-backend-java-springboot/01_springboot_architecture_and_jvm.md) — IoC container, JVM memory spaces, and GC collectors.
* [`02_springboot_security_jwt_oauth2.md`](./09-backend-java-springboot/02_springboot_security_jwt_oauth2.md) — `SecurityFilterChain`, stateless sessions, and `@PreAuthorize`.
* [`03_springboot_microservices_and_resilience4j.md`](./09-backend-java-springboot/03_springboot_microservices_and_resilience4j.md) — Resilience4j Circuit Breakers, Retry policies, and tracing.
* [`04_java21_virtual_threads_and_structured_concurrency.md`](./09-backend-java-springboot/04_java21_virtual_threads_and_structured_concurrency.md) — Project Loom Virtual Threads vs Platform OS Threads, carrier unmounting.
* [`05_jvm_garbage_collectors_zgc_g1_tuning.md`](./09-backend-java-springboot/05_jvm_garbage_collectors_zgc_g1_tuning.md) — Generational ZGC ($< 1\text{ms}$ pauses) vs G1 GC tuning.
* [`06_concurrenthashmap_and_thread_safe_collections.md`](./09-backend-java-springboot/06_concurrenthashmap_and_thread_safe_collections.md) — HashMap bucket treeification, `ConcurrentHashMap` CAS and node locking.
* [`interview-questions/top_java_springboot_interview_questions.md`](./09-backend-java-springboot/interview-questions/top_java_springboot_interview_questions.md) — Core Java & Spring Boot senior interview questions.

### 10. 💎 Ruby on Rails & Fullstack Stacks ([`10-backend-ruby-and-stacks/`](./10-backend-ruby-and-stacks/))
* [`ruby-on-rails/01_ruby_on_rails_mvc_active_record.md`](./10-backend-ruby-and-stacks/ruby-on-rails/01_ruby_on_rails_mvc_active_record.md) — Rails convention over configuration, Active Record, migrations.
* [`ruby-on-rails/02_rails_api_and_sidekiq_jobs.md`](./10-backend-ruby-and-stacks/ruby-on-rails/02_rails_api_and_sidekiq_jobs.md) — API mode (`--api`), ActiveJob, and Redis-backed Sidekiq workers.
* [`mean-vs-mern/01_mean_vs_mern_stack_architecture.md`](./10-backend-ruby-and-stacks/mean-vs-mern/01_mean_vs_mern_stack_architecture.md) — Complete comparative analysis of MEAN vs MERN.

### 11. 🗄️ Databases & Caching ([`11-databases-and-caching/`](./11-databases-and-caching/))
* [`sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md`](./11-databases-and-caching/sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md) — MVCC, dead tuples, Autovacuum, Partial Indexes, `EXPLAIN (ANALYZE, BUFFERS)`.
* [`sql-postgresql/02_postgresql_partitioning_and_replication.md`](./11-databases-and-caching/sql-postgresql/02_postgresql_partitioning_and_replication.md) — Range/List/Hash partitioning, pruning, and WAL replication.
* [`redis-caching/01_redis_data_structures_and_eviction_policies.md`](./11-databases-and-caching/redis-caching/01_redis_data_structures_and_eviction_policies.md) — Hashes, Sorted Sets, LRU vs LFU eviction policies.
* [`redis-caching/02_redis_distributed_locking_and_pubsub.md`](./11-databases-and-caching/redis-caching/02_redis_distributed_locking_and_pubsub.md) — Atomic Redlock (`SET NX PX`), Lua script releases.
* [`nosql-mongodb/01_mongodb_architecture_indexing_sharding.md`](./11-databases-and-caching/nosql-mongodb/01_mongodb_architecture_indexing_sharding.md) — WiredTiger, ESR indexing rule, sharded clusters.
* [`nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md`](./11-databases-and-caching/nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md) — Multi-stage Aggregation pipelines (`$match`, `$unwind`, `$lookup`, `$group`).

### 12. 🤖 AI & GenAI Systems Engineering ([`12-ai-and-genai/`](./12-ai-and-genai/))
* [`01_rag_architecture_and_vector_databases.md`](./12-ai-and-genai/01_rag_architecture_and_vector_databases.md) — Dense embeddings, chunking strategies, and grounded prompting.
* [`02_vector_search_embeddings_and_hnsw.md`](./12-ai-and-genai/02_vector_search_embeddings_and_hnsw.md) — HNSW multi-layer graph search, Cosine similarity vs Dot Product.
* [`03_agentic_workflows_langgraph_and_tool_calling.md`](./12-ai-and-genai/03_agentic_workflows_langgraph_and_tool_calling.md) — ReAct loops, cyclic state machines, and LangGraph StateGraph.
* [`04_llm_fine_tuning_lora_and_quantization.md`](./12-ai-and-genai/04_llm_fine_tuning_lora_and_quantization.md) — LoRA rank decomposition, QLoRA, GGUF, AWQ 4-bit quantization.
* [`05_production_llm_serving_vllm_and_guardrails.md`](./12-ai-and-genai/05_production_llm_serving_vllm_and_guardrails.md) — PagedAttention, continuous batching, and safety guardrails.
* [`interview-questions/coding_simple_rag_pipeline_python.md`](./12-ai-and-genai/interview-questions/coding_simple_rag_pipeline_python.md) — Pure Python Vector Store & RAG pipeline from scratch.

### 13. 🏗️ System Design (HLD & LLD) ([`13-system-design/`](./13-system-design/))
* **High-Level Design (HLD):**
  * [`01_hld_url_shortener_tinyurl.md`](./13-system-design/01_hld_url_shortener_tinyurl.md) — Base62 encoding, Key Generation Service (KGS).
  * [`02_hld_whatsapp_realtime_chat.md`](./13-system-design/02_hld_whatsapp_realtime_chat.md) — WebSockets, Kafka, Presence servers, Cassandra.
  * [`03_hld_netflix_video_streaming.md`](./13-system-design/03_hld_netflix_video_streaming.md) — Transcoding pipeline, HLS/DASH chunks, Open Connect CDN.
  * [`04_hld_uber_ride_matching_spatial_indexing.md`](./13-system-design/04_hld_uber_ride_matching_spatial_indexing.md) — Uber H3 hexagonal spatial indexing, real-time dispatch.
* **Low-Level Design (LLD):**
  * [`05_lld_parking_lot_system.md`](./13-system-design/05_lld_parking_lot_system.md) — Multi-floor OOP design, Factory & Strategy patterns.
  * [`06_lld_distributed_rate_limiter.md`](./13-system-design/06_lld_distributed_rate_limiter.md) — Token Bucket and Sliding Window algorithms in Python.
  * [`interview-questions/system_design_interview_framework.md`](./13-system-design/interview-questions/system_design_interview_framework.md) — The 4-step structural interview framework.

### 14. 🧮 Complete Blind 75 LeetCode Problem Set ([`14-leetcode-blind-75/`](./14-leetcode-blind-75/))
* **All 75 curated Blind 75 problems** complete across 18 pattern subdirectories.
* Includes data structure memory foundations from scratch, 3 evolution versions (Newbie $O(N^2)$ brute-force vs Intermediate vs Senior $O(N)$ optimal), step-by-step trace tables, line-by-line comments, interview pitches, and STAR production war stories.
* [`interview-questions/dsa_patterns_cheat_sheet_and_meta_heuristics.md`](./14-leetcode-blind-75/interview-questions/dsa_patterns_cheat_sheet_and_meta_heuristics.md) — Master pattern recognition matrix & templates.

### 15. 🧪 Testing & DevOps ([`15-testing-and-devops/`](./15-testing-and-devops/))
* [`testing-playwright-jest/01_playwright_e2e_testing_guide.md`](./15-testing-and-devops/testing-playwright-jest/01_playwright_e2e_testing_guide.md) — Playwright E2E cross-browser automation and auto-waiting.
* [`testing-playwright-jest/02_jest_unit_and_integration_testing.md`](./15-testing-and-devops/testing-playwright-jest/02_jest_unit_and_integration_testing.md) — Jest and React Testing Library integration and asynchronous API mocking.
* [`devops-docker-kubernetes-cicd/01_docker_kubernetes_production_setup.md`](./15-testing-and-devops/devops-docker-kubernetes-cicd/01_docker_kubernetes_production_setup.md) — Multi-stage Docker builds and Kubernetes pod/service configurations.
* [`devops-docker-kubernetes-cicd/02_github_actions_production_cicd_pipeline.md`](./15-testing-and-devops/devops-docker-kubernetes-cicd/02_github_actions_production_cicd_pipeline.md) — GitHub Actions CI/CD with Docker Buildx.
* [`devops-docker-kubernetes-cicd/03_kubernetes_helm_and_ingress_setup.md`](./15-testing-and-devops/devops-docker-kubernetes-cicd/03_kubernetes_helm_and_ingress_setup.md) — Helm charts, NGINX Ingress, and Horizontal Pod Autoscaler (HPA).

### 16. 🎯 Master Interview Cheatsheets & Company Guides ([`16-interview-master-guides/`](./16-interview-master-guides/))
* [`01_fullstack_quick_recall_cheatsheet.md`](./16-interview-master-guides/01_fullstack_quick_recall_cheatsheet.md) — 5-minute pre-interview review card.
* [`02_system_design_cheat_sheet.md`](./16-interview-master-guides/02_system_design_cheat_sheet.md) — Math formulas, latency numbers, and trade-off theorems.
* [`interview-questions/behavioral_star_method_master_guide.md`](./16-interview-master-guides/interview-questions/behavioral_star_method_master_guide.md) — Senior Lead behavioral STAR templates with metrics.
* **Company-Specific Guides:**
  * [`service-mnc-tier/tcs_interview_guide.md`](./16-interview-master-guides/service-mnc-tier/tcs_interview_guide.md)
  * [`service-mnc-tier/infosys_interview_guide.md`](./16-interview-master-guides/service-mnc-tier/infosys_interview_guide.md)
  * [`service-mnc-tier/wipro_interview_guide.md`](./16-interview-master-guides/service-mnc-tier/wipro_interview_guide.md)
  * [`service-mnc-tier/cognizant_interview_guide.md`](./16-interview-master-guides/service-mnc-tier/cognizant_interview_guide.md)
  * [`service-mnc-tier/capgemini_interview_guide.md`](./16-interview-master-guides/service-mnc-tier/capgemini_interview_guide.md)
  * [`service-mnc-tier/01_top_mnc_interview_questions_tcs_accenture.md`](./16-interview-master-guides/service-mnc-tier/01_top_mnc_interview_questions_tcs_accenture.md)
  * [`mid-tier-and-startups/jll_interview_guide.md`](./16-interview-master-guides/mid-tier-and-startups/jll_interview_guide.md)
  * [`mid-tier-and-startups/nagarro_interview_guide.md`](./16-interview-master-guides/mid-tier-and-startups/nagarro_interview_guide.md)
  * [`mid-tier-and-startups/startup_tech_lead_interview_guide.md`](./16-interview-master-guides/mid-tier-and-startups/startup_tech_lead_interview_guide.md)

---

## 💻 Tech Stack & Standards

* **Frontend:** JavaScript (ES2024), TypeScript 5+, React 19, Next.js 15 (App Router), Angular 21 (Zoneless, Signals), HTML5/CSS3.
* **Backend:** Node.js 22 (Libuv, Streams), Python 3.12 (FastAPI, Pydantic V2), Java 21 (Spring Boot 3, Loom Virtual Threads), Ruby 3.3 (Rails 7.1, Sidekiq).
* **Databases & Cache:** PostgreSQL 16 (MVCC, Partitioning), Redis 7 (Sorted Sets, Redlock), MongoDB 7 (Aggregation, Sharding).
* **AI / GenAI:** Vector Search (HNSW, FAISS), RAG Pipelines, LangGraph Multi-Agent Workflows, LoRA Fine-Tuning, vLLM Inference.
* **DevOps & Testing:** Docker Multi-Stage, Kubernetes (Helm, Ingress, HPA), GitHub Actions CI/CD, Playwright, Jest.
