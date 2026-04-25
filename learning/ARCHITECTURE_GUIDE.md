# ASUNA Research Architecture Guide

**Framework for designing and experimenting with custom AI architectures for dialogue systems.**

---

## Current System Overview

### Existing Pattern-Based System
```
User Input
    ↓
[Text Normalization]
    ↓
[Pattern Matching Engine] ← 50+ regex patterns
    ↓
[Response Template Selection]
    ↓
[Response Generation]
    ↓
Output Response
```

**Strengths**:
- Fast, deterministic, controllable
- No model latency
- Easy to debug and maintain
- Works well for known patterns

**Weaknesses**:
- Brittle (exact pattern matching)
- Doesn't generalize to unseen inputs
- Hard to handle natural language variations
- No learning from interactions

---

## Research Architecture Design Space

### Design Philosophy
**Goal**: Build hybrid system that combines strengths of rule-based and neural approaches.

**Principles**:
1. **Graceful degradation**: Always have fallback
2. **Explainability**: Understand why system made decisions
3. **Iterative improvement**: Learn from data over time
4. **Research-oriented**: Experiment with novel approaches

---

## Architecture Option 1: Neural Intent + Pattern Response

### Flow
```
User Input
    ↓
[BART Intent Classifier] ← Fine-tuned on your intents
    ↓
Intent prediction + confidence
    ↓
[Pattern Engine] ← Use intent to filter patterns
    ↓
Response
```

### Components to Build
1. **Intent Taxonomy** (`src/intent_taxonomy.py`)
   - Define 12-20 intent classes
   - Map from your existing pattern groups
   - Examples: greeting, question_weather, compliment, farewell, etc.

2. **Intent Classifier** (`src/train_intent_classifier.py`)
   - Fine-tune `facebook/bart-base` for sequence classification
   - Train on labeled conversations
   - Output: intent + confidence score

3. **Integration** (`src/Chat_raw2.py`)
   - Use intent to route to appropriate pattern groups
   - If confidence < threshold, fall back to pattern matching only

### Research Questions
- Does intent classification improve pattern matching accuracy?
- What's the optimal confidence threshold?
- Which intents benefit most from neural classification?

---

## Architecture Option 2: Neural Response Validation

### Flow
```
User Input
    ↓
[Pattern Engine] → Generate N candidate responses
    ↓
[BART Response Validator] ← Score each candidate
    ↓
Select best response (score > threshold)
    ↓
If all scores low: Use safe fallback
    ↓
Response
```

### Components to Build
1. **Response Validator** (`src/train_response_validator.py`)
   - Fine-tune BART to score (query, response) pairs
   - Binary classification: relevant / not relevant
   - Or regression: relevance score 0-1

2. **Candidate Generation** (`src/Chat_raw2.py`)
   - Pattern engine generates multiple candidates
   - Validator scores each
   - Threshold-based selection

3. **Fallback Strategy**
   - If no candidate > threshold, use safe response
   - Log for later analysis

### Research Questions
- Does validation improve response quality?
- How many candidates should be generated?
- Optimal threshold for validator?
- Can validator learn from user feedback?

---

## Architecture Option 3: Retrieval-Augmented Response

### Flow
```
User Input
    ↓
[Encode query] ← BART encoder
    ↓
[Dense Retrieval] ← Search conversation history
    ↓
Retrieve K similar conversations
    ↓
[Response Generator/Selector] ← Use retrieved context
    ↓
Response
```

### Components to Build
1. **Conversation Encoder** (`src/encode_conversations.py`)
   - Use BART/BERT to encode all past conversations
   - Store embeddings in vector database (FAISS, Pinecone)

2. **Retrieval System** (`src/retrieval_system.py`)
   - Query: embed input, find K nearest neighbors
   - Return similar conversations and their responses

3. **Response Selection** (`src/Chat_raw2.py`)
   - Option A: Return response from most similar conversation
   - Option B: Use retrieved context to inform pattern matching
   - Option C: Fine-tune BART to generate based on retrieved context

### Research Questions
- Does retrieval improve response quality?
- Optimal number of retrieved examples (K)?
- Dense vs sparse retrieval?
- How to handle privacy/inappropriate retrieved content?

---

## Architecture Option 4: Multi-Task Learning

### Flow
```
User Input
    ↓
[BART Multi-Task Model]
    ├→ Intent prediction
    ├→ Sentiment prediction
    ├→ Response quality score
    └→ Entity extraction
    ↓
Use predictions to inform response selection
    ↓
Response
```

### Components to Build
1. **Multi-Task BART** (`src/train_multitask_bart.py`)
   - Single model with multiple heads
   - Shared encoder, task-specific decoders
   - Joint training on multiple tasks

2. **Task-Specific Heads**
   - Intent: sequence classification
   - Sentiment: sequence classification
   - Response quality: regression
   - Entities: token classification

3. **Decision Logic** (`src/Chat_raw2.py`)
   - Use multiple signals to make better decisions
   - Example: If sentiment negative + intent complaint → route to support patterns

### Research Questions
- Does multi-task learning improve individual task performance?
- Optimal loss weighting for different tasks?
- Which tasks benefit from shared representation?
- Can we learn tasks with limited labels?

---

## Architecture Option 5: End-to-End Neural Generation

### Flow
```
User Input + Conversation History
    ↓
[BART Seq2Seq Model] ← Fine-tuned on conversations
    ↓
Generate response
    ↓
[Safety Filter] ← Check for inappropriate content
    ↓
Response
```

