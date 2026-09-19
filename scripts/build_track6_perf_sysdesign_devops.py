# -*- coding: utf-8 -*-
"""
Generator for Track 6: Core Web Vitals, Performance, System Design, and Testing / DevOps
Generates:
1. 01-core-web-and-performance/web-core-vitals/02_inp_interaction_to_next_paint_deep_dive.md
2. 01-core-web-and-performance/web-core-vitals/03_cls_cumulative_layout_shift_debugging.md
3. 01-core-web-and-performance/frontend-performance-optimization/01_critical_rendering_path_and_paint.md
4. 01-core-web-and-performance/frontend-performance-optimization/03_image_and_font_optimization.md
5. 07-system-design/03_hld_netflix_video_streaming.md
6. 07-system-design/04_hld_uber_ride_matching_spatial_indexing.md
7. 07-system-design/05_lld_parking_lot_system.md
8. 07-system-design/06_lld_distributed_rate_limiter.md
9. 07-system-design/interview-questions/system_design_interview_framework.md
10. 10-testing-and-devops/testing-playwright-jest/02_jest_unit_and_integration_testing.md
11. 10-testing-and-devops/devops-docker-kubernetes-cicd/02_github_actions_production_cicd_pipeline.md
12. 10-testing-and-devops/devops-docker-kubernetes-cicd/03_kubernetes_helm_and_ingress_setup.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "01-core-web-and-performance", "web-core-vitals", "02_inp_interaction_to_next_paint_deep_dive.md"): """# Interaction to Next Paint (INP): Measurement, Optimization, and Yielding

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Purana metric (FID) ek **Restaurant Ke Reception Counter** jaisa tha: Customer ne entry gate par pucha "Table khali hai kya?", receptionist ne 10ms mein bol diya "Haan khali hai" (FID pass!). Lekin table par baithne ke baad jab customer ne menu manga ya paani manga, toh waiter 5 second tak gayab raha (**Bad INP**)!
**INP (Interaction to Next Paint)** restaurant ke **Pure Dinner Experience (Every Click, Tap, Keystroke)** ko monitor karta hai: User ne button dabaya, uske baad screen par visual confirmation (spinner, highlight, dropdown) aane mein kitni der lagi.
Target: **< 200ms**.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **INP Composition**:
   - **Input Delay**: Time between user input and event listener execution (waiting for long tasks on main thread to clear).
   - **Processing Duration**: Time spent executing JS callbacks (`click`, `keydown`).
   - **Presentation Delay**: Time browser needs to recalculate style, layout, composite layers, and paint pixels to screen.
2. **Break Up Long Tasks (`scheduler.yield()` / `setTimeout`)**:
   - Any JavaScript execution over 50ms is classified as a **Long Task**.
   - Yield control back to browser event loop to let it paint the next frame before continuing computation.
3. **Web Workers for Offloading**: Heavy sorting or filtering should run in a Web Worker, not on the UI main thread.

---

## 💻 3. Line-by-Line Commented Code Snippets

```javascript
// Line 2: scheduler.yield() polyfill for main-thread yielding
async function yieldToMain() {
  if ("scheduler" in window && "yield" in window.scheduler) {
    // Modern browser standard yield
    return await window.scheduler.yield();
  }
  // Fallback for older browsers using message channel or setTimeout
  return new Promise((resolve) => {
    setTimeout(resolve, 0);
  });
}

// Processing large dataset with INP preservation
async function filterLargeDatasetWithYielding(items, predicate) {
  const results = [];
  let lastYieldTime = performance.now();

  for (let i = 0; i < items.length; i++) {
    if (predicate(items[i])) {
      results.push(items[i]);
    }

    // Line 23: If continuous JS execution exceeds 16ms (1 frame budget), yield to main thread!
    if (performance.now() - lastYieldTime > 16) {
      // Yield to let browser handle user clicks and render next paint frame!
      await yieldToMain();
      lastYieldTime = performance.now();
    }
  }

  return results;
}
```
""",

    os.path.join(BASE_DIR, "01-core-web-and-performance", "web-core-vitals", "03_cls_cumulative_layout_shift_debugging.md"): """# Cumulative Layout Shift (CLS): Root Causes, Layout Stability, and Fixes

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Aap mobile par ek article padh rahe ho. Aap "Cancel" button dabane wale the, lekin achanak upar ek image ya ad load hua aur pura content 2 inch neeche chhalang maar gaya! Aapka ungli "Confirm Purchase" button par lag gayi! Is unexpected visual jump ko **Layout Shift** kehte hain.
CLS score target: **< 0.1**.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Common Causes of CLS**:
   - Images, videos, or iframes without explicit `width` and `height` (or CSS `aspect-ratio`).
   - Dynamic ad banners and widgets injected without reserved placeholder containers.
   - Web Fonts causing FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text).
   - Injected banners (cookie consents) at the top of the viewport pushing content down.
