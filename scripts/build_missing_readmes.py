# -*- coding: utf-8 -*-
"""
Generates clean, comprehensive README.md files for the remaining top-level directories:
1. 01-web-core-and-performance/README.md
2. 05-angular-21/README.md
3. 06-nextjs/README.md
4. 09-backend-java-springboot/README.md
5. 10-backend-ruby-and-stacks/README.md
6. 11-databases-and-caching/README.md
7. 15-testing-and-devops/README.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

READMES = {
    os.path.join(BASE_DIR, "01-web-core-and-performance", "README.md"): """# ⚡ 01 - Web Core & Performance Engineering

> Comprehensive engineering reference for modern browser performance, Core Web Vitals (CWV), Critical Rendering Path (CRP), and asset delivery optimization.

---

## 🗂️ Module Contents & Learning Path

### 1. Web Core Vitals Deep Dive
* [**`01_core_web_vitals_lcp_inp_cls.md`**](./web-core-vitals/01_core_web_vitals_lcp_inp_cls.md)
  - Overview of Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS).
* [**`02_inp_interaction_to_next_paint_deep_dive.md`**](./web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md)
  - Input delay, presentation delay, long tasks (>50ms), and yielding via `scheduler.yield()`.
* [**`03_cls_cumulative_layout_shift_debugging.md`**](./web-core-vitals/03_cls_cumulative_layout_shift_debugging.md)
  - Layout stability, `aspect-ratio` bounding boxes, ad slot placeholders, and font swap flicker.

### 2. Frontend Performance Optimization
* [**`01_critical_rendering_path_and_paint.md`**](./frontend-performance-optimization/01_critical_rendering_path_and_paint.md)
  - DOM, CSSOM, Render Tree, Layout Reflow, Repaint, Composite, and layout thrashing prevention.
* [**`02_bundle_splitting_and_lazy_loading.md`**](./frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md)
  - Route-based chunking, dynamic `import()`, tree shaking, and vendor splitting.
* [**`03_image_and_font_optimization.md`**](./frontend-performance-optimization/03_image_and_font_optimization.md)
  - Next-gen image formats (AVIF, WebP), `<picture>` progressive fallback, and variable fonts.
""",

    os.path.join(BASE_DIR, "05-angular-21", "README.md"): """# 🅰️ 05 - Modern Angular 21 Architecture

> Production-grade guide to modern Angular 21: Zoneless change detection, fine-grained Signals reactivity, `@defer` template chunking, Standalone components, and the `inject()` API.

---

## 🗂️ Module Contents & Learning Path

* [**`01_angular21_signals_and_reactivity.md`**](./01_angular21_signals_and_reactivity.md)
  - `signal()`, `computed()`, `effect()`, signal inputs (`input()`), and two-way `model()` binding.
* [**`02_angular21_zoneless_architecture.md`**](./02_angular21_zoneless_architecture.md)
  - Default zoneless change detection in Angular 21, removal of `zone.js`, and signal dirty marking.
* [**`03_angular21_defer_block_and_lazy_loading.md`**](./03_angular21_defer_block_and_lazy_loading.md)
  - Template-level lazy loading via `@defer`, `@placeholder`, `@loading`, and `@error` triggers (`on viewport`, `on interaction`, `when condition`).
* [**`04_angular21_standalone_components_and_inject.md`**](./04_angular21_standalone_components_and_inject.md)
  - Standalone component architecture, the functional `inject()` API, and functional router guards.
* [**`05_angular21_rxjs_interop_to_signal.md`**](./05_angular21_rxjs_interop_to_signal.md)
  - Bridging asynchronous RxJS streams with synchronous Signals via `toSignal()` and `toObservable()`.
* [**`interview-questions/angular21_top_interview_questions.md`**](./interview-questions/angular21_top_interview_questions.md)
  - High-frequency Angular 21 senior technical interview questions and architectural answers.
""",

    os.path.join(BASE_DIR, "06-nextjs", "README.md"): """# ▲ 06 - Next.js 15 Fullstack Engineering

> Production reference for Next.js 15 App Router: React Server Components (RSC), Server Actions, 4-tier caching, and Edge middleware.

---

## 🗂️ Module Contents & Learning Path

* [**`01_app_router_and_react_server_components.md`**](./01_app_router_and_react_server_components.md)
  - Server Components vs Client Components, zero-bundle cost, and streaming SSR.
