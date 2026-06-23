# Datasets for Alignment Robustness Research

This directory contains datasets for studying null results in alignment interventions. Data files are locally available but excluded from git due to size. Follow download instructions below.

---

## Dataset 1: Anthropic HH-RLHF (Helpful-Harmless RLHF)

### Overview
- **Source**: https://huggingface.co/datasets/Anthropic/hh-rlhf
- **Size**: ~160,800 train + ~8,552 test examples
- **Format**: HuggingFace Dataset (chosen/rejected pairs)
- **Task**: Preference learning for helpfulness and harmlessness alignment
- **Splits**: train (160,800), test (8,552)
- **License**: MIT

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("Anthropic/hh-rlhf")
dataset.save_to_disk("datasets/hh_rlhf/full")
```

### Loading

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/hh_rlhf/full")
# OR directly:
from datasets import load_dataset
dataset = load_dataset("Anthropic/hh-rlhf")
```

### Notes
- Contains chosen/rejected conversation pairs where chosen = more helpful+harmless response
- Used for RLHF and DPO training
- Critical for evaluating alignment intervention baseline effectiveness

---

## Dataset 2: PKU-Alignment SafeRLHF

### Overview
- **Source**: https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF
- **Size**: ~73,907 train + ~8,211 test examples
- **Format**: HuggingFace Dataset (response pairs with safety labels)
- **Task**: Safety-aware preference learning
- **Features**: prompt, two responses, safety labels, harm categories, severity levels

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("PKU-Alignment/PKU-SafeRLHF")
dataset.save_to_disk("datasets/pku_safe_rlhf/full")
```

### Notes
- Each example has explicit safety labels for both responses (is_response_0_safe, etc.)
- Also includes harm category and severity level annotations
- Useful for measuring safety alignment effectiveness with granular labels

---

## Dataset 3: TruthfulQA

### Overview
- **Source**: https://huggingface.co/datasets/truthfulqa/truthful_qa
- **Size**: 817 validation examples
- **Format**: HuggingFace Dataset (question + correct/incorrect answers)
- **Task**: Measuring truthfulness of LLM responses
- **Config**: "generation" (for open-ended generation) or "multiple_choice"

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("truthfulqa/truthful_qa", "generation")
dataset.save_to_disk("datasets/truthfulqa/full")
```

### Notes
- Tests whether LLMs confidently generate falsehoods
- Useful for measuring truthfulness-related alignment intervention effectiveness
- 817 questions across 38 categories (e.g., finance, health, law, conspiracies)

---

## Dataset 4: AdvBench (Harmful Behaviors)

### Overview
- **Source**: https://github.com/llm-attacks/llm-attacks (CSV in repo)
- **Size**: 520 harmful behavior examples
- **Format**: CSV with 'goal' and 'target' columns
- **Task**: Red-teaming / safety evaluation
- **File**: `datasets/advbench/harmful_behaviors.csv` (locally available)

### Download Instructions

```bash
wget https://raw.githubusercontent.com/llm-attacks/llm-attacks/main/data/advbench/harmful_behaviors.csv \
  -O datasets/advbench/harmful_behaviors.csv
```

### Loading

```python
import pandas as pd
df = pd.read_csv("datasets/advbench/harmful_behaviors.csv")
# Columns: goal (harmful task), target (desired harmful response prefix)
```

### Notes
- Standard benchmark for testing safety alignment bypass resistance
- Critical for measuring intervention effectiveness at systematically varied strengths
- Each example has goal (attacker objective) and target (first tokens model should NOT generate)

---

## Dataset 5: HarmBench

### Overview
- **Source**: https://github.com/centerforaisafety/HarmBench
- **Size**: 1,214 test behaviors
- **Format**: CSV with Behavior, FunctionalCategory, SemanticCategory, Tags columns
- **Task**: Comprehensive safety evaluation benchmark
- **File**: `datasets/harmbench/harmbench_test.csv` (locally available)

### Download Instructions

```bash
wget https://raw.githubusercontent.com/centerforaisafety/HarmBench/main/data/behavior_datasets/harmbench_behaviors_text_test.csv \
  -O datasets/harmbench/harmbench_test.csv
```

### Loading

```python
import pandas as pd
df = pd.read_csv("datasets/harmbench/harmbench_test.csv")
# Columns: Behavior, FunctionalCategory, SemanticCategory, Tags, ContextString, BehaviorID
```

### Notes
- More comprehensive than AdvBench (1214 vs 520 behaviors)
- Includes semantic and functional categories for fine-grained analysis
- Used in the SAE Interventions paper for cross-benchmark validation

---

## Dataset 6: Toxic-Chat (lmsys)

### Overview
- **Source**: https://huggingface.co/datasets/lmsys/toxic-chat
- **Size**: 5,082 train + 5,083 test examples
- **Format**: HuggingFace Dataset
- **Task**: Toxicity detection in real LLM conversations
- **Config**: toxicchat0124

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("lmsys/toxic-chat", "toxicchat0124")
dataset.save_to_disk("datasets/toxic_chat/full")
```

### Notes
- Real chat conversations with human toxicity annotations
- Includes jailbreaking labels
- Useful for measuring intervention effectiveness on naturalistic harmful queries

---

## Recommended Usage for Experiments

For measuring alignment intervention effectiveness across systematically varied intervention strengths:

1. **Primary safety benchmark**: AdvBench (520 behaviors) + HarmBench (1,214 behaviors)
2. **Alignment preference learning**: HH-RLHF + PKU-SafeRLHF for training
3. **Truthfulness alignment**: TruthfulQA (817 questions)
4. **Naturalistic safety**: Toxic-Chat (10,165 examples)

The key experimental design is to vary intervention strength (e.g., DPO β parameter, RLHF reward scaling, activation steering magnitude) and measure whether safety improvement follows a dose-response curve or shows a plateau (null results despite increasing intervention).
