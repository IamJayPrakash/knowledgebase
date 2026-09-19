# 🧠 The Universal Tech & Senior Interview Knowledge Base

> A comprehensive, zero-to-advanced engineering reference and technical interview preparation guide for **Software Engineers, Senior Technical Leads, Full-Stack Developers (MERN/MEAN), AI/LLM Engineers, and System Architects (0 to 8+ Years Experience)**.

---

## 🌟 The "6-Pillar" Learning Standard

Every single concept, architectural guide, and LeetCode problem in this repository is authored strictly adhering to the **6-Pillar Pedagogical Gold Standard**:
1. 🐣 **Layman's Analogy (Hinglish & Everyday Real-World ELI5):** Crystal-clear everyday intuition so anyone, from absolute beginners to experienced engineers, grasps concepts effortlessly.
2. 📌 **Point-Wise Core Mechanics & Edge Cases:** Concise breakdown of what happens under the hood without confusing academic jargon.
3. 📊 **Visual ASCII & Mermaid Diagrams:** Direct visual mapping of data structures, runtime memory models, execution event loops, and distributed cloud architectures.
4. 💻 **Practical Code Implementations:** Naive/brute-force vs optimal solutions with **line-by-line comments** in JavaScript, TypeScript, and Python.
5. 🎯 **The "Interview Pitch":** Exact, natural English phrasing to explain the concept confidently and authoritatively to an interviewer.
6. 💼 **Production War Story (STAR Method):** Real-world project scenarios detailing the Situation, Task, Action, and Business/System Metrics ($ \downarrow $ Latency, $ \uparrow $ Throughput, 0 outages).

---

## 🗺️ Master Curriculum & Interactive Index

```text
knowledgebase/
├── 01-core-web-and-performance/      # Web Core Vitals (LCP, INP, CLS), Critical Rendering Path, Media Optimization
├── 01-javascript/                    # V8 Engine, Event Loop, Closures, Prototypes, ES6 Classes, CJS vs ESM, DOM Events
├── 02-typescript/                    # Interfaces vs Types, Generics, infer, Conditional Types, Mapped Types, Nominal Branding
├── 03-react/                         # Virtual DOM, Fiber Reconciler, Hooks Deep Dive, Memoization, React 19 Actions
├── 04-frontend-frameworks/           # Next.js App Router (RSC, Server Actions, Caching), Angular 21 (Zoneless, Signals)
├── 04-node/                          # Libuv Event Loop (6 phases), Streams & Backpressure, Worker Threads, Memory Profiling
├── 05-fastapi/                       # Python Asyncio, Pydantic V2, ASGI/Starlette, Dependency Injection, Rate Limiting
├── 05-backend-and-runtimes/          # Ruby on Rails (Active Record, Sidekiq), MEAN vs MERN, Java Spring Boot 3
├── 06-databases-and-caching/         # PostgreSQL (MVCC, Partitioning), Redis (Data structures, Redlock), MongoDB Aggregation
├── 06-ai-genai/                      # Vector DBs (HNSW), RAG Pipelines, LangGraph Agents, LoRA Fine-Tuning, vLLM Serving
├── 07-system-design/                 # HLD (Netflix, Uber, TinyURL, WhatsApp), LLD (Parking Lot, Rate Limiter)
├── 08-leetcode-dsa/                  # 🧮 Complete Blind 75 Solutions with 3 Evolution Versions, Visuals & War Stories!
├── 09-interview-cheatsheet/          # 5-Minute Quick Recall Cards, System Design Cheat Sheet, Behavioral STAR Guide
├── 10-testing-and-devops/            # Playwright E2E, Jest Unit Testing, Docker Multi-Stage, Kubernetes (Helm, HPA)
└── 11-interview-master-cheatsheets/  # TCS, Infosys, Wipro, Cognizant, Capgemini, JLL, Nagarro & Startup Tech Lead Guides
```

---

## 🗂️ Module Directory & Direct Links