* [**`02_server_actions_and_mutations.md`**](./02_server_actions_and_mutations.md)
  - Type-safe RPC mutations with `"use server"`, Zod schema validation, and `revalidatePath()`.
* [**`03_caching_and_revalidation_deep_dive.md`**](./03_caching_and_revalidation_deep_dive.md)
  - The 4 Next.js caching tiers: Request Memoization, Data Cache, Full Route Cache, and Router Cache.
* [**`04_middleware_and_authentication.md`**](./04_middleware_and_authentication.md)
  - Edge runtime routing, session JWT validation, rewrite headers, and path matching.
* [**`interview-questions/nextjs_top_interview_questions.md`**](./interview-questions/nextjs_top_interview_questions.md)
  - Senior Next.js interview questions, hydration mismatches, and parallel/intercepting routes.
""",

    os.path.join(BASE_DIR, "09-backend-java-springboot", "README.md"): """# ☕ 09 - Core Java 21 & Spring Boot 3 Architecture

> Deep-dive engineering reference for Java 21: Virtual Threads (Project Loom), JVM Generational ZGC, ConcurrentHashMap internals, and Spring Boot 3 enterprise microservices.

---

## 🗂️ Module Contents & Learning Path

### 1. Spring Boot 3 Framework
* [**`01_springboot_architecture_and_jvm.md`**](./01_springboot_architecture_and_jvm.md)
  - Spring Boot IoC Container, Bean lifecycle, auto-configuration, and JVM memory layout.
* [**`02_springboot_security_jwt_oauth2.md`**](./02_springboot_security_jwt_oauth2.md)
  - Spring Security 6 `SecurityFilterChain`, stateless sessions, JWT filter chain, and `@PreAuthorize`.
* [**`03_springboot_microservices_and_resilience4j.md`**](./03_springboot_microservices_and_resilience4j.md)
  - Resilience4j Circuit Breakers (Closed, Open, Half-Open), Retry policies, and OpenTelemetry tracing.

### 2. Core Java 21 Internals
* [**`04_java21_virtual_threads_and_structured_concurrency.md`**](./04_java21_virtual_threads_and_structured_concurrency.md)
  - Virtual Threads (Project Loom) vs Platform OS Threads, carrier threads, unmounting during blocking I/O, and `StructuredTaskScope`.
* [**`05_jvm_garbage_collectors_zgc_g1_tuning.md`**](./05_jvm_garbage_collectors_zgc_g1_tuning.md)
  - JVM Heap memory regions, G1 GC tuning, and Java 21 Generational ZGC with $< 1\text{ms}$ concurrent pauses.
* [**`06_concurrenthashmap_and_thread_safe_collections.md`**](./06_concurrenthashmap_and_thread_safe_collections.md)
  - `HashMap` bucket treeification (Red-Black Tree threshold 8), `ConcurrentHashMap` fine-grained CAS and bucket locking.

### 3. Senior Interview Suite
* [**`interview-questions/top_java_springboot_interview_questions.md`**](./interview-questions/top_java_springboot_interview_questions.md)
  - Top technical interview questions on Virtual Threads, Bean scopes, `@Transactional` proxy pitfalls, and Spring Boot 3 enhancements.
""",

    os.path.join(BASE_DIR, "10-backend-ruby-and-stacks", "README.md"): """# 💎 10 - Ruby on Rails & Full-Stack Architectures

> Architecture reference for Ruby on Rails 7+, Active Record ORM, Redis-backed Sidekiq background jobs, and a comprehensive comparative analysis of MEAN vs MERN stacks.

---

## 🗂️ Module Contents & Learning Path

* [**`ruby-on-rails/01_ruby_on_rails_mvc_active_record.md`**](./ruby-on-rails/01_ruby_on_rails_mvc_active_record.md)
  - Rails Convention over Configuration, MVC patterns, Active Record migrations, and association queries.
* [**`ruby-on-rails/02_rails_api_and_sidekiq_jobs.md`**](./ruby-on-rails/02_rails_api_and_sidekiq_jobs.md)
  - Rails API-only mode (`--api`), ActiveJob, and high-concurrency Redis-backed Sidekiq workers.
* [**`mean-vs-mern/01_mean_vs_mern_stack_architecture.md`**](./mean-vs-mern/01_mean_vs_mern_stack_architecture.md)
  - In-depth architectural, data-binding, and enterprise trade-off comparison between MEAN (Angular) and MERN (React) stacks.
