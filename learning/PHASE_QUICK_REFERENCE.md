# ASUNA Learning Quick Reference

**Essential concepts, formulas, and debugging tips for your AI/ML research journey.**

---

## Phase 0: Math Essentials

### Linear Algebra
```
Dot product: a·b = Σ(aᵢbᵢ) = ||a|| ||b|| cos(θ)
Matrix multiplication: (AB)ᵢⱼ = Σₖ Aᵢₖ Bₖⱼ
Transpose: (AB)ᵀ = BᵀAᵀ
Eigenvalue equation: Av = λv
```
**Critical insight**: Attention mechanism is just weighted sum = learned dot products!

### Calculus
```
Chain rule: ∂z/∂x = (∂z/∂y)(∂y/∂x)
Gradient: ∇f = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]
Gradient descent: θ ← θ - α∇L(θ)
```
**Critical insight**: Backpropagation = repeated chain rule through computation graph

### Probability
```
Bayes' theorem: P(A|B) = P(B|A)P(A) / P(B)
Cross-entropy: H(p,q) = -Σ p(x) log q(x)
KL divergence: D_KL(P||Q) = Σ P(x) log(P(x)/Q(x))
```
**Critical insight**: Cross-entropy loss = minimize KL divergence between predicted and true distributions

---

## Phase 1: ML Fundamentals

### Loss Functions
```python
# Mean Squared Error (regression)
MSE = (1/n) Σ(yᵢ - ŷᵢ)²

# Binary Cross-Entropy (binary classification)
BCE = -(1/n) Σ[yᵢ log(ŷᵢ) + (1-yᵢ) log(1-ŷᵢ)]

# Categorical Cross-Entropy (multi-class)
CCE = -(1/n) ΣΣ yᵢⱼ log(ŷᵢⱼ)
```

### Backpropagation (2-Layer Network)
```
Forward:
  z₁ = Wx + b    (linear)
  a₁ = σ(z₁)     (activation)
  z₂ = Va₁ + c   (linear)
  ŷ = softmax(z₂) (output)
  L = CrossEntropy(y, ŷ)

Backward:
  dL/dz₂ = ŷ - y
  dL/dV = (dL/dz₂) ⊗ a₁ᵀ
  dL/da₁ = Vᵀ(dL/dz₂)
  dL/dz₁ = (dL/da₁) ⊙ σ'(z₁)
  dL/dW = (dL/dz₁) ⊗ xᵀ
```
**Critical insight**: Gradients flow backward through computation graph

### Optimization Algorithms
```python
# SGD with momentum
v_t = β*v_{t-1} + ∇L
θ_t = θ_{t-1} - α*v_t

# Adam (most popular)
m_t = β₁*m_{t-1} + (1-β₁)*∇L       # first moment
v_t = β₂*v_{t-1} + (1-β₂)*(∇L)²   # second moment
m̂ = m_t/(1-β₁ᵗ)                    # bias correction
v̂ = v_t/(1-β₂ᵗ)
θ_t = θ_{t-1} - α*m̂/(√v̂ + ε)
```
**Typical hyperparams**: α=1e-3, β₁=0.9, β₂=0.999, ε=1e-8

---

## Phase 2: Transformers

### Self-Attention Formula (THE MOST IMPORTANT)
```
Q = XW_Q    (query)
K = XW_K    (key)
V = XW_V    (value)

Attention(Q,K,V) = softmax(QKᵀ/√d_k) V

Where:
- QKᵀ computes similarity between all token pairs
- /√d_k prevents dot products from getting too large
- softmax converts to probabilities
- Multiply by V to get weighted sum of values
```
**Critical insight**: Each output token is weighted combination of ALL input tokens

### Multi-Head Attention
```python
MultiHead(Q,K,V) = Concat(head₁, ..., headₕ)W_O

where headᵢ = Attention(QW_Qⁱ, KW_Kⁱ, VW_Vⁱ)
```
**Why multiple heads?** Different heads learn different types of relationships

### Transformer Block
```
# Encoder block
x = LayerNorm(x + MultiHeadAttention(x))
x = LayerNorm(x + FFN(x))

# Where FFN(x) = ReLU(xW₁ + b₁)W₂ + b₂
```
**Critical components**: 
- Residual connections (+ x) fight vanishing gradients
- LayerNorm stabilizes training
- FFN adds non-linearity

### Positional Encoding
```python
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```
**Why needed?** Attention has no notion of position - all tokens treated equally

---

## Phase 3: BERT & BART

### BERT (Encoder-only)
- **Pre-training**: Masked Language Modeling (MLM) + Next Sentence Prediction (NSP)
- **MLM**: Mask 15% of tokens, predict them
- **Fine-tuning tasks**: Classification (add head on [CLS] token), NER, QA

