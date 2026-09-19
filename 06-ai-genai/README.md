# 🤖 AI & GenAI Systems Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index from **LLM Foundations & Vector DBs to Advanced RAG & Agentic Workflows** for Senior AI Engineer & System Architect interviews.

---

## 📌 How to Use This Section
- Use this `README.md` as your master index and curriculum roadmap for AI & GenAI.
- Create single concept files inside `06-ai-genai/` (e.g., `01_rag_architecture_and_chunking.md`) as you learn and add your notes, code snippets, and interview pointers.

---

## 🗺️ Learning Roadmap & Concept Index

### 1. LLM Foundations & Transformers
- [ ] `01_transformer_architecture_and_attention.md` — Transformer Decoder-only architecture, Self-Attention mechanism ($\text{Softmax}(\frac{QK^T}{\sqrt{d_k}})V$), Multi-Head Attention, Positional Encodings (RoPE).
- [ ] `02_tokenization_and_inference_parameters.md` — Byte-Pair Encoding (BPE), Tokenizer limits, Temperature, Top-P (Nucleus Sampling), Top-K, Repetition Penalty.

### 2. Vector Embeddings & Vector Databases
- [ ] `03_embeddings_and_distance_metrics.md` — Dense Vector Embeddings, Cosine Similarity vs Dot Product vs Euclidean ($L_2$) Distance, Embedding Model Selection (OpenAI, BGE, Nomic).
- [ ] `04_vector_database_indexing_hnsw.md` — HNSW (Hierarchical Navigable Small World) graphs, IVF-PQ (Inverted File with Product Quantization), Trade-offs between Recall, Latency, and Memory across Pinecone, Milvus, Chroma, Qdrant.

### 3. Retrieval-Augmented Generation (RAG)
- [ ] `05_naive_vs_advanced_rag.md` — Naive RAG pipeline, Document Chunking strategies (Character, Recursive, Semantic, Parent-Child / Small-to-Big Chunking).
- [ ] `06_hybrid_search_and_reranking.md` — Hybrid Search (Combining Sparse BM25 lexical search + Dense Vector semantic search with Reciprocal Rank Fusion - RRF), Cross-Encoder Re-ranking models (Cohere Rerank, BGE-Reranker).

### 4. Agentic AI & Orchestration Frameworks
- [ ] `07_agentic_workflows_langchain_langgraph.md` — ReAct (Reason + Act) pattern, Function Calling / Tool Use, LangGraph stateful multi-agent graphs, Cyclical Agent Loops.
- [ ] `08_llm_memory_management.md` — Conversation Buffer Memory, Summary Memory, Vector Store Memory, Managing Context Window budget.

### 5. Fine-Tuning, Quantization & Serving Architecture
- [ ] `09_fine_tuning_lora_qlora.md` — Full Fine-tuning vs Parameter Efficient Fine-Tuning (PEFT), LoRA rank matrices ($W = W_0 + B \cdot A$), QLoRA 4-bit NormalFloat (NF4).
- [ ] `10_llm_inference_serving_vllm.md` — PagedAttention mechanism, vLLM architecture, Continuous Batching, Model Quantization (GGUF, AWQ, GPTQ).

### 6. Evaluation, Guardrails & Security
- [ ] `11_rag_evaluation_metrics.md` — The RAG Triad: Context Relevance, Groundedness (Faithfulness), Answer Relevance. Ragas / DeepEval frameworks.
- [ ] `12_guardrails_and_prompt_security.md` — Prompt Injection attacks (Direct & Indirect), Guardrails AI / NeMo Guardrails, Structured Output Generation (Instructor, Pydantic Output Parsers).

---

## 💡 High-Yield Senior Interview Questions Pointers

1. **How does HNSW indexing enable ultra-fast nearest neighbor search in Vector DBs?**
   * *Answer Pointer:* HNSW creates a multi-layered skip-list graph. Top layers contain sparse long-range connections for fast routing; bottom layers contain dense local connections for precise nearest-neighbor lookup, reducing search time complexity from $O(N)$ to $O(\log N)$.
2. **Explain the difference between Bi-Encoders and Cross-Encoders in RAG.**
   * *Answer Pointer:* Bi-Encoders compute query and document embeddings independently into vector space (fast vector lookup). Cross-Encoders pass query AND document jointly into a transformer model to compute a fine-grained similarity score (slow, but extremely accurate for re-ranking top-K results).
3. **What is PagedAttention in vLLM and how does it optimize memory?**
   * *Answer Pointer:* Traditional serving pre-allocates contiguous memory for KV-cache (Key-Value cache), causing up to 60-80% memory fragmentation. PagedAttention borrows virtual memory paging concepts from OS operating systems, allocating KV-cache in non-contiguous memory blocks, drastically increasing batch throughput.
