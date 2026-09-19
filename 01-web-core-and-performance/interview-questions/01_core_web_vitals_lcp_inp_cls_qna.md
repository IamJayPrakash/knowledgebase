# Web Performance Master Interview Bank: Part 1 (Q1 - Q20)
## Core Web Vitals (LCP, INP, CLS) & Field vs Lab Metrics

---

### Q1: What are Google's 3 Core Web Vitals (CWV) in 2024-2026 and their 75th percentile thresholds?
**Answer:**
Google assesses web user experience across 3 key pillars (measured at the **75th percentile of real users**):
1. **LCP (Largest Contentful Paint) - Loading Performance:**
   Measures perceived load speed (when the main content of the page has likely loaded).
   - *Good:* $\le 2.5\text{ seconds}$.
   - *Needs Improvement:* $2.5\text{s} - 4.0\text{s}$.
   - *Poor:* $> 4.0\text{ seconds}$.
2. **INP (Interaction to Next Paint) - Responsiveness:**
   Measures overall page responsiveness to user interactions throughout the entire session (replaced FID in March 2024).
   - *Good:* $\le 200\text{ milliseconds}$.
   - *Needs Improvement:* $200\text{ms} - 500\text{ms}$.
   - *Poor:* $> 500\text{ milliseconds}$.
3. **CLS (Cumulative Layout Shift) - Visual Stability:**
   Measures unexpected layout shifts of visual elements during the session.
   - *Good:* $\le 0.1$.
   - *Needs Improvement:* $0.1 - 0.25$.
   - *Poor:* $> 0.25$.

---

### Q2: Why did Google replace FID (First Input Delay) with INP (Interaction to Next Paint)?
**Answer:**
- **FID Limitation:** FID only measured the delay of the **very first interaction** (e.g. first click) and measured **only the Input Delay** (time waiting for the main thread to pick up the event handler), ignoring event processing time and browser rendering delay. Once hydrated, a page could have terrible lag on subsequent clicks and still pass FID!
- **INP Solution:**
  1. Observes **all discrete user interactions** (clicks, taps, keystrokes) throughout the entire lifespan of the page.
  2. Measures the **full latency from user action to visual frame paint** (Input Delay + Processing Time + Presentation Delay).
  3. Reports the worst (or near-worst 98th percentile) interaction as the page's INP score.

---

### Q3: What are the 4 sub-parts of Largest Contentful Paint (LCP)?
**Answer:**
$$\text{LCP} = \text{TTFB} + \text{Resource Load Delay} + \text{Resource Load Duration} + \text{Element Render Delay}$$
1. **Time to First Byte (TTFB):** Time from page request until the browser receives the first byte of HTML from server/CDN. (Target: $< 800\text{ms}$).
2. **Resource Load Delay:** Time between TTFB and when the browser discovers and starts fetching the LCP asset. (Target: $< 10\%\text{ of total LCP}$).
3. **Resource Load Duration:** Time spent downloading the LCP image or video asset over the network. (Target: $< 40\%\text{ of total LCP}$).
4. **Element Render Delay:** Time between when the LCP asset finishes downloading and when the browser actually renders it on screen. (Target: $< 10\%\text{ of total LCP}$).

---

### Q4: Why is adding `loading="lazy"` to a hero image an LCP disaster?
**Answer:**
- `loading="lazy"` tells the browser: "Do not download this image until it is near the visible viewport after layout calculation."
- Browsers will **delay initiating the network request** for lazy-loaded images until after the HTML is parsed, CSS is downloaded, and the layout tree is calculated.
- **Impact:** Adds hundreds of milliseconds of artificial **Resource Load Delay** directly to your LCP!
- **Fix:** Always set `loading="eager"` (or omit `loading`) AND add **`fetchpriority="high"`** to the above-the-fold hero image:
  ```html
  <img src="/hero.webp" fetchpriority="high" alt="Featured Product" />
  ```

---

### Q5: What are the 3 phases of an INP interaction?
**Answer:**
$$\text{Interaction Latency} = \text{Input Delay} + \text{Processing Duration} + \text{Presentation Delay}$$
1. **Input Delay:** Time waiting for background long tasks on the main thread to finish before the browser can even begin running your click event listener.
2. **Processing Duration:** Time spent executing the JavaScript code inside your event listeners (`onClick`, `onKeyDown`).
3. **Presentation Delay:** Time spent by the browser recalculating styles, performing layout reflow, and compositing/painting the new visual frame onto the screen.

---

### Q6: What is a "Long Task" on the main thread and how does `scheduler.yield()` fix it?
**Answer:**
- Any JavaScript task that executes continuously on the main thread for **$> 50\text{ milliseconds}$** is classified as a **Long Task**.
- Long tasks freeze the main thread, blocking user input and driving up INP.
- **`scheduler.yield()` (Modern Web API):**
  Allows long-running JavaScript loops to break work into small micro-chunks, yield control back to the browser to process clicks and render a frame, and automatically resume work immediately:

```javascript
async function processLargeDataset(items) {
  for (let i = 0; i < items.length; i++) {
    computeItem(items[i]);

    // Check if task chunk is taking too long (> 16ms frame budget):
    if (performance.now() - lastYield > 16) {
      if ('scheduler' in window && 'yield' in scheduler) {
        await scheduler.yield(); // Clean native yielding!
      } else {
        await new Promise(resolve => setTimeout(resolve, 0)); // Fallback
      }
      lastYield = performance.now();
    }
  }
}
```

---

### Q7: How does Cumulative Layout Shift (CLS) mathematically calculate shifts?
**Answer:**
$$\text{Layout Shift Score} = \text{Impact Fraction} \times \text{Distance Fraction}$$
- **Impact Fraction:** The union of the visible area of the unstable element before and after the shift relative to the total viewport area (e.g. element occupies 50% of viewport and moves down by 25% $\to$ impact fraction = 0.75).
- **Distance Fraction:** The greatest distance an unstable element moved relative to the viewport's height or width (e.g. moved 200px on an 800px screen $\to$ distance fraction = 0.25).
- $\text{Score} = 0.75 \times 0.25 = 0.1875$ (Fails the $< 0.1$ threshold!).

---

### Q8: What are the 3 primary causes of Cumulative Layout Shift (CLS) and their solutions?
**Answer:**
1. **Images & Videos without Dimensions:**
   - *Fix:* Always declare `width` and `height` attributes or CSS `aspect-ratio: 16 / 9;` so the browser reserves layout space before images load.
2. **Dynamic Advertisements & Embeds:**
   - *Fix:* Wrap ad slots in fixed-height placeholder containers or skeleton loaders (`min-height: 250px`).
3. **Web Fonts (FOUT / FOIT):**
   - *Fix:* Use CSS `@font-face` with `size-adjust`, `ascent-override`, and `descent-override` so the fallback system font matches the exact bounding dimensions of the custom web font.

---

### Q9: What is the difference between Field Data (CrUX) and Lab Data (Lighthouse)?
**Answer:**
- **Lab Data (Google Lighthouse / Synthetic Testing):**
  - Collected in a controlled environment with simulated hardware throttling (simulated 4G mobile, 4x CPU slowdown).
  - *Pros:* Reproducible; ideal for local debugging and CI/CD pipelines.
  - *Cons:* Does NOT reflect real user network variability, device diversity, or live session interactions (cannot measure true INP!).
- **Field Data (Chrome User Experience Report - CrUX / RUM):**
  - Collected from **real human visitors** using Google Chrome worldwide over a 28-day rolling window.
  - *Significance:* **Google Search SEO rankings ONLY use Field Data (CrUX)**. Passing Lighthouse 100 in the lab does NOT guarantee passing Core Web Vitals in Google Search Console!

---

### Q10: How do you measure Core Web Vitals programmatically in production JavaScript?
**Answer:**
Use the official Google **`web-vitals` library** and beacon metrics to an analytics endpoint:

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating, // 'good' | 'needs-improvement' | 'poor'
    delta: metric.delta,
    id: metric.id,
  });

  // Use sendBeacon to guarantee delivery during page unload without blocking:
  navigator.sendBeacon('/analytics/cwv', body);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

---

### Q11: What is the difference between FOUT (Flash of Unstyled Text) and FOIT (Flash of Invisible Text)?
**Answer:**
- **FOIT (Flash of Invisible Text):** The browser hides text until the custom font finishes downloading (`font-display: block`). If the font takes 3 seconds, users see a blank screen.
- **FOUT (Flash of Unstyled Text):** The browser renders text immediately using a fallback system font (Arial), and swaps in the custom font when ready (`font-display: swap`).
- **The CLS Catch:** When `font-display: swap` swaps the font, differing character widths trigger a layout shift (CLS).
- **Fix:** Use `font-display: optional` (cancels font download if not cached within 100ms) or tune font metrics using `size-adjust`.

---

### Q12: What is Time to First Byte (TTFB) and what server optimizations reduce it?
**Answer:**
- **TTFB:** Time elapsed between user navigation start and the arrival of the first response byte from the server.
- **Optimizations:**
  1. **Edge CDN HTML Caching:** Cache static and ISR HTML pages at Cloudflare / CloudFront edge PoPs close to users (reduces TTFB from 600ms to $< 50\text{ms}$).
  2. **Streaming SSR:** Send the initial `<head>` shell immediately while database queries run in parallel.
  3. **Database Connection Pooling:** PgBouncer to eliminate DB connection handshakes.
  4. **HTTP/3 & TLS 1.3:** 0-RTT session resumption.