### 1. ⚡ Web Performance & Core Web Vitals
* [`01_core_web_vitals_lcp_inp_cls.md`](./01-core-web-and-performance/web-core-vitals/01_core_web_vitals_lcp_inp_cls.md) — Largest Contentful Paint (LCP), Interaction to Next Paint (INP), Cumulative Layout Shift (CLS).
* [`02_inp_interaction_to_next_paint_deep_dive.md`](./01-core-web-and-performance/web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md) — Input delay, presentation delay, breaking long tasks with `scheduler.yield()`.
* [`03_cls_cumulative_layout_shift_debugging.md`](./01-core-web-and-performance/web-core-vitals/03_cls_cumulative_layout_shift_debugging.md) — Image aspect-ratio reservation, ad slots, and font swap jitter.
* [`01_critical_rendering_path_and_paint.md`](./01-core-web-and-performance/frontend-performance-optimization/01_critical_rendering_path_and_paint.md) — DOM, CSSOM, Render Tree, Layout Reflow, Repaint, Composite.
* [`02_bundle_splitting_and_lazy_loading.md`](./01-core-web-and-performance/frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md) — Route-based code splitting, dynamic imports, and tree-shaking.
* [`03_image_and_font_optimization.md`](./01-core-web-and-performance/frontend-performance-optimization/03_image_and_font_optimization.md) — AVIF, WebP, responsive `<picture>` fallbacks, and variable fonts.

### 2. 🟨 JavaScript Core Engine & Asynchronous Internals
* [`01_data_types_and_type_coercion.md`](./01-javascript/01_data_types_and_type_coercion.md) — Primitives, IEEE-754 numbers, Symbol, BigInt, and abstract coercion rules.
* [`02_var_let_const_hoisting_tdz.md`](./01-javascript/02_var_let_const_hoisting_tdz.md) — Lexical environments, Temporal Dead Zone (TDZ), and block scope.
* [`04_execution_context_call_stack.md`](./01-javascript/04_execution_context_call_stack.md) — Global vs Function execution contexts, VariableEnvironment vs LexicalEnvironment.
* [`05_closures_and_lexical_scope.md`](./01-javascript/05_closures_and_lexical_scope.md) — Scope chains, closure memory footprint, and private encapsulation.
* [`06_v8_memory_garbage_collection.md`](./01-javascript/06_v8_memory_garbage_collection.md) — V8 heap spaces, Scavenger Minor GC, and Mark-Sweep-Compact Major GC.
* [`07_this_keyword_and_binding.md`](./01-javascript/07_this_keyword_and_binding.md) — Implicit, explicit (`call`/`apply`/`bind`), `new`, and lexical arrow bindings.
* [`08_prototypes_and_inheritance.md`](./01-javascript/08_prototypes_and_inheritance.md) — `__proto__`, `.prototype`, and prototypal delegation chains.
* [`09_es6_classes_under_the_hood.md`](./01-javascript/09_es6_classes_under_the_hood.md) — Prototypal desugaring, `#private` brand checks, and `super` semantics.
* [`10_event_loop_microtasks_macrotasks.md`](./01-javascript/10_event_loop_microtasks_macrotasks.md) — Microtask checkpoint, macrotasks, and UI rendering ticks.
* [`11_promises_deep_dive.md`](./01-javascript/11_promises_deep_dive.md) — Promise states, chaining mechanics, and custom polyfills.
* [`12_async_await_generators_iterators.md`](./01-javascript/12_async_await_generators_iterators.md) — Async/await desugared to generators and co-routines.
* [`13_modules_cjs_vs_esm.md`](./01-javascript/13_modules_cjs_vs_esm.md) — CommonJS copy evaluation vs ESM live bindings and 3-stage module lifecycle.
* [`14_proxy_and_reflect_api.md`](./01-javascript/14_proxy_and_reflect_api.md) — Metaprogramming traps, reactivity triggers, and data validation.
* [`15_dom_events_delegation_bubbling.md`](./01-javascript/15_dom_events_delegation_bubbling.md) — Capturing, Target, and Bubbling phases, and event delegation architecture.
* **Interview Challenges:**
  * [`output_event_loop_promises.md`](./01-javascript/interview-questions/output_event_loop_promises.md) — Tricky event loop output puzzles with execution traces.
  * [`output_this_binding.md`](./01-javascript/interview-questions/output_this_binding.md) — Tricky `this` binding and arrow function scope puzzles.
  * [`coding_deep_clone.md`](./01-javascript/interview-questions/coding_deep_clone.md) — Deep clone with circular reference detection, WeakMap, Dates, and Sets.
  * [`coding_curry_function.md`](./01-javascript/interview-questions/coding_curry_function.md) — Infinite and generalized function currying.
  * [`coding_event_emitter.md`](./01-javascript/interview-questions/coding_event_emitter.md) — Custom production-grade EventEmitter (`on`, `once`, `off`, `emit`).
  * [`coding_debounce_and_throttle.md`](./01-javascript/interview-questions/coding_debounce_and_throttle.md) — Debounce with immediate flag and throttle with trailing execution.
  * [`coding_polyfill_promise_all.md`](./01-javascript/interview-questions/coding_polyfill_promise_all.md) — Polyfill for `Promise.all` and `Promise.allSettled`.
  * [`scenario_memory_leak_debugging.md`](./01-javascript/interview-questions/scenario_memory_leak_debugging.md) — Step-by-step Chrome DevTools heap snapshot leak diagnostics.

