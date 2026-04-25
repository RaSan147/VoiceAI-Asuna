"""
TRANSFORMER FALLBACK MODULE
============================

This module integrates the trained transformer model as a fallback
when regex patterns don't match in the chat system.

INTEGRATION ARCHITECTURE:
=========================

Original flow:
  User input → Regex patterns → Match found? → Yes → Bot response
                                              → No → "I don't understand"

New flow with transformer:
  User input → Regex patterns → Match found? → Yes → Bot response
                                            ↓ No
                                            ↓
                              → Transformer model → Confidence high? 
                                                  → Yes → Bot response
                                                  → No → "I don't understand"

CONFIDENCE SCORING:
===================

The transformer produces a probability distribution over the vocabulary.
We use this to estimate confidence in the response.

For each token position in the generated response:
1. Get logits (unnormalized scores) for all 50,265 tokens
2. Take softmax to get probabilities
3. Compute the max probability
4. Average across all token positions

Example:
Position 0: softmax(logits) = [0.45, 0.3, 0.15, 0.1, ...]
           max_prob = 0.45
Position 1: softmax(logits) = [0.5, 0.25, 0.15, 0.1, ...]
           max_prob = 0.5
Position 2: softmax(logits) = [0.35, 0.3, 0.2, 0.15, ...]
           max_prob = 0.35

Average confidence = (0.45 + 0.5 + 0.35) / 3 = 0.433

Interpretation:
- Confidence < 0.3: Model unsure, don't use
- 0.3-0.6: Medium confidence, might use with disclaimer
- 0.6-0.8: Good confidence, use as primary response
- > 0.8: Very confident, high quality response

FALLBACK STRATEGY:
==================

if regex_match_found:
    use_regex_response
elif transformer_confidence > confidence_threshold:
    use_transformer_response
else:
    use_generic_fallback_response

This ensures we only use the transformer when confident,
and fall back to safe responses when uncertain.
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Tuple, Optional, Dict
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransformerFallback:
    """
    Transformer-based fallback for unmatched inputs.
    """
    
    def __init__(
        self,
        model_path: str = "./models/asuna_seq2seq/best_model",
        device: str = None,
        confidence_threshold: float = 0.5,
        enable_logging: bool = True
    ):
        """
        Args:
            model_path: Path to trained transformer model
            device: 'cuda' or 'cpu'
            confidence_threshold: Only use response if confidence > this
                                 Range: 0.0 to 1.0
                                 Recommendation: 0.5 (50% confidence minimum)
            enable_logging: Log when fallback is used
        """
        self.confidence_threshold = confidence_threshold
        self.enable_logging = enable_logging
        self.model_available = False
        self.stats = {
            'fallback_used': 0,
            'confidence_too_low': 0,
            'model_error': 0,
        }
        
        try:
            if device is None:
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            else:
                self.device = torch.device(device)
            
            model_path = Path(model_path)
            
            if not model_path.exists():
                logger.warning(f"Model path does not exist: {model_path}")
                logger.warning("Transformer fallback will be disabled")
                return
            
            logger.info(f"Loading transformer model from {model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(str(model_path))
            self.model = AutoModelForSeq2SeqLM.from_pretrained(str(model_path))
            self.model.to(self.device)
            self.model.eval()
            
            self.model_available = True
            logger.info("✓ Transformer fallback loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load transformer model: {e}")
            self.model_available = False
    
    def generate_with_confidence(
        self,
        input_text: str,
        max_length: int = 128,
        num_beams: int = 4,
        return_probabilities: bool = True
    ) -> Tuple[str, float, Dict]:
        """
        Generate response and estimate confidence.
        
        CONFIDENCE CALCULATION:
        =======================
        
        During generation, the model produces logits for each token.
        Logits are unnormalized scores: some positive, some negative.
        
        Example logits for position 0:
        logits = [2.1, 0.5, -1.2, 1.8, ..., -0.3]  (50,265 values)
        
        Apply softmax to convert to probabilities:
        softmax(logits) = [0.4, 0.2, 0.05, 0.3, ..., 0.05]
        
        The max probability (0.4) indicates how "sure" the model is
        about its top choice.
        
        Args:
            input_text: User query
            max_length: Max output length
            num_beams: Beam search width
            return_probabilities: Return detailed probability info
        
        Returns:
            Tuple of:
            - generated_text: Model's response
            - confidence: Average probability across output tokens (0-1)
            - info: Dict with detailed statistics
        """
        
        if not self.model_available:
            return "", 0.0, {'error': 'model_not_loaded'}
        
        try:
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
                # Generate with output_scores to get probabilities
                outputs = self.model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_length=max_length,
                    num_beams=num_beams,
                    output_scores=True,  # Key: get probability scores
                    return_dict_in_generate=True,
                    do_sample=False,
                    early_stopping=True,
                    no_repeat_ngram_size=3,
                )
            
            # Decode generated tokens
            generated_ids = outputs.sequences[0]
            generated_text = self.tokenizer.decode(
                generated_ids,
                skip_special_tokens=True
            )
            
            # Calculate confidence from scores
            confidence, detailed_probs = self._calculate_confidence(
                outputs.scores,
                return_probabilities
            )
            
            info = {
                'input_length': len(input_ids[0]),
                'output_length': len(generated_ids),
                'confidence': confidence,
                'detailed_probs': detailed_probs if return_probabilities else None,
                'token_count': outputs.__dict__.get('sequences', [output_ids]).__len__() if hasattr(outputs, 'sequences') else 0
            }
            
            return generated_text, confidence, info
            
        except Exception as e:
            logger.error(f"Error during generation: {e}")
            self.stats['model_error'] += 1
            return "", 0.0, {'error': str(e)}
    
    def _calculate_confidence(
        self,
        scores: Tuple[torch.Tensor],
        return_detailed: bool = False
    ) -> Tuple[float, Optional[list]]:
        """
        Calculate confidence from model scores.
        
        MATHEMATICAL DETAIL:
        ====================
        
        scores is a tuple of tensors, one per output position:
        scores[0] = [raw_score_token_0 for all vocab positions]  shape: (batch=1, vocab=50265)
        scores[1] = [raw_score_token_1 for all vocab positions]
        ...
        
        For each position:
        1. Apply softmax: P(token) = exp(score) / sum(exp(all_scores))
        2. Take max probability
        3. Average across positions
        
        Example:
        scores[0] = [5.0, 0.5, -2.0, ...]
        softmax = [0.95, 0.04, 0.001, ...]
        max_prob[0] = 0.95
        
        scores[1] = [3.0, 2.0, 1.0, ...]
        softmax = [0.66, 0.24, 0.09, ...]
        max_prob[1] = 0.66
        
        confidence = (0.95 + 0.66) / 2 = 0.805
        """
        
        token_confidences = []
        
        for token_scores in scores:
            # token_scores: [batch_size, vocab_size]
            # Convert logits to probabilities
            probs = F.softmax(token_scores, dim=-1)
            
            # Get max probability for this position
            max_prob = torch.max(probs, dim=-1)[0]
            token_confidences.append(max_prob.item())
        
        # Average confidence across all tokens
        avg_confidence = sum(token_confidences) / len(token_confidences) if token_confidences else 0.0
        
        return avg_confidence, token_confidences if return_detailed else None
    
    def should_use_response(self, confidence: float) -> bool:
        """
        Determine if we should use the transformer response.
        
        Decision logic:
        - If confidence > threshold: Use response
        - Otherwise: Fall back to safe default
        """
        return confidence >= self.confidence_threshold
    
    def get_response(
        self,
        input_text: str,
        fallback_response: str = "I'm not sure about that. Could you rephrase?"
    ) -> Tuple[str, Dict]:
        """
        Get response with fallback logic.
        
        Args:
            input_text: User query
            fallback_response: Response to use if confidence too low
        
        Returns:
            Tuple of (response_text, metadata)
        """
        
        if not self.model_available:
            return fallback_response, {'source': 'fallback_not_available'}
        
        # Generate with confidence
        generated, confidence, info = self.generate_with_confidence(input_text)
        
        # Check if we should use it
        if self.should_use_response(confidence):
            self.stats['fallback_used'] += 1
            
            if self.enable_logging:
                logger.info(f"Transformer response (confidence={confidence:.3f}): {generated[:50]}...")
            
            return generated, {
                'source': 'transformer',
                'confidence': confidence,
                'info': info
            }
        else:
            self.stats['confidence_too_low'] += 1
            
            if self.enable_logging:
                logger.info(f"Confidence too low ({confidence:.3f}), using fallback")
            
            return fallback_response, {
                'source': 'fallback_low_confidence',
                'confidence': confidence,
                'threshold': self.confidence_threshold
            }
    
    def adjust_confidence_threshold(self, new_threshold: float):
        """
        Adjust confidence threshold for safety vs utility trade-off.
        
        THRESHOLD TUNING:
        =================
        
        Threshold too low (e.g., 0.1):
        - Pros: Uses transformer often
        - Cons: Low quality responses, weird behavior
        
        Threshold = 0.3:
        - Uses transformer 70% of the time
        - Moderate quality
        
        Threshold = 0.5:
        - Uses transformer 30% of the time
        - Higher quality
        - More fallback usage (recommended)
        
        Threshold = 0.8:
        - Uses transformer rarely
        - Very high quality when used
        - Mostly falls back
        - Might waste trained model
        
        Strategy: Start at 0.5, monitor logs, tune based on results
        """
        if not (0.0 <= new_threshold <= 1.0):
            logger.warning(f"Threshold must be 0-1, got {new_threshold}")
            return
        
        old_threshold = self.confidence_threshold
        self.confidence_threshold = new_threshold
        logger.info(f"Confidence threshold adjusted: {old_threshold:.2f} → {new_threshold:.2f}")
    
    def get_stats(self) -> Dict:
        """Get usage statistics for debugging."""
        return {
            'model_available': self.model_available,
            'confidence_threshold': self.confidence_threshold,
            'stats': self.stats,
            'total_uses': sum(self.stats.values())
        }
    
    def print_stats(self):
        """Print stats in readable format."""
        stats = self.get_stats()
        logger.info("\n" + "="*60)
        logger.info("TRANSFORMER FALLBACK STATISTICS")
        logger.info("="*60)
        logger.info(f"Model available: {stats['model_available']}")
        logger.info(f"Confidence threshold: {stats['confidence_threshold']:.2f}")
        logger.info(f"\nUsage:")
        logger.info(f"  Fallback used: {stats['stats']['fallback_used']}")
        logger.info(f"  Confidence too low: {stats['stats']['confidence_too_low']}")
        logger.info(f"  Model errors: {stats['stats']['model_error']}")
        logger.info(f"  Total uses: {stats['total_uses']}")


# ============================================================================
# INTEGRATION EXAMPLE
# ============================================================================

def example_integration():
    """
    Example of how to use this in Chat_raw2.py
    """
    
    # In Chat_raw2.py, at module initialization:
    fallback = TransformerFallback(
        model_path="./models/asuna_seq2seq/best_model",
        confidence_threshold=0.5,
        enable_logging=True
    )
    
    # In the main chat function, when no regex pattern matches:
    def basic_output(user_input, user):
        # ... existing regex patterns ...
        
        # If no pattern matches:
        if not matched:
            # Try transformer fallback
            response, metadata = fallback.get_response(
                user_input,
                fallback_response="I'm not sure about that. Could you rephrase?"
            )
            
            # Optional: adjust confidence based on user feedback
            # (store in database to improve over time)
            
            return response, metadata
    
    # Periodically check statistics
    # fallback.print_stats()


if __name__ == "__main__":
    # Test the fallback system
    print("Testing Transformer Fallback System\n")
    
    fallback = TransformerFallback(
        model_path="./models/asuna_seq2seq/best_model",
        confidence_threshold=0.5
    )
    
    if fallback.model_available:
        test_queries = [
            "what is your name",
            "hello there",
            "how are you feeling today",
            "tell me something interesting"
        ]
        
        for query in test_queries:
            response, metadata = fallback.get_response(query)
            print(f"Q: {query}")
            print(f"A: {response}")
            print(f"Confidence: {metadata.get('confidence', 'N/A'):.3f}")
            print(f"Source: {metadata.get('source')}")
            print()
        
        fallback.print_stats()
    else:
        print("Model not available. Please train first:")
        print("  python train_quickstart.py")
