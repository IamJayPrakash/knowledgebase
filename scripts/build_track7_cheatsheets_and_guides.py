# -*- coding: utf-8 -*-
"""
Generator for Track 7: DSA Meta-Heuristics, Quick Recall Cheatsheets, Behavioral Guides, and MNC Company Guides
Generates:
1. 08-leetcode-dsa/interview-questions/dsa_patterns_cheat_sheet_and_meta_heuristics.md
2. 09-interview-cheatsheet/01_fullstack_quick_recall_cheatsheet.md
3. 09-interview-cheatsheet/02_system_design_cheat_sheet.md
4. 09-interview-cheatsheet/interview-questions/behavioral_star_method_master_guide.md
5. 11-interview-master-cheatsheets/service-mnc-tier/wipro_interview_guide.md
6. 11-interview-master-cheatsheets/service-mnc-tier/cognizant_interview_guide.md
7. 11-interview-master-cheatsheets/service-mnc-tier/capgemini_interview_guide.md
8. 11-interview-master-cheatsheets/mid-tier-and-startups/nagarro_interview_guide.md
9. 11-interview-master-cheatsheets/mid-tier-and-startups/startup_tech_lead_interview_guide.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "08-leetcode-dsa", "interview-questions", "dsa_patterns_cheat_sheet_and_meta_heuristics.md"): """# DSA Meta-Heuristics and Pattern Recognition Cheat Sheet

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
DSA problem dekh kar ghabrana ek un-labeled medicine box dekhne jaisa hai.
Lekin agar aapke paas **Doctor ka Symptom Checker (Meta-Heuristics)** ho, toh aap problem ki shakal (Constraints & Keywords) dekh kar 5 second mein pehchan loge:
- "Sorted array hai aur search karna hai?" ➔ **Binary Search ($O(\\log N)$)**!
- "Subarray sum / longest substring poocha hai?" ➔ **Sliding Window**!
- "Top K / Most frequent elements?" ➔ **Min-Heap / Max-Heap**!
- "All combinations / permutations?" ➔ **Backtracking**!
- "Shortest path in unweighted graph?" ➔ **BFS (Queue)**!

---

## 📌 2. Master Pattern Recognition Matrix

| If the problem mentions... | Candidate Data Structure / Algorithm | Time Complexity Target |
| :--- | :--- | :--- |
| **Sorted Array & Finding Target/Boundary** | Binary Search (Two Pointers) | $O(\\log N)$ |
| **Contiguous Subarray / Substring with condition** | Sliding Window (Two Pointers + Hash Map) | $O(N)$ |
| **Top K, Smallest K, Median in Stream** | Heap / Priority Queue | $O(N \\log K)$ |
| **Finding cycles, connected components** | Union-Find (Disjoint Set) or DFS | $O(N \\cdot \\alpha(N))$ |
| **Shortest path (Unweighted)** | Breadth-First Search (BFS with Queue) | $O(V + E)$ |
| **Shortest path (Weighted, positive edges)** | Dijkstra's Algorithm (Min-Heap) | $O((V + E) \\log V)$ |
| **Overlapping subproblems & Optimal substructure** | Dynamic Programming (1D/2D Memoization) | $O(N)$ to $O(N^2)$ |
| **Generate all combinations / subsets** | Backtracking (DFS Recursion tree) | $O(2^N)$ or $O(N!)$ |
| **Next Greater / Smaller Element** | Monotonic Stack | $O(N)$ |
| **Prefix / Word dictionary lookups** | Trie (Prefix Tree) | $O(L)$ where $L$ = word length |

---

## 💻 3. Meta-Heuristic Template: Sliding Window Skeleton

```python
# Universal Sliding Window Pattern Template
def sliding_window_template(arr, condition):
    # Line 3: Window state trackers
    left = 0
    window_state = {}
    optimal_result = 0

    # Line 8: Right pointer expands window
    for right in range(len(arr)):
        # Add incoming element to window state
        current_elem = arr[right]
        window_state[current_elem] = window_state.get(current_elem, 0) + 1

        # Line 14: Contract window from left while condition is violated
        while not condition(window_state):
            left_elem = arr[left]
            window_state[left_elem] -= 1
            if window_state[left_elem] == 0:
                del window_state[left_elem]
            left += 1 # Shrink window

        # Line 22: Update optimal result with valid window
        current_window_len = right - left + 1
        optimal_result = max(optimal_result, current_window_len)

    return optimal_result
```
""",

    os.path.join(BASE_DIR, "09-interview-cheatsheet", "01_fullstack_quick_recall_cheatsheet.md"): """# Fullstack Senior Engineer Quick Recall Cheat Sheet (5-Minute Review)

