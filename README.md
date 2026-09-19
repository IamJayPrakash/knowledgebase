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

| **Core Web Vitals (LCP/INP/CLS)** | Google CWV thresholds, real-user metrics, SEO impact | [`01-web-core-and-performance/web-core-vitals/01_core_web_vitals_lcp_inp_cls.md`](./01-web-core-and-performance/web-core-vitals/01_core_web_vitals_lcp_inp_cls.md) |
| **LCP Optimization** | 4 Sub-parts (TTFB, Load Delay/Duration, Render Delay), `fetchpriority` | [`01-web-core-and-performance/web-core-vitals/04_lcp_deep_dive_and_codebase_optimization.md`](./01-web-core-and-performance/web-core-vitals/04_lcp_deep_dive_and_codebase_optimization.md) |
| **INP & Task Yielding** | Long tasks ($>50\text{ms}$), `scheduler.yield()`, layout thrashing | [`01-web-core-and-performance/web-core-vitals/05_inp_long_tasks_and_main_thread_yielding.md`](./01-web-core-and-performance/web-core-vitals/05_inp_long_tasks_and_main_thread_yielding.md) |
| **CLS & Font Metrics** | CSS font metric overrides (`size-adjust`), `aspect-ratio`, FOUT | [`01-web-core-and-performance/web-core-vitals/06_cls_font_metrics_and_aspect_ratio_prevention.md`](./01-web-core-and-performance/web-core-vitals/06_cls_font_metrics_and_aspect_ratio_prevention.md) |
| **DOM Virtualization** | Windowing engine from scratch, Heap Snapshots, detached DOM leaks | [`01-web-core-and-performance/frontend-performance-optimization/05_dom_virtualization_and_memory_leak_profiling.md`](./01-web-core-and-performance/frontend-performance-optimization/05_dom_virtualization_and_memory_leak_profiling.md) |
| **Tree-Shaking & sideEffects** | Dead-code elimination, `"sideEffects": false`, barrel file bottlenecks | [`01-web-core-and-performance/frontend-performance-optimization/06_tree_shaking_side_effects_and_barrel_files.md`](./01-web-core-and-performance/frontend-performance-optimization/06_tree_shaking_side_effects_and_barrel_files.md) |
| **Partytown Web Workers** | Offloading GTM/Meta Pixel to background workers, Facade pattern | [`01-web-core-and-performance/frontend-performance-optimization/07_third_party_scripts_and_web_workers.md`](./01-web-core-and-performance/frontend-performance-optimization/07_third_party_scripts_and_web_workers.md) |
| **JavaScript Data Types** | 7 Primitives vs Heap references, implicit coercion, `NaN` | [`02-javascript/01_data_types_and_type_coercion.md`](./02-javascript/01_data_types_and_type_coercion.md) |
| **JS Operators & Control Flow** | Strict equality (`===`), Nullish Coalescing (`??`), `for...of` | [`02-javascript/03_operators_control_flow_and_loops.md`](./02-javascript/03_operators_control_flow_and_loops.md) |
| **JS Arrays In-Depth** | Mutating vs Non-mutating methods, custom `reduce` polyfill | [`02-javascript/04_arrays_in_depth_methods_and_iteration.md`](./02-javascript/04_arrays_in_depth_methods_and_iteration.md) |
| **JS Objects & Cloning** | Destructuring, rest/spread, shallow vs deep clone, `structuredClone` | [`02-javascript/05_objects_destructuring_rest_spread_and_cloning.md`](./02-javascript/05_objects_destructuring_rest_spread_and_cloning.md) |
| **Event Loop (JS)** | Microtask checkpoints, macrotasks, UI render ticks | [`02-javascript/13_event_loop_microtasks_macrotasks.md`](./02-javascript/13_event_loop_microtasks_macrotasks.md) |
| **Deep Clone (JS)** | Handling cycles with WeakMap, Date, RegExp, Map/Set | [`02-javascript/interview-questions/coding_deep_clone.md`](./02-javascript/interview-questions/coding_deep_clone.md) |
| **TypeScript Generics** | `extends` constraints, `keyof` lookup | [`03-typescript/04_generics_and_constraints.md`](./03-typescript/04_generics_and_constraints.md) |
| **TypeScript infer** | Pattern extraction, recursive `DeepAwaited` | [`03-typescript/05_conditional_types_and_infer.md`](./03-typescript/05_conditional_types_and_infer.md) |
| **React Fiber** | Work loop, double buffering, render vs commit | [`04-react/01_fiber_reconciler_and_concurrent_mode.md`](./04-react/01_fiber_reconciler_and_concurrent_mode.md) |
| **React 19 Actions** | `useActionState`, `useOptimistic`, React Compiler | [`04-react/10_react19_actions_use_hook_compiler.md`](./04-react/10_react19_actions_use_hook_compiler.md) |
| **Angular Signals** | `signal()`, `computed()`, `effect()`, signal inputs | [`05-angular-21/01_angular21_signals_and_reactivity.md`](./05-angular-21/01_angular21_signals_and_reactivity.md) |
| **Angular Zoneless** | Angular 21 default zoneless, removing `zone.js` | [`05-angular-21/02_angular21_zoneless_architecture.md`](./05-angular-21/02_angular21_zoneless_architecture.md) |
| **Next.js Server Actions** | `"use server"`, RPC mutations, Zod validation | [`06-nextjs/02_server_actions_and_mutations.md`](./06-nextjs/02_server_actions_and_mutations.md) |
| **Node.js Streams** | 64KB buffers, `highWaterMark`, backpressure `pipeline` | [`07-backend-node/02_streams_buffers_and_backpressure.md`](./07-backend-node/02_streams_buffers_and_backpressure.md) |
| **Python Fundamentals** | Dynamic typing, name tags, mutability vs immutability, `id()` | [`08-backend-python-fastapi/01_python_fundamentals_syntax_types_and_mutability.md`](./08-backend-python-fastapi/01_python_fundamentals_syntax_types_and_mutability.md) |
| **Python Collections** | List over-allocation, compact dict hash table, comprehensions | [`08-backend-python-fastapi/02_python_collections_lists_tuples_dicts_sets.md`](./08-backend-python-fastapi/02_python_collections_lists_tuples_dicts_sets.md) |
| **Python Decorators** | LEGB rule, `*args`/`**kwargs`, closures, `@functools.wraps` | [`08-backend-python-fastapi/03_python_functions_scopes_args_kwargs_and_decorators.md`](./08-backend-python-fastapi/03_python_functions_scopes_args_kwargs_and_decorators.md) |
| **Python OOP & MRO** | Dunder methods, C3 Linearization MRO, cooperative `super()` | [`08-backend-python-fastapi/04_python_oop_classes_dunder_methods_and_mro.md`](./08-backend-python-fastapi/04_python_oop_classes_dunder_methods_and_mro.md) |
| **Python Generators & with**| `yield` state suspension, context managers `__enter__`/`__exit__` | [`08-backend-python-fastapi/05_python_generators_iterators_and_context_managers.md`](./08-backend-python-fastapi/05_python_generators_iterators_and_context_managers.md) |
| **Python GC & GIL** | Reference counting, Cyclic GC generations, GIL & multiprocessing | [`08-backend-python-fastapi/06_python_memory_gc_gil_and_concurrency.md`](./08-backend-python-fastapi/06_python_memory_gc_gil_and_concurrency.md) |
| **FastAPI Pydantic V2** | Rust core validation, field and model validators | [`08-backend-python-fastapi/09_pydantic_v2_validation_and_serialization.md`](./08-backend-python-fastapi/09_pydantic_v2_validation_and_serialization.md) |
| **Java Pass-by-Value** | JDK/JVM architecture, 8 primitives, Integer Cache, Pass-by-value | [`09-backend-java-springboot/01_java_fundamentals_jvm_primitives_and_pass_by_value.md`](./09-backend-java-springboot/01_java_fundamentals_jvm_primitives_and_pass_by_value.md) |
| **Java Strings & SCP** | String Constant Pool, immutability, `StringBuilder`, `equals` | [`09-backend-java-springboot/02_java_strings_memory_string_pool_stringbuilder.md`](./09-backend-java-springboot/02_java_strings_memory_string_pool_stringbuilder.md) |
| **Java OOP & Polymorphism**| 4 pillars, dynamic dispatch via vtable, abstract vs interfaces | [`09-backend-java-springboot/03_java_oop_encapsulation_inheritance_polymorphism_abstraction.md`](./09-backend-java-springboot/03_java_oop_encapsulation_inheritance_polymorphism_abstraction.md) |
| **Java Collections** | `ArrayList` vs `LinkedList`, `HashMap` treeification to Red-Black | [`09-backend-java-springboot/04_java_collections_framework_list_set_queue_map.md`](./09-backend-java-springboot/04_java_collections_framework_list_set_queue_map.md) |
| **Java Generics & PECS** | Producer Extends Consumer Super, Type Erasure, Bridge methods | [`09-backend-java-springboot/05_java_generics_wildcards_and_type_erasure.md`](./09-backend-java-springboot/05_java_generics_wildcards_and_type_erasure.md) |
| **Java Modern Features** | Lambdas, Stream pipelines, Records, Sealed classes, Java 21 switch | [`09-backend-java-springboot/07_java_modern_features_streams_lambdas_records_sealed.md`](./09-backend-java-springboot/07_java_modern_features_streams_lambdas_records_sealed.md) |
| **ConcurrentHashMap** | Bucket treeification (Red-Black Tree), CAS & synchronized node | [`09-backend-java-springboot/08_concurrenthashmap_and_thread_safe_collections.md`](./09-backend-java-springboot/08_concurrenthashmap_and_thread_safe_collections.md) |
| **Java JVM & ZGC** | Eden/Tenured heap, Generational ZGC ($< 1\text{ms}$ pauses) | [`09-backend-java-springboot/09_jvm_garbage_collectors_zgc_g1_tuning.md`](./09-backend-java-springboot/09_jvm_garbage_collectors_zgc_g1_tuning.md) |
| **Java Virtual Threads** | Project Loom, $M:N$ mapping, carrier threads, unmounting | [`09-backend-java-springboot/10_java21_virtual_threads_and_structured_concurrency.md`](./09-backend-java-springboot/10_java21_virtual_threads_and_structured_concurrency.md) |
| **Spring Security JWT** | `SecurityFilterChain`, stateless sessions, `@PreAuthorize` | [`09-backend-java-springboot/12_springboot_security_jwt_oauth2.md`](./09-backend-java-springboot/12_springboot_security_jwt_oauth2.md) |
| **Spring Resilience4j** | Circuit breaker states (Closed, Open, Half-Open), Retries | [`09-backend-java-springboot/13_springboot_microservices_and_resilience4j.md`](./09-backend-java-springboot/13_springboot_microservices_and_resilience4j.md) |
| **PostgreSQL MVCC** | `xmin`/`xmax` headers, Autovacuum, Partial Indexes | [`11-databases-and-caching/sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md`](./11-databases-and-caching/sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md) |
| **PostgreSQL Partitioning**| Range/List/Hash declarative partitions, partition pruning | [`11-databases-and-caching/sql-postgresql/02_postgresql_partitioning_and_replication.md`](./11-databases-and-caching/sql-postgresql/02_postgresql_partitioning_and_replication.md) |
| **Redis Distributed Lock** | Atomic Redlock (`SET NX PX`), Lua script release | [`11-databases-and-caching/redis-caching/02_redis_distributed_locking_and_pubsub.md`](./11-databases-and-caching/redis-caching/02_redis_distributed_locking_and_pubsub.md) |
| **LLM Fundamentals & BPE** | Tokenization, Context Window, Temperature, Top-P/Top-K | [`12-ai-and-genai/01-llm-foundations/01_llm_fundamentals_tokens_context_and_sampling.md`](./12-ai-and-genai/01-llm-foundations/01_llm_fundamentals_tokens_context_and_sampling.md) |
| **Self-Attention & RoPE** | QKV formula, Multi-Head Attention, RoPE, KV-Cache | [`12-ai-and-genai/01-llm-foundations/02_transformer_architecture_and_self_attention.md`](./12-ai-and-genai/01-llm-foundations/02_transformer_architecture_and_self_attention.md) |
| **Vector Search (HNSW)** | Hierarchical Navigable Small World, Cosine similarity | [`12-ai-and-genai/02-embeddings-and-vector-databases/02_vector_databases_hnsw_and_indexing.md`](./12-ai-and-genai/02-embeddings-and-vector-databases/02_vector_databases_hnsw_and_indexing.md) |
| **Hybrid Search & Reranking**| BM25 + Dense vector search, RRF ($k=60$), Cross-Encoder | [`12-ai-and-genai/03-retrieval-augmented-generation-rag/02_advanced_rag_hybrid_search_and_reranking.md`](./12-ai-and-genai/03-retrieval-augmented-generation-rag/02_advanced_rag_hybrid_search_and_reranking.md) |
| **LangChain LCEL & Runnables**| Pipe operator (`|`), `RunnableParallel`, `astream` | [`12-ai-and-genai/04-orchestration-langchain-and-langflow/01_langchain_core_lcel_and_runnables.md`](./12-ai-and-genai/04-orchestration-langchain-and-langflow/01_langchain_core_lcel_and_runnables.md) |
| **LangFlow Visual AI Canvas** | Low-code DAG editor, JSON serialization, Python export | [`12-ai-and-genai/04-orchestration-langchain-and-langflow/03_langflow_visual_ai_prototyping_and_architecture.md`](./12-ai-and-genai/04-orchestration-langchain-and-langflow/03_langflow_visual_ai_prototyping_and_architecture.md) |
| **LangGraph Cyclic Agents** | StateGraph, cycles vs DAGs, Reducers, Checkpointers | [`12-ai-and-genai/05-agentic-ai-and-langgraph/02_langgraph_state_machines_and_agentic_workflows.md`](./12-ai-and-genai/05-agentic-ai-and-langgraph/02_langgraph_state_machines_and_agentic_workflows.md) |
| **Multi-Agent Supervisor** | Hierarchical supervisor routing, isolated scratchpads | [`12-ai-and-genai/05-agentic-ai-and-langgraph/03_multi_agent_systems_and_hierarchical_orchestration.md`](./12-ai-and-genai/05-agentic-ai-and-langgraph/03_multi_agent_systems_and_hierarchical_orchestration.md) |
| **LLM LoRA & QLoRA** | Low-Rank Adaptation math, 4-bit NF4, Double Quantization | [`12-ai-and-genai/06-fine-tuning-and-serving/01_fine_tuning_lora_qlora_and_peft.md`](./12-ai-and-genai/06-fine-tuning-and-serving/01_fine_tuning_lora_qlora_and_peft.md) |
| **vLLM PagedAttention** | OS virtual memory paging analogy, continuous batching | [`12-ai-and-genai/06-fine-tuning-and-serving/02_production_serving_vllm_paged_attention_and_quantization.md`](./12-ai-and-genai/06-fine-tuning-and-serving/02_production_serving_vllm_paged_attention_and_quantization.md) |
| **Prompt Injection & Security**| Direct/indirect injection, NeMo guardrails, PII redaction | [`12-ai-and-genai/07-guardrails-security-and-evaluation/01_guardrails_security_and_prompt_injection.md`](./12-ai-and-genai/07-guardrails-security-and-evaluation/01_guardrails_security_and_prompt_injection.md) |
| **RAG Triad Evaluation** | Context Precision, Faithfulness, Answer Relevance (Ragas)| [`12-ai-and-genai/07-guardrails-security-and-evaluation/02_llm_evaluation_ragas_and_benchmarking.md`](./12-ai-and-genai/07-guardrails-security-and-evaluation/02_llm_evaluation_ragas_and_benchmarking.md) |
| **110 GenAI Interview Qs** | Master 110 questions bank & System Design Scenarios | [`12-ai-and-genai/interview-questions/README.md`](./12-ai-and-genai/interview-questions/README.md) |
| **50 System Design Concepts** | Complete 50 concepts catalog (Scalability, Consensus, Caching, Resilience) | [`13-system-design/00_master_50_system_design_concepts.md`](./13-system-design/00_master_50_system_design_concepts.md) |
| **Consistent Hashing** | Virtual nodes, hash ring distribution, rehashing minimization | [`13-system-design/07_distributed_systems_primitives_consensus_cap_sharding.md`](./13-system-design/07_distributed_systems_primitives_consensus_cap_sharding.md) |
| **Resilience Patterns** | Circuit Breaker, Bulkhead, Jittered Backoff, XFetch Cache Stampede | [`13-system-design/08_resilience_and_stability_patterns.md`](./13-system-design/08_resilience_and_stability_patterns.md) |
| **Twitter Snowflake** | 64-bit distributed time-sortable unique ID generator | [`13-system-design/interview-questions/top_system_design_interview_questions_catalog.md`](./13-system-design/interview-questions/top_system_design_interview_questions_catalog.md) |
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
* **Web Core Vitals (Measurement, Attribution & Codebase Fixes):**
  * [`web-core-vitals/01_core_web_vitals_lcp_inp_cls.md`](./01-web-core-and-performance/web-core-vitals/01_core_web_vitals_lcp_inp_cls.md) — Overview of Google CWV thresholds (LCP $\le 2.5\text{s}$, INP $\le 200\text{ms}$, CLS $\le 0.1$).
  * [`web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md`](./01-web-core-and-performance/web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md) — Input delay, presentation delay, long tasks ($> 50\text{ms}$), and yielding.
  * [`web-core-vitals/03_cls_cumulative_layout_shift_debugging.md`](./01-web-core-and-performance/web-core-vitals/03_cls_cumulative_layout_shift_debugging.md) — Visual stability, `aspect-ratio` bounding boxes, and ad slot placeholders.
  * [`web-core-vitals/04_lcp_deep_dive_and_codebase_optimization.md`](./01-web-core-and-performance/web-core-vitals/04_lcp_deep_dive_and_codebase_optimization.md) — The 4 LCP sub-parts (TTFB, Load Delay/Duration, Render Delay), `<link rel="preload" fetchpriority="high">`, eliminating `loading="lazy"` hero bugs, and inlining critical CSS.
  * [`web-core-vitals/05_inp_long_tasks_and_main_thread_yielding.md`](./01-web-core-and-performance/web-core-vitals/05_inp_long_tasks_and_main_thread_yielding.md) — Main-thread task chunking via `scheduler.yield()` and `MessageChannel`, batching DOM reads/writes to eliminate layout thrashing, and React 18/19 `useTransition`.
  * [`web-core-vitals/06_cls_font_metrics_and_aspect_ratio_prevention.md`](./01-web-core-and-performance/web-core-vitals/06_cls_font_metrics_and_aspect_ratio_prevention.md) — CSS font metric overrides (`size-adjust`, `ascent-override`), `content-visibility: auto` with `contain-intrinsic-size`, and GPU compositor animations.
