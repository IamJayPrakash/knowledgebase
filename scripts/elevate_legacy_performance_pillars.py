# scripts/elevate_legacy_performance_pillars.py
import os

BASE_DIR = r"D:\Projects\knowledgebase"

CRP_PATH = os.path.join(BASE_DIR, "01-web-core-and-performance", "frontend-performance-optimization", "01_critical_rendering_path_and_paint.md")
MEDIA_PATH = os.path.join(BASE_DIR, "01-web-core-and-performance", "frontend-performance-optimization", "03_image_and_font_optimization.md")
INP_PATH = os.path.join(BASE_DIR, "01-web-core-and-performance", "web-core-vitals", "02_inp_interaction_to_next_paint_deep_dive.md")
CLS_PATH = os.path.join(BASE_DIR, "01-web-core-and-performance", "web-core-vitals", "03_cls_cumulative_layout_shift_debugging.md")

CRP_PILLARS = """
---

## 4. 📊 Visual Architecture Diagram

```text
Critical Rendering Path (CRP) Execution Flow:

   [ HTML Bytes ] ──> Tokenize ──> [ DOM Tree ] ──┐
                                                   ├──> [ Render Tree ] ──> [ Layout (Reflow) ] ──> [ Paint ] ──> [ Composite ]
   [ CSS Bytes ]  ──> Tokenize ──> [ CSSOM Tree ] ─┘    (Visible Nodes)      (Geometric Coordinates)  (Pixels)    (GPU Layers)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What happens in the browser from the moment HTML and CSS are received to the time pixels appear on screen, and what is Layout Thrashing?"
>
> **You:** "The browser constructs the DOM tree from HTML and the CSSOM tree from CSS in parallel. Because CSS is render-blocking, the Render Tree cannot be constructed until the CSSOM is complete. The Render Tree includes only visible nodes, discarding `display: none` elements. Next, the Layout phase computes exact geometric coordinates, followed by Paint which rasterizes pixels, and Compositing which coordinates GPU layers. Layout Thrashing occurs when JavaScript repeatedly interleaves reading geometric properties like `offsetHeight` with style writes, forcing the browser into expensive synchronous reflows on every loop iteration. We resolve this by batching all reads before performing writes."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An e-commerce product listing page experienced severe scroll stuttering and 15 FPS frame drops on mobile Safari when expanding product specification accordion tabs across 50 items.
* **Task / Challenge:** Restore 60 FPS smooth scrolling and eliminate layout reflow delays.
* **Action Taken:** Performance profiling identified layout thrashing inside a resize listener that queried `element.getBoundingClientRect()` immediately after adjusting container heights. Refactored the DOM mutations using `FastDOM` patterns (batching reads then batching writes) and transitioned accordion animations to CSS `transform` and `opacity` to keep execution entirely on the GPU compositor thread.
* **Result & Business Impact:** Eliminated 100% of forced synchronous layouts, restoring a smooth 60 FPS scroll rate and reducing mobile accordion interaction latency from 320ms to 8ms.
"""

MEDIA_PILLARS = """
---

## 4. 📊 Visual Architecture Diagram

```text
Next-Gen Media Delivery & Variable Font Architecture:

   [ Client Request ]
           │
           ├──> Supports AVIF? ──YES──> [ Serve .avif: 45KB (50% smaller than WebP!) ]
           │
           ├──> Supports WebP? ──YES──> [ Serve .webp: 90KB (30% smaller than JPEG!) ]
           │
           └─── Fallback ────────────> [ Serve .jpg:  180KB (Baseline fallback) ]

   Variable Font:
   1 Master File (Inter-Variable.woff2: 48KB) replaces 8 separate static font weights (240KB total)!
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you optimize media and web fonts for high-traffic enterprise web applications?"
>
> **You:** "Media and web fonts represent over 60% of total transferred web bytes. For media, I implement progressive art direction using the HTML `<picture>` element with modern AVIF as the primary source, WebP as the fallback, and standard JPEG as the baseline, combined with responsive `srcset` and `sizes`. For web fonts, I replace multiple static weight files with a single Variable Font (`.woff2`) which reduces HTTP requests and transfer sizes by up to 75%. Furthermore, I apply font subsetting to eliminate unused character sets, preload critical above-the-fold fonts with `crossorigin`, and declare `font-display: swap` to prevent Flash of Invisible Text."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A fashion retailer's catalog homepage payload exceeded 8.5MB, causing excessive data costs and 6-second page load times on emerging market 3G/4G connections.
* **Task / Challenge:** Reduce total page weight from 8.5MB to under 1.5MB without degrading photographic sharpness.
* **Action Taken:** Audited assets via Lighthouse and WebPageTest. Converted 60 product thumbnail JPEGs to responsive AVIF format via an edge image resizing pipeline, implemented progressive lazy-loading (`loading="lazy"` with low-quality blur-up placeholders for below-the-fold assets), and consolidated 6 separate Google Font files into a single subsetted variable `.woff2` font.
* **Result & Business Impact:** Cut homepage transfer size from 8.5MB down to 1.1MB (an 87% reduction), decreasing mobile bounce rate by 22% and improving catalog conversion by 13.5%.
"""

