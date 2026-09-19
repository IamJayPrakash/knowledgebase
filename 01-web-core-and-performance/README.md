# ⚡ 01 - Web Core & Performance Engineering

> Comprehensive engineering reference for modern browser performance, Core Web Vitals (CWV), Critical Rendering Path (CRP), memory profiling, and asset delivery optimization.

---

## 🗂️ Module Contents & Learning Path

### 1. Web Core Vitals Deep Dive (Diagnosis & Codebase Solutions)

* [**`01_core_web_vitals_lcp_inp_cls.md`**](./web-core-vitals/01_core_web_vitals_lcp_inp_cls.md)
  * Overview of Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS).
* [**`02_inp_interaction_to_next_paint_deep_dive.md`**](./web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md)
  * Input delay, presentation delay, long tasks (>50ms), and yielding via `scheduler.yield()`.
* [**`03_cls_cumulative_layout_shift_debugging.md`**](./web-core-vitals/03_cls_cumulative_layout_shift_debugging.md)
  * Layout stability, `aspect-ratio` bounding boxes, ad slot placeholders, and font swap flicker.
* [**`04_lcp_deep_dive_and_codebase_optimization.md`**](./web-core-vitals/04_lcp_deep_dive_and_codebase_optimization.md)
  * The 4 LCP sub-parts (TTFB, Load Delay, Load Duration, Render Delay), `<link rel="preload" fetchpriority="high">`, removing `loading="lazy"` anti-patterns, and inlining critical CSS.
* [**`05_inp_long_tasks_and_main_thread_yielding.md`**](./web-core-vitals/05_inp_long_tasks_and_main_thread_yielding.md)
  * Long tasks ($> 50\text{ms}$) chunking, `scheduler.yield()` vs `MessageChannel`, eliminating layout thrashing by batching DOM reads and writes, and `useTransition`.
* [**`06_cls_font_metrics_and_aspect_ratio_prevention.md`**](./web-core-vitals/06_cls_font_metrics_and_aspect_ratio_prevention.md)
  * CSS Font Metric Overrides (`size-adjust`, `ascent-override`, `descent-override`), `content-visibility: auto` with `contain-intrinsic-size`, and GPU compositor animations.

### 2. Frontend Performance & Codebase Architecture Optimization

* [**`01_critical_rendering_path_and_paint.md`**](./frontend-performance-optimization/01_critical_rendering_path_and_paint.md)
  * DOM, CSSOM, Render Tree, Layout Reflow, Repaint, Composite, and layout thrashing prevention.
* [**`02_bundle_splitting_and_lazy_loading.md`**](./frontend-performance-optimization/02_bundle_splitting_and_lazy_loading.md)
  * Route-based chunking, dynamic `import()`, tree shaking, and vendor splitting.
* [**`03_image_and_font_optimization.md`**](./frontend-performance-optimization/03_image_and_font_optimization.md)
  * Next-gen image formats (AVIF, WebP), `<picture>` progressive fallback, and variable fonts.
* [**`04_resource_hints_speculation_rules_and_caching.md`**](./frontend-performance-optimization/04_resource_hints_speculation_rules_and_caching.md)
  * `dns-prefetch`, `preconnect`, modern Speculation Rules API for instant 0ms prerendering, Brotli compression, and `Cache-Control: immutable`.
* [**`05_dom_virtualization_and_memory_leak_profiling.md`**](./frontend-performance-optimization/05_dom_virtualization_and_memory_leak_profiling.md)
  * Virtual list windowing engine from scratch, Chrome DevTools Heap Snapshots, detached DOM nodes, and `WeakMap` leak prevention.
* [**`06_tree_shaking_side_effects_and_barrel_files.md`**](./frontend-performance-optimization/06_tree_shaking_side_effects_and_barrel_files.md)
  * ESM static analysis, `"sideEffects": false` in `package.json`, `/*#__PURE__*/` annotations, barrel file re-export bottlenecks, and bundle analyzers.
* [**`07_third_party_scripts_and_web_workers.md`**](./frontend-performance-optimization/07_third_party_scripts_and_web_workers.md)
  * Offloading third-party marketing tags (GTM, Meta Pixel) to background Web Workers via Partytown, chat widget Facade pattern, and `requestIdleCallback`.

---

## 📂 Master 60 Interview Question Bank

* [**`interview-questions/README.md`**](./interview-questions/README.md) — ⚡ **Complete 60-Question Master Curriculum Index & Topic Guide**.
* [**`interview-questions/01_core_web_vitals_lcp_inp_cls_qna.md`**](./interview-questions/01_core_web_vitals_lcp_inp_cls_qna.md) — Questions 1 to 20: Core Web Vitals (LCP, INP, CLS) & Field vs Lab Metrics.
* [**`interview-questions/02_rendering_pipeline_and_browser_internals_qna.md`**](./interview-questions/02_rendering_pipeline_and_browser_internals_qna.md) — Questions 21 to 40: Critical Rendering Path, Browser Engine & Layout Optimization.
* [**`interview-questions/03_network_bundling_and_caching_optimization_qna.md`**](./interview-questions/03_network_bundling_and_caching_optimization_qna.md) — Questions 41 to 60: Network Protocols, Bundling, Tree-Shaking & Caching.