* **Frontend Performance & Codebase Architecture:**
  * [`frontend-performance-optimization/01_critical_rendering_path_and_paint.md`](./01-web-core-and-performance/frontend-performance-optimization/01_critical_rendering_path_and_paint.md) — DOM, CSSOM, Render Tree, Reflow Layout, Repaint, Composite, and layout thrashing prevention.
  * [`frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md`](./01-web-core-and-performance/frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md) — Route-based chunking, dynamic `import()`, tree-shaking, and vendor chunking.
  * [`frontend-performance-optimization/03_image_and_font_optimization.md`](./01-web-core-and-performance/frontend-performance-optimization/03_image_and_font_optimization.md) — Next-gen image formats (AVIF, WebP), `<picture>` progressive fallback, and variable fonts.
  * [`frontend-performance-optimization/04_resource_hints_speculation_rules_and_caching.md`](./01-web-core-and-performance/frontend-performance-optimization/04_resource_hints_speculation_rules_and_caching.md) — `dns-prefetch`, `preconnect`, modern Speculation Rules API for instant 0ms prerendering, Brotli compression, and `Cache-Control: immutable`.
  * [`frontend-performance-optimization/05_dom_virtualization_and_memory_leak_profiling.md`](./01-web-core-and-performance/frontend-performance-optimization/05_dom_virtualization_and_memory_leak_profiling.md) — Virtual list windowing engine from scratch, Chrome DevTools Heap Snapshots, detached DOM nodes, and `WeakMap` leak prevention.
  * [`frontend-performance-optimization/06_tree_shaking_side_effects_and_barrel_files.md`](./01-web-core-and-performance/frontend-performance-optimization/06_tree_shaking_side_effects_and_barrel_files.md) — ESM static analysis, `"sideEffects": false` in `package.json`, `/*#__PURE__*/` annotations, barrel file re-export bottlenecks, and bundle visualizers.
  * [`frontend-performance-optimization/07_third_party_scripts_and_web_workers.md`](./01-web-core-and-performance/frontend-performance-optimization/07_third_party_scripts_and_web_workers.md) — Offloading third-party marketing tags (GTM, Meta Pixel) to background Web Workers via Partytown, chat widget Facade pattern, and `requestIdleCallback`.