2. **CSS `aspect-ratio`**: Allows browsers to calculate layout space before images download.
3. **`font-display: optional` or `font-display: swap` with size-adjust**: Eliminates font swap layout jumps.

---

## 💻 3. Line-by-Line Commented Code Snippets

```html
<!-- Line 1: Anti-pattern causing severe CLS: Image without dimensions -->
<!-- <img src="banner.jpg" alt="Sale" /> -->

<!-- Line 4: Correct: Explicit dimensions allow browser to reserve exact layout box -->
<img 
  src="banner.jpg" 
  width="1200" 
  height="400" 
  alt="Summer Sale Banner" 
  style="width: 100%; height: auto; aspect-ratio: 1200 / 400;" 
/>

<!-- Reserved Ad Container to prevent ad injection shifts -->
<div 
  id="ad-banner-slot" 
  style="min-height: 250px; background-color: #f3f4f6; display: flex; align-items: center; justify-content: center;"
>
  <span style="color: #9ca3af;">Advertisement</span>
</div>
```
""",

    os.path.join(BASE_DIR, "01-core-web-and-performance", "frontend-performance-optimization", "01_critical_rendering_path_and_paint.md"): """# Critical Rendering Path (CRP), CSSOM, and Render-Tree Construction

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Browser screen par web page draw karna ek **Film Shooting** ki tarah hai:
1. Script milti hai (HTML Parser -> DOM Tree banata hai).
2. Costumes decide hote hain (CSS Parser -> CSSOM Tree banata hai).
3. Script aur Costume milte hain: Jo actors screen par aayenge sirf unhe list kiya jata hai (Render Tree: `display: none` wale actors bahar nikal diye jate hain!).
4. Camera angles aur stage geometry decide hoti hai (**Layout / Reflow Phase**: Kaun kahan khada hoga, kitne pixel lamba hoga).
5. Colors aur lights turn on hoti hain (**Paint & Composite Phase**).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **CSS is Render-Blocking**: The browser will NOT render any content until the CSSOM tree is completely parsed and constructed.
2. **JavaScript is Parser-Blocking**: `<script>` tags halt HTML parsing while downloading and executing unless `defer` or `async` is used.
   - `defer`: Downloads in parallel, executes in exact document order after DOM parsing finishes.
   - `async`: Downloads in parallel, executes immediately when downloaded (interrupts DOM parsing).
3. **Reflow (Layout) vs Repaint**:
   - Reflow: Calculating element geometries (width, height, margin, top). Triggering reflow on one element can trigger reflow on entire page!
   - Repaint: Visual changes without layout changes (color, background-color, visibility).
   - Composite: Handled by GPU (CSS `transform`, `opacity`). Super fast, zero reflow/repaint cost!

---

## 💻 3. Line-by-Line Commented Code Snippets

```javascript
// ANTI-PATTERN: Layout Thrashing (Forced Synchronous Layout)
// Reading geometry immediately after mutating geometry forces synchronous reflow!
function badResizeBoxes(boxes) {
  for (let i = 0; i < boxes.length; i++) {
    // Reading offsetWidth forces browser to recalculate layout
    const width = boxes[i].offsetWidth;
    // Writing new style invalidates layout
    boxes[i].style.width = width + 10 + "px"; // 1000 reflows in 1 loop!
  }
}

// GOLD STANDARD: Batch Reads then Batch Writes
function goodResizeBoxes(boxes) {
  // Phase 1: Batch all geometric reads
  const widths = boxes.map((box) => box.offsetWidth);

  // Phase 2: Batch all geometric writes (Triggering only 1 single reflow!)
  boxes.forEach((box, i) => {
    box.style.width = widths[i] + 10 + "px";
  });
}
```
""",

    os.path.join(BASE_DIR, "01-core-web-and-performance", "frontend-performance-optimization", "03_image_and_font_optimization.md"): """# Advanced Media and Font Optimization: AVIF, WebP, and Variable Fonts

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Purani JPEG/PNG images ek **Bhari Leather Suitcase** ki tarah hoti hain.
**WebP aur AVIF** ek **Space-Age Vacuum Compression Bag** hain: Picture quality bilkul crystal-clear dikhti hai lekin file size 50% se 80% chota ho jata hai!
Variable Font 10 alag-alag font files (Bold, Light, Italic) download karne ke bajaye ek hi smart master font download karne jaisa hai jo khud ko adjust kar leta hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Next-Gen Image Formats**:
   - **AVIF**: Highest compression efficiency (up to 50% smaller than JPEG with superior chroma fidelity).
   - **WebP**: Universally supported modern standard.
