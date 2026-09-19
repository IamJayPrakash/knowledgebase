# 🤖 Master 110 GenAI & LLM Interview Questions Catalog & Roadmap

> An exhaustive, production-grade interview repository containing **110 high-yield interview questions and system design scenarios** across foundational transformers, vector search, RAG, orchestration frameworks (**LangChain**, **LangFlow**, **LangGraph**), multi-agent systems, fine-tuning, vLLM serving, and enterprise security.

---

## 🗺️ Categorized Question Index

| Module | Focus Area | Question Range | Topics Covered | Link |
| :--- | :--- | :---: | :--- | :--- |
| **Part 1** | **Foundations, Transformers & Sampling** | Q1 – Q20 | Next-token prediction, BPE, Softmax Temperature, Top-P, Top-K, Scaled Dot-Product, Decoder-only, KV-Cache, GQA, RoPE, FlashAttention, SwiGLU, RMSNorm. | [**`01_foundations_and_transformers_qna.md`**](./01_foundations_and_transformers_qna.md) |
| **Part 2** | **Embeddings & Vector Databases** | Q21 – Q40 | Dense vectors, Cosine vs Euclidean vs Dot Product, $L_2$ normalization, HNSW graph mechanics ($M$, $efConstruction$, $efSearch$), IVF-PQ, Matryoshka embeddings, Pre vs Post filtering, Chroma, Qdrant, Pinecone, Milvus. | [**`02_embeddings_and_vectordb_qna.md`**](./02_embeddings_and_vectordb_qna.md) |
| **Part 3** | **RAG & Retrieval Pipelines** | Q41 – Q60 | Naive vs Advanced RAG, Hybrid Search (BM25 + Dense), RRF, Bi-Encoders vs Cross-Encoders, Parent-Document chunking, HyDE, Sub-query decomposition, ColPali Multimodal RAG, Citation grounding, Semantic Caching. | [**`03_rag_and_retrieval_qna.md`**](./03_rag_and_retrieval_qna.md) |
| **Part 4** | **LangChain, LangFlow, LangGraph & Agents** | Q61 – Q80 | LCEL pipe operator, Runnables, LangFlow low-code canvas & Python export, LangGraph StateGraph, Cycles vs DAGs, Reducers, Checkpointing, Human-in-the-Loop, ReAct pattern, Tool calling, Supervisor multi-agent. | [**`04_langchain_langflow_langgraph_agents_qna.md`**](./04_langchain_langflow_langgraph_agents_qna.md) |
| **Part 5** | **Fine-Tuning, Serving & Ops** | Q81 – Q100 | LoRA math, QLoRA NF4, SFT vs DPO, vLLM PagedAttention, Continuous Batching, VRAM sizing formulas, AWQ vs GPTQ vs GGUF, Speculative Decoding, Guardrails AI, Ragas RAG Triad, Prefix Caching. | [**`05_finetuning_serving_and_ops_qna.md`**](./05_finetuning_serving_and_ops_qna.md) |
| **Part 6** | **Scenario-Based AI System Design** | Q101 – Q110 | Enterprise Multi-Tenant RAG, Autonomous Customer Support Multi-Agent, Low-Latency Code Copilot, Financial PDF Extractor, High-Volume Guardrail Gateway, Self-Healing Text-to-SQL, Cost/Latency Optimizer. | [**`06_scenario_based_system_design_ai_qna.md`**](./06_scenario_based_system_design_ai_qna.md) |

---

## 🎯 Coding Exercises
* [**`coding_simple_rag_pipeline_python.md`**](./coding_simple_rag_pipeline_python.md) — Live coding implementation of an in-memory RAG pipeline in pure Python.