* **Master Interview Question Bank (60 Questions):**
  * [`interview-questions/README.md`](./01-web-core-and-performance/interview-questions/README.md) — 60 Deep Dive Questions: Core Web Vitals (LCP, INP, CLS), Browser Rendering Pipeline, and Network/Bundling Optimization.

### 02. 🟨 JavaScript Core Engine & Asynchronous Internals ([`02-javascript/`](./02-javascript/))
* **Beginner Foundations:**
  * [`01_data_types_and_type_coercion.md`](./02-javascript/01_data_types_and_type_coercion.md) — 7 Primitive types vs Heap references, implicit type coercion, `typeof` quirks.
  * [`02_var_let_const_hoisting_tdz.md`](./02-javascript/02_var_let_const_hoisting_tdz.md) — Function vs Block scope, Variable/Function Hoisting, Temporal Dead Zone.
  * [`03_operators_control_flow_and_loops.md`](./02-javascript/03_operators_control_flow_and_loops.md) — Strict equality (`===`), Nullish Coalescing (`??`), `for...of` vs `for...in`.
  * [`04_arrays_in_depth_methods_and_iteration.md`](./02-javascript/04_arrays_in_depth_methods_and_iteration.md) — Mutating vs Non-mutating methods, custom `reduce` polyfill.
  * [`05_objects_destructuring_rest_spread_and_cloning.md`](./02-javascript/05_objects_destructuring_rest_spread_and_cloning.md) — Destructuring, rest/spread, shallow vs deep cloning, `structuredClone`.
  * [`06_functions_first_class_higher_order.md`](./02-javascript/06_functions_first_class_higher_order.md) — First-class functions, pure functions, higher-order functions.