### 3. 🟦 TypeScript Engineering & Type Systems
* [`01_basic_types_any_unknown_never.md`](./02-typescript/01_basic_types_any_unknown_never.md) — Type hierarchies, top types vs bottom type `never`.
* [`02_unions_intersections_type_guards.md`](./02-typescript/02_unions_intersections_type_guards.md) — Discriminated unions, custom type predicates (`is`), and narrowing.
* [`03_interfaces_vs_type_aliases.md`](./02-typescript/03_interfaces_vs_type_aliases.md) — Declaration merging, compiler caching, and architectural decision trees.
* [`04_generics_and_constraints.md`](./02-typescript/04_generics_and_constraints.md) — Generic type parameters, `extends` constraints, and `keyof` lookup.
* [`05_conditional_types_and_infer.md`](./02-typescript/05_conditional_types_and_infer.md) — Conditional algebra, distributive unions, and `infer` pattern extraction.
* [`06_mapped_types_and_template_literals.md`](./02-typescript/06_mapped_types_and_template_literals.md) — Key remapping (`as`), modifier flags (`-readonly`, `-?`), and template literal validation.
* [`07_utility_types_from_scratch.md`](./02-typescript/07_utility_types_from_scratch.md) — Recreating `Partial`, `Pick`, `Omit`, and recursive `DeepReadonly`.
* [`08_function_utility_types.md`](./02-typescript/08_function_utility_types.md) — `Parameters<T>`, `ReturnType<T>`, and `ConstructorParameters<T>` pattern matching.
* [`09_structural_vs_nominal_typing.md`](./02-typescript/09_structural_vs_nominal_typing.md) — Nominal type simulation using unique symbol branding and flavoring.
* [`10_declaration_files_and_ambient_modules.md`](./02-typescript/10_declaration_files_and_ambient_modules.md) — `.d.ts` declaration files, module augmentation, and asset typing.
* [`11_tsconfig_and_compiler_architecture.md`](./02-typescript/11_tsconfig_and_compiler_architecture.md) — `strict: true`, compiler stages, `noUncheckedIndexedAccess`, and build optimization.
* **Interview Challenges:**
  * [`top_typescript_interview_questions.md`](./02-typescript/interview-questions/top_typescript_interview_questions.md) — Covariance vs contravariance, `satisfies` operator, and declaration merging.
  * [`coding_custom_utility_types.md`](./02-typescript/interview-questions/coding_custom_utility_types.md) — `DeepPartial`, `FlattenObjectKeys`, and `RequireAtLeastOne`.

