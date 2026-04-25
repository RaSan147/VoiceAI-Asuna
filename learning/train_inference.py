"""
INFERENCE & EVALUATION MODULE
==============================

This module handles:
1. Loading trained models for inference
2. Generating responses with different strategies
3. Evaluating model quality with various metrics
4. Comparing model outputs with baselines

INFERENCE CONCEPTS:
===================

DECODING STRATEGIES:

1. GREEDY DECODING
   ================
   At each step, pick the token with highest probability
   
   Step 1: P(token | input) = [0.1, 0.5, 0.2, 0.15, 0.05]
           → Pick token 2 (prob 0.5, highest)
   
   Step 2: P(token | input, token_2) = [0.2, 0.1, 0.3, 0.25, 0.15]
           → Pick token 3 (prob 0.3, highest)
   
   Advantages: Fast, simple
   Disadvantages: Can get stuck in loops, suboptimal outputs
   
   Example problem:
   Input: "write a poem"
   Step 1: "the"
   Step 2: "the"
   Step 3: "the"
   Step 4: "the"  ← Gets stuck repeating!

2. BEAM SEARCH
   =============
   Keep track of multiple hypothesis sequences, prune bad ones
   
   Imagine parallel universes at each step:
   
   Step 1: Top 3 hypotheses
   - Hyp 1: "the" (prob 0.5)
   - Hyp 2: "a" (prob 0.3)
   - Hyp 3: "it" (prob 0.15)
   
   Step 2: Expand each to top 3 next tokens
   - From "the": "beautiful" (0.4), "quick" (0.3), "lazy" (0.2)
   - From "a": "cat" (0.6), "dog" (0.3), "bird" (0.1)
   - From "it": "is" (0.8), "was" (0.15), "runs" (0.05)
   
   Now rank all 9 by combined probability:
   Combined probabilities = P(hyp_i) * P(next_token | hyp_i)
   
   - "the beautiful" = 0.5 * 0.4 = 0.20
   - "a cat" = 0.3 * 0.6 = 0.18
   - "the quick" = 0.5 * 0.3 = 0.15
   - "it is" = 0.15 * 0.8 = 0.12
   - ...
   
   Keep top 3:
   - Hyp 1: "the beautiful" (0.20)
   - Hyp 2: "a cat" (0.18)
   - Hyp 3: "the quick" (0.15)
   
   Step 3: Expand again...
   
   Final output: Highest probability complete sequence
   
   Beam width = k = 3 means "keep top 3 hypotheses"
   
   Advantages: Better quality outputs, balances exploration/exploitation
   Disadvantages: Slower (k times more computation), uses more memory
   
   Trade-off: beam_size=3-5 usually good balance

3. SAMPLING (Temperature)
   =======================
   Instead of picking top token, sample from distribution
   Temperature controls how "confident" the distribution is
   
   Without temperature (greedy):
   prob = [0.5, 0.3, 0.15, 0.05]  → always pick first token
   
   With temperature T:
   new_prob = softmax(logits / T)
   
   T < 1.0 (sharper distribution):
   logits = [2.0, 1.0, 0.5, -1.0]
   T = 0.5: logits/T = [4.0, 2.0, 1.0, -2.0]
   softmax = [0.80, 0.15, 0.04, 0.01]  (very confident)
   
   T = 1.0 (normal):
   logits/T = [2.0, 1.0, 0.5, -1.0]
   softmax = [0.50, 0.30, 0.15, 0.05]  (default)
   
   T > 1.0 (flatter distribution):
   T = 2.0: logits/T = [1.0, 0.5, 0.25, -0.5]
   softmax = [0.38, 0.27, 0.21, 0.14]  (less confident, more uniform)
   
   Use sampling with T=0.7 for more creative/diverse outputs
   Use T=1.0 for standard outputs
   Use T=0.1 for very focused/predictable outputs

EVALUATION METRICS:

1. EXACT MATCH (EM)
   =================
   Did the model output exactly match the correct answer?
   
   Example:
   Expected: "The capital of France is Paris"
   Generated: "The capital of France is Paris"
   → EM = 1 (match)
   
   Generated: "Paris is the capital of France"
   → EM = 0 (different word order, no match)
   
   Problem: Ignores semantic similarity
   Use when: Exact format is critical

2. BLEU SCORE
   ===========
   Measures n-gram overlap between generated and expected
   
   N-grams:
   Sentence: "The cat sat on the mat"
   Unigrams (1-gram): "the", "cat", "sat", "on", "the", "mat"
   Bigrams (2-gram): ["the", "cat"], ["cat", "sat"], ["sat", "on"], ["on", "the"], ["the", "mat"]
   
   Precision for 1-grams:
   Expected: "the cat is cute"
   Generated: "the dog is cute cat"
   
   Count n-grams in generated that appear in expected:
   "the" ✓, "dog" ✗, "is" ✓, "cute" ✓, "cat" ✓
   
   Precision = 4/5 = 0.8
   
   BLEU = weighted_product[precision_1gram, precision_2gram, ...]
   
   Example BLEU scores:
   - BLEU=0.0: No overlap at all
   - BLEU=0.3: Poor translation
   - BLEU=0.5: Acceptable translation
   - BLEU=0.7: Good translation
   - BLEU=0.9: Excellent translation
   
   Problem: Doesn't account for semantics
   "The cat sat on mat" vs "A feline rested upon floor" = low BLEU
   but semantically very similar

3. ROUGE SCORE
   =============
   Similar to BLEU but focuses on recall
   
   Recall = (# n-grams in expected that appear in generated) / (total n-grams in expected)
   
   Example:
   Generated: "the cat is cute"  (4 unigrams)
   Expected: "the cat is very cute"  (5 unigrams)
   
   Recall = 4/5 = 0.80
   
   ROUGE handles synonyms better than BLEU
   "the cat is cute" vs "the feline is cute" = higher ROUGE than BLEU

4. METEOR SCORE
   ==============
   Aligns words between generated and expected, handles synonyms
   
   Generated: "the cat is cute"
   Expected: "the feline is cute"
   
   Alignment:
   "the" → "the" (exact match)
   "cat" → "feline" (synonym match)
   "is" → "is" (exact match)
   "cute" → "cute" (exact match)
   
   Fragmentation penalty: Lower for fewer, larger matched chunks
   
   METEOR = better at capturing semantic similarity

5. SEMANTIC SIMILARITY (BERT Score)
   ==================================
   Compute contextual embeddings for both texts using BERT
   Compare embeddings using cosine similarity
   
   This captures meaning, not just word overlap!
   
   "The cat ate the mouse" 
   BERT embedding: [0.2, -0.1, 0.5, ..., 0.3]  (768 dimensions)
   
   "The rodent was consumed by the feline"
   BERT embedding: [0.21, -0.09, 0.51, ..., 0.31]  (similar!)
   
   Cosine similarity = (v1 · v2) / (||v1|| * ||v2||)
                    = dot_product / (magnitude1 * magnitude2)
   
   Result: 0.0 (completely different) to 1.0 (identical meaning)
   
   Problem: Slow (requires running BERT for each comparison)
   Use when: Need semantic equivalence

CONFUSION MATRIX & PERFORMANCE METRICS:

For classification tasks (predict intent):

                 Predicted Positive    Predicted Negative
Actual Positive   TP (correct ✓)       FN (missed)
Actual Negative   FP (false alarm)     TN (correct ✓)

Accuracy = (TP + TN) / (TP + TN + FP + FN)
           = "How often were we correct?"

Precision = TP / (TP + FP)
            = "Of the times we predicted positive, how often were we right?"
            (relevance to user: avoid false alarms)

Recall = TP / (TP + FN)
         = "Of the actual positives, how many did we catch?"
         (relevance to user: don't miss important cases)

F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
           = harmonic mean of precision and recall
           (balanced metric when precision and recall matter equally)

Example: Spam detection
- Accuracy 95%: Looks good, but might miss lots of spam
- Precision 99%: When we say it's spam, we're usually right (low false alarms)
- Recall 75%: We catch 75% of spam, miss 25%
- Better recall for spam detection (don't let spam through)

Example: Medical diagnosis
- Precision 99%: Don't give false diagnosis (good for reassurance)
- Recall 95%: Catch 95% of actual diseases (critical here!)
- High recall more important (don't miss diseases)
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Dict, List, Tuple, Optional
import numpy as np
import json
from pathlib import Path
import logging
from collections import defaultdict

# Try importing optional evaluation libraries
try:
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _default_best_model_path() -> str:
    return str(Path(__file__).resolve().parent.parent / "src" / "models" / "asuna_seq2seq" / "best_model")


class TransformerInference:
    """
    Generate responses using trained model.
    """
    
    def __init__(self, model_path: str, device: str = None):
        """
        Args:
            model_path: Path to saved model directory
            device: 'cuda' or 'cpu'
        """
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        logger.info(f"Loading model from {model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode
    
    def generate(
        self,
        input_text: str,
        max_length: int = 128,
        min_length: int = 10,
        num_beams: int = 4,
        temperature: float = 1.0,
        top_p: float = 0.95,
        no_repeat_ngram_size: int = 3,
        early_stopping: bool = True,
    ) -> str:
        """
        Generate response with BEAM SEARCH (best quality) or SAMPLING
        
        Args:
            input_text: User query
            max_length: Don't generate beyond this many tokens
            min_length: Minimum tokens to generate
            num_beams: Beam search width (≥2 for beam search, 1 for greedy)
                       Recommendations:
                       - num_beams=1: Fast (greedy), low quality
                       - num_beams=4: Good balance (recommended)
                       - num_beams=8: High quality, slower
            temperature: Sampling temperature (≥0.1)
                        - 0.1: Sharp, repetitive
                        - 0.7: Balanced (recommended)
                        - 1.0: Default
                        - 2.0: Creative, varied
            top_p: Nucleus sampling - only consider top p% probability mass
                   (filter unlikely tokens before sampling)
            no_repeat_ngram_size: Penalty for repeating n-grams
                                  (prevents "the the the the...")
            early_stopping: Stop as soon as [EOS] token generated
        
        Returns:
            Generated response text
        """
        # Tokenize input
        inputs = self.tokenizer(
            input_text,
            max_length=128,
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)
        
        with torch.no_grad():
            # Generate using specified strategy
            generated_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=max_length,
                min_length=min_length,
                num_beams=num_beams,
                temperature=temperature,
                top_p=top_p,
                no_repeat_ngram_size=no_repeat_ngram_size,
                early_stopping=early_stopping,
                do_sample=(num_beams == 1),  # Use sampling only for greedy
            )
        
        # Decode to text
        output_text = self.tokenizer.decode(
            generated_ids[0],
            skip_special_tokens=True
        )
        
        return output_text
    
    def generate_batch(
        self,
        input_texts: List[str],
        **kwargs
    ) -> List[str]:
        """Generate for multiple inputs at once."""
        outputs = []
        for text in input_texts:
            output = self.generate(text, **kwargs)
            outputs.append(output)
        return outputs


class ModelEvaluator:
    """
    Evaluate model quality using various metrics.
    """
    
    def __init__(self, inference: TransformerInference):
        self.inference = inference
        self.results = {
            'exact_match': [],
            'bleu': [],
            'rouge': [],
            'metrics_summary': {}
        }
    
    def exact_match(self, generated: str, expected: str) -> int:
        """
        EXACT MATCH: 1 if strings are identical, 0 otherwise
        
        Mathematical formula:
        EM = 1 if generated == expected else 0
        """
        return 1 if generated.lower() == expected.lower() else 0
    
    def bleu_score(
        self,
        generated: str,
        references: List[str],
        max_n: int = 4
    ) -> float:
        """
        BLEU SCORE: N-gram overlap with reference
        
        Args:
            generated: Model output
            references: List of valid reference outputs
            max_n: Use n-grams up to 1-gram to max_n-gram
        
        Returns:
            BLEU score (0-1 scale, higher is better)
        """
        if not NLTK_AVAILABLE:
            logger.warning("NLTK not installed, skipping BLEU")
            return 0.0
        
        gen_tokens = generated.lower().split()
        ref_tokens_list = [ref.lower().split() for ref in references]
        
        # Weights: equal weight for all n-grams
        weights = tuple([1.0 / max_n] * max_n)
        
        smoothing_function = SmoothingFunction().method1
        
        try:
            bleu = sentence_bleu(
                ref_tokens_list,
                gen_tokens,
                weights=weights,
                smoothing_function=smoothing_function
            )
            return bleu
        except:
            return 0.0
    
    def rouge_score(
        self,
        generated: str,
        expected: str,
        rouge_type: str = 'rouge1'
    ) -> float:
        """
        ROUGE SCORE: Recall-oriented n-gram overlap
        
        Args:
            generated: Model output
            expected: Reference output
            rouge_type: 'rouge1' (unigrams), 'rouge2', 'rouge3', 'rougeL'
        
        Returns:
            F-score (0-1, higher is better)
        """
        if not ROUGE_AVAILABLE:
            logger.warning("rouge_score not installed, skipping ROUGE")
            return 0.0
        
        scorer = rouge_scorer.RougeScorer([rouge_type], use_stemmer=True)
        
        try:
            scores = scorer.score(expected, generated)
            return scores[rouge_type].fmeasure
        except:
            return 0.0
    
    def evaluate_batch(
        self,
        test_pairs: List[Dict[str, str]],
        use_bleu: bool = True,
        use_rouge: bool = True,
        num_beams: int = 4
    ) -> Dict:
        """
        Evaluate model on dataset of input-output pairs.
        
        Args:
            test_pairs: List of {"input": "...", "output": "..."}
            use_bleu: Calculate BLEU score
            use_rouge: Calculate ROUGE score
            num_beams: Beam size for generation
        
        Returns:
            Dictionary with aggregate metrics
        """
        em_scores = []
        bleu_scores = []
        rouge_scores = []
        
        logger.info(f"Evaluating on {len(test_pairs)} examples...")
        
        for pair in test_pairs:
            input_text = pair['input']
            expected = pair['output']
            
            # Generate output
            generated = self.inference.generate(
                input_text,
                num_beams=num_beams
            )
            
            # Calculate metrics
            em = self.exact_match(generated, expected)
            em_scores.append(em)
            
            if use_bleu:
                bleu = self.bleu_score(generated, [expected])
                bleu_scores.append(bleu)
            
            if use_rouge:
                rouge = self.rouge_score(generated, expected)
                rouge_scores.append(rouge)
        
        # Aggregate metrics
        metrics = {
            'exact_match': np.mean(em_scores),
            'exact_match_%': np.mean(em_scores) * 100,
            'num_examples': len(test_pairs)
        }
        
        if bleu_scores:
            metrics['bleu'] = np.mean(bleu_scores)
            metrics['bleu_std'] = np.std(bleu_scores)
        
        if rouge_scores:
            metrics['rouge1'] = np.mean(rouge_scores)
            metrics['rouge1_std'] = np.std(rouge_scores)
        
        logger.info(f"\nEvaluation Results:")
        logger.info(json.dumps(metrics, indent=2))
        
        return metrics


class BaselineComparison:
    """
    Compare model against simple baselines to validate improvement.
    
    BASELINE STRATEGIES:
    ====================
    1. Echo baseline: Return input as-is
    2. Random baseline: Return random response
    3. Most common baseline: Return most frequent training response
    4. Simple pattern rules: Use regex patterns (original system)
    """
    
    def __init__(self, inference: TransformerInference):
        self.inference = inference
        self.most_common_outputs = []
    
    def train_most_common_baseline(self, training_data: List[Dict[str, str]]):
        """Learn most common outputs from training data."""
        from collections import Counter
        outputs = [pair['output'] for pair in training_data]
        outputs_counter = Counter(outputs)
        self.most_common_outputs = [
            output for output, _ in outputs_counter.most_common(10)
        ]
    
    def echo_baseline(self, input_text: str) -> str:
        """Baseline: Echo input as output."""
        return input_text
    
    def most_common_baseline(self) -> str:
        """Baseline: Return most common training output."""
        if not self.most_common_outputs:
            return "I don't know"
        return self.most_common_outputs[0]
    
    def random_baseline(self) -> str:
        """Baseline: Return random response."""
        responses = [
            "I'm not sure",
            "That's interesting",
            "Tell me more",
            "I don't understand",
            "Can you repeat that?"
        ]
        return np.random.choice(responses)
    
    def compare(
        self,
        test_pairs: List[Dict[str, str]],
        evaluator: ModelEvaluator
    ) -> Dict:
        """
        Compare trained model against baselines.
        
        COMPARISON LOGIC:
        =================
        If trained model EM = 45% and baseline EM = 5%,
        then relative improvement = (45 - 5) / 5 = 800%
        
        This validates that the model actually learned something!
        """
        results = {}
        
        # Evaluate trained model
        trained_results = evaluator.evaluate_batch(
            test_pairs,
            num_beams=4
        )
        results['trained_model'] = trained_results
        
        # Evaluate echo baseline
        echo_em = np.mean([
            evaluator.exact_match(
                pair['input'],
                pair['output']
            ) for pair in test_pairs
        ])
        results['echo_baseline'] = {'exact_match': echo_em}
        
        # Calculate improvements
        trained_em = trained_results['exact_match']
        echo_em_val = results['echo_baseline']['exact_match']
        
        if echo_em_val > 0:
            improvement = ((trained_em - echo_em_val) / echo_em_val) * 100
        else:
            improvement = float('inf') if trained_em > 0 else 0
        
        results['improvement'] = {
            'absolute': trained_em - echo_em_val,
            'relative_percent': improvement
        }
        
        logger.info(f"\nBaseline Comparison:")
        logger.info(f"Trained Model EM: {trained_em:.4f}")
        logger.info(f"Echo Baseline EM: {echo_em_val:.4f}")
        logger.info(f"Improvement: {improvement:.1f}%")
        
        return results


# Example usage
if __name__ == "__main__":
    # Load inference
    inference = TransformerInference(_default_best_model_path())
    
    # Generate sample
    response = inference.generate("what is the time?")
    print(f"Response: {response}")
    
    # Evaluate on test set
    evaluator = ModelEvaluator(inference)
    
    test_data = [
        {"input": "hello", "output": "hi there"},
        {"input": "what is your name", "output": "I'm Asuna"},
    ]
    
    metrics = evaluator.evaluate_batch(test_data)
    print(json.dumps(metrics, indent=2))