* **Intermediate Engine & OOP:**
  * [`07_execution_context_call_stack.md`](./02-javascript/07_execution_context_call_stack.md) — Global vs Function execution contexts, Call Stack, stack overflow.
  * [`08_closures_and_lexical_scope.md`](./02-javascript/08_closures_and_lexical_scope.md) — Lexical scope, closure heap cells, data privacy, memoization.
  * [`09_this_keyword_and_binding.md`](./02-javascript/09_this_keyword_and_binding.md) — Implicit, explicit (`call`/`apply`/`bind`), `new` binding, arrow functions.
  * [`10_prototypes_and_inheritance.md`](./02-javascript/10_prototypes_and_inheritance.md) — Prototype chain, `__proto__` vs `prototype`, prototypal inheritance.
  * [`11_es6_classes_under_the_hood.md`](./02-javascript/11_es6_classes_under_the_hood.md) — ES6 `class` syntactic sugar desugared to constructor functions, private fields.
* **Advanced Engine Internals & Web APIs:**
  * [`12_v8_memory_garbage_collection.md`](./02-javascript/12_v8_memory_garbage_collection.md) — V8 Heap & Stack, Generational Scavenger & Mark-Sweep-Compact GC.
  * [`13_event_loop_microtasks_macrotasks.md`](./02-javascript/13_event_loop_microtasks_macrotasks.md) — Single-threaded execution model, Microtask vs Macrotask queues, UI render ticks.
  * [`14_promises_deep_dive.md`](./02-javascript/14_promises_deep_dive.md) — Promise lifecycle states, hand-coded `Promise.all` & `Promise.allSettled`.
  * [`15_async_await_generators_iterators.md`](./02-javascript/15_async_await_generators_iterators.md) — `async/await` desugared into Generators + Promises, `Symbol.iterator`.
  * [`16_modules_cjs_vs_esm.md`](./02-javascript/16_modules_cjs_vs_esm.md) — CommonJS (`require`) vs ES Modules (`import`), dynamic imports, tree-shaking.
  * [`17_proxy_and_reflect_api.md`](./02-javascript/17_proxy_and_reflect_api.md) — Metaprogramming, interception traps (`get`/`set`), and `Reflect` API.
  * [`18_dom_events_delegation_bubbling.md`](./02-javascript/18_dom_events_delegation_bubbling.md) — Event Capturing vs Bubbling phases, Event Delegation pattern.
* **Master Interview Question Bank (100 Questions):**
  * [`interview-questions/README.md`](./02-javascript/interview-questions/README.md) — 100 Deep Dive Questions: Types & Operators, Closures & Scope, Prototypes & Classes, Event Loop & Promises, V8 Heap & DOM Events.

### 03. 🟦 TypeScript Engineering & Type Systems ([`03-typescript/`](./03-typescript/))
* **Core Topics:** Basic types, Unions & Intersections, Interfaces vs Type Aliases, Generics & Constraints, Conditional Types & `infer`, Mapped Types & Template Literals, Utility Types from scratch, Function Utility Types, Nominal Branding, `.d.ts` Ambient declarations, `tsconfig.json` architecture.
* **Master Interview Question Bank (50 Questions):**
  * [`interview-questions/README.md`](./03-typescript/interview-questions/README.md) — 50 Deep Dive Questions: Types & Generics (Q1-Q25), Advanced Types, `infer` & Compiler Internals (Q26-Q50).

### 04. ⚛️ React & Concurrent Architecture ([`04-react/`](./04-react/))
* **Core Topics:** Fiber Reconciler, Virtual DOM diffing & keys, State hooks & linked lists, `useEffect` vs `useLayoutEffect`, Memoization (`useMemo`/`useCallback`/`React.memo`), Context API vs Zustand, Custom hooks, Suspense & Streaming SSR, React 19 Actions.
* **Master Interview Question Bank (100 Questions):**
  * [`interview-questions/README.md`](./04-react/interview-questions/README.md) — 100 Deep Dive Questions: VDOM & JSX, Hooks Internals, Fiber Reconciliation, Performance & Memoization, Server Components & React 19.