### 4. ⚛️ Modern Frontend Frameworks (React, Next.js, Angular 21)
* **React:**
  * [`01_fiber_reconciler_and_concurrent_mode.md`](./03-react/01_fiber_reconciler_and_concurrent_mode.md) — Fiber node structures, Render vs Commit phases, and `useTransition`.
  * [`03_virtual_dom_jsx_and_diffing.md`](./03-react/03_virtual_dom_jsx_and_diffing.md) — JSX compilation, heuristic $O(N)$ diffing, and stable `key` invariants.
  * [`04_state_hooks_usestate_usereducer.md`](./03-react/04_state_hooks_usestate_usereducer.md) — Hook singly-linked list on Fiber nodes, state updates, and batching.
  * [`05_effect_hooks_useeffect_uselayouteffect.md`](./03-react/05_effect_hooks_useeffect_uselayouteffect.md) — Execution timing, paint blocking, and layout measurement.
  * [`06_memoization_usememo_usecallback_react_memo.md`](./03-react/06_memoization_usememo_usecallback_react_memo.md) — Referential equality, shallow prop checks, and memoization overhead.
  * [`07_context_api_and_state_management.md`](./03-react/07_context_api_and_state_management.md) — Context API re-render cascades vs Zustand/RTK atomic selectors.
  * [`08_custom_hooks_patterns.md`](./03-react/08_custom_hooks_patterns.md) — Reusable hook patterns (`useDebounce`, `useLocalStorage`).
  * [`09_suspense_and_streaming_ssr.md`](./03-react/09_suspense_and_streaming_ssr.md) — Suspense boundary promise throwing, `renderToPipeableStream`, and selective hydration.
  * [`10_react19_actions_use_hook_compiler.md`](./03-react/10_react19_actions_use_hook_compiler.md) — React 19 Actions, `useActionState`, `useOptimistic`, and the React Compiler.
  * **Machine Coding:** [`machine_coding_autocomplete_search.md`](./03-react/interview-questions/machine_coding_autocomplete_search.md), [`machine_coding_virtualized_list.md`](./03-react/interview-questions/machine_coding_virtualized_list.md).
* **Next.js:**
  * [`01_app_router_and_react_server_components.md`](./04-frontend-frameworks/nextjs/01_app_router_and_react_server_components.md) — Server Components vs Client Components.
  * [`02_server_actions_and_mutations.md`](./04-frontend-frameworks/nextjs/02_server_actions_and_mutations.md) — Type-safe RPC mutations, `"use server"`, and form handling.
  * [`03_caching_and_revalidation_deep_dive.md`](./04-frontend-frameworks/nextjs/03_caching_and_revalidation_deep_dive.md) — The 4 caching layers (Request Memoization, Data Cache, Full Route, Router Cache).
  * [`04_middleware_and_authentication.md`](./04-frontend-frameworks/nextjs/04_middleware_and_authentication.md) — Edge routing, auth guards, and rewrite headers.
* **Modern Angular 21:**
  * [`01_angular21_signals_and_reactivity.md`](./04-frontend-frameworks/angular/01_angular21_signals_and_reactivity.md) — Writable signals, `computed()`, `effect()`, and signal inputs.
  * [`02_angular21_zoneless_architecture.md`](./04-frontend-frameworks/angular/02_angular21_zoneless_architecture.md) — Zone.js removal, default zoneless change detection in Angular 21.
  * [`03_angular21_defer_block_and_lazy_loading.md`](./04-frontend-frameworks/angular/03_angular21_defer_block_and_lazy_loading.md) — `@defer`, `@placeholder`, `@loading`, `@error` triggers.
  * [`04_angular21_standalone_components_and_inject.md`](./04-frontend-frameworks/angular/04_angular21_standalone_components_and_inject.md) — Standalone components, `inject()` function, functional guards.
  * [`05_angular21_rxjs_interop_to_signal.md`](./04-frontend-frameworks/angular/05_angular21_rxjs_interop_to_signal.md) — Interop between RxJS Observables and Signals via `toSignal()` & `toObservable()`.
  * [`angular21_top_interview_questions.md`](./04-frontend-frameworks/angular/interview-questions/angular21_top_interview_questions.md) — Senior Angular 21 interview questions and answers.

