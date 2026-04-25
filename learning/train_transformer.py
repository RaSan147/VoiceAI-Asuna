"""
TRANSFORMER FINE-TUNING TRAINER
================================

This module implements transformer-based sequence-to-sequence training
with detailed mathematical explanations.

ARCHITECTURE OVERVIEW:
======================

We use a pre-trained BART (Denoising Autoencoder) model from HuggingFace.
BART is a transformer architecture with:
- Encoder: Processes input text
- Decoder: Generates output text
- Both use self-attention and feed-forward layers

MATHEMATICAL FOUNDATION:

1. TOKENIZATION & EMBEDDINGS
   ===========================
   User input: "what is the time"
   
   Step 1: Split into tokens
   [CLS] what is the time [SEP]
    0     1    2   3   4    5
   
   Step 2: Convert to token IDs (vocabulary lookup)
   [101, 2054, 2003, 1996, 2051, 102]
   
   Step 3: Create embeddings (768-dimensional vectors in BART)
   Each token becomes a dense vector in embedding space:
   token_embedding(101) = [0.2, -0.1, 0.5, ..., 0.3]  (768 values)
   
   These embeddings capture semantic meaning. Similar words have similar embeddings.

2. POSITIONAL ENCODING
   ====================
   Problem: "The dog bit the cat" vs "The cat bit the dog"
   Without position info, attention sees only word meanings, not order.
   
   Solution: Add positional information to embeddings
   
   position_encoding(pos, 2i) = sin(pos / 10000^(2i/d))
   position_encoding(pos, 2i+1) = cos(pos / 10000^(2i/d))
   
   where:
   - pos = token position (0, 1, 2, ...)
   - i = dimension index
   - d = embedding dimension (768)
   
   Example for position 0:
   PE(0, 0) = sin(0 / 10000^0) = 0
   PE(0, 1) = cos(0 / 10000^0) = 1
   
   Example for position 1:
   PE(1, 0) = sin(1 / 10000^(2*0/768)) = sin(1) ≈ 0.841
   PE(1, 1) = cos(1 / 10000^(2*1/768)) ≈ 0.540
   
   These create unique position "signatures" that the model learns to use.

3. SELF-ATTENTION MECHANISM
   =========================
   This is the core innovation of transformers!
   
   For each token, compute:
   - Query (Q): "What am I looking for?"
   - Key (K): "What information do I have?"
   - Value (V): "What should I pass on?"
   
   Attention = softmax(Q @ K^T / √d_k) @ V
   
   Detailed breakdown:
   
   a) Query, Key, Value projection:
      Q = X @ W_q  (X is input, W_q is learned weight matrix)
      K = X @ W_k
      V = X @ W_v
      
      Dimensions:
      X: [batch_size=32, seq_len=10, d_model=768]
      W_q, W_k, W_v: [d_model=768, d_k=64] (for 12 attention heads)
      Q, K, V: [32, 10, 64]
   
   b) Compute attention scores:
      scores = Q @ K^T / √d_k
      
      Example with 2 tokens, d_k=64:
      Q = [[0.1, -0.3, 0.2, ...], [0.4, 0.1, -0.1, ...]]  (2 x 64)
      K = [[0.2, -0.1, 0.3, ...], [0.3, 0.2, 0.1, ...]]   (2 x 64)
      
      K^T shape: (64 x 2)
      scores = Q @ K^T produces (2 x 2) matrix:
      [
        [q1·k1, q1·k2],  # attention of token 1 to tokens 1,2
        [q2·k1, q2·k2]   # attention of token 2 to tokens 1,2
      ]
      
      Divide by √64 = 8 to control gradient flow
      scores = scores / 8
   
   c) Apply softmax to normalize:
      attention_weights = softmax(scores, dim=-1)
      
      softmax(x_i) = e^x_i / Σ(e^x_j)
      
      Example:
      scores = [[3.0, 1.0]]
      e^3.0 = 20.09
      e^1.0 = 2.72
      softmax = [20.09 / (20.09 + 2.72), 2.72 / (20.09 + 2.72)]
              = [0.88, 0.12]
      
      This means: 88% attention to token 1, 12% to token 2
   
   d) Apply to values:
      output = attention_weights @ V
      
      Continuing example:
      V = [[0.5, 0.1, ...], [0.3, 0.4, ...]]  (2 x 64)
      output = [0.88, 0.12] @ V = 0.88*v1 + 0.12*v2
      
      Result: weighted combination of values, focused on relevant tokens

4. MULTI-HEAD ATTENTION
   =====================
   Instead of one attention mechanism, use 12 in parallel (BART has 12 heads)
   
   Each head has different Q, K, V projections:
   head_i = Attention(Q_i, K_i, V_i)
   
   head_1 might learn syntactic patterns (noun-verb relationships)
   head_2 might learn semantic patterns (word meaning relationships)
   head_3 might learn positional patterns (which words are nearby)
   etc.
   
   Concatenate all heads:
   MultiHead(Q, K, V) = Concat(head_1, ..., head_12) @ W_o
   
   where W_o is a learned output projection

5. FEED-FORWARD NETWORK
   =====================
   After attention, apply:
   FFN(x) = ReLU(x @ W_1 + b_1) @ W_2 + b_2
   
   Typical dimensions in BART:
   x: [batch_size=32, seq_len=10, d_model=768]
   W_1: [768, 3072]  (expansion to 4x)
   W_2: [3072, 768]  (project back)
   
   ReLU(x) = max(0, x) - introduces non-linearity
   
   This allows the model to learn complex non-linear transformations.

6. LAYER NORMALIZATION & RESIDUAL CONNECTIONS
   ============================================
   
   Residual connection:
   output = attention(x) + x
   
   Why? Allows gradients to flow directly: ∂loss/∂x can use direct path
   
   Layer norm:
   normalized = (x - mean(x)) / sqrt(var(x) + ε)
   scaled = normalized * γ + β  (learned scale and shift)
   
   Why? Stabilizes training by keeping activations in reasonable range

7. TRAINING OBJECTIVE - CROSS-ENTROPY LOSS
   ========================================
   
   Goal: Predict next token given previous tokens
   
   For each position in output sequence:
   predicted = model(input, previous_tokens)  # shape: [batch_size, vocab_size]
   
   actual_next_token_id = 5042  (e.g., "hello")
   
   Cross-entropy loss for one example:
   loss = -log(predicted[5042])
   
   Why -log?
   - If predicted[5042] = 0.9 (confident and correct)
     loss = -log(0.9) ≈ 0.105 (small loss, good!)
   
   - If predicted[5042] = 0.1 (uncertain, wrong)
     loss = -log(0.1) ≈ 2.303 (large loss, bad!)
   
   - If predicted[5042] = 0.5 (uncertain)
     loss = -log(0.5) ≈ 0.693 (medium loss)
   
   Total batch loss:
   batch_loss = mean(loss_1, loss_2, ..., loss_32)
   
   Gradient descent updates parameters to minimize this loss.

8. BACKPROPAGATION CHAIN
   ======================
   
   loss → decoder_output → attention → embeddings → encoder
   
   For each parameter:
   ∂loss/∂param = (∂loss/∂output) * (∂output/∂attention) * ... * (∂attention/∂param)
   
   Transformers have many layers (12 encoder, 12 decoder in BART),
   so gradients must flow through 24 layers.
   
   This is where residual connections help - they provide shortcuts.

9. OPTIMIZATION - ADAM OPTIMIZER
   ==============================
   
   Standard gradient descent:
   param := param - learning_rate * gradient
   
   Adam is adaptive learning rate:
   m_t = β_1 * m_(t-1) + (1 - β_1) * gradient   (momentum)
   v_t = β_2 * v_(t-1) + (1 - β_2) * gradient^2 (velocity)
   
   m_hat = m_t / (1 - β_1^t)  (bias correction)
   v_hat = v_t / (1 - β_2^t)  (bias correction)
   
   param := param - learning_rate * m_hat / (sqrt(v_hat) + ε)
   
   Default values (used in training):
   β_1 = 0.9 (momentum decay)
   β_2 = 0.999 (velocity decay)
   ε = 1e-8 (numerical stability)

10. PERPLEXITY METRIC
    ==================
    
    Perplexity = e^(average_cross_entropy_loss)
    
    Interpretation:
    - Perplexity 1.0: Model perfectly predicts (loss = 0)
    - Perplexity 2.0: Model confused between roughly 2 options
    - Perplexity 10.0: Model confused between roughly 10 options
    - Perplexity 100.0: Model very confused
    
    Lower perplexity = better model

TRAINING PROCESS:
==================
1. Load batch of examples (e.g., 32 input-output pairs)
2. Tokenize inputs and outputs
3. Forward pass through encoder-decoder
4. Compute loss on output predictions
5. Backward pass - compute gradients for all parameters
6. Update all parameters using Adam optimizer
7. Repeat for next batch
8. Periodically evaluate on validation set
9. Save best model checkpoint
"""

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import get_linear_schedule_with_warmup
from torch.optim import AdamW
import json
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import numpy as np
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _default_output_dir() -> str:
    return str(Path(__file__).resolve().parent.parent / "src" / "models" / "asuna_seq2seq")


