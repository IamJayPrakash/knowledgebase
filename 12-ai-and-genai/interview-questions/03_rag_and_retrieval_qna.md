# AI & GenAI Interview Questions: Part 3 — RAG & Retrieval Pipelines (Q41 - Q60)

---

### Q41: What is the fundamental difference between Naive RAG and Advanced RAG?

- **Answer**:
  - **Naive RAG**: Fixed-size chunking $\to$ single vector embedding model $\to$ top-$K$ cosine similarity search $\to$ prompt injection $\to$ generation. Prone to low precision, lost context, and hallucinations.
  - **Advanced RAG**: Pre-retrieval optimization (query rewriting, HyDE, semantic chunking), Hybrid retrieval (BM25 + Dense vector search with RRF), Post-retrieval refinement (Cross-encoder re-ranking, context compression), and Citation grounding.

### Q42: Why does pure vector search frequently fail on enterprise queries, and how does Hybrid Search resolve it?

- **Answer**: Dense vectors compress overall semantic concepts and excel at fuzzy intent, but lose exact keyword fidelity on alphanumeric product codes, error strings (`0x8004100E`), acronyms, and names. Hybrid search pairs dense vector search with a sparse lexical engine (BM25). BM25 guarantees exact keyword hits while vector search captures conceptual matches, combining the best of both worlds.

### Q43: Explain Reciprocal Rank Fusion (RRF) and why it is superior to raw score normalization

- **Answer**: BM25 scores (unbounded positive numbers) and Cosine similarities ($[0, 1]$ or $[-1, 1]$) follow completely different statistical distributions, making score normalization (e.g. min-max scaling) unstable across diverse queries. RRF merges candidate lists based strictly on ordinal rank positions using the formula:
  $$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
  Where $k$ is a constant (typically 60). It is distribution-agnostic, robust to outliers, and requires zero calibration.

### Q44: What is the difference between a Bi-Encoder and a Cross-Encoder?

- **Answer**:
  - **Bi-Encoder** (e.g., OpenAI embeddings): Encodes query and document independently into fixed-length vectors. Extremely fast for first-stage search over millions of items via MIPS.
  - **Cross-Encoder** (e.g., Cohere Rerank, BGE-Reranker): Concatenates query and document into a single sequence ($[CLS] + Query + [SEP] + Document$) and evaluates full token-to-token cross-attention. Vastly more accurate at scoring relevance, but computationally expensive, making it suitable only as a second-stage reranker for top-25 candidates.

### Q45: What is Parent-Document (Small-to-Big) Chunking and why is it effective?

- **Answer**: In standard RAG, chunk size involves an unavoidable compromise: small chunks optimize vector search precision, while large chunks provide the LLM with sufficient context to generate coherent answers. Parent-Document chunking decouples retrieval from generation: small child chunks (e.g. 100 tokens) are indexed in the vector database for search, but upon matching, the larger parent document chunk (e.g. 1000 tokens) is fetched from a key-value store and fed into the generation prompt.

### Q46: How does HyDE (Hypothetical Document Embeddings) improve retrieval quality?

- **Answer**: HyDE bridges the semantic gap between interrogative user queries and declarative technical documents. An instruction LLM generates a zero-shot hypothetical answer passage. Even if this synthetic passage contains factual hallucinations, its vocabulary, domain phrasing, and grammatical structure closely match true documentation. Embedding this synthetic document enables document-to-document vector search, significantly increasing retrieval recall.

### Q47: What is Sub-Query Decomposition and when is it required?

- **Answer**: When user queries are multi-hop or comparative (*"Compare the security architecture of AWS Lambda vs Google Cloud Functions"*), a single vector query cannot retrieve distinct documents for both entities accurately. Sub-Query Decomposition uses a planner LLM to break the complex query into atomic sub-queries, executes parallel searches across the knowledge base, and synthesizes the retrieved chunks into a unified response.

### Q48: How do you handle complex tables and financial spreadsheets in a RAG ingestion pipeline?

- **Answer**: Converting tables to raw markdown text often destroys row-column relationships and causes embedding models to fail. Production solutions:
  1. Parse tables into structured JSON or HTML with row/column headers preserved.
  2. Generate natural language summary sentences for each row or table chunk using an auxiliary LLM, and embed both the summary and raw table together.
  3. Route analytical tabular queries to Text-to-SQL / DuckDB pipelines rather than pure vector search.

### Q49: What is Multimodal RAG with ColPali and how does it replace legacy OCR?

- **Answer**: Legacy OCR discards page layout, font hierarchies, diagrams, and visual tables. ColPali uses a Vision-Language Model (PaliGemma) to embed high-resolution images of entire PDF pages directly into multi-vector patch representations using late interaction (ColBERT style). It computes token-to-visual-patch similarity directly, allowing users to retrieve complex charts and infographics without error-prone text extraction.

### Q50: How do you enforce strict citation grounding to eliminate hallucinations in RAG outputs?