### 5. 🟢 Backend Runtimes & Full-Stack Architectures
* **Node.js:**
  * [`01_libuv_event_loop_phases.md`](./04-node/01_libuv_event_loop_phases.md) — Timers, Pending, Poll, Check, and Close phases.
  * [`02_streams_buffers_and_backpressure.md`](./04-node/02_streams_buffers_and_backpressure.md) — Chunked binary processing, `highWaterMark`, and backpressure drainage.
  * [`03_worker_threads_cluster_and_scaling.md`](./04-node/03_worker_threads_cluster_and_scaling.md) — Multi-process Cluster scaling vs multi-threaded V8 Worker Threads.
  * [`04_memory_leaks_and_profiling.md`](./04-node/04_memory_leaks_and_profiling.md) — Programmatic heap snapshots (`v8.writeHeapSnapshot()`) and leak remediation.
* **Express.js:**
  * [`01_express_architecture_and_routing.md`](./05-backend-and-runtimes/node-express/01_express_architecture_and_routing.md) — Middleware chain of responsibility, async route handling, and Router layering.
  * [`02_express_middleware_architecture_and_pipeline.md`](./05-backend-and-runtimes/node-express/02_express_middleware_architecture_and_pipeline.md) — Rate limiting, CORS, and request sanitation pipelines.
  * [`03_express_error_handling_and_logging.md`](./05-backend-and-runtimes/node-express/03_express_error_handling_and_logging.md) — Centralized error handlers and graceful SIGTERM shutdown.
* **Python FastAPI:**
  * [`01_asyncio_event_loop_and_concurrency.md`](./05-fastapi/01_asyncio_event_loop_and_concurrency.md) — Coroutines, event loops, and non-blocking I/O.
  * [`02_pydantic_v2_validation_and_serialization.md`](./05-fastapi/02_pydantic_v2_validation_and_serialization.md) — Rust-powered validation core, field validators, and model dump.
  * [`03_dependency_injection_system.md`](./05-fastapi/03_dependency_injection_system.md) — Declarative `Depends()`, hierarchical DAGs, and `yield` resource cleanup.
  * [`04_background_tasks_and_celery.md`](./05-fastapi/04_background_tasks_and_celery.md) — In-process `BackgroundTasks` vs distributed Celery workers with Redis.
  * [`05_high_performance_asgi_starlette_uvicorn.md`](./05-fastapi/05_high_performance_asgi_starlette_uvicorn.md) — Uvicorn, uvloop, and the `def` vs `async def` threadpool mechanics.
* **Java Spring Boot 3 & Enterprise:**
  * [`01_springboot_architecture_and_jvm.md`](./05-backend-and-runtimes/java-springboot/01_springboot_architecture_and_jvm.md) — IoC container, JVM memory spaces, and GC collectors.
  * [`02_springboot_security_jwt_oauth2.md`](./05-backend-and-runtimes/java-springboot/02_springboot_security_jwt_oauth2.md) — `SecurityFilterChain`, stateless sessions, and `@PreAuthorize`.
  * [`03_springboot_microservices_and_resilience4j.md`](./05-backend-and-runtimes/java-springboot/03_springboot_microservices_and_resilience4j.md) — Resilience4j Circuit Breakers, Retry policies, and OpenTelemetry tracing.
* **Ruby on Rails & Fullstack Paradigms:**
  * [`01_ruby_on_rails_mvc_active_record.md`](./05-backend-and-runtimes/ruby-on-rails/01_ruby_on_rails_mvc_active_record.md) — Rails convention over configuration, Active Record, and migrations.
  * [`02_rails_api_and_sidekiq_jobs.md`](./05-backend-and-runtimes/ruby-on-rails/02_rails_api_and_sidekiq_jobs.md) — API mode (`--api`), ActiveJob, and Redis-backed Sidekiq workers.
  * [`01_mean_vs_mern_stack_architecture.md`](./05-backend-and-runtimes/mean-vs-mern/01_mean_vs_mern_stack_architecture.md) — Full comparative architecture of MEAN vs MERN.

