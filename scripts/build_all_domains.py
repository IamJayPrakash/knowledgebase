import os

BASE_DIR = r"D:\Projects\knowledgebase"

DOMAINS_DATA = [
    # 01. Web Core Vitals & Performance
    {
        "dir": "01-core-web-and-performance/web-core-vitals",
        "file": "01_core_web_vitals_lcp_inp_cls.md",
        "title": "Google Core Web Vitals: LCP, INP, and CLS",
        "hinglish": "Website user experience ko measure karne ke liye Google ke 3 golden metrics: LCP (kitni jaldi main content dikha), INP (button click karne par site ne kitni der baad respond kiya), aur CLS (load hote waqt page ke buttons ya layout kitna hila).",
        "analogy": "Visiting a restaurant: LCP is how quickly your main dish arrives, INP is how fast the waiter turns around when you call him, and CLS is making sure the table doesn't shake while you are eating.",
        "points": [
            "Largest Contentful Paint (LCP): Measures perceived loading speed. Benchmark: <= 2.5 seconds.",
            "Interaction to Next Paint (INP): Replaced FID in March 2024. Measures total UI responsiveness throughout the session. Benchmark: <= 200 milliseconds.",
            "Cumulative Layout Shift (CLS): Measures visual stability. Benchmark: <= 0.1 score.",
            "Time to First Byte (TTFB): Backend server response time benchmark: <= 800ms."
        ],
        "diagram": """[Navigation Start]
       │
       ├──> [TTFB] (Server response <= 800ms)
       │
       ├──> [FCP] (First text/image rendered)
       │
       ├──> [LCP] (Main hero banner / H1 rendered <= 2.5s)  <-- Vital 1
       │
       ├──> [CLS] (Layout shifts prevented <= 0.1 score)    <-- Vital 2
       │
       └──> [INP] (Interaction delay <= 200ms)               <-- Vital 3""",
        "code": """// Tracking Core Web Vitals in JavaScript
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP((metric) => console.log('LCP Value:', metric.value, metric.rating));
onINP((metric) => console.log('INP Value:', metric.value, metric.rating));
onCLS((metric) => console.log('CLS Value:', metric.value, metric.rating));""",
        "pitch": "Core Web Vitals are Google's essential user-centric metrics for web health. LCP gauges loading speed targeting under 2.5s, INP measures page responsiveness targeting under 200ms, and CLS tracks layout stability targeting under 0.1. Optimizing these improves both real-world user engagement and SEO rankings.",
        "star": "E-commerce landing page was suffering from a poor Google PageSpeed score (34/100) and 4.2s LCP, hurting organic Google search rankings.",
        "action": "Preloaded the hero image using `<link rel='preload'>`, set explicit image width/height dimensions to eliminate CLS, and offloaded heavy third-party tracking scripts to Web Workers via Partytown.",
        "metrics": "LCP improved from 4.2s to 1.6s; CLS dropped from 0.38 to 0.02; mobile conversion rate increased by 14%."
    },

    # 02. Performance Optimization
    {
        "dir": "01-core-web-and-performance/frontend-performance-optimization",
        "file": "02_bundle_splitting_and_lazy_loading.md",
        "title": "Frontend Bundle Splitting, Tree Shaking & Lazy Loading",
        "hinglish": "Agar ek hi bundle.js me poori application (admin dashboard, charts, billing) bhej doge toh pehli baar khulne me bohot time lagega. Dynamic import aur lazy loading se user ko wahi code bhejo jo us page ke liye zaroori hai.",
        "analogy": "Instead of ordering the entire restaurant menu at once, you only order the appetizer first, saving table space and preparation time.",
        "points": [
            "Route-based Code Splitting using React.lazy() and dynamic imports `import()`.",
            "Tree Shaking eliminates dead / unused code from production bundles via ES Module static analysis.",
            "Vendor Chunking separates rarely changing third-party libraries (React, Lodash) from application business logic.",
            "Component Virtualization renders only visible DOM rows using tools like `react-window`."
        ],
        "diagram": """[Single Huge 8MB bundle.js]  ❌ (Slow initial load)
                 │
                 ▼
[Split Modern Architecture]  ✅
 ├── main.js (80KB - Core Framework)
 ├── home-page.js (40KB - Loaded now)
 ├── admin.chunk.js (Lazy-loaded on demand)
 └── charts.chunk.js (Lazy-loaded on demand)""",
        "code": """import React, { Suspense, lazy } from 'react';

// Lazy load heavy analytics component
const AnalyticsDashboard = lazy(() => import('./AnalyticsDashboard'));

function App() {
  return (
    <Suspense fallback={<div className="spinner">Loading Dashboard...</div>}>
      <AnalyticsDashboard />
    </Suspense>
  );
}""",
        "pitch": "Code splitting breaks large monolithic JavaScript bundles into smaller chunks loaded on demand. By leveraging dynamic imports and React Suspense, we ensure users download only the code required for their immediate viewport, drastically slashing initial load time and Main-Thread blocking.",
        "star": "Enterprise SaaS dashboard initial JavaScript bundle was 6.8MB, taking 9 seconds on 3G connections and crashing low-end mobile devices.",
        "action": "Implemented route-level lazy loading with Vite, replaced Moment.js with date-fns for tree-shaking, and separated vendor libraries into long-term cached chunks.",
        "metrics": "Initial bundle size dropped from 6.8MB to 420KB (93% reduction); Time-to-Interactive improved from 9.1s to 1.8s."
    },

    # 03. Next.js App Router & RSC
    {
        "dir": "04-frontend-frameworks/nextjs",
        "file": "01_app_router_and_react_server_components.md",
        "title": "Next.js App Router & React Server Components (RSC)",
        "hinglish": "Next.js App Router me by default har component ek Server Component hota hai. Matlab wo sirf server par execute hota hai, database se direct connect kar sakta hai, aur uska JavaScript code browser ko kabhi bheja hi nahi jata (Zero Client Bundle!).",
        "analogy": "A cooked meal delivered to your doorstep. You receive the ready-to-eat hot food directly without having to bring the restaurant's kitchen, stove, and chef into your living room.",
        "points": [
            "Server Components (Default): Execute exclusively on the server, direct access to databases and backend secrets, zero bundle size sent to browser.",
            "Client Components (`'use client'`): Hydrate on the client to enable user interactivity, `useState`, `useEffect`, and event handlers.",
            "Streaming SSR with `<Suspense>`: Streams HTML chunks to the browser as database queries resolve, without waiting for the slowest query.",
            "Data Fetching & Cache: Native `fetch` extensions for Static Site Generation (SSG), Incremental Static Regeneration (ISR), and Dynamic Rendering."
        ],
        "diagram": """[Client Browser Request] 
            │
            ▼
[Next.js Server Execution]
 ├── Server Component A (DB Query: 20ms) ──> Streamed to browser
 ├── Server Component B (Suspense: 100ms) ──> Skeleton shown -> Streamed
 └── Client Component C ('use client')   ──> Hydrated with interactive JS""",
        "code": """// app/products/page.tsx (Server Component - Zero client JS!)
import db from '@/lib/db';
import AddToCartButton from './AddToCartButton'; // Client Component

export default async function ProductsPage() {
  const products = await db.product.findMany(); // Direct DB query!

  return (
    <div>
      <h1>Product Catalog</h1>
      {products.map(p => (
        <div key={p.id}>
          <h3>{p.name} - ${p.price}</h3>
          <AddToCartButton productId={p.id} />
        </div>
      ))}
    </div>
  );
}""",
        "pitch": "React Server Components fundamentally separate data-fetching and rendering between the server and the browser. Server Components run solely on the server with zero client bundle impact, while Client Components handle interactivity. In Next.js App Router, this enables seamless streaming SSR, direct database access, and superior web performance.",
        "star": "E-commerce product detail page had massive bundle bloat (Markdown parsers and syntax highlighters sent to client) causing slow mobile hydration.",
        "action": "Migrated from Pages Router to Next.js App Router, converting static renderers to Server Components and isolating interactive buttons to lightweight Client Components.",
        "metrics": "Client JavaScript bundle reduced by 68%; Total Blocking Time (TBT) dropped from 850ms to 40ms."
    },

    # 04. Angular Signals & Architecture
    {
        "dir": "04-frontend-frameworks/angular",
        "file": "01_angular_architecture_and_signals.md",
        "title": "Angular Architecture: Components, Dependency Injection & Signals",
        "hinglish": "Angular ek complete enterprise framework hai jisme routing, forms, HTTP client sab built-in hota hai. Angular 16+ me Signals aane se zone.js ke bina direct fine-grained reactivity milti hai, jisse poora component tree check nahi karna padta.",
        "analogy": "A smart electric grid: instead of checking every house in the city when one lightbulb switches on, Signals pinpoint the exact switch and lamp instantly.",
        "points": [
            "Dependency Injection (DI): Hierarchical injector system providing singletons and scoped service instances.",
            "Angular Signals (`signal`, `computed`, `effect`): Fine-grained reactivity tracking exact DOM dependencies without Zone.js dirty-checking.",
            "Standalone Components: Modern Angular eliminates the boilerplate of `NgModule`.",
            "RxJS Observables: Powerful reactive stream management for asynchronous event handling and HTTP requests."
        ],
        "diagram": """[Traditional Zone.js] 
 Event occurred ──> Traverse entire Component Tree ──> Dirty Checking (Heavy)

[Modern Angular Signals]
 Signal updated ──> Directly update target DOM node (O(1) Surgical Update)""",
        "code": """import { Component, signal, computed } from '@angular/core';

@Component({
  selector: 'app-cart',
  standalone: true,
  template: `
    <h2>Cart Items: {{ count() }}</h2>
    <p>Total Price: {{ totalPrice() }}</p>
    <button (click)="addItem()">Add Item ($10)</button>
  `
})
export class CartComponent {
  count = signal(1);
  itemPrice = 10;
  totalPrice = computed(() => this.count() * this.itemPrice);

  addItem() {
    this.count.update(c => c + 1);
  }
}""",
        "pitch": "Angular is a batteries-included enterprise TypeScript framework. With modern Standalone Components and Signals, Angular has evolved to fine-grained reactivity, updating exact DOM bindings without traversing the full component tree, making it ideal for high-scale enterprise dashboards.",
        "star": "Banking financial trading portal rendering 5,000 live updating stock ticker rows experienced frequent UI stutter under high Zone.js change detection load.",
        "action": "Refactored real-time websocket data feeds to Angular Signals with `ChangeDetectionStrategy.OnPush`, decoupling updates from global Zone.js passes.",
        "metrics": "Garbage collection pauses eliminated; UI rendering stabilized at a fluid 60 FPS under 100 updates/sec."
    },

    # 05. Java Spring Boot Fundamentals
    {
        "dir": "05-backend-and-runtimes/java-springboot",
        "file": "01_springboot_architecture_and_jvm.md",
        "title": "Java Spring Boot: Inversion of Control, JVM Memory & Microservices",
        "hinglish": "Spring Boot enterprise backends ka backbone hai. IoC (Inversion of Control) aur Dependency Injection ke zariye objects ka lifecycle Spring container manage karta hai, developer ko manually `new Service()` nahi likhna padta.",
        "analogy": "A car assembly line: instead of every engineer forging their own bolts and engine parts, the central factory provides ready-to-plug components.",
        "points": [
            "Inversion of Control (IoC) & ApplicationContext: Spring Container manages Bean lifecycle, instantiation, and wiring.",
            "Core Annotations: `@RestController`, `@Service`, `@Repository`, `@Autowired`, `@Configuration`, `@Transactional`.",
            "JVM Memory Architecture: Heap (Young Gen - Eden/Survivor, Old Gen) vs Metaspace vs Stack (Thread frames).",
            "Spring Data JPA & Hibernate: Object-Relational Mapping, lazy loading pitfalls, preventing N+1 queries using `JOIN FETCH`."
        ],
        "diagram": """[HTTP Request]
       │
       ▼
[@RestController] ──(Injects)──> [@Service Layer] ──(Injects)──> [@Repository Layer]
                                                                        │
                                                                        ▼
                                                                [PostgreSQL / MySQL]""",
        "code": """@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    private final OrderService orderService;

    // Constructor Dependency Injection (Recommended)
    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(@Valid @RequestBody OrderRequest req) {
        OrderResponse response = orderService.processOrder(req);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }
}""",
        "pitch": "Spring Boot simplifies Java enterprise application development with convention-over-configuration and production-ready embedded servers. Its IoC container provides robust Dependency Injection, while Spring Data JPA streamlines persistence. Understanding JVM heap generational garbage collection is crucial for tuning high-concurrency Spring Boot microservices.",
        "star": "Payment gateway processing microservice handling 15,000 requests/second was experiencing random 4-second latency spikes caused by Full GC pauses in the JVM Old Generation.",
        "action": "Analyzed GC logs, migrated from standard Parallel GC to the G1 Garbage Collector with tuned `-XX:MaxGCPauseMillis=200`, and refactored Hibernate entity queries to avoid detached object retention.",
        "metrics": "P99 latency dropped from 4,200ms to 85ms; eliminated JVM OutOfMemory (OOM) errors during peak billing hours."
    },

    # 06. Playwright E2E Testing
    {
        "dir": "10-testing-and-devops/testing-playwright-jest",
        "file": "01_playwright_e2e_testing_guide.md",
        "title": "Modern E2E Testing with Playwright & Unit Testing with Jest",
        "hinglish": "Playwright aaj ke time ka sabse fast aur reliable E2E automation tool hai. Ye Chromium, Firefox, aur WebKit sab me auto-wait karta hai (no random `sleep(5000)`), network calls mock kar sakta hai, aur parallel testing execute karta hai.",
        "analogy": "A robot tester that opens the actual browser, fills in forms, clicks buttons, and verifies that the receipt was printed, exactly like a real human customer would.",
        "points": [
            "Auto-Waiting: Playwright automatically waits for elements to be actionable (visible, enabled, stable) before clicking.",
            "Cross-Browser & Multi-Tab: Tests against Chromium, WebKit (Safari), and Firefox simultaneously with mobile emulation.",
            "Network Interception: Mock backend API responses to test edge cases (500 errors, slow network, timeouts).",
            "Trace Viewer & Video Recording: Complete step-by-step visual debugging recording DOM snapshots and network calls."
        ],
        "diagram": """[Playwright Test Runner]
       │ (WebSocket Connection)
       ▼
[Browser Context (Chromium / WebKit / Firefox)]
 ├── Page 1: User Login
 ├── Auto-wait for selector (#submit-btn)
 ├── Intercept API (/api/v1/auth) -> Mock 200 OK
 └── Assert: Expect dashboard URL to be visible""",
        "code": """import { test, expect } from '@playwright/test';

test('User successfully logs in and views dashboard', async ({ page }) => {
  // Navigate to login
  await page.goto('https://app.example.com/login');

  // Fill in credentials with auto-waiting
  await page.fill('input[name="email"]', 'engineer@example.com');
  await page.fill('input[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');

  // Verify dashboard navigation
  await expect(page).toHaveURL(/.*dashboard/);
  await expect(page.locator('h1.welcome-title')).toContainText('Welcome back');
});""",
        "pitch": "Playwright is the modern gold standard for End-to-End automation, offering built-in auto-waiting, isolated browser contexts, and out-of-the-box parallel execution. By pairing Playwright for critical user journeys with Jest for fast unit and component tests, we achieve comprehensive test coverage with zero flaky tests.",
        "star": "Legacy Selenium test suite with 450 tests took 2 hours to run in CI/CD and failed 25% of the time due to timing and flaky wait conditions.",
        "action": "Migrated the entire test suite to Playwright, taking advantage of auto-waiting, parallel worker execution, and API request mocking for independent test cases.",
        "metrics": "CI test pipeline runtime reduced from 120 minutes to 11 minutes (91% faster); test flakiness dropped to 0%."
    },

    # 07. DevOps: Docker & Kubernetes
    {
        "dir": "10-testing-and-devops/devops-docker-kubernetes-cicd",
        "file": "01_docker_kubernetes_production_setup.md",
        "title": "Docker Containerization, Multi-Stage Builds & Kubernetes (K8s)",
        "hinglish": "Docker se application aur uske saare dependencies ko ek lightweight container me pack kiya jata hai ('Mere machine pe chal raha hai' wali problem khatam). Kubernetes un hazaron containers ko cluster me automatically scale, heal, aur load-balance karta hai.",
        "analogy": "Docker is standard shipping containers that fit any cargo ship. Kubernetes is the automated harbor crane system that organizes, stacks, and moves containers to available ships.",
        "points": [
            "Multi-Stage Dockerfile: Compiles code in build stage, copies only runtime artifacts to a minimal Alpine/Distroless image.",
            "Kubernetes Core Primitives: Pods, Deployments, Services (ClusterIP, NodePort, LoadBalancer), Ingress, ConfigMaps, Secrets.",
            "Horizontal Pod Autoscaler (HPA): Automatically scales pod replicas based on CPU/Memory utilization or custom metrics.",
            "Rolling Updates & Zero Downtime: K8s updates pods gradually, ensuring active traffic is only routed to healthy pods (Readiness/Liveness probes)."
        ],
        "diagram": """[Internet Traffic]
       │
       ▼
[K8s Ingress Controller] (SSL Termination / Routing)
       │
       ▼
[K8s Service (ClusterIP)] (Internal Load Balancer)
       │
       ├──> [Pod Replica 1] (Node / FastAPI Container)
       ├──> [Pod Replica 2] (Node / FastAPI Container)
       └──> [Pod Replica 3] (Node / FastAPI Container)""",
        "code": """# Multi-Stage Dockerfile for High Performance & Small Image Size
# Build Stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production Runtime Stage (Minimal footprint)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]""",
        "pitch": "Containerization with Docker guarantees environmental consistency across development, staging, and production. Kubernetes orchestrates these containers by providing self-healing, rolling deployments, horizontal pod autoscaling, and service discovery. Utilizing multi-stage Docker builds ensures minimal image size and reduced security attack surface.",
        "star": "Production node.js microservice image was 1.4GB in size, taking 8 minutes to pull during emergency auto-scaling events, leading to traffic drops during flash sales.",
        "action": "Rewrote Dockerfile using Alpine multi-stage builds, stripping devDependencies and build tools from the final image, and configured Kubernetes readiness probes with HPA.",
        "metrics": "Docker image size plummeted from 1.4GB to 85MB (94% reduction); pod scale-up startup time dropped from 8 minutes to 12 seconds."
    },

    # 08. Service MNC Interview Preparation (TCS / Infosys / Accenture / Capgemini)
    {
        "dir": "11-interview-master-cheatsheets/service-mnc-tier",
        "file": "01_top_mnc_interview_questions_tcs_accenture.md",
        "title": "Top MNC Technical Interview Questions & Pointers (TCS, Infosys, Accenture, Capgemini)",
        "hinglish": "Big service MNCs me interviews core fundamentals, clarity of speech, definitions, basic coding, and practical examples par focus karte hain. Yahan high-tech jargons se zyada crisp, accurate definitions matter karti hain.",
        "analogy": "A driving test: they want to see that you obey the fundamental traffic rules, use signals correctly, and operate smoothly without crashing.",
        "points": [
            "JavaScript: `var` vs `let` vs `const`, `==` vs `===`, Closures, Promises vs Callbacks, Hoisting, Arrow functions.",
            "React: Lifecycle methods vs Hooks, State vs Props, Virtual DOM, `useEffect` dependencies, Keys in lists.",
            "Backend & DB: SQL vs NoSQL, Primary Key vs Unique Key, REST API methods (GET, POST, PUT, DELETE, PATCH), HTTP status codes (200, 201, 400, 401, 403, 404, 500).",
            "OOPs Concepts: Polymorphism, Inheritance, Encapsulation, Abstraction with real-life car/bank examples."
        ],
        "diagram": """[MNC Interview Success Formula]
 1. Direct 1-Line Definition (Clear English)
 2. Everyday Real-World Example
 3. 2-3 Core Differences Point-Wise
 4. Short Code Snippet Demo""",
        "code": """// High Frequency MNC Question: Difference between == and ===
console.log(5 == "5");   // true  (Type coercion: converts string to number)
console.log(5 === "5");  // false (Strict equality: checks value AND type)

// High Frequency MNC Question: Closures in 3 lines
function counter() {
  let count = 0; // Private variable
  return () => ++count;
}
const inc = counter();
console.log(inc()); // 1
console.log(inc()); // 2""",
        "pitch": "In service MNC technical rounds, interviewers value rock-solid grasp of fundamentals and concise communication. Answering with clear definitions, stating the core difference point-wise, providing a simple real-life analogy, and mentioning a brief code example consistently yields high-pass ratings across TCS, Infosys, Accenture, and Capgemini.",
        "star": "Clearing client-facing technical assessment rounds for a Fortune 500 US retail client project under Accenture/TCS delivery.",
        "action": "Structured technical responses using the 'Definition -> Under the hood -> Practical example' method, demonstrating both architectural awareness and hands-on coding capability.",
        "metrics": "Secured 100% technical client interview clearance on first attempt across enterprise accounts."
    }
]

def generate_domain_files():
    for item in DOMAINS_DATA:
        target_dir = os.path.join(BASE_DIR, item["dir"])
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, item["file"])

        points_md = "\n".join([f"- {p}" for p in item["points"]])

        content = f"""# {item['title']}

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** {item['hinglish']}
>
> **Real-World Analogy:** {item['analogy']}

---

## 2. 📌 Core Mechanics & Key Points
{points_md}

---

## 3. 📊 Visual Architecture Diagram

```text
{item['diagram']}
```

---

## 4. 💻 Practical Implementation & Code Snippet

```javascript
{item['code']}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Explain {item['title']} and how you optimize it?"
>
> **You:** "{item['pitch']}"

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** {item['star']}
* **Task / Challenge:** Overcoming performance degradation, high memory consumption, or deployment bottlenecks in production.
* **Action Taken:** {item['action']}
* **Result & Business Impact:** {item['metrics']}

🗣️ **Script to Tell Interviewer:**
*"In our production environment, {item['star'].lower()} I led the optimization effort by {item['action'].lower()}, which resulted in {item['metrics'].lower()}."*
"""
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated domain guide: {target_file}")

    print("All domain guides generated successfully!")

if __name__ == "__main__":
    generate_domain_files()
