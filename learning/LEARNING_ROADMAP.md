# ASUNA Research Learning Roadmap

**Goal**: Build deep understanding of AI/ML/NLP fundamentals and design custom research architectures for the Asuna chatbot system.

**Timeline**: 6-9 months progressive learning + experimentation

---

## Phase 0: Mathematical Foundations (Weeks 1-4)

### Objective
Build the mathematical toolkit required for understanding modern ML/NLP.

### Topics

#### Linear Algebra
- Vectors, matrices, tensors
- Matrix operations: multiplication, transpose, inverse
- Eigenvalues and eigenvectors
- Vector spaces, basis, orthogonality
- **Application**: Understanding embeddings, attention matrices, weight transformations

#### Calculus
- Derivatives and partial derivatives
- Chain rule (critical for backpropagation)
- Gradients and Jacobians
- Basic optimization concepts
- **Application**: Understanding gradient descent, loss minimization

#### Probability & Statistics
- Probability distributions (normal, Bernoulli, categorical)
- Expected value, variance, covariance
- Conditional probability and Bayes' theorem
- Maximum likelihood estimation
- **Application**: Understanding loss functions, sampling, probabilistic models

### Learning Activities
- [ ] Work through linear algebra exercises (3Blue1Brown series recommended)
- [ ] Implement matrix operations from scratch in NumPy
- [ ] Derive backpropagation using chain rule on paper
- [ ] Study probability distributions and implement sampling
- [ ] Read: "Mathematics for Machine Learning" (Deisenroth et al.)

### Checkpoint
- Can derive gradient for simple functions by hand
- Can explain what dot product means geometrically
- Can explain cross-entropy loss using probability theory

---

## Phase 1: Machine Learning Fundamentals (Weeks 5-10)

### Objective
Understand core ML concepts and neural network basics.

### Topics

#### Supervised Learning Foundations
- Loss functions: MSE, cross-entropy, hinge loss
- Gradient descent: batch, mini-batch, stochastic
- Regularization: L1, L2, dropout
- Overfitting vs underfitting
- Train/validation/test split philosophy

#### Neural Networks
- Perceptron and multilayer perceptrons (MLPs)
- Activation functions: sigmoid, tanh, ReLU, GELU
- Backpropagation algorithm (derive it!)
- Weight initialization strategies
- Optimization algorithms: SGD, Adam, AdamW

#### Practical ML
- Data preprocessing and normalization
- Feature engineering
- Hyperparameter tuning strategies
- Evaluation metrics: accuracy, precision, recall, F1, AUC
- Cross-validation

### Learning Activities
- [ ] Implement a 2-layer neural network from scratch (no frameworks)
- [ ] Derive backpropagation equations on paper for your network
- [ ] Train classifiers on toy datasets (MNIST, Iris)
- [ ] Experiment with different learning rates and observe convergence
- [ ] Implement gradient descent variants (SGD, momentum, Adam)
- [ ] Read: "Deep Learning" Ch 5-8 (Goodfellow et al.)

### Checkpoint
- Can implement and train a neural network without frameworks
- Can explain why Adam usually works better than vanilla SGD
- Can diagnose overfitting and underfitting from training curves

---

## Phase 2: Deep Learning & Transformers (Weeks 11-18)

### Objective
Master modern deep learning, especially transformer architecture.

### Topics

#### Advanced Neural Architectures
- Convolutional Neural Networks (CNNs) - optional for NLP
- Recurrent Neural Networks (RNNs, LSTMs, GRUs)
- Sequence-to-sequence models
- Limitations of RNNs for long sequences

#### Attention Mechanism
- Self-attention intuition and mathematics
- Query, Key, Value matrices
- Scaled dot-product attention formula
- Multi-head attention
- **Critical**: Derive attention formula from scratch

#### Transformer Architecture
- Encoder-decoder structure
- Positional encoding
- Layer normalization
- Feedforward sublayers
- Residual connections
- Why transformers solve the long-range dependency problem

#### BERT & BART Specifically
- Bidirectional encoding (BERT)
- Masked language modeling objective
- BART: denoising autoencoder approach
- Pre-training vs fine-tuning paradigm
- Token classification, sequence classification, seq2seq tasks

### Learning Activities
- [ ] Implement self-attention mechanism from scratch
- [ ] Read "Attention Is All You Need" paper (Vaswani et al.)
- [ ] Implement a mini-transformer encoder in PyTorch
- [ ] Study BERT and BART papers thoroughly
- [ ] Visualize attention weights for sample sentences
- [ ] Fine-tune a small BERT model on text classification
- [ ] Read: "Deep Learning" Ch 10-12, "Natural Language Processing with Transformers" (Tunstall et al.)

### Checkpoint
- Can explain attention mechanism mathematically and intuitively
- Can draw transformer architecture from memory with all components
- Can explain difference between BERT, GPT, and BART
- Successfully fine-tuned a transformer on a task

---

## Phase 3: NLP & Dialogue Systems (Weeks 19-26)

### Objective
Apply deep learning to NLP tasks and understand dialogue system design.

### Topics

#### Core NLP Tasks
- Text classification (sentiment, intent, topic)
- Named entity recognition (NER)
- Question answering
- Text generation and decoding strategies
- Evaluation metrics: perplexity, BLEU, ROUGE, BERTScore

#### Dialogue Systems
- Task-oriented vs open-domain dialogue
- Intent detection and slot filling
- Dialogue state tracking
- Response selection vs response generation
- Context management in multi-turn conversations
- Evaluation: human evaluation strategies, automatic metrics

#### Advanced Techniques
- Retrieval-augmented generation (RAG)
- Hybrid systems (rule-based + neural)
- Few-shot and zero-shot learning
- Prompt engineering for large models
- Knowledge grounding

