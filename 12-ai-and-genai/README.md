# 🤖 12 - AI & GenAI Systems Master Curriculum & Index

> A comprehensive, end-to-end architectural roadmap and senior interview index covering **LLM Foundations, Vector DBs, Advanced RAG, Orchestration (LangChain, LangFlow, LangGraph), Multi-Agent Systems, Fine-Tuning, vLLM Serving, and Security Guardrails**.

---

## 🗺️ Master Curriculum & Architectural Subdirectories

### 1. 🧠 [01-llm-foundations/](./01-llm-foundations/)

* [**`01_llm_fundamentals_tokens_context_and_sampling.md`**](./01-llm-foundations/01_llm_fundamentals_tokens_context_and_sampling.md) — Next-token prediction, BPE Tokenization, Context Windows, Softmax Temperature, Top-P, Top-K, Frequency & Presence Penalties.
* [**`02_transformer_architecture_and_self_attention.md`**](./01-llm-foundations/02_transformer_architecture_and_self_attention.md) — Scaled Dot-Product Attention, $Q, K, V$ intuition, Multi-Head Attention, RoPE (Rotary Position Embeddings), KV-Cache, and FlashAttention.
* [**`03_prompt_engineering_cot_and_structured_outputs.md`**](./01-llm-foundations/03_prompt_engineering_cot_and_structured_outputs.md) — Zero-shot, Few-shot in-context learning, Chain-of-Thought (CoT), Tree of Thoughts (ToT), Constrained Decoding, and Pydantic JSON Schemas.

---

### 2. 🔢 [02-embeddings-and-vector-databases/](./02-embeddings-and-vector-databases/)

* [**`01_embeddings_vector_spaces_and_similarity_metrics.md`**](./02-embeddings-and-vector-databases/01_embeddings_vector_spaces_and_similarity_metrics.md) — Dense vector representations, Cosine Similarity vs Dot Product vs Euclidean ($L_2$) distance, $L_2$ normalization, Bi-Encoders vs Cross-Encoders, Matryoshka embeddings.
* [**`02_vector_databases_hnsw_and_indexing.md`**](./02-embeddings-and-vector-databases/02_vector_databases_hnsw_and_indexing.md) — HNSW multi-layer skip graphs ($M$, $efConstruction$, $efSearch$), IVF-PQ quantization, Single-stage metadata pre-filtering, Chroma, Qdrant, Pinecone, and Milvus.

---

### 3. 🔍 [03-retrieval-augmented-generation-rag/](./03-retrieval-augmented-generation-rag/)

* [**`01_rag_architecture_chunking_and_retrieval.md`**](./03-retrieval-augmented-generation-rag/01_rag_architecture_chunking_and_retrieval.md) — Naive RAG vs Production RAG, Recursive character splitting, Semantic chunking, Parent-Document (Small-to-Big) chunking, and Grounded citation prompts.
* [**`02_advanced_rag_hybrid_search_and_reranking.md`**](./03-retrieval-augmented-generation-rag/02_advanced_rag_hybrid_search_and_reranking.md) — Sparse BM25 lexical search + Dense vector search, Reciprocal Rank Fusion (RRF: $k=60$), and Cross-Encoder Re-ranking (Cohere / BGE-Reranker).
* [**`03_query_transformation_hyde_and_multimodal_rag.md`**](./03-retrieval-augmented-generation-rag/03_query_transformation_hyde_and_multimodal_rag.md) — HyDE (Hypothetical Document Embeddings), Sub-Query decomposition, Step-back prompting, and Multimodal Vision RAG (ColPali).

---

### 4. ⛓️ [04-orchestration-langchain-and-langflow/](./04-orchestration-langchain-and-langflow/)

* [**`01_langchain_core_lcel_and_runnables.md`**](./04-orchestration-langchain-and-langflow/01_langchain_core_lcel_and_runnables.md) — LangChain Expression Language pipe operator (`|`), `ChatPromptTemplate`, `ChatModel`, `StrOutputParser`, `RunnableParallel`, `RunnablePassthrough`, streaming (`astream`).
* [**`02_langchain_chains_memory_and_tools.md`**](./04-orchestration-langchain-and-langflow/02_langchain_chains_memory_and_tools.md) — ConversationSummaryBufferMemory, Token budget management, Custom Tools via `@tool` decorator, Structured tools with Pydantic arguments.
* [**`03_langflow_visual_ai_prototyping_and_architecture.md`**](./04-orchestration-langchain-and-langflow/03_langflow_visual_ai_prototyping_and_architecture.md) — LangFlow low-code canvas, Component nodes, Graph serialization to JSON, Headless REST API deployment, and exporting visual canvas to clean Python code.

