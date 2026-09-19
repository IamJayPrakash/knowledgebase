# Machine Coding: End-to-End RAG Pipeline in Pure Python

---

## 🐣 1. Layman's Analogy
RAG pipeline ek **Open-Book Exam** ki tarah hai: Jab question aata hai, toh student (Search Engine) library se relevant 2 page nikalta hai (`Chunk Retrieval`), aur fir professor (LLM) ko bolta hai: "Sirf in 2 panno ko dekh kar answer likho, apne man se kahani mat banao" (`Grounded Prompt Generation`)!

---

## 💻 2. Line-by-Line Commented Code Solution

```python
import numpy as np

# Simple In-Memory Vector Store for RAG Pipeline
class SimpleVectorRAG:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    # Simulated embedding generator (In production, call OpenAI / HuggingFace API)
    def _mock_embed(self, text: str) -> np.ndarray:
        # Deterministic pseudo-embedding based on character hashes for demo
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(64).astype("float32")
        norm = np.linalg.norm(vec)
        return vec / (norm if norm > 0 else 1.0)

    # Line 18: Ingest and chunk documents
    def add_document(self, doc_id: str, text: str):
        self.documents.append({"id": doc_id, "text": text})
        embedding = self._mock_embed(text)
        self.embeddings.append(embedding)

    # Line 24: Retrieve Top-K most relevant document chunks
    def retrieve(self, query: str, k: int = 2):
        query_vec = self._mock_embed(query)
        similarities = []

        for idx, doc_vec in enumerate(self.embeddings):
            # Calculate cosine similarity (vectors are unit normalized)
            score = float(np.dot(query_vec, doc_vec))
            similarities.append((score, self.documents[idx]))

        # Sort descending by similarity score
        similarities.sort(key=lambda x: x[0], reverse=True)
        return similarities[:k]

    # Line 38: Construct augmented grounded prompt for LLM
    def generate_grounded_prompt(self, user_query: str) -> str:
        relevant_chunks = self.retrieve(user_query, k=2)
        context_str = "\n---\n".join([c[1]["text"] for c in relevant_chunks])

        prompt = f'''You are an enterprise AI assistant. Answer the user question strictly using ONLY the provided context below.
If the answer cannot be deduced from the context, respond with "I cannot find this information in the knowledge base."

CONTEXT:
{context_str}

USER QUESTION:
{user_query}

ANSWER:'''
        return prompt

# Test RAG Pipeline
rag = SimpleVectorRAG()
rag.add_document("doc1", "Next.js App Router uses React Server Components by default to eliminate client bundle size.")
rag.add_document("doc2", "Redis distributed locking requires the Redlock algorithm or atomic SET NX PX with Lua script verification.")

augmented_prompt = rag.generate_grounded_prompt("How does Next.js handle server components?")
print("Constructed Grounded Prompt:\n")
print(augmented_prompt)
```
