# LLM Fine-Tuning: LoRA, QLoRA, and Quantization (GGUF, AWQ, GPTQ)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Full Fine-Tuning 70 Billion parameters wale model ke **Har Ek Screw Ko Khologe Dobara Fit Karne Jaisa Hai** (Requires $100,000 worth of GPUs and 80GB VRAM).
**LoRA (Low-Rank Adaptation)** ek **Chote Transparent Sticky Note** ki tarah hai: Asli 1000-page ki book (Base LLM weights) ko chhedne ke bajaye, aap uske upar ek chota sticky note chipkate ho (Rank decomposition matrices A and B). Model wahi rehta hai, sirf 0.1% naye parameters train hote hain!
**Quantization** ek **High-Res 4K Video ko 1080p mein Compress** karne jaisa hai: 16-bit floating point numbers (`FP16`) ko 4-bit integers (`INT4`) mein convert kar diya jata hai taaki 70B model aapke normal gaming laptop par chal sake!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **The Math of LoRA**:
   - Instead of updating weight matrix $W \in \mathbb{R}^{d \times k}$ directly ($W = W + \Delta W$), we decompose $\Delta W$ into two low-rank matrices: $\Delta W = B \times A$, where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with rank $r \ll \min(d, k)$.
   - Freezes 99.9% of base model weights; only updates adapters.
2. **QLoRA (Quantized LoRA)**:
   - Quantizes the base model weights to NormalFloat4 (NF4) and introduces Double Quantization, enabling fine-tuning a 65B model on a single 48GB GPU.
3. **Quantization Formats**:
   - **GGUF**: Modern standard for CPU/Metal inference (via llama.cpp).
   - **AWQ (Activation-aware Weight Quantization)**: Preserves salient weights based on activation distribution; state-of-the-art for high-throughput GPU serving (vLLM).
   - **GPTQ**: Post-training 4-bit quantization optimized for fast GPU matrix multiplication.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
# PEFT LoRA Configuration Setup
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM

# Line 5: Define LoRA Hyperparameters
lora_config = LoraConfig(
    r=16,                                    # Rank dimension (lower = fewer parameters)
    lora_alpha=32,                           # Scaling factor for adapter weights
    target_modules=["q_proj", "v_proj"],     # Apply LoRA to attention query and value layers
    lora_dropout=0.05,                       # Dropout for regularization
    bias="none",                             # Do not train bias terms
    task_type=TaskType.CAUSAL_LM             # Generative Language Modeling task
)

# Base model load with 4-bit quantization (BitsAndBytes)
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B", load_in_4bit=True)
# peft_model = get_peft_model(model, lora_config)
# peft_model.print_trainable_parameters()
# Trainable params: 0.08% of total weights!
```