2. **HTML `<picture>` Responsive Art Direction**:
   - Allows browser to pick the best format it supports via progressive fallbacks (AVIF -> WebP -> JPEG).
3. **Font Subsetting & Preload**:
   - Strip out unused characters (e.g. Cyrillic/Greek alphabets if site is in English).
   - Preload critical font files (`<link rel="preload" as="font" crossorigin>`).

---

## 💻 3. Line-by-Line Commented Code Snippets

```html
<!-- Progressive Picture Fallback with AVIF, WebP and JPEG -->
<picture>
  <!-- Browser checks AVIF first (best compression) -->
  <source srcset="hero.avif" type="image/avif" />
  <!-- If AVIF not supported, fallback to WebP -->
  <source srcset="hero.webp" type="image/webp" />
  <!-- Default standard JPEG fallback -->
  <img 
    src="hero.jpg" 
    alt="Hero Product" 
    width="800" 
    height="450" 
    loading="lazy" 
    decoding="async" 
  />
</picture>
```
""",

    os.path.join(BASE_DIR, "07-system-design", "03_hld_netflix_video_streaming.md"): """# High-Level System Design: Global Video Streaming Architecture (Netflix / YouTube)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Jab Netflix par koi 4K movie upload hoti hai, toh wo ek single video file nahi rehti.
**Transcoding Pipeline** us movie ko 1000 alag-alag version mein todta hai: 1080p, 720p, 480p, 360p, aur har resolution ko **2-second ke chote chote tukdo (Chunks)** mein kaat deta hai (**HLS / DASH**).
Jab user local metro mein chalta hai aur network kamzor hota hai, video player apne aap 1080p chunk se 480p chunk par switch kar leta hai (**Adaptive Bitrate Streaming**) taaki video buffering na kare! Aur ye chunks user ke sabse paas wale Internet Provider (ISP) ke **Open Connect CDN Cache** se aate hain!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Scale Requirements**:
   - 250M+ active subscribers globally.
   - Petabytes of video data transmitted every second.
2. **Adaptive Bitrate Streaming (ABR)**:
   - Protocols: HLS (HTTP Live Streaming) and MPEG-DASH.
   - Master manifest file (`playlist.m3u8`) lists bitrates, audio tracks, and subtitles.
   - Player monitors network buffer health and dynamically requests higher/lower bitrate 2-second chunk segments (`.ts` / `.m4s`).
3. **Content Delivery Network (CDN) & Open Connect**:
   - Netflix places physical custom storage appliances (OCAs - Open Connect Appliances) directly inside global Internet Service Provider (ISP) data centers, delivering 95%+ of video traffic locally without traversing internet backbones.
4. **Data Storage Architecture**:
   - Video raw files: Amazon S3 object storage.
   - Metadata & User Viewing History: Cassandra / CockroachDB (distributed wide-column NoSQL).
   - Real-time recommendations: Microservices on AWS, caching via EVCache (distributed memcached).

---

## 📊 3. Visual Architecture Diagram

```
                 GLOBAL VIDEO STREAMING ARCHITECTURE
                 
   [ Creator / Studio ] ──► Raw 4K Master Video ──► AWS S3
                                                        │
                                                        ▼
                                    [ Video Transcoding & Chunking Pipeline ]
                                    (Converts to HLS/DASH 2-second segments)
                                                        │
                                                        ▼
                                    [ Replicate to Edge CDNs / Open Connect ]
                                                        │
                                    ┌───────────────────┴───────────────────┐
                                    ▼                                       ▼
                             [ ISP CDN Node A ]                      [ ISP CDN Node B ]
                                    │                                       │
                                    ▼                                       ▼
                             Client Device                           Client Device
                             (4G Mobile: 720p)                       (Smart TV: 4K HDR)
```
""",

    os.path.join(BASE_DIR, "07-system-design", "04_hld_uber_ride_matching_spatial_indexing.md"): """# High-Level System Design: Real-Time Ride Matching & Geospatial Dispatch (Uber / Lyft)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Agar aapko apne aas-paas 2 kilometer ke andar khadi taxis dhoondni hain, toh database mein 10 lakh drivers ka latitude/longitude scan karna system ko crash kar dega.
