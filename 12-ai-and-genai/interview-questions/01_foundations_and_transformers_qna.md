# AI & GenAI Interview Questions: Part 1 — Foundations, Transformers & Sampling (Q1 - Q20)

---

### Q1: What is next-token prediction and why are modern LLMs described as autoregressive?
- **Answer**: Modern LLMs are autoregressive probabilistic functions modeled as $P(w_t \mid w_1, w_2, \dots, w_{t-1})$. "Autoregressive" means that each newly generated token is conditioned on the sequence of previously generated tokens, fed back into the model's context window as input for the subsequent step. The model repeats this single forward-pass cycle until it produces a special end-of-sequence token (`<|endoftext|>` / `<|eos|>`) or hits the user-configured token ceiling.

### Q2: What is Byte-Pair Encoding (BPE) and how does it prevent Out-Of-Vocabulary (OOV) errors?
- **Answer**: BPE is a subword tokenization algorithm that starts with an atomic base vocabulary of individual bytes (256 ASCII/UTF-8 byte values) and iteratively identifies and merges the most frequently co-occurring byte pairs in the training corpus into new subword units. Because the base vocabulary contains all raw byte values, any arbitrary unicode character or novel neologism can always be decomposed into its constituent bytes, mathematically eliminating Out-Of-Vocabulary (OOV) exceptions.

### Q3: How do Temperature, Top-P, and Top-K sampling parameters interact during token generation?
- **Answer**:
  - **Temperature ($T$)**: Divides raw unnormalized logits ($z_i / T$) prior to softmax. Lowering $T \to 0$ sharpens probabilities into greedy argmax decoding (deterministic). Raising $T > 1$ flattens the distribution for creative variability.
  - **Top-K**: Restricts candidate tokens strictly to the $K$ highest-ranked logits.
  - **Top-P (Nucleus Sampling)**: Dynamically selects the minimal subset of tokens whose cumulative probability exceeds threshold $P$ (e.g., $0.90$).
  - **Execution Order**: Logits $\to$ Temperature Scaling $\to$ Top-K filtering $\to$ Top-P cumulative truncation $\to$ Softmax normalization $\to$ Random sample.

### Q4: Explain the mathematical formula of Scaled Dot-Product Attention.
- **Answer**:
  $$\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$
  $Q$ (Query) represents what the current token seeks; $K$ (Key) identifies token properties; and $V$ (Value) holds the contextual representation. The dot product $QK^T$ calculates pairwise affinity scores. Dividing by $\sqrt{d_k}$ (the head dimension) prevents dot products from growing excessively large for high dimensions, which would otherwise push the softmax function into regions with near-zero gradients (saturation).

### Q5: Why did Decoder-Only architectures surpass Encoder-Decoder (T5/BART) in frontier LLMs?
- **Answer**: Decoder-only architectures (GPT, Llama, Mistral) feature uniform, causal self-attention across every layer, simplifying pre-training objectives to next-token prediction at scale. They exhibit superior sample efficiency during self-supervised pre-training on web corpora, avoid the architectural bottleneck of cross-attention between separate encoder and decoder stacks, and unify few-shot in-context learning under a single generative paradigm.

### Q6: What is the Key-Value (KV) Cache and why is it essential for autoregressive inference?
- **Answer**: In naive transformer inference, generating token $t$ requires computing $Q, K, V$ projections for all tokens $1 \dots t$, resulting in quadratic $O(N^2)$ computational overhead. The KV-Cache saves the calculated Key and Value matrices of historical tokens in GPU High-Bandwidth Memory (HBM). During subsequent forward passes, the model only computes $Q, K, V$ for the single newest token and attends against the cached $K, V$ tensors, reducing per-token generation complexity from $O(N^2)$ to $O(N)$ memory-bandwidth operations.

### Q7: What is Grouped-Query Attention (GQA) and how does it compare to MHA and MQA?
- **Answer**:
  - **Multi-Head Attention (MHA)**: Each Query head has its own dedicated Key and Value head (1:1 ratio). Highest quality, but massive KV-cache VRAM consumption.
  - **Multi-Query Attention (MQA)**: All Query heads share a single Key and Value head ($H:1$ ratio). Minimal VRAM, but causes quality degradation on complex reasoning.
  - **Grouped-Query Attention (GQA)**: Divides Query heads into $G$ groups, where each group shares 1 Key and Value head (e.g. 8 Query heads per 1 KV head in Llama 3). Delivers ~75% KV-cache memory reduction with virtually zero perplexity loss.

### Q8: How does Rotary Position Embedding (RoPE) encode token positions compared to absolute sinusoidal embeddings?
- **Answer**: Absolute sinusoidal embeddings add static position vectors directly to token input embeddings. RoPE instead rotates Query and Key representations in 2D complex planes by an angle proportional to the token index: $R_{\Theta, m} x$. The inner product between rotated vectors depends solely on their relative distance $(m - n)$ rather than absolute positions, preserving translational invariance and enabling length extrapolation (e.g., via NTK-aware scaling).

