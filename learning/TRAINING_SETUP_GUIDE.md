# TRANSFORMER TRAINING SYSTEM - SETUP & USAGE GUIDE

## Overview

This comprehensive training system allows you to fine-tune a transformer model on your chat data to improve response quality beyond regex patterns.

**What you get:**
- Full transformer training pipeline with mathematical explanations
- Automatic data preparation from unknown query logs
- Model evaluation with multiple metrics  
- Fallback integration into Chat_raw2.py
- Complete documentation of all math concepts

## Quick Start (5 minutes)

### 1. Install Requirements

```bash
# Install training dependencies
pip install -r requirements_training.txt

# This installs:
# - torch (deep learning framework)
# - transformers (HuggingFace models)
# - evaluation metrics libraries
# - and more
```

### 2. Prepare Your Training Data

You have two options:

**Option A: Auto from unknown queries (recommended for first run)**
```python
# Place your existing unknown queries in the standard location
# Already populated: src/Asuna_data/server/unknown query.txt
```

**Option B: Manual labeled data**
```json
// Create: src/Asuna_data/server/training_data.json
[
  {"input": "hello", "output": "Hi there!"},
  {"input": "what time", "output": "I don't have access to time"},
  ...
]
```

### 3. Run Training

```bash
cd src
python train_quickstart.py
```

That's it! The script will:
1. Load and clean your data
2. Split into train/val/test
3. Train a BART transformer
4. Evaluate performance
5. Save the best model

**Expected runtime:** 
- 2-5 minutes on GPU
- 15-30 minutes on CPU
- Depends on dataset size

---

## In-Depth Setup

### Installation Details

#### GPU Support (Recommended)

```bash
# NVIDIA GPU (most common)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# AMD GPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7

# Mac with Apple Silicon
pip install torch torchvision torchaudio

# Check installation
python -c "import torch; print(f'GPU available: {torch.cuda.is_available()}')"
```

#### CPU Only

```bash
pip install torch torchvision torchaudio

# This works anywhere but is slower (100x slower than GPU!)
```

### Directory Structure Expected

```
VoiceAI-Asuna/
├── learning/
│   ├── train_data_prep.py           (data loading & splitting)
│   ├── train_transformer.py         (training loop)
│   ├── train_inference.py           (inference & evaluation)
│   ├── train_fallback_integration.py (Chat_raw2.py integration)
│   ├── train_quickstart.py          (main script)
│   ├── TRAIN_MATH_GUIDE.md          (mathematical explanations)
│   └── requirements_training.txt
├── src/
│   ├── Asuna_data/
│   │   └── server/
│   │       ├── unknown query.txt             (your chat logs)
│   │       ├── example_training_data.json    (optional)
│   │       ├── train.jsonl                   (generated)
│   │       ├── val.jsonl                     (generated)
│   │       └── test.jsonl                    (generated)
│   └── models/
│       └── asuna_seq2seq/                    (generated)
│           ├── best_model/
│           ├── final_model/
│           └── training_stats.json
```

---

## Understanding the Training System

### 1. Data Preparation (`train_data_prep.py`)

**What it does:**
- Loads unknown queries from logs
- Removes duplicates
- Analyzes dataset statistics
- Performs stratified train/val/test split

**Key concepts:**
- **Stratification:** Ensures each split has same intent distribution
- **Deduplication:** Keeps highest confidence version of duplicate inputs
- **Statistics:** Calculates mean sequence lengths, distribution