---

### 5. 🤖 [05-agentic-ai-and-langgraph/](./05-agentic-ai-and-langgraph/)

* [**`01_agentic_ai_react_pattern_and_tool_calling.md`**](./05-agentic-ai-and-langgraph/01_agentic_ai_react_pattern_and_tool_calling.md) — ReAct loop (Thought $\to$ Action $\to$ Observation), Native Tool Calling protocols (OpenAI, Anthropic schemas), Self-healing exception loops, and Stopping guardrails.
* [**`02_langgraph_state_machines_and_agentic_workflows.md`**](./05-agentic-ai-and-langgraph/02_langgraph_state_machines_and_agentic_workflows.md) — LangGraph StateGraph, Cycles vs DAGs, Reducers (`Annotated[..., operator.add]`), Conditional edge routers, Checkpointing (`PostgresSaver`), and Human-in-the-Loop (`interrupt_before`).
* [**`03_multi_agent_systems_and_hierarchical_orchestration.md`**](./05-agentic-ai-and-langgraph/03_multi_agent_systems_and_hierarchical_orchestration.md) — Multi-agent collaboration topologies, Centralized Supervisor pattern, Isolated sub-agent scratchpads, Recursion ceilings, and Preventing infinite conversational loops.

---

### 6. ⚙️ [06-fine-tuning-and-serving/](./06-fine-tuning-and-serving/)

* [**`01_fine_tuning_lora_qlora_and_peft.md`**](./06-fine-tuning-and-serving/01_fine_tuning_lora_qlora_and_peft.md) — When to Fine-Tune vs RAG, Parameter-Efficient Fine-Tuning (PEFT), LoRA math ($W = W_0 + \frac{\alpha}{r} BA$), QLoRA 4-bit NF4, Double Quantization, Paged Optimizers, SFT vs DPO.
* [**`02_production_serving_vllm_paged_attention_and_quantization.md`**](./06-fine-tuning-and-serving/02_production_serving_vllm_paged_attention_and_quantization.md) — High-throughput serving, KV-Cache memory bottleneck, PagedAttention block tables, Continuous Batching (Iteration-level), AWQ vs GPTQ vs GGUF quantization, Speculative Decoding.

---

### 7. 🛡️ [07-guardrails-security-and-evaluation/](./07-guardrails-security-and-evaluation/)

* [**`01_guardrails_security_and_prompt_injection.md`**](./07-guardrails-security-and-evaluation/01_guardrails_security_and_prompt_injection.md) — Direct & Indirect prompt injection, Jailbreaking, System prompt extraction, NeMo Guardrails, Input/Output PII scrubbing (Presidio), Data exfiltration countermeasures.
* [**`02_llm_evaluation_ragas_and_benchmarking.md`**](./07-guardrails-security-and-evaluation/02_llm_evaluation_ragas_and_benchmarking.md) — LLM-as-a-Judge, The RAG Triad (Context Relevance, Faithfulness/Groundedness, Answer Relevance), Ragas & DeepEval frameworks, Mitigating judge bias (position, verbosity).

---

### 8. 🎓 [interview-questions/](./interview-questions/)

* [**`interview-questions/README.md`**](./interview-questions/README.md) — Master 110 Questions Index & Curriculum Matrix.
* [**`01_foundations_and_transformers_qna.md`**](./interview-questions/01_foundations_and_transformers_qna.md) — Questions 1 to 20.
* [**`02_embeddings_and_vectordb_qna.md`**](./interview-questions/02_embeddings_and_vectordb_qna.md) — Questions 21 to 40.
* [**`03_rag_and_retrieval_qna.md`**](./interview-questions/03_rag_and_retrieval_qna.md) — Questions 41 to 60.
* [**`04_langchain_langflow_langgraph_agents_qna.md`**](./interview-questions/04_langchain_langflow_langgraph_agents_qna.md) — Questions 61 to 80.
* [**`05_finetuning_serving_and_ops_qna.md`**](./interview-questions/05_finetuning_serving_and_ops_qna.md) — Questions 81 to 100.
* [**`06_scenario_based_system_design_ai_qna.md`**](./interview-questions/06_scenario_based_system_design_ai_qna.md) — Questions 101 to 110 (Complex System Design Scenarios).
* [**`coding_simple_rag_pipeline_python.md`**](./interview-questions/coding_simple_rag_pipeline_python.md) — Live Coding RAG pipeline in pure Python.