### 05. 🅰️ Modern Angular 21 Architecture ([`05-angular-21/`](./05-angular-21/))
* [`01_angular21_signals_and_reactivity.md`](./05-angular-21/01_angular21_signals_and_reactivity.md) — Writable signals, `computed()`, `effect()`, signal inputs.
* [`02_angular21_zoneless_architecture.md`](./05-angular-21/02_angular21_zoneless_architecture.md) — Angular 21 default zoneless change detection and signal dirty marking.
* [`03_angular21_defer_block_and_lazy_loading.md`](./05-angular-21/03_angular21_defer_block_and_lazy_loading.md) — `@defer`, `@placeholder`, `@loading`, `@error` triggers.
* [`04_angular21_standalone_components_and_inject.md`](./05-angular-21/04_angular21_standalone_components_and_inject.md) — Standalone components, `inject()` API, functional guards.
* [`05_angular21_rxjs_interop_to_signal.md`](./05-angular-21/05_angular21_rxjs_interop_to_signal.md) — `toSignal()` and `toObservable()` bridging.
* [`06_angular21_built_in_control_flow_and_optimization.md`](./05-angular-21/06_angular21_built_in_control_flow_and_optimization.md) — Built-in `@if`, `@for` with mandatory `track`, `@empty`, `@switch`, migration from `*ngFor`/`*ngIf`.
* [`07_angular21_signal_inputs_outputs_model_and_queries.md`](./05-angular-21/07_angular21_signal_inputs_outputs_model_and_queries.md) — Signal queries (`input()`, `output()`, `model()`, `viewChild()`, `viewChildren()`, `contentChild()`).
* [`08_angular21_modern_routing_functional_guards_and_interceptors.md`](./05-angular-21/08_angular21_modern_routing_functional_guards_and_interceptors.md) — Functional `CanActivateFn`, `RedirectCommand`, `withComponentInputBinding`, functional `HttpInterceptorFn`.
* **Master Interview Question Bank (50 Questions):**
  * [`interview-questions/README.md`](./05-angular-21/interview-questions/README.md) — 50 Deep Dive Questions: Signals & Zoneless Reactivity (Q1-Q25), Architecture, SSR & Performance (Q26-Q50).

### 06. ▲ Next.js 15 Fullstack Framework ([`06-nextjs/`](./06-nextjs/))
* [`01_app_router_and_react_server_components.md`](./06-nextjs/01_app_router_and_react_server_components.md) — Server Components vs Client Components.
* [`02_server_actions_and_mutations.md`](./06-nextjs/02_server_actions_and_mutations.md) — Type-safe RPC mutations with `"use server"` and Zod validation.
* [`03_caching_and_revalidation_deep_dive.md`](./06-nextjs/03_caching_and_revalidation_deep_dive.md) — 4-tier Caching (Request Memoization, Data Cache, Full Route, Router Cache).
* [`04_middleware_and_authentication.md`](./06-nextjs/04_middleware_and_authentication.md) — Edge routing, auth guards, and rewrite headers.
* [`05_streaming_ssr_and_partial_prerendering.md`](./06-nextjs/05_streaming_ssr_and_partial_prerendering.md) — Streaming SSR with React Suspense, Partial Prerendering (PPR), Next.js 15 async Request APIs (`cookies()`, `headers()`).
* [`06_parallel_and_intercepting_routes.md`](./06-nextjs/06_parallel_and_intercepting_routes.md) — Parallel routes (`@slot`), Intercepting routes (`(..)photo`), shareable modal architecture, and `default.tsx`.
* **Master Interview Question Bank (50 Questions):**
  * [`interview-questions/README.md`](./06-nextjs/interview-questions/README.md) — 50 Deep Dive Questions: App Router, RSC & Server Actions (Q1-Q25), Caching, Streaming & Production Operations (Q26-Q50).

### 07. 🟢 Backend Node.js & Express ([`07-backend-node/`](./07-backend-node/))
* [`01_libuv_event_loop_phases.md`](./07-backend-node/01_libuv_event_loop_phases.md) — Libuv 6 event loop phases.
* [`02_streams_buffers_and_backpressure.md`](./07-backend-node/02_streams_buffers_and_backpressure.md) — Binary chunks, `highWaterMark`, and backpressure drainage.
* [`03_worker_threads_cluster_and_scaling.md`](./07-backend-node/03_worker_threads_cluster_and_scaling.md) — Cluster multi-process vs Worker Threads shared memory.
* [`04_memory_leaks_and_profiling.md`](./07-backend-node/04_memory_leaks_and_profiling.md) — Programmatic heap snapshots and leak diagnostics.
* [`express/01_express_architecture_and_routing.md`](./07-backend-node/express/01_express_architecture_and_routing.md) — Express middleware pipeline and modular routers.
* [`express/03_express_error_handling_and_logging.md`](./07-backend-node/express/03_express_error_handling_and_logging.md) — Centralized error middleware and SIGTERM graceful shutdown.
* **Master Interview Question Bank (60 Questions):**
  * [`interview-questions/README.md`](./07-backend-node/interview-questions/README.md) — 60 Deep Dive Questions: Libuv Event Loop & Concurrency (Q1-Q20), Streams & Memory (Q21-Q40), Express & Production Scaling (Q41-Q60).


### 08. 🐍 Python Core & FastAPI Enterprise ([`08-backend-python-fastapi/`](./08-backend-python-fastapi/))
* **Python Core Foundations:**
  * [`01_python_fundamentals_syntax_types_and_mutability.md`](./08-backend-python-fastapi/01_python_fundamentals_syntax_types_and_mutability.md) — CPython execution model, dynamic typing, variables as name bindings, memory mutability vs immutability, `id()`, `is` vs `==`, small integer caching.
  * [`02_python_collections_lists_tuples_dicts_sets.md`](./08-backend-python-fastapi/02_python_collections_lists_tuples_dicts_sets.md) — `list` over-allocation resizing formula, `tuple` immutability & hashability, `set` hash table operations, Python 3.7+ Compact Dict split-table architecture.
  * [`03_python_functions_scopes_args_kwargs_and_decorators.md`](./08-backend-python-fastapi/03_python_functions_scopes_args_kwargs_and_decorators.md) — First-class functions, `*args`/`**kwargs`, LEGB rule, closures (`__closure__`), decorator factories with arguments, `@functools.wraps`.
  * [`04_python_oop_classes_dunder_methods_and_mro.md`](./08-backend-python-fastapi/04_python_oop_classes_dunder_methods_and_mro.md) — `__init__` vs `__new__`, `@classmethod`, `@staticmethod`, `@property`, dunder methods, C3 Linearization (MRO), cooperative `super()`.
  * [`05_python_generators_iterators_and_context_managers.md`](./08-backend-python-fastapi/05_python_generators_iterators_and_context_managers.md) — Iteration protocol (`__iter__`, `__next__`), `yield` state suspension, generator expressions, `with` statement, `__enter__`/`__exit__`.
  * [`06_python_memory_gc_gil_and_concurrency.md`](./08-backend-python-fastapi/06_python_memory_gc_gil_and_concurrency.md) — Reference counting (`ob_refcnt`), Cyclic GC generations, Global Interpreter Lock (GIL) internals, and concurrency matrix (`multiprocessing` vs `threading` vs `asyncio`).
  * [`07_python_exceptions_typing_and_modern_features.md`](./08-backend-python-fastapi/07_python_exceptions_typing_and_modern_features.md) — Exception hierarchy, `try-except-else-finally`, explicit exception chaining (`raise ... from`), Static typing with `typing.Protocol`, Walrus operator (`:=`), Structural Pattern Matching (`match-case`).
