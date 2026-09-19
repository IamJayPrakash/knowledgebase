# Top AI & GenAI Senior Interview Questions (Production Systems)

---

## 1. What is the difference between RAG (Retrieval-Augmented Generation) and Fine-Tuning?

- **RAG**:
  - Injects external knowledge dynamically into the LLM context window at query time.
  - Ideal for constantly updating company knowledge bases, verifiable citations, and zero training costs.
  - Cannot alter the fundamental tone, style, or vocabulary of the model.
- **Fine-Tuning**:
  - Updates the actual weights of the neural network using specialized datasets.
  - Ideal for teaching domain-specific output formats (JSON/SQL), specialized styles, or complex syntax.
  - Static: Does not possess knowledge of documents created after the training cutoff.

---

## 2. What causes Hallucinations in LLMs and how do you mitigate them?

- **Causes**: LLMs are probabilistic token prediction engines trained on statistical likelihood, not fact-checkers. Gaps in training data or ambiguous context prompt the model to generate plausible-sounding falsehoods.
- **Mitigation**:
  - Enforce strict ground-truth context via RAG.
  - Lower the sampling `temperature` to 0.0 or 0.1 for factual tasks.
  - Add negative constraints: "If the information is not present in the provided context, state 'I do not have enough information'".
  - Implement programmatic output evaluation guardrails (e.g. Ragas faithfulness checks).

---

## 3. Explain how PagedAttention solves the KV-Cache memory fragmentation problem

- In traditional inference, KV-Cache memory must be allocated contiguously based on the maximum possible sequence length (e.g. 4096 tokens). Because most requests are much shorter, up to 70% of GPU VRAM is wasted in internal fragmentation.
- PagedAttention divides the KV Cache into fixed-sized blocks (pages) stored in non-contiguous physical GPU memory, managed via a page table like modern OS virtual memory. Memory is allocated on-demand, enabling massive batch concurrency.
