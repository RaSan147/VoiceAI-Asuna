# QUICK REFERENCE: EVERYTHING YOU NEED TO KNOW

## 📚 Documentation Map

| Document | Purpose | Read When |
|----------|---------|-----------|
| **TRAINING_SYSTEM_SUMMARY.md** | Overview of entire system | First! |
| **TRAINING_SETUP_GUIDE.md** | Step-by-step setup & troubleshooting | Setting up |
| **TRAIN_MATH_GUIDE.md** | All mathematics explained | Want to understand how it works |
| **train_quickstart.py** | Main script - run this! | Ready to train |

## 🚀 Quick Start (Copy-Paste)

### 1. Install
```bash
cd P:\C_coding\Python\VoiceAI-Asuna
pip install -r requirements_training.txt
```

### 2. Train
```bash
cd src
python train_quickstart.py
```

This will:
- Load your unknown queries
- Train a transformer model 
- Evaluate and save the best model
- Show sample responses

### 3. Integrate (Optional)

Add to `Chat_raw2.py` after existing imports:

```python
# At top of file
from train_fallback_integration import TransformerFallback

# In module initialization (e.g., at top of basic_output function)
# Or at module level:
_fallback = None

def get_fallback():
    global _fallback
    if _fallback is None:
        _fallback = TransformerFallback(
            "./models/asuna_seq2seq/best_model",
            confidence_threshold=0.5
        )
    return _fallback

# In basic_output() function, when no regex pattern matches:
if no_pattern_matched:
    fallback = get_fallback()
    response, metadata = fallback.get_response(user_input)
    msg.rep(response)
    return
```

## 📊 The Pipeline Explained

```
YOUR DATA
   ↓
[train_data_prep.py]
   ├─ Load unknown queries
   ├─ Clean & deduplicate  
   ├─ Split train/val/test
   └─ Save as JSONL
   ↓
[train_transformer.py]
   ├─ Load BART model
   ├─ Train 3 epochs
   ├─ Validate each epoch
   └─ Save best checkpoint
   ↓
[train_inference.py]
   ├─ Load best model
   ├─ Generate responses
   ├─ Calculate metrics
   └─ Compare to baselines
   ↓
[train_fallback_integration.py]
   ├─ Load model
   ├─ Estimate confidence
   ├─ Return response if confident
   └─ Fallback if not
   ↓
[Chat_raw2.py]
   └─ Use transformer as fallback for unmatched queries
```

## 🧮 Mathematics at a Glance

### Attention Mechanism (Most Important!)
```
Attention = softmax(Query × Key^T / √64) × Value

This lets tokens "pay attention" to relevant other tokens
- Each token can focus on any other token's meaning
- Model learns what's relevant through training
- Multiple heads learn different patterns
```

### Loss Function
```
Loss = -log(P(correct_token))

Training minimizes this loss.
Lower loss = better predictions.
```

### Metrics
- **EM (Exact Match)**: % of perfect word-for-word matches
- **BLEU**: N-gram overlap (0-1 scale)
- **ROUGE**: Recall-oriented overlap (0-1 scale)  
- **Perplexity**: How confused model is (lower = better)

## ⚙️ Configuration Options

Edit `train_quickstart.py` CONFIG dict:

```python
{
    # Danger zone - only change if you know what to do:
    'learning_rate': 5e-5,    # 1e-5 to 5e-4 typical
    'num_epochs': 3,          # More = better but slower
    'batch_size': 16,         # Smaller if out of memory
    'max_length': 128,        # Longer = more memory
    
    # Safe to change anytime:
    'model_name': 'facebook/bart-base',  # or 'bart-large', 't5-base'
    'output_dir': './models/asuna_seq2seq',
}
```

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "CUDA out of memory" | Batch too large | Set `batch_size: 8` |
| "No module named torch" | Not installed | `pip install torch` |
| "Model not found" | Training didn't complete | Check for errors in run |
| "Poor quality responses" | Not enough training data | Collect 100+ examples |
| "Training super slow" | Using CPU | Install PyTorch with CUDA |

## 🔍 File Locations

**Data files:**
- Input: `src/Asuna_data/server/unknown query.txt`
- Output: `src/Asuna_data/server/train.jsonl`, `val.jsonl`, `test.jsonl`

**Model files:**
- Best model: `src/models/asuna_seq2seq/best_model/`
- Final model: `src/models/asuna_seq2seq/final_model/`
- Stats: `src/models/asuna_seq2seq/training_stats.json`

**Training scripts:**
- All in: `src/` directory

## 📈 What Success Looks Like

### During Training
```
Epoch 1/3
Training: 100%|████| loss decreases from 2.5 → 1.5
Validation: loss = 1.4, perplexity = 4.1
✓ Saved best model

Epoch 2/3
Training: loss 1.5 → 1.2  
Validation: loss = 1.3, perplexity = 3.7
✓ Saved best model

Epoch 3/3
Training: loss 1.2 → 1.0
Validation: loss = 1.2 (improvements slow)
```