* **Advanced Asyncio & FastAPI Framework:**
  * [`08_asyncio_event_loop_and_concurrency.md`](./08-backend-python-fastapi/08_asyncio_event_loop_and_concurrency.md) — Python `asyncio` cooperative multitasking, Coroutines, Tasks, and worker threading.
  * [`09_pydantic_v2_validation_and_serialization.md`](./08-backend-python-fastapi/09_pydantic_v2_validation_and_serialization.md) — Rust-powered validation core, field and model validators, and high-throughput serialization.
  * [`10_dependency_injection_system.md`](./08-backend-python-fastapi/10_dependency_injection_system.md) — FastAPI `Depends()` DAG and `yield` resource teardown.
  * [`11_background_tasks_and_celery.md`](./08-backend-python-fastapi/11_background_tasks_and_celery.md) — In-process tasks vs distributed Celery queues.
  * [`12_high_performance_asgi_starlette_uvicorn.md`](./08-backend-python-fastapi/12_high_performance_asgi_starlette_uvicorn.md) — ASGI architecture, Uvicorn, and `def` vs `async def` threadpools.
* **Master Interview Question Bank (100 Questions):**
  * [`interview-questions/README.md`](./08-backend-python-fastapi/interview-questions/README.md) — 100 Deep Dive Questions: Python Core (Q1-Q20), OOP & Dunder (Q21-Q40), Asyncio & GIL (Q41-Q60), FastAPI & Pydantic (Q61-Q80), SQLAlchemy & Celery (Q81-Q100).

### 09. ☕ Core Java 21 & Spring Boot 3 ([`09-backend-java-springboot/`](./09-backend-java-springboot/))
* **Core Java Foundations (Newbie to Experienced):**
  * [`01_java_fundamentals_jvm_primitives_and_pass_by_value.md`](./09-backend-java-springboot/01_java_fundamentals_jvm_primitives_and_pass_by_value.md) — Bytecode compilation (`javac`), JVM ClassLoader, Tiered JIT (C1/C2), 8 Primitive types vs Wrapper classes, Integer Cache (`[-128, 127]`), and Pass-by-value proof.
  * [`02_java_strings_memory_string_pool_stringbuilder.md`](./09-backend-java-springboot/02_java_strings_memory_string_pool_stringbuilder.md) — String immutability rationale, String Constant Pool (SCP) in Heap, `String.intern()`, `StringBuilder` vs `StringBuffer`, and `equals()` & `hashCode()` contract.
  * [`03_java_oop_encapsulation_inheritance_polymorphism_abstraction.md`](./09-backend-java-springboot/03_java_oop_encapsulation_inheritance_polymorphism_abstraction.md) — 4 OOP Pillars, dynamic dispatch via Metaspace vtable, Abstract Classes vs Interfaces, Java 8/9 default/private methods, and `final` mechanics.
  * [`04_java_collections_framework_list_set_queue_map.md`](./09-backend-java-springboot/04_java_collections_framework_list_set_queue_map.md) — JCF architecture: `ArrayList` ($1.5\times$ resizing) vs `LinkedList`, `HashSet` vs `TreeSet`, `HashMap` bucket treeification (Red-Black Tree after 8 elements), Fail-Fast vs Fail-Safe.
  * [`05_java_generics_wildcards_and_type_erasure.md`](./09-backend-java-springboot/05_java_generics_wildcards_and_type_erasure.md) — Type parameters, Bounded types, PECS Principle (**Producer Extends, Consumer Super**), and Type Erasure under the hood.
  * [`06_java_exception_handling_and_try_with_resources.md`](./09-backend-java-springboot/06_java_exception_handling_and_try_with_resources.md) — `Throwable` hierarchy (`Error` vs `Exception`), Checked vs Unchecked, `try-catch-finally`, Java 7+ `try-with-resources` with `AutoCloseable`.
  * [`07_java_modern_features_streams_lambdas_records_sealed.md`](./09-backend-java-springboot/07_java_modern_features_streams_lambdas_records_sealed.md) — Functional Interfaces (`Predicate`, `Function`), Stream API lazy pipelines, immutable `record` types, `sealed` classes, and Java 21 `switch` pattern matching.
* **Advanced Java 21 High-Concurrency Internals:**
  * [`08_concurrenthashmap_and_thread_safe_collections.md`](./09-backend-java-springboot/08_concurrenthashmap_and_thread_safe_collections.md) — HashMap bucket treeification, `ConcurrentHashMap` CAS and synchronized bucket head locking.
  * [`09_jvm_garbage_collectors_zgc_g1_tuning.md`](./09-backend-java-springboot/09_jvm_garbage_collectors_zgc_g1_tuning.md) — Generational ZGC ($< 1\text{ms}$ pauses) vs G1 GC tuning.
  * [`10_java21_virtual_threads_and_structured_concurrency.md`](./09-backend-java-springboot/10_java21_virtual_threads_and_structured_concurrency.md) — Project Loom Virtual Threads vs Platform OS Threads, carrier unmounting.
* **Enterprise Spring Boot 3 Microservices:**
  * [`11_springboot_architecture_and_jvm.md`](./09-backend-java-springboot/11_springboot_architecture_and_jvm.md) — IoC container, JVM memory spaces, and GC collectors.
  * [`12_springboot_security_jwt_oauth2.md`](./09-backend-java-springboot/12_springboot_security_jwt_oauth2.md) — `SecurityFilterChain`, stateless sessions, and `@PreAuthorize`.
  * [`13_springboot_microservices_and_resilience4j.md`](./09-backend-java-springboot/13_springboot_microservices_and_resilience4j.md) — Resilience4j Circuit Breakers, Retry policies, and tracing.