---

### Q13: What is Layout Thrashing (Forced Synchronous Layout) and how do you profile it?
**Answer:**
- **Layout Thrashing:** When JavaScript queries a geometric DOM property (e.g. `element.offsetWidth`, `element.scrollTop`, `getComputedStyle()`) immediately after modifying DOM styles (e.g. `element.style.width = ...`).
- The browser cannot wait for the end of the frame; it is **forced to stop and recalculate layout synchronously** on the spot to answer the read query.
- **Chrome DevTools Profiling:** In Performance tab, appears as repeated red warning badges labeled: **`Forced Reflow`** or **`Recalculate Style`** taking $> 10\text{ms}$.

---

### Q14: What is CSS `content-visibility: auto` and how does it improve initial rendering?
**Answer:**
- `content-visibility: auto` tells the browser engine to **skip rendering (layout, style, and paint) for off-screen elements** until the user scrolls close to them.
- **Benefit:** Cuts initial DOM rendering time on large pages (e.g. 5,000 DOM nodes) by up to 70%!
- **Mandatory Companion Rule:** Always pair with **`contain-intrinsic-size`** (e.g. `contain-intrinsic-size: 0 500px;`) to provide an estimated placeholder height, preventing scrollbar jumping and CLS bugs.

---

### Q15: Why should you avoid CSS `@import` inside stylesheets?
**Answer:**
- When the browser downloads a CSS file containing `@import url("other.css");`, it cannot start downloading `other.css` until it has finished parsing the first file.
- Creates **sequential network request waterfalls** that delay the Critical Rendering Path and directly inflate LCP.
- **Fix:** Use multiple `<link rel="stylesheet">` tags in HTML (which download concurrently in parallel) or bundle stylesheets into a single minified bundle during build.

---

### Q16: What is the Speculation Rules API and how does it achieve 0ms navigation?
**Answer:**
- Modern JSON-based browser API that enables **instant prerendering of full pages in the background** before the user clicks a link:
  ```html
  <script type="speculationrules">
  {
    "prerender": [
      {
        "source": "list",
        "urls": ["/checkout", "/pricing"],
        "eagerness": "moderate"
      }
    ]
  }
  </script>
  ```
- **"Moderate" Eagerness:** Pre-renders the destination page as soon as the user hovers over the link or moves the pointer towards it. When clicked, navigation is **completely instantaneous ($0\text{ms}$ LCP)!**

---

### Q17: What are Resource Hints: `dns-prefetch`, `preconnect`, `preload`, and `prefetch`?
**Answer:**
1. **`dns-prefetch`:** Resolves the DNS of a third-party domain in the background (`<link rel="dns-prefetch" href="https://api.cdn.com">`).
2. **`preconnect`:** Performs DNS lookup + TCP handshake + TLS negotiation ahead of time.
3. **`preload`:** High-priority imperative instruction telling the browser to fetch a critical resource needed for the **current page** immediately (`<link rel="preload" href="/hero.webp" as="image">`).
4. **`prefetch`:** Low-priority background hint fetching resources needed for the **next probable page navigation**.

---

### Q18: What is the difference between Brotli (`br`) and Gzip (`gzip`) compression?
**Answer:**
- **Brotli (`br`):** Modern compression algorithm developed by Google.
  - Achieves **15% to 25% smaller file sizes** than Gzip for text assets (JavaScript, CSS, HTML).
  - Uses a built-in static dictionary of common web words and phrases.
- **Production Standard:** Configure web servers (NGINX/Cloudflare) to serve Brotli for all modern browsers (`Accept-Encoding: br`), falling back to Gzip for legacy clients.

---

### Q19: What is `Cache-Control: public, max-age=31536000, immutable`?
**Answer:**
- Tells browsers and CDN proxies:
  - `public`: Any intermediary cache (CDN, proxy) can store the response.
  - `max-age=31536000`: Cache for 1 full year (31,536,000 seconds).
  - **`immutable`:** The file content will **never change** during its lifetime. The browser will NOT send a conditional HTTP `304 Not Modified` validation request on page reloads!
- **Requirement:** Must be paired with **Cache-Busting Content Hashes** in asset file names (`app.a89f7b.js`).

---

### Q20: How does `stale-while-revalidate` caching header work?
**Answer:**
- `Cache-Control: max-age=60, stale-while-revalidate=86400`
  1. Requests within 60 seconds are served instantly from cache (Fresh).
  2. Requests between 60 seconds and 24 hours (86,400s) are **served instantly from stale cache**, while the browser/CDN automatically fires an asynchronous background request to fetch fresh data and update the cache!
  3. Gives users **instant 0ms response latency** while keeping data reasonably up-to-date.