### Learning Activities
- [ ] Build intent classifier using BART/BERT for your Asuna system
- [ ] Implement response relevance scorer (query-response matching)
- [ ] Study existing dialogue datasets (MultiWOZ, PersonaChat, DailyDialog)
- [ ] Design evaluation framework for your chatbot
- [ ] Implement retrieval system for unknown queries
- [ ] Experiment with different decoding strategies (greedy, beam search, sampling)
- [ ] Read dialogue system papers and surveys

### Checkpoint
- Can design and train intent classifier with >85% accuracy
- Can implement and evaluate response ranking system
- Understand tradeoffs between different dialogue architectures
- Can critically evaluate existing chatbot systems

---

## Phase 4: Research Implementation (Weeks 27-36)

### Objective
Design and implement custom research architecture for Asuna.

### Research Questions to Explore
1. **Hybrid Architecture**: How to best combine pattern-based rules with neural models?
2. **Context Modeling**: How to effectively use conversation history?
3. **Personalization**: Can the system adapt to individual users?
4. **Uncertainty Handling**: How to detect and handle low-confidence responses?
5. **Multi-task Learning**: Can intent, sentiment, and relevance be learned jointly?

### Implementation Tracks

#### Track A: Neural Intent + Validation Layer
- Design: Pattern matching → BART intent classifier → Response validator
- Experiments:
  - Compare pattern-only vs hybrid performance
  - Ablation studies: what does each component contribute?
  - Error analysis: where does the system fail?

#### Track B: Retrieval-Augmented Response
- Design: Query → Retrieve similar past conversations → Generate/select response
- Experiments:
  - Dense retrieval vs sparse retrieval
  - Optimal retrieval set size
  - Retrieval + pattern fusion strategies

#### Track C: Multi-Task Learning
- Design: Single model predicting intent + sentiment + response quality
- Experiments:
  - Does multi-task help or hurt individual task performance?
  - Optimal loss weighting strategies
  - Transfer learning effects

### Learning Activities
- [ ] Define research questions and hypotheses
- [ ] Design experiments with clear metrics
- [ ] Implement baseline systems for comparison
- [ ] Build data collection and annotation pipeline
- [ ] Implement and train custom architectures
- [ ] Run controlled experiments and analyze results
- [ ] Write technical reports documenting findings
- [ ] Read recent papers from ACL, EMNLP, NeurIPS dialogue tracks

### Checkpoint
- Clear hypothesis-driven research design
- Working implementation with evaluation framework
- Statistical significance testing for experiments
- Documented insights and failure cases

---

## Phase 5: Advanced Research Directions (Weeks 37+)

### Objective
Push boundaries and explore cutting-edge research areas.

### Advanced Topics

#### Robustness & Reliability
- Adversarial examples in NLP
- Out-of-distribution detection
- Calibration of confidence scores
- Stress testing with typos, slang, code-switching

#### Efficient Models
- Knowledge distillation
- Quantization and pruning
- Model compression techniques
- Latency optimization

#### Continual Learning
- Learning from user interactions
- Catastrophic forgetting problem
- Online learning strategies
- Active learning for data collection

#### Explainability
- Attention visualization
- Feature importance analysis
- Decision explanation generation
- User-facing transparency

### Learning Activities
- [ ] Pick one advanced area and go deep
- [ ] Implement state-of-the-art techniques
- [ ] Contribute to research community (papers, blog posts, open source)
- [ ] Iterate on Asuna architecture based on research findings
- [ ] Build unique features not seen in other chatbots

### Checkpoint
- Novel contributions to your chatbot system
- Deep expertise in chosen research area
- Documented experimental results
- Potential for academic publication or technical blog series

---

## Learning Resources

### Books
- "Mathematics for Machine Learning" - Deisenroth, Faisal, Ong
- "Deep Learning" - Goodfellow, Bengio, Courville
- "Natural Language Processing with Transformers" - Tunstall et al.
- "Speech and Language Processing" - Jurafsky & Martin (3rd ed, free online)

### Online Courses
- Fast.ai Practical Deep Learning
- Stanford CS224N: NLP with Deep Learning
- DeepLearning.AI Transformer courses
- Hugging Face NLP course (free)

### Key Papers to Read
- "Attention Is All You Need" (Vaswani et al., 2017)
- "BERT: Pre-training of Deep Bidirectional Transformers" (Devlin et al., 2018)
- "BART: Denoising Sequence-to-Sequence Pre-training" (Lewis et al., 2019)
- Recent dialogue papers from ACL/EMNLP/NAACL

### Coding Practice
- Implement algorithms from scratch before using libraries
- Work through PyTorch tutorials
- Study Hugging Face Transformers source code
- Build progressively complex projects

---

## Success Criteria

### Understanding Level
- Can explain core concepts to others clearly
- Can derive key equations from first principles
- Can read and understand recent research papers
- Can identify good research questions

### Implementation Level
- Can implement models from paper descriptions
- Can debug training issues (vanishing gradients, overfitting, etc.)
- Can design and run controlled experiments
- Can optimize models for inference

### Research Level
- Can formulate novel hypotheses
- Can design rigorous experiments
- Can interpret results and draw conclusions
- Can contribute new ideas to the field

---

## Notes

- **Don't rush fundamentals**: Deep understanding of math and basics will accelerate everything else
- **Implement from scratch first**: Use frameworks only after understanding what they do
- **Read papers actively**: Try to reproduce results, question assumptions
- **Document everything**: Keep research journal of experiments and insights
- **Balance theory and practice**: Alternate between studying and building
- **Stay curious**: Follow recent papers, but focus on understanding over novelty
