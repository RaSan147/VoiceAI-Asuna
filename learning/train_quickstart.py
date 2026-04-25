"""
QUICK-START TRAINING SCRIPT
============================

This script runs the complete training pipeline in one go:
1. Prepare data (load, clean, split)
2. Train transformer model
3. Evaluate on test set
4. Save final model

Usage:
    python train_quickstart.py

Requirements:
    pip install torch transformers datasets

Configuration:
    Modify the config dict below to customize training
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from train_data_prep import TrainingDataset
from train_transformer import TransformerTrainer
from train_inference import TransformerInference, ModelEvaluator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _src_data_server_dir() -> str:
    return str(_REPO_ROOT / "src" / "Asuna_data" / "server") + os.sep


def _src_models_seq2seq_dir() -> str:
    return str(_REPO_ROOT / "src" / "models" / "asuna_seq2seq")


# ============================================================================
# CONFIGURATION - MODIFY THESE VALUES
# ============================================================================

CONFIG = {
    # Data paths (under repo src/; safe when running from learning/)
    'data_dir': _src_data_server_dir(),
    'unknown_queries_file': 'unknown query.txt',
    'manual_training_file': 'example_training_data.json',  # Optional
    
    # Data split ratios
    'train_ratio': 0.7,
    'val_ratio': 0.15,
    'test_ratio': 0.15,
    
    # Model config
    'model_name': 'facebook/bart-base',  # Other options: 'facebook/bart-large', 't5-base'
    'output_dir': _src_models_seq2seq_dir(),
    'device': 'cuda',  # or 'cpu'
    
    # Training hyperparameters
    'num_epochs': 3,
    'batch_size': 16,  # Reduce if out of memory (8, 4)
    'learning_rate': 5e-5,
    'max_length': 128,
    'warmup_ratio': 0.1,
    
    # Early stopping
    'early_stopping_patience': 2,  # Stop if val loss doesn't improve for N epochs
    
    # Inference config
    'num_beams': 4,  # Beam search width (higher = better quality, slower)
}


# ============================================================================
# STEP 1: PREPARE DATA
# ============================================================================

def prepare_data(config):
    """
    Load, clean, and split training data.
    
    This step:
    - Loads unknown queries from logs
    - Optionally loads manually labeled data
    - Removes duplicates
    - Analyzes statistics
    - Splits into train/val/test
    - Saves as JSONL files
    """
    logger.info("\n" + "="*70)
    logger.info("STEP 1: PREPARING DATA")
    logger.info("="*70)
    
    # Initialize dataset manager
    dataset = TrainingDataset(data_dir=config['data_dir'])
    
    # Load data from unknown queries
    logger.info("Loading unknown queries...")
    loaded_unknown = dataset.load_unknown_queries(config['unknown_queries_file'])
    
    # Optionally load manually labeled training data
    if os.path.exists(os.path.join(config['data_dir'], config['manual_training_file'])):
        logger.info("Loading manual training data...")
        loaded_manual = dataset.load_manual_training_data(config['manual_training_file'])
    else:
        logger.info(f"Manual training file not found: {config['manual_training_file']}")
        loaded_manual = 0
    
    total_loaded = loaded_unknown + loaded_manual
    
    if total_loaded == 0:
        logger.error("No training data loaded! Check file paths.")
        return None
    
    logger.info(f"Total examples loaded: {total_loaded}")
    
    # Clean data
    logger.info("Cleaning data...")
    removed = dataset.remove_duplicates()
    
    # Analyze statistics
    logger.info("Calculating statistics...")
    dataset.calculate_statistics()
    
    # Split data
    logger.info("Splitting data...")
    train, val, test = dataset.train_val_test_split(
        train_ratio=config['train_ratio'],
        val_ratio=config['val_ratio'],
        test_ratio=config['test_ratio']
    )
    
    # Save splits
    logger.info("Saving data splits...")
    dataset.save_all_splits(train, val, test)
    
    return train, val, test


# ============================================================================
# STEP 2: TRAIN MODEL
# ============================================================================

def train_model(config, train, val):
    """
    Train transformer model on prepared data.
    
    This step:
    - Initializes BART model
    - Creates data loaders
    - Trains with Adam optimizer
    - Validates on each epoch
    - Saves best checkpoint
    - Early stops if needed
    """
    logger.info("\n" + "="*70)
    logger.info("STEP 2: TRAINING MODEL")
    logger.info("="*70)
    
    # Initialize trainer
    trainer = TransformerTrainer(
        model_name=config['model_name'],
        device=config['device'],
        output_dir=config['output_dir']
    )
    
    # Train
    logger.info("Starting training loop...")
    train_path = os.path.join(config['data_dir'], 'train.jsonl')
    val_path = os.path.join(config['data_dir'], 'val.jsonl')
    
    trainer.train(
        train_path=train_path,
        val_path=val_path,
        num_epochs=config['num_epochs'],
        batch_size=config['batch_size'],
        learning_rate=config['learning_rate'],
        max_length=config['max_length'],
        early_stopping_patience=config['early_stopping_patience']
    )
    
    # Save stats
    trainer.save_training_stats()
    
    return trainer


# ============================================================================
# STEP 3: EVALUATE MODEL
# ============================================================================

def evaluate_model(config, test):
    """
    Evaluate trained model on test set.
    
    This step:
    - Loads best model checkpoint
    - Generates responses for test examples
    - Calculates evaluation metrics (EM, BLEU, ROUGE)
    - Compares against baselines
    """
    logger.info("\n" + "="*70)
    logger.info("STEP 3: EVALUATING MODEL")
    logger.info("="*70)
    
    # Load best model
    best_model_path = os.path.join(config['output_dir'], 'best_model')
    
    if not os.path.exists(best_model_path):
        logger.error(f"Best model not found at {best_model_path}")
        return None
    
    logger.info(f"Loading model from {best_model_path}")
    inference = TransformerInference(best_model_path, device=config['device'])
    
    # Create evaluator
    evaluator = ModelEvaluator(inference)
    
    # Convert test data to dict format
    test_pairs = [
        {'input': ex.input_text, 'output': ex.output_text}
        for ex in test
    ]
    
    # Evaluate
    logger.info(f"Evaluating on {len(test_pairs)} test examples...")
    metrics = evaluator.evaluate_batch(
        test_pairs,
        use_bleu=True,
        use_rouge=True,
        num_beams=config['num_beams']
    )
    
    return inference, metrics


# ============================================================================
# STEP 4: GENERATE SAMPLE RESPONSES
# ============================================================================

def generate_samples(inference, config):
    """Generate sample responses to see model in action."""
    logger.info("\n" + "="*70)
    logger.info("STEP 4: SAMPLE RESPONSES")
    logger.info("="*70)
    
    sample_queries = [
        "hello",
        "what is your name",
        "how are you",
        "tell me a joke",
        "what can you do"
    ]
    
    logger.info("Generating sample responses...\n")
    
    for query in sample_queries:
        response = inference.generate(
            query,
            num_beams=config['num_beams'],
            max_length=128
        )
        logger.info(f"Q: {query}")
        logger.info(f"A: {response}\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run complete training pipeline."""
    
    logger.info("\n")
    logger.info("╔" + "═"*68 + "╗")
    logger.info("║" + "ASUNA TRANSFORMER TRAINING PIPELINE".center(68) + "║")
    logger.info("╚" + "═"*68 + "╝")
    logger.info(f"\nConfiguration:")
    for key, value in CONFIG.items():
        logger.info(f"  {key}: {value}")
    
    try:
        # Step 1: Prepare data
        result = prepare_data(CONFIG)
        if result is None:
            logger.error("Data preparation failed!")
            return False
        train, val, test = result
        
        # Step 2: Train model
        trainer = train_model(CONFIG, train, val)
        
        # Step 3: Evaluate model
        result = evaluate_model(CONFIG, test)
        if result is None:
            logger.error("Evaluation failed!")
            return False
        inference, metrics = result
        
        # Step 4: Generate samples
        generate_samples(inference, CONFIG)
        
        # Success!
        logger.info("\n" + "="*70)
        logger.info("✓ TRAINING COMPLETE!")
        logger.info("="*70)
        logger.info(f"\nModel saved to: {CONFIG['output_dir']}")
        logger.info("To use the model for inference:")
        logger.info(f"  from train_inference import TransformerInference")
        logger.info(f"  inference = TransformerInference('{CONFIG['output_dir']}/best_model')")
        logger.info(f"  response = inference.generate('your query')")
        
        return True
        
    except Exception as e:
        logger.error(f"\n✗ Training failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