* **Master Interview Question Bank (100 Questions):**
  * [`interview-questions/README.md`](./09-backend-java-springboot/interview-questions/README.md) — 100 Deep Dive Questions: JVM & Memory (Q1-Q20), OOP & Collections (Q21-Q40), Concurrency & Virtual Threads (Q41-Q60), Spring Boot Core (Q61-Q80), Security & Microservices (Q81-Q100).

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
* **Master Interview Question Bank (60 Questions):**
  * [`interview-questions/README.md`](./11-databases-and-caching/interview-questions/README.md) — 60 Deep Dive Questions: SQL & PostgreSQL Internals (Q1-Q20), Redis Caching & Distributed Systems (Q21-Q40), NoSQL & MongoDB Architecture (Q41-Q60).

### 12. 🤖 AI & GenAI Systems Engineering ([`12-ai-and-genai/`](./12-ai-and-genai/))
* **01. LLM Foundations & Transformers:**
  * [`01-llm-foundations/01_llm_fundamentals_tokens_context_and_sampling.md`](./12-ai-and-genai/01-llm-foundations/01_llm_fundamentals_tokens_context_and_sampling.md) — Next-token prediction, BPE Tokenization, Context Window limits, Temperature, Top-P, Top-K, Frequency/Presence penalties.
  * [`01-llm-foundations/02_transformer_architecture_and_self_attention.md`](./12-ai-and-genai/01-llm-foundations/02_transformer_architecture_and_self_attention.md) — Scaled Dot-Product Attention, $Q, K, V$ intuition, Multi-Head Attention, RoPE (Rotary Position Embeddings), KV-Cache, and FlashAttention.
  * [`01-llm-foundations/03_prompt_engineering_cot_and_structured_outputs.md`](./12-ai-and-genai/01-llm-foundations/03_prompt_engineering_cot_and_structured_outputs.md) — Zero-shot, Few-shot in-context learning, Chain-of-Thought (CoT), Tree of Thoughts (ToT), Constrained Decoding, and Pydantic JSON Schemas.
* **02. Embeddings & Vector Databases:**
  * [`02-embeddings-and-vector-databases/01_embeddings_vector_spaces_and_similarity_metrics.md`](./12-ai-and-genai/02-embeddings-and-vector-databases/01_embeddings_vector_spaces_and_similarity_metrics.md) — Dense embeddings, Cosine Similarity vs Dot Product vs Euclidean ($L_2$), $L_2$ normalization, Bi-Encoders vs Cross-Encoders, Matryoshka embeddings.
  * [`02-embeddings-and-vector-databases/02_vector_databases_hnsw_and_indexing.md`](./12-ai-and-genai/02-embeddings-and-vector-databases/02_vector_databases_hnsw_and_indexing.md) — HNSW multi-layer skip graphs ($M$, $efConstruction$, $efSearch$), IVF-PQ quantization, Single-stage metadata pre-filtering, Chroma, Qdrant, Pinecone, and Milvus.
* **03. Retrieval-Augmented Generation (RAG):**
  * [`03-retrieval-augmented-generation-rag/01_rag_architecture_chunking_and_retrieval.md`](./12-ai-and-genai/03-retrieval-augmented-generation-rag/01_rag_architecture_chunking_and_retrieval.md) — Naive RAG vs Production RAG, Recursive character splitting, Semantic chunking, Parent-Document (Small-to-Big) chunking, and Grounded citation prompts.
  * [`03-retrieval-augmented-generation-rag/02_advanced_rag_hybrid_search_and_reranking.md`](./12-ai-and-genai/03-retrieval-augmented-generation-rag/02_advanced_rag_hybrid_search_and_reranking.md) — Sparse BM25 lexical search + Dense vector search, Reciprocal Rank Fusion (RRF: $k=60$), and Cross-Encoder Re-ranking (Cohere / BGE-Reranker).
  * [`03-retrieval-augmented-generation-rag/03_query_transformation_hyde_and_multimodal_rag.md`](./12-ai-and-genai/03-retrieval-augmented-generation-rag/03_query_transformation_hyde_and_multimodal_rag.md) — HyDE (Hypothetical Document Embeddings), Sub-Query decomposition, Step-back prompting, and Multimodal Vision RAG (ColPali).
* **04. Orchestration (LangChain & LangFlow):**
  * [`04-orchestration-langchain-and-langflow/01_langchain_core_lcel_and_runnables.md`](./12-ai-and-genai/04-orchestration-langchain-and-langflow/01_langchain_core_lcel_and_runnables.md) — LangChain Expression Language pipe operator (`|`), `ChatPromptTemplate`, `ChatModel`, `StrOutputParser`, `RunnableParallel`, `RunnablePassthrough`, streaming (`astream`).
  * [`04-orchestration-langchain-and-langflow/02_langchain_chains_memory_and_tools.md`](./12-ai-and-genai/04-orchestration-langchain-and-langflow/02_langchain_chains_memory_and_tools.md) — ConversationSummaryBufferMemory, Token budget management, Custom Tools via `@tool` decorator, Structured tools with Pydantic arguments.
  * [`04-orchestration-langchain-and-langflow/03_langflow_visual_ai_prototyping_and_architecture.md`](./12-ai-and-genai/04-orchestration-langchain-and-langflow/03_langflow_visual_ai_prototyping_and_architecture.md) — LangFlow low-code canvas, Component nodes, Graph serialization to JSON, Headless REST API deployment, and exporting visual canvas to clean Python code.
* **05. Agentic AI & LangGraph:**
  * [`05-agentic-ai-and-langgraph/01_agentic_ai_react_pattern_and_tool_calling.md`](./12-ai-and-genai/05-agentic-ai-and-langgraph/01_agentic_ai_react_pattern_and_tool_calling.md) — ReAct loop (Thought $\to$ Action $\to$ Observation), Native Tool Calling protocols (OpenAI, Anthropic schemas), Self-healing exception loops, and Stopping guardrails.
  * [`05-agentic-ai-and-langgraph/02_langgraph_state_machines_and_agentic_workflows.md`](./12-ai-and-genai/05-agentic-ai-and-langgraph/02_langgraph_state_machines_and_agentic_workflows.md) — LangGraph StateGraph, Cycles vs DAGs, Reducers (`Annotated[..., operator.add]`), Conditional edge routers, Checkpointing (`PostgresSaver`), and Human-in-the-Loop (`interrupt_before`).
  * [`05-agentic-ai-and-langgraph/03_multi_agent_systems_and_hierarchical_orchestration.md`](./12-ai-and-genai/05-agentic-ai-and-langgraph/03_multi_agent_systems_and_hierarchical_orchestration.md) — Multi-agent collaboration topologies, Centralized Supervisor pattern, Isolated sub-agent scratchpads, Recursion ceilings, and Preventing infinite conversational loops.
