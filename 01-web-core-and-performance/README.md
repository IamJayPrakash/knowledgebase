# ⚡ 01 - Web Core & Performance Engineering

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