---

## 🚀 1. JavaScript & Web Core
- **Event Loop Order**: Call Stack ➔ Microtasks (`Promise.then`, `queueMicrotask`, `process.nextTick`) ➔ Browser Render/Paint ➔ Macrotasks (`setTimeout`, `setInterval`, `setImmediate`, I/O).
- **Prototypal Inheritance**: `obj.__proto__ === Constructor.prototype`. `Object.prototype.__proto__ === null`.
- **`this` Binding Priority**: `new` binding ➔ Explicit (`bind`/`apply`/`call`) ➔ Implicit (Object method dot) ➔ Default (Global or `undefined` in strict). Arrow functions capture `this` lexically at creation time.
- **Core Web Vitals Targets**:
  - **LCP** (Largest Contentful Paint): $\\le 2.5s$.
  - **INP** (Interaction to Next Paint): $\\le 200ms$.
  - **CLS** (Cumulative Layout Shift): $\\le 0.1$.

---

## ⚛️ 2. React & Next.js
- **Reconciliation Diffing**: Types differ ➔ Tear down subtree. Same types ➔ Update changed props. Keys provide stable identity across sibling renders.
- **`useEffect` vs `useLayoutEffect`**: `useEffect` runs async after browser paint. `useLayoutEffect` runs synchronously before paint (for layout measurements & anti-flicker).
- **Next.js App Router**: Server Components by default (0 client bundle). Server Actions (`"use server"`) provide RPC mutations with `revalidatePath()` and `revalidateTag()`.

---

## 🅰️ 3. Modern Angular 21
- **Signals**: `signal()`, `computed()`, `effect()`. Fine-grained synchronous reactivity without Zone.js.
- **Zoneless Architecture**: Angular 21 is zoneless by default. Change detection is triggered via signal notifications and `ChangeDetectorRef`.
- **`@defer` Block**: Template-level lazy loading (`@defer (on viewport) { <HeavyComp /> } @placeholder { <Skeleton /> }`).

---

## 🐍 4. Python FastAPI & Node.js
- **Node.js**: Libuv event loop. 4-thread pool for `fs`, `crypto`, `zlib`, `dns`. Never use synchronous I/O or block event loop.
- **FastAPI**: Pydantic V2 (Rust core). `async def` runs on asyncio event loop (use only async non-blocking calls); regular `def` runs in a background threadpool.
""",

    os.path.join(BASE_DIR, "09-interview-cheatsheet", "02_system_design_cheat_sheet.md"): """# System Design Master Cheat Sheet (Formulas, Trade-offs & Numbers)

---

## 📊 1. Back-of-the-Envelope Math & Numbers Everyone Should Know
- $1 \\text{ Million Requests/day} \\approx 12 \\text{ Requests/second (QPS)}$.
- $100 \\text{ Million Requests/day} \\approx 1,200 \\text{ QPS}$.
- $1 \\text{ Billion Requests/day} \\approx 12,000 \\text{ QPS}$.
- **Latency Numbers**:
  - L1 Cache reference: $0.5 \\text{ ns}$.
  - Main Memory (RAM) reference: $100 \\text{ ns}$.
  - Read $1 \\text{ MB}$ sequentially from RAM: $250 \\text{ µs}$.
  - Read $1 \\text{ MB}$ sequentially from SSD: $1 \\text{ ms}$.
  - Send packet California to Netherlands & back: $150 \\text{ ms}$.

---

## ⚖️ 2. Architectural Trade-offs
- **CAP Theorem**: In the presence of a Network Partition ($P$), choose between Consistency ($C$) or Availability ($A$).
- **PACELC Theorem**: If Partition ($P$), choose $A$ vs $C$; Else ($E$), choose Latency ($L$) vs Consistency ($C$).
- **Cache Invalidation Patterns**:
  - **Cache-Aside**: App reads cache; if miss, reads DB, writes to cache. (Most flexible).
  - **Write-Through**: App writes to cache; cache writes to DB synchronously. (Consistent, higher write latency).
  - **Write-Behind (Write-Back)**: App writes to cache; cache asynchronously writes to DB in batch. (Fast writes, risk of data loss on crash).