### Q9: What causes "Hallucinations" in LLMs from a probabilistic perspective?
- **Answer**: Hallucinations occur because LLMs optimize for statistical plausibility over factual truth. The training loss function minimizes cross-entropy on text corpora without an epistemic ground-truth validation mechanism. When user prompts touch sparse, conflicting, or out-of-distribution training regions, the model samples tokens that flow with grammatical fluency and high conversational confidence despite having no empirical factual grounding.

### Q10: What is FlashAttention and why is it dramatically faster than standard PyTorch attention?
- **Answer**: Standard PyTorch attention writes intermediate $N \times N$ attention matrices ($QK^T$ and Softmax) to slow GPU High-Bandwidth Memory (HBM) and reads them back repeatedly. FlashAttention restructures the computation into SRAM blocks using GPU tiling and online softmax scaling, computing attention without ever materializing the large $N \times N$ intermediate matrices in HBM. This converts an IO-bound memory bandwidth bottleneck into a compute-bound operation, accelerating inference by 2x–4x.

### Q11: What is the difference between Frequency Penalty and Presence Penalty in OpenAI/vLLM APIs?
- **Answer**:
  - `frequency_penalty`: Discourages tokens based on their proportional occurrence frequency in the generated completion so far.
  - `presence_penalty`: Applies a flat, one-time logit penalty to any token that has appeared at least once, regardless of frequency, encouraging the model to introduce novel topics.

### Q12: What is In-Context Learning (ICL) and how does it differ from gradient-based fine-tuning?
- **Answer**: In-context learning steers model outputs purely through prompt demonstrations (few-shot examples) placed in the context window. No weights or model gradients are updated. Fine-tuning calculates backpropagation gradients over a loss function to adjust internal model weights permanently in VRAM.

### Q13: What is Chain-of-Thought (CoT) prompting and why does it improve reasoning?
- **Answer**: CoT forces the LLM to generate intermediate reasoning tokens ("Let's think step by step") before outputting a final answer. Because transformers predict tokens autoregressively, producing intermediate reasoning tokens allows the model to utilize additional forward-pass compute cycles and attention steps over its own partial conclusions, dramatically reducing logical leaps and calculation blunders.

### Q14: What is Tree of Thoughts (ToT) prompting?
- **Answer**: ToT generalizes Chain-of-Thought into a tree search exploration. The LLM generates multiple candidate reasoning steps (thoughts) at each juncture, self-evaluates the viability of each branch using heuristic scores, and employs search algorithms (BFS or DFS) with backtracking to abandon dead-end thoughts.

### Q15: How does Constrained Decoding guarantee valid JSON outputs?
- **Answer**: Rather than relying on the LLM to write valid syntax via prompt instructions, Constrained Decoding (e.g. via Outlines or llama.cpp CFG grammars) enforces a Context-Free Grammar (CFG) or JSON Schema directly at the token sampling step. At every generation step, the engine parses the active state machine and assigns $-\infty$ logits to any token that would violate the grammar, mathematically guaranteeing 100% syntactically valid JSON.

### Q16: What is the difference between System, User, and Assistant prompt roles?
- **Answer**:
  - `System`: High-priority operational contract setting personality, negative constraints, and output schema.
  - `User`: The end-user's dynamic question or input payload.
  - `Assistant`: Prior model responses or synthetic few-shot completions forming conversational history.

### Q17: What is the "Lost-in-the-Middle" attention effect in large context windows?
- **Answer**: Empirical studies show that transformer attention is heavily biased toward tokens located at the extreme beginning (primacy effect) and extreme end (recency effect) of long context prompts. When critical information is buried in the middle 40%–60% of a 32K+ token context, retrieval recall drops substantially.

### Q18: What is SwiGLU activation and why is it preferred over ReLU in modern LLMs?
- **Answer**: SwiGLU is a gated activation function combining Swish (SiLU) and GLU (Gated Linear Unit): $\text{SwiGLU}(x) = \text{Swish}(x W) \otimes (x V)$. The bilinear gating mechanism allows the network to dynamically scale information flow through features, consistently achieving lower perplexity than standard ReLU or GELU across LLM scaling laws.

### Q19: What is Root Mean Square Normalization (RMSNorm) and why does Llama use it over LayerNorm?
- **Answer**: Standard LayerNorm computes both mean and variance across activations: $y = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \gamma + \beta$. RMSNorm assumes the mean is approximately zero and normalizes strictly by the root mean square: $y = \frac{x}{\text{RMS}(x)} \gamma$. Eliminating mean centering reduces calculation complexity by ~7% per layer with zero observable degradation in model training stability.

### Q20: What is Context Window Extrapolation and how does YaRN / NTK-aware RoPE work?
- **Answer**: When evaluating sequences longer than the pre-trained context window, high rotational frequencies in RoPE lead to out-of-distribution phase shifts. NTK-aware scaling and YaRN (Yet another RoPE extensioN) scale the base frequency $\Theta$ non-linearly across dimensions: low frequencies (broad global context) are compressed while high frequencies (local token distinction) are preserved, enabling models trained on 4K contexts to extrapolate reliably to 128K tokens without fine-tuning.