- **Answer**:
  1. Prepend explicit XML tags with unique IDs to every retrieved chunk in the prompt: `<source id="doc_12">...</source>`.
  2. Instruct the LLM in the system prompt: *"Answer strictly using facts from the provided sources. For every factual claim, append the citation tag `[Source: id]`"*.
  3. Validate citations programmatically using post-generation regex or Pydantic output schemas, rejecting or regenerating any response containing uncited statements.

### Q51: What is Context Compression in LangChain / LlamaIndex?

- **Answer**: Rather than passing raw retrieved chunks verbatim into the prompt, Context Compression uses a lightweight model to filter out irrelevant sentences within the retrieved chunks dynamically. It extracts only the specific paragraphs or sentences directly relevant to the user query, reducing context window token costs by 50–70% and minimizing prompt distraction.

### Q52: How do you prevent context window saturation in multi-turn conversational RAG?

- **Answer**: If a user asks 5 follow-up questions, appending every round of retrieved context explodes the context budget. Solutions:
  1. Re-phrase follow-up queries into standalone search queries using conversational history (*"Query Condenser"*).
  2. Flush prior retrieved chunks from context, retaining only the past dialogue summary and fresh chunks retrieved for the latest turn.

### Q53: What is Self-RAG (Self-Reflective Retrieval-Augmented Generation)?

- **Answer**: Self-RAG trains an LLM to generate special reflection tokens dynamically:
  - `[Retrieve]`: Decides whether external retrieval is even necessary for the query.
  - `[ISREL]`: Evaluates whether retrieved context is relevant.
  - `[ISSUP]`: Checks whether the generated response is supported by context (grounding).
  - `[ISUSE]`: Evaluates utility of response. This enables the model to self-diagnose and re-retrieve on the fly.

### Q54: What is Corrective RAG (CRAG)?

- **Answer**: CRAG adds an automated retrieval evaluator that scores the confidence of retrieved documents:
  - **Correct**: Proceeds to generation with compressed context.
  - **Incorrect**: Triggers an automated fallback to public web search (e.g. Google/Tavily API) to find missing facts.
  - **Ambiguous**: Combines vector knowledge with web search results for hybrid synthesis.

### Q55: How do you handle document versioning and real-time updates in a production RAG knowledge base?

- **Answer**: Documents are tracked with hash fingerprints (SHA-256) and semantic versions in metadata. When a document is updated:
  1. The pipeline identifies all chunk IDs associated with `doc_id`.
  2. Issues a batch delete for existing vectors in the vector DB.
  3. Ingests, chunks, embeds, and upserts new chunks with incremented version tags.
  4. Flushes semantic query caches associated with the modified topic.

### Q56: What is GraphRAG and when does Knowledge Graph RAG outperform Vector RAG?

- **Answer**: Vector RAG is excellent for point-specific semantic retrieval, but struggles with global, holistic questions (*"What are the main themes across all 500 customer interview transcripts?"*). GraphRAG (pioneered by Microsoft Research) extracts an entity-relationship knowledge graph from the corpus using LLMs, clusters entities into hierarchical communities, and generates pre-computed community summaries, enabling high-level thematic synthesis across millions of words.

### Q57: How do you benchmark retrieval accuracy independently from generation quality?

- **Answer**: Using information retrieval metrics:
  - **Hit Rate@K**: Proportion of queries where at least one ground-truth chunk is present in the top-$K$ retrieved results.
  - **Mean Reciprocal Rank (MRR)**: Average reciprocal rank ($1/\text{rank}$) of the first relevant document.
  - **NDCG@K (Normalized Discounted Cumulative Gain)**: Measures ranking quality, giving higher credit when the most relevant chunks are placed at the very top.

### Q58: What is the "Negative Rejection" problem in RAG and how is it addressed?

- **Answer**: When a user asks a question whose answer is NOT present in the retrieved context, poorly tuned models hallucinate plausible answers from pre-trained weights. Mitigate by:
  1. Adding explicit negative few-shot examples in system prompts showing the model responding: *"Based on the provided documentation, I cannot verify this information"*.
  2. Applying post-generation grounding guardrails that flag responses when citation overlap is below a confidence threshold.

### Q59: How does Chunk Overlap prevent context truncation at chunk boundaries?

- **Answer**: Without overlap, splitting a sentence like *"Alex Turner was appointed CEO in 2021. He previously led engineering"* across a 50-character boundary splits the pronoun from its antecedent. Chunk overlap (typically 10%–20%) carries the tail end of the preceding chunk into the start of the next chunk, preserving cross-sentence references and semantic cohesion.

### Q60: What is Semantic Caching in RAG architectures (e.g. GPTCache)?

- **Answer**: Rather than caching exact string matches (which misses synonymous queries), Semantic Caching embeds incoming user queries and computes cosine similarity against a vector store of past cached queries. If similarity exceeds a high threshold (e.g. 0.96), the system immediately returns the cached LLM response, dropping query latency from 2,000ms to 8ms and reducing API token costs to zero.
