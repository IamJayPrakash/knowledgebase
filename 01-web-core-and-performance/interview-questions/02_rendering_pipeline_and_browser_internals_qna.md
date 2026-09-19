# Web Performance Master Interview Bank: Part 2 (Q21 - Q40)

## Critical Rendering Path, Browser Engine & Layout Optimization

---

### Q21: Diagram and explain the 6 stages of the Critical Rendering Path (CRP)

**Answer:**

```
HTML Bytes ──► Tokenizer ──► [ DOM Tree ]
                                  │
                                  ├─► [ Render Tree ] ──► [ Layout (Reflow) ] ──► [ Paint ] ──► [ Composite ]
                                  │   (Visible nodes)     (Geometry: x, y, w, h)   (Pixels)       (GPU Layers)
CSS Bytes  ──► Tokenizer ──► [ CSSOM Tree ]
```

1. **DOM Construction:** Parses HTML bytes into tokens, nodes, and constructs the Document Object Model tree.
2. **CSSOM Construction:** Parses CSS stylesheets into the CSS Object Model tree. (CSS is render-blocking!).
3. **Render Tree:** Combines DOM and CSSOM, ignoring non-visible elements (`display: none`, `<head>`).
4. **Layout (Reflow):** Computes exact geometry (positions `x, y` and dimensions `width, height`) for each visible box on the viewport screen.
5. **Paint:** Converts vector box representations into actual RGB pixels across multiple layers (Rasterization).
6. **Composite:** GPU combines layers in correct stacking order (`z-index`, 3D transforms) and outputs frames to the physical display monitor.

---

### Q22: Why is CSS considered "Render-Blocking" while `<script>` is "Parser-Blocking"?

**Answer:**

- **CSS is Render-Blocking:** The browser will not render any pixel on the screen until it has fully downloaded and constructed the **CSSOM Tree**. If it rendered HTML before CSS arrived, the user would see a horrific unstyled flash (FOUC).
- **JavaScript is Parser-Blocking:** When the HTML parser encounters a synchronous `<script src="...">`:
  1. It **halts HTML parsing immediately**.
  2. Waits for the JavaScript file to download over the network.
  3. Executes the script immediately (because the script might call `document.write()` or modify the DOM).
  4. Resumes HTML parsing only after script execution finishes.

---

### Q23: What is the difference between `<script async>` and `<script defer>`?

**Answer:**

| Attribute | Download Behavior | Execution Timing | Preserves Order? | Blocks HTML Parser? |
| :--- | :--- | :--- | :--- | :--- |
| **Regular `<script>`** | Blocks parser while downloading. | Executes **immediately** when downloaded. | ✅ Yes | **Blocks completely**. |
| **`<script async>`** | Downloads **in parallel** in background. | Executes **immediately when download completes**, pausing HTML parser if running. | ❌ No (executes whichever finishes first). | Pauses parser during execution only. |
| **`<script defer>`** | Downloads **in parallel** in background. | Executes **ONLY after HTML parsing completes**, right before `DOMContentLoaded`. | ✅ Yes (guarantees execution order). | **Zero blocking**. |

- **Best Practice:** Use `defer` for your core application bundles; use `async` only for independent, standalone third-party analytics trackers.

---

### Q24: Which CSS properties trigger Composite-Only (GPU accelerated)?

**Answer:**
To achieve locked **60 FPS / 120 FPS animations**, you must animate properties that skip both Layout and Paint:

- **Composite-Only Properties (GPU):**
  1. **`transform`** (`translate3d`, `scale`, `rotate`)
  2. **`opacity`**
  3. **`filter`** (in modern GPU engines)
- **Properties that trigger Layout (Slowest):** `width`, `height`, `margin`, `padding`, `top`, `left`, `border`, `font-size`.
- **Properties that trigger Paint (Moderate):** `color`, `background-color`, `box-shadow`, `border-radius`.

---

### Q25: How does `will-change: transform` work and why can overusing it degrade performance?

**Answer:**

- `will-change: transform` gives a hint to the browser compositor to **promote the element to its own independent GPU graphics layer** ahead of time.
- **Benefit:** When animated, only that layer's texture matrix is updated on the GPU without repainting the rest of the page.
- **Danger of Overuse:** Every GPU layer consumes substantial VRAM memory and introduces compositing overhead. Promoting hundreds of elements crashes mobile browser tabs due to GPU memory exhaustion!

---

### Q26: How do you eliminate Layout Thrashing using Batching?

