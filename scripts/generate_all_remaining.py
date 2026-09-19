import os

BASE_DIR = r"D:\Projects\knowledgebase"

REMAINING_FILES = [
    # 04-node
    {
        "path": "04-node/01_node_architecture_v8_libuv.md",
        "title": "Node.js Core Architecture: V8 Engine, Libuv & C++ Bindings",
        "hinglish": "Node.js koi programming language nahi hai balki ek JavaScript runtime environment hai. Iska architecture 3 main cheezon se bana hai: Google ka V8 Engine (JS code execute karta hai), Libuv (cross-platform asynchronous I/O handle karta hai), aur C++ Bindings (jo JS aur OS ke beech bridge ka kaam karte hain).",
        "analogy": "A restaurant: V8 is the chef cooking food quickly, Libuv is the team of waiters taking orders and handling deliveries in parallel, and C++ bindings are the kitchen tools connecting the chef to the stoves.",
        "points": [
            "V8 Engine: Compiles JS to machine code via Ignition (interpreter) and TurboFan (JIT compiler).",
            "Libuv: C library providing the event loop and a thread pool (default 4 threads) for blocking I/O (File system, DNS, Crypto).",
            "C++ Bindings: Native Node.js modules bridging JavaScript calls to underlying OS system calls.",
            "Single-Threaded Illusion: JavaScript execution is single-threaded, but underlying I/O is multi-threaded via Libuv and OS kernel epoll/kqueue."
        ],
        "diagram": """┌────────────────────────────────────────────────────────┐
│                   JavaScript Layer                     │
│               (Your Code / Node.js API)                │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    Node.js Bindings                    │
│                 (C++ Wrapper Layer)                    │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
┌─────────────▼─────────────┐ ┌───────────▼──────────────┐
│        Google V8          │ │          Libuv           │
│  (JS Execution Engine)    │ │ (Event Loop + ThreadPool)│
└───────────────────────────┘ └──────────────────────────┘""",
        "code": """// Inspecting Node.js Process Architecture & Threadpool
const crypto = require('crypto');

// Line 1: Measure execution time of CPU-bound cryptographic hash operations
const start = Date.now();

// Line 2: Trigger 4 concurrent PBKDF2 hashing tasks (matches default UV_THREADPOOL_SIZE = 4)
for (let i = 1; i <= 4; i++) {
  crypto.pbkdf2('secretPassword', 'salt', 100000, 512, 'sha512', () => {
    // Line 3: Log completion time for each thread in the Libuv pool
    console.log(`Thread ${i} finished in: ${Date.now() - start}ms`);
  });
}

// Line 4: Non-blocking synchronous code runs immediately on the main V8 stack
console.log('Main thread synchronous execution continues without waiting!');""",
        "pitch": "Node.js combines V8 for single-threaded JavaScript execution with Libuv for asynchronous cross-platform I/O. Non-blocking network I/O is managed via OS-level event notification mechanisms like epoll or kqueue, while heavy blocking tasks like file I/O and crypto are handled by Libuv's C thread pool. Adjusting UV_THREADPOOL_SIZE allows tuning for I/O vs CPU-intensive workloads.",
        "star": "Cryptographic password hashing and PDF generation endpoint blocking incoming HTTP requests and causing 10-second API timeouts.",
        "action": "Increased `UV_THREADPOOL_SIZE=8`, offloaded PDF rendering to Node Worker Threads, and verified non-blocking event loop ticks via Clinic.js Doctor.",
        "metrics": "API throughput increased by 400% (from 220 RPS to 1,100 RPS); P99 latency dropped from 9,800ms to 65ms."
    },

    # 05-fastapi
    {
        "path": "05-fastapi/01_asyncio_event_loop_and_concurrency.md",
        "title": "FastAPI & Python Asyncio: Event Loop, Coroutines & Concurrency Mechanics",
        "hinglish": "FastAPI modern Python ka sabse fast web framework hai kyunki ye Python `asyncio` event loop aur Starlette ASGI par chalta hai. Agar aap `async def` likhte ho toh code asyncio loop par chalta hai; agar aap regular `def` likhte ho toh FastAPI use automatically background threadpool me run karta hai taaki loop block na ho.",
        "analogy": "A fast food cashier: instead of waiting for burgers to cook before taking the next customer's order, the cashier gives you a token (`await`) and immediately serves the next person in line.",
        "points": [
            "Asyncio Event Loop: Single-threaded cooperative multitasking managing coroutines via `await` yield points.",
            "FastAPI Execution Rules: `async def` runs on the main asyncio event loop thread; regular `def` runs in an external `anyio` threadpool.",
            "Never Call Synchronous Blocking Code in `async def`: Calling `time.sleep()` in an `async def` route freezes the entire server instance.",
            "Pydantic V2 Core: Rust-compiled validation engine delivering 5x-20x faster JSON serialization."
        ],
        "diagram": """[Incoming ASGI Requests]
         │
         ├── async def route ────> [Main Asyncio Event Loop] (Non-blocking I/O)
         │
         └── regular def route ──> [Worker Threadpool Executor] (Offloaded threads)""",
        "code": """from fastapi import FastAPI, Depends
import asyncio
from pydantic import BaseModel, Field

app = FastAPI()

# Line 1: Define validated request body using Pydantic V2
class OrderCreate(BaseModel):
    item_id: str = Field(..., min_length=3)
    quantity: int = Field(..., gt=0)

# Line 2: Async route controller running directly on the Asyncio Event Loop
@app.post("/api/v1/orders")
async def create_order(order: OrderCreate):
    # Line 3: Simulate non-blocking async database query
    await asyncio.sleep(0.05)
    
    # Line 4: Return serialized dictionary response
    return {"status": "created", "order": order.model_dump()}""",
        "pitch": "FastAPI achieves enterprise performance by leveraging Starlette's ASGI foundation and Pydantic V2's Rust-based validation core. Its cooperative multitasking handles concurrent I/O using python's asyncio event loop. Understanding the distinction between `async def` and synchronous `def` routes is essential to prevent event loop thread exhaustion.",
        "star": "AI model inference microservice experiencing frozen request queues whenever long-running file downloads executed in `async def` handlers.",
        "action": "Replaced blocking `requests` calls with `httpx.AsyncClient` and moved CPU-intensive image tensor preprocessing to threadpool workers using `anyio.to_thread.run_sync`.",
        "metrics": "Concurrency handled surged from 50 concurrent requests to 3,500 concurrent requests; zero server timeout incidents."
    },

    # 06-ai-genai
    {
        "path": "06-ai-genai/01_rag_architecture_and_vector_databases.md",
        "title": "Enterprise RAG Architecture: Vector Databases, HNSW Indexing & Hybrid Search",
        "hinglish": "RAG (Retrieval-Augmented Generation) se hum LLM ko company ke private data se connect karte hain bina model ko dubara train kiye. Query aane par use Vector Embeddings me convert karte hain, Vector DB (HNSW Index) se top-k relevant chunks nikalte hain, aur prompt me attach karke LLM se grounded answer mangte hain.",
        "analogy": "An open-book exam: instead of memorizing an entire 1,000-page encyclopedia (fine-tuning), the student uses an index to quickly find the 2 exact pages needed (retrieval) and summarizes the answer (generation).",
        "points": [
            "Vector Embeddings: High-dimensional numerical representations of semantic meaning (e.g., 1536-dimensional vectors).",
            "HNSW (Hierarchical Navigable Small World): Skip-list graph indexing algorithm achieving logarithmic search time O(log N).",
            "Hybrid Search: Combining Dense Vector semantic search with Sparse Lexical BM25 keyword search using Reciprocal Rank Fusion (RRF).",
            "Cross-Encoder Re-Ranking: Re-scoring the top-20 retrieved candidates to extract the highest-quality top-5 context chunks."
        ],
        "diagram": """[User Query: "What is our refund policy?"]
         │
         ├── 1. Generate Query Embedding
         │        │
         │        ▼
         ├── 2. [Vector Database (HNSW Index)] ──> Top 20 Dense Chunks
         │        ▲
         ├── 3. [BM25 Keyword Index]            ──> Top 20 Keyword Chunks
         │        │
         ▼        ▼
    [Reciprocal Rank Fusion (RRF)] ──> [Cross-Encoder Re-ranker] ──> Top 5 Chunks
                                                                          │
                                                                          ▼
                                                       [LLM Prompt with Context]
                                                                          │
                                                                          ▼
                                                       [Grounded, Factual Answer]""",
        "code": """# Production Hybrid Search & RAG Retrieval Flow in Python
from typing import List

# Line 1: Reciprocal Rank Fusion (RRF) combining BM25 and Vector Search scores
def reciprocal_rank_fusion(dense_ranks: List[str], sparse_ranks: List[str], k: int = 60):
    rrf_scores = {}
    
    # Line 2: Accumulate RRF reciprocal rank scores for dense semantic vector results
    for rank, doc_id in enumerate(dense_ranks):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
        
    # Line 3: Accumulate RRF reciprocal rank scores for sparse BM25 keyword results
    for rank, doc_id in enumerate(sparse_ranks):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
        
    # Line 4: Sort documents descending by blended RRF relevance score
    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, score in sorted_docs]""",
        "pitch": "Enterprise RAG grounds LLM generation in verified external documents. To eliminate hallucinations and retrieval blind spots, we implement a Hybrid Search pipeline combining HNSW-indexed dense vectors with BM25 sparse keyword search via Reciprocal Rank Fusion, followed by a cross-encoder re-ranking pass before prompting the foundation model.",
        "star": "Internal enterprise HR and legal chatbot hallucinating policy rules and missing domain acronyms in naive vector search.",
        "action": "Engineered a hybrid retrieval pipeline pairing Chroma/Milvus dense vectors with BM25 keyword search, followed by Cohere Rerank model filtering.",
        "metrics": "Retrieval recall jumped from 61% to 94%; hallucination error rate dropped from 18% down to 0.4%."
    },

    # 07-system-design
    {
        "path": "07-system-design/02_hld_whatsapp_realtime_chat.md",
        "title": "System Design: WhatsApp / Slack Real-Time Chat Architecture",
        "hinglish": "Ek real-time chat application me persistent connections zaroori hote hain. Iske liye WebSockets use karte hain, jo TCP connection open rakhte hain. User ka status track karne ke liye Redis Presence Service, messages buffer karne ke liye Kafka, aur message history store karne ke liye Cassandra use karte hain.",
        "analogy": "A private telephone line kept off the hook: instead of sending letters back and forth every time someone talks (HTTP polling), the audio line is permanently open for instant two-way conversation (WebSockets).",
        "points": [
            "Protocol: WebSockets over TCP for full-duplex bi-directional communication.",
            "Connection Gateway: Stateful Gateway servers maintaining open WebSocket connections to millions of connected devices.",
            "User Presence & Routing: Redis cluster tracking `userId -> gateway_server_ip` mappings.",
            "Storage Architecture: Apache Cassandra for message history (optimized for sequential write throughput) and S3 for media attachments."
        ],
        "diagram": """[User A (Mobile)] ──(WebSocket)──> [Chat Gateway 1]
                                          │
                                          ├──> [Kafka Message Queue]
                                          │          │
                                          │          ├──> [Cassandra DB] (Store message)
                                          │          │
                                          │          ▼
[User B (Mobile)] <──(WebSocket)── [Chat Gateway 2] <── [Message Consumer Service]""",
        "code": """// WebSocket Chat Server Gateway in Node.js
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 8080 });
// Line 1: In-memory map of active connected users: userId -> WebSocket
const activeConnections = new Map();

wss.on('connection', (ws, req) => {
  // Line 2: Extract authenticated userId from request URL
  const userId = req.url.split('?userId=')[1];
  activeConnections.set(userId, ws);

  ws.on('message', async (messageData) => {
    // Line 3: Parse incoming chat payload
    const { recipientId, text } = JSON.parse(messageData);

    // Line 4: Check if recipient is connected to this gateway server
    const recipientSocket = activeConnections.get(recipientId);
    if (recipientSocket && recipientSocket.readyState === ws.OPEN) {
      // Line 5: Forward message immediately over open WebSocket connection
      recipientSocket.send(JSON.stringify({ from: userId, text, timestamp: Date.now() }));
    } else {
      // Line 6: Offload message to Kafka/Push Notification worker for offline user
      console.log(`User ${recipientId} is offline. Enqueuing Push Notification.`);
    }
  });

  ws.on('close', () => {
    // Line 7: Clean up socket connection on client disconnect
    activeConnections.delete(userId);
  });
});""",
        "pitch": "Designing a real-time messaging platform like WhatsApp requires maintaining millions of persistent WebSocket connections. The system decouples stateful connection gateways from stateless business logic using Apache Kafka. A distributed Redis Presence store maps users to their active gateway nodes, while Apache Cassandra provides high-throughput append-only message history storage.",
        "star": "Real-time collaborative document commenting system dropping messages during sudden traffic spikes of 50,000 concurrent active users.",
        "action": "Replaced short-polling HTTP endpoints with clustered WebSocket gateways managed by Redis Pub/Sub and backed by Kafka message buffering.",
        "metrics": "Message delivery latency dropped from 2,400ms to 28ms; server bandwidth consumption dropped by 72%."
    },

    # 11-interview-master-cheatsheets: Infosys
    {
        "path": "11-interview-master-cheatsheets/service-mnc-tier/infosys_interview_guide.md",
        "title": "Infosys Technical Interview Guide: High-Frequency Questions & Simple Pointers",
        "hinglish": "Infosys ke technical rounds me core programming logic, OOPs concepts, Java/JavaScript fundamentals, database normalization, aur clean coding practices sabse zaroori hoti hain.",
        "analogy": "A structured fitness assessment: checking strength in all fundamental muscles (syntax, logic, DB, OOPs) to verify you can handle enterprise client projects.",
        "points": [
            "Difference between Interface and Abstract Class.",
            "Database Normalization (1NF, 2NF, 3NF) with real-life examples.",
            "Difference between Method Overloading (Compile-time) and Method Overriding (Runtime).",
            "String immutability in Java/JavaScript and memory benefits.",
            "REST API idempotent methods (GET, PUT, DELETE) vs non-idempotent (POST)."
        ],
        "diagram": """[Infosys Technical Evaluation Criteria]
 ├── 1. Conceptual Clarity (40%) -> Clear definitions without hesitation
 ├── 2. Code Writing & Logic (30%) -> Whiteboard string/array problem
 ├── 3. Database & SQL Queries (20%) -> Joins and Aggregations
 └── 4. Communication & Professionalism (10%)""",
        "code": """// High Frequency Infosys Question: Check for Anagrams using Frequency Array
function isAnagram(s, t) {
  // Line 1: Length check
  if (s.length !== t.length) return false;
  
  // Line 2: Frequency counter array
  const count = new Array(26).fill(0);
  
  for (let i = 0; i < s.length; i++) {
    count[s.charCodeAt(i) - 97]++;
    count[t.charCodeAt(i) - 97]--;
  }
  
  // Line 3: Ensure all counts are 0
  return count.every(c => c === 0);
}

console.log(isAnagram("listen", "silent")); // true
console.log(isAnagram("hello", "world"));   // false""",
        "pitch": "For Infosys interviews, maintain structured explanations. Always follow the pattern: 1) One sentence crisp definition, 2) Key difference point-wise, 3) Real-world example, and 4) Clean code with boundary edge cases.",
        "star": "Clearing client-facing interview rounds for high-value US enterprise banking clients through Infosys delivery.",
        "action": "Prepared point-wise explanations of OOPs and database normalization, demonstrating clean coding principles.",
        "metrics": "Selected for premium technical lead role with top client evaluation feedback."
    }
]

def generate_remaining():
    count = 0
    for item in REMAINING_FILES:
        target_path = os.path.join(BASE_DIR, item["path"])
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
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

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
{item['code']}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain {item['title'].split(':')[0]} and your production experience with it?"
>
> **You:** "{item['pitch']}"

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** {item['star']}
* **Task / Challenge:** Resolving critical production bottlenecks, scaling limits, or security vulnerabilities under active business pressure.
* **Action Taken:** {item['action']}
* **Result & Business Impact:** {item['metrics']}

🗣️ **Script to Tell Interviewer:**
*"In one of my core projects, {item['star'].lower()} I spearheaded the solution by {item['action'].lower()}, successfully achieving {item['metrics'].lower()}."*
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"[{count}] Generated: {target_path}")

    print(f"Generated {count} remaining domain files!")

if __name__ == "__main__":
    generate_remaining()
