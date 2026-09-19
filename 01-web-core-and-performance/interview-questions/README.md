# ⚡ Web Performance & Core Web Vitals Senior & Lead Master Interview Question Bank (60 Questions)

> Comprehensive, production-grade 60-question interview bank covering Google Core Web Vitals (LCP, INP, CLS), Critical Rendering Path, layout thrashing, modern image/font engineering, and high-performance network bundling.

---

## 📑 Curriculum & Question Bank Structure

```
01-web-core-and-performance/interview-questions/
├── 01_core_web_vitals_lcp_inp_cls_qna.md            ──► Questions 1 to 20
├── 02_rendering_pipeline_and_browser_internals_qna.md ──► Questions 21 to 40
└── 03_network_bundling_and_caching_optimization_qna.md ──► Questions 41 to 60
```

---

## 🎯 Master Question Index (1 - 60)

### Part 1: Core Web Vitals (LCP, INP, CLS) & Field vs Lab Metrics (Q1 - Q20)

* [`01_core_web_vitals_lcp_inp_cls_qna.md`](./01_core_web_vitals_lcp_inp_cls_qna.md)
  1. Google's 3 Core Web Vitals in 2024-2026 and 75th percentile thresholds.
  2. Why Google replaced FID (First Input Delay) with INP (Interaction to Next Paint).
  3. The 4 sub-parts of Largest Contentful Paint (LCP: TTFB, Load Delay, Load Duration, Render Delay).
  4. Why adding `loading="lazy"` to a hero image is an LCP disaster.
  5. The 3 phases of an INP interaction (Input Delay, Processing, Presentation Delay).
  6. Long Tasks (>50ms) on the main thread and yielding via `scheduler.yield()`.
  7. Mathematical calculation of Cumulative Layout Shift (Impact Fraction $\times$ Distance Fraction).
  8. Three primary causes of CLS and their technical remedies.
  9. Field Data (CrUX / RUM) vs Lab Data (Lighthouse) and Google SEO implications.
  10. Measuring Core Web Vitals programmatically via `web-vitals` library.
  11. Flash of Unstyled Text (FOUT) vs Flash of Invisible Text (FOIT).
  12. Time to First Byte (TTFB) and server/CDN edge caching optimizations.
  13. Layout Thrashing (Forced Synchronous Layout) profiling in Chrome DevTools.
  14. CSS `content-visibility: auto` and `contain-intrinsic-size` placeholder pairing.
  15. Why CSS `@import` creates sequential network waterfalls.
  16. Speculation Rules API for instant 0ms pre-rendering.
  17. Resource hints: `dns-prefetch`, `preconnect`, `preload`, and `prefetch`.
  18. Brotli (`br`) vs Gzip (`gzip`) compression algorithms.
  19. `Cache-Control: public, max-age=31536000, immutable` and content hashing.
  20. The `stale-while-revalidate` caching header.

### Part 2: Critical Rendering Path, Browser Engine & Layout Optimization (Q21 - Q40)

* [`02_rendering_pipeline_and_browser_internals_qna.md`](./02_rendering_pipeline_and_browser_internals_qna.md)
  21. The 6 stages of the Critical Rendering Path (DOM, CSSOM, Render Tree, Layout, Paint, Composite).
  22. Why CSS is Render-Blocking while JavaScript is Parser-Blocking.
  23. `<script async>` vs `<script defer>` download and execution differences.
  24. Composite-Only CSS properties (GPU hardware acceleration).
  25. `will-change: transform` and GPU layer VRAM memory exhaustion.
  26. Eliminating layout thrashing using FastDOM batching.
  27. Next-gen image format comparison: AVIF vs WebP vs MozJPEG.
  28. Progressive image fallback using the `<picture>` tag.
  29. `decoding="async"` on `<img>` tags offloading raster decoding.
  30. Variable Fonts reducing multiple weight requests into one file.
  31. `font-display: optional` as Google's recommended CWV font strategy.
  32. CSS `size-adjust` eliminating layout shifts caused by fallback fonts.
  33. DOM Virtual Windowing engine mathematical index calculations.
  34. CSS Containment (`contain: strict / content`) scoping layout calculations.
  35. Client-Side Rendering (CSR) vs Server-Side Rendering (SSR) vs Static Site Generation (SSG).
  36. Cumulative Layout Shift caused by asynchronous CSS injection.
  37. Detecting and fixing memory leaks in Single Page Applications with DevTools.
  38. `requestIdleCallback` vs `setTimeout(fn, 0)`.
  39. DOM tree depth limits (<1,500 nodes) and reflow performance.
  40. Partytown offloading third-party marketing tags to Web Workers.

### Part 3: Network Protocols, Bundling, Tree-Shaking & Caching (Q41 - Q60)

* [`03_network_bundling_and_caching_optimization_qna.md`](./03_network_bundling_and_caching_optimization_qna.md)
  41. HTTP/3 (QUIC / UDP) eliminating transport-level Head-of-Line blocking.
  42. The "Barrel File" (`index.ts`) re-export performance trap.
  43. Tree-shaking static analysis and `"sideEffects": false` in `package.json`.
  44. The `/*#__PURE__*/` minification comment annotation.
  45. Code splitting strategies: Route-based vs Vendor chunking in Vite/Webpack.
  46. Why preloaded web fonts strictly require the `crossorigin` attribute.
  47. The Facade Pattern for third-party embeds (YouTube / Chat widgets).
  48. Service Workers enabling offline-first caching via Cache Storage API.
  49. Service Worker caching strategies: Cache-First vs Network-First vs Stale-While-Revalidate.
  50. Modern JavaScript bundlers comparison: Vite vs Webpack vs Turbopack.
  51. HTTP 103 Early Hints accelerating LCP.
  52. `localStorage` (blocking) vs `IndexedDB` (async transactional).
  53. Preventing Flash of Unstyled Content (FOUC) in SSR apps.
  54. `NetworkInformation` API adapting quality to cellular networks.
  55. Content Security Policy (CSP) blocking rogue unoptimized scripts.
  56. Production Source Map best practices (`hidden-source-map`).
  57. Font Subsetting stripping unused unicode glyphs.
  58. `<script defer>` vs dynamic `import()`.
  59. HTTP compression and TLS BREACH attack mitigations.
  60. Chrome DevTools Performance Insights panel for CWV remediation.