**Answer:**
Separate all DOM reads from all DOM writes:

```javascript
// ❌ BAD: Layout thrashing (forces 3 synchronous layout reflows!)
const box1Width = box1.offsetWidth; // Read
box1.style.width = box1Width + 10 + 'px'; // Write -> Invalidates layout!
const box2Width = box2.offsetWidth; // Read -> Forces layout reflow!
box2.style.width = box2Width + 10 + 'px'; // Write

// ✅ GOOD: Batched Reads and Writes
const w1 = box1.offsetWidth; // Read 1
const w2 = box2.offsetWidth; // Read 2
// Layout remains valid; now batch writes together:
box1.style.width = w1 + 10 + 'px'; // Write 1
box2.style.width = w2 + 10 + 'px'; // Write 2
```

---

### Q27: Compare Next-Gen Image Formats: AVIF vs WebP vs JPEG

**Answer:**

| Format | Compression Tech | File Size vs JPEG | Browser Support | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **JPEG** | Discrete Cosine Transform (1992) | Baseline (100%) | 100% | Legacy fallback |
| **WebP** | VP8 video intra-frame (Google 2010) | **25% - 35% smaller** | >97% | Universal modern standard |
| **AVIF** | AV1 video keyframe (AOMedia 2019) | **50% - 60% smaller** | >93% (Chrome, Safari, Firefox) | Peak compression quality & HDR |

---

### Q28: How do you configure progressive image fallback using the `<picture>` tag?

**Answer:**
Serve cutting-edge AVIF first, falling back to WebP, and finally standard JPEG:

```html
<picture>
  <source srcset="/images/hero.avif" type="image/avif" />
  <source srcset="/images/hero.webp" type="image/webp" />
  <img 
    src="/images/hero.jpg" 
    alt="Hero Banner" 
    width="1200" 
    height="600" 
    loading="eager" 
    fetchpriority="high" 
    decoding="async"
  />
</picture>
```

---

### Q29: What is `decoding="async"` on `<img>` tags?

**Answer:**

- By default, decoding compressed image data (JPEG/WebP to raw bitmap pixels) can occur synchronously on the main thread, causing minor frame drops during scrolling.
- **`decoding="async"`** tells the browser to decode the image raster off the main thread in a background worker thread, keeping main-thread scrolling buttery smooth.

---

### Q30: What are Variable Fonts and how do they save bandwidth?

**Answer:**

- **Traditional Fonts:** Each weight and style requires a separate file:
  `Roboto-Regular.woff2` (25KB), `Roboto-Bold.woff2` (25KB), `Roboto-Italic.woff2` (25KB) = 75KB across 3 HTTP requests.
- **Variable Font (`Roboto-Variable.woff2`):**
  A single file (~35KB) containing an infinite continuum of weights (`font-weight: 100` to `900`), slant angles, and optical sizes along design axes.
  - Reduces total network payloads by 50% and eliminates multiple connection requests.

---

### Q31: What is `font-display: optional` and why is it Google's recommended CWV font strategy?

**Answer:**

- Gives the font a tiny **100ms block period** and **0ms swap period**:
  1. If the font is already cached in memory, it renders instantly with the custom font.
  2. If the font must be downloaded over a slow network and takes $> 100\text{ms}$, the browser renders the system font and **NEVER swaps the font during this session**, completely eliminating FOIT and CLS!
  3. The font is saved into browser cache in the background so it is available instantly on the user's second pageview.

---

### Q32: How does `size-adjust` eliminate Cumulative Layout Shift caused by fallback fonts?

**Answer:**
`@font-face` CSS descriptors allow overriding system fallback font metrics to match the exact bounding box of the web font:

```css
@font-face {
  font-family: 'FallbackArial';
  src: local('Arial');
  ascent-override: 95%;
  descent-override: 25%;
  line-gap-override: 0%;
  size-adjust: 102%; /* Stretches Arial characters to match custom font width! */
}

body {
  font-family: 'CustomFont', 'FallbackArial', sans-serif;
}
```

When `CustomFont` downloads and swaps with `FallbackArial`, text occupies the **exact same vertical and horizontal space**, achieving **0.000 CLS**!

---

### Q33: How does a DOM Virtual Windowing engine work mathematically?

**Answer:**
Given a list of 100,000 items with item height $H = 50\text{px}$ and viewport height $V = 600\text{px}$:

