# AI & GenAI Interview Questions: Part 6 — Scenario-Based AI System Design (Q101 - Q110)

---

### Q101: System Design — Design an Enterprise Multi-Tenant RAG Search Platform for 1,000 Corporate Clients.
- **Problem Statement**: Build a secure, SOC2-compliant RAG system indexing millions of internal enterprise documents with strict tenant isolation, sub-100ms search latency, and role-based access control (RBAC).
- **Architecture Breakdown**:
  ```
  [ User Search API ] ──> [ Auth & Tenant Router (JWT/RBAC) ] ──> [ Semantic Query Cache ]
                                      │ (Cache Miss)
                                      ▼
                        [ Query Expansion & HyDE ]
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
     [ BM25 Lexical Engine ]                           [ Qdrant Vector Cluster ]
     (Tenant Index Partition)                         (HNSW + Payload Pre-filter)
            │                                                   │
            └─────────────────────────┬─────────────────────────┘
                                      ▼
                       [ Reciprocal Rank Fusion (RRF) ]
                                      │
                                      ▼
                     [ Cross-Encoder Re-ranker (Top 25) ]
                                      │
                                      ▼
               [ Generation LLM with Citation Verification ]
  ```
- **Key Design Choices**:
  1. **Tenant Isolation**: Leverage Qdrant with integrated payload indexing (`tenant_id` and `user_group_ids` evaluated during HNSW graph traversal).
  2. **Two-Stage Retrieval**: BM25 (Elasticsearch) + Dense Vector search merged via RRF ($k=60$), re-ranked with a local `bge-reranker-large` model on an Nvidia L4 GPU.
  3. **Ingestion Pipeline**: Asynchronous Kafka queue feeding layout-aware document chunkers with small-to-big (parent-document) storage in Redis.

---

### Q102: System Design — Design an Autonomous Customer Support Multi-Agent System with Human-in-the-Loop.
- **Problem Statement**: Automate tier-1 e-commerce customer support (order lookups, address updates, refunds) with self-healing tools, strict fraud controls, and human manager escalation for high-value refunds.
- **Architecture Breakdown**:
  ```mermaid
  stateDiagram-v2
      [*] --> Supervisor
      Supervisor --> OrdersAgent: Inquire / Track Order
      Supervisor --> RefundAgent: Request Refund
      Supervisor --> GeneralFAQ: Store Policies
      
      RefundAgent --> CheckValue: Evaluate Refund Amount
      state CheckValue <<choice>>
      CheckValue --> AutoApprove: Amount <= $50
      CheckValue --> HumanEscalation: Amount > $50 (Pause Graph)
      
      HumanEscalation --> AdminDashboard: interrupt_before webhook
      AdminDashboard --> RefundAgent: Human Approved / Rejected
      
      AutoApprove --> Supervisor: Refund Processed
      OrdersAgent --> Supervisor: Order Details Fetched
      GeneralFAQ --> Supervisor: Policy Answered
      Supervisor --> [*]: Final Response to Customer
  ```
- **Key Design Choices**:
  1. **Framework**: LangGraph StateGraph with `PostgresSaver` for conversation checkpointing.
  2. **Human-in-the-Loop**: Use `interrupt_before=["execute_stripe_refund_node"]` whenever refund exceeds \$50. Graph state freezes and alerts human support via Slack/Retool dashboard.
  3. **Self-Healing Loop**: If the database lookup tool throws a database error, route back to `RefundAgent` with the error trace to self-correct parameters (max 3 retries).

---

### Q103: System Design — Design a Low-Latency Real-Time Code Completion Copilot.
- **Problem Statement**: Provide inline code completions inside IDEs (VS Code / JetBrains) with strict sub-150ms Time-To-First-Token (TTFT) and high multi-token throughput.
- **Architecture Breakdown**:
  - **IDE Plugin**: Debounces typing events (50ms), extracts surrounding file context using Tree-sitter AST parsing (current function signature, imports, preceding 20 lines, cursor position).
  - **Inference Fleet**: Hosted on Kubernetes using **vLLM with Speculative Decoding**.
    - **Draft Model**: 1B parameter code model generating 5 candidate tokens in 12ms.
    - **Target Model**: 14B parameter model verifying candidates in a single forward pass.
  - **Optimizations**: Prefix Caching on project import headers, AWQ 4-bit quantization, and HTTP/2 Server-Sent Events (SSE) streaming.

---

### Q104: System Design — Design an Automated Financial Document Processing Engine for Complex Multi-Column PDFs.
- **Problem Statement**: Extract structured balance sheets, P&L tables, and executive summaries from 100-page quarterly financial reports with 99.9% numerical accuracy.
- **Architecture Breakdown**:
  1. **Vision-Language Ingestion (ColPali)**: Index raw page screenshots directly into multi-vector patch embeddings to preserve table layout and footnotes.
  2. **Table Extraction**: Route tabular pages through layout-aware parsers to extract raw Markdown/HTML tables.
  3. **Pydantic Schema Validation**: Parse financial entities into strongly-typed Pydantic classes with mathematical cross-validation validators (e.g. `assert assets == liabilities + equity`).
  4. **Self-Correction**: If mathematical validation fails, feed the validation error and raw table back to the LLM to reconcile line items.

---