**Spatial Indexing (Uber H3 / Google S2)** poori prithvi ko **Chote Chote Hexagons (Madhumakkhi Ke Chhatte)** mein baant deta hai. Har hexagon ka ek unique numeric ID hota hai. Jab rider ride mangta hai, system sirf rider ke hexagon aur uske padosi 6 hexagons ke drivers ko check karta hai (**$O(1)$ Hash Map Lookup**)!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Spatial Indexing Options**:
   - **Uber H3**: Hexagonal hierarchical spatial index. Hexagons have the property that all 6 neighbors have identical center distances (unlike squares).
   - **Google S2 / Geohash**: Quadrilateral hierarchical indexing.
2. **Real-time Location Ingestion**:
   - 5M+ drivers sending GPS coordinates every 4 seconds.
   - Ingestion Layer: WebSockets / gRPC terminating at Netty/Go gateway -> Kafka topic.
   - Memory Cache: In-memory distributed geospatial store (Redis Geo or custom Go ring buffer).
3. **Dispatch & Ride Matching**:
   - Ring search: Match driver within expanding H3 resolution k-ring (Radius 1 -> Radius 2).
   - ETA computation using routing engine (OSRM / Google Maps API).
   - Distributed state machine handling: Driver Offered -> Driver Accepted -> Driver Arrived.

---

## 📊 3. Visual Architecture Diagram

```
                 UBER REAL-TIME DISPATCH PIPELINE
                 
   [ Driver App (GPS) ] ──(Every 4s)──► [ WebSocket Gateway ]
                                                │
                                                ▼
                                         [ Kafka Stream ]
                                                │
                                                ▼
                                   [ Location Worker (Go/Rust) ]
                                   (Maps Lat/Lng to H3 Hexagon ID)
                                                │
                                                ▼
                                    [ Distributed Redis GEO ]
                                                │
   [ Rider Requests Ride ] ─────────────► [ Dispatch Engine ]
                                                │ (Find drivers in H3 Hexagon)
                                                ▼
                                    [ Match & Send Push Notification ]
```
""",

    os.path.join(BASE_DIR, "07-system-design", "05_lld_parking_lot_system.md"): """# Low-Level Design (LLD): Scalable Multi-Floor Parking Lot System

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Parking lot ek **Object-Oriented Mall Parking** hai.
Gaadiyan alag-alag type ki hoti hain (Bike, Car, Truck). Har gaadi ke liye alag size ka spot chahiye (Compact, Large, Handicapped).
System ko pata hona chahiye ki:
- Gaadi aayi -> Ticket print karo jisme entry time ho.
- Gaadi gayi -> Total hours calculate karo, fee calculate karo, aur spot ko khali mark karo.
- SOLID Principles aur Strategy Pattern use karo taaki agar kal nayi Electric Car parking ya Hourly Fee rule badal jaye, toh pura code na rewrite karna pade!

---

## 📌 2. Core OOP Design Patterns Applied
1. **Singleton Pattern**: For `ParkingLot` central instance.
2. **Factory Pattern**: For `Vehicle` and `ParkingFeeStrategy` instantiation.
3. **Strategy Pattern**: For calculating parking charges (Flat rate vs Hourly vs Dynamic peak rate).

---

## 💻 3. Line-by-Line Commented Code Solution (Python)