""",

    os.path.join(BASE_DIR, "09-interview-cheatsheet", "interview-questions", "behavioral_star_method_master_guide.md"): """# Behavioral Interview Mastery: The STAR Method for Senior Engineers

---

## 🌟 1. The STAR Framework Structure
- **S - Situation**: Set the business context, system scale, and high stakes in 2-3 sentences.
- **T - Task**: What was your specific, personal responsibility? (Avoid saying "We did", say "My direct objective was...").
- **A - Action**: Deep technical steps, architectural tradeoffs considered, and how you led team alignment.
- **R - Result**: Quantifiable business and technical outcomes (e.g. "Reduced latency by 45%", "Saved $30,000/month", "0 outages").

---

## 💼 2. Top Senior Behavioral Questions & Tailored STAR Answers

### Question 1: "Tell me about a time you handled a severe production outage under high pressure."
- **Situation**: During a Black Friday flash sale with 120,000 concurrent active users, our primary payment processing service latency spiked to 15 seconds, and checkout failure rate hit 42%.
- **Task**: As the on-call Technical Lead, my task was to isolate the failure, restore payment processing within 15 minutes, and protect our database from cascading crash.
- **Action**: I opened an incident war room. I analyzed Datadog APM traces and noticed connection pool exhaustion in PostgreSQL caused by a third-party fraud-check webhook hanging for 10 seconds. I immediately engaged a feature flag to bypass synchronous fraud checks for low-value carts (< $50) and activated a Resilience4j circuit breaker with a 1.5s timeout.
- **Result**: Checkout success rate recovered to 99.8% within 8 minutes. We saved an estimated $420,000 in at-risk revenue, and later re-architected the fraud check to an asynchronous Kafka event consumer.

---

### Question 2: "Tell me about a technical disagreement you had with another senior engineer and how you resolved it."
- **Situation**: When architecting our real-time messaging pipeline, the lead architect advocated for polling an existing PostgreSQL database every 2 seconds, while I proposed adopting WebSockets backed by Redis Pub/Sub.
- **Task**: Align the architecture on a scalable solution without alienating team members or delaying the sprint milestone.
- **Action**: Instead of debating opinion, I built a fast benchmark test running both approaches with 10,000 simulated client connections. The benchmark proved that DB polling saturated CPU at 98% and caused 3.8s message delivery latency, while Redis WebSockets used 8% CPU and delivered sub-30ms latency. I presented the empirical telemetry objectively and praised my colleague's concern regarding Redis operational maintenance, proposing a fully managed AWS ElastiCache cluster to mitigate maintenance worries.
- **Result**: The team enthusiastically adopted the Redis WebSocket architecture, delivering the feature 1 week ahead of schedule with zero operational incidents.
""",

    os.path.join(BASE_DIR, "11-interview-master-cheatsheets", "service-mnc-tier", "wipro_interview_guide.md"): """# Wipro Senior Fullstack Engineer Interview Guide

---

## 🏢 1. Hiring Process & Focus Areas
- **Round 1: Online Technical Assessment**: Core Java/JavaScript, OOP, SQL, and 2 medium DSA coding questions.
- **Round 2: Technical Deep Dive (L1)**: Hands-on coding, Spring Boot / Node.js architecture, React/Angular lifecycle, and microservices patterns.
- **Round 3: Techno-Managerial (L2)**: Client-facing communication, production project challenges, cloud migration, and team mentoring.

---

## 🎯 2. High-Frequency Wipro Technical Questions
1. **Explain Spring Boot Auto-Configuration (`@EnableAutoConfiguration`)**: How Spring inspects classpath JARs and registers beans conditionally using `@ConditionalOnClass` and `@ConditionalOnMissingBean`.
2. **Difference between `fork()` and `spawn()` in Node.js child processes**.
3. **How does Angular's Change Detection differ between Default and OnPush?** (And modern Angular Signals).
4. **SQL Query: Find the 3rd Highest Salary in an Employee table** (`DENSE_RANK() OVER (ORDER BY salary DESC)`).
""",

    os.path.join(BASE_DIR, "11-interview-master-cheatsheets", "service-mnc-tier", "cognizant_interview_guide.md"): """# Cognizant (CTS) Senior Developer / Architect Interview Guide