### Q105: System Design — Design a High-Volume AI Security Guardrail Gateway Processing 10,000 Requests/Sec.
- **Problem Statement**: Provide an enterprise ingress/egress proxy that redacts PII, blocks prompt injections, and prevents secret leaks with an added latency overhead of less than 25ms.
- **Architecture Breakdown**:
  - **Layer 1: Fast Regex & Heuristic Bloom Filters (< 2ms)**:
    - Scans for common jailbreak signatures (`"ignore previous instructions"`).
    - Regex PII masking for credit card and social security numbers.
  - **Layer 2: Lightweight Classifier Model (Llama Guard on TensorRT-LLM, < 15ms)**:
    - Highly parallelized binary classification scoring injection probability and content safety.
  - **Layer 3: Egress Token Sanitizer (< 3ms)**:
    - Scans outgoing model streams using Aho-Corasick string matching against enterprise API keys, internal IP ranges, and proprietary secret tokens.

---

### Q106: System Design — Design a Self-Healing Text-to-SQL Analytics Agent.
- **Problem Statement**: Enable business analysts to query a 200-table data warehouse in plain English with 0% risk of data modification and automated correction of syntax errors.
- **Architecture Breakdown**:
  1. **Schema Pruning**: Use vector similarity to retrieve only the top-8 most relevant table schemas and column descriptions based on the user's natural language question.
  2. **ReadOnly Connection**: Bind execution strictly to a read-only database user account (`GRANT SELECT ON ...`).
  3. **LangGraph Cyclic Verification**:
     - `Node 1 (Generate SQL)` $\to$ `Node 2 (Dry Run EXPLAIN ANALYZE)` $\to$ `Node 3 (Result Check)`.
     - If Postgres returns an error (missing join or column mismatch), the error string is fed back to Node 1 for dynamic query regeneration (capped at 3 cycles).

---

### Q107: System Design — Design an Automated Continuous Evaluation & Benchmarking CI/CD Pipeline for LLMs.
- **Problem Statement**: Eliminate subjective "vibe checks" and automatically block pull requests that degrade RAG accuracy or increase hallucinations.
- **Architecture Breakdown**:
  - **Golden Test Dataset**: 500 hand-curated and synthetic (Query, Ground-Truth Context, Ground-Truth Answer) triplets stored in Git LFS.
  - **Evaluation Runner (GitHub Actions)**:
    - Pull request triggers parallel evaluation using **Ragas**.
    - Calculates the RAG Triad: Context Precision, Faithfulness (Groundedness), and Answer Relevance.
  - **Quality Gates**: PR fails automatically if Faithfulness drops below 0.94 or Context Recall drops below 0.90. Metrics and regression diffs are posted as automated PR comments.

---

### Q108: System Design — Design a Real-Time Audio Meeting Summarizer & Action-Item Tracker.
- **Problem Statement**: Ingest live multi-speaker audio streams, transcribe speaker-diarized text in real time, and generate rolling meeting summaries and extracted task assignments.
- **Architecture Breakdown**:
  1. **Audio Ingestion**: WebSocket stream chunked into 3-second PCM audio buffers.
  2. **Transcription & Diarization**: Whisper + PyAnnote running on GPU workers emitting `[Speaker A]: ...` text events.
  3. **Rolling Context Buffer**: LangChain `ConversationSummaryBufferMemory` that maintains a compact running executive summary while tracking raw turns from the last 2 minutes.
  4. **Action Item Extractor**: Secondary background worker running every 60 seconds with Pydantic structured output: `List[ActionItem(assignee, task, deadline)]`.

---

### Q109: System Design — Design a GraphRAG Enterprise Knowledge Discovery Platform.
- **Problem Statement**: Enable global thematic exploration over 50,000 unstructured customer research reports where standard vector RAG fails to provide high-level conceptual answers.
- **Architecture Breakdown**:
  1. **Entity-Relationship Extraction**: Batched LLM pipeline parses documents into Graph Nodes (Entities), Edges (Relationships), and Claims.
  2. **Graph Clustering (Leiden Algorithm)**: Groups entities into hierarchical communities at multiple granularity levels.
  3. **Community Summarization**: Auxiliary models generate rich thematic summary reports for each cluster ahead of time.
  4. **Global Query Traversal**: High-level prompts (*"What are the top 3 product adoption blockers across all regions?"*) query the community summaries in parallel, synthesizing a global perspective.

---

### Q110: System Design — Design a Cost & Latency Optimization Architecture for a 10M DAU GenAI Application.
- **Problem Statement**: Cut monthly frontier model API costs from \$1,200,000 to under \$300,000 while reducing P95 user latency by 60%.
- **Architecture Breakdown**:
  ```
  [ Incoming User Query ]
             │
             ▼
  [ Semantic Cache (GPTCache / Redis) ] ──> (Cosine Sim > 0.96) ──> [ Return Cached Response (8ms) ]
             │ (Cache Miss)
             ▼
  [ Model Complexity Router (Fast Classifier) ]
        /                               \
  (Simple / Factual: 70% of traffic)    (Complex Reasoning: 30% of traffic)
      /                                           \
     ▼                                             ▼
  [ Local Self-Hosted vLLM ]                  [ Frontier Cloud Model ]
  (Quantized Llama 3 8B AWQ)                  (Claude 3.5 Sonnet / GPT-4o)
  - Prefix Caching enabled                     - Prompt caching enabled
  - Continuous batching                        - Strict token output limits
  ```
- **Cost Reduction Drivers**:
  1. **Semantic Caching**: Handles 28% of repetitive user queries at \$0 cost.
  2. **Intelligent Model Routing**: Routes 70% of straightforward queries to a local, 4-bit quantized Llama 3 8B model hosted on spot GPU instances (costing \$0.0002 per 1K tokens vs \$0.015).
  3. **Prefix Caching**: Cuts input token costs by 50% on long shared system prompts.