### 6. 🗄️ Databases & Caching (PostgreSQL, Redis, MongoDB)
* [`01_postgresql_mvcc_indexing_query_tuning.md`](./06-databases-and-caching/sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md) — MVCC, dead tuples, Autovacuum, Partial Indexes, and `EXPLAIN (ANALYZE, BUFFERS)`.
* [`02_postgresql_partitioning_and_replication.md`](./06-databases-and-caching/sql-postgresql/02_postgresql_partitioning_and_replication.md) — Declarative range/list/hash table partitioning, partition pruning, and WAL streaming replication.
* [`01_redis_data_structures_and_eviction_policies.md`](./06-databases-and-caching/redis-caching/01_redis_data_structures_and_eviction_policies.md) — Hashes, Sorted Sets, `maxmemory-policy` (LRU vs LFU), and sliding window rate limiters.
* [`02_redis_distributed_locking_and_pubsub.md`](./06-databases-and-caching/redis-caching/02_redis_distributed_locking_and_pubsub.md) — Atomic Redlock (`SET NX PX`), Lua script releases, and distributed locks.
* [`01_mongodb_architecture_indexing_sharding.md`](./06-databases-and-caching/nosql-mongodb/01_mongodb_architecture_indexing_sharding.md) — WiredTiger storage engine, ESR compound indexing rule, and sharded cluster topologies.
* [`02_mongodb_aggregation_pipeline_mastery.md`](./06-databases-and-caching/nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md) — Multi-stage document aggregation (`$match`, `$unwind`, `$lookup`, `$group`).

### 7. 🤖 AI & GenAI Systems Engineering
* [`01_rag_architecture_and_vector_databases.md`](./06-ai-genai/01_rag_architecture_and_vector_databases.md) — Chunking strategies, dense embeddings, vector retrieval, and grounded prompting.
* [`02_vector_search_embeddings_and_hnsw.md`](./06-ai-genai/02_vector_search_embeddings_and_hnsw.md) — Cosine similarity vs dot product, curse of dimensionality, and HNSW multi-layer graphs.
* [`03_agentic_workflows_langgraph_and_tool_calling.md`](./06-ai-genai/03_agentic_workflows_langgraph_and_tool_calling.md) — ReAct loops, cyclic state machines, LangGraph StateGraph, and JSON tool calling.
* [`04_llm_fine_tuning_lora_and_quantization.md`](./06-ai-genai/04_llm_fine_tuning_lora_and_quantization.md) — LoRA rank decomposition, QLoRA, GGUF, AWQ, and 4-bit quantization.
* [`05_production_llm_serving_vllm_and_guardrails.md`](./06-ai-genai/05_production_llm_serving_vllm_and_guardrails.md) — KV Cache fragmentation, PagedAttention, continuous batching, and safety guardrails.
* **Code Implementation:** [`coding_simple_rag_pipeline_python.md`](./06-ai-genai/interview-questions/coding_simple_rag_pipeline_python.md) — Complete vector store & RAG pipeline built from scratch in pure Python.

### 8. 🏗️ System Design (HLD & LLD)
* **High-Level Design (HLD):**
  * [`01_hld_url_shortener_tinyurl.md`](./07-system-design/01_hld_url_shortener_tinyurl.md) — Base62 encoding, Key Generation Service (KGS), and Cache-Aside.
  * [`02_hld_whatsapp_realtime_chat.md`](./07-system-design/02_hld_whatsapp_realtime_chat.md) — WebSocket gateways, message queues, presence servers, and Cassandra.
  * [`03_hld_netflix_video_streaming.md`](./07-system-design/03_hld_netflix_video_streaming.md) — Transcoding pipelines, HLS/DASH chunking, Adaptive Bitrate Streaming, and Open Connect CDN.
  * [`04_hld_uber_ride_matching_spatial_indexing.md`](./07-system-design/04_hld_uber_ride_matching_spatial_indexing.md) — Uber H3 hexagonal spatial indexing, real-time location stream ingestion, and dispatch ring search.