### BART (Encoder-Decoder)
- **Pre-training**: Denoising autoencoder
- **Corruption types**: token masking, deletion, permutation, rotation, text infilling
- **Fine-tuning**: Can do classification (encoder) OR generation (full model)

### Fine-Tuning for Classification
```python
# Pseudo-code
model = BartForSequenceClassification.from_pretrained('facebook/bart-base')
inputs = tokenizer(text, return_tensors='pt')
outputs = model(**inputs, labels=labels)
loss = outputs.loss
loss.backward()
optimizer.step()
```

---

## Phase 4: Dialogue Systems

### Intent Classification
```
Input: "What's the weather like?"
Output: intent = "weather_query" (confidence: 0.92)
```
**Approach**: Fine-tune BART encoder as sequence classifier

### Response Ranking
```
Input: (query, candidate_response)
Output: relevance_score ∈ [0,1]
```
**Approach**: Fine-tune BART as binary classifier or regression

### System Architecture (Hybrid)
```
User Query
    ↓
Pattern Matcher → Candidates
    ↓
Intent Classifier → Filter by intent
    ↓ 
Response Ranker → Score candidates
    ↓
Select best (score > threshold)
    ↓
Response
```

### Evaluation Metrics
```python
Accuracy = (TP + TN) / (TP + TN + FP + FN)
Precision = TP / (TP + FP)  # What % of predictions are correct?
Recall = TP / (TP + FN)     # What % of actual positives found?
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```
**For imbalanced classes**: Use F1, not accuracy!

---

## Common Debugging Issues

### Training Not Converging
- **Check**: Learning rate too high? Try 1e-4, 1e-5
- **Check**: Gradients exploding? Add gradient clipping
- **Check**: Loss is NaN? Check for log(0), division by zero
- **Check**: Data normalized? Normalize inputs to mean=0, std=1

### Overfitting
- **Symptom**: Training loss ↓, validation loss ↑
- **Solutions**: More data, regularization (dropout, L2), early stopping, data augmentation

### Underfitting
- **Symptom**: Both training and validation loss high
- **Solutions**: Bigger model, train longer, reduce regularization, check data quality

### Model Outputs Nonsense
- **Check**: Tokenizer matches model?
- **Check**: Input/output format correct?
- **Check**: Special tokens ([CLS], [SEP]) in right places?
- **Check**: Attention mask correct?

### Attention/Transformer Issues
- **Vanishing gradients**: Use residual connections + LayerNorm
- **Positional info lost**: Add positional encodings
- **Out of memory**: Reduce batch size or sequence length
- **Slow training**: Use mixed precision (fp16)

---

## Quick Implementation Checklist

### Before Training
- [ ] Data cleaned and explored
- [ ] Train/val/test split done (typically 80/10/10)
- [ ] No data leakage between splits
- [ ] Class balance checked (imbalanced?)
- [ ] Baseline model performance measured

### During Training
- [ ] Monitor both training and validation loss
- [ ] Plot loss curves
- [ ] Save model checkpoints
- [ ] Log hyperparameters
- [ ] Check predictions on sample inputs

### After Training
- [ ] Evaluate on test set (ONE TIME ONLY)
- [ ] Error analysis on failed examples
- [ ] Visualize attention weights
- [ ] Test edge cases
- [ ] Document results

---

## Useful PyTorch Snippets

```python
# Check GPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Move model to GPU
model = model.to(device)

# Gradient clipping (prevent explosion)
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# Save/load checkpoint
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, filepath)

# Count parameters
num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

# Freeze layers
for param in model.encoder.parameters():
    param.requires_grad = False
```

---

## Research Experiment Template

1. **Hypothesis**: "Adding intent classification will improve response relevance by 10%"
2. **Baseline**: Pattern matching only
3. **Treatment**: Pattern matching + intent classifier
4. **Metric**: User satisfaction score (1-5 scale)
5. **Data**: 1000 conversations, 500 control / 500 treatment
6. **Analysis**: T-test for statistical significance
7. **Document**: Results, insights, next steps

---

## Key Intuitions to Remember

- **Embeddings**: Words as points in space, similar meanings = close points
- **Attention**: "Which parts of input are relevant for this output?"
- **Transformers**: Process entire sequence at once (parallel), not sequentially
- **Pre-training**: Learn general language understanding from massive unlabeled data
- **Fine-tuning**: Adapt pre-trained model to specific task with small labeled data
- **Cross-entropy loss**: Measure how different predicted distribution is from true distribution
- **Gradient descent**: Follow downhill direction in loss landscape
- **Backpropagation**: Compute gradients efficiently using chain rule