---

## 🏢 1. Hiring Process & Focus Areas
- **Focus**: Microservices architectures, REST design, database performance tuning, CI/CD, and client stakeholder management.

---

## 🎯 2. High-Frequency Cognizant Technical Questions
1. **How do you handle Distributed Transactions across Microservices?** (Saga Pattern: Choreography vs Orchestration; 2-Phase Commit drawbacks).
2. **Explain React Fiber Reconciler and double buffering**.
3. **What is an Index Seek vs Index Scan in SQL?**
4. **How do you secure REST APIs using OAuth 2.0 / OpenID Connect?**
""",

    os.path.join(BASE_DIR, "11-interview-master-cheatsheets", "service-mnc-tier", "capgemini_interview_guide.md"): """# Capgemini Senior Technical Consultant Interview Guide

---

## 🏢 1. Hiring Process & Focus Areas
- **Focus**: Enterprise Java / Spring Boot or MERN stack, Cloud fundamentals (AWS/Azure), Docker/Kubernetes containerization, and Design Patterns.

---

## 🎯 2. High-Frequency Capgemini Technical Questions
1. **Explain the SOLID Principles with real-world enterprise code examples**.
2. **How does the JVM Garbage Collector (G1 GC vs ZGC) manage heap memory?**
3. **How do you implement Idempotency in REST APIs?** (`Idempotency-Key` header with Redis deduplication).
4. **Explain Event-Driven Architecture with Apache Kafka (Partitioning, Consumer Groups, Offsets)**.
""",

    os.path.join(BASE_DIR, "11-interview-master-cheatsheets", "mid-tier-and-startups", "nagarro_interview_guide.md"): """# Nagarro Senior Technology Specialist Interview Guide

---

## 🏢 1. Hiring Process & Focus Areas
- Nagarro has rigorous coding and algorithmic rounds with deep emphasis on design patterns, clean code principles, and real-time problem solving.

---

## 🎯 2. High-Frequency Nagarro Technical Questions
1. **Implement custom LRU Cache from scratch using Doubly Linked List and Hash Map**.
2. **Deep dive into JavaScript Event Loop, Microtasks, and Promise execution order**.
3. **Design a Thread-Safe Singleton in Java / Python / C#**.
4. **Explain Monorepo Architecture vs Polyrepo for enterprise micro-frontends**.
""",

    os.path.join(BASE_DIR, "11-interview-master-cheatsheets", "mid-tier-and-startups", "startup_tech_lead_interview_guide.md"): """# Startup Tech Lead / Staff SDE Interview Guide (Series A to Unicorn)

---

## 🚀 1. What Startups Look For
In high-growth startups (Series A-C), interviewers do not ask trivia. They evaluate:
1. **Speed vs Quality Tradeoffs**: When to build a quick monolithic MVP vs when to decouple into microservices.
2. **Cost & Cloud Economics**: Designing architectures that minimize AWS/GCP bills (e.g. S3 intelligent tiering, spot instances).
3. **Ownership & Zero-to-One Delivery**: Ability to debug obscure production crashes across the entire stack without documentation.
4. **Pragmatic Technology Choices**: Picking boring, reliable technology (PostgreSQL, Redis, Next.js) over unproven hype.

---

## 🎯 2. Archetypal Startup Architectural Scenarios
- **Scenario 1**: "Our AWS bill jumped by $15,000 this month due to RDS egress and DynamoDB read capacity. How do you audit and reduce costs in 48 hours?"
- **Scenario 2**: "We need to ingest 50,000 IoT events per second with an engineering team of 4 people. Design a low-maintenance pipeline." (Solution: Managed Cloud PubSub/Kinesis ➔ ClickHouse / Snowflake ➔ Grafana).
"""
}

def main():
    print(f"Generating {len(FILES)} Track 7 Cheatsheets & Guides...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Track 7 Cheatsheets & Guides generation complete!")

if __name__ == "__main__":
    main()