### After Training
```
Test Results:
  Exact Match: 45%        (45 out of 100 test examples perfect)
  BLEU: 0.52              (good)
  ROUGE: 0.58             (good)
  Improvement: 900%       (vs baseline)
```

### After Integration
```
User: "tell me a joke"
[Regex patterns don't match]
[Transformer fallback: confidence 0.87]
Bot: "Why did the AI go to school? To improve its neural networks!"
```

## 🎯 Confidence Threshold Guide

**In `train_fallback_integration.py`:**

```python
TransformerFallback(
    confidence_threshold=0.3   # Use transformer 70% of time (risky)
    confidence_threshold=0.5   # 30% of time (recommended)
    confidence_threshold=0.8   # 10% of time (very conservative)
)
```

Higher threshold = safer but transformer used less. Find your balance!

## 📋 Checklist: Before Running

- [ ] Install requirements: `pip install -r requirements_training.txt`
- [ ] Check data exists: `src/Asuna_data/server/unknown query.txt`
- [ ] Read `TRAINING_SETUP_GUIDE.md`
- [ ] Review `train_quickstart.py` CONFIG
- [ ] Have 30+ minutes (or 5 with GPU)
- [ ] GPU available? (optional but 100x faster)

## 🎓 Learn More

### Want to understand the math?
Read: `TRAIN_MATH_GUIDE.md`

Topics covered:
- Tokenization & embeddings
- Positional encoding (sine/cosine formula)
- Self-attention mechanism
- Feedforward networks
- Loss functions
- Backpropagation
- Optimization algorithms
- Evaluation metrics

### Want to customize training?
Read: `TRAINING_SETUP_GUIDE.md` → "Advanced: Custom Training"

Examples:
- Using different models (T5, etc.)
- Adding your own training data
- Hyperparameter tuning
- Custom train/val/test splits

### Want to debug?
Read: `TRAINING_SETUP_GUIDE.md` → "Troubleshooting"

Or check the code: Each file has detailed comments

## 🔄 Training Again (Iteration)

After first training:

1. **Review results**: Check metrics and sample outputs
2. **Collect feedback**: Monitor which responses work/don't work
3. **Label more data**: If quality is bad, collect more examples
4. **Retrain**: Run `train_quickstart.py` again

Each iteration:
```
More data (50 → 100 → 200 examples)
           ↓        ↓        ↓
Better quality (20% → 40% → 60% EM)
```

## 💡 Pro Tips

**Tip 1: Compare models**
```python
# Save multiple checkpoints
CONFIG['output_dir'] = './models/asuna_v1'  # Run 1
CONFIG['output_dir'] = './models/asuna_v2'  # Run 2
# Compare metrics in training_stats.json
```

**Tip 2: Use confidence scores**
```python
# Log when transformer is used
response, meta = fallback.get_response(user_input)
print(f"Confidence: {meta['confidence']:.2f}")

# Adjust threshold based on logs
if too_many_low_quality:
    fallback.adjust_confidence_threshold(0.6)  # More conservative
```

**Tip 3: Collect user feedback**
```python
# Ask user to rate response
# if rating < 3: mark as bad example
# Retrain with bad examples
```

## ❓ FAQ

**Q: How long does training take?**
A: 1-2 min on GPU, 10-30 min on CPU

**Q: How much training data do I need?**
A: 50+ examples minimum, 200+ for good results

**Q: Which model should I use?**
A: Start with `bart-base` (default), upgrade to `bart-large` if quality is bad

**Q: Can I use my GPU?**
A: Yes! Install PyTorch with CUDA: `pip install torch --index-url https://download.pytorch.org/whl/cu118`

**Q: What if model produces weird text?**
A: Increase confidence threshold, or collect better training data

**Q: Can I use this with languages other than English?**
A: Yes, but you need multilingual models. We use English-only BART by default.

## 📞 Support

If something breaks:

1. Check error message - usually tells you what's wrong
2. Read `TRAINING_SETUP_GUIDE.md` troubleshooting section
3. Check file paths - make sure relative paths are correct
4. Verify installation: `python -c "import torch; print(torch.cuda.is_available())"`

## 🎉 Next Steps

1. **Install & Test**: Run quick start above
2. **Train**: `python train_quickstart.py`
3. **Review Results**: Check metrics and samples
4. **Integrate**: Add fallback to Chat_raw2.py
5. **Monitor**: Track quality in production
6. **Iterate**: Collect more data, retrain

---

**Ready? Let's go! 🚀**

```bash
pip install -r requirements_training.txt
cd src
python train_quickstart.py
```

Good luck! 🌟