* **06. Fine-Tuning & Serving:**
  * [`06-fine-tuning-and-serving/01_fine_tuning_lora_qlora_and_peft.md`](./12-ai-and-genai/06-fine-tuning-and-serving/01_fine_tuning_lora_qlora_and_peft.md) — When to Fine-Tune vs RAG, Parameter-Efficient Fine-Tuning (PEFT), LoRA math ($W = W_0 + \frac{\alpha}{r} BA$), QLoRA 4-bit NF4, Double Quantization, Paged Optimizers, SFT vs DPO.
  * [`06-fine-tuning-and-serving/02_production_serving_vllm_paged_attention_and_quantization.md`](./12-ai-and-genai/06-fine-tuning-and-serving/02_production_serving_vllm_paged_attention_and_quantization.md) — High-throughput serving, KV-Cache memory bottleneck, PagedAttention block tables, Continuous Batching (Iteration-level), AWQ vs GPTQ vs GGUF quantization, Speculative Decoding.
* **07. Guardrails, Security & Evaluation:**
  * [`07-guardrails-security-and-evaluation/01_guardrails_security_and_prompt_injection.md`](./12-ai-and-genai/07-guardrails-security-and-evaluation/01_guardrails_security_and_prompt_injection.md) — Direct & Indirect prompt injection, Jailbreaking, System prompt extraction, NeMo Guardrails, Input/Output PII scrubbing (Presidio), Data exfiltration countermeasures.
  * [`07-guardrails-security-and-evaluation/02_llm_evaluation_ragas_and_benchmarking.md`](./12-ai-and-genai/07-guardrails-security-and-evaluation/02_llm_evaluation_ragas_and_benchmarking.md) — LLM-as-a-Judge, The RAG Triad (Context Relevance, Faithfulness/Groundedness, Answer Relevance), Ragas & DeepEval frameworks, Mitigating judge bias (position, verbosity).
* **Master 110 Interview Questions & System Design Scenarios:**
  * [`interview-questions/README.md`](./12-ai-and-genai/interview-questions/README.md) — Master 110 Questions Index & Curriculum Matrix.
  * [`interview-questions/01_foundations_and_transformers_qna.md`](./12-ai-and-genai/interview-questions/01_foundations_and_transformers_qna.md) — Questions 1 to 20.
  * [`interview-questions/02_embeddings_and_vectordb_qna.md`](./12-ai-and-genai/interview-questions/02_embeddings_and_vectordb_qna.md) — Questions 21 to 40.
  * [`interview-questions/03_rag_and_retrieval_qna.md`](./12-ai-and-genai/interview-questions/03_rag_and_retrieval_qna.md) — Questions 41 to 60.
  * [`interview-questions/04_langchain_langflow_langgraph_agents_qna.md`](./12-ai-and-genai/interview-questions/04_langchain_langflow_langgraph_agents_qna.md) — Questions 61 to 80.
  * [`interview-questions/05_finetuning_serving_and_ops_qna.md`](./12-ai-and-genai/interview-questions/05_finetuning_serving_and_ops_qna.md) — Questions 81 to 100.
  * [`interview-questions/06_scenario_based_system_design_ai_qna.md`](./12-ai-and-genai/interview-questions/06_scenario_based_system_design_ai_qna.md) — Questions 101 to 110 (Complex System Design Scenarios).
  * [`interview-questions/coding_simple_rag_pipeline_python.md`](./12-ai-and-genai/interview-questions/coding_simple_rag_pipeline_python.md) — Pure Python Vector Store & RAG pipeline from scratch.

### 13. 🏗️ System Design (HLD & LLD) ([`13-system-design/`](./13-system-design/))
* **Core Foundations & 50 Concepts Playbook:**
  * [`00_master_50_system_design_concepts.md`](./13-system-design/00_master_50_system_design_concepts.md) — Complete 50 concepts encyclopedia across Scalability, Consensus, Caching, Protocols, and Resilience.
  * [`07_distributed_systems_primitives_consensus_cap_sharding.md`](./13-system-design/07_distributed_systems_primitives_consensus_cap_sharding.md) — CAP Theorem, Raft Consensus (Leader Election & Log Replication), Consistent Hashing with Virtual Nodes.
  * [`08_resilience_and_stability_patterns.md`](./13-system-design/08_resilience_and_stability_patterns.md) — Circuit Breaker state machine, Bulkhead isolation, Exponential Backoff + Jitter, XFetch Cache Stampede avoidance.
  * [`09_communication_protocols_rest_graphql_grpc_webrtc_websockets.md`](./13-system-design/09_communication_protocols_rest_graphql_grpc_webrtc_websockets.md) — REST vs GraphQL vs gRPC (HTTP/2) vs WebSockets vs WebRTC.
  * [`10_event_driven_streaming_batch_mapreduce.md`](./13-system-design/10_event_driven_streaming_batch_mapreduce.md) — Message Queues vs Event Streams, At-least-once / Exactly-once idempotency, Lambda vs Kappa architecture.
  * [`11_observability_deployments_bluegreen_canary.md`](./13-system-design/11_observability_deployments_bluegreen_canary.md) — Distributed Tracing, Correlation IDs, Structured Logging, Blue-Green & Canary Zero-Downtime deployments.
* **High-Level Design (HLD):**
  * [`01_hld_url_shortener_tinyurl.md`](./13-system-design/01_hld_url_shortener_tinyurl.md) — Base62 encoding, Key Generation Service (KGS).
  * [`02_hld_whatsapp_realtime_chat.md`](./13-system-design/02_hld_whatsapp_realtime_chat.md) — WebSockets, Kafka, Presence servers, Cassandra.
  * [`03_hld_netflix_video_streaming.md`](./13-system-design/03_hld_netflix_video_streaming.md) — Transcoding pipeline, HLS/DASH chunks, Open Connect CDN.
  * [`04_hld_uber_ride_matching_spatial_indexing.md`](./13-system-design/04_hld_uber_ride_matching_spatial_indexing.md) — Uber H3 hexagonal spatial indexing, real-time dispatch.
* **Low-Level Design (LLD):**
  * [`05_lld_parking_lot_system.md`](./13-system-design/05_lld_parking_lot_system.md) — Multi-floor OOP design, Factory & Strategy patterns.
  * [`06_lld_distributed_rate_limiter.md`](./13-system-design/06_lld_distributed_rate_limiter.md) — Token Bucket and Sliding Window algorithms in Python.
* **Master Interview Question Bank (100 Questions):**
  * [`interview-questions/README.md`](./13-system-design/interview-questions/README.md) — 100 Deep Dive Questions: Fundamentals & Scale (Q1-Q20), Distributed Consensus & Consistency (Q21-Q40), Event-Driven & Streaming (Q41-Q60), Protocols & SRE Resilience (Q61-Q80), Top 20 HLD Case Studies (Q81-Q100).
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
* **Master Interview Question Bank (50 Questions):**
  * [`interview-questions/README.md`](./15-testing-and-devops/interview-questions/README.md) — 50 Deep Dive Questions: Jest, RTL & Playwright (Q1-Q25), Docker, Kubernetes & CI/CD (Q26-Q50).


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