* **Low-Level Design (LLD) & Frameworks:**
  * [`05_lld_parking_lot_system.md`](./07-system-design/05_lld_parking_lot_system.md) — OOP design, Factory pattern, Strategy fee calculation, and spot assignment.
  * [`06_lld_distributed_rate_limiter.md`](./07-system-design/06_lld_distributed_rate_limiter.md) — Token Bucket and Sliding Window algorithms implemented in Python.
  * [`system_design_interview_framework.md`](./07-system-design/interview-questions/system_design_interview_framework.md) — The 4-step structural framework to ace any system design interview.

### 9. 🧮 Complete Blind 75 LeetCode Problem Set
* **[`08-leetcode-dsa/README.md`](./08-leetcode-dsa/README.md)** — **All 75 curated Blind 75 problems** solved with data structure memory foundations from scratch, 3 evolution versions (Newbie $O(N^2)$ vs Intermediate vs Senior Optimal $O(N)$), step-by-step trace tables, line-by-line comments, interview pitches, and STAR war stories across all 18 patterns:
  1. Arrays & Hashing (Two Sum, Contains Duplicate, Anagrams, Group Anagrams, Top K, Product Except Self, Longest Consecutive)
  2. Two Pointers (Valid Palindrome, 3Sum, Container With Most Water)
  3. Sliding Window (Best Time to Buy/Sell Stock, Longest Substring Without Repeating Characters, Character Replacement, Min Window Substring)
  4. Stack (Valid Parentheses)
  5. Binary Search (Find Min in Rotated Array, Search in Rotated Sorted Array)
  6. Linked List (Reverse List, Merge Two Lists, Reorder List, Remove Nth Node, Cycle Detection, Merge K Sorted Lists)
  7. Trees (Invert Tree, Max Depth, Same Tree, Subtree, LCA, Level Order, Validate BST, Kth Smallest, Construct from Pre/Inorder, Max Path Sum, Serialize/Deserialize)
  8. Tries (Implement Prefix Tree, Add & Search Words, Word Search II)
  9. Heap / Priority Queue (Merge K Lists, Top K Frequent, Find Median from Data Stream)
  10. Backtracking (Combination Sum, Word Search)
  11. Graphs (Number of Islands, Clone Graph, Pacific Atlantic, Course Schedule, Graph Valid Tree, Connected Components)
  12. Advanced Graphs (Alien Dictionary)
  13. 1D Dynamic Programming (Climbing Stairs, Coin Change, LIS, Word Break, Combination Sum IV, House Robber I & II, Decode Ways)
  14. 2D Dynamic Programming (Unique Paths, Longest Common Subsequence)
  15. Greedy (Maximum Subarray, Jump Game)
  16. Intervals (Insert Interval, Merge Intervals, Non-overlapping, Meeting Rooms I & II)
  17. Math & Geometry (Rotate Image, Spiral Matrix)
  18. Bit Manipulation (Number of 1 Bits, Counting Bits, Reverse Bits, Missing Number, Sum of Two Integers, Reverse Integer)
  * [`dsa_patterns_cheat_sheet_and_meta_heuristics.md`](./08-leetcode-dsa/interview-questions/dsa_patterns_cheat_sheet_and_meta_heuristics.md) — Master pattern recognition matrix & templates.

### 10. 🧪 Testing & DevOps
* [`01_playwright_e2e_testing_guide.md`](./10-testing-and-devops/testing-playwright-jest/01_playwright_e2e_testing_guide.md) — Playwright E2E cross-browser automation, auto-waiting, and network interception.
* [`02_jest_unit_and_integration_testing.md`](./10-testing-and-devops/testing-playwright-jest/02_jest_unit_and_integration_testing.md) — Jest and React Testing Library integration and asynchronous API mocking.
* [`01_docker_kubernetes_production_setup.md`](./10-testing-and-devops/devops-docker-kubernetes-cicd/01_docker_kubernetes_production_setup.md) — Multi-stage Docker builds and Kubernetes pod/service configurations.
* [`02_github_actions_production_cicd_pipeline.md`](./10-testing-and-devops/devops-docker-kubernetes-cicd/02_github_actions_production_cicd_pipeline.md) — Production GitHub Actions pipeline with Docker Buildx and cache optimization.
* [`03_kubernetes_helm_and_ingress_setup.md`](./10-testing-and-devops/devops-docker-kubernetes-cicd/03_kubernetes_helm_and_ingress_setup.md) — Helm charts, NGINX Ingress Controller, and Horizontal Pod Autoscaler (HPA).

