# ASUNA Learning Journey - Getting Started

**Welcome to your research-oriented learning path. This guide will help you start your journey from mathematical foundations to building custom AI architectures.**

---

## Before You Start

### Prerequisites Check
- [ ] Python programming comfortable (functions, classes, basic libraries)
- [ ] Familiar with NumPy basics (arrays, basic operations)
- [ ] Can use Jupyter notebooks or Python scripts
- [ ] Have a GPU (optional but recommended for later phases)

### Environment Setup
```bash
# Create virtual environment
python -m venv asuna_ml_env
source asuna_ml_env/bin/activate  # Windows: asuna_ml_env\Scripts\activate

# Install basic requirements
pip install numpy scipy matplotlib jupyter

# For later phases (can install now)
pip install torch torchvision  # PyTorch
pip install transformers datasets  # Hugging Face
pip install scikit-learn pandas seaborn
```

---

## Week 1: Math Foundations Kickoff

### Day 1-2: Linear Algebra (3-4 hours)
**Goal**: Understand vectors, matrices, and operations

**Activities**:
1. Watch: 3Blue1Brown "Essence of Linear Algebra" (first 4 videos)
2. Read: *Mathematics for Machine Learning* Chapter 2 (sections 2.1-2.4)
3. Code: Implement matrix multiplication from scratch in NumPy

```python
# Exercise: Implement matrix multiplication without @
def matmul(A, B):
    # Your implementation here
    pass

# Test
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
assert np.allclose(matmul(A, B), A @ B)
```

### Day 3-4: Calculus Basics (3-4 hours)
**Goal**: Understand derivatives and chain rule

**Activities**:
1. Watch: 3Blue1Brown "Essence of Calculus" (first 5 videos)
2. Practice: Compute derivatives by hand for common functions
3. Code: Implement numerical gradient checking

```python
# Exercise: Numerical gradient
def numerical_gradient(f, x, h=1e-5):
    """Compute gradient numerically"""
    grad = np.zeros_like(x)
    for i in range(x.size):
        x_plus = x.copy()
        x_plus[i] += h
        x_minus = x.copy()
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad
```

### Day 5-7: Probability & Statistics (4-5 hours)
**Goal**: Understand probability distributions and key concepts

**Activities**:
1. Read: *Mathematics for Machine Learning* Chapter 6 (sections 6.1-6.3)
2. Code: Implement and visualize common distributions
3. Exercise: Derive cross-entropy loss from first principles

```python
# Exercise: Implement and plot distributions
import matplotlib.pyplot as plt

# Normal distribution
mu, sigma = 0, 1
x = np.linspace(-5, 5, 100)
y = (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu)/sigma)**2)
plt.plot(x, y)
plt.title('Normal Distribution')
plt.show()

# Try: Bernoulli, Categorical
```

**Week 1 Checkpoint**:
- [ ] Can explain dot product geometrically
- [ ] Can compute derivatives using chain rule
- [ ] Can explain what cross-entropy measures

---

## Week 2-3: First Neural Network from Scratch

### Goal
Build and train a 2-layer neural network without any ML frameworks - only NumPy.

### Step-by-Step Implementation

**Step 1: Implement forward pass** (2-3 hours)
```python
class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights randomly
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def forward(self, X):
        # TODO: Implement forward pass
        # z1 = X @ W1 + b1
        # a1 = relu(z1)
        # z2 = a1 @ W2 + b2
        # probs = softmax(z2)
        pass
```

**Step 2: Derive backpropagation on paper** (2-3 hours)
- Write out the computation graph
- Apply chain rule step by step
- Derive gradient for each parameter

**Step 3: Implement backward pass** (3-4 hours)
```python
def backward(self, X, y):
    # TODO: Implement backpropagation
    # Compute gradients for W2, b2, W1, b1
    pass
```

**Step 4: Train on MNIST** (2-3 hours)
```python
# Load data (use sklearn or download manually)
from sklearn.datasets import load_digits
X, y = load_digits(return_X_y=True)

# Train
for epoch in range(100):
    # Forward pass
    # Compute loss
    # Backward pass
    # Update weights
    pass
```