1. **Total Virtual Height:** $\text{TotalHeight} = 100,000 \times 50 = 5,000,000\text{px}$. Render an outer container with this CSS height so the browser scrollbar is authentic.
2. **Calculate Visible Range on Scroll (`scrollTop`):**
   $$\text{startIndex} = \max\left(0, \left\lfloor \frac{\text{scrollTop}}{H} \right\rfloor - \text{overscan}\right)$$
   $$\text{endIndex} = \min\left(N - 1, \left\lceil \frac{\text{scrollTop} + V}{H} \right\rceil + \text{overscan}\right)$$
3. Only render items between `startIndex` and `endIndex` (typically ~15-20 DOM nodes), positioning each with `transform: translateY(index * H)`.

---

### Q34: What is CSS Containment (`contain: strict / content`)?

**Answer:**

- Tells the browser engine that an element's subtree is **independent of the rest of the document tree**:
  - `contain: layout`: Changes inside this element never affect the layout of outside elements.
  - `contain: paint`: Descendants cannot paint outside the element's bounding box.
  - `contain: size`: The size of the element can be calculated without examining its children.
- Allows the browser to scope style and layout recalculations strictly to that isolated container, speeding up complex app re-renders.

---

### Q35: What is the difference between Client-Side Rendering (CSR), Server-Side Rendering (SSR), and Static Site Generation (SSG)?

**Answer:**

- **CSR (Client-Side Rendering - SPA):** Server returns empty HTML `<div id="root"></div>` + large JS bundle. Browser downloads JS, parses, runs React, queries API, and renders. High initial load latency, blank white screen on slow devices.
- **SSR (Server-Side Rendering):** Server runs React on every request, populates HTML with data, and streams fully rendered HTML. Fast FCP/LCP, but higher server TTFB.
- **SSG (Static Site Generation):** HTML is pre-rendered at build time and cached on global Edge CDNs. Lowest possible TTFB ($< 30\text{ms}$), but content is static until re-built or revalidated (ISR).

---

### Q36: What is Cumulative Layout Shift caused by late-loading CSS?

**Answer:**

- If CSS is split incorrectly or loaded asynchronously via JavaScript after HTML has rendered unstyled, applying late CSS rules alters element margins, padding, and font sizes.
- This shifts all elements on the page simultaneously, triggering a massive CLS spike ($> 0.5$).
- **Rule:** Critical above-the-fold CSS must always be **inlined inside `<style>` in the document `<head>`**.

---

### Q37: How do you detect and fix memory leaks in Single Page Applications (SPAs)?

**Answer:**

1. Open Chrome DevTools $\to$ **Memory** tab.
2. Record **Allocation instrumentation on timeline**.
3. Perform repetitive actions (e.g. open and close modal 10 times).
4. If blue allocation spikes do not drop back to zero after manual Garbage Collection, memory is leaking.
5. Take a Heap Snapshot, sort by **Retained Size**, and look for:
   - Uncleared `setInterval` or event listeners attached to `window`.
   - Detached DOM nodes retained in closures.
   - Global Redux/Zustand caches growing without bounds.

---

### Q38: What is the difference between `requestIdleCallback` and `setTimeout(fn, 0)`?

**Answer:**

- `setTimeout(fn, 0)`: Schedules a macrotask that runs at the earliest opportunity in the next event loop turn, regardless of whether the browser is busy rendering.
- `requestIdleCallback(fn, { timeout: 2000 })`: Executes the callback **ONLY when the browser has determined that the main thread is idle** and has spare time remaining before the next frame deadline.

---

### Q39: What is DOM Tree Depth and why does Google recommend $< 1,500$ nodes?

**Answer:**

- Excessive DOM size ($> 1,500$ nodes, depth $> 32$ levels) increases memory usage, slows down CSS selector matching engines, and makes layout reflow computations quadratic $O(N^2)$.
- **Solution:** Flatten nested container wrappers (`<div><div><div>...</div></div></div>`), utilize DOM virtualization, and remove hidden elements.

---

### Q40: What is Partytown and how does it optimize third-party marketing tags?

**Answer:**

- Third-party scripts (Google Tag Manager, Facebook Pixel, Hotjar) consume hundreds of milliseconds of main thread execution time, destroying INP.
- **Partytown:** Relocates and executes third-party scripts inside a background **Web Worker**.
- Uses synchronous `XMLHttpRequest` or `Atomics` to proxy DOM calls from the worker to the main thread transparently, freeing up 100% of the main UI thread for user interaction!