INP_PILLARS = """
---

## 4. 📊 Visual Architecture Diagram

```text
INP 3-Phase Interaction Timeline:

   [ User Action: Click ]
              │
              ├── 1. Input Delay (Waiting for main-thread Long Tasks to finish)
              │
              ├── 2. Processing Time (Event handler JavaScript execution)
              │
              └── 3. Presentation Delay (Style recalculation, Layout, Paint, Frame swap)
                         │
                         v
              [ Next Paint Appears On Screen! ] (Target: <= 200ms)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What is Interaction to Next Paint (INP), and how does it differ from the old First Input Delay (FID) metric?"
>
> **You:** "First Input Delay (FID) only measured the input delay of the very first user interaction during page load, completely ignoring the event handler execution duration and subsequent interactions. In March 2024, Google replaced FID with Interaction to Next Paint (INP). INP measures the complete end-to-end latency—input delay plus processing duration plus presentation delay—across every single click, tap, and keypress throughout the user's entire session, reporting the worst-case 75th percentile. We optimize INP by breaking long tasks over 50ms using `scheduler.yield()`, keeping event listeners lean, and offloading heavy compute to Web Workers."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A real-time document editor reported poor INP scores exceeding 600ms whenever users pasted large markdown snippets, causing the typing cursor to freeze visibly.
* **Task / Challenge:** Reduce paste and render latency under 150ms.
* **Action Taken:** Profiling showed the markdown syntax highlighter and AST tokenizer ran synchronously inside the `input` event listener on the main thread. Decoupled the syntax tokenization into a background Web Worker via `Comlink` and used `scheduler.yield()` to chunk DOM node updates into 16ms animation frame slices.
* **Result & Business Impact:** Reduced typing and paste INP from 600ms to 32ms, completely eliminating typing freezes for 250,000 daily active writers.
"""

CLS_PILLARS = """
---

## 4. 📊 Visual Architecture Diagram

```text
Cumulative Layout Shift (CLS) Geometry:

   Viewport (1000px high)
   ┌─────────────────────────────────────────┐
   │ [ Nav Bar ]                             │
   │                                         │
   │ [ Ad Banner Injected Late! (200px) ]    │ <── Unstable element pushes content down!
   │                                         │
   │ [ Article Heading ] (Shifted by 200px!) │ <── Shift Distance: 200px / 1000px = 0.20
   │                                         │     Impact Area: 70% of screen = 0.70
   └─────────────────────────────────────────┘     CLS Score = 0.70 * 0.20 = 0.14 (POOR!)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How is Cumulative Layout Shift calculated, and what are the most common causes in production?"
>
> **You:** "Cumulative Layout Shift measures visual stability by multiplying the Impact Fraction—the percentage of the viewport affected by shifting elements—by the Distance Fraction—the greatest distance those elements moved relative to the viewport height. A good CLS score is 0.1 or below. The most common production causes are images and videos without explicit width/height dimensions, dynamic advertisements injected without reserved bounding boxes, Flash of Unstyled Text from un-calibrated fallback fonts, and CSS animations targeting geometric properties like `top` or `height` rather than GPU-accelerated `transform`."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A cryptocurrency exchange trading dashboard suffered a CLS score of 0.38 because live ticker prices and dynamic order book columns constantly resized table headers as numbers fluctuated.
* **Task / Challenge:** Achieve visual stability with a target CLS under 0.05 without hiding dynamic price data.
* **Action Taken:** Fixed numeric font shifting by applying CSS `font-variant-numeric: tabular-nums` (giving all digits uniform monospaced widths), reserved fixed column widths on the order book grid using CSS Grid `grid-template-columns: repeat(4, minmax(120px, 1fr))`, and encapsulated dynamic banner slots with `min-height`.
* **Result & Business Impact:** Dropped CLS from 0.38 to 0.002, moving the application into the top 5% of web performance benchmarks and eliminating accidental click trade executions.
"""

def append_if_missing(fpath, extra_text, search_token):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    if search_token not in content:
        with open(fpath, "a", encoding="utf-8") as f:
            f.write(extra_text.strip() + "\n")
        print(f"Updated: {fpath}")
    else:
        print(f"Already contains pillars: {fpath}")

append_if_missing(CRP_PATH, CRP_PILLARS, "Interview Answering Pitch")
append_if_missing(MEDIA_PATH, MEDIA_PILLARS, "Interview Answering Pitch")
append_if_missing(INP_PATH, INP_PILLARS, "Interview Answering Pitch")
append_if_missing(CLS_PATH, CLS_PILLARS, "Interview Answering Pitch")
print("Done elevating legacy performance files!")