### 11. 🎯 Master Interview Cheatsheets & Company Guides
* **Quick Recall & Strategy:**
  * [`01_fullstack_quick_recall_cheatsheet.md`](./09-interview-cheatsheet/01_fullstack_quick_recall_cheatsheet.md) — 5-minute pre-interview review card covering JS, React, Angular 21, and Node.
  * [`02_system_design_cheat_sheet.md`](./09-interview-cheatsheet/02_system_design_cheat_sheet.md) — Math formulas, latency numbers, and trade-off theorems.
  * [`behavioral_star_method_master_guide.md`](./09-interview-cheatsheet/interview-questions/behavioral_star_method_master_guide.md) — Senior Lead behavioral STAR templates with metrics.
* **MNC Service Tier Guides:**
  * [`tcs_interview_guide.md`](./11-interview-master-cheatsheets/service-mnc-tier/tcs_interview_guide.md) — TCS Technical Round 1 & 2 preparation.
  * [`infosys_interview_guide.md`](./11-interview-master-cheatsheets/service-mnc-tier/infosys_interview_guide.md) — Infosys Specialist Programmer & Lead Developer guide.
  * [`wipro_interview_guide.md`](./11-interview-master-cheatsheets/service-mnc-tier/wipro_interview_guide.md) — Wipro L1/L2 technical rounds & microservices.
  * [`cognizant_interview_guide.md`](./11-interview-master-cheatsheets/service-mnc-tier/cognizant_interview_guide.md) — Cognizant CTS senior architect & distributed systems guide.
  * [`capgemini_interview_guide.md`](./11-interview-master-cheatsheets/service-mnc-tier/capgemini_interview_guide.md) — Capgemini enterprise Java, MERN & Cloud guide.
  * [`01_top_mnc_interview_questions_tcs_accenture.md`](./11-interview-master-cheatsheets/service-mnc-tier/01_top_mnc_interview_questions_tcs_accenture.md) — Cross-MNC high-frequency questions and straightforward answers.
* **Product Companies & Startups:**
  * [`jll_interview_guide.md`](./11-interview-master-cheatsheets/mid-tier-and-startups/jll_interview_guide.md) — JLL scenario-based problem solving and secure auth architectures.
  * [`nagarro_interview_guide.md`](./11-interview-master-cheatsheets/mid-tier-and-startups/nagarro_interview_guide.md) — Nagarro design patterns and algorithmic rigor.
  * [`startup_tech_lead_interview_guide.md`](./11-interview-master-cheatsheets/mid-tier-and-startups/startup_tech_lead_interview_guide.md) — Series A-C Startup Tech Lead architectural trade-offs, cloud cost reduction, and 0-to-1 delivery.

---

## 💻 Tech Stack & Standards

* **Frontend:** JavaScript (ES2024), TypeScript 5+, React 19, Next.js 15 (App Router), Angular 21 (Zoneless, Signals), HTML5/CSS3.
* **Backend:** Node.js 22 (Libuv, Streams), Python 3.12 (FastAPI, Pydantic V2), Java 21 (Spring Boot 3), Ruby 3.3 (Rails 7.1, Sidekiq).
* **Databases & Cache:** PostgreSQL 16 (MVCC, Partitioning), Redis 7 (Sorted Sets, Redlock), MongoDB 7 (Aggregation, Sharding).
* **AI / GenAI:** Vector Search (HNSW, FAISS), RAG Pipelines, LangGraph Multi-Agent Workflows, LoRA Fine-Tuning, vLLM Inference.
* **DevOps & Testing:** Docker Multi-Stage, Kubernetes (Helm, Ingress, HPA), GitHub Actions CI/CD, Playwright, Jest.