### Components to Build
1. **Conversation Dataset** (`src/prepare_conversation_data.py`)
   - Format: (context, response) pairs
   - Include multi-turn conversations
   - Clean and filter data

2. **BART Generator** (`src/train_bart_generator.py`)
   - Fine-tune `facebook/bart-base` for seq2seq
   - Experiment with different decoding strategies:
     - Greedy decoding
     - Beam search
     - Top-k sampling
     - Nucleus (top-p) sampling

3. **Safety Layer** (`src/safety_filter.py`)
   - Filter inappropriate/unsafe generations
   - Detect off-topic responses
   - Fallback to safe response if filtered

### Research Questions
- Can generation match pattern-based quality?
- How to control response style/personality?
- How to prevent repetitive/generic responses?
- How to ensure factual accuracy?

**Warning**: Generation is hardest approach, requires most data and careful evaluation.

---

## Recommended Research Progression

### Phase 1: Start Simple (Option 1 or 2)
- **Easiest**: Intent Classification (Option 1)
- **Next**: Response Validation (Option 2)
- Build foundation, learn fine-tuning process
- Establish evaluation methodology

### Phase 2: Add Complexity (Option 3 or 4)
- **Retrieval** (Option 3): If you have good conversation history
- **Multi-Task** (Option 4): If you can label multiple tasks
- Experiment with hybrid approaches

### Phase 3: Advanced (Option 5)
- **Generation** (Option 5): Most challenging
- Requires large dataset and careful evaluation
- Consider only after mastering earlier options

---

## Evaluation Framework

### Automatic Metrics
```python
# Accuracy (for classification)
accuracy = correct_predictions / total_predictions

# Precision, Recall, F1 (for classification)
from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred))

# Perplexity (for generation)
perplexity = math.exp(cross_entropy_loss)

# BLEU (for generation - compare to reference)
from nltk.translate.bleu_score import sentence_bleu
bleu = sentence_bleu([reference], hypothesis)
```

### Human Evaluation
- **Relevance**: Is response relevant to input? (1-5)
- **Coherence**: Does response make sense? (1-5)
- **Engagement**: Is response interesting? (1-5)
- **Correctness**: Is information accurate? (Yes/No)
- **Style**: Matches Asuna personality? (1-5)

### A/B Testing
```python
# Compare two systems
def ab_test(system_a, system_b, test_queries):
    # Randomly assign queries
    # Collect user satisfaction ratings
    # Statistical significance test
    pass
```

---

## Experimentation Best Practices

### 1. Define Hypothesis First
"Adding intent classification will improve response accuracy by 15% on ambiguous queries."

### 2. Establish Baseline
Measure current system performance before changes.

### 3. Control Variables
Change ONE thing at a time to isolate effects.

### 4. Version Everything
```python
# Model version
model_version = "intent_classifier_v1.2"

# Dataset version
dataset_hash = hash(training_data)

# Config version
config = {
    "model": "facebook/bart-base",
    "learning_rate": 2e-5,
    "epochs": 3,
    "batch_size": 16
}
```

### 5. Log Everything
```python
import logging

logger.info(f"Query: {query}")
logger.info(f"Intent: {intent} (confidence: {confidence})")
logger.info(f"Response: {response}")
logger.info(f"Latency: {latency_ms}ms")
```

### 6. Analyze Failures
When system fails, understand WHY:
- Collect failure examples
- Categorize failure types
- Prioritize fixes based on frequency

---

## File Structure for Research Implementation

```
src/
├── models/
│   ├── intent_classifier.py       # Intent classification model
│   ├── response_validator.py      # Response validation model
│   ├── response_generator.py      # Response generation model
│   └── multitask_model.py         # Multi-task model
│
├── training/
│   ├── train_intent_classifier.py # Training script for intent
│   ├── train_validator.py         # Training script for validator
│   └── data_preparation.py        # Data loading and preprocessing
│
├── inference/
│   ├── intent_predictor.py        # Intent prediction at runtime
│   ├── response_scorer.py         # Response scoring at runtime
│   └── retrieval_engine.py        # Retrieval system
│
├── evaluation/
│   ├── eval_intent.py             # Evaluate intent classifier
│   ├── eval_responses.py          # Evaluate response quality
│   └── human_eval.py              # Human evaluation tools
│
├── utils/
│   ├── intent_taxonomy.py         # Intent definitions
│   ├── metrics.py                 # Custom metrics
│   └── logging_utils.py           # Logging helpers
│
└── Chat_raw2.py                   # Main chatbot integration
```

---

## Next Steps

1. **Choose one architecture option** to start (recommend Option 1 or 2)
2. **Define research questions** you want to answer
3. **Collect/label initial dataset** (start small: 100-500 examples)
4. **Implement baseline** (measure current system)
5. **Build and train model** (start with pre-trained BART)
6. **Evaluate rigorously** (automatic + human evaluation)
7. **Iterate based on results**

**Remember**: Research is about learning, not perfection. Expect failures, learn from them, iterate.

---

## Key Insights to Remember

- **Hybrid > Pure Neural**: Combine rules and learning
- **Fallback is Essential**: Always have a safe default
- **Evaluation is Hard**: Multiple metrics + human eval
- **Data Quality > Quantity**: 500 good examples > 5000 noisy
- **Simple First**: Master basics before complexity
- **Iterate Quickly**: Fast experiments > perfect first try
