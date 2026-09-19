# Web Performance Master Interview Bank: Part 3 (Q41 - Q60)

## Network Protocols, Bundling, Tree-Shaking & Caching

---

### Q41: How does HTTP/3 (QUIC) improve upon HTTP/2?

**Answer:**

- **The TCP Head-of-Line Blocking Problem in HTTP/2:**
  Although HTTP/2 multiplexes streams over a single TCP connection, TCP is a sequential byte stream. If a single packet is lost on a poor cellular network, the **entire TCP connection stalls** while waiting for packet retransmission, freezing all multiplexed streams!
- **HTTP/3 (Built on UDP + QUIC):**
  1. Each stream is an independent flow over UDP: loss of a packet in Stream 1 has **zero impact on Stream 2**.
  2. **0-RTT Connection Establishment:** Combines cryptographic TLS 1.3 handshake with transport handshake in a single round-trip.
  3. **Connection Migration:** If a user walks out of their house and their phone switches from Wi-Fi to 5G cellular, the connection does not drop; QUIC uses a unique Connection ID rather than IP addresses.

---

### Q42: What is the "Barrel File" import problem in modern JavaScript bundlers?

**Answer:**

- **Barrel File:** An `index.ts` file that re-exports dozens or hundreds of modules:
  `export * from './Button'; export * from './Table'; export * from './Chart';`
- **The Performance Problem:**
  When a developer imports a single button: `import { Button } from '@/components'`, bundlers must parse, compile, and evaluate **every single re-exported module** inside `index.ts`.
  - Dramatically inflates build times (can increase cold start times from 2s to 45s in dev).
  - Can defeat tree-shaking if any re-exported file has side effects, bloating client production bundle size with megabytes of dead code.
- **Solution:** Direct path imports: `import { Button } from '@/components/Button'` or using compiler transforms like `modularize-imports`.

---

### Q43: How does Tree-Shaking work and what does `"sideEffects": false` do?

**Answer:**

- **Tree-Shaking:** Dead code elimination based on static analysis of ES Modules (`import`/`export`).
- **Why Bundlers Hesitate:**
  If a file contains top-level expressions: `window.hasInit = true;` or modifies prototypes, removing an unused export would break runtime behavior (it has a **side effect**).
- **`"sideEffects": false` in `package.json`:**
  Explicit contract guaranteeing to Webpack/Rollup that none of the files in this package contain top-level side effects.
  - Allows bundlers to aggressively prune unused exports completely from final client bundles.
  - If only CSS files have side effects, declare: `"sideEffects": ["*.css"]`.

---

### Q44: What does the `/*#__PURE__*/` annotation mean?

**Answer:**

- A hint to minifiers (Terser, esbuild) that a specific function call is **pure and has zero side effects**.
- If the variable receiving the return value is unused, the minifier can safely drop the entire function call:

  ```javascript
  // Minifier knows this can be deleted if 'Component' is unused:
  const Component = /*#__PURE__*/ React.memo(MyBaseComponent);
  ```

---

### Q45: How do you configure optimal Code Splitting in Webpack / Vite?

**Answer:**

1. **Route-Based Splitting:** Dynamically import page routes using `React.lazy()` or Next.js App Router subdirectories.
2. **Vendor Chunk Splitting:** Split stable third-party dependencies (`node_modules`) into a separate vendor chunk:

   ```javascript
   // vite.config.js
   build: {
     rollupOptions: {
       output: {
         manualChunks: {
           vendor: ['react', 'react-dom'],
           charting: ['chart.js'],
         }
       }
     }
   }
   ```

   Ensures that updating application code does not invalidate the cached vendor bundle in user browsers!

---

### Q46: Why must preloaded web fonts include the `crossorigin` attribute?

**Answer:**

```html
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin />
```

- According to W3C specification, web font requests are **always fetched using anonymous CORS mode**, even if loaded from the same origin.
- If you omit `crossorigin` on the `<link rel="preload">`, the browser downloads the font once without CORS, rejects it when CSS requests it with CORS, and **downloads the font a second time**, wasting double bandwidth!

---

### Q47: What is the Facade Pattern for third-party embeds (YouTube / Chat Widgets)?

**Answer:**

- An embedded YouTube iframe or Intercom chat widget downloads ~1.5 MB of JavaScript before the user even clicks play.
- **The Facade Pattern:**
  Render a lightweight static image mock / button that looks identical to the real player (`<div class="youtube-facade">...</div>` - ~10KB).
- Only when the user explicitly hovers or clicks the placeholder do you dynamically load the real iframe/widget.
  - Saves 99% of bandwidth for non-interacting visitors.

---

### Q48: How do Service Workers enable offline-first web applications?

**Answer:**

- A **Service Worker** is an event-driven programmable network proxy running in a background browser thread between the web page and the network.
- Intercepts all outgoing HTTP `fetch` requests (`self.addEventListener('fetch', ...)`).
- Can return responses directly from the **Cache Storage API** instantly, enabling offline operation.

---

### Q49: Compare Service Worker Caching Strategies

**Answer:**