**Mathematical detail:** See [TRAIN_MATH_GUIDE.md](TRAIN_MATH_GUIDE.md#stratified-train-test-split)

### 2. Transformer Training (`train_transformer.py`)

**What it does:**
- Loads pre-trained BART model from HuggingFace
- Creates data loaders with batching
- Trains for multiple epochs
- Validates and saves best checkpoint
- Implements early stopping

**Key concepts:**
- **Self-Attention:** Each token learns to focus on relevant tokens
- **Cross-Entropy Loss:** Measures prediction error
- **Backpropagation:** Computes gradients through all layers
- **Adam Optimizer:** Adaptive learning rate for each parameter

**Mathematical detail:** See [TRAIN_MATH_GUIDE.md](#transformer-training-pipeline)

### 3. Evaluation (`train_inference.py`)

**Metrics calculated:**
- **Exact Match (EM):** Percentage of perfect matches (0-100%)
- **BLEU:** N-gram overlap with reference (0-1 scale)
- **ROUGE:** Recall-oriented n-gram overlap (0-1 scale)
- **Perplexity:** How confused the model is (lower is better)

**Baseline comparison:** Compares against simple strategies

### 4. Fallback Integration (`train_fallback_integration.py`)

**What it does:**
- Loads trained model as fallback for unmatched queries
- Estimates confidence for each response
- Only uses response if confidence exceeds threshold
- Falls back to generic response if uncertain

**Confidence calculation:** See [train_fallback_integration.py](train_fallback_integration.py#confidence-scoring)

---

## Configuration

Edit `learning/train_quickstart.py` CONFIG dict to customize:

```python
CONFIG = {
    # Data
    'data_dir': './Asuna_data/server/',
    'unknown_queries_file': 'unknown query.txt',
    
    # Split ratios
    'train_ratio': 0.7,      # 70% for training
    'val_ratio': 0.15,       # 15% for validation
    'test_ratio': 0.15,      # 15% for testing
    
    # Model
    'model_name': 'facebook/bart-base',  # Options: 'bart-large', 't5-base'
    'output_dir': './models/asuna_seq2seq',
    'device': 'cuda',  # 'cpu' if no GPU
    
    # Training hyperparameters
    'num_epochs': 3,         # More = better but risk overfitting
    'batch_size': 16,        # Smaller if out of memory
    'learning_rate': 5e-5,   # 1e-5 to 5e-4 typical range
    'max_length': 128,       # Input/output token limit
    
    # Early stopping
    'early_stopping_patience': 2,  # Stop if val loss doesn't improve for N epochs
    
    # Inference
    'num_beams': 4,  # 1=greedy, 4-8=good balance, 8+=slow
}
```

### Hyperparameter Tuning Guide

**Too much memory used?**
- Reduce `batch_size` (8 or 4)
- Reduce `max_length` (64 instead of 128)
- Reduce `num_beams` (1 = greedy, fastest)

**Training too slow?**
- Increase `batch_size` (32, 64)
- Reduce `num_epochs` (1-2)
- Use GPU instead of CPU
- Reduce `max_length`

**Bad quality results?**
- Increase `num_epochs` (5-10)
- Collect more training data
- Increase `learning_rate` slightly (5e-5 to 1e-4)
- Increase `batch_size` (32, 64)

**Model overfits (train loss low, val loss high)?**
- Reduce `learning_rate`
- Reduce `num_epochs`
- Increase `batch_size`
- Use `early_stopping_patience=1` or 2

---

## Running the Training

### Step 1: Prepare Data

```bash
python -c "
from train_data_prep import TrainingDataset

# Quick test to verify data loads
dataset = TrainingDataset('./Asuna_data/server/')
dataset.load_unknown_queries('unknown query.txt')
print(f'Loaded {len(dataset.examples)} examples')
"
```

### Step 2: Run Full Pipeline

```bash
python train_quickstart.py
```

**Expected output:**
```
======================================================================
ASUNA TRANSFORMER TRAINING PIPELINE
======================================================================

Configuration:
  data_dir: ./Asuna_data/server/
  num_epochs: 3
  batch_size: 16
  ...

======================================================================
STEP 1: PREPARING DATA
======================================================================
Loading unknown queries...
Loaded 150 examples from unknown query.txt
Cleaning data...
Removed 10 duplicate examples
Calculating statistics...
Dataset Statistics:
  total_examples: 140
  avg_input_length: 8.5
  avg_output_length: 10.2
  max_input_length: 45
  ...

Splitting data...
Split sizes - Train: 98, Val: 21, Test: 21
Saving data splits...

======================================================================
STEP 2: TRAINING MODEL
======================================================================
Loading model from facebook/bart-base
Starting training loop...

Epoch 1/3
Training: 100%|████████| 7/7 [00:45<00:00, 6.43s/batch]
Training Loss: 2.3456
Evaluating: 100%|████████| 2/2 [00:05<00:00, 2.50s/batch]
Validation - Loss: 2.1234, Perplexity: 8.35
✓ Saved best model (loss: 2.1234)

Epoch 2/3
...

======================================================================
STEP 3: EVALUATING MODEL
======================================================================
Evaluating on 21 test examples...
Evaluation Results:
{
  "exact_match": 0.33,
  "exact_match_%": 33,
  "bleu": 0.45,
  "rouge1": 0.52
}

Model Performance vs Baselines:
Trained Model EM: 0.33
Echo Baseline EM: 0.0
Improvement: ∞%  (or very high)

======================================================================
STEP 4: SAMPLE RESPONSES
======================================================================
Q: hello
A: Hi there! I'm Asuna, nice to meet you

Q: what is your name
A: I'm Asuna, your AI assistant

...

✓ TRAINING COMPLETE!
======================================================================

Model saved to: ./models/asuna_seq2seq
```

### Step 3: Monitor Training

During training, check statistics:

```bash
# In a separate terminal
tail -f models/asuna_seq2seq/training_stats.json | python -m json.tool
```

---

## Integrating with Chat_raw2.py

### Quick Integration (5 lines of code)

Add to `src/Chat_raw2.py`:

```python
# At top of file
from train_fallback_integration import TransformerFallback

# In __init__ or module startup
transformer_fallback = TransformerFallback(
    model_path="./models/asuna_seq2seq/best_model",
    confidence_threshold=0.5
)

# In your message handling, when regex match fails
def basic_output(user_input, user):
    # ... existing regex patterns ...
    
    if not any_pattern_matched:
        # Use transformer fallback
        response, metadata = transformer_fallback.get_response(user_input)
        msg.rep(response)
        return
```

### Advanced Integration (with logging)

```python
# Track when transformer is used
def basic_output(user_input, user):
    # ... existing regex patterns ...
    
    if not any_pattern_matched:
        response, metadata = transformer_fallback.get_response(user_input)
        
        # Log usage
        if metadata['source'] == 'transformer':
            logger.info(f"Transformer used: confidence={metadata['confidence']:.3f}")
            user.stats.transformer_uses += 1
        else:
            user.stats.fallback_uses += 1
        
        msg.rep(response)
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'torch'"

```bash
pip install torch transformers
```

### "CUDA out of memory"

```python
# In train_quickstart.py CONFIG:
'batch_size': 8,      # was 16
'max_length': 64,     # was 128
```

### "Model not found" error during inference

Make sure training completed successfully:
```bash
ls -la models/asuna_seq2seq/best_model/
# Should show: config.json, generation_config.json, pytorch_model.bin, etc.
```

### Poor model quality

**Check:**
1. Is training data diverse? (20+ examples of different intents)
2. Are labels accurate? (check example_training_data.json)
3. Is model running long enough? (try 5-10 epochs)

**Solutions:**
- Collect more diverse training data
- Label examples more carefully
- Train for more epochs
- Increase model size (bart-large instead of bart-base)

### Training very slow

```bash
# Check GPU usage
nvidia-smi

# If GPU not used:
python -c "import torch; print(torch.cuda.is_available())"

# If False, reinstall PyTorch with CUDA support
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## Performance Metrics Explanation

### Exact Match (EM)

```
EM = 33% means:
- 33 out of 100 test examples had perfect word-for-word matches
- This is strict (ignores semantic equivalence)
- Improvement from baseline often dramatic
```

### BLEU Score

```
BLEU = 0.45 means:
- 0-0.3: Poor
- 0.3-0.5: Acceptable
- 0.5-0.7: Good
- 0.7+: Excellent

BLEU measures n-gram overlap (shared phrases).
```

### ROUGE Score

```
ROUGE = 0.52 means:
- Similar to BLEU but emphasizes recall
- 0.52 is decent for chat tasks
- Higher values: model captures reference content well
```

### Perplexity

```
Perplexity = 8.35 means:
- Model equally confused between ~8 options at each step
- Lower is better
- Baseline ~50 → 200 depending on task
- 5-10 is good for fine-tuned model
```

---

## Advanced: Custom Training

### Using Your Own Model

```python
# In config:
'model_name': 'google/t5-small',  # or any HuggingFace model
```

Popular alternatives:
- `facebook/bart-large` (best quality, slower)
- `google/t5-base` (balanced)
- `distilbart-cnn-6-6` (fast, less accurate)

### Adding More Data

```python
# In train_data_prep.py after loading unknown_queries:

dataset.load_manual_training_data('my_labeled_data.json')
dataset.load_manual_training_data('more_data.json')  # Can load multiple
```

### Custom Train/Val/Test Split

```python
train, val, test = dataset.train_val_test_split(
    train_ratio=0.8,    # More training data
    val_ratio=0.1,
    test_ratio=0.1,
    seed=42,            # For reproducibility
    stratify_by_intent=True
)
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `train_quickstart.py` | Main entry point - run this first! |
| `train_data_prep.py` | Data loading and preparation |
| `train_transformer.py` | Training loop with math explanations |
| `train_inference.py` | Inference and evaluation metrics |
| `train_fallback_integration.py` | Integration with Chat_raw2.py |
| `TRAIN_MATH_GUIDE.md` | Complete mathematical explanations |
| `example_training_data.json` | Sample labeled data |
| `requirements_training.txt` | All dependencies |

---

## Next Steps

1. **Run training:** `python train_quickstart.py`
2. **Check results:** Review output metrics
3. **Integrate:** Add fallback to Chat_raw2.py
4. **Collect feedback:** Monitor transformer usage
5. **Iterate:** Collect more training data, retrain

---

## Support & Debugging

### Print detailed logs

```python
# In any training script
import logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see detailed information
```

### Save logs to file

```python
import logging
handler = logging.FileHandler('training.log')
logging.getLogger().addHandler(handler)
```

### Inspect model

```python
from train_transformer import TransformerTrainer

trainer = TransformerTrainer()
print(trainer.model)  # Shows architecture
print(trainer.model.config)  # Shows hyperparameters
```

---

## References

- Transformer Architecture: https://arxiv.org/abs/1706.03762
- BART Model: https://arxiv.org/abs/1910.13461
- HuggingFace Docs: https://huggingface.co/docs/transformers/
- Training Tips: https://huggingface.co/docs/transformers/training

---

**Happy training! 🚀**

For math details, see: [TRAIN_MATH_GUIDE.md](TRAIN_MATH_GUIDE.md)