```python
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# Line 7: Vehicle and Spot Type Enums
class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class SpotType(Enum):
    COMPACT = 1
    MEDIUM = 2
    LARGE = 3

# Line 18: Parking Spot Abstraction
class ParkingSpot:
    def __init__(self, spot_id: str, floor_id: int, spot_type: SpotType):
        self.spot_id = spot_id
        self.floor_id = floor_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle = None

    def park(self, vehicle):
        self.vehicle = vehicle
        self.is_occupied = True

    def unpark(self):
        self.vehicle = None
        self.is_occupied = False

# Line 36: Strategy Pattern for Pricing
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, hours: float, vehicle_type: VehicleType) -> float:
        pass

class HourlyPricingStrategy(PricingStrategy):
    RATES = {
        VehicleType.MOTORCYCLE: 10.0,
        VehicleType.CAR: 20.0,
        VehicleType.TRUCK: 50.0
    }

    def calculate_fee(self, hours: float, vehicle_type: VehicleType) -> float:
        rate = self.RATES.get(vehicle_type, 20.0)
        return max(1.0, hours) * rate

# Line 53: Parking Ticket Entity
class Ticket:
    def __init__(self, spot: ParkingSpot, vehicle_type: VehicleType):
        self.ticket_id = str(uuid.uuid4())[:8]
        self.spot = spot
        self.vehicle_type = vehicle_type
        self.entry_time = datetime.now()

# Line 61: Central ParkingLot Coordinator (Singleton)
class ParkingLot:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.spots = []
        self.pricing_strategy = pricing_strategy

    def add_spot(self, spot: ParkingSpot):
        self.spots.append(spot)

    def issue_ticket(self, vehicle_type: VehicleType) -> Ticket:
        for spot in self.spots:
            if not spot.is_occupied:
                spot.park(vehicle_type)
                return Ticket(spot, vehicle_type)
        raise Exception("Parking Lot is Full!")

    def process_exit(self, ticket: Ticket, duration_hours: float) -> float:
        ticket.spot.unpark()
        return self.pricing_strategy.calculate_fee(duration_hours, ticket.vehicle_type)
```
""",

    os.path.join(BASE_DIR, "07-system-design", "06_lld_distributed_rate_limiter.md"): """# Low-Level Design (LLD): Production Distributed Rate Limiter

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Rate Limiter ek **Token Dispenser Machine** ki tarah hai.
Har user ko ek bucket milti hai jisme har second 5 naye tokens girtay hain (**Token Bucket Algorithm**). Jab user API request karta hai, toh ek token kharch ho jata hai. Agar bucket khali ho gayi, toh system request reject kar deta hai (`429 Too Many Requests`).

---

## 📌 2. Key Algorithms Compared
1. **Token Bucket**: Allows controlled bursts; tokens refill at constant rate.
2. **Leaky Bucket**: Enforces strictly smooth output rate like a FIFO queue.
3. **Sliding Window Log**: Stores timestamps of every request (accurate, high memory).
4. **Sliding Window Counter**: Combines counters from current and previous window (low memory, high accuracy).

---

## 💻 3. Line-by-Line Commented Code Solution (Python Token Bucket)

```python
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        # Line 5: Maximum burst capacity of bucket
        self.capacity = capacity
        # Line 7: Rate at which tokens refill into bucket per second
        self.refill_rate = refill_rate_per_sec
        self.current_tokens = capacity
        self.last_refill_timestamp = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill_timestamp
        # Line 15: Calculate newly accumulated tokens based on elapsed time
        tokens_to_add = elapsed * self.refill_rate
        self.current_tokens = min(self.capacity, self.current_tokens + tokens_to_add)
        self.last_refill_timestamp = now

    def allow_request(self, tokens_needed: int = 1) -> bool:
        self._refill()
        # Line 22: Consume token if available
        if self.current_tokens >= tokens_needed:
            self.current_tokens -= tokens_needed
            return True
        return False
```
""",

    os.path.join(BASE_DIR, "07-system-design", "interview-questions", "system_design_interview_framework.md"): """# Master System Design Interview Framework (The 4-Step Playbook)

---

## 🎯 The 4-Step Structural Playbook

### Step 1: Requirements Clarification & Scope (5-7 Minutes)
- **Functional Requirements**: 3 core user journeys (e.g. "User can shorten URL", "User is redirected to original URL", "Analytics tracking").
- **Non-Functional Requirements**: High availability vs Strong consistency (CAP Theorem), latency target (P99 < 50ms), throughput (Read:Write ratio).
- **Scale Estimations (Back of the Envelope)**: DAU, Read QPS, Write QPS, Storage per year, Network Bandwidth.

### Step 2: High-Level Architecture & API Design (10-12 Minutes)
- Define clean REST / gRPC API contracts.
- Draw main components: Client -> DNS/CDN -> API Gateway / Load Balancer -> Application Services -> Caching Layer -> Primary/Replica Databases.

### Step 3: Deep Dive into Core Bottlenecks (15-20 Minutes)
- Partitioning/Sharding strategy (Hash vs Range).
- Caching policies (Cache-Aside, Write-Through, LRU).
- Fault tolerance, replication lag, and split-brain scenarios.