1. **Cache-First (Falling back to Network):**
   Checks cache first. If found, returns immediately. If missing, queries network.
   - *Best for:* Static immutable versioned assets (images, hashed JS/CSS, fonts).
2. **Network-First (Falling back to Cache):**
   Tries fetching from network. If offline or network fails, returns cached copy.
   - *Best for:* Real-time data feeds, user account balance.
3. **Stale-While-Revalidate:**
   Returns cached response immediately; fires background network fetch to update cache for next time.
   - *Best for:* News articles, avatars, social media posts.

---

### Q50: Compare Modern JavaScript Bundlers: Vite vs Webpack vs Turbopack

**Answer:**

| Feature | Webpack | Vite | Turbopack |
| :--- | :--- | :--- | :--- |
| **Dev Server Architecture** | Bundles entire codebase into memory before startup. | Uses **native browser ES Modules (ESM)**; compiles on-demand. | Rust-based incremental computation engine. |
| **Language** | JavaScript (Node.js) | esbuild (Go) for dev + Rollup for prod | **Rust** |
| **HMR Speed** | Degrades as app scales ($> 5\text{s}$). | **Instant (< 50ms)** regardless of app size. | **Ultra-fast (< 10ms)**. |
| **Production Bundler** | Webpack | Rollup | Turbopack (Next.js 15) |

---

### Q51: What is Early Hints (HTTP Status Code 103)?

**Answer:**

- Standardized HTTP status code allowing servers to send preliminary response headers **before the main HTML page has finished server-side rendering**:

  ```http
  HTTP/1.1 103 Early Hints
  Link: </app.css>; rel=preload; as=style
  Link: </hero.webp>; rel=preload; as=image
  ```

- The browser starts downloading critical CSS and hero images while the server is still running slow database queries to render the HTML, cutting hundreds of milliseconds off LCP!

---

### Q52: What is the difference between `localStorage`, `sessionStorage`, and `IndexedDB`?

**Answer:**

- **`localStorage` / `sessionStorage`:**
  - Synchronous storage; limited to ~5MB.
  - **Blocks the main thread** on reads and writes; stores strings only.
- **`IndexedDB`:**
  - **Asynchronous, non-blocking** transactional object-oriented database.
  - Can store gigabytes of structured data, Blobs, ArrayBuffers, and typed objects.
  - Ideal for offline PWA storage and caching massive datasets.

---

### Q53: How do you prevent FOUC (Flash of Unstyled Content) in SSR applications?

**Answer:**

- Extract critical CSS styles during server-side rendering and inline them directly into a `<style>` tag inside the server-rendered `<head>`.
- Defer non-critical stylesheets using `<link rel="preload" as="style" onload="this.rel='stylesheet'">`.

---

### Q54: What is the `NetworkInformation` API and how can it adapt asset quality?

**Answer:**

- `navigator.connection` exposes network metrics: `effectiveType` (`'4g'`, `'3g'`, `'2g'`) and `saveData` boolean.
- Allows applications to adaptively serve low-resolution images or disable autoplay video loops on slow cellular connections.

---

### Q55: What is Content Security Policy (CSP) and how does it impact performance?

**Answer:**

- An HTTP response header that restricts what domains can execute scripts, styles, and iframes on a page.
- **Performance Benefit:** Prevents rogue third-party extensions and cross-site scripting (XSS) injectors from injecting heavy unoptimized scripts onto the main thread.

---

### Q56: What is a Source Map and should you enable Source Maps in production?

**Answer:**

- Maps minified, bundled production code back to original uncompiled TypeScript/React source files.
- **Best Practice:** Generate hidden source maps (`hidden-source-map`), upload them securely to error tracking services (Sentry/Datadog), and **do NOT serve them publicly** on your web server to prevent exposing proprietary source code.

---

### Q57: How does `font-subsetting` reduce font file sizes from 2MB to 30KB?

**Answer:**

- Full font files contain thousands of glyphs for Cyrillic, Greek, Hebrew, and Chinese characters.
- **Subsetting:** Strips out all unused unicode glyphs, retaining only the ASCII Latin character set (e.g. `U+0000-00FF`), shrinking font files by up to 90%!

---

### Q58: What is the difference between `defer` and dynamic `import()`?

**Answer:**

- `<script defer>` downloads during initial page load and executes before `DOMContentLoaded`.
- **Dynamic `import()`:** Downloads and executes on-demand at runtime triggered by user interaction (e.g. clicking "Open Modal" or navigating to a route).

---

### Q59: How does Gzip / Brotli compression interact with TLS (BREACH attack)?

**Answer:**

- Compressing HTTP responses containing both secrets (CSRF tokens) and user-supplied reflection allows attackers to guess secrets by observing ciphertext size variations (BREACH attack).
- **Defense:** Disable HTTP compression on endpoints reflecting user input with secret tokens or use masked/randomized CSRF tokens.

---

### Q60: What is the Google Chrome "Performance Insights" panel?

**Answer:**

- A curated DevTools diagnostic panel designed specifically for Core Web Vitals remediation.
- Automatically identifies layout shifts, long tasks, and LCP candidates, providing actionable insights with direct links to corresponding source code lines.