def _default_train_val_jsonl() -> Tuple[str, str]:
    base = Path(__file__).resolve().parent.parent / "src" / "Asuna_data" / "server"
    return str(base / "train.jsonl"), str(base / "val.jsonl")


class TrainingDatasetTokenized(Dataset):
    """
    PyTorch Dataset for tokenized examples.
    
    This handles:
    - Loading JSONL file
    - Tokenizing input/output text
    - Creating attention masks
    - Padding sequences (mathematical detail below)
    """
    
    def __init__(self, jsonl_path: str, tokenizer, max_length: int = 128):
        """
        Args:
            jsonl_path: Path to file with one JSON per line
            tokenizer: HuggingFace tokenizer (e.g., BartTokenizer)
            max_length: Maximum sequence length in tokens
                       (longer sequences are truncated, shorter are padded)
        """
        self.examples = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                example = json.loads(line)
                self.examples.append(example)
        
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        input_text = example['input_text']
        output_text = example['output_text']
        
        # TOKENIZATION FOR ENCODER (input)
        # ================================
        # "what is the time?" → After tokenization:
        # tokens: [bos_id, 2054, 2003, 1996, 2051, 30, eos_id]
        #         where 2054 = "what", 2003 = "is", etc.
        #
        # Truncate if longer than max_length
        # If longer: ["a","b","c","d","e"] → max_len=3 → ["a","b","c"]
        
        inputs = self.tokenizer(
            input_text,
            max_length=self.max_length,
            truncation=True,  # Truncate if too long
            padding='max_length',  # Pad shorter sequences
            return_tensors='pt'
        )
        
        # PADDING MATHEMATICAL CONCEPT:
        # If sequence is shorter than max_length:
        # Original: [101, 2054, 2003, 102]  (length 4)
        # Padded:   [101, 2054, 2003, 102, 0, 0, 0, 0]  (length 8, padded with 0)
        #
        # Attention mask: [1, 1, 1, 1, 0, 0, 0, 0]
        # This tells the model: "Pay attention to first 4 tokens, ignore padding"
        #
        # Without mask, padding tokens would affect attention calculations:
        # attention_weights for token 1 might be influenced by padding (0s)
        # This is incorrect - padding should be invisible to the model
        
        # TOKENIZATION FOR DECODER (output)
        # =================================
        labels = self.tokenizer(
            output_text,
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        
        # Copy labels and replace padding (0) with -100 (ignore in loss)
        # This ensures padding doesn't contribute to training loss:
        # loss = mean([loss_for_real_tokens only])
        # Padding token losses (marked -100) are automatically ignored by PyTorch
        labels['input_ids'][labels['input_ids'] == self.tokenizer.pad_token_id] = -100
        
        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': labels['input_ids'].squeeze(),
            'decoder_attention_mask': labels['attention_mask'].squeeze(),
        }