**Week 2-3 Checkpoint**:
- [ ] Implemented neural network from scratch
- [ ] Training loss decreases
- [ ] Can explain every line of code
- [ ] Achieved >85% accuracy on test set

---

## Month 2: Deep Learning with PyTorch

### Week 4-5: Learn PyTorch
**Goal**: Transition from NumPy to PyTorch, understand automatic differentiation

**Activities**:
1. Work through official PyTorch tutorials
2. Reimplement your neural network in PyTorch
3. Compare: your gradients vs PyTorch autograd
4. Experiment with different architectures and optimizers

### Week 6-8: Start Transformer Study
**Goal**: Understand attention mechanism deeply

**Week 6**: Sequence models (RNN, LSTM) - understand the problems
**Week 7**: Study attention mechanism, implement from scratch
**Week 8**: Study transformer architecture, implement mini-transformer

---

## Learning Resources by Phase

### Phase 0 (Math)
- **Videos**: 3Blue1Brown (Linear Algebra, Calculus)
- **Book**: *Mathematics for Machine Learning* (free PDF online)
- **Practice**: Khan Academy for exercises

### Phase 1 (ML Basics)
- **Course**: Fast.ai Practical Deep Learning (free)
- **Book**: *Deep Learning* by Goodfellow et al. (Chapters 5-8)
- **Practice**: Implement algorithms from scratch

### Phase 2 (Transformers)
- **Papers**: 
  - "Attention Is All You Need" (Vaswani et al.)
  - "BERT" (Devlin et al.)
  - "BART" (Lewis et al.)
- **Course**: Stanford CS224N (YouTube)
- **Book**: *Natural Language Processing with Transformers*

### Phase 3 (NLP/Dialogue)
- **Course**: Hugging Face NLP course (free)
- **Papers**: Recent papers from ACL, EMNLP
- **Practice**: Fine-tune models on real tasks

---

## Study Tips

### Active Learning
- **Don't just read**: Implement everything yourself first
- **Derive on paper**: Work through math by hand before coding
- **Experiment**: Change hyperparameters, break things, understand why
- **Teach**: Explain concepts to others (or rubber duck)

### Time Management
- **Consistency over intensity**: 2 hours daily beats 14 hours on weekends
- **Pomodoro technique**: 25 min focus, 5 min break
- **Track progress**: Use LEARNING_PROGRESS.md checkboxes

### When Stuck
- **Don't spin wheels**: If stuck >1 hour, seek help or move on
- **Multiple resources**: Try different explanations (videos, books, articles)
- **Community**: Join ML Discord servers, Reddit r/MachineLearning
- **Office hours**: Virtual study groups

---

## Your First 30 Days Plan

### Week 1: Math Sprint
- Linear algebra fundamentals
- Calculus and derivatives
- Probability basics
- **Deliverable**: Written notes + code exercises

### Week 2: Neural Network Project
- Implement 2-layer network from scratch
- Derive backpropagation
- Train on simple dataset
- **Deliverable**: Working code with comments explaining each step

### Week 3: Optimization Deep Dive
- Implement SGD, Momentum, Adam
- Study learning rate effects
- Understand regularization
- **Deliverable**: Comparison experiments with plots

### Week 4: PyTorch Transition
- Learn PyTorch basics
- Reimplement your network
- Explore torchvision, datasets
- **Deliverable**: PyTorch version of your network

---

## Set Your Goals

**Short-term (1 month)**:
- [ ] 
- [ ] 
- [ ] 

**Medium-term (3 months)**:
- [ ] 
- [ ] 
- [ ] 

**Long-term (6-9 months)**:
- [ ] 
- [ ] 
- [ ] 

---

## Notes

- **Progress over perfection**: Understanding comes gradually
- **Fundamentals matter**: Don't rush Phase 0, it pays off massively later
- **Hands-on practice**: Reading alone won't work - you must code
- **Ask why**: Always understand the "why" behind techniques
- **Document journey**: Keep notes of insights and challenges

**Ready to start? Open LEARNING_PROGRESS.md and check off your first task!**