""",

    os.path.join(BASE_DIR, "11-databases-and-caching", "README.md"): """# 🗄️ 11 - Databases, Relational Storage & Caching

> Enterprise reference for PostgreSQL (MVCC, Partitioning), Redis (Data Structures, Distributed Locks), and MongoDB (Indexing, Aggregation).

---

## 🗂️ Module Contents & Learning Path

### 1. PostgreSQL Relational Database
* [**`sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md`**](./sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md)
  - Multi-Version Concurrency Control (`xmin`/`xmax`), Autovacuum, Partial Indexes, and `EXPLAIN (ANALYZE, BUFFERS)`.
* [**`sql-postgresql/02_postgresql_partitioning_and_replication.md`**](./sql-postgresql/02_postgresql_partitioning_and_replication.md)
  - Declarative table partitioning (Range, List, Hash), partition pruning, and WAL physical streaming replication.

### 2. Redis High-Performance Cache & Distributed Locks
* [**`redis-caching/01_redis_data_structures_and_eviction_policies.md`**](./redis-caching/01_redis_data_structures_and_eviction_policies.md)
  - Strings, Hashes, Sorted Sets, `maxmemory-policy` (LRU vs LFU), and sliding window rate limiting.
* [**`redis-caching/02_redis_distributed_locking_and_pubsub.md`**](./redis-caching/02_redis_distributed_locking_and_pubsub.md)
  - Atomic distributed locking (Redlock, `SET NX PX`), Lua script verification, and Pub/Sub.

### 3. MongoDB NoSQL Document Store
* [**`nosql-mongodb/01_mongodb_architecture_indexing_sharding.md`**](./nosql-mongodb/01_mongodb_architecture_indexing_sharding.md)
  - WiredTiger storage engine, ESR compound indexing rule, and sharded cluster architectures.
* [**`nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md`**](./nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md)
  - Multi-stage Aggregation pipelines (`$match`, `$unwind`, `$lookup`, `$group`).

### 4. Database Interview Questions
* [**`interview-questions/database_indexing_and_caching_questions.md`**](./interview-questions/database_indexing_and_caching_questions.md)
  - Clustered vs Non-Clustered indexes, Cache Breakdown / Penetration / Avalanche, and Connection Pooling.
""",

    os.path.join(BASE_DIR, "15-testing-and-devops", "README.md"): """# 🧪 15 - Testing, Containerization & Production DevOps

> Production guide for automated testing with Playwright and Jest, multi-stage Docker builds, GitHub Actions CI/CD pipelines, and Kubernetes Helm & HPA deployments.

---

## 🗂️ Module Contents & Learning Path

### 1. Automated Testing Suite
* [**`testing-playwright-jest/01_playwright_e2e_testing_guide.md`**](./testing-playwright-jest/01_playwright_e2e_testing_guide.md)
  - Playwright E2E cross-browser automation, auto-waiting, network interception, and trace viewers.
* [**`testing-playwright-jest/02_jest_unit_and_integration_testing.md`**](./testing-playwright-jest/02_jest_unit_and_integration_testing.md)
  - Jest & React Testing Library integration tests, asynchronous API mocking, and snapshot assertions.

### 2. DevOps, Containers & CI/CD
* [**`devops-docker-kubernetes-cicd/01_docker_kubernetes_production_setup.md`**](./devops-docker-kubernetes-cicd/01_docker_kubernetes_production_setup.md)
  - Production multi-stage Dockerfiles, image size reduction, Kubernetes Pods, Services, and Deployments.
* [**`devops-docker-kubernetes-cicd/02_github_actions_production_cicd_pipeline.md`**](./devops-docker-kubernetes-cicd/02_github_actions_production_cicd_pipeline.md)
  - Automated GitHub Actions workflow with caching, linting, testing, Docker Buildx, and container registry publishing.
* [**`devops-docker-kubernetes-cicd/03_kubernetes_helm_and_ingress_setup.md`**](./devops-docker-kubernetes-cicd/03_kubernetes_helm_and_ingress_setup.md)
  - Production Helm charts, NGINX Ingress Controller routing, and Horizontal Pod Autoscaler (HPA).
"""
}

def main():
    print(f"Generating {len(READMES)} directory README files...")
    for path, content in READMES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Directory README generation complete!")

if __name__ == "__main__":
    main()