class TransformerTrainer:
    """
    Trainer for fine-tuning a BART model on input-output pairs.
    """
    
    def __init__(
        self,
        model_name: str = "facebook/bart-base",
        device: str = None,
        output_dir: Optional[str] = None,
    ):
        """
        Args:
            model_name: HuggingFace model ID
            device: 'cuda' or 'cpu'
            output_dir: Directory to save checkpoints
        """
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        logger.info(f"Using device: {self.device}")
        
        self.model_name = model_name
        out = output_dir if output_dir is not None else _default_output_dir()
        self.output_dir = Path(out)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load pretrained model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.model.to(self.device)
        
        self.training_stats = {
            'losses': [],
            'perplexities': [],
            'learning_rates': [],
        }
    
    def create_data_loaders(
        self,
        train_path: str,
        val_path: str,
        batch_size: int = 32,
        max_length: int = 128
    ) -> Tuple[DataLoader, DataLoader]:
        """
        Create PyTorch DataLoaders for training and validation.
        
        BATCH PROCESSING CONCEPT:
        Instead of updating parameters after each example (slow),
        we process 32 examples at once and compute average loss:
        
        batch_loss = mean([loss_ex1, loss_ex2, ..., loss_ex32])
        
        Advantages:
        1. More stable gradients (averaging reduces noise)
        2. Faster (can parallelize across GPU cores)
        3. Better generalization (noise in gradients acts as regularization)
        """
        train_dataset = TrainingDatasetTokenized(train_path, self.tokenizer, max_length)
        val_dataset = TrainingDatasetTokenized(val_path, self.tokenizer, max_length)
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=0  # Set to 0 on Windows, can use >0 on Linux
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0
        )
        
        return train_loader, val_loader
    
    def compute_loss(self, batch: Dict) -> torch.Tensor:
        """
        Compute cross-entropy loss for a batch.
        
        MATHEMATICAL DETAIL:
        =====================
        model(input) outputs logits: [batch_size=32, seq_len=10, vocab_size=50265]
        
        Each position has a distribution over vocabulary:
        logits[0, 0, :] = [0.1, -0.5, 0.3, ..., 0.2]  (50265 values)
        
        These represent unnormalized log probabilities.
        
        Target: labels[0, 0] = 5042 (index of word "hello")
        
        Cross-entropy loss:
        loss = -log(softmax(logits[0, 0, :])[5042])
        
        Or more efficiently (log-sum-exp trick):
        loss = log(Σ_j exp(logits[0, 0, j])) - logits[0, 0, 5042]
        
        This is numerically stable and fast.
        
        PyTorch's CrossEntropyLoss does this automatically.
        It also ignores positions with label = -100 (padding)
        """
        input_ids = batch['input_ids'].to(self.device)
        attention_mask = batch['attention_mask'].to(self.device)
        labels = batch['labels'].to(self.device)
        
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
            return_dict=True
        )
        
        # outputs.loss is the cross-entropy loss computed by the model
        return outputs.loss
    
    def train_epoch(
        self,
        train_loader: DataLoader,
        optimizer,
        scheduler,
        epoch: int
    ) -> float:
        """
        Train for one epoch.
        
        EPOCH CONCEPT:
        One epoch = model sees all training data once
        If dataset has 7000 examples and batch_size = 32:
        Number of batches = ceil(7000 / 32) = 219 batches per epoch
        
        Typical training: 3-10 epochs
        """
        self.model.train()
        total_loss = 0
        num_batches = 0
        
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}")
        
        for batch_idx, batch in enumerate(progress_bar):
            # FORWARD PASS
            # Takes batch through entire model, computes loss
            loss = self.compute_loss(batch)
            
            # BACKWARD PASS
            # Compute gradients: ∂loss/∂param for all parameters
            optimizer.zero_grad()  # Clear old gradients
            loss.backward()  # Compute new gradients
            
            # GRADIENT CLIPPING (optional but recommended)
            # Prevents "exploding gradients" where gradients become NaN
            # Theory: if ||gradient|| > max_norm, scale it down
            # After clipping: ||gradient|| ≤ max_norm
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            # PARAMETER UPDATE
            # param := param - learning_rate * gradient (with Adam's adaptive scaling)
            optimizer.step()
            
            # Update learning rate according to schedule
            # (if learning_rate should decrease over time)
            scheduler.step()
            
            total_loss += loss.item()
            num_batches += 1
            
            current_lr = scheduler.get_last_lr()[0]
            progress_bar.set_postfix({
                'loss': loss.item(),
                'avg_loss': total_loss / num_batches,
                'lr': current_lr
            })
        
        avg_loss = total_loss / num_batches
        self.training_stats['losses'].append(avg_loss)
        
        return avg_loss
    
    def evaluate(self, val_loader: DataLoader) -> Dict:
        """
        Evaluate on validation set.
        
        VALIDATION CONCEPT:
        =====================
        Training loss might decrease indefinitely (overfitting),
        but validation loss indicates true generalization.
        
        Early stopping strategy:
        - If val_loss doesn't improve for N epochs, stop training
        - Save checkpoint with best val_loss
        - Return that checkpoint instead of final model
        
        This prevents overfitting:
        Fig: overfitting_curve
        
        train_loss: ↓ ↓ ↓ ↓ ↓ ↓  (keeps decreasing)
        val_loss:   ↓ ↓ ↓ ↑ ↑ ↑  (increases after epoch 3)
                        ↑ best
        """
        self.model.eval()
        total_loss = 0
        num_batches = 0
        
        with torch.no_grad():  # Don't compute gradients during eval
            for batch in tqdm(val_loader, desc="Evaluating"):
                loss = self.compute_loss(batch)
                total_loss += loss.item()
                num_batches += 1
        
        avg_loss = total_loss / num_batches
        
        # PERPLEXITY CALCULATION
        # perplexity = e^loss
        # Interpretation: "effective vocabulary size the model is confused about"
        perplexity = np.exp(avg_loss)
        
        self.training_stats['perplexities'].append(perplexity)
        
        logger.info(f"Validation - Loss: {avg_loss:.4f}, Perplexity: {perplexity:.4f}")
        
        return {
            'loss': avg_loss,
            'perplexity': perplexity
        }
    
    def train(
        self,
        train_path: str,
        val_path: str,
        num_epochs: int = 3,
        batch_size: int = 32,
        learning_rate: float = 5e-5,
        max_length: int = 128,
        early_stopping_patience: int = 2
    ):
        """
        Complete training loop.
        
        HYPERPARAMETER MEANINGS:
        ========================
        - learning_rate = 5e-5: Step size for parameter updates
          Too high: Training unstable, loss increases
          Too low: Training slow, might get stuck
          For fine-tuning pretrained models: usually 1e-5 to 5e-5
        
        - batch_size = 32: How many examples per update
          Larger batches: More stable gradients, faster, but less frequent updates
          Smaller batches: Noisier gradients, slower, but more frequent updates
        
        - num_epochs = 3: How many times to see entire dataset
          More epochs: Better fit, but risk of overfitting
          Fewer epochs: Faster training, but might underfit
        
        - warmup_steps = 500: Gradually increase learning rate at start
          Why? Pretrained model starts with good weights, small LR helps
          Warmup: if total_steps = 5000
                  LR(0) = 0 (no updates yet)
                  LR(100) = 0.1 * 5e-5 (10% of full LR)
                  LR(500) = 5e-5 (full LR)
                  LR(5000) = 0 (linear decay to 0)
        """
        # Create data loaders
        train_loader, val_loader = self.create_data_loaders(
            train_path, val_path, batch_size, max_length
        )
        
        # Setup optimizer
        optimizer = AdamW(self.model.parameters(), lr=learning_rate)
        
        # Setup learning rate scheduler
        total_steps = len(train_loader) * num_epochs
        warmup_steps = min(500, total_steps // 10)  # 10% warmup
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps=total_steps
        )
        
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(num_epochs):
            logger.info(f"\n{'='*60}")
            logger.info(f"Epoch {epoch+1}/{num_epochs}")
            logger.info(f"{'='*60}")
            
            # Train
            train_loss = self.train_epoch(train_loader, optimizer, scheduler, epoch)
            logger.info(f"Training Loss: {train_loss:.4f}")
            
            # Evaluate
            val_metrics = self.evaluate(val_loader)
            
            # Early stopping logic
            if val_metrics['loss'] < best_val_loss:
                best_val_loss = val_metrics['loss']
                patience_counter = 0
                
                # Save best checkpoint
                self.save_model(f"best_model")
                logger.info(f"✓ Saved best model (loss: {best_val_loss:.4f})")
            else:
                patience_counter += 1
                if patience_counter >= early_stopping_patience:
                    logger.info(f"\nEarly stopping after {epoch+1} epochs")
                    logger.info(f"Best validation loss: {best_val_loss:.4f}")
                    break
        
        # Save final model
        self.save_model("final_model")
        logger.info("\n✓ Training complete!")
    
    def save_model(self, name: str):
        """Save model checkpoint."""
        save_path = self.output_dir / name
        save_path.mkdir(parents=True, exist_ok=True)
        
        self.model.save_pretrained(str(save_path))
        self.tokenizer.save_pretrained(str(save_path))
        
        logger.info(f"Model saved to {save_path}")
    
    def save_training_stats(self):
        """Save training statistics for analysis."""
        stats_path = self.output_dir / "training_stats.json"
        
        with open(stats_path, 'w') as f:
            json.dump(self.training_stats, f, indent=2)
        
        logger.info(f"Training stats saved to {stats_path}")


# Example usage
if __name__ == "__main__":
    _tp, _vp = _default_train_val_jsonl()
    trainer = TransformerTrainer(
        model_name="facebook/bart-base",
    )
    
    trainer.train(
        train_path=_tp,
        val_path=_vp,
        num_epochs=3,
        batch_size=32,
        learning_rate=5e-5,
        max_length=128,
        early_stopping_patience=2
    )
    
    trainer.save_training_stats()