### Step 4: Wrap-Up, Resilience & Bottleneck Resolution (5 Minutes)
- Single Point of Failure (SPOF) audit.
- Rate limiting, Circuit Breakers, and DDoS mitigation.
- Monitoring, SLIs, and SLOs (Prometheus/Grafana).
""",

    os.path.join(BASE_DIR, "10-testing-and-devops", "testing-playwright-jest", "02_jest_unit_and_integration_testing.md"): """# Jest & React Testing Library: Unit, Integration, and Mocking Mastery

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Code test na karna **Bina Safety Net Ke Circus Mein Rope Par Chalne Jaisa Hai**.
**Unit Test** ek screw check karne jaisa hai: "Kya ye screw theek se tight ho raha hai?".
**Integration Test** poori bicycle chala ke dekhne jaisa hai: "Pedal marne par chain ghoom rahi hai aur pahiya chal raha hai ya nahi?".
**React Testing Library** ka golden rule hai: **"Test your app the way real users use it!"** Internal state variables check mat karo; check karo ki button screen par dikh raha hai aur click karne par expected text aaya ya nahi.

---

## 💻 2. Line-by-Line Commented Code Snippets

```javascript
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { UserProfileLoader } from "./UserProfileLoader";

// Line 6: Mocking external fetch API
beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.clearAllMocks();
});

describe("UserProfileLoader Integration Test", () => {
  test("renders user profile data after successful API fetch", async () => {
    // Line 17: Mock resolved API payload
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 101, username: "jay_lead", email: "jay@test.com" })
    });

    // Line 23: Render component into simulated DOM
    render(<UserProfileLoader userId={101} />);

    // Line 26: Verify loading spinner appears initially
    expect(screen.getByText(/loading profile/i)).toBeInTheDocument();

    // Line 29: Wait for asynchronous fetch resolution and UI update
    await waitFor(() => {
      expect(screen.getByText(/jay_lead/i)).toBeInTheDocument();
    });

    // Line 34: Assert API was called with correct parameters
    expect(global.fetch).toHaveBeenCalledWith("/api/v1/users/101");
  });
});
```
""",

    os.path.join(BASE_DIR, "10-testing-and-devops", "devops-docker-kubernetes-cicd", "02_github_actions_production_cicd_pipeline.md"): """# Production CI/CD Pipeline with GitHub Actions and Docker Buildx

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
GitHub Actions ek **Automated Assembly Inspection Robot** hai:
Jaise hi developer code commit karke push karta hai:
1. Robot code download karta hai.
2. Linter aur TypeScript compiler chala ke spelling aur types check karta hai.
3. Automated test suits chala ke verify karta hai ki koi feature toota toh nahi.
4. Docker container build karta hai aur production server (Kubernetes) par naya code live deploy kar deta hai bina kisi manual button dabaye!

---

## 💻 2. Line-by-Line Commented Workflow YAML

```yaml
name: Production CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-and-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: Install Dependencies
        run: npm ci

      - name: Run ESLint & TypeScript Validation
        run: npm run lint && npm run type-check

      - name: Execute Automated Unit Tests
        run: npm test -- --ci --coverage

  build-and-push-docker:
    needs: test-and-lint
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: actions/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & Push Multi-Arch Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```
""",

    os.path.join(BASE_DIR, "10-testing-and-devops", "devops-docker-kubernetes-cicd", "03_kubernetes_helm_and_ingress_setup.md"): """# Kubernetes Production Deployment: Helm Charts, Ingress, and HPA

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Kubernetes ek **Container Cargo Ship ka Captain** hai:
- **Pod**: Ek container box jisme aapka application code chal raha hai.
- **Service**: Ek internal intercom phone number taaki doosre containers isse baat kar sakein.
- **Ingress Controller (NGINX)**: Port ka security gate jo internet se aane wale URL (`https://api.domain.com`) ko sahi container tak pahunchata hai.
- **HPA (Horizontal Pod Autoscaler)**: Captain dekhta hai ki load badh raha hai, toh wo 2 pods ki jagah 10 pods auto-scale kar deta hai!

---

## 💻 2. Line-by-Line Commented Kubernetes Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: knowledgebase-api
  labels:
    app: knowledgebase-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: knowledgebase-api
  template:
    metadata:
      labels:
        app: knowledgebase-api
    spec:
      containers:
        - name: web
          image: ghcr.io/iamjayprakash/knowledgebase:latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
---
# hpa.yaml - Horizontal Pod Autoscaler based on CPU
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: knowledgebase-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: knowledgebase-api
  minReplicas: 3
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 75
```
"""
}

def main():
    print(f"Generating {len(FILES)} Track 6 Perf, System Design & DevOps files...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Track 6 Perf, System Design & DevOps generation complete!")

if __name__ == "__main__":
    main()
